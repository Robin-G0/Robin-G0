"""Generate the profile's SVG cards. Python standard library only.

Run with --refresh to collect public GitHub statistics; otherwise use the last
saved snapshot. All graphics share the palette below, ready for the Pages site.
"""

import argparse
import hashlib
from datetime import date, datetime, timezone
import json
from pathlib import Path
import re
from xml.sax.saxutils import escape

if __package__:
    from .profile_themes import THEMES, theme_for_day, variants
    from .profile_stats import CollectionError, collect, pending
    from .validate_profile import validate_outputs
    from . import profile_art as art
else:
    from profile_themes import THEMES, theme_for_day, variants
    from profile_stats import CollectionError, collect, pending
    from validate_profile import validate_outputs
    import profile_art as art

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
SNAPSHOT = ASSETS / "stats.json"
THEME_STATE = ASSETS / "theme.json"
BUTTONS = {'source':'Project source', 'demo':'Interactive demo', 'studio':'Open Studio',
           'website':'Website', 'repos':'Repositories', 'themes':'All themes',
           'data':'Statistics data', 'previous':'Previous theme',
           'next':'Next theme', 'daily':'Profile'}


def flight(t):
    return art.scene(t, 'flight')


def mig(t):
    return art.scene(t, 'mig')


def stats(t, data):
    return art.activity(t, data)


def theme_banner(t, selected, preview=False):
    return art.label_card(t, selected=selected, preview=preview)


def themed_readme(readme, theme, selected, preview=False, revision=None):
    """A Markdown label stays readable without loading the decorative banner."""
    block = (f"<!-- current-theme:start -->\n"
             f"<!-- Visual identity: {escape(theme['name'])} / {escape(theme['era'])} -->\n"
             f"<!-- current-theme:end -->")
    pattern = r'<!-- current-theme:start -->.*?<!-- current-theme:end -->'
    if re.search(pattern, readme, flags=re.S):
        readme = re.sub(pattern, lambda _: block, readme, flags=re.S)
    else:
        readme = block + '\n\n' + readme
    # Version every image together, so yesterday's cached theme isn't reused.
    version = f"{selected.isoformat()}-{theme['id']}"
    if revision:
        version += '-' + revision
    return re.sub(r'assets/((?:theme|flight|about|mig|stats|button-[a-z]+)-(?:light|dark)\.svg)(?:\?v=[^"\s]+)?',
                  lambda m: f'assets/{m[1]}?v={version}', readme).replace('\u2014',' / ').replace('\u2013','-')


def theme_assets(identity, data, selected, preview=False):
    rendered = {}
    for mode, theme in variants(identity).items():
        cards = dict(theme=theme_banner(theme, selected, preview), flight=flight(theme), about=art.about(theme),
                     mig=mig(theme), stats=stats(theme, data))
        cards.update({f'button-{key}': art.action_button(theme,label) for key,label in BUTTONS.items()})
        rendered.update({f'{kind}-{mode}.svg': svg for kind, svg in cards.items()})
    return rendered


def asset_revision(assets):
    return hashlib.sha256(json.dumps(assets, sort_keys=True).encode()).hexdigest()[:12]


def gallery_navigation(readme, links):
    block = '<!-- theme-gallery:start -->\n' + links + '\n<!-- theme-gallery:end -->'
    pattern = r'<!-- theme-gallery:start -->.*?<!-- theme-gallery:end -->'
    if re.search(pattern, readme, flags=re.S):
        return re.sub(pattern, lambda _: block, readme, flags=re.S)
    marker = '<!-- current-theme:end -->'
    if marker in readme:
        return readme.replace(marker, marker + '\n\n' + block, 1)
    return block + '\n\n' + readme


def linked_button(key,url,width=220):
    return (f'<a href="{url}"><picture>'
            f'<source media="(prefers-color-scheme: dark)" srcset="assets/button-{key}-dark.svg">'
            f'<img src="assets/button-{key}-light.svg" alt="{BUTTONS[key]}" width="{width}">'
            '</picture></a>')


def theme_row(t, number):
    return art.label_card(t, number=number)


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
        assets = theme_assets(identity, data, selected, preview=True)
        preview = gallery_navigation(readme, '<p>\n'+'\n'.join([
            linked_button('themes','../README.md'),linked_button('daily','../../README.md'),
            linked_button('previous',f'../{previous}/README.md'),
            linked_button('next',f'../{following}/README.md')])+'\n</p>')
        # The same profile content is reused; only image paths and navigation vary.
        preview = preview.replace('(assets/stats.json)', '(../../assets/stats.json)')
        preview = preview.replace('href="assets/stats.json"', 'href="../../assets/stats.json"')
        preview = preview.replace('alt="Current visual theme, era and selection date"',
                                  'alt="Visual identity and era"')
        preview = themed_readme(preview, identity, selected, preview=True, revision=asset_revision(assets))
        outputs[f'{base}/README.md'] = preview
        for mode, theme in variants(identity).items():
            assets[f'row-{mode}.svg'] = theme_row(theme, i + 1)
        outputs.update({f'{base}/assets/{name}': svg for name, svg in assets.items()})
        name = escape(identity['name'], {'"': '&quot;'})
        rows.append(f'''<tr><td>
<a href="{key}/README.md"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="{key}/assets/row-dark.svg">
  <img src="{key}/assets/row-light.svg" alt="{name} — {escape(identity['era'])}. Open this theme." width="900">
</picture></a>
</td></tr>''')
    outputs['themes/README.md'] = (
        '# Visual eras\n\n[← Profile](../README.md)\n\n'
        'Explore every visual identity. All themes share the same profile and public statistics.\n\n'
        f'{len(ids)} themes. Rows follow each theme’s light/dark appearance.\n\n'
        '<!-- Generated from scripts/profile_themes.py; add themes to that catalog. -->\n'
        '<table>\n' + '\n'.join(rows) + '\n</table>\n')
    return outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument("--user", default="Robin-G0")
    parser.add_argument('--snapshot', type=Path,
                        help='Render a collected public snapshot without another network request')
    parser.add_argument("--date", type=date.fromisoformat,
                        help="Override selection date (YYYY-MM-DD), e.g. for local previews")
    args = parser.parse_args()
    if args.refresh and args.snapshot:
        parser.error('--refresh and --snapshot cannot be used together')
    ASSETS.mkdir(exist_ok=True)
    if args.refresh:
        data = collect(args.user)
    elif args.snapshot:
        data = json.loads(args.snapshot.read_text(encoding='utf-8'))
        if data.get('schema') != 4 or data.get('scope') != 'owned_public' or data.get('status') != 'ready':
            raise ValueError('A publication snapshot must contain complete public statistics.')
    else:
        data = json.loads(SNAPSHOT.read_text(encoding="utf-8")) if SNAPSHOT.exists() else None
    # Discard older snapshots that could include private aggregates.
    if not data or data.get('schema') != 4 or data.get('scope') != 'owned_public':
        data = pending(args.user)
    # Offline renders preserve the selection instead of silently changing the day.
    if args.date:
        selected = args.date
    elif args.refresh or args.snapshot:
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
    readme = gallery_navigation(readme_path.read_text(encoding='utf-8'), '<p>'+linked_button('themes','themes/README.md')+'</p>')
    readme = themed_readme(readme, identity, selected,
                           revision=asset_revision(rendered))
    outputs = {f'assets/{filename}': content for filename, content in rendered.items()}
    outputs.update(gallery_outputs(readme, data, selected))
    outputs['README.md'] = readme
    outputs['assets/stats.json'] = json.dumps(data, indent=2) + '\n'
    outputs = {name: content.replace('\u2014',' / ').replace('\u2013','-')
               if name.endswith(('.md','.svg')) else content for name,content in outputs.items()}
    outputs = {name: content.rstrip()+'\n' if name.endswith('.md') else content
               for name,content in outputs.items()}
    validate_outputs(outputs)
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
