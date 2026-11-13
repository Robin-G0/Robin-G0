"""Illustrated motion in the biography's text-free lower margin."""


def about(t,a):
    k=t['id'];ink=t['ink'];accent=t['accent'];b='';css=''
    if k=='phosphor':
        b+=a.P('M35 179H864',accent,.6,opacity='.35')
        b+=a.T(36,204,'$ interests --scope current',11,accent,font=a.MONO)
        b+=a.T(36,232,'vision / quantum',12,accent,font=a.MONO)
        b+=a.R(193,220,7,13,accent,**{'class':'bio-terminal-cursor'})
        b+='<defs><clipPath id="bio-scope-frame"><rect x="490" y="187" width="371" height="56"/></clipPath></defs><g clip-path="url(#bio-scope-frame)">'
        b+=a.P('M490 219H860',accent,.5,opacity='.25')
        trace='M490 219H531L540 207 550 232 563 193 577 219H630L642 207 654 232 666 193 680 219H734L745 207 756 232 769 193 783 219H860'
        b+=a.P(trace,accent,1.4)+a.R(490,188,20,54,accent,opacity='.12',**{'class':'bio-scope-beam'})+'</g>'
        css='''.bio-terminal-cursor{animation:bio-terminal-blink 1.1s steps(1) infinite}.bio-scope-beam{animation:bio-scope-sweep 5s steps(38) infinite}
@keyframes bio-terminal-blink{50%{opacity:0}}@keyframes bio-scope-sweep{to{transform:translateX(371px)}}'''
    elif k=='desktop95':
        b+=a.P('M47 191H851','#b6bec5',1)
        # A small system-dialog hourglass, rather than another generic card.
        b+='<g transform="translate(64 214)"><g class="bio-hourglass">'+a.P('M-9 -12H9V-8L2 0 9 8V12H-9V8L-2 0 -9 -8Z','#37445a',1,'#edf7ff')+a.P('M-6 -7H6L0 -1Z M-6 9L0 3 6 9Z','none',fill='#c6a55c')+a.P('M-11 -13H11M-11 13H11','#000080',2)+'</g></g>'
        b+=a.T(87,219,'about.txt',12,'#4c5c70',font='Tahoma,sans-serif')
        b+='<g class="bio-dialog-button">'+a.button(t,749,201,'OK',w=89)+a.R(755,207,77,22,'none',0,'#444',stroke_dasharray='1 2')+'</g>'
        css='''.bio-hourglass{animation:bio-hourglass-turn 5s steps(1) infinite}.bio-dialog-button{animation:bio-dialog-press 8s steps(1) infinite}
@keyframes bio-hourglass-turn{0%,65%,100%{transform:rotate(0deg)}66%,90%{transform:rotate(180deg)}}
@keyframes bio-dialog-press{0%,84%,94%,100%{transform:translate(0)}85%,93%{transform:translate(1px,1px)}}'''
    elif k=='construction':
        b+='<defs><linearGradient id="bio-web-rainbow"><stop stop-color="#ff3890"/><stop offset=".25" stop-color="#ffee37"/><stop offset=".5" stop-color="#43ef8e"/><stop offset=".75" stop-color="#46dfff"/><stop offset="1" stop-color="#bc6cff"/></linearGradient><clipPath id="bio-web-footer"><rect x="26" y="182" width="845" height="62"/></clipPath></defs>'
        b+=a.R(29,250,842,3,'url(#bio-web-rainbow)')
        for i,(x,y) in enumerate(((48,205),(505,230),(756,193))):
            b+=f'<g transform="translate({x} {y})"><g class="bio-web-comet" style="animation-delay:-{i*2.1}s;animation-duration:{7+i*1.3}s">'+a.P('M0 0H-23M-7 -4H-18M-7 4H-18','#72d7ff',2)+a.R(-3,-3,6,6,'#fff')+'</g></g>'
        b+='<g transform="translate(443 216)"><g class="bio-web-mail">'+a.P('M-26 -15H26V16H-26Z','#ffff64',2,'#2523a4')+a.P('M-26 -15L0 5 26 -15 M-26 16L-8 0M26 16L8 0','#ffff64',2)+'</g></g>'
        css='''.bio-web-mail{animation:bio-mail-wiggle 3.7s steps(4) infinite}.bio-web-comet{animation:bio-comet 7s linear infinite}
@keyframes bio-mail-wiggle{0%,55%,100%{transform:rotate(0)}65%,85%{transform:rotate(-7deg)}75%,95%{transform:rotate(7deg)}}
@keyframes bio-comet{0%{transform:translateX(-35px);opacity:0}15%,75%{opacity:1}100%{transform:translateX(120px);opacity:0}}'''
    elif k=='matrix':
        b+='<defs><clipPath id="bio-vision-frame"><rect x="36" y="185" width="365" height="59"/></clipPath></defs><g clip-path="url(#bio-vision-frame)">'
        b+=a.R(36,185,365,59,'url(#graph)',0,'#173b28')
        for x,y in ((104,210),(226,222),(329,202)):
            b+=a.P(f'M{x-9} {y-3}V{y-9}H{x-3}M{x+3} {y-9}H{x+9}V{y-3}M{x+9} {y+3}V{y+9}H{x+3}M{x-3} {y+9}H{x-9}V{y+3}',accent,1)
            b+=a.C(x,y,2,'#e2ffe9',**{'class':'bio-vision-point','style':f'animation-delay:-{x/90:.2f}s'})
        b+=a.R(36,186,2,58,'#a6ffd0',**{'class':'bio-vision-scan'})+'</g>'
        b+='<g transform="translate(695 215)"><circle r="28" fill="none" stroke="#2d794b"/><ellipse rx="28" ry="9" fill="none" stroke="#2d794b"/><ellipse rx="10" ry="28" fill="none" stroke="#2d794b"/>'+a.P('M-39 0H39M0 -35V35',accent,.6,opacity='.6')+'<g class="bio-qubit-state">'+a.P('M0 0L18 -21',accent,1.4)+a.C(18,-21,3,'#dbffe8')+'</g></g>'
        css='''.bio-vision-scan{animation:bio-vision-scan 6s linear infinite}.bio-vision-point{animation:bio-vision-lock 4.3s steps(2) infinite}.bio-qubit-state{animation:bio-qubit 12s linear infinite}
@keyframes bio-vision-scan{from{transform:translateX(0)}to{transform:translateX(365px)}}@keyframes bio-vision-lock{0%,80%,100%{opacity:.45}30%,60%{opacity:1}}@keyframes bio-qubit{to{transform:rotate(360deg)}}'''
    elif k=='y2k':
        b+=a.P('M36 199H396L427 224H36Z','#8998bf',1,'url(#chrome)')
        b+=a.P('M490 199H846L861 224H490Z','#8998bf',1,'url(#chrome)')
        for i in range(18):
            h=8+(i*7%13)
            b+=a.R(52+i*18,211-h/2,8,h,'#324c95',**{'class':'bio-chrome-equalizer','style':f'animation-delay:-{i*.19:.2f}s'})
        b+='<defs><clipPath id="bio-chrome-track"><path d="M496 203H843L852 220H496Z"/></clipPath><linearGradient id="bio-chrome-glint"><stop stop-color="#7bd7ff" stop-opacity="0"/><stop offset=".5" stop-color="#fff"/><stop offset="1" stop-color="#7bd7ff" stop-opacity="0"/></linearGradient></defs>'
        b+='<g clip-path="url(#bio-chrome-track)">'+a.R(496,203,80,17,'url(#bio-chrome-glint)',**{'class':'bio-chrome-glint'})+'</g>'
        css='''.bio-chrome-equalizer{transform-box:fill-box;transform-origin:center;animation:bio-equalizer 2.4s ease-in-out infinite}.bio-chrome-glint{animation:bio-chrome-glint 5s cubic-bezier(.7,0,.2,1) infinite}
@keyframes bio-equalizer{0%,100%{transform:scaleY(.4);opacity:.5}40%{transform:scaleY(1);opacity:1}}
@keyframes bio-chrome-glint{0%,10%{transform:translateX(-80px)}80%,100%{transform:translateX(370px)}}'''
    elif k=='aqua':
        b+=a.P('M48 181H850','#b8c9d6',1)
        b+=a.R(53,201,365,15,'#92a9ba',8,'#728da2')+a.R(55,202,361,12,'url(#gel)',6)
        b+='<defs><clipPath id="bio-aqua-progress"><rect x="56" y="203" width="359" height="10" rx="5"/></clipPath></defs><g clip-path="url(#bio-aqua-progress)"><g class="bio-aqua-candy">'+a.R(31,202,409,13,'url(#candy)')+'</g></g>'+a.R(59,203,353,3,'#ffffff88',2)
        b+=a.R(498,207,341,5,'#c1d2de',3,'#8ea7ba')
        b+='<g class="bio-aqua-slider">'+a.C(523,209,9,'url(#gel)','#447daf')+a.C(520,206,3,'#fff',fill_opacity='.7')+'</g>'
        css='''.bio-aqua-candy{animation:bio-aqua-candy 1.5s linear infinite}.bio-aqua-slider{animation:bio-aqua-slider 12s ease-in-out infinite}
@keyframes bio-aqua-candy{to{transform:translateX(24px)}}@keyframes bio-aqua-slider{0%,15%,100%{transform:translateX(0)}45%,65%{transform:translateX(272px)}}'''
    elif k=='metro':
        b+='<defs><clipPath id="bio-metro-code"><rect x="41" y="185" width="102" height="52"/></clipPath></defs><g clip-path="url(#bio-metro-code)"><g class="bio-metro-code">'
        for y in (0,64):
            b+=a.P(f'M63 {197+y}L50 {210+y} 63 {223+y}M100 {197+y}L113 {210+y} 100 {223+y}M90 {191+y}L76 {229+y}','#fff',3)
        b+='</g></g>'
        b+=a.P('M503 217L559 195 612 225 667 199 721 221 777 194 833 214','#c5b6e8',1.5)
        for i,(x,y) in enumerate(((503,217),(559,195),(612,225),(667,199),(721,221),(777,194),(833,214))):
            b+=a.C(x,y,4,'#fff',**{'class':'bio-metro-network','style':f'animation-delay:-{i*.6}s'})
        css='''.bio-metro-code{animation:bio-metro-page 8s cubic-bezier(.1,.8,.2,1) infinite}.bio-metro-network{animation:bio-metro-signal 4.2s ease-in-out infinite}
@keyframes bio-metro-page{0%,35%,100%{transform:translateY(0)}48%,85%{transform:translateY(-64px)}}
@keyframes bio-metro-signal{0%,80%,100%{opacity:.35}20%,45%{opacity:1}}'''
    elif k=='material':
        b+=a.T(49,218,'RESEARCH',11,accent,font='Arial,sans-serif',letter_spacing=1)
        b+=a.T(233,218,'DEVELOPMENT',11,accent,font='Arial,sans-serif',letter_spacing=1)
        b+=a.P('M48 234H430',t['border'],1)
        b+=a.R(48,232,137,3,accent,**{'class':'bio-material-tab'})
        b+='<defs><clipPath id="bio-material-paper"><rect x="494" y="180" width="355" height="59"/></clipPath></defs><g clip-path="url(#bio-material-paper)">'
        for i in range(3):
            x=570+i*51
            b+=f'<g transform="translate({x} 185)"><g class="bio-material-page" style="animation-delay:-{i*1.2}s">'+a.R(0,0,83,64,t['soft'],3)+a.R(0,0,83,5,accent,fill_opacity='.35')+a.P('M14 22H68M14 33H58',t['border'],2)+'</g></g>'
        b+='</g>'
        css='''.bio-material-tab{animation:bio-material-tab 8s cubic-bezier(.4,0,.2,1) infinite}.bio-material-page{animation:bio-material-page 7s cubic-bezier(.4,0,.2,1) infinite}
@keyframes bio-material-tab{0%,30%,100%{transform:translateX(0)}45%,80%{transform:translateX(184px)}}
@keyframes bio-material-page{0%,100%{transform:translateY(12px)}50%{transform:translateY(-3px)}}'''
    elif k=='field-notes':
        b+=a.P('M37 211H428M39 205V228M427 205V228',t['muted'],.7)
        for i in range(19):
            x=51+i*20
            b+=a.P(f'M{x} 211V{219 if i%5 else 225}',t['muted'],.7)
        b+='<g transform="translate(69 211)"><g class="bio-notes-caliper">'+a.P('M0 -17V18H14M-2 -17H14V-8',ink,1.2)+a.P('M2 -8H12V10H2Z',ink,.6,t['goldbg'])+'</g></g>'
        b+=a.P('M536 217H839M554 184V237',t['border'],.8)
        b+=a.P('M569 220L605 208 646 216 689 190 733 205 780 185 824 194',accent,1.2,pathLength=1,stroke_dasharray=1,**{'class':'bio-notes-plot'})
        for i,(x,y) in enumerate(((569,220),(605,208),(646,216),(689,190),(733,205),(780,185),(824,194))):
            b+=a.C(x,y,2,t['bg'],accent,stroke_width='.8',**{'class':'bio-notes-point','style':f'animation-delay:{i*.55}s'})
        css='''.bio-notes-caliper{animation:bio-notes-measure 16s ease-in-out infinite}.bio-notes-plot{animation:bio-notes-plot 14s linear infinite}.bio-notes-point{animation:bio-notes-mark 14s linear infinite}
@keyframes bio-notes-measure{0%,12%,100%{transform:translateX(0)}45%,65%{transform:translateX(325px)}}
@keyframes bio-notes-plot{0%,5%{stroke-dashoffset:1}40%,90%{stroke-dashoffset:0}100%{stroke-dashoffset:1}}
@keyframes bio-notes-mark{0%,3%{opacity:0}8%,90%,100%{opacity:1}}'''
    return ('<g data-biography-detail="'+k+'" aria-hidden="true">'+b+'</g>' if b else ''),css
