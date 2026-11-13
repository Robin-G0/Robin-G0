"""Code-native materials and motion. No script, remote resource or SMIL needed."""

import re
AURORA_PERIOD=900
AURORA_LAYERS=(('far',180,.8),('mid',130,.65),('near',90,.75))


def definitions(theme):
    resources = '''
<linearGradient id="aqua-title" x2="0" y2="1"><stop stop-color="#fcfdff"/><stop offset=".45" stop-color="#edf0f3"/><stop offset="1" stop-color="#c5cbd2"/></linearGradient>
<linearGradient id="aqua-toolbar" x2="0" y2="1"><stop stop-color="#edf1f5"/><stop offset="1" stop-color="#cbd4dd"/></linearGradient>
<linearGradient id="aero-blue" x2="0" y2="1"><stop stop-color="#b9f5ff"/><stop offset=".46" stop-color="#38b6ed"/><stop offset=".5" stop-color="#087cc5"/><stop offset="1" stop-color="#06579e"/></linearGradient>
<radialGradient id="bubble" cx=".28" cy=".2" r=".8"><stop stop-color="#fff" stop-opacity=".8"/><stop offset=".22" stop-color="#d6fbff" stop-opacity=".08"/><stop offset=".73" stop-color="#46a8dd" stop-opacity=".04"/><stop offset=".94" stop-color="#ddffff" stop-opacity=".48"/><stop offset="1" stop-color="#fff" stop-opacity=".12"/></radialGradient>
<pattern id="candy" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M-6 24L18 0M6 24L30 0" stroke="#b9edff" stroke-width="5" opacity=".45"/></pattern>
<pattern id="hatch" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M-12 24L12 0M0 24L24 0M12 24L36 0" stroke="#100b3b" stroke-width="5" opacity=".48"/></pattern>
<filter id="glass-lens" x="-10%" y="-15%" width="120%" height="130%" color-interpolation-filters="sRGB"><feTurbulence type="fractalNoise" baseFrequency=".006 .014" numOctaves="2" seed="8" result="noise"/><feDisplacementMap in="SourceGraphic" in2="noise" scale="42" xChannelSelector="R" yChannelSelector="G"/><feGaussianBlur stdDeviation="2.5"/><feColorMatrix type="saturate" values="1.35"/></filter>
<linearGradient id="lens-edge" x2=".8" y2="1"><stop stop-color="#fff" stop-opacity=".95"/><stop offset=".25" stop-color="#e1faff" stop-opacity=".14"/><stop offset=".65" stop-color="#91d9ff" stop-opacity=".08"/><stop offset="1" stop-color="#fff" stop-opacity=".65"/></linearGradient>
'''
    needed={'aqua':('aqua-title','aqua-toolbar','candy'),
            'aero':('aero-blue','bubble'), 'construction':('hatch',),
            'glass':('glass-lens','lens-edge')}.get(theme,())
    return ''.join(node.group(0) for node in re.finditer(r'<(linearGradient|radialGradient|pattern|filter) id="([^"]+)".*?</\1>',resources)
                   if node.group(2) in needed)


MOTION = {
    'phosphor': '.era-copy{animation:terminal-write 17s steps(38,end) infinite}.meter-head{animation:meter-step 6s steps(20,end) infinite}',
    'desktop95': '.era-copy{animation:dialog-focus 14s steps(1) infinite}.meter-head{animation:meter-step 7s steps(18,end) infinite}',
    'construction': '.era-copy{animation:web-link 9s steps(1) infinite}.meter-texture{animation:stripe-scroll 1s linear infinite}',
    'matrix': '.era-copy{animation:decode-write 19s steps(32,end) infinite}.meter-head{animation:meter-step 8s steps(24,end) infinite}',
    'y2k': '.era-copy{animation:chrome-copy 13s ease-in-out infinite}.meter-head{animation:chrome-sweep 5s cubic-bezier(.7,0,.2,1) infinite}',
    'aqua': '.era-copy{animation:aqua-copy 15s ease-in-out infinite}.meter-texture{animation:stripe-scroll 1.7s linear infinite}.gel-breathe{animation:gel-breathe 4s ease-in-out infinite}',
    'aero': '.era-copy{animation:aero-copy 16s ease-in-out infinite}.meter-head{animation:aero-sweep 6s ease-in-out infinite}.aero-wallpaper{animation:aero-current 21s ease-in-out infinite alternate}.bubble-rise{animation:bubble-rise 13s ease-in-out infinite alternate}.gel-breathe{animation:gel-breathe 6s ease-in-out infinite}',
    'metro': '.era-copy{animation:metro-copy 15s cubic-bezier(.1,.8,.2,1) infinite}.meter-dot{animation:metro-dot 4s cubic-bezier(.1,.8,.8,.1) infinite}',
    'material': '.era-copy{animation:paper-copy 16s cubic-bezier(.4,0,.2,1) infinite}.meter-head{animation:material-sweep 6s cubic-bezier(.4,0,.2,1) infinite}',
    'glass': '.era-copy{animation:glass-copy 18s ease-in-out infinite}.meter-head{animation:glass-sweep 8s ease-in-out infinite}',
    'field-notes': '.era-copy{animation:pen-copy 21s linear infinite}.meter-ink{animation:ink-dry 9s ease-out infinite}',
}


def motion(theme):
    selectors=MOTION.get(theme, '')
    if theme=='glass':
        selectors+=''.join(f'.aurora-{name}{{animation:aurora-current {duration}s linear -{duration*.23:g}s infinite;}}'
                           for name,duration,_ in AURORA_LAYERS)
    keyframes='''
@keyframes meter-step{0%,12%{transform:translateX(-40px)}75%,100%{transform:translateX(var(--travel))}}
@keyframes stripe-scroll{to{transform:translateX(24px)}}
@keyframes chrome-sweep{0%,15%{transform:translateX(-40px)}70%,100%{transform:translateX(var(--travel))}}
@keyframes aero-sweep{0%,8%{transform:translateX(-50px);opacity:0}25%{opacity:.85}80%,100%{transform:translateX(var(--travel));opacity:0}}
@keyframes metro-dot{0%,8%{transform:translateX(-30px);opacity:0}20%,75%{opacity:1}95%,100%{transform:translateX(var(--travel));opacity:0}}
@keyframes material-sweep{0%,22%{transform:translateX(-50px) scaleX(.3)}60%{transform:translateX(calc(var(--travel)*.4)) scaleX(1.5)}90%,100%{transform:translateX(var(--travel)) scaleX(.3)}}
@keyframes glass-sweep{0%,12%{transform:translateX(-50px);opacity:0}30%{opacity:.7}88%,100%{transform:translateX(var(--travel));opacity:0}}
@keyframes ink-dry{0%,100%{opacity:.65}25%,80%{opacity:1}}
@keyframes terminal-write{0%,2%{clip-path:inset(0 100% 0 0)}19%,100%{clip-path:inset(0 0 0 0)}}
@keyframes decode-write{0%,3%{clip-path:inset(0 100% 0 0);opacity:.4}20%,100%{clip-path:inset(0);opacity:1}}
@keyframes dialog-focus{0%,88%{opacity:1}89%,92%{opacity:.6}93%,100%{opacity:1}}
@keyframes web-link{0%,84%,100%{text-decoration:underline}85%,94%{text-decoration:none}}
@keyframes chrome-copy{0%,100%{letter-spacing:1px}50%{letter-spacing:1.6px}}
@keyframes aqua-copy{0%,85%,100%{opacity:1}92%{opacity:.72}}
@keyframes aero-copy{0%,100%{opacity:1}50%{opacity:.8}}
@keyframes aero-current{to{transform:translate(5px,2px)}}
@keyframes metro-copy{0%,2%{transform:translateY(6px);opacity:0}9%,94%{transform:translateY(0);opacity:1}100%{opacity:0}}
@keyframes paper-copy{0%,2%{transform:translateY(5px);opacity:0}10%,100%{transform:translateY(0);opacity:1}}
@keyframes glass-copy{0%,100%{opacity:.8}45%,75%{opacity:1}}
@keyframes pen-copy{0%,2%{clip-path:inset(0 100% 0 0)}8%{clip-path:inset(0 65% 0 0)}12%{clip-path:inset(0 65% 0 0)}24%,100%{clip-path:inset(0)}}
@keyframes gel-breathe{50%{opacity:.45}}
@keyframes bubble-rise{to{transform:translate(9px,-24px)}}
@keyframes aurora-current{from{transform:translateX(0)}to{transform:translateX(-900px)}}
'''
    names=set(re.findall(r'animation:([\w-]+)',selectors))
    frames=''.join(match.group(0) for match in re.finditer(r'@keyframes ([\w-]+)\{(?:[^{}]|\{[^{}]*\})*\}',keyframes)
                   if match.group(1) in names)
    return selectors+frames+'''.era-copy{transform-box:fill-box;animation-delay:var(--copy-phase,0s)}.meter-head,.meter-dot{animation-delay:var(--phase,0s)!important}'''


def aurora_resources(embedded_asset):
    """One copy of each photographic layer, shared by the field and its lens."""
    resources='<linearGradient id="aurora-feather"><stop stop-color="#fff" stop-opacity="0"/><stop offset=".16" stop-color="#fff"/><stop offset=".84" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
    resources+='<mask id="aurora-tile-mask" maskUnits="userSpaceOnUse" x="0" y="0" width="900" height="440"><rect width="900" height="440" fill="url(#aurora-feather)"/></mask>'
    for name,_,_ in AURORA_LAYERS:
        uri=embedded_asset('art/glass-aurora-'+name+'-v1.png')
        resources+=(f'<pattern id="aurora-photo-{name}" patternUnits="userSpaceOnUse" width="{AURORA_PERIOD}" height="440">'
                    f'<image width="900" height="440" href="{uri}" preserveAspectRatio="none" mask="url(#aurora-tile-mask)"/></pattern>')
    return resources


def waves(height=440):
    """Same-direction photographic parallax; exact repeats avoid a reset flash."""
    body=(f'<g transform="scale(1 {height/440:.4f})" aria-hidden="true">'
          '<rect width="900" height="440" fill="url(#aurora)"/>')
    for name,_,opacity in AURORA_LAYERS:
        body+=(f'<g class="aurora-{name}" data-aurora-layer="{name}">'
               f'<rect x="-900" y="0" width="3600" height="440" fill="url(#aurora-photo-{name})" opacity="{opacity}"/></g>')
    return body+'</g>'


def glass_backdrop(height=440):
    return f'<defs><clipPath id="glass-frame"><rect width="900" height="{height}" rx="24"/></clipPath></defs><g clip-path="url(#glass-frame)">{waves(height)}</g>'


def lens(x,y,w,h,height=440,uid='panel',radius=24):
    # Text is drawn later, outside the filter. Duplicate only the backdrop.
    return f'''<defs><clipPath id="lens-{uid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}"/></clipPath></defs>
<g clip-path="url(#lens-{uid})" data-material="refracted-backdrop"><g filter="url(#glass-lens)">{waves(height)}</g></g>
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="#142342" fill-opacity=".28" stroke="url(#lens-edge)" stroke-width="1.5"/>
<rect x="{x+2}" y="{y+2}" width="{w-4}" height="{h-4}" rx="{radius-2}" fill="url(#glass)" stroke="#ffffff18"/>
'''


def bubbles():
    return ''.join(f'''<g class="bubble-rise" style="animation-duration:{duration}s;animation-delay:-{i*2.1}s"><circle cx="{x}" cy="{y}" r="{r}" fill="url(#bubble)" stroke="#eaffff" stroke-opacity=".45"/><path d="M{x-r*.6} {y-r*.4}Q{x-r*.3} {y-r*.9} {x+r*.15} {y-r*.75}" fill="none" stroke="#fff" stroke-width="2" opacity=".8"/></g>'''
                   for i,(x,y,r,duration) in enumerate(((563,77,22,13),(848,191,34,17),(582,386,13,11),(802,365,20,19))))


def copy_motion(body,theme):
    """Animate secondary notes with staggered timing; keep headings and data still."""
    if theme not in MOTION:
        return body
    count=0
    def replace(match):
        nonlocal count
        node=match.group(0)
        label=match.group(1)
        eligible=('$ ' in label or 'testers' in label.lower() or 'research' in label.lower()
                  or 'open-source' in label.lower() or 'LANGUAGE DISTRIBUTION' in label)
        if not eligible or 'class=' in node:
            return node
        # Several short independently delayed notes; no window titles or numbers.
        count+=1
        return node.replace('<text ', f'<text class="era-copy" style="--copy-phase:{(count-1)*.53:.2f}s" ', 1)
    return re.sub(r'<text\b[^>]*>([^<]+)</text>', replace, body)
