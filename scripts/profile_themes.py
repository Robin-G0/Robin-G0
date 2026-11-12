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
    dict(id='construction', name='Under Construction', era='1996–2001', radius=0, font="'Times New Roman', Times, serif",
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
    dict(id='field-notes', name='Field Notes', era='Contemporary / original identity', radius=20, font='Georgia, serif',
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
    return {mode: dict(theme[mode], id=theme['id'], name=theme['name'], mode=mode,
                       era=theme['era'], radius=theme['radius'], font=theme['font'])
            for mode in ('light', 'dark')}
