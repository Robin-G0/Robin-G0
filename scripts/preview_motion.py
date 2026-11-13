"""Small era-specific moving illustrations for collection rows and title cards."""


def illustration(t, a):
    k=t['id'];accent=t['accent'];body='';css=''
    if k=='phosphor':
        body=a.T(620,33,'SIGNAL / ONLINE',9,accent,font=a.MONO,letter_spacing=1)
        body+=a.P('M619 74H646L655 61 666 84 681 43 694 74H724L735 64 747 78H850',accent,1.5)
        body+='<g class="preview-terminal-head">'+a.R(617,42,3,45,accent,opacity='.65')+'</g>'
        body+=a.R(845,22,7,12,accent,**{'class':'preview-terminal-cursor'})
        css='''.preview-terminal-head{animation:preview-terminal 4.5s steps(35) infinite}.preview-terminal-cursor{animation:preview-cursor 1.1s steps(1) infinite}
@keyframes preview-terminal{0%{transform:translateX(0);opacity:0}6%,90%{opacity:.7}100%{transform:translateX(235px);opacity:0}}
@keyframes preview-cursor{50%{opacity:0}}'''
    elif k=='desktop95':
        for x in (626,799):
            body+=a.P(f'M{x} 54V43H{x+19}L{x+6+19} 49H{x+42}V77H{x}Z','#836700',1,'#f1cf56')
            body+=a.P(f'M{x} 54H{x+44}L{x+40} 78H{x-3}Z','#836700',1,'#ffe594')
        sheet=a.P('M0 0H13L19 6V25H0Z','#555',1,'#fff')+a.P('M13 0V6H19M4 11H14M4 15H14M4 19H11','#000080',1)
        body+='<g transform="translate(676 38)"><g class="preview-copy-file">'+sheet+'</g></g>'
        body+=a.R(682,79,104,8,'#fff',0,'#808080')
        body+='<g class="preview-copy-progress">'+''.join(a.R(685+i*8,81,6,4,'#000080') for i in range(12))+'</g>'
        css='''.preview-copy-file{animation:preview-copy 3.6s steps(12) infinite}.preview-copy-progress{clip-path:inset(0);animation:preview-copy-blocks 3.6s steps(12) infinite}
@keyframes preview-copy{0%{transform:translate(-42px,9px);opacity:0}12%{opacity:1}55%{transform:translate(26px,-10px)}85%{opacity:1}100%{transform:translate(119px,9px);opacity:0}}
@keyframes preview-copy-blocks{from{clip-path:inset(0 100% 0 0)}to{clip-path:inset(0)}}'''
    elif k=='construction':
        body+='<g class="preview-web-globe">'+a.globe(735,56,29,'#032f9f','#59ef8a',True)+'</g>'
        for x,y,delay in ((646,46,0),(814,30,1.7),(847,72,3.1)):
            body+=a.P(f'M{x-6} {y}H{x+6}M{x} {y-6}V{y+6}','#ffff66',2,**{'class':'preview-web-star','style':f'animation-delay:-{delay}s'})
        css='''.preview-web-globe{transform-origin:735px 56px;animation:preview-web-spin 16s linear infinite}.preview-web-star{animation:preview-web-glint 4.7s steps(2) infinite}
@keyframes preview-web-spin{to{transform:rotate(360deg)}}@keyframes preview-web-glint{0%,70%,100%{opacity:1}80%,90%{opacity:.15}}'''
    elif k=='matrix':
        body='<defs><clipPath id="preview-rain-frame"><rect x="605" y="9" width="252" height="80"/></clipPath></defs><g clip-path="url(#preview-rain-frame)">'
        for i in range(17):
            x=610+i*15
            chars=''.join(f'<tspan x="{x}" dy="13">{(i*7+j*3)%10}</tspan>' for j in range(9))
            body+=f'<text y="-120" fill="{accent}" font-family="{a.MONO}" font-size="10" opacity=".45" class="preview-rain" style="animation-duration:{4+i%4*.7}s;animation-delay:-{i*.61:.2f}s">{chars}<tspan x="{x}" dy="13" fill="#e6ffed">1</tspan></text>'
        body+='</g>'
        css='''.preview-rain{animation:preview-rain 5s linear infinite}@keyframes preview-rain{to{transform:translateY(235px)}}'''
    elif k=='y2k':
        body='<g transform="translate(736 49)"><g class="preview-chrome-ring">'+a.aero.sprite(a,'y2k-chrome-orbit-v1.png',-106,-49,212,98)+'</g></g>'
        css='''.preview-chrome-ring{animation:preview-orbit 9s ease-in-out infinite}@keyframes preview-orbit{0%,100%{transform:translateY(3px) rotate(-3deg)}50%{transform:translateY(-3px) rotate(3deg)}}'''
    elif k=='aqua':
        body=a.R(620,48,218,19,'#8ca6bb',10,'#627f9b')+a.R(622,49,214,16,'url(#gel)',8)
        body+='<defs><clipPath id="preview-aqua-track"><rect x="623" y="50" width="212" height="14" rx="7"/></clipPath></defs><g clip-path="url(#preview-aqua-track)"><g class="preview-aqua-stripes">'+a.R(598,49,264,17,'url(#candy)')+'</g></g>'
        body+=a.R(627,50,204,5,'#ffffff80',3)
        css='''.preview-aqua-stripes{animation:preview-aqua-flow 1.4s linear infinite}@keyframes preview-aqua-flow{to{transform:translateX(24px)}}'''
    elif k=='aero':
        for i,(x,y,r) in enumerate(((651,58,17),(825,39,11),(793,80,23))):
            body+=f'<g class="preview-aero-bubble" style="animation-delay:-{i*2.3}s;animation-duration:{8+i*2}s">'+a.C(x,y,r,'url(#bubble)','#f5ffff',stroke_opacity='.55')+a.P(f'M{x-r*.55} {y-r*.4}Q{x-r*.3} {y-r*.82} {x+r*.2} {y-r*.7}','#fff',1.5,opacity='.8')+'</g>'
        css='''.preview-aero-bubble{animation:preview-aero-rise 10s ease-in-out infinite alternate}@keyframes preview-aero-rise{from{transform:translate(-4px,9px)}to{transform:translate(7px,-13px)}}'''
    elif k=='metro':
        for i,color in enumerate(('#0078ad','#7434a6','#009f86')):
            x=626+i*70
            body+=f'<g transform="translate({x} 20)"><g class="preview-live-tile" style="animation-delay:-{i*1.4}s">'+a.R(0,0,62,49,color)
            if i==0:body+=a.P('M17 15H45V34H17ZM17 15L31 26 45 15','#fff',1.5)
            elif i==1:body+=a.P('M20 19H25L28 14H36L39 19H44V35H20Z','#fff',1.5)+a.C(32,27,6,'none','#fff')
            else:body+=a.P('M19 17H25V23H19ZM36 17H42V23H36ZM19 30H25V36H19ZM36 30H42V36H36Z','#fff',1,'#fff')
            body+='</g></g>'
        for i in range(5):
            body+=a.C(625,84,2,accent,**{'class':'preview-metro-dot','style':f'animation-delay:-{i*.19}s'})
        css='''.preview-live-tile{transform-origin:31px 24px;animation:preview-tile 7s cubic-bezier(.1,.8,.2,1) infinite}.preview-metro-dot{animation:preview-metro-travel 3.2s cubic-bezier(.1,.8,.8,.1) infinite}
@keyframes preview-tile{0%,70%,100%{transform:scaleY(1)}77%{transform:scaleY(.04)}84%{transform:scaleY(1)}}
@keyframes preview-metro-travel{0%,8%{transform:translateX(0);opacity:0}18%,75%{opacity:1}90%,100%{transform:translateX(202px);opacity:0}}'''
    elif k=='material':
        body='<defs><clipPath id="preview-paper-frame"><rect x="618" y="18" width="224" height="72" rx="4"/></clipPath></defs><g clip-path="url(#preview-paper-frame)">'
        body+=a.R(618,18,224,72,t['soft'],4)
        body+='<g class="preview-paper-sheet">'+a.R(641,30,153,71,t['bg'],3,filter='url(#shadow)')+a.R(641,30,153,6,accent)+a.P('M657 52H776M657 64H732',t['border'],3)+'</g>'
        body+='<g transform="translate(788 70)"><g class="preview-paper-ripple">'+a.C(0,0,28,accent,fill_opacity='.22')+'</g></g></g>'
        css='''.preview-paper-sheet{animation:preview-paper-lift 7s cubic-bezier(.4,0,.2,1) infinite}.preview-paper-ripple{animation:preview-paper-touch 4s cubic-bezier(.4,0,.2,1) infinite}
@keyframes preview-paper-lift{0%,100%{transform:translateY(4px)}50%{transform:translateY(-6px)}}
@keyframes preview-paper-touch{0%{transform:scale(.1);opacity:0}10%{opacity:.8}75%,100%{transform:scale(2.5);opacity:0}}'''
    elif k=='glass':
        # Keep the photographic aurora as the entire illustration, rather than
        # placing an unrelated spinner on top of the glass.
        css='''.glass-scene-identity .aurora-far{animation-duration:144s}.glass-scene-identity .aurora-mid{animation-duration:104s}.glass-scene-identity .aurora-near{animation-duration:72s}'''
    else:
        route='M 625 77 C 653 77 656 42 682 42 S 726 80 753 61 S 794 27 833 42'
        body+=a.P('M620 88H844M622 26V89',t['border'],1)
        body+=''.join(a.P(f'M{x} 85V91',t['border'],1) for x in range(642,843,20))
        body+=a.P(route,accent,1.5,pathLength=1,stroke_dasharray=1,**{'class':'preview-ink-line'})
        nib=a.P('M0 0L-14 -4 -9 -12Z',t['ink'],1,t['gold'])+a.P('M-14 -4L-34 -25 -29 -32 -9 -12',t['ink'],1,t['bg'])
        body+='<g class="preview-pen">'+nib+'</g>'
        css=f'''.preview-ink-line{{animation:preview-ink 10s linear infinite}}.preview-pen{{offset-path:path('{route}');offset-distance:100%;offset-rotate:0deg;animation:preview-pen 10s linear infinite}}
@keyframes preview-ink{{0%,5%{{stroke-dashoffset:1}}55%,90%{{stroke-dashoffset:0}}100%{{stroke-dashoffset:1}}}}
@keyframes preview-pen{{0%,5%{{offset-distance:0%;opacity:1}}55%{{offset-distance:100%;opacity:1}}65%,90%{{offset-distance:100%;opacity:0}}100%{{offset-distance:0%;opacity:0}}}}'''
    return f'<g data-preview-motion="{k}" aria-hidden="true">{body}</g>',css
