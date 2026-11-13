import re
import unittest
import xml.etree.ElementTree as ET

from scripts import profile_art as art
from scripts.profile_themes import THEMES, variants
from scripts.profile_stats import pending


SVG = '{http://www.w3.org/2000/svg}'


class EraMaterialsTests(unittest.TestCase):
    def test_material_and_animation_references_resolve_in_every_theme(self):
        data = dict(pending('Robin-G0'), status='ready', updated='2026-11-12',
                    repositories=1, commits=1, lines_changed=1,
                    languages={'Python':9999, 'C':1})
        for identity in THEMES:
            for theme in variants(identity).values():
                for document in (art.scene(theme,'flight'), art.scene(theme,'mig'),
                                 art.about(theme), art.activity(theme,data),
                                 art.label_card(theme),art.label_card(theme,number=1)):
                    with self.subTest(theme=theme['id'], mode=theme['mode']):
                        root=ET.fromstring(document)
                        ids=[node.get('id') for node in root.iter() if node.get('id')]
                        self.assertEqual(len(ids),len(set(ids)))
                        self.assertFalse(set(re.findall(r'url\(#([\w-]+)\)',document))-set(ids))
                        css=root.find(SVG+'style').text
                        animations=set(re.findall(r'animation:([a-z][\w-]*)',css)) - {'none'}
                        frames=set(re.findall(r'@keyframes ([\w-]+)',css))
                        self.assertFalse(animations-frames)

    def test_percentage_boundary_never_animates_even_for_tiny_shares(self):
        for identity in THEMES:
            theme=variants(identity)['light']
            for width in (.02, 0.5, 128.75):
                root=ET.fromstring('<svg xmlns="http://www.w3.org/2000/svg">'+
                                   art.meter(theme,20,30,width,9,'#abc',0)+'</svg>')
                clip=root.find('.//'+SVG+'clipPath')
                rect=clip.find(SVG+'rect')
                self.assertEqual(float(rect.get('width')),width)
                self.assertFalse(list(rect))
                self.assertIsNone(rect.get('class'))
                group=root.find(SVG+'g')
                self.assertEqual(group.get('clip-path'),'url(#meter-0)')
                self.assertNotIn('stat-fill',ET.tostring(group,encoding='unicode'))

    def test_glass_filters_only_backdrop_and_has_reduced_motion_fallback(self):
        theme=variants(next(t for t in THEMES if t['id']=='glass'))['light']
        for document in (art.scene(theme,'flight'),art.scene(theme,'mig'),art.about(theme)):
            root=ET.fromstring(document)
            lenses=[node for node in root.iter() if node.get('data-material')=='refracted-backdrop']
            self.assertTrue(lenses)
            for lens in lenses:
                self.assertFalse(list(lens.iter(SVG+'text')))
                self.assertFalse(any(node.get('aria-label') for node in lens.iter()))
                self.assertTrue(any(node.get('filter')=='url(#glass-lens)' for node in lens.iter()))
            self.assertNotIn('<animate',document)
            self.assertIn('@media(prefers-reduced-motion:reduce){*{animation:none!important;}',document)

    def test_aqua_title_material_has_no_internal_dark_chrome_band(self):
        theme=variants(next(t for t in THEMES if t['id']=='aqua'))['light']
        document=art.scene(theme,'mig')
        root=ET.fromstring(document)
        titlebars=[node for node in root.iter() if node.get('data-aqua-titlebar')]
        self.assertEqual(len(titlebars),1)
        self.assertEqual(titlebars[0].get('fill'),'url(#aqua-title)')
        self.assertFalse(any(node.get('fill')=='url(#chrome)' for node in root.iter()))


if __name__=='__main__':
    unittest.main()
