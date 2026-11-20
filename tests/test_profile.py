from datetime import timedelta
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

from scripts import render_profile as render
from scripts.profile_themes import DEFAULT_THEME_ID, EPOCH, THEMES, default_theme, variants
from scripts.profile_stats import pending


class RotationTests(unittest.TestCase):
    def test_the_profile_keeps_the_portfolio_default_theme_on_every_date(self):
        self.assertEqual(default_theme()['id'], DEFAULT_THEME_ID)
        self.assertIn(DEFAULT_THEME_ID, {t['id'] for t in THEMES})
        for offset in range(0, 400, 37):
            day = EPOCH + timedelta(days=offset)
            self.assertIn(f"{day.isoformat()}-{DEFAULT_THEME_ID}", render.themed_readme('<img src="assets/mig-light.svg">', default_theme(), day))

    def test_all_eras_render_valid_svg_in_both_modes(self):
        data = dict(pending('Robin-G0'), status='ready', updated='2026-11-12',
                    repositories=0, commits=0, lines_changed=0, languages={'A&B <example>': 1})
        for identity in THEMES:
            for theme in variants(identity).values():
                for svg in (render.theme_banner(theme, EPOCH), render.flight(theme),
                            render.mig(theme), render.stats(theme, data)):
                    with self.subTest(theme=identity['id']):
                        root = ET.fromstring(svg)
                        self.assertEqual(root.tag, '{http://www.w3.org/2000/svg}svg')
                        self.assertIn('prefers-reduced-motion', svg)
                        self.assertNotIn('<script', svg)

    def test_readme_updates_all_versions_and_is_idempotent(self):
        readme = '<img src="assets/flight-light.svg?v=old"><img src="assets/mig-dark.svg">'
        updated = render.themed_readme(readme, THEMES[0], EPOCH)
        self.assertEqual(updated.count('current-theme:start'), 1)
        self.assertEqual(updated.count('?v=2026-01-01-phosphor'), 2)
        self.assertEqual(updated, render.themed_readme(updated, THEMES[0], EPOCH))
        next_day = EPOCH + timedelta(days=1)
        changed = render.themed_readme(updated, THEMES[1], next_day)
        self.assertNotIn('phosphor', changed)
        self.assertEqual(changed.count('current-theme:start'), 1)

    def test_offline_run_preserves_selection_and_refresh_failure_preserves_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            assets = root / 'assets'
            assets.mkdir()
            (root / 'README.md').write_text('<img src="assets/mig-light.svg">', encoding='utf-8')
            data = dict(pending('Robin-G0'), status='ready', updated='2026-10-01',
                        repositories=0, commits=0, lines_changed=0)
            (assets / 'stats.json').write_text(json.dumps(data), encoding='utf-8')
            (assets / 'theme.json').write_text('{"selected":"2026-11-12"}', encoding='utf-8')
            with patch.multiple(render, ROOT=root, ASSETS=assets,
                                SNAPSHOT=assets / 'stats.json', THEME_STATE=assets / 'theme.json'):
                with patch('sys.argv', ['render_profile.py']):
                    render.main()
                    before = {p.relative_to(root): p.read_bytes() for p in root.rglob('*') if p.is_file()}
                    render.main()
                    self.assertEqual(before, {p.relative_to(root): p.read_bytes() for p in root.rglob('*') if p.is_file()})
                self.assertEqual(json.loads((assets / 'theme.json').read_text())['selected'], '2026-11-12')
                with patch('sys.argv', ['render_profile.py', '--refresh']), patch.object(render, 'collect', side_effect=OSError):
                    with self.assertRaises(OSError):
                        render.main()
                self.assertEqual(before, {p.relative_to(root): p.read_bytes() for p in root.rglob('*') if p.is_file()})
                for path in assets.glob('*.svg'):
                    ET.parse(path)


if __name__ == '__main__':
    unittest.main()
