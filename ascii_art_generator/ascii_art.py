"""
ASCII Generator Module

This module contains all the ASCII art generation functions.
"""

import math
import random
import time
import sys
from typing import List, Dict, Optional, Tuple


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


def text_to_ascii(text: str, font: str = 'small') -> str:
    """Convert text to ASCII art using the specified font."""
    if font not in FONTS:
        font = 'small'
    
    font_data = FONTS[font]
    lines = [[] for _ in range(5)]
    
    for char in text.upper():
        if char in font_data:
            char_lines = font_data[char]
            for idx, line in enumerate(char_lines):
                lines[idx].append(line)
        else:
            for idx in range(5):
                lines[idx].append("     ")
    
    result = []
    for line in lines:
        result.append(''.join(line))
    
    return '\n'.join(result)


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
    """Draw an approximation of a circle using ASCII characters."""
    result = []
    for y in range(-radius, radius + 1):
        line = []
        for x in range(-radius, radius + 1):
            distance = (x ** 2 + y ** 2) ** 0.5
            if abs(distance - radius) < 0.8:
                line.append(char)
            else:
                line.append(' ')
        result.append(''.join(line))
    return '\n'.join(result)


def draw_heart(size: int = 3, char: str = '*') -> str:
    """Draw a heart shape, scaled by size (rounded lobes, pointed base)."""
    size = min(max(size, 1), 8)
    n = size * 4

    contents = []
    for i in range(n // 2, n + 1, 2):
        gap = n - i
        contents.append(char * i + ' ' * gap + char * i)
    for i in range(n, 0, -1):
        contents.append(char * (2 * i - 1))

    width = max(len(line) for line in contents)
    return '\n'.join(line.center(width) for line in contents)


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


def generate_gradient(width: int = 10, height: int = 5) -> str:
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


def generate_checkerboard(size: int = 8, chars: str = '# ') -> str:
    """Generate a checkerboard pattern."""
    result = []
    for y in range(size):
        line = []
        for x in range(size):
            char_idx = (x + y) % len(chars)
            line.append(chars[char_idx] * 2)
        result.append(''.join(line))
    return '\n'.join(result)


def generate_spiral(size: int = 15, char: str = '*') -> str:
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


def generate_tree(height: int = 5, char: str = '*') -> str:
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


def random_abstract(width: int = 20, height: int = 10) -> str:
    """Generate random abstract ASCII art."""
    chars = '.*:;+*#@&$%^~!=-'
    result = []
    for _ in range(height):
        result.append(''.join([random.choice(chars) for _ in range(width)]))
    return '\n'.join(result)


def random_face() -> str:
    """Generate a random ASCII face."""
    eyes = ['O', 'o', '@', '*', '.', '-', 'x', 'X', '^']
    noses = ['-', '^', 'v', '<', '>']
    mouths = [')', '(', 'D', 'P', 'O', 'o', '/', '\\', '|', '_']
    eye = random.choice(eyes)
    nose = random.choice(noses)
    mouth = random.choice(mouths)
    faces = [
        f" {eye} {nose} {mouth}",
        f" {eye}-{mouth}",
        f" {eye}_{mouth}",
        f" {eye}{nose}{mouth}",
    ]
    return random.choice(faces)


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


def random_animal() -> str:
    """Generate a random ASCII animal."""
    animal = random.choice(list(ANIMALS.keys()))
    return ANIMALS[animal]


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


def get_animal_art(name: str) -> Tuple[str, bool]:
    """Get ASCII art for an animal by name.

    Returns (art, has_dedicated_art). Many animal words are recognized by
    the command parser without a bespoke drawing existing for them - in
    that case this falls back to a drawing from the same visual family when
    one is known (e.g. "eagle" -> a bird we do draw), or a random animal
    otherwise, instead of failing outright.
    """
    if name in ANIMALS:
        return ANIMALS[name], True
    family = ANIMAL_WORD_FAMILY.get(name)
    pool = ANIMAL_FAMILIES.get(family, list(ANIMALS.keys()))
    return ANIMALS[random.choice(pool)], False


def random_emoji() -> str:
    """Generate a random ASCII emoji."""
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
        padding = width - len(line) - 2
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
        'random_abstract': 'Generate random abstract art',
        'random_face': 'Generate a random face',
        'random_animal': 'Generate a random animal',
        'random_emoji': 'Generate a random emoji',
        'create_banner': 'Create a banner',
        'create_box': 'Create a box',
    }
