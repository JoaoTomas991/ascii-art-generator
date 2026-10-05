"""
Console output setup shared by every entry point.

The generated art is not always pure ASCII: border styles use box-drawing
characters ('bold' uses U+2588, 'rounded' uses U+256D..U+2570), the 'blocks'
brightness ramp in image_art.py uses shade blocks, and random_emoji() can return
kaomoji. On Windows, sys.stdout only uses UTF-8 while it is attached to a
console; as soon as output is redirected to a pipe or a file it falls back to
the locale encoding (cp1252 on a Western install), where those characters do
not exist and printing them raises UnicodeEncodeError. Linux and macOS use
UTF-8 either way, so the crash only ever showed up on Windows - and only when
redirecting, which is exactly what CI and "> art.txt" do.

Reconfiguring to UTF-8 is a no-op when already attached to a Windows console
(it is UTF-8 there) and on Linux/macOS. errors='replace' is a last-resort net
for a terminal that genuinely cannot represent a character: a substituted
glyph beats a traceback in the middle of a drawing.
"""

import sys


def enable_utf8_output() -> None:
    """Make stdout/stderr able to carry the non-ASCII characters art uses."""
    for stream in (sys.stdout, sys.stderr):
        # reconfigure() exists on TextIOWrapper (Python 3.7+), but stdout can
        # be replaced by something else entirely (pytest capture, a custom
        # wrapper), so never assume it is there.
        reconfigure = getattr(stream, 'reconfigure', None)
        if reconfigure is None:
            continue
        try:
            reconfigure(encoding='utf-8', errors='replace')
        except (OSError, ValueError):
            # A detached or already-closed stream; printing will fail later
            # on its own terms, with a clearer error than one from here.
            pass
