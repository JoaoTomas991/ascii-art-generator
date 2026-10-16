"""
Animated startup banner.

Standard library only: the effect is plain ANSI escape codes plus short
sleeps. It degrades to a static banner whenever the output is not an
interactive terminal, the terminal is "dumb", or the user turned it off
(``--no-animation`` or ``ASCII_GENERATOR_NO_ANIMATION=1``).
"""

import os
import shutil
import sys
import threading
import time
from typing import List, Optional, Tuple

from .ascii_art import _figlet_to_ascii, text_to_ascii

TITLE = "ASCII"
TITLE_FONT = "solid"    # pyfiglet's heavy-stroke font; the built-in "block" font stands in without pyfiglet
RULE = "━"
SUBTITLE = "G E N E R A T O R"
WIDTH = 66

# 256-colour ramp, red -> yellow -> green -> cyan -> blue -> magenta.
_GRADIENT = [196, 202, 208, 214, 220, 226, 190, 154, 118, 82, 46, 48,
             51, 45, 39, 33, 27, 63, 99, 135, 171, 207]

_RESET = '\033[0m'
_HIDE_CURSOR = '\033[?25l'
_SHOW_CURSOR = '\033[?25h'


def _is_tty() -> bool:
    """isatty() that never raises (closed, detached or exotic streams)."""
    try:
        return bool(sys.stdout.isatty())
    except (AttributeError, ValueError, OSError):
        return False


def animation_enabled() -> bool:
    """True when it is safe and wanted to play the animated intro."""
    if os.environ.get('ASCII_GENERATOR_NO_ANIMATION'):
        return False
    if os.environ.get('TERM') == 'dumb':
        return False
    return _is_tty()


def title_lines() -> List[str]:
    art = _figlet_to_ascii(TITLE, TITLE_FONT) or text_to_ascii(TITLE, 'block')
    lines = art.split('\n')
    while lines and not lines[-1].strip():
        lines.pop()
    # Terminal cells are about twice as tall as wide, so stretch the letters
    # horizontally (every column doubled) when there is room for it.
    if max(len(line) for line in lines) * 2 <= WIDTH:
        lines = [''.join(ch * 2 for ch in line) for line in lines]
    pad = max(0, (WIDTH - max(len(line) for line in lines)) // 2)
    return [' ' * pad + line for line in lines]


def banner_lines() -> Tuple[List[str], List[str]]:
    """The banner as plain text: (logo lines, [rule, subtitle, rule])."""
    rule = RULE * WIDTH
    return title_lines(), [rule, f'{SUBTITLE:^{WIDTH}}', rule]


def _paint(line: str, shift: int, reveal: int, color: bool) -> str:
    """Colour one title line: columns up to `reveal` are visible, the rest blank."""
    out = []
    for col, ch in enumerate(line):
        if col > reveal or ch == ' ':
            out.append(' ')
        elif color:
            idx = (col // 2 + shift) % len(_GRADIENT)
            tint = 231 if col == reveal else _GRADIENT[idx]   # white leading edge
            out.append(f'\033[1;38;5;{tint}m{ch}')
        else:
            out.append(ch)
    return ''.join(out) + (_RESET if color else '')


def _bar(width: int, color: bool) -> str:
    text = (RULE * width).center(WIDTH)
    return f'\033[1;95m{text}{_RESET}' if color else text


def show_intro(animate: bool = True) -> None:
    """Print the startup banner, animated when the terminal allows it.

    Purely cosmetic, so a stream that cannot take it (closed, no flush, ...)
    skips the banner instead of stopping the program.
    """
    try:
        _render_intro(animate)
    except (ValueError, OSError, AttributeError):
        pass


def _render_intro(animate: bool) -> None:
    animate = animate and animation_enabled()
    color = animate or _is_tty()
    lines = title_lines()
    full = max(len(line) for line in lines)

    print()
    if not animate:
        for line in lines:
            print(_paint(line, 0, full, color))
        print(_bar(WIDTH, color))
        print(f'\033[1;95m{SUBTITLE:^{WIDTH}}{_RESET}' if color else f'{SUBTITLE:^{WIDTH}}')
        print(_bar(WIDTH, color))
        print()
        return

    out = sys.stdout
    try:
        out.write(_HIDE_CURSOR)
        # 1. Wipe the title in from the left with a shifting rainbow.
        for step in range(0, full + 1, 2):
            out.write('\n'.join(_paint(line, step // 2, step, True) for line in lines) + '\n')
            out.write(f'\033[{len(lines)}A')
            out.flush()
            time.sleep(0.015)
        # 2. Settle on the static gradient.
        out.write('\n'.join(_paint(line, 0, full, True) for line in lines) + '\n')
        # 3. Grow the rule outward from the centre.
        for width in list(range(2, WIDTH, 4)) + [WIDTH]:
            out.write('\r' + _bar(width, True))
            out.flush()
            time.sleep(0.008)
        out.write('\n')
        # 4. Type the subtitle, then close with the rule.
        typed = ''
        for ch in SUBTITLE:
            typed += ch
            out.write('\r' + f'\033[1;95m{typed:^{WIDTH}}{_RESET}')
            out.flush()
            time.sleep(0.03)
        out.write('\n' + _bar(WIDTH, True) + '\n\n')
    except KeyboardInterrupt:
        # Skip the rest of the effect on Ctrl+C, and leave the terminal tidy.
        out.write('\n' * len(lines))
    finally:
        out.write(_RESET + _SHOW_CURSOR)
        out.flush()


def rainbow(text: str, shift: int) -> str:
    """Colour `text` with the gradient, rotated by `shift` (one step per frame)."""
    out = []
    for col, ch in enumerate(text):
        if ch == ' ':
            out.append(' ')
        else:
            out.append(f'\033[1;38;5;{_GRADIENT[(col // 2 + shift) % len(_GRADIENT)]}m{ch}')
    return ''.join(out) + _RESET


class LiveLines:
    """Keep already-printed lines animating while the program waits on input().

    input() blocks, so a background thread redraws each target line in place:
    save the cursor, jump up `offset` lines, rewrite the line, restore the
    cursor (so whatever the user is typing is untouched). `offset` is how many
    lines above the cursor the target sits. Targets that would be off screen
    are skipped, and the whole thing is a no-op when the animation is disabled.

        with LiveLines([(1, '=' * 60)]):
            answer = input('> ')

    Known limit: if the user types a line longer than the terminal is wide,
    it wraps onto a second row and the offsets are one too small until Enter.
    """

    def __init__(self, targets: List[Tuple[int, str]], interval: float = 0.12,
                 min_cols: int = 0):
        size = shutil.get_terminal_size((80, 24))
        # Offsets count printed lines, so they only match screen rows while no
        # line wraps. In a terminal narrower than the widest line, do nothing.
        if size.columns < max([min_cols] + [len(text) for _, text in targets]):
            targets = []
        self.targets = [(off, text) for off, text in targets if 0 < off < size.lines]
        self.interval = interval
        self._stop = threading.Event()
        self._thread: Optional[threading.Thread] = None

    def _loop(self) -> None:
        frame = 0
        while not self._stop.wait(self.interval):
            frame += 1
            parts = [f'\0337\033[{off}A\r{rainbow(text, frame + off)}\0338'
                     for off, text in self.targets]
            try:
                sys.stdout.write(''.join(parts))
                sys.stdout.flush()
            except (ValueError, OSError):
                return

    def __enter__(self) -> 'LiveLines':
        if self.targets and animation_enabled():
            self._thread = threading.Thread(target=self._loop, daemon=True)
            self._thread.start()
        return self

    def __exit__(self, *exc) -> None:
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=1)
