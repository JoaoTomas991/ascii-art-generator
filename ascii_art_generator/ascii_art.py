"""
ASCII Generator Module

This module contains all the ASCII art generation functions.
"""

import math
import random
import time
import shutil
import sys
from typing import List, Dict, Optional, Tuple

from .emoji_art import emoji_face


# =============================================================================
# TEXT TO ASCII ART
# =============================================================================

# Built-in ASCII fonts
FONT_SMALL = {
    'A': ["  A  ", " A A ", "AAAAA", "A   A", "A   A"],
    'B': ["BBBB ", "B   B", "BBBB ", "B   B", "BBBB "],
    'C': [" CCCC", "C    ", "C    ", "C    ", " CCCC"],
    'D': ["DDDD ", "D   D", "D   D", "D   D", "DDDD "],
    'E': ["EEEEE", "E    ", "EEEEE", "E    ", "EEEEE"],
    'F': ["FFFFF", "F    ", "FFFF ", "F    ", "F    "],
    'G': [" GGGG", "G    ", "G  GG", "G   G", " GGGG"],
    'H': ["H   H", "H   H", "HHHHH", "H   H", "H   H"],
    'I': ["IIIII", "  I  ", "  I  ", "  I  ", "IIIII"],
    'J': ["JJJJJ", "   J ", "   J ", "J  J ", " JJ  "],
    'K': ["K   K", "K  K ", "KKK  ", "K  K ", "K   K"],
    'L': ["L    ", "L    ", "L    ", "L    ", "LLLLL"],
    'M': ["M   M", "MM MM", "M M M", "M   M", "M   M"],
    'N': ["N   N", "NN  N", "N N N", "N  NN", "N   N"],
    'O': [" OOO ", "O   O", "O   O", "O   O", " OOO "],
    'P': ["PPPP ", "P   P", "PPPP ", "P    ", "P    "],
    'Q': [" QQQ ", "Q   Q", "Q   Q", "Q  Q ", " QQ Q"],
    'R': ["RRRR ", "R   R", "RRRR ", "R  R ", "R   R"],
    'S': [" SSS ", "S    ", " SSS ", "    S", "SSSS "],
    'T': ["TTTTT", "  T  ", "  T  ", "  T  ", "  T  "],
    'U': ["U   U", "U   U", "U   U", "U   U", " UUU "],
    'V': ["V   V", "V   V", "V   V", " V V ", "  V  "],
    'W': ["W   W", "W   W", "W W W", "WW WW", "W   W"],
    'X': ["X   X", " X X ", "  X  ", " X X ", "X   X"],
    'Y': ["Y   Y", " Y Y ", "  Y  ", "  Y  ", "  Y  "],
    'Z': ["ZZZZZ", "   Z ", "  Z  ", " Z   ", "ZZZZZ"],
    ' ': ["     ", "     ", "     ", "     ", "     "],
    '!': ["  !  ", "  !  ", "  !  ", "     ", "  !  "],
    '?': ["  ?  ", " ? ? ", "  ?  ", "     ", "  ?  "],
}

# Font BLOCK - letters are filled
FONT_BLOCK = {
    'A': ["  A  ", " A A ", "AAAAA", "A   A", "A   A"],
    'B': ["BBBB ", "B   B", "BBBB ", "B   B", "BBBB "],
    'C': [" CCC ", "C   C", "C    ", "C   C", " CCC "],
    'D': ["DDDD ", "D   D", "D   D", "D   D", "DDDD "],
    'E': ["EEEEE", "E    ", "EEEEE", "E    ", "EEEEE"],
    'F': ["FFFFF", "F    ", "FFFF ", "F    ", "F    "],
    'G': [" GGG ", "G    ", "G  GG", "G   G", " GGG "],
    'H': ["H   H", "H   H", "HHHHH", "H   H", "H   H"],
    'I': ["IIIII", "  I  ", "  I  ", "  I  ", "IIIII"],
    'J': ["JJJJJ", "   J ", "   J ", "J  J ", " JJ  "],
    'K': ["K   K", "K  K ", "KKKK ", "K  K ", "K   K"],
    'L': ["L    ", "L    ", "L    ", "L    ", "LLLLL"],
    'M': ["M   M", "MM MM", "M M M", "M   M", "M   M"],
    'N': ["N   N", "NN  N", "N N N", "N  NN", "N   N"],
    'O': [" OOO ", "O   O", "O   O", "O   O", " OOO "],
    'P': ["PPPP ", "P   P", "PPPP ", "P    ", "P    "],
    'Q': [" QQQ ", "Q   Q", "Q   Q", "Q  Q ", " QQ Q"],
    'R': ["RRRR ", "R   R", "RRRR ", "R  R ", "R   R"],
    'S': [" SSSS", "S    ", " SSS ", "    S", "SSSS "],
    'T': ["TTTTT", "  T  ", "  T  ", "  T  ", "  T  "],
    'U': ["U   U", "U   U", "U   U", "U   U", " UUU "],
    'V': ["V   V", "V   V", "V   V", " V V ", "  V  "],
    'W': ["W   W", "W   W", "W W W", "WW WW", "W   W"],
    'X': ["X   X", " X X ", "  X  ", " X X ", "X   X"],
    'Y': ["Y   Y", " Y Y ", "  Y  ", "  Y  ", "  Y  "],
    'Z': ["ZZZZZ", "   Z ", "  Z  ", " Z   ", "ZZZZZ"],
    ' ': ["     ", "     ", "     ", "     ", "     "],
}

# Font BANNER - large block letters
FONT_BANNER = {
    'A': ["  A  ", " A A ", "AAAAA", "A   A", "A   A"],
    'B': ["BBBBB", "B    ", "BBBB ", "B    ", "BBBBB"],
    'C': [" CCCC", "C    ", "C    ", "C    ", " CCCC"],
    'D': ["DDDD ", "D   D", "D   D", "D   D", "DDDD "],
    'E': ["EEEEE", "E    ", "EEEEE", "E    ", "EEEEE"],
    'F': ["FFFFF", "F    ", "FFFF ", "F    ", "F    "],
    'G': [" GGGG", "G    ", "G  GG", "G   G", " GGGG"],
    'H': ["H   H", "H   H", "HHHHH", "H   H", "H   H"],
    'I': ["IIIII", "  I  ", "  I  ", "  I  ", "IIIII"],
    'J': ["  J  ", "  J  ", "  J  ", "J J  ", " JJ  "],
    'K': ["K   K", "K  K ", "KKK  ", "K  K ", "K   K"],
    'L': ["L    ", "L    ", "L    ", "L    ", "LLLLL"],
    'M': ["M   M", "MM MM", "M M M", "M   M", "M   M"],
    'N': ["N   N", "NN  N", "N N N", "N  NN", "N   N"],
    'O': [" OOO ", "O   O", "O   O", "O   O", " OOO "],
    'P': ["PPPP ", "P   P", "PPPP ", "P    ", "P    "],
    'R': ["RRRR ", "R   R", "RRRR ", "R  R ", "R   R"],
    'S': [" SSS ", "S    ", " SSS ", "    S", "SSSS "],
    'T': ["TTTTT", "  T  ", "  T  ", "  T  ", "  T  "],
    'U': ["U   U", "U   U", "U   U", "U   U", " UUU "],
    'V': ["V   V", "V   V", " V V ", " V V ", "  V  "],
    'W': ["W   W", "W   W", "W W W", "WW WW", "W   W"],
    'X': ["X   X", " X X ", "  X  ", " X X ", "X   X"],
    'Y': ["Y   Y", " Y Y ", "  Y  ", "  Y  ", "  Y  "],
    'Z': ["ZZZZZ", "   Z ", "  Z  ", " Z   ", "ZZZZZ"],
    ' ': ["     ", "     ", "     ", "     ", "     "],
}

# Font SHADOW - letters with shadow effect
FONT_SHADOW = {
    'A': ["  A  ", " A A ", "AAAAA", "A   A", "A   A"],
    'B': ["BBBB  ", "B   B ", "BBBB  ", "B   B ", "BBBB  "],
    'C': [" CCCC ", "C     ", "C     ", "C     ", " CCCC "],
    'D': ["DDDD  ", "D   D ", "D   D ", "D   D ", "DDDD  "],
    'E': ["EEEEE ", "E     ", "EEEEE ", "E     ", "EEEEE "],
    'F': ["FFFFF ", "F     ", "FFFF  ", "F     ", "F     "],
    'G': [" GGGG ", "G     ", "G  GG ", "G   G ", " GGGG "],
    'H': ["H   H ", "H   H ", "HHHHH ", "H   H ", "H   H "],
    'I': ["IIIII ", "  I   ", "  I   ", "  I   ", "IIIII "],
    'J': ["JJJJJ ", "   J  ", "   J  ", "J  J  ", " JJ   "],
    'K': ["K   K ", "K  K  ", "KKKK  ", "K  K  ", "K   K "],
    'L': ["L     ", "L     ", "L     ", "L     ", "LLLLL "],
    'M': ["M   M ", "MM MM ", "M M M ", "M   M ", "M   M "],
    'N': ["N   N ", "NN  N ", "N N N ", "N  NN ", "N   N "],
    'O': [" OOO  ", "O   O ", "O   O ", "O   O ", " OOO  "],
    'P': ["PPPP  ", "P   P ", "PPPP  ", "P     ", "P     "],
    'R': ["RRRR  ", "R   R ", "RRRR  ", "R  R  ", "R   R "],
    'S': [" SSSS ", "S     ", " SSS  ", "    S ", "SSSS  "],
    'T': ["TTTTT ", "  T   ", "  T   ", "  T   ", "  T   "],
    'U': ["U   U ", "U   U ", "U   U ", "U   U ", " UUU  "],
    'V': ["V   V ", "V   V ", " V V  ", " V V  ", "  V   "],
    'W': ["W   W ", "W   W ", "W W W ", "WW WW ", "W   W "],
    'X': ["X   X ", " X X  ", "  X   ", " X X  ", "X   X "],
    'Y': ["Y   Y ", " Y Y  ", "  Y   ", "  Y   ", "  Y   "],
    'Z': ["ZZZZZ ", "   Z  ", "  Z   ", " Z    ", "ZZZZZ "],
    ' ': ["      ", "      ", "      ", "      ", "      "],
}

FONTS = {
    'small': FONT_SMALL,
    'block': FONT_BLOCK,
    'banner': FONT_BANNER,
    'shadow': FONT_SHADOW,
}


# The project's font names map onto real FIGlet fonts when pyfiglet is
# installed; any other FIGlet font name (e.g. "slant", "ansi_shadow") is
# also accepted as-is. The built-in FONTS above are only the fallback.
FIGLET_FONT_ALIASES = {
    'small': 'small',
    'block': 'block',
    'banner': 'banner3',
    'shadow': 'shadow',
    'solid': 'banner',      # pyfiglet's solid-stroke '#' font (used for the startup banner)
}

# Drawn for characters a built-in font has no glyph for, so they're visibly
# unsupported instead of silently turning into blank space.
_MISSING_GLYPH = [" ??? ", "?   ?", "  ?? ", "     ", "  ?  "]


def _figlet_to_ascii(text: str, font: str) -> Optional[str]:
    """Render text with pyfiglet, or return None if it isn't installed.

    The import is deferred (like Pillow in image_art.py) so pyfiglet stays
    an optional dependency: without it, text_to_ascii() falls back to the
    built-in fonts.
    """
    try:
        import pyfiglet
    except ImportError:
        return None

    figlet_font = FIGLET_FONT_ALIASES.get(font, font)
    width = shutil.get_terminal_size((120, 24)).columns
    try:
        figlet = pyfiglet.Figlet(font=figlet_font, width=width)
    except pyfiglet.FontNotFound:
        try:
            figlet = pyfiglet.Figlet(font=FIGLET_FONT_ALIASES['small'], width=width)
        except pyfiglet.FontNotFound:
            # pyfiglet is importable but ships no usable fonts (e.g. a
            # PyInstaller build missing --collect-data pyfiglet): fall back
            # to the built-in fonts instead of crashing.
            return None

    # pyfiglet silently drops characters the font has no glyph for (e.g.
    # accented letters in most fonts); draw '?' instead, like the built-in
    # fonts' _MISSING_GLYPH, so they're visibly unsupported.
    glyphs = figlet.Font.chars
    text = ''.join(c if c == '\n' or ord(c) in glyphs else '?' for c in text)
    try:
        rendered = figlet.renderText(text)
    except pyfiglet.CharNotPrinted:
        # Terminal narrower than a single glyph: pyfiglet refuses to render.
        # Give up on wrapping to the terminal width instead of crashing.
        figlet.width = 1000
        rendered = figlet.renderText(text)

    lines = rendered.split('\n')
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return '\n'.join(lines)


def text_to_ascii(text: str, font: str = 'small') -> str:
    """Convert text to ASCII art using the specified font."""
    figlet = _figlet_to_ascii(text, font)
    if figlet is not None:
        return figlet

    if font not in FONTS:
        font = 'small'
    
    font_data = FONTS[font]
    lines = [[] for _ in range(5)]
    
    for char in text.upper():
        char_lines = font_data.get(char, _MISSING_GLYPH)
        for idx, line in enumerate(char_lines):
            lines[idx].append(line)
    
    # One column of spacing so neighbouring letters don't run together.
    return '\n'.join(' '.join(line) for line in lines)


# =============================================================================
# GEOMETRIC SHAPES
# =============================================================================


def draw_rectangle(width: int, height: int, char: str = '#', filled: bool = True) -> str:
    """Draw a rectangle with the given dimensions."""
    if width < 2 or height < 2:
        return char * max(width, 1)
    
    result = []
    for y in range(height):
        if filled or y == 0 or y == height - 1:
            result.append(char * width)
        else:
            result.append(char + ' ' * (width - 2) + char)
    return '\n'.join(result)


def draw_triangle(height: int, char: str = '*', direction: str = 'up') -> str:
    """Draw a triangle pointing in the specified direction."""
    result = []
    
    if direction == 'up':
        for i in range(1, height + 1):
            spaces = ' ' * (height - i)
            stars = char * (2 * i - 1)
            result.append(spaces + stars)
    elif direction == 'down':
        for i in range(height, 0, -1):
            spaces = ' ' * (height - i)
            stars = char * (2 * i - 1)
            result.append(spaces + stars)
    elif direction == 'left':
        for i in range(1, height + 1):
            result.append(char * i)
        for i in range(height - 1, 0, -1):
            result.append(char * i)
    elif direction == 'right':
        for i in range(1, height + 1):
            spaces = ' ' * (height - i)
            result.append(spaces + char * i)
        for i in range(height - 1, 0, -1):
            spaces = ' ' * (height - i)
            result.append(spaces + char * i)
    
    return '\n'.join(result)


def draw_circle(radius: int, char: str = 'O') -> str:
    """Draw an approximation of a circle using ASCII characters.

    Terminal characters are roughly twice as tall as they are wide, so the
    x axis is scanned at double resolution and halved before the distance
    check - without this the circle renders as a tall egg shape instead of
    round (same correction draw_star uses).
    """
    result = []
    for y in range(-radius, radius + 1):
        line = []
        for x in range(-radius * 2, radius * 2 + 1):
            distance = ((x / 2) ** 2 + y ** 2) ** 0.5
            if abs(distance - radius) < 0.8:
                line.append(char)
            else:
                line.append(' ')
        result.append(''.join(line))
    return '\n'.join(result)


def draw_heart(size: int = 6, char: str = '*') -> str:
    """Draw a heart shape, scaled by size (round lobes, smooth pointed base).

    Samples the classic implicit heart curve (x^2 + y^2 - 1)^3 - x^2 * y^3 <= 0
    on a character grid. The grid starts 5 * size + 1 rows tall (blank edge
    rows are trimmed afterwards) and about 2.1x as many columns wide, which
    compensates for terminal characters being roughly twice as tall as they
    are wide. The result is left-right symmetric, with a dip between the lobes
    and no trailing padding.
    """
    size = min(max(size, 1), 12)
    rows = 5 * size + 1
    cols = int(rows * 2.1) // 2 * 2   # even, so the cleft sits on a column boundary

    # The curve spans x in [-1.135, 1.135] and y in [-1.0, 1.235]; pad slightly.
    x_max, y_min, y_max = 1.15, -1.01, 1.25
    lines = []
    for r in range(rows):
        y = y_max - (r + 0.5) * (y_max - y_min) / rows
        line = []
        for c in range(cols):
            x = -x_max + (c + 0.5) * (2 * x_max) / cols
            inside = (x * x + y * y - 1) ** 3 - x * x * y ** 3 <= 0
            line.append(char if inside else ' ')
        lines.append(''.join(line).rstrip())

    while lines and not lines[-1]:   # the sampling grid is padded; drop empty edge rows
        lines.pop()
    while lines and not lines[0]:
        lines.pop(0)
    indent = min(len(l) - len(l.lstrip()) for l in lines if l.strip())
    return '\n'.join(l[indent:] for l in lines)


def draw_diamond(size: int, char: str = '*') -> str:
    """Draw a diamond shape."""
    result = []
    for i in range(1, size + 1):
        spaces = ' ' * (size - i)
        result.append(spaces + char * (2 * i - 1))
    for i in range(size - 1, 0, -1):
        spaces = ' ' * (size - i)
        result.append(spaces + char * (2 * i - 1))
    return '\n'.join(result)


# =============================================================================
# PATTERNS
# =============================================================================


def generate_gradient(width: int = 32, height: int = 8) -> str:
    """Generate a gradient pattern."""
    chars = ['.', ',', ':', ';', 'i', 'l', '!', 'I', 'L', '@', '#', '*']
    result = []
    for y in range(height):
        line = []
        for x in range(width):
            idx = (x + y) % len(chars)
            line.append(chars[idx] * 2)
        result.append(''.join(line))
    return '\n'.join(result)


def generate_checkerboard(size: int = 12, chars: str = '# ') -> str:
    """Generate a checkerboard pattern."""
    result = []
    for y in range(size):
        line = []
        for x in range(size):
            char_idx = (x + y) % len(chars)
            line.append(chars[char_idx] * 2)
        result.append(''.join(line))
    return '\n'.join(result)


def generate_spiral(size: int = 18, char: str = '*') -> str:
    """Generate a spiral pattern (Archimedean spiral traced onto a grid)."""
    grid = [[' ' for _ in range(size)] for _ in range(size)]
    center = (size - 1) / 2
    max_radius = size / 2 - 0.5
    turns = 2.2
    arc_step = 0.75
    max_angle = turns * 2 * math.pi

    theta = 0.0
    while theta <= max_angle:
        radius = (theta / max_angle) * max_radius
        x = center + radius * math.cos(theta)
        y = center + radius * math.sin(theta)
        xi, yi = int(round(x)), int(round(y))
        if 0 <= xi < size and 0 <= yi < size:
            grid[yi][xi] = char
        # Keep the arc-length step roughly constant so the curve stays
        # continuous without over-plotting near the center.
        theta += arc_step / max(radius, 1.5)

    return '\n'.join([''.join(row) for row in grid])


def generate_tree(height: int = 8, char: str = '*') -> str:
    """Generate a Christmas tree."""
    result = []
    for i in range(1, height + 1):
        spaces = ' ' * (height - i)
        result.append(spaces + char * (2 * i - 1))
    trunk_width = max(1, height // 2)
    trunk_spaces = ' ' * (height - trunk_width)
    trunk = '|' * (2 * trunk_width - 1)
    result.append(trunk_spaces + trunk)
    return '\n'.join(result)


# =============================================================================
# RANDOM GENERATORS
# =============================================================================


ANIMALS = {
    'cat': " /\\_/\\ \n( o.o ) \n > ^ < ",
    'dog': "  / \\__\n (    @\\___\n /         O\n/   (_____/\n/_____/   U",
    'owl': "  /\\ \n (oo) \n /\\/\\ ",
    'penguin': "  _(__) \n <(.)__ \n  (___)",
    'fish': "  >=====| \n (     ) \n  >=====| ",
    'bear': "  (\\___/) \n  (U^._.^U) \n  /  \\  3 ",
    'rabbit': "  (\\_)~ \n  (='.'=) \n  (\" _) (\" _)",
    'crow': "  _~_ \n /\\  /\\ \n(  .  .  )\n  >=v=< \n /\\  /\\ \n_~_   _~_",
    'raven': "   .-^~ \n  /   @  @ \\ \n |         |\n  \\  >^<  /\n   '-...-' ",
}


# Bigger, more detailed drawings of the same animals, used for "draw a big
# cat" / "a large dog" etc. Every key in ANIMALS must also exist here, so
# get_animal_art(name, big=True) works for any animal with dedicated art.
ANIMALS_BIG = {name: art.strip('\n') for name, art in {
'cat': r"""
     /\_____/\
    /  o   o  \
   ( ==  ^  == )
    )         (
   (           )
  ( (  )   (  ) )
 (__(__)___(__)__)
""",
'dog': r"""
   .-"-.______.-"-.
  /  /          \  \
 |  /   o    o   \  |
 | |      __      | |
  \|     (__)     |/
    \    \__/    /
     '.________.'
      /        \
     (_|      |_)
""",
'owl': r"""
   ,_         _,
   |\\.-'~~~'-.//|
   \`         `/
  /    _   _    \
  |   (o) (o)   |
  \      V      /
   \  \_____/  /
    `.       .'
     /`-----`\
    /  |   |  \
    ^^^^   ^^^^
""",
'penguin': r"""
      .---.
     / o o \
     \  v  /
    /'-----'\
   / /     \ \
  ( (       ) )
   \ \     / /
    '-'---'-'
     _/   \_
""",
'fish': r"""
        _.-'''''-._
      .'  o        '.  /|
     (  <)   ))  ))  ><  |
      '.           .'  \|
        '-._____.-'
""",
'bear': r"""
   .-.       .-.
  (   '-----'   )
   \  o     o  /
   |     ^     |
    \  '---'  /
   .'-._____.-'.
  /  /       \  \
 (__(         )__)
     \__/ \__/
""",
'rabbit': r"""
    (\       /)
     \\     //
      )\___/(
     ( o   o )
    (  = v =  )
     (  ---  )
   ( _)     (_ )
   (__)-----(__)
""",
'crow': r"""
         ___
       _/ o \__
      /       __>
     /  /\   (
    /  /  \   \
   <__/    \___\
       |    |
   ----+----+----
""",
'raven': r"""
  __                 __
  \ \__    ___    __/ /
   \   \__/ o \__/   /
    \______   ______/
           \ /
            V
""",
}.items()}
assert set(ANIMALS) == set(ANIMALS_BIG), \
    'ANIMALS and ANIMALS_BIG must have the same animals'


def random_animal(big: bool = False) -> str:
    """Generate a random ASCII animal (a bigger drawing if big=True)."""
    drawings = ANIMALS_BIG if big else ANIMALS
    return random.choice(list(drawings.values()))


# Visual families used to pick a plausible fallback drawing for animal
# words the parser recognizes but that don't have bespoke art of their own
# (see get_animal_art below) - e.g. "eagle" falls back to a bird we do
# draw instead of a random animal from any family.
ANIMAL_FAMILIES: Dict[str, List[str]] = {
    'bird': ['crow', 'raven', 'owl'],
    'fish': ['fish'],
    'cat': ['cat'],
    'dog': ['dog'],
    'bear': ['bear'],
    'rabbit': ['rabbit'],
    'penguin': ['penguin'],
}

# Common animal nouns without their own drawing, mapped to the family whose
# art best represents them. Anything not listed here still resolves (via
# get_animal_art's fallback) to a random animal instead of failing.
ANIMAL_WORD_FAMILY: Dict[str, str] = {
    # birds
    'bird': 'bird', 'eagle': 'bird', 'hawk': 'bird', 'sparrow': 'bird',
    'seagull': 'bird', 'dove': 'bird', 'parrot': 'bird', 'peacock': 'bird',
    'duck': 'bird', 'goose': 'bird', 'swan': 'bird', 'pigeon': 'bird',
    'falcon': 'bird', 'vulture': 'bird', 'flamingo': 'bird',
    'woodpecker': 'bird', 'robin': 'bird', 'canary': 'bird', 'stork': 'bird',
    'pelican': 'bird', 'toucan': 'bird', 'chicken': 'bird', 'hen': 'bird',
    'rooster': 'bird', 'turkey': 'bird', 'ostrich': 'bird',
    # fish / sea creatures
    'shark': 'fish', 'salmon': 'fish', 'tuna': 'fish', 'goldfish': 'fish',
    'trout': 'fish', 'bass': 'fish', 'carp': 'fish', 'eel': 'fish',
    'whale': 'fish', 'dolphin': 'fish', 'stingray': 'fish',
    # cat family
    'kitten': 'cat', 'kitty': 'cat', 'lion': 'cat', 'tiger': 'cat',
    'leopard': 'cat', 'panther': 'cat', 'lynx': 'cat', 'jaguar': 'cat',
    'cheetah': 'cat',
    # dog family
    'puppy': 'dog', 'wolf': 'dog', 'fox': 'dog', 'hound': 'dog',
    'husky': 'dog', 'poodle': 'dog', 'coyote': 'dog', 'jackal': 'dog',
    # bear family
    'panda': 'bear', 'koala': 'bear', 'grizzly': 'bear',
    # rabbit family
    'bunny': 'rabbit', 'hare': 'rabbit',
}

# Animal words with no obvious matching family - still recognized as "the
# user wants an animal", but get_animal_art falls back to a fully random
# pick among ANIMALS for these.
UNCATEGORIZED_ANIMAL_WORDS = [
    'horse', 'snake', 'elephant', 'mouse', 'rat', 'frog', 'toad', 'sheep',
    'lamb', 'cow', 'bull', 'pig', 'spider', 'turtle', 'tortoise', 'monkey',
    'ape', 'gorilla', 'chimpanzee', 'chimp', 'giraffe', 'zebra', 'kangaroo',
    'deer', 'goat', 'hedgehog', 'squirrel', 'camel', 'donkey', 'mule',
    'bat', 'hippo', 'hippopotamus', 'octopus', 'crab', 'lobster', 'shrimp',
    'jellyfish', 'ant', 'bee', 'wasp', 'worm', 'alligator', 'crocodile',
    'seal', 'walrus', 'otter', 'beaver', 'moose', 'buffalo', 'bison',
    'raccoon', 'skunk', 'mole', 'weasel', 'ferret', 'gecko', 'iguana',
    'chameleon', 'scorpion', 'centipede',
]

# Every word the parser should recognize as "the user wants an animal" -
# both the ones with dedicated art (ANIMALS' own keys) and the broader
# vocabulary above. Exposed so cli.py's SHAPE_SYNONYMS doesn't need to
# maintain its own separate copy of this list.
KNOWN_ANIMAL_WORDS: List[str] = sorted(
    set(ANIMALS.keys()) | set(ANIMAL_WORD_FAMILY.keys()) | set(UNCATEGORIZED_ANIMAL_WORDS)
)


def get_animal_art(name: str, big: bool = False) -> Tuple[str, bool]:
    """Get ASCII art for an animal by name.

    Returns (art, has_dedicated_art). Many animal words are recognized by
    the command parser without a bespoke drawing existing for them - in
    that case this falls back to a drawing from the same visual family when
    one is known (e.g. "eagle" -> a bird we do draw), or a random animal
    otherwise, instead of failing outright. big=True picks the larger
    drawing from ANIMALS_BIG instead of ANIMALS.
    """
    drawings = ANIMALS_BIG if big else ANIMALS
    if name in drawings:
        return drawings[name], True
    family = ANIMAL_WORD_FAMILY.get(name)
    pool = ANIMAL_FAMILIES.get(family, list(drawings.keys()))
    return drawings[random.choice(pool)], False


def random_emoji(big: bool = True) -> str:
    """Generate a random emoji: a composed face (big=True, the default, about
    the size of a big animal) or a one-line kaomoji (big=False)."""
    if big:
        return '\n'.join(emoji_face()[0])
    emojis = [
        "(^_^)", "(>_<)", "(≧∇≦)", "(≧▽≦)", "(⊙_⊙)",
        "(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧", "(✿◠‿◠)", "(◕ ◡ ◕)",
        "(⊙ > ◕)", "(◕ < ◕)", "(⊙ _ ☉)",
        "(/▽＼)", "(◕︵◕)", "(ﾟ∀ﾟ；)", "(¬‿¬)",
    ]
    return random.choice(emojis)


# =============================================================================
# BANNERS AND BOXES
# =============================================================================


def create_banner(text: str, width: int = 50, char: str = '=') -> str:
    """Create a banner with the given text."""
    padding = (width - len(text) - 2) // 2
    border = char * width
    lines = [
        border,
        char + ' ' * (width - 2) + char,
        char + ' ' * padding + text + ' ' * (width - padding - len(text) - 2) + char,
        char + ' ' * (width - 2) + char,
        border
    ]
    return '\n'.join(lines)


def create_box(text: str, width: Optional[int] = None, char: str = '#') -> str:
    """Create a box with the given text."""
    if width is None:
        width = max(len(line) for line in text.split('\n')) + 4
    lines = text.split('\n')
    border = char * width
    result = [border]
    for line in lines:
        padding = width - len(line) - 3
        result.append(char + ' ' + line + ' ' * padding + char)
    result.append(border)
    return '\n'.join(result)


# =============================================================================
# ANIMATIONS
# =============================================================================


def spinner_animation(duration: float = 2.0) -> None:
    """Display a spinning animation."""
    spinner = ['|', '/', '-', '\\']
    end_time = time.time() + duration
    while time.time() < end_time:
        for spin in spinner:
            sys.stdout.write(f'\r{spin} Loading...')
            sys.stdout.flush()
            time.sleep(0.1)
    print()


def progress_bar(duration: float = 3.0, char: str = '=') -> None:
    """Display a progress bar animation."""
    width = 40
    end_time = time.time() + duration
    while time.time() < end_time:
        elapsed = time.time() - (end_time - duration)
        progress = min(elapsed / duration, 1.0)
        filled = int(width * progress)
        bar = char * filled + ' ' * (width - filled)
        sys.stdout.write(f'\r[{bar}] {progress * 100:.1f}%')
        sys.stdout.flush()
        time.sleep(0.05)
    print()


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================


def get_available_fonts() -> List[str]:
    """Get list of available fonts."""
    return list(FONTS.keys())


# =============================================================================
# FILL STYLES FOR SHAPES
# =============================================================================

def get_fill_style_pattern(style: str, width: int, height: int) -> str:
    """Generate a fill pattern based on style."""
    patterns = {
        'empty': ' ',
        'solid': '#',
        'dotted': '.',
        'striped_h': '-',
        'striped_v': '|',
        'crosshatch': 'X',
        'plus': '+',
        'star': '*',
        'random': None,  # Will be handled separately
        'gradient': None,  # Will be handled separately
    }
    
    if style in patterns:
        char = patterns[style]
        if char:
            return char
    
    return '#'  # default


def generate_gradient_fill(width: int, height: int) -> str:
    """Generate a gradient fill pattern."""
    chars = ['.', ':', ';', 'i', 'l', '!', 'I', 'L', '@', '#', '*']
    result = []
    for y in range(height):
        line = []
        for x in range(width):
            idx = (x + y) % len(chars)
            line.append(chars[idx])
        result.append(''.join(line))
    return '\n'.join(result)


# =============================================================================
# BORDER STYLES
# =============================================================================

def get_border_chars(style: str):
    """Get border characters for a given style."""
    border_styles = {
        'simple': ('#', '#', '#', '#'),  # top, bottom, left, right
        'double': ('=', '=', '||', '||'),  # Double lines
        'dashed': ('-', '-', '|', '|'),
        'wavy': ('~', '~', '{', '}'),
        'bold': ('█', '█', '█', '█'),
        'light': ('.', '.', '.', '.'),
        'star': ('*', '*', '*', '*'),
        'plus': ('+', '+', '+', '+'),
    }
    return border_styles.get(style, border_styles['simple'])


# =============================================================================
# COLOR MAPPING (ANSI colors)
# =============================================================================

def get_color_code(color_name: str) -> str:
    """Get ANSI color code for a given color name."""
    color_map = {
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'bright_black': '\033[90m',
        'bright_red': '\033[91m',
        'bright_green': '\033[92m',
        'bright_yellow': '\033[93m',
        'bright_blue': '\033[94m',
        'bright_magenta': '\033[95m',
        'bright_cyan': '\033[96m',
        'bright_white': '\033[97m',
        'reset': '\033[0m',
        '': '\033[0m',
    }
    return color_map.get(color_name.lower(), color_map['reset'])


def get_all_functions() -> Dict[str, str]:
    """Get all available ASCII art functions."""
    return {
        'text_to_ascii': 'Convert text to ASCII art',
        'draw_rectangle': 'Draw a rectangle',
        'draw_triangle': 'Draw a triangle',
        'draw_circle': 'Draw a circle',
        'draw_heart': 'Draw a heart',
        'draw_diamond': 'Draw a diamond',
        'generate_gradient': 'Generate a gradient pattern',
        'generate_checkerboard': 'Generate a checkerboard',
        'generate_spiral': 'Generate a spiral',
        'generate_tree': 'Generate a tree',
        'random_animal': 'Generate a random animal',
        'random_emoji': 'Generate a random emoji',
        'create_banner': 'Create a banner',
        'create_box': 'Create a box',
    }
