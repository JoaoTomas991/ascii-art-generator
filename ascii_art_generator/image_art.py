"""
Image to ASCII Art conversion.

This is the one module in the project with a third-party dependency
(Pillow) - see .claude/skills/generator-core/SKILL.md for why the rest of
the codebase stays standard-library-only and this module is the deliberate
exception. The import is deferred into image_to_ascii() itself so that not
having Pillow installed only breaks image conversion, not the rest of the
CLI.
"""

from typing import List, Optional, Tuple

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
        gamma = max(gamma, 0.05)
        # gamma > 1 brightens the midtones, gamma < 1 darkens them.
        table = [round(255 * ((i / 255) ** (1 / gamma))) for i in range(256)]
        img = img.point(table * 3)
    return img


def _edge_map(img, width: int, height: int) -> List[List[float]]:
    """Return a width x height grid of 0..1 edge strengths for an RGB image.

    Edges are found on a grayscale copy three times the output size and then
    averaged down, so thin outlines (an eye, a nose, a whisker line) survive
    the shrink to character resolution instead of vanishing.
    """
    from PIL import Image, ImageFilter, ImageOps

    big = img.convert('L').resize((width * 3, height * 3), Image.LANCZOS)
    # A median pass flattens fine texture (fur, fabric weave) while keeping
    # real contours, then a blur of about one and a half cells keeps only
    # edges that are larger than a single character.
    big = big.filter(ImageFilter.MedianFilter(5)).filter(ImageFilter.GaussianBlur(4.5))
    big = big.filter(ImageFilter.FIND_EDGES)
    # FIND_EDGES leaves a false bright frame on the image border; trim it
    # off and stretch the rest back to the output size.
    margin = min(6, (big.width - 1) // 2, (big.height - 1) // 2)
    if margin > 0:
        big = big.crop((margin, margin, big.width - margin, big.height - margin))
    small = ImageOps.autocontrast(big.resize((width, height), Image.BOX), cutoff=1)
    px = small.load()
    # Drop weak responses and keep a soft knee, so only clear outlines remain.
    return [[max(0.0, (px[x, y] / 255 - 0.2) / 0.8) ** 1.5 for x in range(width)]
            for y in range(height)]


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


# Bit for each dot of a Braille cell, indexed [row][column] (Unicode order:
# dots 1-3 and 7 are the left column, dots 4-6 and 8 the right).
_BRAILLE_BITS = ((0x01, 0x08), (0x02, 0x10), (0x04, 0x20), (0x40, 0x80))


def _braille_lines(pixels, levels: List[List[int]], width: int, height: int,
                   color: bool, invert: bool) -> str:
    """Pack a 2x4 block of on/off dots into each Braille character.

    Dots are lit where the image is bright (as the ASCII ramp does, for dark
    terminals); `invert` lights the dark ones instead. With `color`, each
    character takes the average color of its 8 source pixels.
    """
    lines: List[str] = []
    for cy in range(height):
        row = []
        for cx in range(width):
            code = 0
            r_sum = g_sum = b_sum = 0
            for dy in range(4):
                for dx in range(2):
                    x, y = cx * 2 + dx, cy * 4 + dy
                    on = levels[y][x] == 1
                    if on != invert:
                        code |= _BRAILLE_BITS[dy][dx]
                    if color:
                        r, g, b = pixels[x, y]
                        r_sum += r
                        g_sum += g
                        b_sum += b
            ch = chr(0x2800 + code)
            if color:
                row.append(f"\033[38;2;{r_sum // 8};{g_sum // 8};{b_sum // 8}m{ch}")
            else:
                row.append(ch)
        line = ''.join(row)
        if color:
            line += '\033[0m'
        lines.append(line)
    return '\n'.join(lines)


def image_to_ascii(path: str, width: int = 100, ramp: str = 'standard',
                    color: bool = False, invert: bool = False,
                    contrast: float = 1.0, gamma: float = 1.0,
                    auto_contrast: bool = False, dither: bool = False,
                    edges: bool = False, braille: bool = False,
                    crop: Optional[Tuple[float, float, float, float]] = None) -> str:
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
        edges: emphasize outlines by mixing an edge map into the shading, so
            features such as eyes and contours stay readable.
        braille: draw with Unicode Braille characters (a 2x4 grid of dots per
            character) instead of the ASCII ramp. This gives about eight
            times the detail, always uses dithering, and needs a font with
            Braille glyphs. `invert` flips which dots are on; `ramp` is ignored.
        crop: (left, top, width, height) of the region to convert, each as a
            percentage (0-100) of the image; the default is the whole image.

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

    if ramp not in ASCII_RAMPS:
        raise ValueError(
            f"Unknown ramp '{ramp}'. Available ramps: {', '.join(ASCII_RAMPS)}"
        )
    chars = ASCII_RAMPS[ramp]
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
    if crop:
        left, top, crop_w, crop_h = crop
        iw, ih = img.size
        box = (
            round(iw * max(0, min(left, 99)) / 100),
            round(ih * max(0, min(top, 99)) / 100),
            round(iw * min(100, max(1, left + crop_w)) / 100),
            round(ih * min(100, max(1, top + crop_h)) / 100),
        )
        # A region that rounds to nothing still keeps one pixel, rather than
        # silently falling back to the whole image.
        box = (min(box[0], iw - 1), min(box[1], ih - 1),
               max(box[2], min(box[0], iw - 1) + 1), max(box[3], min(box[1], ih - 1) + 1))
        img = img.crop(box)
    orig_w, orig_h = img.size
    if braille:
        # One character is a 2x4 block of dots, so sample twice as many
        # columns and four times as many rows as the output has characters.
        # The dots are close to square, so no aspect correction is needed.
        height = max(1, round(width * 2 * (orig_h / orig_w) / 4))
        grid_w, grid_h = width * 2, height * 4
    else:
        height = max(1, round(width * (orig_h / orig_w) * _ASPECT_CORRECTION))
        grid_w, grid_h = width, height
    edge_grid = _edge_map(img, grid_w, grid_h) if edges else None
    img = img.resize((grid_w, grid_h), Image.LANCZOS)
    img = _adjust(img, contrast, gamma, auto_contrast)
    pixels = img.load()

    brightness = [
        [(0.299 * r + 0.587 * g + 0.114 * b) / 255
         for r, g, b in (pixels[x, y] for x in range(grid_w))]
        for y in range(grid_h)
    ]
    if edge_grid:
        # Keep a dimmed copy of the shading and let strong edges push a
        # cell toward the heavy end of the ramp (the lightest cells stay blank).
        brightness = [
            [min(1.0, 0.4 * b + 1.1 * e) for b, e in zip(b_row, e_row)]
            for b_row, e_row in zip(brightness, edge_grid)
        ]
    if braille:
        return _braille_lines(pixels, _levels(brightness, 2, True), width, height,
                              color, invert)
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
