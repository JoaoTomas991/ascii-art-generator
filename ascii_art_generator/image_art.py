"""
Image to ASCII Art conversion.

This is the one module in the project with a third-party dependency
(Pillow) - see .claude/skills/generator-core/SKILL.md for why the rest of
the codebase stays standard-library-only and this module is the deliberate
exception. The import is deferred into image_to_ascii() itself so that not
having Pillow installed only breaks image conversion, not the rest of the
CLI.
"""

from typing import List

# Character ramps, ordered lightest -> heaviest. 'standard' is the classic
# 10-level ramp; 'detailed' gives finer gradation for larger renders;
# 'blocks' uses Unicode shade blocks for a bolder, more graphic look.
ASCII_RAMPS = {
    'standard': ' .:-=+*#%@',
    'detailed': " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$",
    'blocks': ' ░▒▓█',
}

# Terminal characters are roughly twice as tall as they are wide, so an
# image resized to (width, height == width * source_aspect) would look
# vertically stretched. Scaling the sampled height down compensates, the
# same correction draw_circle/draw_star apply to shapes.
_ASPECT_CORRECTION = 0.55


def image_to_ascii(path: str, width: int = 100, ramp: str = 'standard',
                    color: bool = False, invert: bool = False) -> str:
    """Convert an image file to ASCII art using a brightness ramp.

    Args:
        path: path to an image file (any format Pillow can open).
        width: output width in characters; height is derived from the
            image's own aspect ratio.
        ramp: key into ASCII_RAMPS choosing which characters to shade with.
        color: if True, wrap each character in a 24-bit ANSI color code
            sampled from that pixel, instead of plain brightness-only text.
        invert: reverse the ramp (useful for light-background terminals).

    Raises:
        ImportError: Pillow isn't installed.
        FileNotFoundError: path doesn't exist.
        OSError: path exists but isn't a readable image.
    """
    try:
        from PIL import Image
    except ImportError as exc:
        raise ImportError(
            "Image conversion requires Pillow. Install it with: "
            "pip install -r requirements.txt"
        ) from exc

    chars = ASCII_RAMPS.get(ramp, ASCII_RAMPS['standard'])
    if invert:
        chars = chars[::-1]

    width = max(10, min(width, 400))
    img = Image.open(path).convert('RGB')
    orig_w, orig_h = img.size
    height = max(1, round(width * (orig_h / orig_w) * _ASPECT_CORRECTION))
    img = img.resize((width, height))
    pixels = img.load()

    lines: List[str] = []
    for y in range(height):
        row = []
        for x in range(width):
            r, g, b = pixels[x, y]
            brightness = (0.299 * r + 0.587 * g + 0.114 * b) / 255
            ch = chars[min(len(chars) - 1, int(brightness * len(chars)))]
            if color:
                row.append(f"\033[38;2;{r};{g};{b}m{ch}")
            else:
                row.append(ch)
        line = ''.join(row)
        if color:
            line += '\033[0m'
        lines.append(line)

    return '\n'.join(lines)


def get_available_ramps() -> List[str]:
    """Get list of available brightness ramps for image_to_ascii."""
    return list(ASCII_RAMPS.keys())
