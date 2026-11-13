import unittest
import xml.etree.ElementTree as ET

from scripts import era_materials as materials
from scripts import profile_art as art
from scripts import glass_worlds as worlds
from scripts.profile_themes import THEMES, variants
from scripts.profile_stats import pending

SVG='{http://www.w3.org/2000/svg}'


class GlassTests(unittest.TestCase):
    def test_each_section_has_its_own_motion_and_matching_refraction(self):
        identity=next(t for t in THEMES if t['id']=='glass')
        data=dict(pending('Robin-G0'),status='ready',updated='2026-11-12',
                  repositories=1,commits=2,lines_changed=3,languages={'Python':1})
        for theme in variants(identity).values():
            scenes={'identity':art.label_card(theme),'flight':art.scene(theme,'flight'),
                    'about':art.about(theme),'project':art.scene(theme,'mig'),
                    'activity':art.activity(theme,data)}
            treatments=set()
            for section,document in scenes.items():
                root=ET.fromstring(document)
                fields=[node for node in root.iter() if node.get('data-glass-section')]
                self.assertEqual(len(fields),2)
                self.assertEqual({node.get('data-glass-section') for node in fields},{section})
                self.assertEqual(fields[0].get('class'),fields[1].get('class'))
                self.assertFalse(any(list(node.iter(SVG+'text')) for node in fields))
                treatments.add(fields[0].get('class'))
                self.assertIn('animation:none!important',root.find(SVG+'style').text)
            self.assertEqual(len(treatments),len(scenes))

    def test_aurora_layers_are_slow_distinct_and_travel_in_one_direction(self):
        durations=[duration for _,duration,_ in materials.AURORA_LAYERS]
        self.assertEqual(len(set(durations)),3)
        self.assertGreaterEqual(min(durations),90)
        css=materials.motion('glass')
        self.assertNotIn('reverse',css)
        self.assertNotIn('alternate',css)
        self.assertIn(f'translateX(-{materials.AURORA_PERIOD}px)',css)
        for height in (130,440,686):
            field=ET.fromstring('<svg xmlns="http://www.w3.org/2000/svg">'+materials.waves(height)+'</svg>')
            layers=[node for node in field.iter() if node.get('data-aurora-layer')]
            self.assertEqual(len(layers),3)
            self.assertFalse(list(field.iter(SVG+'path')))
            for node in layers:
                tile=node.find(SVG+'rect')
                self.assertGreaterEqual(float(tile.get('width')),3*materials.AURORA_PERIOD)

    def test_photographic_layers_are_embedded_once_and_seams_fade_to_zero(self):
        theme=variants(next(t for t in THEMES if t['id']=='glass'))['light']
        root=ET.fromstring(art.label_card(theme))
        patterns=[node for node in root.iter(SVG+'pattern') if node.get('id','').startswith('aurora-photo-')]
        self.assertEqual(len(patterns),3)
        for pattern in patterns:
            images=list(pattern.iter(SVG+'image'))
            self.assertEqual(len(images),1)
            self.assertTrue(images[0].get('href').startswith('data:image/png;base64,'))
            self.assertEqual(float(pattern.get('width')),materials.AURORA_PERIOD)
            self.assertEqual(images[0].get('mask'),'url(#aurora-tile-mask)')
        gradient=next(node for node in root.iter(SVG+'linearGradient') if node.get('id')=='aurora-feather')
        stops=list(gradient)
        self.assertEqual(stops[0].get('stop-opacity'),'0')
        self.assertEqual(stops[-1].get('stop-opacity'),'0')

    def test_content_sections_use_distinct_generated_assets_instead_of_auroras(self):
        data=dict(pending('Robin-G0'),status='ready',updated='2026-11-12',
                  repositories=1,commits=2,lines_changed=3,languages={'Python':1})
        identity=next(t for t in THEMES if t['id']=='glass')
        for theme in variants(identity).values():
            scenes={'flight':art.scene(theme,'flight'),'about':art.about(theme),
                    'project':art.scene(theme,'mig'),'activity':art.activity(theme,data)}
            seen=set();seen_sources=set()
            for section,document in scenes.items():
                with self.subTest(mode=theme['mode'],section=section):
                    root=ET.fromstring(document)
                    images=[node for node in root.iter(SVG+'image') if node.get('data-scene-asset')]
                    assets={node.get('data-scene-asset') for node in images}
                    self.assertEqual(assets,{worlds.WORLDS[section]['background'],worlds.WORLDS[section]['foreground']})
                    self.assertEqual(len(images),2)
                    self.assertFalse(seen.intersection(assets))
                    sources={node.get('href') for node in images}
                    self.assertFalse(seen_sources.intersection(sources))
                    self.assertFalse(any(node.get('data-aurora-layer') for node in root.iter()))
                    self.assertTrue(all(node.get('href').startswith('data:image/') for node in images))
                    self.assertLess(len(document.encode('utf-8')),800_000)
                    seen.update(assets)
                    seen_sources.update(sources)
                    ids={node.get('id') for node in root.iter() if node.get('id')}
                    for node in root.iter(SVG+'use'):
                        self.assertIn(node.get('href')[1:],ids)
                    if section!='about':
                        foreground=next(node for node in root.iter() if node.get('data-scene-foreground'))
                        self.assertFalse(any(node.get('filter') for node in foreground.iter()))

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
                self.assertAlmostEqual(float(clip.get('width')),200*data['languages'][name]/10000)
                self.assertIsNone(clip.get('class'))
                self.assertTrue(any(node.text==name for node in row.iter(SVG+'text')))
                track=next(node for node in row.iter() if node.get('data-language-track'))
                self.assertEqual(float(track.get('width')),200)
                self.assertNotEqual(track.get('fill'),'#0b173d')
                self.assertFalse(list(row.iter(SVG+'circle')))


if __name__=='__main__':
    unittest.main()
