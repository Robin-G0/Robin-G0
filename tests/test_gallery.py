from datetime import date
import posixpath
import re
import unittest
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

from scripts.profile_stats import pending
from scripts.profile_themes import THEMES
from scripts.render_profile import gallery_outputs


TEMPLATE = '''<picture>
<source media="(prefers-color-scheme: dark)" srcset="assets/theme-dark.svg?v=old">
<img src="assets/theme-light.svg?v=old" alt="Theme">
</picture>
<img src="assets/flight-light.svg">
<a href="https://github.com/Robin-G0/Motion-Input-Grid">MIG</a>
<img src="assets/mig-dark.svg">
<img src="assets/stats-light.svg">
[View the data](assets/stats.json)
'''


class GalleryTests(unittest.TestCase):
    def setUp(self):
        self.day = date(2026, 11, 12)
        self.data = dict(pending('Robin-G0'), status='ready', updated='2026-11-11',
                         repositories=10, commits=830, lines_changed=123456, languages={'Python':100})

    def test_each_theme_has_full_readme_and_unique_styled_row(self):
        outputs = gallery_outputs(TEMPLATE, self.data, self.day)
        index = outputs['themes/README.md']
        self.assertEqual(index.count('<tr>'), len(THEMES))
        rows = set()
        for theme in THEMES:
            key = theme['id']
            readme = outputs[f'themes/{key}/README.md']
            self.assertIn(f'Preview theme: {theme["name"]}', readme)
            self.assertNotIn('Current theme:', readme)
            self.assertIn(f'?v=2026-11-12-{key}', readme)
            self.assertIn('href="../README.md"', readme)
            self.assertIn('href="../../README.md"', readme)
            self.assertIn('(../../assets/stats.json)', readme)
            self.assertIn(f'href="{key}/README.md"', index)
            for mode in ('light', 'dark'):
                for kind in ('theme', 'flight', 'mig', 'stats', 'row'):
                    svg = outputs[f'themes/{key}/assets/{kind}-{mode}.svg']
                    ET.fromstring(svg)
                banner = outputs[f'themes/{key}/assets/theme-{mode}.svg']
                self.assertIn('fixed identity', banner)
                self.assertNotIn('daily rotation', banner)
                self.assertIn('2026-11-11', outputs[f'themes/{key}/assets/stats-{mode}.svg'])
            rows.add(outputs[f'themes/{key}/assets/row-light.svg'])
        self.assertEqual(len(rows), len(THEMES))

    def test_all_relative_links_and_images_resolve(self):
        outputs = gallery_outputs(TEMPLATE, self.data, self.day)
        known = set(outputs) | {'README.md', 'assets/stats.json'}
        for path, content in outputs.items():
            if not path.endswith('.md'):
                continue
            targets = re.findall(r'(?:href|src|srcset)="([^"]+)"', content)
            targets += re.findall(r'\]\(([^)]+)\)', content)
            for target in targets:
                if urlsplit(target).scheme or target.startswith('#'):
                    continue
                resolved = posixpath.normpath(posixpath.join(posixpath.dirname(path), urlsplit(target).path))
                with self.subTest(page=path, link=target):
                    self.assertIn(resolved, known)

    def test_new_catalog_entry_automatically_gets_an_index_row_and_readme(self):
        extra = dict(THEMES[-1], id='new-era', name='New Era')
        outputs = gallery_outputs(TEMPLATE, self.data, self.day, [*THEMES, extra])
        self.assertIn('themes/new-era/README.md', outputs)
        self.assertIn('href="new-era/README.md"', outputs['themes/README.md'])
        self.assertIn('New Era', outputs['themes/new-era/assets/row-dark.svg'])
        self.assertEqual(outputs['themes/README.md'].count('<tr>'), len(THEMES) + 1)

    def test_invalid_or_duplicate_ids_cannot_overwrite_other_files(self):
        for invalid in ([THEMES[0], THEMES[0]], [dict(THEMES[0], id='../escape')], []):
            with self.assertRaises(ValueError):
                gallery_outputs(TEMPLATE, self.data, self.day, invalid)


if __name__ == '__main__':
    unittest.main()
