"""Eleven art directions. Shared facts, independently composed SVG scenes.

Everything is self-contained: original vector illustrations, saved title outlines,
patterns and CSS animation. No remote fonts, images, scripts or tracking.
"""

import json
import math
from pathlib import Path
from xml.sax.saxutils import escape

TYPE = json.loads(Path(__file__).with_name('typefaces.json').read_text(encoding='utf-8'))
MONO = "'Lucida Console',Consolas,monospace"
SERIF = "Georgia,'Times New Roman',serif"
COLORS = ['#5bb7c8','#b59bdb','#dcb368','#9dbd82','#dd8e8e','#7d9ed0']


def T(x, y, label, size=15, fill='currentColor', font=None, **attrs):
    attrs = ' '.join(f'{k.replace("_", "-")}="{escape(str(v))}"' for k,v in attrs.items())
    family = f'font-family="{font}"' if font else ''
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" {family} {attrs}>{escape(str(label))}</text>'


def H(t, x, y, label, size=48, fill=None, **attrs):
    """Saved font outlines keep the actual display face on every visitor's OS."""
    glyph = TYPE.get(t['id'], TYPE['field-notes'])['glyphs'].get(label)
    fill = fill or t['ink']
    if not glyph:
        return T(x,y,label,size,fill,font=t['font'],**attrs)
    extra = ' '.join(f'{k.replace("_", "-")}="{v}"' for k,v in attrs.items())
    return f'<g aria-label="{escape(label)}" transform="translate({x} {y-size*.76:.2f}) scale({size/100})" {extra}><title>{escape(label)}</title><path d="{glyph["d"]}" fill="{fill}"/></g>'


def R(x,y,w,h,fill,rx=0,stroke='none',**attrs):
    extra=' '.join(f'{k.replace("_","-")}="{v}"' for k,v in attrs.items())
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" {extra}/>'


def P(d,stroke, width=1,fill='none',**attrs):
    extra=' '.join(f'{k.replace("_","-")}="{v}"' for k,v in attrs.items())
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" {extra}/>'


def C(x,y,r,fill,stroke='none',**attrs):
    extra=' '.join(f'{k.replace("_","-")}="{v}"' for k,v in attrs.items())
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" {extra}/>'


def svg(t,h,title,body,css=''):
    motion=ERA_MOTION.get(t['id'],'')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="{h}" viewBox="0 0 900 {h}" role="img" aria-labelledby="title">
<title id="title">{escape(title)}</title>
<defs>
<filter id="shadow" x="-30%" y="-30%" width="160%" height="170%"><feDropShadow dx="0" dy="7" stdDeviation="8" flood-color="#061227" flood-opacity=".18"/></filter>
<filter id="paper"><feTurbulence type="fractalNoise" baseFrequency=".7" numOctaves="3" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter>
<linearGradient id="gel" x2="0" y2="1"><stop stop-color="#fff"/><stop offset=".48" stop-color="#99d6ff"/><stop offset=".51" stop-color="#348bd4"/><stop offset="1" stop-color="#0f55ad"/></linearGradient>
<linearGradient id="chrome" x2="0" y2="1"><stop stop-color="#fafcff"/><stop offset=".42" stop-color="#c6d0e8"/><stop offset=".49" stop-color="#fff"/><stop offset=".51" stop-color="#6e7c9b"/><stop offset="1" stop-color="#e6edfb"/></linearGradient>
<linearGradient id="sky" x2="0" y2="1"><stop stop-color="#2298da"/><stop offset="1" stop-color="#d0f4fc"/></linearGradient>
<radialGradient id="ocean" cx=".3" cy=".25" r=".8"><stop stop-color="#8fefff"/><stop offset=".55" stop-color="#158acb"/><stop offset="1" stop-color="#074b89"/></radialGradient>
<linearGradient id="aurora" x2="1" y2="1"><stop stop-color="#172254"/><stop offset=".5" stop-color="#5b579d"/><stop offset="1" stop-color="#21868f"/></linearGradient>
<linearGradient id="glass" x2="1" y2="1"><stop stop-color="#fff" stop-opacity=".25"/><stop offset="1" stop-color="#fff" stop-opacity=".035"/></linearGradient>
<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><path d="M0 1H4" stroke="#000" opacity=".18"/></pattern>
<pattern id="pinstripe" width="4" height="4" patternUnits="userSpaceOnUse"><path d="M0 0H4" stroke="{t['accent']}" opacity=".09"/></pattern>
<pattern id="graph" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="{t['border']}" opacity=".55"/></pattern>
<pattern id="stars" width="117" height="97" patternUnits="userSpaceOnUse"><path d="M18 12v6m-3-3h6M89 67v4m-2-2h4" stroke="#fff"/><circle cx="54" cy="45" r="1" fill="#9a9aff"/></pattern>
</defs>
<style>text{{font-family:{t['font']};}}svg{{color:{t['ink']};}}.mono{{font-family:{MONO};}} {css} {motion}
@media(prefers-reduced-motion:reduce){{*{{animation:none!important;}}.trail{{stroke-dashoffset:0!important;}}}}
</style>{body}</svg>'''


def flight_path(t,d,ink=None,style='jet',duration=18,steps=False):
    ink=ink or t['accent']
    shapes={
        'jet':'M21 0Q21 -3 13 -3L3 -3 -8 -17 -13 -17 -7 -3 -16 -3 -21 -8 -24 -8 -21 0 -24 8 -21 8 -16 3 -7 3 -13 17 -8 17 3 3 13 3Q21 3 21 0Z',
        'pixel':'M18 -2H6V-6H2V-10H-2V-14H-6V-2H-14V-6H-18V6H-14V2H-6V14H-2V10H2V6H6V2H18Z',
        'paper':'M22 -11L-19 -4 -4 2 3 15Z M-4 2L22 -11',
    }
    plane=P(shapes.get(style,shapes['jet']),ink,1.2,ink,stroke_linejoin='round')
    body=P(d,ink,1.4,stroke_dasharray='3 7',opacity='.5',data_flight_route='true')
    body+=f'<g class="aircraft" data-travel="round-trip">{plane}</g>'
    css=f'''.aircraft{{offset-path:path('{d}');offset-distance:50%;offset-rotate:auto;animation:roundtrip {duration}s {'steps(32)' if steps else 'linear'} infinite;}}
@keyframes roundtrip{{0%,5%{{offset-distance:0%;offset-rotate:auto;}}44%,49%{{offset-distance:100%;offset-rotate:auto;}}50%,55%{{offset-distance:100%;offset-rotate:reverse;}}94%,99%{{offset-distance:0%;offset-rotate:reverse;}}100%{{offset-distance:0%;offset-rotate:auto;}}}}'''
    return body,css


def globe(x,y,r,fill='#65bce9',land='#c1ecbc',wire=False):
    b=C(x,y,r,fill,land,stroke_width='1.5')
    b+=f'<g transform="translate({x} {y}) scale({r/100})">'
    if wire:
        b+='<g fill="none" stroke="'+land+'" stroke-width="1"><ellipse rx="42" ry="100"/><ellipse rx="76" ry="100"/><ellipse rx="100" ry="34"/><ellipse rx="100" ry="68"/></g>'
    else:
        b+=P('M-67 -56L-40 -78 -9 -63 6 -43 -18 -18 -28 4 -48 -7 -58 -28Z M-23 13L0 17 13 42 -2 69 -15 83 -20 47Z M27 -62L57 -55 76 -28 48 -9 37 16 11 5 21 -23Z M34 39L66 44 61 65 44 69Z','none',fill=land)
    return b+'</g>'


def skeleton(x,y,scale=1,ink='#80ffc0',pose=False):
    d='M0 28V90M-30 44L0 35 34 47 56 19M0 90L-24 136M0 90L25 136'
    if pose: d='M0 28V90M-50 12L-30 44 0 35 34 47 56 19M0 90L-24 136M0 90L25 136'
    b=f'<g transform="translate({x} {y}) scale({scale})">'+C(0,10,13,'none',ink,stroke_width=2)+P(d,ink,2,stroke_linecap='round')
    b+=''.join(C(a,c,3,ink) for a,c in [(0,35),(-30,44),(34,47),(56,19),(0,90),(-24,136),(25,136)])
    return b+'</g>'


def grid(x,y,cell=48,ink='#266b65',soft='#dceee7',bg='#fff',square=False):
    b=''
    for row in range(3):
        for col in range(3):
            i=row*3+col
            b+=R(x+col*cell,y+row*cell,cell-5,cell-5,soft if i in(0,3,4,5) else bg,0 if square else 5,ink,stroke_opacity='.35',**{'class':f'cell cell-{i}'})
    route=f'M{x+(cell-5)/2} {y+(cell-5)/2}V{y+cell+(cell-5)/2}H{x+2*cell+(cell-5)/2}'
    b+=P(route,ink,2.5,pathLength=1,stroke_dasharray=1,**{'class':'trail'})
    b+=C(x+2*cell+(cell-5)/2,y+cell+(cell-5)/2,cell*.28,'none',ink,**{'class':'confirm'})
    return b


GRID_CSS='.trail{animation:recognize 7s ease-in-out infinite;}@keyframes recognize{0%,8%{stroke-dashoffset:1;}65%,90%{stroke-dashoffset:0;}100%{stroke-dashoffset:1;}}.confirm{animation:confirm 7s infinite;}@keyframes confirm{0%,60%,100%{opacity:.25;}70%,90%{opacity:1;}}'

ERA_MOTION={
    'phosphor':'.trail{animation-timing-function:steps(8);}.confirm{animation-timing-function:steps(1);}',
    'desktop95':'.cell-0,.cell-3,.cell-4,.cell-5{animation:selection 8s steps(1) infinite;}.cell-3{animation-delay:1s}.cell-4{animation-delay:2s}.cell-5{animation-delay:3s}@keyframes selection{0%,80%,100%{stroke-width:1}15%,65%{stroke-width:3;stroke-dasharray:2 2}}',
    'construction':'.trail{animation-duration:5s;animation-timing-function:steps(4);}',
    'matrix':'.tracking-scan{animation:tracking 6s linear infinite;}@keyframes tracking{0%{opacity:0;transform:translateY(0)}10%,85%{opacity:.6}100%{opacity:0;transform:translateY(240px)}}',
    'y2k':'.device-float{animation:levitate 6s ease-in-out infinite;}@keyframes levitate{50%{transform:translateY(-7px)}}',
    'aqua':'.confirm{stroke-width:4;animation:aqua-focus 5s ease-in-out infinite;}@keyframes aqua-focus{50%{stroke-width:1;opacity:.3}}',
    'aero':'.confirm{animation:aero-match 4s ease-in-out infinite;}@keyframes aero-match{50%{fill-opacity:.6;stroke-width:4}}',
    'metro':'.cell-5{transform-box:fill-box;transform-origin:center;animation:tileflip 8s ease-in-out infinite;}@keyframes tileflip{0%,65%,100%{transform:scaleY(1)}80%{transform:scaleY(.06)}}',
    'material':'.ink-ripple{transform-box:fill-box;transform-origin:center;animation:ink 4s ease-out infinite;}@keyframes ink{0%{transform:scale(.5);opacity:.6}75%,100%{transform:scale(1.6);opacity:0}}',
    'glass':'.spatial-device{animation:spatial 8s ease-in-out infinite;}@keyframes spatial{50%{transform:translateY(-6px)}}.aurora-flow{animation:auroraflow 15s ease-in-out infinite alternate;}@keyframes auroraflow{to{transform:translateX(35px)}}',
    'field-notes':'.trail{animation:pen 10s ease-in-out infinite;}@keyframes pen{0%,8%{stroke-dashoffset:1}30%,36%{stroke-dashoffset:.65}65%,91%{stroke-dashoffset:0}100%{stroke-dashoffset:1}}',
}


def button(t,x,y,label,kind=None,w=180):
    k=kind or t['id']; a=t['accent']
    if k=='desktop95':
        b=R(x,y,w,34,'#c0c0c0')+P(f'M{x} {y+34}V{y}H{x+w}','#fff',2)+P(f'M{x+1} {y+34}H{x+w}V{y+1}','#333',2)
        return b+T(x+w/2,y+22,label,13,'#111',font='Tahoma, sans-serif',text_anchor='middle')
    if k=='construction':
        return R(x,y,w,34,'#ffef00',0,'#fff',stroke_width=2)+T(x+w/2,y+23,label,17,'#000080',font=SERIF,text_anchor='middle',font_weight='bold')
    if k=='aqua':
        return R(x,y,w,32,'url(#gel)',16,'#2463a0')+T(x+w/2,y+22,label,13,'#fff',text_anchor='middle',font_weight='bold')
    if k=='aero':
        return R(x,y,w,36,'#147fb7',7,'#d8f7ff')+R(x+2,y+2,w-4,15,'#fff',5,opacity='.25')+T(x+w/2,y+24,label,14,'#fff',text_anchor='middle')
    if k=='y2k':
        d=f'M{x+10} {y}H{x+w}L{x+w-10} {y+34}H{x}Z'
        return P(d,'#7d8cac',1,'url(#chrome)')+T(x+w/2,y+23,label.upper(),12,'#182b5b',font='Arial, sans-serif',text_anchor='middle',font_weight='bold',letter_spacing=2)
    if k in ('phosphor','matrix'):
        return R(x,y,w,32,'none',0,a)+T(x+14,y+21,'> '+label,12,a,font=MONO)
    if k=='field-notes':
        return P(f'M{x} {y+31}H{x+w}',a,1)+T(x,y+22,label+' ↗',15,a,font=SERIF,font_style='italic')
    if k=='glass':
        return R(x,y,w,38,'url(#glass)',12,'#ffffff66')+T(x+w/2,y+25,label,13,t['ink'],text_anchor='middle')
    if k=='material':
        return R(x,y,w,38,a,4,filter='url(#shadow)')+T(x+w/2,y+25,label.upper(),12,t['bg'],text_anchor='middle',font_weight='bold',letter_spacing=1)
    return R(x,y,w,38,a)+T(x+15,y+26,label,16,t['bg'])


def window95(x,y,w,h,title):
    b=R(x,y,w,h,'#c0c0c0')+P(f'M{x} {y+h}V{y}H{x+w}','#fff',3)+P(f'M{x+2} {y+h}H{x+w}V{y+2}','#404040',3)
    b+=R(x+5,y+5,w-10,25,'#000080')+T(x+13,y+23,title,13,'#fff',font='Tahoma, sans-serif',font_weight='bold')
    for dx,label in ((w-64,'_'),(w-44,'□'),(w-24,'×')):
        b+=R(x+dx,y+9,16,16,'#c0c0c0',0,'#fff')+T(x+dx+8,y+21,label,13,'#111',text_anchor='middle')
    return b


def aqua_window(x,y,w,h,title):
    b=R(x,y,w,h,'#edf2f6',12,'#7b93a9',filter='url(#shadow)')+R(x+1,y+1,w-2,34,'url(#chrome)',11)
    b+=R(x+1,y+20,w-2,15,'url(#chrome)')
    for i,c in enumerate(('#f2766c','#f2cb69','#83c77b')): b+=C(x+18+i*22,y+17,6,c,'#77818d')+C(x+16+i*22,y+15,2,'#ffffff88')
    return b+T(x+w/2,y+22,title,13,'#2c3c4b',text_anchor='middle')


def scene_phosphor(t,kind):
    a=t['accent']; b=R(0,0,900,420,'#172016',22)+R(14,14,872,392,'#070e08',34,'#35462c')
    b+=R(24,24,852,372,'url(#scan)',30)+T(49,54,'VT-100  /  ROBIN-G0',12,a,font=MONO)+T(849,54,'CONNECTED',10,a,font=MONO,text_anchor='end')
    css='.cursor{animation:cursor 1.1s steps(1) infinite;}@keyframes cursor{50%{opacity:0;}}'
    if kind=='flight':
        b+=T(50,98,'$ whoami',14,a,font=MONO)+H(t,50,169,'ROBIN-G0',62,a)
        b+=T(52,205,'SOFTWARE ENGINEER / RESEARCH & DEVELOPMENT',13,a,font=MONO)
        b+=T(52,250,'$ route --from CA --to FR --return',13,a,font=MONO)
        f,c=flight_path(t,'M 118 307 H 779',a,'pixel',20,True); b+=f;css+=c
        b+=T(67,352,'[CANADA]',14,a,font=MONO)+T(735,352,'[FRANCE]',14,a,font=MONO)+R(50,370,9,15,a,**{'class':'cursor'})
    else:
        b+=T(50,100,'$ open motion-input-grid',14,a,font=MONO)+H(t,50,153,'Motion Input Grid',35,a)
        b+=T(50,193,'BODY LANDMARKS -> CONDITIONS -> ACTIONS',12,a,font=MONO)+T(50,228,'[x] open source   [ ] testers wanted',12,a,font=MONO)
        b+=button(t,50,273,'OPEN PROJECT',w=207)+T(50,346,'wrist.x  +0.31     wrist.y  -0.08',12,a,font=MONO)
        b+=P('M565 98V334H829 M565 216H829 M697 98V334',a,1,stroke_dasharray='2 7')
        b+=P('M595 130V269H771V178',a,2,pathLength=1,stroke_dasharray=1,**{'class':'trail'})
        for x,y,label in [(595,130,'01'),(595,269,'02'),(771,269,'03')]:
            b+=R(x-4,y-4,8,8,a)+T(x+10,y-10,label,10,a,font=MONO)
        b+=R(754,160,34,34,'none',0,a,**{'class':'confirm'})+T(605,372,'WRIST / X-Y TRACE',11,a,font=MONO);css+=GRID_CSS
    return svg(t,420,'Robin-G0: Canada ↔ France' if kind=='flight' else 'Motion Input Grid: open-source body motion input',b,css)


def scene_desktop95(t,kind):
    b=R(0,0,900,420,'#087e7d')
    for y,label in ((45,'My Computer'),(134,'Network')):
        b+=R(30,y,35,25,'#c8d8e5',0,'#fff')+R(34,y+4,27,17,'#000080')+P(f'M47 {y+25}v7m-12 0h24','#ddd',3)+T(48,y+51,label,10,'#fff',text_anchor='middle')
    css=''
    if kind=='flight':
        b+=window95(128,25,728,322,'Network Neighborhood — Robin-G0')
        b+=T(145,75,'File     Edit     View     Help',12,'#111',font='Tahoma, sans-serif')+R(141,89,700,241,'#fff',0,'#808080')
        b+=H(t,164,147,'Robin-G0',44,'#000080')+T(165,177,'Software Engineer · R&D',16,'#222')
        for x,label in ((206,'Canada'),(728,'France')):
            b+=P(f'M{x-22} 222v-12h24l6 7h27v32h-57Z','#8d6f04',1,'#ffe477')+T(x+5,279,label,14,'#111',text_anchor='middle')
        f,c=flight_path(t,'M 269 237 H 691','#000080','pixel',18,True);b+=f;css+=c
        b+=T(165,314,'2 locations selected',11,'#555')
    else:
        b+=window95(120,20,737,357,'Motion Input Grid — Properties')+T(138,69,'File     Profile     Camera     Help',12,'#111')
        b+=R(136,85,282,233,'#fff',0,'#808080')+grid(174,104,68,'#000080','#d5d5ee','#fff',True)
        b+=H(t,442,127,'Motion Input Grid',31,'#111')+T(443,164,'Body movements as input.',16,'#222')
        b+=T(443,196,'Web · Desktop · Games',14,'#333')+T(443,227,'Open source. Looking for testers.',13,'#333')
        b+=button(t,443,263,'Open project',w=171)+T(638,285,'Testers welcome',12,'#333')+T(139,349,'Status: waiting for a movement...',12,'#111');css+=GRID_CSS
    b+=R(0,386,900,34,'#c0c0c0')+P('M0 386H900','#fff',2)+button(t,5,390,'Start',w=75)+R(90,391,225,23,'#ddd',0,'#888')+T(102,407,'Robin-G0',12,'#111')+T(875,407,'CA ↔ FR',12,'#111',text_anchor='end')
    return svg(t,420,'Robin-G0 — a Windows 95 desktop' if kind=='flight' else 'Motion Input Grid — a Windows 95 configuration dialog',b,css)


def scene_construction(t,kind):
    b=R(0,0,900,440,'#050523')+R(0,0,900,440,'url(#stars)')
    css='.twinkle{animation:twinkle 2s steps(2) infinite;}@keyframes twinkle{50%{opacity:.35;}}.webspin{transform-box:fill-box;transform-origin:center;animation:spin 16s linear infinite;}@keyframes spin{to{transform:rotate(360deg);}}'
    b+=P('M8 8H892V432H8Z','#b14cff',3)+T(450,38,'★  WELCOME TO MY PERSONAL HOMEPAGE  ★' if kind=='flight' else '★  PROJECT SPOTLIGHT  ★',16,'#ffff66',font=SERIF,text_anchor='middle',**{'class':'twinkle'})
    if kind=='flight':
        b+=H(t,171,122,'Robin-G0',76,'#38f1fc')+T(450,161,'Software Engineer — Research & Development',19,'#fff',font=SERIF,text_anchor='middle')
        b+=f'<g class="webspin">{globe(97,107,40,"#002ba2","#32d886",True)}</g>'+globe(803,107,40,'#002ba2','#32d886',True)
        b+=R(68,192,764,39,'#1a1264',0,'#8888ff')+T(450,217,'Computer vision · Systems · Quantum computing',17,'#ffb7ef',font=SERIF,text_anchor='middle')
        f,c=flight_path(t,'M 145 306 Q 450 226 755 306','#ffff55','pixel',17,True);b+=f;css+=c
        b+=T(92,355,'CANADA',19,'#5dff91',font=SERIF)+T(734,355,'FRANCE',19,'#5dff91',font=SERIF)
        b+=R(265,382,370,27,'#000',0,'#fff')+T(450,401,'[ SOFTWARE ENGINEER • ROBIN-G0 ]',12,'#ffff00',font=MONO,text_anchor='middle')
    else:
        b+=H(t,144,111,'Motion Input Grid',53,'#fff')+T(450,150,'Move your body. Control your applications.',20,'#38f1fc',font=SERIF,text_anchor='middle')
        b+=R(49,182,380,168,'#16115c',0,'#ffeb00')+grid(167,193,49,'#ffff55','#391c80','#151144',True)
        b+=T(465,210,'An open-source motion input',18,'#fff',font=SERIF)+T(465,238,'framework for web, desktop & games.',18,'#fff',font=SERIF)
        b+=T(465,279,'TESTERS WANTED!',23,'#ff83bd',font=SERIF,**{'class':'twinkle'})+button(t,467,304,'ENTER PROJECT >>',w=290)
        for x in range(14,888,27): b+=P(f'M{x} 391l18 -18','#ffec00',9)
        b+=R(170,372,560,30,'#090924')+T(450,393,'UNDER ACTIVE DEVELOPMENT',15,'#ffff55',font=MONO,text_anchor='middle');css+=GRID_CSS
    return svg(t,440,'Robin-G0 — personal web, 1996' if kind=='flight' else 'Motion Input Grid — animated personal-web project page',b,css)


def scene_matrix(t,kind):
    a='#67ff9c';b=R(0,0,900,420,'#020906');css=GRID_CSS
    if kind=='flight':
        for col in range(32):
            x=18+col*28; chars=''.join(f'<tspan x="{x}" dy="20">{(col*19+n*11)%10}</tspan>' for n in range(20))
            b+=f'<text y="-400" fill="#19a15a" opacity=".17" font-family="monospace" font-size="12" class="rain" style="animation-delay:-{col*.41}s">{chars}</text>'
        css+='.rain{animation:rain 13s linear infinite;}@keyframes rain{to{transform:translateY(820px);}}'
        b+=R(38,57,824,183,'#020906',opacity='.84')+T(58,84,'IDENTITY / ROBIN-G0',11,a,font=MONO,letter_spacing=3)+H(t,55,163,'ROBIN-G0',76,'#caffde')
        b+=T(59,204,'SOFTWARE ENGINEER · R&D',14,a,font=MONO)+P('M58 225H842','#1b4b32',1)
        f,c=flight_path(t,'M 132 312 C 323 254 577 254 768 312',a,'jet',20);b+=f;css+=c
        b+=T(60,368,'CA / CANADA',12,a,font=MONO)+T(840,368,'FR / FRANCE',12,a,font=MONO,text_anchor='end')
    else:
        b+=P('M30 63V30H63 M837 30H870V63 M870 357V390H837 M63 390H30V357',a,2)
        b+=T(55,62,'INPUT RECOGNITION / LIVE MODEL',10,a,font=MONO,letter_spacing=2)+H(t,55,129,'Motion Input Grid',43,'#d6ffe4')
        b+=T(57,168,'LANDMARKS → CONDITIONS → ACTIONS',12,a,font=MONO)+T(57,211,'An open-source motion input framework.',13,'#9bbdaa',font=MONO)
        b+=button(t,58,262,'ACCESS PROJECT',w=224)+T(58,351,'WEB / DESKTOP / GAMES',11,a,font=MONO)
        b+=R(576,73,262,269,'url(#graph)',0,'#163d29')+skeleton(701,109,1.3,a,True)
        b+='<defs><clipPath id="tracking-frame"><rect x="576" y="73" width="262" height="269"/></clipPath></defs><g clip-path="url(#tracking-frame)">'+P('M577 75H837',a,1,**{'class':'tracking-scan'})+'</g>'
        b+=P('M742 116H801V171H742Z',a,1)+C(773,143,23,'none',a,**{'class':'confirm'})+T(600,369,'GESTURE MATCH / 001',11,a,font=MONO)
    return svg(t,420,'Robin-G0 — Matrix identity console' if kind=='flight' else 'Motion Input Grid — landmark recognition schematic',b,css)


def scene_y2k(t,kind):
    b=R(0,0,900,420,t['bg'])+P('M0 0H900V51H0Z','none',fill='url(#chrome)')
    b+=T(28,31,'RG-00  /  PERSONAL SYSTEM',11,'#203866',font='Arial, sans-serif',letter_spacing=3)
    css='.orbit{transform-origin:700px 205px;animation:orbit 9s ease-in-out infinite;}@keyframes orbit{50%{transform:rotate(-8deg);}}'+GRID_CSS
    if kind=='flight':
        b+=f'<g class="orbit">'+f'<ellipse cx="701" cy="207" rx="157" ry="75" transform="rotate(-35 701 207)" fill="none" stroke="url(#chrome)" stroke-width="24"/>'+C(700,204,80,'#8299de',stroke='#dce4ff')+'</g>'
        b+=H(t,30,161,'ROBIN-G0',84,t['ink'])+T(34,202,'SOFTWARE ENGINEER',18,t['accent'],font='Arial, sans-serif',letter_spacing=4)+T(35,231,'Research & development',16,t['muted'])
        b+=P('M34 263H462L491 240',t['accent'],1.5)+T(35,288,'COMPUTER VISION / SYSTEMS / QUANTUM',10,t['muted'],letter_spacing=1)
        f,c=flight_path(t,'M 120 346 C 270 308 451 308 548 346',t['accent'],'jet',15);b+=f;css+=c
        b+=T(35,383,'CANADA',12,t['ink'],letter_spacing=2)+T(495,383,'FRANCE',12,t['ink'],letter_spacing=2)
    else:
        b+=P('M581 162L751 98 856 171 846 298 674 361 572 292Z','#7d8eb9',2,'url(#chrome)')+P('M604 174L748 121 827 179 818 278 675 332 599 279Z','#7d8eb9',1,'#253d7a')
        b+=H(t,33,142,'Motion',68,t['ink'])+H(t,33,206,'Input Grid',68,t['ink'])+T(37,242,'MOTION INPUT FRAMEWORK / OPEN SOURCE',11,t['accent'],letter_spacing=1)
        b+=button(t,36,288,'Explore project',w=233)+T(37,374,'WEB  /  DESKTOP  /  GAMES',12,t['muted'],letter_spacing=2)
        b+=f'<g class="device-float"><g transform="translate(649 187) skewY(-14)">{grid(0,0,44,"#263d7a","#b4c5ee","#e7ecfc",True)}</g></g>'
    b+=P('M0 411H900',t['accent'],3)+P('M750 404H900',t['accent'],10)
    return svg(t,420,'Robin-G0 — Y2K chrome and orbital sculpture' if kind=='flight' else 'Motion Input Grid — Y2K industrial interface',b,css)


def scene_aqua(t,kind):
    b=R(0,0,900,430,'#316fae')+P('M0 380C260 120 480 530 900 30V430H0Z','none',fill='#6da6d1')+P('M0 420C350 120 590 450 900 135','#b9daf1',2)
    css=GRID_CSS
    if kind=='flight':
        b+=aqua_window(35,28,830,372,'Robin-G0 — Address Book')+R(36,63,828,336,'url(#pinstripe)',10)
        b+=R(54,84,235,278,'#dbe6ee',9)+globe(172,191,82,'#4e91ca','#c1e7c7')
        b+=T(171,318,'Canada ↔ France',16,'#264c70',text_anchor='middle')
        b+=H(t,319,140,'Robin-G0',57,'#182f4b')+T(321,181,'Software Engineer',22,'#315978')+T(322,210,'Research & development',15,'#536d82')
        b+=P('M320 230H824','#b5c4d0',1)+T(321,262,'Computer vision · Systems · Quantum computing',13,'#3a566f')
        f,c=flight_path(t,'M 368 327 Q 571 260 775 327','#2b6eb9','jet',19);b+=f;css+=c
        b+=T(327,366,'CANADA',10,'#355b78',letter_spacing=2)+T(814,366,'FRANCE',10,'#355b78',text_anchor='end',letter_spacing=2)
    else:
        b+=aqua_window(28,22,844,382,'Motion Input Grid')+R(29,57,842,43,'url(#chrome)')
        b+=T(48,83,'Profile     Camera     Recognize',13,'#293d50')+R(44,114,368,258,'#142e42',6)
        b+=grid(126,139,68,'#a9d9ff','#244d68','#19394e')+T(62,355,'Camera input · Gesture recognition',10,'#aacfe5')
        b+=H(t,441,155,'Motion Input Grid',34,'#273d52')+T(443,192,'Body movements as application input.',16,'#4d6174')
        b+=T(443,231,'Websites, desktop applications and games.',13,'#4d6174')+T(443,260,'Open source. Testers welcome.',13,'#4d6174')
        b+=button(t,443,303,'Open project',w=181)+T(646,324,'Testers welcome',12,'#536d82')
    return svg(t,430,'Robin-G0 — Aqua Address Book' if kind=='flight' else 'Motion Input Grid — Aqua desktop application',b,css)


def landscape():
    b=R(0,0,900,440,'url(#sky)')
    b+=C(725,80,57,'#fff',opacity='.25')+C(725,80,33,'#fff',opacity='.7')
    for x,y,w in ((370,31,100),(750,153,140)):
        b+=f'<g class="cloud">{R(x,y,w,19,"#fff",10,opacity=".56")}{C(x+w*.35,y,21,"#fff",opacity=".56")}{C(x+w*.60,y-2,29,"#fff",opacity=".56")}</g>'
    b+=P('M0 314Q235 241 491 318T900 302V440H0Z','none',fill='#78bb43')+P('M0 355Q324 256 566 353T900 334V440H0Z','none',fill='#398d45')
    b+=P('M0 396Q300 348 900 390V440H0Z','none',fill='#7dcad7')
    return b


def scene_aero(t,kind):
    b=landscape() if kind=='flight' else R(0,0,900,440,'#82c4d9')+P('M0 380Q290 255 900 377V440H0Z','none',fill='#397ba5')
    css='.cloud{animation:clouds 12s ease-in-out infinite alternate;}@keyframes clouds{to{transform:translateX(25px);}}'+GRID_CSS
    if kind=='flight':
        b+=H(t,42,121,'Robin-G0',68,'#fff')+T(47,160,'Software Engineer · R&D',20,'#123d59')
        b+=T(48,192,'Computer vision · Systems · Quantum computing',14,'#164b67')
        b+=globe(691,260,100,'url(#ocean)','#b2dd61')+C(662,218,24,'#fff',opacity='.24')
        b+='<ellipse cx="691" cy="260" rx="98" ry="38" fill="none" stroke="#fff" opacity=".2"/><ellipse cx="691" cy="260" rx="42" ry="98" fill="none" stroke="#fff" opacity=".16"/>'
        b+=R(31,240,390,131,'#fff',15,stroke='#d5f8ff',fill_opacity='.65',filter='url(#shadow)')
        f,c=flight_path(t,'M 92 310 Q 225 253 359 310','#125785','jet',19);b+=f;css+=c
        b+=T(53,350,'CANADA',12,'#185575',letter_spacing=2)+T(400,350,'FRANCE',12,'#185575',text_anchor='end',letter_spacing=2)
    else:
        b+=R(29,29,842,376,'#fff',16,fill_opacity='.78',stroke='#e3fbff',filter='url(#shadow)')+R(32,32,836,34,'#b4e7f5',14,fill_opacity='.6')
        b+=T(50,55,'Motion Input Grid',14,'#1d4f68')+H(t,55,130,'Motion Input Grid',44,'#194c69')
        b+=T(57,168,'An open-source framework for motion input.',16,'#3b697f')+T(57,197,'Web · Desktop · Games',14,'#3b697f')
        b+=button(t,57,236,'Explore project',w=210)+T(59,307,'Looking for testers',14,'#306c80')
        b+=R(535,90,285,253,'#e5f6fc',12,'#8dbfcf')+skeleton(650,114,1.2,'#258eb1',True)
        b+=C(718,139,28,'#9ac447',stroke='#e7ffd5',fill_opacity='.3',**{'class':'confirm'})+T(676,369,'CAMERA → MOVEMENT → ACTION',10,'#24556d',text_anchor='middle')
    return svg(t,440,'Robin-G0 — sky, globe and a France–Canada flight' if kind=='flight' else 'Motion Input Grid — Aero motion recognition window',b,css)


def scene_metro(t,kind):
    bg='#172951' if t.get('mode')=='dark' else '#f2f3f5';ink='#fff' if t.get('mode')=='dark' else '#172951'
    b=R(0,0,900,430,bg);css=GRID_CSS
    if kind=='flight':
        b+=H(t,34,91,'Robin-G0',68,ink)+T(38,127,'Software Engineer · Research & development',19,ink)
        b+=R(36,162,275,223,'#087aa5')+R(322,162,322,223,'#b33c7b')+R(655,162,208,106,'#dc6d23')+R(655,279,208,106,'#4b963d')
        b+=T(57,357,'Canada',26,'#fff')+T(621,357,'France',26,'#fff',text_anchor='end')
        b+=globe(763,218,33,'none','#fff',True)+P('M725 337l25 -25 23 22 28 -35','#fff',3)
        f,c=flight_path(t,'M 115 254 H 563','#fff','jet',16,True);b+=f;css+=c
    else:
        b+=T(37,44,'projects / motion input',15,ink)+H(t,32,129,'Motion',86,ink)+H(t,32,211,'Input Grid',86,ink)
        b+=T(38,253,'Open-source motion input framework.',17,ink)+T(38,282,'Web · Desktop · Games',16,ink)
        b+=button(t,38,328,'Explore project →',w=272)
        b+=R(520,79,343,307,'#d86924')+grid(573,110,82,'#fff','#e7894b','#d86924',True)
        b+=T(540,365,'MOVEMENT → ACTION',14,'#fff',letter_spacing=2)
    return svg(t,430,'Robin-G0 — Metro start screen' if kind=='flight' else 'Motion Input Grid — Metro project poster',b,css)


def scene_material(t,kind):
    b=R(0,0,900,430,t['soft']);css=GRID_CSS
    if kind=='flight':
        b+=P('M0 0H900V100L0 270Z','none',fill=t['accent'])+R(29,31,544,357,t['bg'],8,filter='url(#shadow)')
        b+=T(54,72,'PROFILE',11,t['muted'],letter_spacing=3)+H(t,53,149,'Robin-G0',65,t['ink'])
        b+=T(57,193,'Software Engineer',23,t['accent'])+T(58,225,'Research & development',16,t['muted'])
        b+=P('M56 249H538',t['border'],1)+T(58,285,'Computer vision',15,t['ink'])+T(58,313,'Systems · Quantum computing',15,t['ink'])
        b+=R(600,109,270,279,t['bg'],8,filter='url(#shadow)')+T(624,143,'CANADA ↔ FRANCE',13,t['muted'])
        f,c=flight_path(t,'M 642 317 Q 666 177 830 213',t['accent'],'paper',19);b+=f;css+=c
        b+=C(641,318,4,t['accent'])+C(829,213,4,t['accent'])+T(625,360,'CA',14,t['accent'])+T(846,247,'FR',14,t['accent'],text_anchor='end')
    else:
        b+=R(30,25,840,374,t['bg'],8,filter='url(#shadow)')+R(30,25,840,66,t['accent'],8)+R(30,64,840,27,t['accent'])
        b+=T(57,67,'Motion Input Grid',25,t['bg'])+T(59,128,'Open-source motion input framework',16,t['ink'])
        for i,(label,sub) in enumerate((('Camera','Track landmarks'),('Movement','Match conditions'),('Action','Control an application'))):
            x=58+i*267
            b+=R(x,157,249,133,t['soft'],6)+C(x+28,185,15,t['accent'])+T(x+28,190,i+1,12,t['bg'],text_anchor='middle')
            b+=T(x+20,227,label,21,t['ink'])+T(x+20,257,sub,12,t['muted'])
        b+=P('M305 221H322M572 221H589',t['accent'],2)+button(t,58,326,'Explore project',w=212)
        b+=C(815,347,26,t['accent'],filter='url(#shadow)')+C(815,347,27,'none',t['accent'],**{'class':'ink-ripple'})+P('M804 347H826M815 336V358',t['bg'],2)
    return svg(t,430,'Robin-G0 — Material paper profile and flight itinerary' if kind=='flight' else 'Motion Input Grid — Material movement pipeline',b,css)


def scene_glass(t,kind):
    b=R(0,0,900,440,'url(#aurora)',24);css=GRID_CSS
    if kind=='flight':b+=P('M-90 390C85 -85 472 476 1002 24','#b1b4f8',100,opacity='.12',**{'class':'aurora-flow'})
    if kind=='flight':
        b+=T(42,57,'ROBIN-G0',11,'#dae6ff',letter_spacing=4)+H(t,39,159,'Robin-G0',77,'#fff')
        b+=T(45,204,'Software Engineer',24,'#edf2ff')+T(46,237,'Research & development',16,'#c5d6f4')
        b+=T(46,333,'Computer vision',15,'#e5eeff')+T(46,362,'Systems · Quantum computing',15,'#e5eeff')
        b+=R(564,40,292,359,'url(#glass)',25,'#ffffff55',filter='url(#shadow)')+T(590,78,'CANADA / FRANCE',11,'#e6eeff',letter_spacing=2)
        b+=T(594,138,'CA',38,'#fff',font='Segoe UI Light, sans-serif')+T(824,337,'FR',38,'#fff',font='Segoe UI Light, sans-serif',text_anchor='end')
        f,c=flight_path(t,'M 622 177 C 784 159 643 289 791 283','#e7fbff','jet',20);b+=f;css+=c
        b+=P('M587 362H832','#ffffff44',1)+T(590,383,'ROUND TRIP',10,'#d6e4fa',letter_spacing=3)
    else:
        b+=R(26,26,848,388,'url(#glass)',24,'#ffffff55')
        b+=f'<g class="spatial-device"><g transform="translate(67 94) skewY(-12)">{grid(0,0,87,"#c9ddff","#ffffff22","#ffffff09")}</g></g>'
        b+=H(t,390,143,'Motion Input Grid',44,'#fff')+T(393,185,'Body movements as input.',21,'#ecf2ff')
        b+=T(393,224,'An open-source framework for web,',15,'#cfdcf6')+T(393,248,'desktop applications and games.',15,'#cfdcf6')
        # In this dark illustration use a light-ink button, regardless of page mode.
        b+=button(dict(t,ink='#fff'),393,295,'Explore project ↗',w=229)+T(395,371,'LOOKING FOR TESTERS',10,'#e5eeff',letter_spacing=2)
    return svg(t,440,'Robin-G0 — glass itinerary on an aurora desktop' if kind=='flight' else 'Motion Input Grid — spatial glass input device',b,css)


def scene_field_notes(t,kind):
    b=R(0,0,900,430,t['bg'])+R(0,0,900,430,'#b4a98c',opacity='.06',filter='url(#paper)')
    b+=P('M36 46H864M36 392H864',t['ink'],1)+T(37,32,'ROBIN-G0  /  ENGINEERING NOTES',10,t['accent'],font=MONO,letter_spacing=1)
    css=GRID_CSS
    if kind=='flight':
        b+=H(t,33,145,'Robin-G0',91,t['ink'])+T(41,185,'Software Engineer · Research & development',18,t['muted'],font=SERIF)
        b+=T(42,231,'Computer vision, systems',16,t['ink'],font=SERIF)+T(42,255,'and quantum computing.',16,t['ink'],font=SERIF)
        b+=f'<g transform="translate(597 193) scale(.68)">{globe(0,0,100,"none",t["border"],True)}</g>'
        f,c=flight_path(t,'M 100 331 Q 450 241 802 331',t['accent'],'paper',22);b+=f;css+=c
        b+=T(43,371,'Canada',18,t['ink'],font=SERIF,font_style='italic')+T(857,371,'France',18,t['ink'],font=SERIF,font_style='italic',text_anchor='end')
    else:
        b+=H(t,34,115,'Motion Input Grid',53,t['ink'])+T(40,151,'An open-source motion input framework.',17,t['muted'],font=SERIF)
        b+=R(464,175,400,188,'url(#graph)')+grid(582,180,57,t['accent'],t['soft'],t['bg'],True)
        b+=P('M557 180H542V345H557M582 357V365H747V357',t['muted'],.8)+T(525,265,'3',11,t['muted'],font=MONO)+T(664,382,'REQUIRED CELLS → TRIGGER',9,t['accent'],font=MONO,text_anchor='middle')
        b+=T(40,207,'Body movements become actions',19,t['ink'],font=SERIF)+T(40,237,'in websites, desktop apps and games.',16,t['muted'],font=SERIF)
        b+=button(t,40,282,'Explore the project',w=241)+T(41,359,'Testers welcome.',15,t['muted'],font=SERIF,font_style='italic')
    b+=T(864,414,'CA ↔ FR',10,t['muted'],font=MONO,text_anchor='end')
    return svg(t,430,'Robin-G0 — printed engineering notebook' if kind=='flight' else 'Motion Input Grid — annotated notebook schematic',b,css)


SCENES={'phosphor':scene_phosphor,'desktop95':scene_desktop95,'construction':scene_construction,
        'matrix':scene_matrix,'y2k':scene_y2k,'aqua':scene_aqua,'aero':scene_aero,
        'metro':scene_metro,'material':scene_material,'glass':scene_glass,'field-notes':scene_field_notes}


def scene(t,kind):
    return SCENES.get(t['id'],scene_field_notes)(t,kind)


def action_button(t,label):
    body=button(t,12,12,label,w=256)
    if t['id'] in ('phosphor','matrix'):
        body=R(6,6,268,50,'#080f09',4)+body
    if t['id']=='glass':
        body=R(7,6,266,49,t['soft'],14,t['border'])+body
    document=svg(t,64,label,body)
    return document.replace('width="900" height="64" viewBox="0 0 900 64"',
                            'width="280" height="64" viewBox="0 0 280 64"',1)


def metrics(data):
    def number(k): return f"{data[k]:,}" if data.get(k) is not None else '—'
    return [(number('repositories'),'public repos'),(number('commits'),'commits'),
            (number('lines_changed'),'filtered line edits')]


def language_rows(data):
    items=sorted(data['languages'].items(),key=lambda p:(-p[1],p[0]));total=sum(n for _,n in items) or 1
    return [(name,n/total,f'{n/total:.1%}' if n/total>=.001 else '<0.1%') for name,n in items]


def activity(t,data):
    """Distinct information layouts, while keeping every number and language."""
    k=t['id'];rows=language_rows(data);values=metrics(data);a=t['accent'];ink=t['ink'];mut=t['muted'];css=''
    updated=data['updated'] if data.get('updated') else 'pending'
    foot='Public repositories · Language share by bytes · Filtered additions + deletions'
    if k=='phosphor':
        h=306+max(len(rows),1)*29;b=R(0,0,900,h,'#080f09',15)+R(0,0,900,h,'url(#scan)',15)
        b+=T(32,40,'$ git report --public --exclude-generated',14,a,font=MONO)+P(f'M30 58H870',a)
        for i,(v,label) in enumerate(values):b+=T(35+i*288,103,v,32,a,font=MONO)+T(35+i*288,132,label.upper(),11,a,font=MONO)
        b+=T(35,184,'LANGUAGE              DISTRIBUTION                         SHARE',12,a,font=MONO)
        for i,(name,pct,label) in enumerate(rows):
            y=218+i*29;b+=T(35,y,name,13,a,font=MONO)+T(255,y,'█'*max(1,round(pct*40)),13,a,font=MONO)+T(856,y,label,13,a,font=MONO,text_anchor='end')
        b+=T(35,h-43,'UPDATED '+updated+' UTC',10,a,font=MONO)+T(35,h-20,foot,10,a,font=MONO)
    elif k=='desktop95':
        h=282+max(len(rows),1)*28;b=R(0,0,900,h,'#087e7d')+window95(13,12,874,h-27,'System Monitor — Public GitHub activity')
        b+=R(25,58,196,h-88,'#d1d1d1',0,'#808080')
        for i,(v,label) in enumerate(values):b+=T(40,91+i*95,label,12,'#333')+T(40,125+i*95,v,27,'#000080')
        b+=R(237,59,634,h-89,'#fff',0,'#808080')+T(254,88,'Language',13,'#111')+T(850,88,'Code size',13,'#111',text_anchor='end')
        for i,(name,pct,label) in enumerate(rows):
            y=123+i*28;b+=T(254,y,name,12,'#111')+R(406,y-11,330*pct,13,'#000080')+T(852,y,label,12,'#111',text_anchor='end')
        b+=T(34,h-23,'Updated '+updated+' UTC · owned public repositories',10,'#111')
    elif k=='construction':
        h=280+max(len(rows),1)*29;b=R(0,0,900,h,'#050523')+R(0,0,900,h,'url(#stars)')
        b+=T(450,43,'★ MY GITHUB STATS ★',29,'#ffff66',font=SERIF,text_anchor='middle',font_weight='bold')
        for i,(v,label) in enumerate(values):
            x=28+i*294;b+=R(x,69,264,90,'#171148',0,'#8888ff')+T(x+132,109,v,30,'#6effcc',font=MONO,text_anchor='middle')+T(x+132,140,label,15,'#fff',font=SERIF,text_anchor='middle')
        b+=P('M28 181H872','#ffed00',3)
        for i,(name,pct,label) in enumerate(rows):
            y=218+i*29;c=COLORS[i%len(COLORS)];b+=T(31,y,name,16,'#fff',font=SERIF)+R(220,y-13,540*pct,15,c,0,'#fff')+T(867,y,label,14,'#ffff66',font=MONO,text_anchor='end')
        b+=T(450,h-33,'Last updated: '+updated+' UTC',12,'#bdbdff',font=SERIF,text_anchor='middle')+T(450,h-12,foot,11,'#fff',font=SERIF,text_anchor='middle')
    elif k=='matrix':
        h=max(448,140+len(rows)*28);b=R(0,0,900,h,'#020906')+P(f'M321 30V{h-30}',a,1)
        b+=T(28,47,'ACTIVITY / PUBLIC',12,a,font=MONO,letter_spacing=2)
        for i,(v,label) in enumerate(values):b+=T(29,111+i*103,v,40,'#d1ffdf',font=MONO)+T(30,139+i*103,label.upper(),10,a,font=MONO)
        b+=T(350,48,'LANGUAGE DISTRIBUTION',11,a,font=MONO)
        for i,(name,pct,label) in enumerate(rows):
            y=87+i*28;b+=T(351,y,name,11,'#b1d5bd',font=MONO)+P(f'M500 {y-4}H{500+272*pct}',a,3)+T(870,y,label,11,a,font=MONO,text_anchor='end')
        b+=T(28,h-20,updated+' UTC / DEFAULT BRANCH HISTORY',10,a,font=MONO)
    elif k=='y2k':
        h=330+max(len(rows),1)*28;b=R(0,0,900,h,t['bg'])+R(0,0,900,21,'url(#chrome)')+H(t,29,84,'Public activity',45,ink)
        for i,(v,label) in enumerate(values):
            x=30+i*289;b+=P(f'M{x} 113H{x+269}L{x+256} 219H{x-1}Z','#8895b4',1,'url(#chrome)')+T(x+18,163,v,35,'#192747',font='Arial, sans-serif',font_weight='bold',font_style='italic')+T(x+18,193,label.upper(),10,'#243857',letter_spacing=1)
        for i,(name,pct,label) in enumerate(rows):
            y=267+i*28;b+=T(32,y,name,13,ink)+P(f'M207 {y-8}H{207+566*pct}L{204+566*pct} {y+1}H204Z',a,.5,a)+T(870,y,label,12,mut,text_anchor='end')
        b+=P(f'M30 {h-45}H870',a,1)+T(30,h-20,'PUBLIC DATA / '+updated+' UTC',11,mut,letter_spacing=2)
    elif k=='aqua':
        h=258+max(len(rows),1)*28;b=R(0,0,900,h,'#316fae')+aqua_window(16,15,868,h-30,'GitHub Library — Statistics')
        b+=R(29,61,187,h-94,'#dce7ef')+T(44,92,'LIBRARY',10,'#62778a',font_weight='bold')
        for i,(v,label) in enumerate(values):b+=T(44,129+i*92,label,12,'#3b536b')+T(44,163+i*92,v,26,'#245e91')
        b+=T(235,89,'Language',12,'#344f68')+T(853,89,'Share',12,'#344f68',text_anchor='end')
        for i,(name,pct,label) in enumerate(rows):
            y=121+i*28;b+=R(226,y-19,643,28,'#e7eff7' if i%2==0 else '#fff')+C(243,y-5,5,COLORS[i%6])+T(259,y,name,12,'#294b69')+R(433,y-11,337*pct,12,'url(#gel)',6)+T(852,y,label,12,'#294b69',text_anchor='end')
        b+=T(235,h-32,'Updated '+updated+' UTC · Public repositories only',10,'#49637a')
    elif k=='aero':
        h=290+max(len(rows),1)*27;b=R(0,0,900,h,'#d9f0f5')+P(f'M0 {h}Q450 {h-145} 900 {h-30}V{h}Z','none',fill='#c0dfa4')
        b+=R(20,19,860,h-40,'#ffffffaa',16,'#fff')+T(43,54,'GitHub activity',23,'#1c6082')
        for i,(v,label) in enumerate(values):
            x=42+i*285;b+=R(x,78,251,91,'#d2edf8',10,'#a4cedd')+T(x+17,119,v,32,'#1c668a')+T(x+18,148,label,12,'#47758b')
        for i,(name,pct,label) in enumerate(rows):
            y=210+i*27;b+=T(44,y,name,12,'#275b72')+R(213,y-10,544,11,'#c5e3ec',6)+R(213,y-10,544*pct,11,'#428eb8',6)+P(f'M218 {y-8}H{213+544*pct}', '#c6f7ff',2)+T(850,y,label,12,'#275b72',text_anchor='end')
        b+=T(44,h-33,'Public repositories · Updated '+updated+' UTC',11,'#47758b')
    elif k=='metro':
        h=267+math.ceil(max(len(rows),1)/3)*105;b=R(0,0,900,h,t['bg'])+H(t,30,65,'Public activity',45,ink)
        for i,(v,label) in enumerate(values):
            x=30+i*288;c=['#087aa5','#b33c7b','#4b963d'][i];b+=R(x,89,272,105,c)+T(x+16,138,v,36,'#fff',font='Segoe UI Light, sans-serif')+T(x+18,176,label,14,'#fff')
        for i,(name,pct,label) in enumerate(rows):
            x=30+(i%3)*288;y=218+(i//3)*105;c=['#145e93','#654698','#b3512b','#347c62'][i%4]
            b+=R(x,y,272,93,c)+T(x+16,y+30,name,15,'#fff')+T(x+16,y+70,label,29,'#fff',font='Segoe UI Light, sans-serif')
        b+=T(30,h-15,'Updated '+updated+' UTC · owned public repositories',11,mut)
    elif k=='material':
        h=284+math.ceil(max(len(rows),1)/2)*47;b=R(0,0,900,h,t['soft'])+R(23,19,854,h-42,t['bg'],8,filter='url(#shadow)')
        b+=T(46,58,'Public activity',24,ink)
        for i,(v,label) in enumerate(values):x=47+i*283;b+=T(x,124,v,34,a)+T(x,155,label,12,mut)
        b+=P('M46 179H854',t['border'],1)
        for i,(name,pct,label) in enumerate(rows):
            x=48+(i%2)*413;y=216+(i//2)*47;c=COLORS[i%6]
            b+=C(x+5,y-4,5,c)+T(x+20,y,name,12,ink)+T(x+365,y,label,12,mut,text_anchor='end')+R(x+20,y+9,345,3,t['soft'])+R(x+20,y+9,345*pct,3,a)
        b+=T(48,h-40,'Updated '+updated+' UTC · filtered additions + deletions',10,mut)
    elif k=='glass':
        h=290+math.ceil(max(len(rows),1)/2)*44;b=R(0,0,900,h,t['bg'],24)+R(17,17,866,h-34,t['soft'],22,t['border'])
        b+=H(t,40,72,'Public activity',38,ink)
        for i,(v,label) in enumerate(values):
            x=41+i*286;b+=T(x,134,v,37,ink,font='Segoe UI Light, sans-serif')+T(x,164,label,12,mut)
        b+=R(42,190,815,7,t['border'],4);x=42
        for i,(_,pct,_) in enumerate(rows):b+=R(x,190,815*pct,7,COLORS[i%6],3);x+=815*pct
        for i,(name,pct,label) in enumerate(rows):
            x=42+(i%2)*422;y=237+(i//2)*44;b+=C(x+4,y-4,4,COLORS[i%6])+T(x+19,y,name,12,ink)+T(x+372,y,label,12,mut,text_anchor='end')+P(f'M{x+19} {y+12}H{x+372}',t['border'],.5)
        b+=T(42,h-37,'Updated '+updated+' UTC · owned public repositories',10,mut)
    else:
        h=max(440,155+len(rows)*29);b=R(0,0,900,h,t['bg'])+R(0,0,900,h,'#b4a98c',opacity='.05',filter='url(#paper)')
        b+=T(35,30,'PUBLIC WORK / ACTIVITY LEDGER',10,a,font=MONO,letter_spacing=1)+P('M35 46H866',ink,1)
        for i,(v,label) in enumerate(values):b+=T(37,117+i*104,v,44,ink,font=SERIF)+T(39,143+i*104,label,14,mut,font=SERIF,font_style='italic')
        b+=P(f'M338 70V{h-54}',t['border'],1)+T(366,89,'Language',14,mut,font=SERIF)+T(862,89,'Share of code',14,mut,font=SERIF,text_anchor='end')
        for i,(name,pct,label) in enumerate(rows):
            y=123+i*29;b+=P(f'M366 {y+9}H863',t['border'],.6)+T(366,y,name,13,ink,font=SERIF)+T(862,y,label,13,ink,font=SERIF,text_anchor='end')+P(f'M549 {y-4}H{549+218*pct}',a,2)
        b+=P(f'M35 {h-41}H866',ink,1)+T(37,h-19,'Recorded '+updated+' UTC · Public repositories only',10,mut,font=MONO)
    if not rows:
        notice_ink={'aqua':'#294b69','aero':'#275b72','desktop95':'#111','construction':'#fff','matrix':'#67ff9c','phosphor':a}.get(k,mut)
        b+=T(365 if k in ('matrix','field-notes') else 35,228,'Statistics pending collection.' if data['status']!='ready' else 'No detected languages.',13,notice_ink)
    return svg(t,h,'Public activity: personal commits, filtered line edits, repositories and every detected language',b,css)


def label_card(t,selected=None,preview=False,number=None):
    """Era-specific navigation strips; these do not repeat section decorations."""
    k=t['id'];name=t['name'];era=t['era'];row=number is not None
    head=f'{number:02} / THEME COLLECTION' if row else ('THEME PREVIEW' if preview else 'CURRENT THEME')
    detail='Open theme →' if row else f"{'Preview updated' if preview else 'Selected'} {selected.isoformat()} UTC · {'fixed identity' if preview else 'daily rotation'}"
    h=130;a=t['accent'];ink=t['ink'];font=t['font'];css=''
    if k=='desktop95':
        b=R(0,0,900,h,'#087e7d')+window95(4,3,892,122,name)+T(23,62,head,10,'#444')+H(t,22,97,name,30,'#000080')+T(870,96,era,12,'#222',text_anchor='end')+T(23,116,detail,10,'#444')
    elif k=='construction':
        b=R(0,0,900,h,'#050523')+R(0,0,900,h,'url(#stars)')+T(24,28,head,11,'#ffef00',font=SERIF)+H(t,22,78,name,39,'#57f8ff')+T(25,109,detail,12,'#fff',font=SERIF)+T(875,107,era,12,'#ffff55',font=SERIF,text_anchor='end')
        b+=P('M7 124H893','#ffec00',4,stroke_dasharray='12 9')
    elif k=='phosphor':
        b=R(0,0,900,h,'#080f09',7)+R(0,0,900,h,'url(#scan)')+T(24,29,'> '+head,11,a,font=MONO)+H(t,23,78,name,35,a)+T(24,109,detail,10,a,font=MONO)+T(875,106,era,11,a,font=MONO,text_anchor='end')
    elif k=='matrix':
        b=R(0,0,900,h,'#020906')+P('M15 35V14H38 M862 116H885V95',a,2)+T(32,32,head,10,a,font=MONO,letter_spacing=2)+H(t,31,81,name,37,'#d1ffdf')+T(32,109,detail,10,a,font=MONO)+T(866,108,era,11,a,font=MONO,text_anchor='end')
    elif k=='y2k':
        b=R(0,0,900,h,'url(#chrome)',28)+P('M594 0H900L853 130H544Z','none',fill='#1e3476')+T(30,30,head,10,'#304567',letter_spacing=2)+H(t,27,82,name,41,'#182b57')+T(30,111,detail,10,'#304567')+T(857,103,era,11,'#dce6ff',text_anchor='end')
    elif k=='aqua':
        b=aqua_window(2,2,896,125,'Appearance')+H(t,24,87,name,40,'#274b6c')+T(25,112,detail,10,'#4e6982')+T(874,87,era,12,'#4e6982',text_anchor='end')
    elif k=='aero':
        b=R(0,0,900,h,'url(#sky)',13)+C(801,36,38,'#ffffff55')+R(13,13,874,104,'#ffffffaa',9,'#fff')+T(29,37,head,10,'#3a7692')+H(t,27,82,name,40,'#1a5c7d')+T(29,108,detail,10,'#3a7692')+T(868,103,era,12,'#3a7692',text_anchor='end')
    elif k=='metro':
        b=R(0,0,900,h,t['bg'])+R(0,0,14,h,a)+T(34,28,head,11,t['muted'])+H(t,31,82,name,45,ink)+T(35,113,detail,11,t['muted'])+T(870,104,era,12,t['muted'],text_anchor='end')
    elif k=='material':
        b=R(0,0,900,h,t['soft'])+R(8,5,884,115,t['bg'],6,filter='url(#shadow)')+R(8,5,7,115,a,3)+T(33,31,head,10,t['muted'],letter_spacing=1)+H(t,31,81,name,40,ink)+T(34,107,detail,10,t['muted'])+T(865,105,era,12,t['muted'],text_anchor='end')
    elif k=='glass':
        b=R(0,0,900,h,'url(#aurora)',20)+R(10,10,880,110,'url(#glass)',16,'#ffffff44')+T(31,33,head,10,'#dae6ff',letter_spacing=2)+H(t,29,82,name,40,'#fff')+T(32,109,detail,10,'#dae6ff')+T(869,106,era,12,'#dae6ff',text_anchor='end')
    else:
        b=R(0,0,900,h,t['bg'])+P('M24 17H876M24 120H876',ink,1)+T(25,36,head,9,a,font=MONO,letter_spacing=2)+H(t,23,85,name,43,ink)+T(25,109,detail,10,t['muted'],font=SERIF,font_style='italic')+T(873,107,era,12,t['muted'],font=SERIF,text_anchor='end')
    return svg(t,h,f"{'Explore' if row else 'Preview' if preview else 'Current theme'}: {name} — {era}",b,css)
