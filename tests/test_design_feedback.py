import unittest
import xml.etree.ElementTree as ET

from scripts import profile_art as art
from scripts.profile_themes import THEMES, variants
from scripts.profile_stats import pending


class FeedbackTests(unittest.TestCase):
    def test_bio_and_interests_are_in_every_theme_and_long_dashes_are_absent(self):
        data=dict(pending('Robin-G0'),status='ready',updated='2026-11-12',
                  repositories=10,commits=832,lines_changed=138148,
                  languages={'Python':10,'JavaScript':20})
        for identity in THEMES:
            for t in variants(identity).values():
                bio=art.about(t)
                self.assertIn('full-stack developer',bio)
                self.assertIn('research and development',bio)
                self.assertIn('quantum computing at the moment',bio)
                for document in (bio,art.scene(t,'flight'),art.scene(t,'mig'),art.activity(t,data)):
                    ET.fromstring(document)
                    self.assertNotIn('\u2014',document)
                    self.assertNotIn('\u2013',document)
                self.assertIn('stat-sheen',art.activity(t,data))
                self.assertIn('prefers-reduced-motion',art.activity(t,data))

    def test_icons_are_present_in_windows95_and_metro_and_embedded(self):
        data=dict(pending('Robin-G0'),status='ready',updated='2026-11-12',
                  repositories=1,commits=1,lines_changed=1,languages={'Python':1,'JavaScript':1})
        for key in ('desktop95','metro'):
            t=variants(next(t for t in THEMES if t['id']==key))['light']
            svg=art.activity(t,data)
            self.assertIn('data-language-icon="Python"',svg)
            self.assertIn('data-language-icon="JavaScript"',svg)
            for node in ET.fromstring(svg).iter('{http://www.w3.org/2000/svg}image'):
                self.assertTrue(node.get('href','').startswith('data:image/'))

    def test_testers_checked_and_95_window_not_named_after_the_profile(self):
        t=variants(THEMES[0])['light']
        self.assertIn('[x] testers wanted',art.scene(t,'mig'))
        t=variants(THEMES[1])['light']
        visible=[node.text for node in ET.fromstring(art.scene(t,'flight')).iter('{http://www.w3.org/2000/svg}text')]
        self.assertNotIn('Robin-G0',visible)


if __name__=='__main__':
    unittest.main()
