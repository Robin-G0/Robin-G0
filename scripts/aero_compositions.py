"""Frutiger Aero as illustrated landscapes and objects, not framed UI cards.

Generated bitmap materials are embedded locally; typography and measured data
remain accessible SVG text/outlines. No runtime dependencies or scripts.
"""

from xml.sax.saxutils import escape


INK='#084b70'
MUTED='#286782'
BODY="'Tahoma','Verdana',sans-serif"
DISPLAY="'Segoe UI Light','Segoe UI',sans-serif"
EDITORIAL="Georgia,'Times New Roman',serif"


def definitions(a):
    # One bitmap shared by every language meter, instead of embedding it per row.
    return ('<pattern id="aero-meter-material" width="1" height="1" patternContentUnits="objectBoundingBox">'
            f'<image width="1" height="1" href="{a.embedded_asset("art/aero-meter-v3.png")}" preserveAspectRatio="none"/>'
            '</pattern>')


def sprite(a,name,x,y,w,h,fit='xMidYMid meet',**attrs):
    extra=' '.join(f'{k.replace("_","-")}="{escape(str(v))}"' for k,v in attrs.items())
    return f'<image x="{x}" y="{y}" width="{w}" height="{h}" href="{a.embedded_asset("art/"+name)}" preserveAspectRatio="{fit}" {extra}/>'


def background(a,name,height,uid):
    return (f'<defs><clipPath id="{uid}">{a.R(0,0,900,height,"#fff",20)}</clipPath></defs>'
            f'<g clip-path="url(#{uid})">'+a.bitmap('art/'+name,-7,-4,914,height+8,**{'class':'aero-wallpaper'}))


def heading(a,t,x,y,label,size=48,fill=INK):
    return a.H(t,x,y,label,size,fill,**{'class':'aero-heading'})


def copy(a,x,y,label,size=16,fill=INK,**attrs):
    return a.T(x,y,label,size,fill,font=BODY,**attrs)


def button(t,x,y,label,a,w=180):
    # A generated glass object, rather than another rounded SVG rectangle.
    return (sprite(a,'aero-button-v3.png',x,y,w,38,fit='none',data_aero_art='glass-button')
            +copy(a,x+w/2,y+24,label,13,'#fff',text_anchor='middle'))


def scene(t,kind,a):
    if kind=='flight':
        h=450;b=background(a,'aero-sky-v3.jpg',h,'aero-hero')
        b+=copy(a,41,56,'SOFTWARE ENGINEER',11,INK,letter_spacing=3)
        b+=heading(a,t,35,153,'Robin-G0',86)
        b+=a.T(42,201,'Research & development',24,MUTED,font=EDITORIAL,font_style='italic')
        b+=copy(a,43,238,'Computer vision / Systems / Quantum computing',13)
        plane=sprite(a,'aero-plane-v3.png',-35,-18,70,36,**{'class':'plane-attitude'})
        flight,css=a.flight_path(t,'M 89 358 Q 270 282 470 354','#237ba1','jet',22,plane_svg=plane)
        b+=flight+copy(a,47,412,'CANADA',11,letter_spacing=2)+copy(a,501,412,'FRANCE',11,text_anchor='end',letter_spacing=2)
        css+='''.plane-attitude{transform-box:fill-box;transform-origin:center;animation:airframe-level 22s linear infinite}@keyframes airframe-level{0%,49%{transform:scaleY(1)}50%,99%{transform:scaleY(-1)}100%{transform:scaleY(1)}}'''
        return a.svg(t,h,'Robin-G0: software engineer, Canada / France',b+'</g>',css)

    h=430
    b=background(a,'aero-instrument-v3.jpg',h,'aero-project')
    # An open editorial composition: the generated hand and device are the hero.
    b+=copy(a,39,45,'OPEN SOURCE / MOTION INPUT',10,MUTED,letter_spacing=2)
    b+=heading(a,t,35,120,'Motion',64)+heading(a,t,35,184,'Input Grid',64)
    b+=a.T(41,228,'Gesture recognition',20,MUTED,font=EDITORIAL,font_style='italic')
    b+=copy(a,41,266,'Body movements as application input.',14)
    b+=copy(a,41,292,'Websites, desktop apps and games.',14)
    b+=button(t,39,324,'Explore project',a,w=215)
    b+=copy(a,43,392,'Open source. Looking for testers.',12,MUTED)
    b+='<g class="aero-device">'+sprite(a,'aero-motion-device-v3.png',412,36,469,350,data_aero_art='gesture-device')+'</g>'
    # Recognition follows the object, rather than recreating a generic window.
    b+=a.C(710,206,21,'none','#2ab4df',stroke_width=1.5,**{'class':'device-recognition'})
    css='''.aero-device{animation:device-hover 9s ease-in-out infinite}.device-recognition{transform-box:fill-box;transform-origin:center;animation:device-recognition 5.5s ease-out infinite}@keyframes device-hover{50%{transform:translateY(-7px)}}@keyframes device-recognition{0%{transform:scale(.5);opacity:0}25%{opacity:.7}85%,100%{transform:scale(1.6);opacity:0}}'''
    return a.svg(t,h,'Motion Input Grid: open-source gesture recognition for web, desktop and games',b+'</g>',css)


def fish(a,name,x,y,w,h,route,klass,delay,duration,flip=False):
    face=' transform="scale(-1 1)"' if flip else ''
    return (f'<g class="fish-track {klass}" data-swimming-fish="{name}" '
            f'style="offset-path:path(\'{route}\');animation-delay:-{delay}s;animation-duration:{duration}s">'
            f'<g{face}><g class="fish-body">'+sprite(a,name,x,y,w,h)+'</g></g></g>')


def about(t,a):
    h=360;b=background(a,'aero-aquarium-v3.jpg',h,'aero-aquarium')
    b+=heading(a,t,40,56,'About me',35)
    b+=copy(a,42,100,'I’m a software engineer and',17)
    b+=copy(a,42,129,'full-stack developer,',17)
    b+=copy(a,42,160,'focused on research and development.',14,MUTED)
    b+=a.T(492,56,'Current interests',25,MUTED,font=EDITORIAL,font_style='italic')
    b+=copy(a,493,100,'Exploring computer vision and',16)
    b+=copy(a,493,129,'quantum computing at the moment.',16)
    # The whole lower strip is an aquarium lane, away from all biography text.
    b+=fish(a,'aero-fish-orange-v3.png',-62,-39,124,78,'M -130 257 C 240 217 610 310 1040 249','fish-gold',9,31)
    b+=fish(a,'aero-fish-blue-v3.png',-42,-22,84,44,'M 1020 299 C 680 333 250 260 -110 308','fish-blue',5,25,True)
    b+=fish(a,'aero-fish-blue-v3.png',-26,-14,52,28,'M -90 222 C 350 196 550 240 980 210','fish-small',15,38)
    css='''.fish-track{offset-distance:45%;offset-rotate:0deg;animation:fish-swim 31s linear infinite}.fish-blue{offset-distance:37%;opacity:.9}.fish-small{offset-distance:67%;opacity:.65}.fish-body{transform-box:fill-box;transform-origin:center;animation:fish-fin 1.8s ease-in-out infinite alternate}.fish-blue .fish-body{animation-duration:1.2s}.fish-small .fish-body{animation-duration:1.5s}@keyframes fish-swim{from{offset-distance:0%}to{offset-distance:100%}}@keyframes fish-fin{from{transform:skewX(-2deg) scaleY(.97)}to{transform:skewX(2deg) scaleY(1.02)}}'''
    return a.svg(t,h,'About me: software engineer and full-stack developer focused on research and development; exploring computer vision and quantum computing; swimming fish',b+'</g>',css)


def activity(t,data,a):
    rows=a.language_rows(data);values=a.metrics(data)
    h=300+max(len(rows),1)*31
    # Quiet white canvas for facts; ecological artwork forms the lower shoreline.
    b=a.R(0,0,900,h,'#f4fcff',20)
    b+='<defs><clipPath id="aero-report">'+a.R(0,0,900,h,'#fff',20)+'</clipPath></defs><g clip-path="url(#aero-report)">'
    b+=a.bitmap('art/aero-instrument-v3.jpg',0,h-265,900,320,opacity='.85')
    b+=heading(a,t,40,57,'GitHub activity',36)
    # Numbers stand on a ruled baseline, rather than inside three matching boxes.
    for i,(value,label) in enumerate(values):
        x=42+i*286
        b+=a.T(x,124,value,38,INK,font=DISPLAY)+copy(a,x+2,151,label,11,MUTED)
    b+=a.P('M42 174H856','#c0e2ed',1)
    for i,(name,pct,label) in enumerate(rows):
        y=210+i*31
        b+=copy(a,44,y,name,13)+copy(a,854,y,label,13,text_anchor='end')
        b+=a.R(213,y-11,540,12,'#cae9f0',6,'#b3d8e5')
        b+=a.meter(t,213,y-11,540*pct,12,'url(#aero-blue)',i,6)
    if not rows:
        b+=copy(a,44,220,'No detected languages.' if data['status']=='ready' else 'Statistics pending collection.',15)
    updated=data.get('updated') or 'pending'
    b+=copy(a,44,h-47,'Public repositories / Language share by bytes',10,MUTED)
    b+=copy(a,44,h-27,'Filtered additions + deletions / Updated '+updated+' UTC',10,MUTED)
    return a.svg(t,h,'Public activity: personal commits, filtered line edits, repositories and every detected language',b+'</g>')


def label_card(t,selected,preview,number,a):
    row=number is not None;h=144
    head=f'{number:02} / THEME COLLECTION' if row else 'THEME PREVIEW' if preview else 'CURRENT THEME'
    detail='Open theme →' if row else f'{"Preview updated" if preview else "Selected"} {selected.isoformat()} UTC / {"fixed identity" if preview else "daily rotation"}'
    b=background(a,'aero-sky-v3.jpg',h,'aero-title')
    # Fade to paper along the text edge, keeping the globe visible at the right.
    b+=a.P('M0 0H615L555 144H0Z','none',fill='#effbff',opacity='.88')
    b+=copy(a,29,28,head,9,MUTED,letter_spacing=2)
    b+=heading(a,t,25,86,'Frutiger Aero',43)
    b+=copy(a,30,121,detail,10,MUTED)
    b+=copy(a,863,123,t['era'],10,'#fff',text_anchor='end')
    return a.svg(t,h,'Frutiger Aero / '+head,b+'</g>')
