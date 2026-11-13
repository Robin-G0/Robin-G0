import unittest
import xml.etree.ElementTree as ET

from scripts import era_materials as materials
from scripts import profile_art as art
from scripts.profile_themes import THEMES, variants
from scripts.profile_stats import pending

SVG='{http://www.w3.org/2000/svg}'


class GlassTests(unittest.TestCase):
    def test_aurora_height_thickness_and_velocity_match_at_loop_seam(self):
        for base,amplitude,phase in ((190,70,.5),(145,62,0),(265,45,2.2)):
            for x in (-100,0,100,450,899):
                left=materials.aurora_profile(x,base,amplitude,phase)
                right=materials.aurora_profile(x+materials.AURORA_PERIOD,base,amplitude,phase)
                for a,b in zip(left,right):self.assertAlmostEqual(a,b,places=9)
                step=.001
                for position in (x,x+materials.AURORA_PERIOD):
                    before=materials.aurora_profile(position-step,base,amplitude,phase)
                    after=materials.aurora_profile(position+step,base,amplitude,phase)
                    slope=tuple((b-a)/(2*step) for a,b in zip(before,after))
                    if position==x:first_slope=slope
                    else:
                        for a,b in zip(first_slope,slope):self.assertAlmostEqual(a,b,places=7)
        self.assertIn(f'translateX(-{materials.AURORA_PERIOD}px)',materials.motion('glass'))

    def test_each_language_has_a_separate_bar_at_its_true_share(self):
        identity=next(t for t in THEMES if t['id']=='glass')
        data=dict(pending('Robin-G0'),status='ready',updated='2026-11-12',
                  repositories=1,commits=2,lines_changed=3,languages={'Python':9999,'C':1})
        for theme in variants(identity).values():
            root=ET.fromstring(art.activity(theme,data))
            rows={node.get('data-language-row'):node for node in root.iter() if node.get('data-language-row')}
            self.assertEqual(set(rows),set(data['languages']))
            for name,row in rows.items():
                clip=next(row.iter(SVG+'clipPath')).find(SVG+'rect')
                self.assertAlmostEqual(float(clip.get('width')),168*data['languages'][name]/10000)
                self.assertIsNone(clip.get('class'))
                self.assertTrue(any(node.text==name for node in row.iter(SVG+'text')))


if __name__=='__main__':
    unittest.main()
