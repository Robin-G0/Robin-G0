from datetime import date
import unittest
import xml.etree.ElementTree as ET

from scripts.render_profile import asset_revision, themed_readme
from scripts.profile_themes import THEMES
from scripts.validate_profile import validate_outputs


class PublicationTests(unittest.TestCase):
    def test_invalid_svg_and_conflict_markers_cannot_be_published(self):
        with self.assertRaises(ET.ParseError):
            validate_outputs({'assets/stats.svg': '<svg><text></svg>'})
        for filename in ('assets/stats.svg', 'README.md', 'assets/stats.json'):
            with self.assertRaises(ValueError):
                validate_outputs({filename: '<<<<<<< HEAD\none\n=======\ntwo\n>>>>>>> other\n'})

    def test_content_change_versions_image_urls_on_the_same_day(self):
        readme = '<img src="assets/stats-dark.svg?v=old">'
        day = date(2026, 11, 12)
        a = asset_revision({'stats.svg': 'first'})
        b = asset_revision({'stats.svg': 'second'})
        first = themed_readme(readme, THEMES[0], day, revision=a)
        second = themed_readme(first, THEMES[0], day, revision=b)
        self.assertNotEqual(a, b)
        self.assertNotIn(a, second)
        self.assertIn(b, second)
        self.assertEqual(second, themed_readme(second, THEMES[0], day, revision=b))


if __name__ == '__main__':
    unittest.main()
