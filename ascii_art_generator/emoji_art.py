"""
Big emoji faces, composed from a round head plus eyes, brows, a mouth and extras.

`random_emoji()` used to pick one of a few one-line kaomoji. A face composed
here is about as big as a large animal drawing and varies much more: each
mood (happy, wink, sad, angry, ...) lists the eyes, brows, mouths and extras
that belong together, so a random pick is always a coherent expression.

Everything is plain ASCII and returns plain lines (no ANSI colors).
"""

import random
from typing import Dict, List, Optional, Tuple

# The head is 21 columns by 11 rows. Anything drawn on it is placed with the
# coordinates below: the eyes sit on rows 4-5 around columns 5 and 15, the
# brows on row 3, cheeks or tears on row 6 and the mouth on rows 7-9.
_HEAD = [
    '     .-"""""""-.     ',
    "   .'           '.   ",
    " .'               '. ",
    "/                   \\",
    "|                   |",
    "|                   |",
    "|                   |",
    "\\                   /",
    " '.               .' ",
    "   '.           .'   ",
    "     '-._____.-'     ",
]
_WIDTH = 21
assert all(len(row) == _WIDTH for row in _HEAD), "every _HEAD row must be _WIDTH wide"
_EYE_CENTERS = (5, 15)
_MARGIN = 6   # blank columns each side of the head, for hearts, sparkles and the like

# --- parts ------------------------------------------------------------------
# Eyes: (left, right) sprites of two rows each. Brows: (left, right) strings.
# Mouths: three rows, centered under the nose.

_EYES: Dict[str, Tuple[List[str], List[str]]] = {
    'open':   ([".-.", "(o)"], [".-.", "(o)"]),
    'wide':   ([".-.", "(O)"], [".-.", "(O)"]),
    'dot':    (["   ", " o "], ["   ", " o "]),
    'happy':  ([".-.", "   "], [".-.", "   "]),
    'sleepy': (["   ", "'-'"], ["   ", "'-'"]),
    'wink':   ([".-.", "(o)"], ["   ", "---"]),
    'x':      (["\\ /", "/ \\"], ["\\ /", "/ \\"]),
    'star':   (["\\|/", "/|\\"], ["\\|/", "/|\\"]),
    'heart':  (["(\\/)", " \\/ "], ["(\\/)", " \\/ "]),
}
_SHADES = [
    "   .====.---.====.   ",
    "   '####'   '####'   ",
]

_BROWS: Dict[str, Tuple[str, str]] = {
    'none':   ("", ""),
    'flat':   ("___", "___"),
    'angry':  ("\\__", "__/"),
    'sad':    ("__/", "\\__"),
    'worried': ("~~~", "~~~"),
}

_MOUTHS: Dict[str, List[str]] = {
    'smile':  ["\\     /", " '---' ", "       "],
    'grin':   ["\\_______/", " \\_____/ ", "         "],
    'laugh':  [".-------.", "\\  ___  /", " '.___.' "],
    'frown':  [" .---. ", "/     \\", "       "],
    'flat':   ["         ", "---------", "         "],
    'oh':     ["  .---.  ", " (     ) ", "  '---'  "],
    'wavy':   ["         ", "~-~-~-~-~", "         "],
    'tongue': ["\\_______/", " '-----' ", "  (___)  "],
    'kiss':   ["   .-.   ", "  ( o )  ", "   '-'   "],
}
_SHADES_MOUTHS = ('smile', 'grin', 'flat')

# --- moods ------------------------------------------------------------------
# Each mood lists what a face with that expression can be made of. 'extras'
# names entries of _EXTRAS; 'color' is a suggestion for the caller.

_MOODS: Dict[str, dict] = {
    'happy':    {'eyes': ['open', 'dot', 'happy'], 'brows': ['none', 'flat'],
                 'mouths': ['smile', 'grin'], 'extras': ['none', 'cheeks', 'sparkles'],
                 'color': ['yellow', 'light_yellow']},
    'laugh':    {'eyes': ['happy'], 'brows': ['none'],
                 'mouths': ['laugh'], 'extras': ['joy', 'cheeks', 'none'],
                 'color': ['yellow', 'light_yellow']},
    'wink':     {'eyes': ['wink'], 'brows': ['none', 'flat'],
                 'mouths': ['smile', 'grin', 'tongue'], 'extras': ['none', 'sparkles'],
                 'color': ['yellow', 'light_yellow']},
    'sad':      {'eyes': ['open', 'dot'], 'brows': ['sad'],
                 'mouths': ['frown'], 'extras': ['tears', 'none'],
                 'color': ['light_blue', 'blue', 'cyan']},
    'angry':    {'eyes': ['dot', 'open'], 'brows': ['angry'],
                 'mouths': ['frown', 'flat'], 'extras': ['steam', 'none'],
                 'color': ['light_red', 'red']},
    'surprised': {'eyes': ['wide'], 'brows': ['flat'],
                  'mouths': ['oh'], 'extras': ['none', 'sparkles'],
                  'color': ['light_yellow', 'yellow']},
    'cool':     {'eyes': ['shades'], 'brows': ['none'],
                 'mouths': ['smile', 'flat', 'grin'], 'extras': ['none', 'sparkles'],
                 'color': ['light_cyan', 'yellow']},
    'love':     {'eyes': ['heart'], 'brows': ['none'],
                 'mouths': ['smile', 'kiss'], 'extras': ['hearts', 'cheeks'],
                 'color': ['light_red', 'light_magenta']},
    'sleepy':   {'eyes': ['sleepy'], 'brows': ['none'],
                 'mouths': ['flat', 'oh'], 'extras': ['zzz'],
                 'color': ['light_blue', 'cyan']},
    'calm':     {'eyes': ['happy', 'sleepy'], 'brows': ['none'],
                 'mouths': ['smile'], 'extras': ['none', 'sparkles'],
                 'color': ['light_cyan', 'light_green']},
    'dizzy':    {'eyes': ['x'], 'brows': ['worried', 'none'],
                'mouths': ['wavy', 'oh'], 'extras': ['none', 'sparkles'],
                'color': ['light_green', 'green']},
    'starstruck': {'eyes': ['star'], 'brows': ['flat', 'none'],
                   'mouths': ['grin', 'laugh'], 'extras': ['sparkles'],
                   'color': ['light_yellow', 'yellow']},
    'silly':    {'eyes': ['open', 'wide'], 'brows': ['flat', 'worried'],
                 'mouths': ['tongue'], 'extras': ['none', 'sparkles'],
                 'color': ['light_green', 'light_magenta']},
}

# The command parser's moods (happy, sad, angry, calm, sleepy) mapped to the
# faces that express them, so "draw a sad emoji" gives a sad face.
MOOD_FACES: Dict[str, List[str]] = {
    'happy': ['happy', 'laugh', 'wink', 'starstruck'],
    'sad': ['sad'],
    'angry': ['angry'],
    'calm': ['calm'],
    'sleepy': ['sleepy'],
}


def _stamp(canvas: List[List[str]], lines: List[str], top: int, left: int) -> None:
    """Draw lines onto the canvas, writing only the visible characters."""
    for dy, line in enumerate(lines):
        for dx, ch in enumerate(line):
            y, x = top + dy, left + dx
            if ch != ' ' and 0 <= y < len(canvas) and 0 <= x < len(canvas[0]):
                canvas[y][x] = ch


def _stamp_centered(canvas: List[List[str]], lines: List[str], top: int, center: int) -> None:
    """Stamp lines so the widest one is centered on a column of the canvas."""
    width = max(len(l) for l in lines)
    _stamp(canvas, lines, top, center - width // 2)


def _extras(canvas: List[List[str]], name: str, off: int) -> None:
    """Add one extra (cheeks, tears, hearts, ...) to the face; off is the head's left column."""
    left_c, right_c = off + _EYE_CENTERS[0], off + _EYE_CENTERS[1]
    if name == 'cheeks':
        _stamp_centered(canvas, ["###"], 6, left_c - 2)
        _stamp_centered(canvas, ["###"], 6, right_c + 2)
    elif name == 'tears':
        _stamp_centered(canvas, ["'"], 6, left_c)
        _stamp_centered(canvas, ["'"], 6, right_c)
    elif name == 'joy':
        _stamp_centered(canvas, ["'-.", "  '"], 6, left_c - 2)
        _stamp_centered(canvas, [".-'", "'  "], 6, right_c + 2)
    elif name == 'steam':
        _stamp(canvas, [" ) )", "( ( "], 0, off - 5)
        _stamp(canvas, ["( ( ", " ) )"], 0, off + _WIDTH + 1)
    elif name == 'hearts':
        for top, side in ((1, 'l'), (4, 'r'), (7, 'l')):
            if random.random() < 0.8:
                col = off - 5 if side == 'l' else off + _WIDTH + 1
                _stamp(canvas, ["<3"], top, col + random.randint(0, 2))
    elif name == 'zzz':
        _stamp(canvas, ["z"], 4, off + _WIDTH + 1)
        _stamp(canvas, ["Z"], 2, off + _WIDTH + 3)
        _stamp(canvas, ["Z"], 0, off + _WIDTH + 5)
    elif name == 'sparkles':
        spots = [(top, col) for top in range(0, 11, 2) for col in
                 (off - 4, off - 2, off + _WIDTH + 1, off + _WIDTH + 3)]
        for top, col in random.sample(spots, random.randint(3, 5)):
            _stamp(canvas, [random.choice(["*", "+", "*", "."])], top, col)


def emoji_face(mood: Optional[str] = None) -> Tuple[List[str], str]:
    """Compose a face for the given mood, or a random one.

    mood is a face mood (see _MOODS) or one of the parser's moods (see
    MOOD_FACES), which picks among the faces that express it. Returns
    (lines, face_mood). Use emoji_color(face_mood) for a color that suits it.
    """
    if mood is None:
        mood = random.choice(list(_MOODS))
    elif mood in MOOD_FACES:
        mood = random.choice(MOOD_FACES[mood])
    if mood not in _MOODS:
        raise ValueError(f"unknown mood {mood!r}; choose from {tuple(_MOODS)}")
    spec = _MOODS[mood]
    eyes = random.choice(spec['eyes'])
    brows = random.choice(spec['brows'])
    mouth = random.choice(spec['mouths'])
    extra = random.choice(spec['extras'])

    off = _MARGIN
    canvas = [[' '] * (_WIDTH + 2 * off) for _ in _HEAD]
    _stamp(canvas, _HEAD, 0, off)

    if eyes == 'shades':
        _stamp(canvas, _SHADES, 4, off)
        mouth = mouth if mouth in _SHADES_MOUTHS else 'smile'
    else:
        left, right = _EYES[eyes]
        _stamp_centered(canvas, left, 4, off + _EYE_CENTERS[0])
        _stamp_centered(canvas, right, 4, off + _EYE_CENTERS[1])
        left_b, right_b = _BROWS[brows]
        if left_b:
            _stamp_centered(canvas, [left_b], 3, off + _EYE_CENTERS[0])
            _stamp_centered(canvas, [right_b], 3, off + _EYE_CENTERS[1])

    _stamp_centered(canvas, _MOUTHS[mouth], 7, off + _WIDTH // 2)
    if extra != 'none':
        _extras(canvas, extra, off)

    rows = [''.join(r).rstrip() for r in canvas]
    indent = min(len(r) - len(r.lstrip()) for r in rows if r.strip())
    return [r[indent:] for r in rows], mood


def emoji_color(mood: str) -> str:
    """A color that suits the mood (yellow for happy faces, red for angry ones)."""
    return random.choice(_MOODS[mood]['color'])
