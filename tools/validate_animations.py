#!/usr/bin/env python3
"""Validate all authentic SVG brand marks, semantic overlays and accessibility."""
from pathlib import Path
import hashlib
import re
import sys
import xml.etree.ElementTree as ET

BASE = Path(__file__).resolve().parents[1] / 'assets' / 'animated'
IDS = ['c','cpp','csharp','go','python','rust','kotlin','next','nodejs','java','typescript','react','html','css','javascript','vue','tensorflow','docker','mysql','postgres','mongodb','graphql','sqlite','git','linux','postman','fastapi','rest-api']
SVG = '{http://www.w3.org/2000/svg}'
# Filled by the build's original, byte-for-byte SVG brand blocks. Any later
# recolor/path modification of the nested authentic artwork fails validation.
BRAND_SHA256 = {'c': '04f81aa87d225eb7d5ad8ddc99df50b253a0e12e02561b8e4b8bd16695e9f1c3',
 'cpp': '7183a2c6aca2d554fd946959bcebc5299962fb1632cd8b4ab74e432893d6ac8f',
 'csharp': 'f3e0fd8632c0120251f6d1853c5419fb2817b16e5202419827b031f13da78361',
 'css': '17374804cf132f7153bdd5a8f33cce304dfaca5fb3bc4bff46dc37dde0634ea9',
 'docker': 'cc32a6b61f21aadabd20c676937f93930fcb5f7f1ebab01512ec1f1fbd14ccad',
 'fastapi': 'f0b65498a6e61ee48b1ce76d77b00a5af59e702a1d0de016dd68d06070c5ba4d',
 'git': 'adacce1ceff0343d902477866edcb2a3ab54e88cedf6b193baef195c22fa84fa',
 'go': '009fd2a62d1a2284a28bf7ecf4d5f6c7ad776ca84a77ddc74f55862a1315ce34',
 'graphql': 'e73b28d96915c1827224a80088b6b6002234b7ed0dcabbfcc64b2e3cec29d374',
 'html': '182ed3f7693080b2aeb2d58fd646513c4ac4d1134e05d2fea4ac3671e380887a',
 'java': '0529c3c591a4ee7a5b0f6639eb3cbd27117e90de9c932389c09dac086917b938',
 'javascript': 'cea3ec9f04ba21ce0c59affc4b187a31b45f923e269afdb9853e7e1f9f5fd77f',
 'kotlin': 'a558a81c37fc2effb2d528fbf0f7c807823b5d523ae2884b2622b4d5c4534f52',
 'linux': '64f94973726d000c12dd18a42f1ad95f5638c1840368797a6ce6778c8bcb565a',
 'mongodb': '648cb1907ce1552f0c1a435e6762c0ad5d0c39eab689fb1fe74d3ee5bdb6b1da',
 'mysql': '76183b94a2fc0c522ecef6c7c843ac86af03ab5d4a29eb5e0c97320d20338c48',
 'next': 'd137d4cfd5dd9257d565db92cec85d0f08673a6270729e5f2277f06e75b1d810',
 'nodejs': 'e8263b2712f971b520bbaa44a4b2e7b411672e2993ebb1bb31816e356a874978',
 'postgres': '3f893cb96d6e33683dffca8560d2c0431052325462b63140da70f90817d39973',
 'postman': '2910bc523ba090eecdac39c4d13cc0f7424622e07b37a5532d534057f53e5b0d',
 'python': 'c0facecf8a314c751d54e0f5872e192b94c8e3a60bd8352b70c0b6838d8bab83',
 'react': '0f092c80be636cec05f4373289c11f3e12c6919067ef093a9f631cbd2d19d07b',
 'rest-api': 'c412036838086bc0feeab45c0e5cc8e4d5bbe41e8510a03059c599926ed2f238',
 'rust': 'bdac7bb878ce77100d116791a1769f1f8c769877b25cb517fbd4dbf1a7d46aa8',
 'sqlite': '214fa0f6012083efcce5d2f3f674691b652b6540b401785a63703d4f62f04d46',
 'tensorflow': '2a0c374e5a8f7660881494895d6f04f7a2dbdca22e040c4dffc723086bcf628d',
 'typescript': '02180a71d023b1e2b7531b8512efa79814fb43bea3f988244108351694a3e1f7',
 'vue': '0d580256f042ed33d55586f280120f5f32a674056f8efe58a69091bcd24086ef'}
errors=[]
svg_names={p.stem for p in BASE.glob('*.svg')}
if svg_names!=set(IDS):
    errors.append(f'Expected exactly 28 SVGs: missing {sorted(set(IDS)-svg_names)}, extra {sorted(svg_names-set(IDS))}')
descriptions=set()
for name in IDS:
    source_path=BASE / (name+'.svg')
    if not source_path.exists(): continue
    source=source_path.read_text('utf-8')
    try: root=ET.fromstring(source)
    except ET.ParseError as err:
        errors.append(f'{name}: invalid XML: {err}');continue
    if root.tag!=SVG+'svg' or root.get('viewBox')!='0 0 64 64' or root.get('width')!='64' or root.get('height')!='64':
        errors.append(f'{name}: root must retain 64x64 dimensions and viewBox')
    brands=[node for node in root.iter(SVG+'svg') if node is not root]
    overlays=[node for node in root if node.tag==SVG+'g' and node.get('class')=='tech-effect']
    if len(brands)!=1 or len(overlays)!=1:
        errors.append(f'{name}: expected one authentic nested logo and one separate tech-effect');continue
    brand=brands[0]
    marker=source.find('<svg',source.find('</desc>')+7)
    end=source.find('</svg>',marker)+6
    if marker<0 or end<6 or hashlib.sha256(source[marker:end].encode('utf-8')).hexdigest()!=BRAND_SHA256[name]:
        errors.append(f'{name}: original nested brand artwork has been modified')
    desc=root.find(SVG+'desc')
    desc_text=(desc.text or '').strip() if desc is not None else ''
    if not desc_text or desc_text in descriptions:
        errors.append(f'{name}: missing or reused semantic description')
    descriptions.add(desc_text)
    style=root.find(SVG+'style')
    css=style.text or '' if style is not None else ''
    if ':root:hover' not in css or 'is-interactive' not in css or 'prefers-reduced-motion:reduce' not in css or '.tech-effect{display:none' not in css:
        errors.append(f'{name}: missing hover/focus bridge or reliable reduced-motion suppression')
    animations=[n for n in overlays[0].iter() if n.tag in {SVG+'animate',SVG+'animateMotion',SVG+'animateTransform'}]
    if not animations: errors.append(f'{name}: technical overlay has no native motion')
    if name=='react':
        motions=list(overlays[0].iter(SVG+'animateMotion'))
        if len(motions)!=6 or any('21.875 8.34' not in (m.get('path') or '') for m in motions):
            errors.append('react: expected exactly three precisely aligned elliptical electron+halo pairs')
    else:
        if 'electron' in desc_text.lower() or any('21.875 8.34' in (m.get('path') or '') for m in overlays[0].iter(SVG+'animateMotion')):
            errors.append(f'{name}: only React may have Electron Orbit')
    for node in root.iter():
        if node.tag.rsplit('}',1)[-1] in {'script','foreignObject','image'}:
            errors.append(f'{name}: disallowed embedded node {node.tag}')
        for key,value in node.attrib.items():
            if key.endswith('href') or any(token in value.lower() for token in ('javascript:','http://','https://')):
                errors.append(f'{name}: disallowed external reference')
if errors:
    print('\n'.join('FAIL: '+err for err in errors),file=sys.stderr)
    sys.exit(1)
print(f'PASS: {len(IDS)}/28 original brand hashes; distinct SVG overlays; exact React ellipses; hover bridge; reduced motion.')
