"""A small dot canvas that prints as Unicode Braille characters.

One Braille character holds a grid of 2 by 4 dots, so a drawing made of dots
has twice the horizontal and four times the vertical detail of one made of
whole characters, and a dot pattern can stand for a shade of grey.

This is the opt-in "Braille" look (`style braille`, `style shaded`); the
classic ASCII drawings stay the default. Braille is Unicode, not ASCII, and
needs a font with the Braille glyphs. Standard library only.
"""

from typing import List

# Bit of each dot inside a Braille character, indexed [row][column].
BRAILLE_BITS = ((0x01, 0x08), (0x02, 0x10), (0x04, 0x20), (0x40, 0x80))
BRAILLE_BLANK = chr(0x2800)

DOTS_X, DOTS_Y = 2, 4      # dots per character, across and down

# Ordered-dither thresholds (a 4x4 Bayer matrix, scaled to 0..1). A dot whose
# shade is above the threshold at its position is lit, which turns a smooth
# shade into an even dot pattern with no random noise.
_BAYER = tuple(
    tuple((value + 0.5) / 16 for value in row)
    for row in ((0, 8, 2, 10), (12, 4, 14, 6), (3, 11, 1, 9), (15, 7, 13, 5))
)


class PixelCanvas:
    """A grid of dots, each holding how much of it is covered (0.0 to 1.0).

    `width` and `height` are in characters; the dot grid is `width * 2` by
    `height * 4`.
    """

    def __init__(self, width: int, height: int):
        self.width = max(0, width)
        self.height = max(0, height)
        self.dots_w = self.width * DOTS_X
        self.dots_h = self.height * DOTS_Y
        self.coverage = [[0.0] * self.dots_w for _ in range(self.dots_h)]

    @classmethod
    def from_art(cls, lines: List[str]) -> 'PixelCanvas':
        """Redraw character art as dots, with its blocky edges smoothed.

        Every drawn character counts as a filled cell. The cells are blended
        between their centres (bilinear interpolation), so a staircase of
        characters becomes a slope of dots and a corner becomes a curve.
        """
        height = len(lines)
        width = max((len(line) for line in lines), default=0)
        canvas = cls(width, height)

        # The cells as 0/1, with a blank cell of margin all round so the
        # blend below never has to test for the edge.
        cells = [[0.0] * (width + 2)]
        for line in lines:
            row = [0.0 if ch.isspace() else 1.0 for ch in line]
            cells.append([0.0] + row + [0.0] * (width - len(row) + 1))
        cells.append([0.0] * (width + 2))

        # Each dot sits between two cell centres: the cell to its left (or
        # above) and how far along it is toward the next one.
        across = [divmod((x + 0.5) / DOTS_X + 0.5, 1) for x in range(canvas.dots_w)]
        for y in range(canvas.dots_h):
            cy, fy = divmod((y + 0.5) / DOTS_Y + 0.5, 1)
            upper, lower = cells[int(cy)], cells[int(cy) + 1]
            row = canvas.coverage[y]
            for x, (cx, fx) in enumerate(across):
                cx = int(cx)
                top = upper[cx] + (upper[cx + 1] - upper[cx]) * fx
                bottom = lower[cx] + (lower[cx + 1] - lower[cx]) * fx
                row[x] = top + (bottom - top) * fy
        return canvas

    def to_braille(self, shaded: bool = False) -> List[str]:
        """The canvas as lines of Braille characters, all `width` long.

        A dot is part of the drawing when at least half of it is covered.
        With `shaded`, the inside is lit from the top left: dense dots there,
        thinning out toward the bottom right, while the rim stays solid so
        the outline remains sharp.
        """
        lines: List[str] = []
        for cy in range(self.height):
            row = []
            for cx in range(self.width):
                code = 0
                for dy in range(DOTS_Y):
                    for dx in range(DOTS_X):
                        x, y = cx * DOTS_X + dx, cy * DOTS_Y + dy
                        if self._lit(x, y, shaded):
                            code |= BRAILLE_BITS[dy][dx]
                row.append(chr(0x2800 + code))
            lines.append(''.join(row))
        return lines

    def _inside(self, x: int, y: int) -> bool:
        return 0 <= x < self.dots_w and 0 <= y < self.dots_h and self.coverage[y][x] >= 0.5

    def _lit(self, x: int, y: int, shaded: bool) -> bool:
        if not self._inside(x, y):
            return False
        if not shaded:
            return True
        # A dot on the rim (one that touches the outside) is always lit.
        if not all(self._inside(x + ox, y + oy) for ox, oy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            return True
        across = x / max(1, self.dots_w - 1)
        down = y / max(1, self.dots_h - 1)
        shade = 1.0 - (0.45 * across + 0.55 * down)       # 1 at the top left, 0 at the bottom right
        return 0.12 + 0.88 * shade > _BAYER[y % 4][x % 4]


def braille_art(lines: List[str], shaded: bool = False) -> List[str]:
    """Character art redrawn in Braille dots, in the same number of lines and columns."""
    return PixelCanvas.from_art(lines).to_braille(shaded)
