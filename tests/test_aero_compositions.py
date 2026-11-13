import re
import unittest
import xml.etree.ElementTree as ET

from scripts import profile_art as art
from scripts.profile_themes import THEMES, variants
from scripts.profile_stats import pending


SVG='{http://www.w3.org/2000/svg}'


class AeroCompositionTests(unittest.TestCase):
    def setUp(self):
        self.theme=variants(next(t for t in THEMES if t['id']=='aero'))['light']

    def test_fish_lanes_stay_below_the_copy_and_use_local_alpha_images(self):
        document=art.about(self.theme);root=ET.fromstring(document)
        text_bottom=max(float(node.get('y')) for node in root.iter(SVG+'text'))
        fish=[node for node in root.iter() if node.get('data-swimming-fish')]
        self.assertEqual(len(fish),3)
        for node in fish:
            # All authored control-point Y values, including the tallest fish.
            path=re.search(r"offset-path:path\('([^']+)'\)",node.get('style')).group(1)
            coordinates=list(map(float,re.findall(r'-?\d+(?:\.\d+)?',path)))
            image=next(node.iter(SVG+'image'))
            self.assertGreater(min(coordinates[1::2])-float(image.get('height'))/2,text_bottom)
            self.assertTrue(image.get('href').startswith('data:image/png;base64,'))
        self.assertIn('@media(prefers-reduced-motion:reduce){*{animation:none!important;}',document)

    def test_aero_flight_is_one_round_trip_with_upright_return(self):
        document=art.scene(self.theme,'flight');root=ET.fromstring(document)
        aircraft=[node for node in root.iter() if node.get('data-travel')=='round-trip']
        self.assertEqual(len(aircraft),1)
        self.assertEqual(len([node for node in root.iter() if node.get('data-flight-route')=='true']),1)
        self.assertTrue(list(aircraft[0].iter(SVG+'image')))
        self.assertIn('50%,99%{transform:scaleY(-1)}',document)

    def test_glass_meter_bitmap_is_shared_and_width_is_measured(self):
        data=dict(pending('Robin-G0'),status='ready',updated='2026-11-12',
                  repositories=10,commits=20,lines_changed=30,languages={'Python':9999,'C':1})
        document=art.activity(self.theme,data);root=ET.fromstring(document)
        material=[node for node in root.iter() if node.get('id')=='aero-meter-material']
        self.assertEqual(len(material),1)
        self.assertEqual(len(list(material[0].iter(SVG+'image'))),1)
        widths=[float(node.find(SVG+'rect').get('width')) for node in root.iter(SVG+'clipPath')
                if node.get('id','').startswith('meter-')]
        self.assertEqual(widths,[540*.9999,540*.0001])
        self.assertLess(len(document.encode('utf-8')),1_000_000)

    def test_default_font_is_inherited_so_section_typefaces_are_respected(self):
        root=ET.fromstring(art.about(self.theme));css=root.find(SVG+'style').text
        self.assertNotRegex(css,r'(?:^|[;}])\s*text\s*\{[^}]*font-family')
        families={node.get('font-family') for node in root.iter(SVG+'text')}
        self.assertTrue(any('Tahoma' in (font or '') for font in families))
        self.assertTrue(any('Georgia' in (font or '') for font in families))

    def test_aquarium_uses_a_local_water_loop_and_static_reduced_motion_fallback(self):
        document=art.about(self.theme);root=ET.fromstring(document)
        loops=[node for node in root.iter(SVG+'image') if node.get('data-aquarium-loop')]
        self.assertEqual(len(loops),1)
        self.assertTrue(loops[0].get('href').startswith('data:image/gif;base64,'))
        self.assertIn('.aquarium-moving{display:none!important}',document)
        self.assertIn('.aquarium-still{display:inline!important}',document)
        self.assertLess(len(document.encode('utf-8')),3_000_000)


if __name__=='__main__':
    unittest.main()
