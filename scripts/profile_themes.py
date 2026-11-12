"""Visual eras and a reproducible daily shuffle, without external dependencies."""

from datetime import date
import hashlib
import random


def palette(bg, ink, muted, border, accent, soft, gold, goldbg):
    return dict(zip(('bg', 'ink', 'muted', 'border', 'accent', 'soft', 'gold', 'goldbg'),
                    (bg, ink, muted, border, accent, soft, gold, goldbg)))


THEMES = [
    dict(id='phosphor', name='Phosphor', era='1970–1989', radius=0, font='Consolas, monospace',
         light=palette('#101709','#c2fa89','#9dc878','#58833c','#b8ff6b','#24341a','#efd78c','#3a3420'),
         dark=palette('#070d07','#a5f7a0','#80bd7d','#355d35','#75f488','#172d1b','#dfe88a','#2e341a')),
    dict(id='desktop95', name='Desktop 95', era='1995–1998', radius=0, font='Tahoma, Arial, sans-serif',
         light=palette('#c0c0c0','#111111','#373737','#808080','#000080','#d7d7e5','#633800','#e9dab5'),
         dark=palette('#303b3b','#ffffff','#d0dada','#788888','#8fbaff','#445457','#ffe090','#5b5036')),
    dict(id='construction', name='Under Construction', era='1996–2001', radius=0, font='Verdana, sans-serif',
         light=palette('#10103b','#ffffff','#d1c5ff','#8d68ff','#62ffff','#26265b','#ffff55','#494124'),
         dark=palette('#080823','#ffffff','#ccc0ff','#745be0','#5affee','#20204b','#ffff55','#443d1d')),
    dict(id='matrix', name='Matrix / Construct', era='1999–2003', radius=2, font='Consolas, monospace',
         light=palette('#07160c','#c4ffcf','#91c69b','#265337','#42f587','#153721','#ddff9c','#324722'),
         dark=palette('#030c07','#b1ffc5','#83b890','#1b442c','#36ef77','#102b1b','#d5fa89','#293b19')),
    dict(id='y2k', name='Y2K Chrome', era='1999–2004', radius=36, font='Arial, sans-serif',
         light=palette('#edf0ff','#162254','#515b80','#a0aed2','#3734cc','#d9ddfa','#813c89','#f0d9f0'),
         dark=palette('#101329','#eef2ff','#b1badd','#5d688d','#9aabff','#28305a','#f0a8f2','#4d2b55')),
    dict(id='aqua', name='Aqua', era='2001–2007', radius=14, font='Lucida Grande, Verdana, sans-serif',
         light=palette('#f5faff','#172e4c','#4e6481','#9db7d0','#075fbb','#d1e9fd','#775d13','#f9edbd'),
         dark=palette('#172431','#e6f5ff','#a9c4d7','#4b6c87','#77c7ff','#28485f','#ffe19a','#51462c')),
    dict(id='aero', name='Frutiger Aero', era='2004–2012', radius=24, font='Trebuchet MS, sans-serif',
         light=palette('#effbff','#123b50','#39667b','#85bfcc','#076ca8','#c7e8f5','#41651b','#e1efb4'),
         dark=palette('#102c40','#e5faff','#a3cddc','#407a95','#83dbff','#204d65','#d1f58e','#3b542d')),
    dict(id='metro', name='Metro', era='2012–2016', radius=0, font='Segoe UI, Arial, sans-serif',
         light=palette('#ffffff','#162a40','#485e73','#c0cfda','#006ca9','#d9edf9','#7a3d7a','#f0dff2'),
         dark=palette('#101c2d','#ffffff','#b9cee2','#3a5474','#5fc5ff','#123e60','#efafff','#4a2858')),
    dict(id='material', name='Material', era='2014–2020', radius=8, font='Arial, sans-serif',
         light=palette('#faf9ff','#25263d','#62647e','#d5d5e8','#5946b2','#e9e2ff','#956300','#fff0c7'),
         dark=palette('#211e2b','#f3edff','#c0b6cf','#534b64','#c6b4ff','#3e3553','#ffcf78','#51412b')),
    dict(id='glass', name='Glass / Fluent', era='2020–2026', radius=28, font='Segoe UI, Arial, sans-serif',
         light=palette('#f1f3ff','#202440','#5e6481','#c4cbe9','#4b52ad','#dfe4fb','#84612c','#f4e6cb'),
         dark=palette('#1a2035','#f0f2ff','#b4bfdc','#4a557c','#b2bfff','#303d61','#f3d392','#514934')),
    dict(id='field-notes', name='Field Notes', era='Contemporary / original identity', radius=20, font='Segoe UI, Arial, sans-serif',
         light=palette('#f7f4ed','#202923','#586159','#cdcfc5','#245e51','#dce9df','#846119','#eee0bd'),
         dark=palette('#111c18','#e9efe8','#a6b8ac','#334b3e','#91d5af','#203e30','#e7c677','#443b24')),
]

EPOCH = date(2026, 1, 1)


def shuffled_cycle(cycle):
    order = list(range(len(THEMES)))
    seed = hashlib.sha256(f'Robin-G0/visual-eras/v1/{cycle}'.encode()).digest()
    random.Random(seed).shuffle(order)
    return order


def theme_for_day(day):
    """Visit each era once per cycle, with no repeat at cycle boundaries."""
    cycle, index = divmod((day - EPOCH).days, len(THEMES))
    order = shuffled_cycle(cycle)
    # Swapping only the first two leaves the previous cycle's last item intact.
    if order[0] == shuffled_cycle(cycle - 1)[-1]:
        order[0], order[1] = order[1], order[0]
    return THEMES[order[index]]


def variants(theme):
    return {mode: dict(theme[mode], id=theme['id'], name=theme['name'],
                       era=theme['era'], radius=theme['radius'], font=theme['font'])
            for mode in ('light', 'dark')}


def decoration(t, height):
    """Era-specific window chrome and scenery, behind the readable content."""
    k, a, s, g = t['id'], t['accent'], t['soft'], t['gold']
    css = ''
    body = ''
    if k == 'phosphor':
        body = ''.join(f'<path d="M2 {y} H898" stroke="{a}" opacity=".07"/>' for y in range(4, height, 4))
        body += f'<path d="M12 16 H28 M12 16 V32 M888 {height-16} H872 M888 {height-16} V{height-32}" fill="none" stroke="{a}"/>'
        css = 'text { font-family: Consolas, monospace; } .route { stroke-dasharray: 2 8; }'
    elif k == 'desktop95':
        body = f'<path d="M3 {height-4} V3 H896" fill="none" stroke="#fff" stroke-width="3"/><path d="M5 {height-4} H896 V5" fill="none" stroke="#555" stroke-width="3"/><rect x="6" y="6" width="888" height="16" fill="{a}"/>'
        body += ''.join(f'<rect x="{x}" y="9" width="10" height="10" fill="#c0c0c0" stroke="#fff"/>' for x in (848, 862, 876))
        css = 'rect:not(:first-of-type) { shape-rendering: crispEdges; } .bar { rx: 0; }'
    elif k == 'construction':
        body = ''.join(f'<path d="M{x-3} {y} h6 M{x} {y-3} v6" stroke="{g}" opacity=".4"/>' for x, y in [(12,60),(884,90),(480,64),(540,280),(20,height-23),(879,height-33)])
        body += f'<path d="M8 {height-7} H892" stroke="{g}" stroke-width="5" stroke-dasharray="12 8"/>'
        css = '.aircraft { filter: drop-shadow(3px 3px 0 #ff49d2); } .trigger { stroke-dasharray: 3 3; }'
    elif k == 'matrix':
        for i in range(14):
            x = 28 + i * 65
            glyphs = ''.join(f'<tspan x="{x}" dy="18">{(i*17+j*7)%2}</tspan>' for j in range(10))
            body += f'<text y="-160" fill="{a}" opacity=".08" font-family="monospace" font-size="13" class="rain" style="animation-delay:-{i*.7}s">{glyphs}</text>'
        css = f'.rain {{ animation: rain 9s linear infinite; fill: {a}; }} @keyframes rain {{ to {{ transform: translateY({height+180}px); }} }}'
    elif k == 'y2k':
        body = f'<defs><linearGradient id="chrome" x2="0" y2="1"><stop stop-color="#fff"/><stop offset=".45" stop-color="{s}"/><stop offset=".5" stop-color="{a}"/><stop offset="1" stop-color="#fff"/></linearGradient></defs><ellipse cx="760" cy="90" rx="125" ry="54" transform="rotate(-24 760 90)" fill="none" stroke="url(#chrome)" stroke-width="12" opacity=".24"/><path d="M38 13 H660" stroke="url(#chrome)" stroke-width="6"/>'
        css = '.aircraft { filter: drop-shadow(0 3px 3px #8899cc); } .trigger { stroke-width: 5; }'
    elif k == 'aqua':
        body = ''.join(f'<path d="M2 {y} H898" stroke="{a}" opacity=".035"/>' for y in range(3, height, 4))
        body += f'<defs><linearGradient id="gel" x2="0" y2="1"><stop stop-color="#fff"/><stop offset=".45" stop-color="{s}"/><stop offset="1" stop-color="{a}"/></linearGradient></defs><rect x="20" y="8" width="860" height="12" rx="6" fill="url(#gel)" opacity=".7"/>'
        css = '.bar { fill: url(#gel); } .trigger { stroke-width: 4; }'
    elif k == 'aero':
        body = f'<defs><linearGradient id="sky" x2="0" y2="1"><stop stop-color="{a}" stop-opacity=".16"/><stop offset="1" stop-color="{s}" stop-opacity="0"/></linearGradient></defs><rect x="2" y="2" width="896" height="{height-4}" rx="24" fill="url(#sky)"/><path d="M3 {height-26} Q210 {height-65} 450 {height-25} T897 {height-35} V{height-2} H3Z" fill="{g}" opacity=".12"/>'
        for x, y, r in [(821,55,22),(855,100,11),(565,75,14)]:
            body += f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" fill-opacity=".1" stroke="{a}" stroke-opacity=".2" class="bubble"/>'
        css = '.bubble { animation: bubble 5s ease-in-out infinite; } @keyframes bubble { 50% { transform: translateY(-6px); } } .bar { filter: drop-shadow(0 2px 1px #55889955); }'
    elif k == 'metro':
        body = f'<rect x="1" y="1" width="10" height="{height-2}" fill="{a}"/><rect x="803" y="12" width="24" height="10" fill="{a}"/><rect x="831" y="12" width="24" height="10" fill="{g}"/><rect x="859" y="12" width="24" height="10" fill="{t["muted"]}"/>'
        css = 'text { font-weight: 300; } rect { rx: 0; } .trigger { stroke-width: 4; }'
    elif k == 'material':
        body = f'<path d="M18 {height-5} H882" stroke="{t["border"]}" stroke-width="4"/><circle cx="858" cy="49" r="22" fill="{s}"/><path d="M851 49 H865 M858 42 V56" stroke="{a}" stroke-width="2"/>'
        css = '.trigger { stroke-width: 6; } .bar { filter: drop-shadow(0 2px 1px #00000022); }'
    elif k == 'glass':
        body = f'<defs><radialGradient id="glow"><stop stop-color="{a}" stop-opacity=".17"/><stop offset="1" stop-color="{a}" stop-opacity="0"/></radialGradient><linearGradient id="sheen" x2="1" y2="1"><stop stop-color="#fff" stop-opacity=".3"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/></linearGradient></defs><ellipse cx="740" cy="{height//2}" rx="155" ry="{height//2}" fill="url(#glow)"/><rect x="3" y="3" width="894" height="{height-6}" rx="26" fill="url(#sheen)" stroke="#fff" stroke-opacity=".18"/>'
        css = '.aircraft { filter: drop-shadow(0 0 5px #9baaff); } .bar { rx: 5; }'
    else:
        body = f'<path d="M16 30 V16 H30 M870 {height-16} H884 V{height-30}" fill="none" stroke="{t["border"]}"/>'
    return body, css
