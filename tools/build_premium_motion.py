#!/usr/bin/env python3
"""Build 28 self-contained, differentiated SVG tech mini-visualizations.

Preserves the original nested brand markup verbatim. The original brand layout is
uniformly scaled only for the composition; no SVG path, fill or brand attribute
inside that nested SVG is rewritten.
"""
from __future__ import annotations
from pathlib import Path
from html import escape
import re

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'assets'/'animated'
NAMES=['c','cpp','csharp','go','python','rust','kotlin','next','nodejs','java','typescript','react','html','css','javascript','vue','tensorflow','docker','mysql','postgres','mongodb','graphql','sqlite','git','linux','postman','fastapi','rest-api']
# composed by moving the complete intact brand artwork; never change the paths.
LAYOUT={
    'top':'translate(9 0) scale(.72)',
    'bottom':'translate(9 16) scale(.72)',
    'left':'translate(17 8) scale(.72)',
    'right':'translate(0 8) scale(.72)',
    'center':'translate(0 0) scale(1)'
}

DUR='5.6s'
def t(x,y,s,color='#EAF7FF',size=6,weight=600,**more):
    extra=' '.join(f'{k.replace("_","-")}="{v}"' for k,v in more.items())
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="{size}" font-weight="{weight}" {extra}>{escape(s)}</text>'
def p(d,col='#E0EDFF',w=1.35,extra=''):
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'
def r(x,y,w,h,color='#EAF7FF',fill='none',radius=1.6,extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{color}" stroke-width="1.1" {extra}/>'
def c(x,y,rad=1.8,fill='#DDF8FF',extra=''):
    return f'<circle cx="{x}" cy="{y}" r="{rad}" fill="{fill}" {extra}/>'
def a(attr,values,dur=DUR,times=None,begin='0s',repeat='indefinite'):
    return f'<animate attributeName="{attr}" values="{values}" dur="{dur}" begin="{begin}"'+(f' keyTimes="{times}"' if times else '')+f' repeatCount="{repeat}"/>'
def motion(path,dur=DUR,begin='0s'):
    return f'<animateMotion path="{path}" dur="{dur}" begin="{begin}" calcMode="paced" repeatCount="indefinite"/>'
def reveal(begin, dur=DUR, peak='1'):
    return a('opacity',f'0;0;{peak};{peak};0',dur,'0;.24;.44;.82;1',begin)
def drawpath(d,color,length,dur=DUR,begin='0s',w=1.3):
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-dasharray="{length}" stroke-dashoffset="{length}">'+a('stroke-dashoffset',f'{length};{length};0;0;{length}',dur,'0;.12;.56;.85;1',begin)+'</path>'
def panel(x,y,w,h,accent='#A2BDDD',fill='#071320',alpha='.90'):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3.1" fill="{fill}" fill-opacity="{alpha}" stroke="{accent}" stroke-opacity=".74" stroke-width=".85"/>'
def seg(x,y,w,color='#D3EEFF'):
    return f'<rect x="{x}" y="{y}" width="{w}" height="1.7" rx=".85" fill="{color}"/>'
def chip(x,y,text,color='#BFEFFF',bg='#142B3E',size=5.4):
    width=max(11,len(text)*size*.57+4)
    return f'<rect x="{x}" y="{y-size+0.5}" width="{width:.2f}" height="{size+3}" rx="2" fill="{bg}" stroke="{color}" stroke-opacity=".5" stroke-width=".65"/>'+t(x+2,y+1,text,color,size,700)

# Each SVG is authored for its own visual concept. Every vignette combines
# a readable persistent technical diagram and an ordered purpose-specific cycle.
FX={}
# 1 C: 8-bit memory register under real bus / addressing lines
FX['c']=('left','Low-level register addressing and instruction decode',lambda: (
 panel(2,13,27,39,'#B7CFFF')+t(5,20,'0x1F','#D5E4FF',5.4)+
 p('M5 25H25M5 42H25','#C4D7FF',.85)+
 ''.join(r(5+i*2.7,29,2.3,7,'#C9DDFF','#2B468A',.5,extra='stroke-opacity=".72"') for i in range(8))+
 ''.join(f'<rect x="{5+i*2.7:.1f}" y="30" width="2.3" height="5" rx=".4" fill="#FFFFFF" opacity="0">'+a('opacity','0;0;1;0;0',f'{3.2+i*.12:.1f}s', '0;.24;.52;.75;1',f'-{i*.39:.2f}s')+'</rect>' for i in range(8))+
 t(5,49,'R0 → R1','#DBE8FF',5.2)+
 p('M5 54H25','#80E6FF',1.4)+c(25,54,2,'#75F2FF')
 ))
# 2 C++: SIMD lanes and performance funnel
FX['cpp']=('top','Parallel vector execution with an explicit synchronization barrier',lambda: (
 panel(4,3,56,19,'#A9E3FF')+t(7,9,'SIMD','#D8F3FF',5.3)+
 ''.join(p(f'M{9} {12+i*3.3:.1f}H49','#B4EBFF',1.05) for i in range(3))+
 ''.join(f'<rect x="10" y="{11+i*3.3:.1f}" width="5" height="1.6" rx=".8" fill="#FFFFFF">'+a('x','10;44;10',f'{1.7+i*.2:.1f}s','0;.82;1',f'-{i*.31:.1f}s')+'</rect>' for i in range(3))+
 p('M50 11V20','#FFFFFF',2)+t(53,19,'✓','#9CFDE7',6.3)
 ))
# 3 C#: module boxes and typed dependency graph
FX['csharp']=('right','Component contracts are linked through a dependency architecture',lambda: (
 panel(35,8,27,48,'#F0C3FF')+
 ''.join(r(x,y,10,8,'#F7D6FF','#402344',1.6) for x,y in [(39,13),(39,28),(39,43)])+
 p('M44 21V28M44 36V43','#E9BDFF',1.3)+
 ''.join(t(42,y,s,'#FFFFFF',5.6) for y,s in [(19,'A'),(34,'B'),(49,'C')])+
 drawpath('M44 21V28V43','#FFFFFF',23,'5.9s',w=1.75)+
 c(55,17,2,'#EBC7FF')+p('M49 17H55','#DEC1FF',1.2)
 ))
# 4 Go: goroutine lanes converge at sync barrier
FX['go']=('top','Three goroutines converge at a channel synchronization point',lambda: (
 panel(3,3,58,19,'#BDFBFF')+
 ''.join(p(f'M7 {8+i*5}H38L45 13','#CAFCFF',1.05) for i in range(3))+
 ''.join(f'<rect x="9" y="{6.7+i*5}" width="5.2" height="2.6" rx="1.2" fill="#FFFFFF">'+a('x','9;34;9','3.0s','0;.8;1',f'-{i*.35}s')+'</rect>' for i in range(3))+
 p('M46 6V20','#F4FFFF',1.8)+chip(48,17,'sync','#E6FFFF','#065B73',4.8)
 ))
# 5 Python: interpreter transforms list to result in three directed phases
FX['python']=('right','An interpreter transforms parsed input through evaluation to output',lambda: (
 panel(35,8,27,49,'#9BCFF9')+
 chip(39,16,'input','#D2E8FF','#183650',4.6)+
 t(40,25,'[1,2]','#E5F1FF',5.4)+p('M47 27v7m-3-3 3 3 3-3','#A3DEFF',1.1)+
 chip(39,42,'eval','#F9DC79','#3C3820',4.6)+
 t(43,51,'3','#FFDF76',8.2,700)+
 r(40,44,13,10,'#FFE38C','none',1.1,extra='stroke-opacity="0"')+
 '<circle cx="56" cy="49" r="2" fill="#FFE4A0">'+reveal('-.5s')+'</circle>'
 ))
# 6 Rust: two scopes, move and immutable borrow returned
FX['rust']=('left','Owner value moves A→B; immutable borrow returns safely',lambda: (
 panel(2,6,29,53,'#FFD0A9')+
 t(5,14,'OWN / &','#FFE3CE',5.5)+
 r(5,18,22,14,'#F7C7A7','#361F18',1.8)+r(5,38,22,14,'#F7C7A7','#361F18',1.8)+
 t(7,24,'A','#FFEDE3',5.4)+t(7,44,'B','#FFEDE3',5.4)+
 p('M23 32V38l-2-2m2 2 2-2','#FFE4CC',1.1)+
 '<rect x="15" y="22" width="7" height="6" rx="1" fill="#F6AB71">'+a('y','22;22;42;42;22','6.8s','0;.23;.5;.8;1')+'</rect>'+
 p('M10 48C4 48 4 29 10 29','#E2F8E4',1.25)+
 t(14,49,'&','#D4FFE5',7.3,700)+
 '<circle cx="24" cy="56" r="2.5" fill="#A8FFE0">'+reveal('-.8s','6.8s')+'</circle>'+
 p('M22 56l2 2 3-4','#163D31',.9)
 ))
# 7 Kotlin coroutine structured suspend-resume & two tone ribbons
FX['kotlin']=('top','Coroutine flow suspends then resumes across a gradient transition',lambda: (
 panel(3,3,58,19,'#D0A4FF')+
 '<defs><linearGradient id="kor-flow"><stop stop-color="#FE8C5A"/><stop offset=".5" stop-color="#E16BE6"/><stop offset="1" stop-color="#8B75FF"/></linearGradient></defs>'+
 p('M7 11Q23 5 34 14T56 11','url(#kor-flow)',2.4)+
 p('M7 17Q23 23 34 12T56 17','#F0C0FF',1.4,extra='stroke-opacity=".6"')+
 r(27,7,10,13,'#F3D2FF','#2C2147',1.4)+t(28.5,15,'II','#E8DAFF',6.2)+
 '<circle r="2" fill="#FFFFFF">'+motion('M7 11Q23 5 34 14T56 11','5.6s')+'</circle>'
 ))
# 8 Next.js: server request, selected route, SSR render document
FX['next']=('top','Request passes through a router, selects a page and renders HTML',lambda: (
 panel(2,2,60,23,'#DDEAFF')+
 r(5,8,9,11,'#C4D3E1','#1A2430',1.2)+t(6,14,'GET','#FFFFFF',4.3)+
 p('M14 13H20','#F0F7FF',1.4)+
 '<path d="M24 7l5 6-5 6-5-6z" fill="#263747" stroke="#F8FBFF" stroke-width="1.2"/>'+
 p('M29 13H34V8H42M34 13v7h8','#B2CDE2',1.0)+
 r(40,4,11,7,'#97B5D6','#152431',.8)+t(41,9,'/app','#DDF0FF',4.1)+
 r(40,16,11,7,'#97B5D6','#152431',.8)+t(41,21,'/doc','#DDF0FF',4.1)+
 p('M51 19H55','#F8FFFF',1.3)+
 '<rect x="55" y="9" width="5" height="12" rx="1" fill="#E9F4FF">'+a('height','1;12;12;1','6.5s','0;.45;.81;1')+'</rect>'+
 drawpath('M13 13H20L24 13H34V19H40','#FFFFFF',32,'6.5s',w=1.7)
 ))
# 9 Node.js: task queue / event loop / callback stage, not orbit
FX['nodejs']=('right','FIFO task queue feeds an event-loop dispatch and callback',lambda: (
 panel(36,7,26,51,'#B5F6A0')+
 t(39,15,'QUEUE','#D6FFCE',5.2)+
 ''.join(r(39+i*7,18,6,7,'#C4FDA8','#294A26',.8) for i in range(3))+
 r(40,32,20,10,'#C6F4A2','#1E3C24',2)+t(42,39,'LOOP','#E6FFDD',6)+
 p('M50 25V32M50 42V47','#B0F68D',1.2)+
 chip(40,53,'CB','#DAFFCA','#294529',5)+
 ''.join(f'<rect x="{40+i*7}" y="19" width="4.5" height="5" rx=".8" fill="#D8FFAE" opacity=".25">'+reveal(f'-{i*.64}s','4.5s')+'</rect>' for i in range(3))+
 r(41,33,18,8,'#FFFFFF','none',1.4,extra='stroke-dasharray="6 7"')
 ))
# 10 Java: JVM bytecode decode and stack push/pop
FX['java']=('left','JVM executes bytecode by pushing and popping stack frames',lambda: (
 panel(2,8,29,51,'#F8C4A9')+
 chip(5,16,'JVM','#FFE1CF','#38251C',5)+
 r(6,22,21,29,'#E9B9A6','#1B2733',1.8)+
 ''.join(r(8,41-i*7,17,5,'#FFD5B0','#3A4D5A',.6) for i in range(3))+
 t(11,32,'PC','#FFE2C5',4.8)+
 '<rect x="8.4" y="42" width="16.2" height="4.2" rx=".5" fill="#FFBC86" opacity=".85">'+a('y','42;35;28;42','5.3s','0;.35;.7;1')+'</rect>'+
 t(7,56,'push/pop','#EED8C5',5)
 ))
# 11 TypeScript: typed source -> checker -> JS emit
FX['typescript']=('top','Compile-time typed declaration passes validation before emitting JavaScript',lambda: (
 panel(2,2,60,25,'#B6D7FF')+
 t(5,10,'let n:','#EEF6FF',5.3)+t(5,17,'number','#93C7FF',5.7)+t(29,17,'=20','#FFFFFF',5.7)+
 p('M36 14H41','#C8E3FF',1.2)+r(41,8,11,12,'#D1E8FF','#194B80',1.3)+t(42,16,'TS','#FFFFFF',5.6)+
 r(54,8,7,12,'#C6E3FF','#194B80',1.2)+'<text x="54.8" y="16" font-size="6.4" fill="#B2FFDE" opacity="0">✓'+reveal('-.3s','5.8s')+'</text>'+
 '<path d="M44 21h7" stroke="#AEFFDF" stroke-width="1.6" stroke-linecap="round"/>'+
 '<path d="M43 16l3 2 5-6" fill="none" stroke="#B6FFE2" stroke-width="1.5" opacity="0">'+reveal('0s','5.8s')+'</path>'+
 t(53,24,'JS','#C6E5FF',5.4)
 ))
# 12 React (no compositional scaling, true ellipses matching brand)
def react_orbit(deg,speed,reverse=False):
    ellipse='M10.14 32.06A21.875 8.34 0 1 '+('1' if reverse else '0')+' 53.89 32.06A21.875 8.34 0 1 '+('1' if reverse else '0')+' 10.14 32.06'
    return f'<g transform="rotate({deg} 32.06 32.06)"><circle cx="10.14" cy="32.06" r="2.7" fill="#70E6FF" opacity=".14" filter="url(#electron-halo)">'+motion(ellipse,speed)+'</circle><circle cx="10.14" cy="32.06" r="1.35" fill="#E7FAFF">'+motion(ellipse,speed)+'</circle></g>'
FX['react']=('center','Three calibrated elliptic electron trajectories aligned to the official React atom',lambda: (
 '<defs><filter id="electron-halo" x="-150%" y="-150%" width="400%" height="400%"><feGaussianBlur stdDeviation=".8"/></filter></defs>'+
 '<g class="moving">'+react_orbit(0,'5.4s')+react_orbit(60,'6.8s',True)+react_orbit(-60,'7.9s')+'</g>'+
 '<g class="hover-detail" fill="none" stroke="#84EFFF" stroke-opacity=".32" stroke-width=".5"><ellipse cx="32.06" cy="32.06" rx="21.875" ry="8.34"/><ellipse cx="32.06" cy="32.06" rx="21.875" ry="8.34" transform="rotate(60 32.06 32.06)"/><ellipse cx="32.06" cy="32.06" rx="21.875" ry="8.34" transform="rotate(-60 32.06 32.06)"/></g>'
 ))
# 13 HTML: DOM tree with element nodes building in document order
FX['html']=('left','A document tree expands from html to head/body elements',lambda: (
 panel(2,7,29,49,'#FFD6BB')+
 chip(5,15,'DOM','#FFE3D1','#653822',5.1)+
 r(11,19,13,7,'#FFD4C1','#542D20',1.0)+t(13,24,'html','#FFE7D7',4.9)+
 p('M17.5 26V31H9V34M17.5 31H25V34','#FFDFCE',1.15)+
 r(4,34,12,8,'#FFD2B9','#592E20',1)+t(5.5,40,'head','#FFE7D7',4.3)+
 r(18,34,12,8,'#FFD2B9','#592E20',1)+t(19.5,40,'body','#FFE7D7',4.3)+
 drawpath('M17.5 26V31H9V34M17.5 31H25V34','#FFFFFF',35,'6.2s')+
 ''.join(f'<rect x="{x}" y="45" width="{w}" height="2" rx="1" fill="#FFE8DA" opacity=".7"/>' for x,w in [(5,10),(19,10)])
 ))
# 14 CSS: cascade of overlapping style layers plus applied swatch
FX['css']=('right','Cascade resolves overlapping rules into a computed visual style',lambda: (
 panel(36,7,26,49,'#B5E1FF')+
 ''.join(f'<rect x="{38+i*3}" y="{14+i*5}" width="{17-i*1.5}" height="18" rx="2" fill="{cl}" fill-opacity=".17" stroke="{cl}" stroke-width="1.05"/>' for i,cl in enumerate(['#9ACDFF','#70B6F8','#A999FF']))+
 t(40,12,'CSS','#D5EBFF',5.5)+
 r(41,44,17,8,'#D2ECFF','#29496C',1.5)+
 '<rect x="44" y="46" width="11" height="4" rx="1" fill="#A7D2FF">'+a('fill','#9FCFFF;#AA91FF;#7EE2E7;#9FCFFF','5.6s')+'</rect>'+
 p('M45 38H56','#A8E3FF',1.2)
 ))
# 15 JS: runtime expression evaluation and resulting value (not type checking)
FX['javascript']=('right','The JavaScript runtime evaluates 5 + 10 into its result',lambda: (
 panel(37,7,25,50,'#FFE37F','#141410')+
 chip(40,15,'RUN','#FFE97F','#4E461C',5.1)+
 t(40,26,'5+10','#FFE758',7.4)+
 p('M40 30H58','#FCE56B',1.5)+
 '<rect x="40" y="31" width="6" height="2.2" rx="1.1" fill="#FFDF4D">'+a('x','40;52;40','4.5s','0;.6;1')+'</rect>'+
 '<text x="42" y="44" fill="#FFFFFF" font-family="monospace" font-size="11.4" font-weight="800" opacity="0">15'+reveal('-.4s','4.5s')+'</text>'+
 r(40,37,18,12,'#FFF19C','none',2,extra='stroke-opacity=".3"')+
 t(42,54,'OUT','#FFE785',5.2)
 ))
# 16 Vue: reactive data propagation: source, computed, view
FX['vue']=('bottom','Reactive source propagates via computed state into an updated view',lambda: (
 panel(3,39,58,23,'#B1F8D8')+
 chip(6,46,'state','#C9FFE7','#1B4938',5)+chip(25,46,'calc','#C9FFE7','#1B4938',5)+chip(45,46,'view','#C9FFE7','#1B4938',5)+
 p('M12 50H51','#A0FBD1',1.05)+
 ''.join(f'<rect x="{x}" y="53" width="{w}" height="4" rx="1" fill="#79F4C7" opacity=".35">'+reveal(f'-{i*.75}s','5.9s')+'</rect>' for i,(x,w) in enumerate([(8,10),(28,10),(48,9)]))+
 c(10,58,1.3,'#C9FFE7')+c(50,58,1.3,'#C9FFE7')
 ))
# 17 TensorFlow: weighted 3-layer net with activations
FX['tensorflow']=('right','A weighted neural net processes inputs across three inference layers',lambda: (
 panel(34,7,28,52,'#FFD9A1')+
 ''.join(p(f'M{xa} {ya}L{xb} {yb}','#D6AB67',.8,extra='stroke-opacity=".62"') for xa,ya,xb,yb in [(39,19,47,15),(39,19,47,26),(39,35,47,15),(39,35,47,26),(47,15,56,22),(47,26,56,22)])+
 ''.join(c(x,y,2.2,'#FFE4B7',extra='stroke="#704925" stroke-width=".7"') for x,y in [(39,19),(39,35),(47,15),(47,26),(56,22)])+
 ''.join(f'<circle cx="{x}" cy="{y}" r="3.5" fill="#FFBE73" opacity="0">'+reveal(f'-{i*.65}s','4.7s')+'</circle>' for i,(x,y) in enumerate([(39,19),(47,15),(56,22)]))+
 t(40,49,'INFER','#FFE0AA',5.2)+seg(40,53,18,'#FFD28F')
 ))
# 18 Docker: build image layers then container RUN state
FX['docker']=('bottom','Image layers stack into a container and transition to RUN',lambda: (
 panel(3,39,58,23,'#B5EBFF')+
 ''.join(r(7,53-i*5,25,4,'#A6E1FF','#2A6485',.7) for i in range(3))+
 '<rect x="7" y="43" width="25" height="4" rx=".7" fill="#CAEFFD" opacity=".72">'+a('y','53;48;43;43;53','5.6s','0;.2;.42;.82;1')+'</rect>'+
 p('M34 50H43l-3-3m3 3-3 3','#C5F1FF',1.2)+
 r(44,43,13,14,'#A5DFFF','#1D4F6B',1.6)+t(46,52,'RUN','#E5FAFF',5)+
 '<circle cx="54" cy="45" r="2" fill="#8DFFE1">'+reveal('-.6s','5.6s')+'</circle>'
 ))
# 19 MySQL: query planner table scan, cursor lands on matching row
FX['mysql']=('right','SQL SELECT scans table rows and returns matching tuples',lambda: (
 panel(35,8,27,50,'#ADD8EF')+
 t(38,15,'SELECT','#DFF2FF',5.0)+
 r(38,19,21,27,'#C9E5F7','#1E3447',1.2)+
 ''.join(p(f'M38 {y}H59','#B1D8F1',.9) for y in (25,31,37))+
 p('M46 19V46','#A5C6DF',.8)+
 '<rect x="39" y="25.5" width="19" height="5" rx=".7" fill="#F1CE8A" fill-opacity=".72">'+a('y','26;32;38;26','6.2s','0;.3;.65;1')+'</rect>'+
 chip(38,54,'rows','#D4EBF8','#2A4259',4.8)
 ))
# 20 PostgreSQL: transaction ACID ordered phases
FX['postgres']=('bottom','ACID transaction progresses BEGIN, WRITE, COMMIT and confirmation',lambda: (
 panel(3,39,58,23,'#BFD9F6')+
 ''.join(r(x,45,15,12,'#A5C8EB','#263D56',1.5) for x in [6,25,44])+
 t(8,52,'BEGIN','#DDEBFF',4.6)+t(27,52,'WRITE','#DDEBFF',4.6)+t(46,52,'COMMIT','#DDEBFF',4.3)+
 p('M21 50h4m15 0h4','#E2F0FF',1.2)+
 ''.join(f'<rect x="{x}" y="55" width="{15}" height="1.5" rx=".8" fill="#93D6FF" opacity=".2">'+reveal(f'-{i*.95}s','6.6s')+'</rect>' for i,x in enumerate([6,25,44]))+
 '<circle cx="57" cy="41" r="2" fill="#B5FFD2">'+reveal('-1s','6.6s')+'</circle>'
 ))
# 21 MongoDB: document store JSON records plus selected document expansion
FX['mongodb']=('top','JSON-style documents stack; a selected document opens and returns',lambda: (
 panel(4,3,56,20,'#A5E5B0')+
 ''.join(r(x,6,12,14,'#A3E4BB','#173F32',1.3) for x in (8,23,38))+
 ''.join(t(x+2,15,'{}','#D6FFDA',7.0) for x in (8,23,38))+
 '<rect x="23" y="6" width="12" height="14" rx="1.3" fill="#A5E9B5" fill-opacity=".19" stroke="#C5FFD3" stroke-width="1">'+a('width','12;18;18;12','5.7s','0;.34;.66;1')+'</rect>'+
 t(50,16,'DB','#D3FFDC',5.4)
 ))
# 22 GraphQL: sparse selective graph traversal, unrelated remains dim
FX['graphql']=('top','A typed graph query follows only selected field nodes',lambda: (
 panel(4,2,56,23,'#FFC5EB')+
 ''.join(p(path,'#F4A6D8',.9,extra='stroke-opacity=".38"') for path in ('M9 14L26 7L44 13L55 7','M26 7L30 22L44 13','M9 14L30 22L55 7'))+
 ''.join(c(x,y,2.2,'#F4A6D8',extra=f'opacity="{0.9 if i in (0,1,3) else .4}"') for i,(x,y) in enumerate([(9,14),(26,7),(30,22),(44,13),(55,7)]))+
 drawpath('M9 14L26 7L44 13','#FFFFFF',44,'5.4s',w=1.8)+
 t(36,22,'QUERY','#FFE8F7',5.0)
 ))
# 23 SQLite: chip with memory cells and read/write arrows
FX['sqlite']=('left','An embedded database writes then reads a local flash-memory region',lambda: (
 panel(2,7,29,51,'#BDE8FF')+
 r(7,16,19,29,'#D1EAFF','#1B4E76',1.5)+
 ''.join(r(10+i*4.4,20+j*5.2,3.5,3.7,'#B8DFFD','#265C80',.4) for i in range(3) for j in range(4))+
 p('M4 49H28','#DEF7FF',1.15)+
 t(5,56,'R / W','#D6EFFF',5.4)+
 '<rect x="10" y="20" width="3.5" height="3.7" rx=".4" fill="#FAF0C0">'+a('x','10;14.4;18.8;10','5.8s','0;.34;.68;1')+'</rect>'
 ))
# 24 Git: structurally correct branch graph, commits & merge
FX['git']=('bottom','A clean commit DAG: main branch, feature divergence, commits and merge',lambda: (
 panel(3,38,58,24,'#FFE7DC')+
 p('M8 55H56','#FFCEB8',1.5)+
 p('M18 55C24 55 23 45 30 45H41C48 45 46 55 52 55','#69B0DD',1.15,extra='stroke-opacity=".72"')+
 drawpath('M18 55C24 55 23 45 30 45H41C48 45 46 55 52 55','#99D7FF',48,'6.5s',w=1.8)+
 ''.join(c(x,55,2.0,'#FFE7D5',extra='stroke="#B95437" stroke-width=".85"') for x in (10,18,54))+
 ''.join(f'<circle cx="{x}" cy="45" r="2.1" fill="#C3EAFF" stroke="#2274A5" stroke-width=".8" opacity="0">'+reveal(f'-{i*.65}s','6.5s')+'</circle>' for i,x in enumerate((30,36,41)))+
 '<circle r="1.5" fill="#FFFFFF">'+motion('M18 55C24 55 23 45 30 45H41C48 45 46 55 52 55','6.5s')+'</circle>'+
 p('M55 49v3m-2-2 2 2 3-4','#A8FFDD',1.3,extra='opacity=".45"')+
 t(7,43,'main','#FFE6D4',4.7)+t(7,50,'feat','#BBE4FF',4.7)
 ))
# 25 Linux: authentic single terminal frame, command -> output
FX['linux']=('bottom','A true terminal prompt types ls and displays a directory listing',lambda: (
 panel(3,37,58,26,'#FFDFA3','#071015',alpha='.98')+
 '<rect x="3" y="37" width="58" height="6" rx="2" fill="#273744"/>'+
 ''.join(c(8+i*4.2,40,1.0,fill) for i,fill in enumerate(['#FF817A','#EACF71','#83E3B1']))+
 t(7,51,'$','#BEF7CB',7.8)+
 ''.join(f'<text x="{x}" y="51" font-family="monospace" font-size="7.5" font-weight="600" fill="#F2F5F8" opacity="0">{v}'+a('opacity','0;1;1;0','5.9s','0;.22;.84;1',f'-{i*.5:.1f}s')+'</text>' for i,(x,v) in enumerate([(16,'l'),(21,'s')]))+
 '<rect x="27" y="45" width="2.2" height="8" fill="#D8EAF0">'+a('opacity','1;0;1','1.15s')+'</rect>'+
 '<text x="7" y="59" font-family="monospace" font-size="5.3" fill="#B9DDE5" opacity="0">src/  app/  tests/'+reveal('-1.6s','5.9s')+'</text>'
 ))
# 26 Postman: method + request editor + response body + status, not generic endpoints
FX['postman']=('bottom','Two-panel HTTP testing console with GET, request, response and 200 status',lambda: (
 panel(2,37,60,26,'#FFBD93')+
 r(5,42,23,17,'#FFD0AF','#39221B',1.7)+r(36,42,23,17,'#FFD0AF','#302620',1.7)+
 chip(7,49,'GET','#FFFFFF','#E36E35',4.8)+
 p('M6 53H26M6 56H20','#DDA98F',.9)+
 t(38,47,'RESP','#F3DECA',5.5)+
 p('M39 53H55M39 56H49','#FFD9B6',.9)+
 '<rect x="47" y="50" width="10" height="7" rx="1.3" fill="#14583F" opacity="0">'+reveal('-.75s','6.6s')+'</rect>'+
 '<text x="48" y="55.5" font-family="monospace" font-size="5.6" font-weight="700" fill="#B2FFE0" opacity="0">200'+reveal('-.75s','6.6s')+'</text>'+
 p('M28 47H35l-2-2m2 2-2 2','#FFD1BA',1.1)+p('M35 56H28l2-2m-2 2 2 2','#9FCFFF',1.1)+
 '<rect x="29" y="45.9" width="4" height="2.2" rx="1" fill="#FFB174">'+a('x','29;33;33;29','6.6s','0;.28;.54;1')+'</rect>'
 ))
# 27 FastAPI: endpoint mapping then serialized JSON response
FX['fastapi']=('right','An endpoint router matches GET /v1 and serializes a fast JSON reply',lambda: (
 panel(35,7,27,51,'#A5FFEB')+
 chip(39,15,'GET','#D6FFF4','#164B48',5)+
 t(39,23,'/v1','#DEFFF8',7.0)+
 p('M39 27H57M48 27V32','#A9EEE0',1.15)+
 r(40,33,17,10,'#BBFFF0','#174A48',1.6)+t(42,40,'200','#C5FFE8',6.6)+
 t(39,52,'{ ok }','#E4FFF7',6.1)+
 '<rect x="40" y="46" width="16" height="1.7" rx=".85" fill="#A0FFE7">'+a('width','0;16;16;0','3.8s','0;.3;.83;1')+'</rect>'
 ))
# 28 REST: conceptual topology, client vs server with two independent packet shapes
FX['rest-api']=('bottom','Client/server topology with distinct request and response packets',lambda: (
 panel(2,38,60,24,'#A6E6DD')+
 r(5,43,17,15,'#B0EDE6','#153E49',2)+r(42,43,17,15,'#C4DFFC','#24405D',2)+
 t(7,49,'CLIENT','#D5FCF3',4.6)+t(43,49,'SERVER','#D9EAFE',4.2)+
 r(9,52,9,3,'#D9F9F1','#1A3C44',.7)+
 ''.join(r(45+i*4,52,3,3,'#D7EAFF','#284B64',.4) for i in range(3))+
 p('M23 46H41M41 55H23','#BDEBF5',1.3)+
 '<path d="M24 44l5 2-5 2z" fill="#A8FFEC">'+a('transform','translate(0 0);translate(11 0);translate(11 0);translate(0 0)','6.7s','0;.33;.8;1')+'</path>'+
 '<rect x="35" y="53.5" width="5" height="2.5" rx=".7" fill="#C7E0FF">'+a('x','35;35;24;35','6.7s','0;.36;.77;1')+'</rect>'+
 '<rect x="48" y="39" width="4" height="2" rx=".65" fill="#9FE5FF" opacity="0">'+reveal('-.5s','6.7s')+'</rect>'
 ))


# Every hover reveals a DIFFERENT semantic state, rather than merely raising opacity.
# The parent gallery forwards pointer/keyboard state into the SVG root.
HOVER={
 'c':t(5,27,'BUS','#E3F4FF',4.4),
 'cpp':chip(52,8,'x4','#A2FFE9','#134A60',4.2),
 'csharp':p('M49 46H55V18','#FFF4FF',1.1),
 'go':c(46,13,3,'#AAFFEB')+t(47,9,'3','#E5FFFF',4.8),
 'python':t(40,56,'int','#FFEC98',4.8),
 'rust':t(6,56,'SAFE','#C1FFDD',4.7),
 'kotlin':t(46,9,'resume','#F5DCFF',4.2),
 'next':t(51,24,'SSR','#F6FFFF',4.2),
 'nodejs':t(40,58,'CALL','#D7FFC4',4.4),
 'java':t(10,19,'BC','#FFE4C9',5),
 'typescript':p('M38 6h12','#A4FFE2',1.8),
 'html':t(5,52,'TREE','#FFE2D3',4.6),
 'css':t(40,59,'APPLY','#D4EEFF',4.4),
 'javascript':p('M39 47h20','#FFEE82',1.3),
 'vue':t(10,61,'reactive','#DBFFEF',4.3),
 'tensorflow':t(37,58,'CLASS','#FFE5C5',4.3),
 'docker':t(45,61,'ready','#CEFFED',4.6),
 'mysql':t(38,59,'1 MATCH','#D8F0FF',4.2),
 'postgres':t(47,60,'ACID','#D5F0FF',4.6),
 'mongodb':t(45,22,'json','#D3FFE5',4.2),
 'graphql':p('M44 13L55 7','#FFAEE7',2),
 'sqlite':t(6,12,'LOCAL','#D9F4FF',4.8),
 'git':p('M53 48l2 2 3-4','#B8FFE4',1.6),
 'linux':t(54,59,'✓','#9BFFE2',6.1),
 'postman':t(7,61,'TEST','#FFDDC8',4.4),
 'fastapi':t(38,57,'3ms','#C3FFED',5.3),
 'rest-api':p('M47 51v4M50 51v4M53 51v4','#95DEFF',1.3)
}
assert set(HOVER)==set(NAMES)-{'react'}

assert set(FX)==set(NAMES),(set(NAMES)-set(FX),set(FX)-set(NAMES))

STYLE='''<style><![CDATA[
.tech-effect{opacity:.78;pointer-events:none;transition:opacity .36s ease}
.tech-effect .hover-detail{opacity:0;transition:opacity .36s ease}
:root:hover>.tech-effect,:root:focus>.tech-effect,:root.is-interactive>.tech-effect{opacity:1}
:root:hover .hover-detail,:root:focus .hover-detail,:root.is-interactive .hover-detail{opacity:.92}
:root:active>.tech-effect,:root.is-active>.tech-effect{opacity:1}
@media (prefers-reduced-motion:reduce){.tech-effect{display:none!important;transition:none}}
]]></style>'''

def extract_brand(content:str)->str:
    # original file contains nested <svg> brand immediately after outer description and before effect layer
    start=content.find('<svg',content.index('</desc>')+7)
    end=content.index('</svg>',start)+6
    assert start!=-1 and end>start
    return content[start:end]

def make(n,prior):
    brand=extract_brand(prior)
    layout,description,fn=FX[n]
    title=re.search(r'<title[^>]*>(.*?)</title>',prior,re.S).group(1)
    title=re.sub(r'(: interactive technology animation| — technical motion showcase)$','',title)
    artwork=brand if n=='react' else f'<g class="brand-art" transform="{LAYOUT[layout]}">{brand}</g>'
    # Technical hover/focus reveals domain-specific information, not only brightness.
    hover_markup=('<g class="hover-detail">'+HOVER[n]+'</g>') if n!='react' else ''
    # Transparent effect class remains separate from authentic logo paths and colors.
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64" role="img" aria-labelledby="title desc">
<title id="title">{title} — technical motion showcase</title>
<desc id="desc">{description}. Authentic logo paths, shapes, and brand colors are preserved.</desc>
{STYLE}
{artwork}
<g class="tech-effect" aria-hidden="true">{fn()}{hover_markup}</g>
</svg>\n'''

def main():
    import sys
    action=sys.argv[1] if len(sys.argv)>1 else '--write'
    if action=='--write':
        # First run: original files are repository baseline in .qa/baseline-svg
        baseline=ROOT/'.qa'/'baseline-svg'
        baseline.mkdir(parents=True,exist_ok=True)
        for n in NAMES:
            path=ASSETS/(n+'.svg'); ref=baseline/(n+'.svg')
            if not ref.exists(): ref.write_bytes(path.read_bytes())
            content=make(n,ref.read_text(encoding='utf-8'))
            path.write_text(content,encoding='utf-8')
        print('Built 28 premium technical SVG motion vignettes')
    else:
        raise SystemExit('usage: python3 tools/build_premium_motion.py --write')
if __name__=='__main__': main()
