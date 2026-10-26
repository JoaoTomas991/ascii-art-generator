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


def _adjust(img, contrast: float, gamma: float, auto_contrast: bool):
    """Apply auto-contrast, a contrast factor and a gamma curve to an RGB image."""
    from PIL import ImageEnhance, ImageOps

    if auto_contrast:
        img = ImageOps.autocontrast(img, cutoff=1)
    if contrast != 1.0:
        img = ImageEnhance.Contrast(img).enhance(contrast)
    if gamma != 1.0:
        # gamma > 1 brightens the midtones, gamma < 1 darkens them.
        table = [round(255 * ((i / 255) ** (1 / gamma))) for i in range(256)]
        img = img.point(table * 3)
    return img


def _levels(brightness: List[List[float]], count: int, dither: bool) -> List[List[int]]:
    """Map a grid of 0..1 brightness values to ramp indexes.

    Without dithering each value is quantized on its own. With dithering the
    quantization error is pushed onto the neighbouring pixels
    (Floyd-Steinberg), so smooth gradients keep their shading instead of
    collapsing into a few flat bands.
    """
    height = len(brightness)
    width = len(brightness[0]) if height else 0
    if not dither:
        return [[min(count - 1, int(v * count)) for v in row] for row in brightness]

    grid = [row[:] for row in brightness]
    out = [[0] * width for _ in range(height)]
    top = count - 1
    for y in range(height):
        for x in range(width):
            old = min(1.0, max(0.0, grid[y][x]))
            level = round(old * top)
            out[y][x] = level
            err = old - level / top if top else 0.0
            if x + 1 < width:
                grid[y][x + 1] += err * 7 / 16
            if y + 1 < height:
                if x > 0:
                    grid[y + 1][x - 1] += err * 3 / 16
                grid[y + 1][x] += err * 5 / 16
                if x + 1 < width:
                    grid[y + 1][x + 1] += err * 1 / 16
    return out


def image_to_ascii(path: str, width: int = 100, ramp: str = 'standard',
                    color: bool = False, invert: bool = False,
                    contrast: float = 1.0, gamma: float = 1.0,
                    auto_contrast: bool = False, dither: bool = False) -> str:
    """Convert an image file to ASCII art using a brightness ramp.

    Args:
        path: path to an image file (any format Pillow can open).
        width: output width in characters; height is derived from the
            image's own aspect ratio.
        ramp: key into ASCII_RAMPS choosing which characters to shade with.
        color: if True, wrap each character in a 24-bit ANSI color code
            sampled from that pixel, instead of plain brightness-only text.
        invert: reverse the ramp (useful for light-background terminals).
        contrast: contrast factor applied before shading (1.0 = unchanged).
        gamma: gamma correction applied before shading (1.0 = unchanged).
        auto_contrast: stretch the histogram so the image uses the full
            dark-to-light range (helps flat or washed-out photos).
        dither: spread quantization error between neighbouring characters
            (Floyd-Steinberg) for smoother shading.

    Raises:
        ImportError: Pillow isn't installed.
        FileNotFoundError: path doesn't exist.
        OSError: path exists but isn't a readable image.
    """
    try:
        from PIL import Image
    except ImportError as exc:
        raise ImportError(
            "Image conversion requires Pillow. From the project folder, "
            "install it with: pip install -e \".[images]\" "
            "(for a uv tool install: uv tool install --editable \".[images]\" --force)"
        ) from exc

    chars = ASCII_RAMPS.get(ramp, ASCII_RAMPS['standard'])
    if invert:
        chars = chars[::-1]

    width = max(10, min(width, 400))
    img = Image.open(path)
    if img.mode in ('RGBA', 'LA', 'P'):
        # Composite transparency onto white instead of letting it turn black.
        img = img.convert('RGBA')
        background = Image.new('RGBA', img.size, (255, 255, 255, 255))
        img = Image.alpha_composite(background, img)
    img = img.convert('RGB')
    orig_w, orig_h = img.size
    height = max(1, round(width * (orig_h / orig_w) * _ASPECT_CORRECTION))
    img = img.resize((width, height), Image.LANCZOS)
    img = _adjust(img, contrast, gamma, auto_contrast)
    pixels = img.load()

    brightness = [
        [(0.299 * r + 0.587 * g + 0.114 * b) / 255
         for r, g, b in (pixels[x, y] for x in range(width))]
        for y in range(height)
    ]
    levels = _levels(brightness, len(chars), dither)

    lines: List[str] = []
    for y in range(height):
        row = []
        for x in range(width):
            ch = chars[levels[y][x]]
            if color:
                r, g, b = pixels[x, y]
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
