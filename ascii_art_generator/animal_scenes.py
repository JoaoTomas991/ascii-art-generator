"""
Animal compositions: an animal drawing set inside a coin, a frame or a scene.

`random_animal()` only picks one of a handful of fixed drawings, so it keeps
repeating itself. A composition combines one of those drawings with a random
setting (and random decoration inside it), which multiplies the variety:

- coin:  a round medallion with a caption, e.g. a dog on a "$DOG" coin
- frame: a framed portrait with a title
- scene: the animal in one of several themes (meadow, rain, snow, beach,
         space, forest), each with its own sky, weather, scenery and ground

Everything here returns plain lines (no ANSI colors); `scene_color` suggests a
fitting one and the caller decides whether to apply it.
"""

import math
import random
from typing import Dict, List, Optional, Tuple

from .ascii_art import ANIMALS, get_animal_art

SETTINGS = ('coin', 'frame', 'scene')

_RIM_PAIRS = [('*', 'o'), ('O', 'o'), ('#', '='), ('@', '*'), ('o', '.')]
_FRAME_STYLES = [('+', '-', '|'), ('#', '#', '#'), ('*', '*', '*'), ('+', '=', '|'), ('.', '.', ':')]
_COIN_CAPTIONS = ['${}', '{} COIN', '1 {}', '{} TOKEN']
_FRAME_TITLES = ['~ {} ~', '* {} *', '= {} =', '[ {} ]']

# --- sprites ----------------------------------------------------------------

_SUNS = [
    [r"\ | /", r"-- O --", r"/ | \ "],
    [r" \|/ ", r"-(O)-", r" /|\ "],
]
_MOONS = [
    [r"  _.._ ", r" .' .-'`", r"/  /    ", r"|  |    ", r"\  '.___.;", r" '._  _.'"],
    [r" _ ", r"( \ ", r" \_)"],
]
_CLOUDS = [
    [r" .--. ", r"(    ).", r" `--' "],
    [r"  _  _  ", r" ( `' ) ", r"(_______)"],
]
_PLANETS = [
    [r"   _.-'''-._   ", r" .'  o   .  '. ", r" |  .    O   | ", r" '.   .   o .' ", r"   '-.___.-'   "],
    [r"    ___    ", r" .-'   '-. ", r"'--.___.--'"],
]
_PINES = [
    [r"  /\  ", r" /  \ ", r"/____\ ", r"  ||  "],
    [r"   /\   ", r"  /  \  ", r" /    \ ", r"/______\ ", r"   ||   "],
]
_PALMS = [
    [r" \\ | // ", r"  \\|//  ", r"    |    ", r"    |    "],
]
_ROCKS = [
    [r" .-. ", r"(   )"],
    [r"  __  ", r" /  \_ ", r"/_____\ "],
]

# --- scene themes -----------------------------------------------------------
# sky:       sprites that may hang in the sky (one or more are picked)
# particles: (characters, min, max, rows) scattered before the rest is drawn;
#            rows is 'sky' (only above the animal) or 'all' (the whole scene)
# sides:     scenery placed to the left/right of the animal
# ground:    tiles repeated to fill the ground rows

THEMES: Dict[str, dict] = {
    'meadow': {
        'sky': [_SUNS, _MOONS, _CLOUDS], 'sky_count': (1, 1),
        'particles': ('*.+', 0, 0, 'sky'), 'sides': [],
        'ground': ['"^"^', '~-~-', '_.-._', ',;,;', '=-=-'],
    },
    'rain': {
        'sky': [_CLOUDS], 'sky_count': (2, 3),
        'particles': ("/'|", 16, 26, 'all'), 'sides': [],
        'ground': ['~ ~ ~ ', '- ~ - ~', '_~_~_'],
    },
    'snow': {
        'sky': [_CLOUDS], 'sky_count': (1, 2),
        'particles': ('*.+', 18, 30, 'all'), 'sides': [_PINES],
        'ground': ['_.-._.', '.-""-.', '_.~._.'],
    },
    'beach': {
        'sky': [_SUNS], 'sky_count': (1, 1),
        'particles': ('', 0, 0, 'sky'), 'sides': [_PALMS, _ROCKS],
        'ground': ['.:.:.:', '.,.,.,'],
        'water': ['~^~^', '~-~-', '^~^~'],
    },
    'space': {
        'sky': [_PLANETS], 'sky_count': (1, 1),
        'particles': ('*.+', 10, 16, 'all'), 'sides': [_ROCKS],
        'ground': ['_.-"-._', "-.o.-.O.", '_.._.o._'],
    },
    'forest': {
        'sky': [_CLOUDS], 'sky_count': (0, 1),
        'particles': ('', 0, 0, 'sky'), 'sides': [_PINES],
        'ground': ['"^"^', ',;,;', '"\'"\''],
    },
}
_THEME_COLORS = {
    'meadow': ['light_green', 'light_cyan', 'light_yellow'],
    'rain': ['light_blue', 'cyan'],
    'snow': ['light_white', 'light_cyan', 'white'],
    'beach': ['light_yellow', 'yellow'],
    'space': ['light_magenta', 'magenta', 'light_blue'],
    'forest': ['green', 'light_green'],
}
_COLORS = {
    'coin': ['yellow', 'light_yellow'],
    'frame': ['cyan', 'magenta', 'light_blue', 'light_green', 'light_red'],
    **_THEME_COLORS,
}
# Weights when no setting is given: scenes are the most varied, so favor them.
_SETTING_WEIGHTS = {'coin': 0.25, 'frame': 0.15, 'scene': 0.60}


def _animal_block(name: Optional[str], big: bool) -> Tuple[List[str], str]:
    """The drawing as trimmed lines (common indent and trailing blanks removed)."""
    if name is None:
        name = random.choice(list(ANIMALS))
    art, _ = get_animal_art(name, big)
    lines = [line.rstrip() for line in art.split('\n')]
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    indent = min(len(l) - len(l.lstrip()) for l in lines if l.strip())
    return [l[indent:] for l in lines], name


def _with_caption(block: List[str], caption: str) -> List[str]:
    """The drawing kept rigid (one shared left edge), caption centered under it."""
    block_w = max(len(l) for l in block)
    width = max(block_w, len(caption))
    left = ' ' * ((width - block_w) // 2)
    return [left + l for l in block] + ['', caption.center(width).rstrip()]


def _stamp(canvas: List[List[str]], lines: List[str], top: int, left: int,
           solid: bool = False) -> None:
    """Draw lines onto the canvas; solid also blanks the gaps inside the shape.

    Plain stamping only writes visible characters, so whatever is behind
    (stars, rain, ...) shows through the holes of the drawing. Solid stamping
    treats everything between a line's first and last visible character as
    part of the drawing, so the animal stays clean.
    """
    for dy, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
        first = len(line) - len(line.lstrip())
        last = len(line.rstrip()) - 1
        for dx, ch in enumerate(line):
            y, x = top + dy, left + dx
            if not (0 <= y < len(canvas) and 0 <= x < len(canvas[0])):
                continue
            if ch != ' ' or (solid and first <= dx <= last):
                canvas[y][x] = ch


def _coin(content: List[str]) -> List[str]:
    width = max(len(l) for l in content)
    a, b = width / 2, len(content) / 2
    # Smallest ellipse (terminal cells are ~2x taller than wide, so rx = 2*ry)
    # whose inner area comfortably holds the content's bounding box.
    rx = math.ceil(math.sqrt((a * a + 4 * b * b) / 0.42))
    ry = rx / 2
    cx, cy = rx, math.ceil(ry)
    rim_a, rim_b = random.choice(_RIM_PAIRS)
    inner_ring = random.choice([None, '.', ':'])

    canvas = []
    for y in range(2 * cy + 1):
        row = []
        for x in range(2 * cx + 1):
            d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
            if 0.78 < d <= 1.0:
                row.append(rim_a if (x + y) % 2 == 0 else rim_b)
            elif inner_ring and 0.66 < d <= 0.70:
                row.append(inner_ring)
            else:
                row.append(' ')
        canvas.append(row)

    _stamp(canvas, content, cy - len(content) // 2, cx - width // 2)
    return [''.join(r).rstrip() for r in canvas]


def _frame(content: List[str]) -> List[str]:
    corner, horiz, vert = random.choice(_FRAME_STYLES)
    width = max(len(l) for l in content) + 4
    top = corner + horiz * width + corner
    body = [vert + ('  ' + l).ljust(width) + vert for l in [''] + content + ['']]
    return [top] + body + [top]


def _scene(block: List[str], theme: str) -> List[str]:
    spec = THEMES[theme]
    aw = max(len(l) for l in block)

    sky_sprites = []
    lo, hi = spec['sky_count']
    for _ in range(random.randint(lo, hi)):
        sky_sprites.append(random.choice(random.choice(spec['sky'])))
    sky = max([len(s) for s in sky_sprites] + [4]) + 1

    sides = []
    if spec['sides']:
        # at least one side has scenery; each side is optional beyond that
        flags = random.choice([(1, 0), (0, 1), (1, 1), (1, 1)])
        sides = [random.choice(random.choice(spec['sides'])) if f else None for f in flags]
    side_w = max([len(s[0]) for s in sides if s] + [0])

    width = max(aw + 14, 30, aw + 2 * (side_w + 3))
    ground_rows = 3 if 'water' in spec else 2
    height = sky + len(block) + ground_rows
    canvas = [[' '] * width for _ in range(height)]
    animal_left = (width - aw) // 2
    ground_top = sky + len(block)

    chars, pmin, pmax, area = spec['particles']
    if chars and pmax:
        rows = sky if area == 'sky' else height - ground_rows
        for _ in range(random.randint(pmin, pmax)):
            canvas[random.randrange(rows)][random.randrange(width)] = random.choice(chars)

    for sprite in sky_sprites:
        top = random.randrange(0, max(1, sky - len(sprite) + 1))
        _stamp(canvas, sprite, top, random.randrange(0, max(1, width - len(sprite[0]))), solid=True)

    for i, sprite in enumerate(sides):
        if sprite:
            sw = max(len(l) for l in sprite)
            left = animal_left - sw - 2 if i == 0 else animal_left + aw + 2
            _stamp(canvas, sprite, ground_top - len(sprite), max(0, left), solid=True)

    _stamp(canvas, block, sky, animal_left, solid=True)

    tile = random.choice(spec['ground'])
    for r in range(ground_top, ground_top + 2):
        canvas[r] = list((tile * width)[:width])
    if 'water' in spec:
        canvas[ground_top + 2] = list((random.choice(spec['water']) * width)[:width])
    return [''.join(r).rstrip() for r in canvas]


def scene_color(kind: str) -> str:
    """A color that suits what animal_scene drew (a coin is gold, and so on)."""
    return random.choice(_COLORS[kind])


def animal_scene(name: Optional[str] = None, big: bool = True,
                 setting: Optional[str] = None) -> Tuple[List[str], str]:
    """Compose an animal in a random (or given) setting.

    name=None picks any animal; big=True (the default) uses the larger
    drawing, which leaves more room for detail and decoration. setting is
    one of SETTINGS or a scene theme name (see THEMES); None picks at random.
    Returns (lines, kind) where kind is 'coin', 'frame' or the theme name, to
    be passed to scene_color.
    """
    if setting is None:
        setting = random.choices(list(_SETTING_WEIGHTS), list(_SETTING_WEIGHTS.values()))[0]
    if setting not in SETTINGS and setting not in THEMES:
        raise ValueError(f"unknown setting {setting!r}; choose from {SETTINGS + tuple(THEMES)}")
    block, name = _animal_block(name, big)
    label = name.upper()

    if setting == 'coin':
        caption = random.choice(_COIN_CAPTIONS).format(label)
        return _coin(_with_caption(block, caption)), 'coin'
    if setting == 'frame':
        title = random.choice(_FRAME_TITLES).format(label)
        return _frame(_with_caption(block, title)), 'frame'
    theme = setting if setting in THEMES else random.choice(list(THEMES))
    return _scene(block, theme), theme
