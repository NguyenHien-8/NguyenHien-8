#!/usr/bin/env python3
"""Headless browser visual QA: gallery, 48/64 px, hover, keyboard, motion.

Requires `pip install playwright pillow` and installed system Chrome/Chromium.
Screenshots are test artifacts, never committed to the profile README.
"""
from __future__ import annotations
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
from threading import Thread
from contextlib import contextmanager
import hashlib
import json
import os
import shutil

ROOT=Path(__file__).resolve().parents[1]
OUT=Path(os.environ.get('QA_OUTPUT',ROOT/'.qa'/'screenshots'))
PRIORITY=['git','postman','rest-api','linux','javascript','typescript','rust','next']
IDS=['c','cpp','csharp','go','python','rust','kotlin','next','nodejs','java','typescript','react','html','css','javascript','vue','tensorflow','docker','mysql','postgres','mongodb','graphql','sqlite','git','linux','postman','fastapi','rest-api']

@contextmanager
def serve():
    class Server(ThreadingHTTPServer): allow_reuse_address=True
    class Quiet(SimpleHTTPRequestHandler):
        def log_message(self,*args): pass
    previous=os.getcwd()
    os.chdir(ROOT)
    srv=Server(('127.0.0.1',0),lambda *a,**kw:Quiet(*a,directory=str(ROOT),**kw))
    worker=Thread(target=srv.serve_forever,daemon=True);worker.start()
    try: yield f'http://127.0.0.1:{srv.server_address[1]}/assets/animated/preview.html'
    finally: srv.shutdown();srv.server_close();os.chdir(previous)

def sprites(paths,outfile,per_row=4,label_height=24):
    imgs=[Image.open(p).convert('RGBA') for p in paths]
    width=max(img.width for img in imgs)+12
    height=max(img.height for img in imgs)+label_height+10
    canvas=Image.new('RGB',(per_row*width,((len(imgs)+per_row-1)//per_row)*height),'#101b2b')
    draw=ImageDraw.Draw(canvas)
    for i,img in enumerate(imgs):
        x=i%per_row*width;y=i//per_row*height
        canvas.paste(img,(x+6,y+5),img)
        draw.text((x+8,y+height-label_height),paths[i].stem,fill='#DCE9FC')
    canvas.save(outfile)


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    results={'svg_files':len(list((ROOT/'assets/animated').glob('*.svg'))),'priority_48':[],'priority_64':[],'checks':{}}
    chrome=shutil.which('google-chrome') or shutil.which('chromium') or shutil.which('chromium-browser')
    if not chrome: raise SystemExit('No system browser found')
    with serve() as address, sync_playwright() as pw:
        browser=pw.chromium.launch(executable_path=chrome,headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
        context=browser.new_context(viewport={'width':1300,'height':900},device_scale_factor=1)
        page=context.new_page();page.goto(address,wait_until='networkidle')
        page.locator('.card').first.wait_for(state='visible')
        assert page.locator('.card').count()==28
        assert page.locator('object').count()==28
        loaded=page.evaluate('''() => Array.from(document.querySelectorAll('object')).filter(o => o.contentDocument?.querySelector('.tech-effect')).length''')
        assert loaded==28,f'Only {loaded}/28 interactive SVG objects loaded'
        results['checks']['gallery_objects']='28/28 loaded'
        page.screenshot(path=str(OUT/'gallery-ambient.png'),full_page=True)
        # Search / category interaction and reset
        page.locator('#search').fill('typescript');assert page.locator('.card').count()==1
        page.locator('#search').fill('');page.locator('#category').select_option('Infrastructure')
        assert 2<=page.locator('.card').count()<28
        page.locator('#category').select_option('');assert page.locator('.card').count()==28
        results['checks']['search_filter']='PASS'
        # Native <object> state bridge for pointer and keyboard
        first=page.locator('.card').first
        first.hover()
        assert first.locator('object').evaluate("o=>o.contentDocument.documentElement.classList.contains('is-interactive')")
        first.click(position={'x':10,'y':10})
        first.focus()
        assert first.locator('object').evaluate("o=>o.contentDocument.documentElement.classList.contains('is-interactive')")
        page.keyboard.down('Enter')
        assert first.locator('object').evaluate("o=>o.contentDocument.documentElement.classList.contains('is-active')")
        page.keyboard.up('Enter')
        results['checks']['hover_focus_active']='PASS'
        # Responsive grid at narrow viewport
        page.set_viewport_size({'width':390,'height':820});page.wait_for_timeout(150)
        assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth + 4')
        results['checks']['mobile_overflow']='PASS'
        page.set_viewport_size({'width':1300,'height':900})
        # Take actual-size priority captures and composite tiles
        for size in [48,64]:
            page.locator('#logo-size').select_option(str(size))
            page.wait_for_timeout(120)
            images=[]
            for tech in PRIORITY:
                card=page.locator('.card').filter(has=page.locator(f'object[data="./{tech}.svg"]')).first
                assert card.count()==1,tech
                ob=card.locator('object');box=ob.bounding_box(); assert box and abs(box['width']-size)<1, (tech,size,box)
                output=OUT/f'{tech}-{size}.png'
                ob.screenshot(path=str(output));images.append(output)
            sprites(images,OUT/f'priority-{size}.png')
            results[f'priority_{size}']=PRIORITY
        # In-browser animation time progression check for 8 critical samples.
        # Read pixel hash of screenshot after at least 1.4s; a live SMIL
        # animation should change pixels without any hover dependency.
        changed=[]
        page.locator('#logo-size').select_option('64')
        for tech in PRIORITY:
            ob=page.locator(f'object[data="./{tech}.svg"]').first
            frame1=ob.screenshot()
            page.wait_for_timeout(1600)
            frame2=ob.screenshot()
            changed.append(tech) if hashlib.sha256(frame1).digest()!=hashlib.sha256(frame2).digest() else None
        results['checks']['ambient_motion']=changed
        assert len(changed)>=7,f'Ambient motion not seen in enough priority assets: {changed}'
        # GitHub README uses <img> rather than <object>. Verify that native
        # SVG animation still advances inside an ordinary image element.
        page.evaluate("""() => {
          const img=document.createElement('img');img.id='qa-readme-image';
          img.src='./react.svg';img.width=48;img.height=48;
          Object.assign(img.style,{position:'fixed',right:'12px',top:'12px',background:'#101a29',zIndex:'99999'});
          document.body.appendChild(img);
        }""")
        img=page.locator('#qa-readme-image')
        img.wait_for(state='visible')
        first_img=img.screenshot()
        page.wait_for_timeout(1900)
        second_img=img.screenshot()
        assert hashlib.sha256(first_img).digest()!=hashlib.sha256(second_img).digest(), 'README-style <img> did not animate'
        results['checks']['readme_img_ambient']='PASS (animated at 48 px without hover)'
        page.evaluate("document.querySelector('#qa-readme-image').remove()")
        page.screenshot(path=str(OUT/'gallery-64.png'),full_page=True)
        context.close()
        # Reduced motion: overlays disappear entirely and authentic brand remains.
        reduced=browser.new_context(reduced_motion='reduce',viewport={'width':1300,'height':900})
        pg=reduced.new_page();pg.goto(address,wait_until='networkidle')
        suppressed=pg.evaluate('''() => Array.from(document.querySelectorAll('object')).filter(o => o.contentDocument && getComputedStyle(o.contentDocument.querySelector('.tech-effect')).display === 'none').length''')
        assert suppressed==28,f'{suppressed}/28 effect overlays disabled under reduced-motion'
        pg.screenshot(path=str(OUT/'gallery-reduced-motion.png'),full_page=True)
        results['checks']['reduced_motion']='28/28 hidden overlays'
        reduced.close();browser.close()
    (OUT/'qa-results.json').write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n')
    print('PASS',json.dumps(results['checks'],ensure_ascii=False))

if __name__=='__main__':main()
