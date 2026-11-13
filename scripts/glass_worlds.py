"""Distinct locally generated environments for the four Glass content sections."""

WORLDS={
    'flight':dict(name='space',background='glass-space-sky-v1.jpg',foreground='glass-space-earth-v1.png',
                  background_seconds=3600,foreground_seconds=180,placement=(540,88,330,330),base='#050c21',motion='orbital'),
    'about':dict(name='ocean',background='glass-ocean-water-v1.jpg',foreground='glass-ocean-caustics-v1.png',
                 background_seconds=2400,foreground_seconds=24,placement=(-40,185,980,255),base='#052539',motion='caustics'),
    'project':dict(name='abyss',background='glass-abyss-depths-v1.jpg',foreground='glass-abyss-jellyfish-v1.png',
                   background_seconds=4200,foreground_seconds=110,placement=(84,130,230,290),base='#030d1d',motion='jellyfish'),
    'activity':dict(name='lunar',background='glass-lunar-horizon-v1.jpg',foreground='glass-lunar-ledge-v1.png',
                    background_seconds=5200,foreground_seconds=240,placement=(490,340,440,110),base='#080e1c',motion='terrain'),
}


def resources(embedded_asset,section):
    scene=WORLDS[section]
    background=embedded_asset('art/'+scene['background'])
    foreground=embedded_asset('art/'+scene['foreground'])
    x,y,w,h=scene['placement']
    still=(f'<use href="#world-background-image"/><use href="#world-background-image" transform="translate(1800 0) scale(-1 1)"/>')
    water=''
    if section=='about':
        animated=embedded_asset('art/glass-ocean-water-loop-v1.gif')
        water=f'<image id="water-surface-loop" data-water-loop="true" width="900" height="440" href="{animated}" preserveAspectRatio="xMidYMid slice"/>'
        still=('<g class="water-still">'+still+'</g><g class="water-moving">'
               '<use href="#water-surface-loop"/><use href="#water-surface-loop" transform="translate(1800 0) scale(-1 1)"/></g>')
    # Mirrored neighboring tiles meet at identical edge pixels. Only one encoded
    # copy of each image is embedded; all scenery and refraction share the defs.
    return (f'<image id="world-background-image" data-scene-asset="{scene["background"]}" width="900" height="440" href="{background}" preserveAspectRatio="xMidYMid slice"/>'
            +water+'<pattern id="world-panorama" patternUnits="userSpaceOnUse" width="1800" height="440">'
            +still+'</pattern>'
            f'<image id="world-foreground-image" data-scene-asset="{scene["foreground"]}" x="{x}" y="{y}" width="{w}" height="{h}" href="{foreground}" preserveAspectRatio="xMidYMid meet"/>')


def motion():
    selectors=''
    for section,scene in WORLDS.items():
        selectors+=(f'.world-{section}-background{{animation:world-background {scene["background_seconds"]}s linear infinite;}}'
                    f'.world-{section}-foreground{{animation:world-{scene["motion"]} {scene["foreground_seconds"]}s linear -{scene["foreground_seconds"]*.23:g}s infinite;}}')
    return selectors+'''
.water-still{display:none}.water-moving{display:inline}
@media(prefers-reduced-motion:reduce){.water-still{display:inline!important}.water-moving{display:none!important}}
@keyframes world-background{from{transform:translateX(0)}to{transform:translateX(-1800px)}}
@keyframes world-orbital{0%{transform:translate(50px,0);opacity:0}12%,88%{opacity:1}100%{transform:translate(-50px,0);opacity:0}}
@keyframes world-caustics{0%{transform:translate(80px,9px);opacity:0}18%{opacity:.65}75%{opacity:.45}100%{transform:translate(-80px,-9px);opacity:0}}
@keyframes world-jellyfish{0%{transform:translate(35px,30px);opacity:0}16%,82%{opacity:.85}100%{transform:translate(-35px,-30px);opacity:0}}
@keyframes world-terrain{0%{transform:translate(65px,0);opacity:0}12%,88%{opacity:.8}100%{transform:translate(-65px,0);opacity:0}}
'''


def field(height,section):
    scene=WORLDS[section]
    caustics=(f'<g class="world-{section}-foreground"><use href="#world-foreground-image"/></g>'
              if section=='about' else '')
    return (f'<g transform="scale(1 {height/440:.4f})" aria-hidden="true">'
            f'<rect width="900" height="440" fill="{scene["base"]}"/>'
            f'<g class="glass-scene-{section}" data-glass-section="{section}" data-glass-world="{scene["name"]}">'
            f'<g class="world-{section}-background"><rect x="-1800" width="7200" height="440" fill="url(#world-panorama)"/></g>'
            +caustics+
            '<rect width="900" height="440" fill="#061326" fill-opacity=".18"/>'
            '</g></g>')


def foreground(height,section):
    """Near objects stay in focus in front of the refracting glass surface."""
    opacity=' opacity=".45"' if section=='about' else ''
    return (f'<g clip-path="url(#glass-frame)" aria-hidden="true" data-scene-foreground="{section}">'
            f'<g transform="scale(1 {height/440:.4f})"{opacity}><g class="world-{section}-foreground">'
            '<use href="#world-foreground-image"/></g></g></g>')
