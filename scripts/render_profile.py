"""Generate the profile's SVG cards. Python standard library only.

Run with --refresh to collect public GitHub statistics; otherwise use the last
saved snapshot. All graphics share the palette below, ready for the Pages site.
"""

import argparse
from datetime import date, datetime, timezone
import json
from pathlib import Path
import re
from xml.sax.saxutils import escape

if __package__:
    from .profile_themes import THEMES, decoration, theme_for_day, variants
    from .profile_stats import CollectionError, collect, pending
else:
    from profile_themes import THEMES, decoration, theme_for_day, variants
    from profile_stats import CollectionError, collect, pending

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
SNAPSHOT = ASSETS / "stats.json"
THEME_STATE = ASSETS / "theme.json"


def text(x, y, value, cls="", size=16, extra=""):
    return f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}" {extra}>{escape(str(value))}</text>'


def card(t, height, title, body, css=""):
    scenery, era_css = decoration(t, height)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="{height}" viewBox="0 0 900 {height}" role="img" aria-labelledby="title">
<title id="title">{escape(title)}</title>
<style>
text {{ font-family: {t['font']}; fill: {t['ink']}; }}
.mono {{ font-family: Consolas, 'Liberation Mono', monospace; letter-spacing: 2px; fill: {t['muted']}; }}
.muted {{ fill: {t['muted']}; }}
.accent {{ fill: {t['accent']}; }}
.gold {{ fill: {t['gold']}; }}
{css}
{era_css}
@media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} .trail {{ stroke-dashoffset: 0 !important; }} }}
</style>
<rect x="1" y="1" width="898" height="{height-2}" rx="{t['radius']}" fill="{t['bg']}" stroke="{t['border']}"/>
{scenery}
{body}
</svg>
'''


def flight(t):
    # The plane points along the direction of travel, including the return leg.
    route = "M 180 236 C 320 130 580 130 720 236"
    body = text(36, 43, "ROBIN-G0 / IDEAS ACROSS ERAS", "mono", 12)
    body += text(36, 93, "Ideas in motion.", size=42, extra='font-weight="700"')
    body += text(36, 124, "Software engineering · Research & development", "muted", 18)
    body += f'<path d="{route}" fill="none" stroke="{t["border"]}" stroke-width="2" stroke-dasharray="4 8"/>'
    for x, name, code in [(180, "CANADA", "CA"), (720, "FRANCE", "FR")]:
        body += f'<circle cx="{x}" cy="236" r="7" fill="{t["soft"]}" stroke="{t["accent"]}" stroke-width="2"/>'
        body += text(x, 274, name, "mono", 14, 'text-anchor="middle"')
        body += text(x, 297, code, "muted", 12, 'text-anchor="middle"')
    body += f'''<g class="aircraft">
<g fill="{t['accent']}" stroke="{t['bg']}" stroke-width="1.5" stroke-linejoin="round">
<path d="M20 0 Q20 -3 13 -3 L3 -3 L-8 -18 L-13 -18 L-7 -3 L-16 -3 L-21 -9 L-24 -9 L-21 0 L-24 9 L-21 9 L-16 3 L-7 3 L-13 18 L-8 18 L3 3 L13 3 Q20 3 20 0 Z"/>
</g></g>'''
    # CSS offset-path keeps reduced-motion support in the same image.
    css = f'''.aircraft {{ offset-path: path('{route}'); offset-rotate: auto; offset-distance: 50%; animation: flight 16s linear infinite; }}
@keyframes flight {{ 0%, 6% {{ offset-distance: 0%; offset-rotate: auto; }} 44%, 49% {{ offset-distance: 100%; offset-rotate: auto; }} 50%, 56% {{ offset-distance: 100%; offset-rotate: reverse; }} 94%, 99% {{ offset-distance: 0%; offset-rotate: reverse; }} 100% {{ offset-distance: 0%; offset-rotate: auto; }} }}'''
    return card(t, 328, "Robin-G0 — an airplane travels between Canada and France", body, css)


def mig(t):
    body = text(36, 43, "01 / CURRENT PROJECT", "mono", 12)
    body += text(36, 96, "Motion Input Grid", size=34, extra='font-weight="700"')
    body += text(36, 133, "Turn a movement into an action.", "accent", 20)
    body += text(36, 176, "An open-source motion input framework", "muted", 16)
    body += text(36, 202, "for websites, desktop applications and games.", "muted", 16)
    body += f'<rect x="36" y="238" width="172" height="36" rx="18" fill="{t["soft"]}"/>'
    body += text(53, 262, "LOOKING FOR TESTERS", "accent", 12, 'font-weight="700"')
    body += text(228, 262, "Explore the project →", "accent", 15)
    positions = [(606 + col * 68, 74 + row * 68) for row in range(3) for col in range(3)]
    for i, (x, y) in enumerate(positions):
        fill = t["goldbg"] if i == 5 else t["soft"] if i in (0, 3, 4) else t["bg"]
        body += f'<rect x="{x}" y="{y}" width="58" height="58" rx="10" fill="{fill}" stroke="{t["border"]}"/>'
    for order, i in enumerate((0, 3, 4, 5)):
        x, y = positions[i]
        body += text(x + 9, y + 17, order + 1 if i != 5 else "GO", "gold" if i == 5 else "accent", 11, 'font-weight="700"')
    body += f'<path d="M635 103 V171 H771" class="trail" pathLength="1" fill="none" stroke="{t["accent"]}" stroke-width="3" stroke-linecap="round" stroke-dasharray="1"/>'
    body += f'<circle cx="771" cy="171" r="23" class="trigger" fill="none" stroke="{t["gold"]}" stroke-width="2"/>'
    body += text(704, 301, "MOVE → MATCH → TRIGGER", "mono", 10, 'text-anchor="middle"')
    css = '''.trail { animation: draw 6s ease-in-out infinite; }
@keyframes draw { 0%, 8% { stroke-dashoffset: 1; } 65%, 88% { stroke-dashoffset: 0; } 100% { stroke-dashoffset: 1; } }
.trigger { transform-box: fill-box; transform-origin: center; animation: pulse 6s ease-in-out infinite; }
@keyframes pulse { 0%, 60%, 100% { opacity: .25; transform: scale(.85); } 72%, 88% { opacity: 1; transform: scale(1.15); } }'''
    return card(t, 332, "Motion Input Grid — movement follows three required cells to an action trigger", body, css)


def stats(t, data):
    body = text(36, 43, "02 / GITHUB SIGNAL", "mono", 12)
    ready = data['status'] == 'ready'
    timestamp = f"UPDATED {data['updated']} UTC" if ready else 'NOT YET COLLECTED'
    body += text(864, 43, timestamp, "mono", 10, 'text-anchor="end"')
    values = [(data['repositories'], 'public repositories'),
              (data['commits'], 'commits · authored, non-merge'),
              (data['lines_changed'], 'lines changed · added + deleted')]
    for i, (value, label) in enumerate(values):
        x = 36 + i * 282
        formatted = f'{value:,}' if value is not None else '—'
        body += text(x, 111, formatted, "accent", min(40, 250 / max(len(formatted) * .63, 1)), 'font-weight="700"')
        body += text(x, 140, label, "muted", 11)
    body += text(36, 191, "Languages · share of code size", "muted", 14)
    languages = sorted(data['languages'].items(), key=lambda item: (-item[1], item[0]))
    total = sum(data["languages"].values()) or 1
    for i, (name, n) in enumerate(languages):
        y = 223 + i * 30
        body += text(36, y, name, size=13)
        body += f'<rect x="190" y="{y-10}" width="590" height="9" rx="4" fill="{t["soft"]}"/>'
        body += f'<rect x="190" y="{y-10}" width="{590*n/total:.2f}" height="9" rx="4" fill="{t["accent"]}" class="bar" style="animation-delay:{i*.12}s"/>'
        percent = f'{n/total:.1%}' if n / total >= .001 else '<0.1%'
        body += text(864, y, percent, "muted", 13, 'text-anchor="end"')
    if not languages:
        body += text(36, 229, 'No detected languages.' if ready else 'Public statistics pending collection.', 'muted', 14)
    foot = 259 + max(1, len(languages)) * 30
    body += text(36, foot, "Owned public repositories only · language share measured in bytes", "muted", 11)
    body += text(36, foot + 20, "Personal history on default branches · duplicate commits counted once", "muted", 11)
    css = '''.bar { transform-box: fill-box; transform-origin: left; animation: fill 1.5s ease-out backwards; }
@keyframes fill { from { transform: scaleX(0); } to { transform: scaleX(1); } }'''
    return card(t, foot + 46, "Public GitHub languages, personal commits, lines changed and repository totals", body, css)


def theme_banner(t, selected, preview=False):
    heading = 'THEME PREVIEW / APERCU DU THEME' if preview else 'CURRENT THEME / THEME DU JOUR'
    body = text(36, 43, heading, "mono", 11)
    body += text(36, 78, t['name'], size=27, extra='font-weight="700"')
    body += text(864, 78, t['era'], "muted", 13, 'text-anchor="end"')
    detail = f'Preview updated {selected.isoformat()} · fixed identity · UTC' if preview else f'Selected {selected.isoformat()} · daily rotation · UTC'
    body += text(36, 108, detail, "muted", 12)
    return card(t, 130, f"{'Preview' if preview else 'Current theme'}: {t['name']}, inspired by {t['era']}, updated {selected.isoformat()} UTC", body)


def themed_readme(readme, theme, selected, preview=False):
    """A Markdown label stays readable without loading the decorative banner."""
    block = (f"<!-- current-theme:start -->\n"
             f"<sub>{'Preview theme' if preview else 'Current theme'}: <strong>{escape(theme['name'])}</strong> · {escape(theme['era'])} · "
             f"{'Updated' if preview else 'Selected'} {selected.isoformat()} (UTC)</sub>\n"
             f"<!-- current-theme:end -->")
    pattern = r'<!-- current-theme:start -->.*?<!-- current-theme:end -->'
    if re.search(pattern, readme, flags=re.S):
        readme = re.sub(pattern, lambda _: block, readme, flags=re.S)
    else:
        readme = block + '\n\n' + readme
    # Version every image together, so yesterday's cached theme isn't reused.
    version = f"{selected.isoformat()}-{theme['id']}"
    return re.sub(r'assets/((?:theme|flight|mig|stats)-(?:light|dark)\.svg)(?:\?v=[^"\s]+)?',
                  lambda m: f'assets/{m[1]}?v={version}', readme)


def theme_assets(identity, data, selected, preview=False):
    rendered = {}
    for mode, theme in variants(identity).items():
        cards = dict(theme=theme_banner(theme, selected, preview), flight=flight(theme),
                     mig=mig(theme), stats=stats(theme, data))
        rendered.update({f'{kind}-{mode}.svg': svg for kind, svg in cards.items()})
    return rendered


def gallery_navigation(readme, links):
    block = '<!-- theme-gallery:start -->\n' + links + '\n<!-- theme-gallery:end -->'
    pattern = r'<!-- theme-gallery:start -->.*?<!-- theme-gallery:end -->'
    if re.search(pattern, readme, flags=re.S):
        return re.sub(pattern, lambda _: block, readme, flags=re.S)
    marker = '<!-- current-theme:end -->'
    return readme.replace(marker, marker + '\n\n' + block, 1)


def theme_row(t, number):
    body = text(36, 36, f'{number:02} / VISUAL ERAS', 'mono', 10)
    body += text(36, 70, t['name'], size=28, extra='font-weight="700"')
    body += text(36, 99, t['era'], 'muted', 12)
    body += text(864, 99, 'OPEN THEME →', 'accent', 13, 'text-anchor="end"')
    return card(t, 122, f"Explore {t['name']} — {t['era']}", body)


def gallery_outputs(readme, data, selected, identities=None):
    """One catalog generates every fixed README and its styled index row."""
    identities = THEMES if identities is None else identities
    ids = [theme['id'] for theme in identities]
    if not ids or len(ids) != len(set(ids)) or any(not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', key) for key in ids):
        raise ValueError('Theme IDs must be unique, nonempty, lowercase URL-safe names.')
    outputs = {}
    rows = []
    for i, identity in enumerate(identities):
        key = identity['id']
        base = f'themes/{key}'
        previous, following = ids[(i-1) % len(ids)], ids[(i+1) % len(ids)]
        preview = themed_readme(readme, identity, selected, preview=True)
        preview = gallery_navigation(preview,
            '[← All themes](../README.md) · [Daily profile](../../README.md) · '
            f'[← Previous](../{previous}/README.md) · [Next →](../{following}/README.md)')
        # The same profile content is reused; only image paths and navigation vary.
        preview = preview.replace('(assets/stats.json)', '(../../assets/stats.json)')
        preview = preview.replace('alt="Current visual theme, era and selection date"',
                                  'alt="Fixed visual theme preview, era and update date"')
        outputs[f'{base}/README.md'] = preview
        assets = theme_assets(identity, data, selected, preview=True)
        for mode, theme in variants(identity).items():
            assets[f'row-{mode}.svg'] = theme_row(theme, i + 1)
        outputs.update({f'{base}/assets/{name}': svg for name, svg in assets.items()})
        name = escape(identity['name'], {'"': '&quot;'})
        rows.append(f'''<tr><td>
<a href="{key}/README.md"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="{key}/assets/row-dark.svg">
  <img src="{key}/assets/row-light.svg" alt="{name} — {escape(identity['era'])}. Open this theme." width="900">
</picture></a><br>
<a href="{key}/README.md">{name}</a>
</td></tr>''')
    outputs['themes/README.md'] = (
        '# Visual eras\n\n[← Daily profile](../README.md)\n\n'
        'Explore every implemented theme at any time. Each preview keeps its own '
        'visual identity and shares the latest public statistics. Opening a preview '
        'does not change the daily profile.\n\n'
        f'{len(ids)} themes · previews updated {selected.isoformat()} (UTC). '
        'Rows follow each theme’s light/dark appearance.\n\n'
        '<!-- Generated from scripts/profile_themes.py; add themes to that catalog. -->\n'
        '<table>\n' + '\n'.join(rows) + '\n</table>\n')
    return outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument("--user", default="Robin-G0")
    parser.add_argument("--date", type=date.fromisoformat,
                        help="Override selection date (YYYY-MM-DD), e.g. for local previews")
    args = parser.parse_args()
    ASSETS.mkdir(exist_ok=True)
    if args.refresh:
        data = collect(args.user)
    else:
        data = json.loads(SNAPSHOT.read_text(encoding="utf-8")) if SNAPSHOT.exists() else None
    # Discard older snapshots that could include private aggregates.
    if not data or data.get('schema') != 3 or data.get('scope') != 'owned_public':
        data = pending(args.user)
    # Offline renders preserve the selection instead of silently changing the day.
    if args.date:
        selected = args.date
    elif args.refresh:
        selected = date.fromisoformat(data['updated'])
    elif THEME_STATE.exists():
        selected = date.fromisoformat(json.loads(THEME_STATE.read_text(encoding='utf-8'))['selected'])
    else:
        selected = date.fromisoformat(data['updated']) if data.get('updated') else datetime.now(timezone.utc).date()
    identity = theme_for_day(selected)
    rendered = theme_assets(identity, data, selected)
    state = dict(id=identity['id'], name=identity['name'], era=identity['era'],
                 selected=selected.isoformat(), timezone='UTC',
                 palette={mode: identity[mode] for mode in ('light', 'dark')})
    rendered['theme.json'] = json.dumps(state, indent=2, ensure_ascii=False) + '\n'
    readme_path = ROOT / 'README.md'
    readme = themed_readme(readme_path.read_text(encoding='utf-8'), identity, selected)
    readme = gallery_navigation(readme, '[Explore all visual themes →](themes/README.md)')
    outputs = {f'assets/{filename}': content for filename, content in rendered.items()}
    outputs.update(gallery_outputs(readme, data, selected))
    outputs['README.md'] = readme
    outputs['assets/stats.json'] = json.dumps(data, indent=2) + '\n'
    # Finish collection and rendering before changing any existing files.
    for filename, content in outputs.items():
        target = ROOT / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding='utf-8')


if __name__ == "__main__":
    try:
        main()
    except CollectionError as error:
        raise SystemExit(str(error)) from None
