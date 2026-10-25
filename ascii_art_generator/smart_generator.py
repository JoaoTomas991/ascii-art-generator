"""
ASCII Art Generator - Smart Generator

This module provides intelligent ASCII art generation with:
- Automatic style selection
- More fill patterns
- More border styles
- Advanced shapes
- Random interesting combinations
- Context-aware generation
"""

import random
import math
from typing import List, Dict, Optional, Tuple, Callable
from .animal_scenes import animal_scene, scene_color
from .ascii_art import (
    draw_rectangle, draw_circle, draw_heart, draw_diamond,
    draw_triangle, generate_tree, generate_spiral, generate_checkerboard,
    generate_gradient, text_to_ascii, random_emoji,
    get_color_code, create_banner, create_box
)


def _normalize_lines(art) -> List[str]:
    """Normalize a generator's output to a list of lines.

    Several `ascii_art` functions (draw_rectangle, draw_heart, generate_tree,
    generate_spiral, ...) return a single '\\n'-joined string, while the
    smart-generation helpers below always expect a List[str]. Iterating a
    str yields individual characters, so without this normalization the
    fill/border/color steps silently corrupt the art into one character per
    line. Call this right after invoking any shape function.
    """
    if isinstance(art, str):
        return art.split('\n')
    return art


# =============================================================================
# EXTENDED FILL PATTERNS
# =============================================================================

def apply_fill_pattern(width: int, height: int, pattern: str, char: str = '#') -> List[str]:
    """Apply various fill patterns to a shape."""
    patterns = {
        # Basic patterns
        'solid': lambda w, h: [[char for _ in range(w)] for _ in range(h)],
        'empty': lambda w, h: [[char if (i == 0 or i == h-1 or j == 0 or j == w-1) else ' ' for j in range(w)] for i in range(h)],
        'dotted': lambda w, h: [[char if (i + j) % 2 == 0 else ' ' for j in range(w)] for i in range(h)],
        'striped': lambda w, h: [[char if i % 2 == 0 else ' ' for j in range(w)] for i in range(h)],
        'horizontal_stripes': lambda w, h: [[char if i % 2 == 0 else ' ' for j in range(w)] for i in range(h)],
        'vertical_stripes': lambda w, h: [[char if j % 2 == 0 else ' ' for j in range(w)] for i in range(h)],
        
        # Cross patterns
        'cross': lambda w, h: [[char if (i == j or i + j == h - 1) else ' ' for j in range(w)] for i in range(h)],
        'crosshatch': lambda w, h: [[char if (i + j) % 2 == 0 else ' ' for j in range(w)] for i in range(h)],
        'diagonal': lambda w, h: [[char if i == j else ' ' for j in range(w)] for i in range(h)],
        'anti_diagonal': lambda w, h: [[char if (i + j) == h - 1 else ' ' for j in range(w)] for i in range(h)],
        'x_pattern': lambda w, h: [[char if (i == j or i + j == h - 1 or i == h//2 or j == w//2) else ' ' for j in range(w)] for i in range(h)],
        
        # Grid patterns
        'grid': lambda w, h: [[char if (i % 2 == 0 and j % 2 == 0) else ' ' for j in range(w)] for i in range(h)],
        'checkerboard': lambda w, h: [[char if (i + j) % 2 == 0 else ' ' for j in range(w)] for i in range(h)],
        'dense_checkerboard': lambda w, h: [[char if (i // 2 + j // 2) % 2 == 0 else ' ' for j in range(w)] for i in range(h)],
        
        # Random patterns
        'random': lambda w, h: [[char if random.random() > 0.5 else ' ' for j in range(w)] for i in range(h)],
        'sparse_random': lambda w, h: [[char if random.random() > 0.8 else ' ' for j in range(w)] for i in range(h)],
        'dense_random': lambda w, h: [[char if random.random() > 0.2 else ' ' for j in range(w)] for i in range(h)],
        
        # Character-based patterns
        'dots': lambda w, h: [[ '.' if (i + j) % 3 == 0 else ' ' for j in range(w)] for i in range(h)],
        'stars': lambda w, h: [[ '*' if (i + j) % 4 == 0 else ' ' for j in range(w)] for i in range(h)],
        'plus_signs': lambda w, h: [[ '+' if (i + j) % 5 == 0 else ' ' for j in range(w)] for i in range(h)],
        'mixed': lambda w, h: [[random.choice(['#', '@', '*', '.', '+', '-']) if (i + j) % 2 == 0 else ' ' for j in range(w)] for i in range(h)],
        
        # Gradient patterns - a smooth light-to-heavy density ramp, not a
        # binary half-and-half split (see create_directional_gradient).
        'left_gradient': lambda w, h: create_directional_gradient(w, h, 'left'),
        'right_gradient': lambda w, h: create_directional_gradient(w, h, 'right'),
        'top_gradient': lambda w, h: create_directional_gradient(w, h, 'top'),
        'bottom_gradient': lambda w, h: create_directional_gradient(w, h, 'bottom'),
        'center_gradient': lambda w, h: create_directional_gradient(w, h, 'center'),
        'dense_gradient': lambda w, h: create_directional_gradient(w, h, 'left', DENSE_GRADIENT_RAMP),

        # Special patterns
        'spiral_pattern': lambda w, h: create_spiral_pattern(w, h, char),
        'concentric': lambda w, h: create_concentric_pattern(w, h, char),
        'wave': lambda w, h: create_wave_pattern(w, h, char),
        'zigzag': lambda w, h: create_zigzag_pattern(w, h, char),
        'honeycomb': lambda w, h: create_honeycomb_pattern(w, h, char),
    }
    
    if pattern in patterns:
        grid = patterns[pattern](width, height)
        return [''.join(row) for row in grid]
    else:
        # Default to solid (List[str] like the branch above - a list of
        # lists here crashed mask_fill_pattern on unknown pattern names)
        return [char * width for _ in range(height)]


GRADIENT_RAMP = ' .:-=+*#%@'
# Heavy half of the ramp only, so a dense_gradient never leaves blank or
# near-blank cells inside the shape.
DENSE_GRADIENT_RAMP = '=+*#%@'


def _ramp_char(t: float, ramp: str = GRADIENT_RAMP) -> str:
    """Map a 0..1 fraction to a character in the light->heavy density ramp."""
    idx = min(len(ramp) - 1, max(0, int(t * len(ramp))))
    return ramp[idx]


def create_directional_gradient(width: int, height: int, direction: str,
                                ramp: str = GRADIENT_RAMP) -> List[List[str]]:
    """Create a smooth density gradient across the grid (light to heavy).

    Unlike a binary half-and-half split, every column/row gets its own
    shade from GRADIENT_RAMP, so the fill actually looks like a gradient.
    """
    grid = []
    for y in range(height):
        row = []
        for x in range(width):
            if direction == 'left':
                t = x / max(width - 1, 1)
            elif direction == 'right':
                t = 1 - x / max(width - 1, 1)
            elif direction == 'top':
                t = y / max(height - 1, 1)
            elif direction == 'bottom':
                t = 1 - y / max(height - 1, 1)
            else:  # center
                dist = math.hypot(x - width / 2, y - height / 2)
                max_dist = math.hypot(width / 2, height / 2) or 1
                t = 1 - dist / max_dist
            row.append(_ramp_char(t, ramp))
        grid.append(row)
    return grid


def create_spiral_pattern(width: int, height: int, char: str) -> List[List[str]]:
    """Create a spiral pattern."""
    grid = [[' ' for _ in range(width)] for _ in range(height)]
    
    x, y = width // 2, height // 2
    dx, dy = 0, -1
    length = 1
    step = 0
    steps = 0
    
    for i in range(min(width, height) * 2):
        for _ in range(length):
            if 0 <= x < width and 0 <= y < height:
                grid[y][x] = char
            x += dx
            y += dy
            steps += 1
            if steps >= width * height:
                return grid
        
        dx, dy = -dy, dx
        if steps % 2 == 0:
            length += 1
    
    return grid


def create_concentric_pattern(width: int, height: int, char: str) -> List[List[str]]:
    """Create concentric circles/squares pattern."""
    grid = [[' ' for _ in range(width)] for _ in range(height)]
    center_x, center_y = width // 2, height // 2
    
    for r in range(0, max(width, height), 2):
        for y in range(height):
            for x in range(width):
                dist = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
                if abs(dist - r) < 1:
                    grid[y][x] = char
    
    return grid


def create_wave_pattern(width: int, height: int, char: str) -> List[List[str]]:
    """Create a wave pattern."""
    grid = [[' ' for _ in range(width)] for _ in range(height)]
    
    for y in range(height):
        offset = int((height / 2 - y) * width / height)
        for x in range(width):
            if (x + offset) % 10 < 5:
                grid[y][x] = char
    
    return grid


def create_zigzag_pattern(width: int, height: int, char: str) -> List[List[str]]:
    """Create a zigzag pattern."""
    grid = [[' ' for _ in range(width)] for _ in range(height)]
    
    for y in range(height):
        start = 0 if y % 2 == 0 else width // 2
        for x in range(start, min(start + width // 2, width)):
            grid[y][x] = char
    
    return grid


def mask_fill_pattern(art: List[str], fill: str, char: str) -> List[str]:
    """Apply a fill pattern's texture without losing the shape's silhouette.

    apply_fill_pattern only knows a bounding box, not the shape's outline.
    Naively swapping the whole grid for the pattern (as the smart-generation
    methods used to do) replaces e.g. a hexagon with a plain rectangle -
    the shape's own drawing is discarded. Instead, only cells the shape
    actually drew a character on get replaced by the pattern's character at
    that position; cells the shape left blank stay blank.
    """
    if fill == 'solid' or not art:
        return art

    height = len(art)
    width = max(len(row) for row in art)

    if fill == 'empty':
        # The bounding-box pattern would only keep the box edge, leaving stray
        # fragments on non-rectangular shapes; outline the silhouette instead.
        rows = [row.ljust(width) for row in art]

        def filled(y: int, x: int) -> bool:
            return 0 <= y < height and 0 <= x < width and rows[y][x] != ' '

        return [''.join(
            char if filled(y, x) and not all(
                filled(y + dy, x + dx) for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)))
            else ' '
            for x in range(width)
        ).rstrip() for y in range(height)]
    pattern = apply_fill_pattern(width, height, fill, char)

    result = []
    for y, row in enumerate(art):
        row = row.ljust(width)
        pattern_row = pattern[y].ljust(width) if y < len(pattern) else ' ' * width
        result.append(''.join(
            pattern_row[x] if row[x] != ' ' else ' '
            for x in range(width)
        ).rstrip())
    return result


def create_honeycomb_pattern(width: int, height: int, char: str) -> List[List[str]]:
    """Create a honeycomb pattern."""
    grid = [[' ' for _ in range(width)] for _ in range(height)]
    
    for y in range(0, height, 2):
        for x in range(0, width, 3):
            if y < height and x < width:
                grid[y][x] = char
            if y < height and x + 1 < width:
                grid[y][x + 1] = char
            if y + 1 < height and x + 1 < width:
                grid[y + 1][x + 1] = char
    
    return grid


# =============================================================================
# EXTENDED BORDER STYLES
# =============================================================================

def apply_border(grid: List[str], border_style: str, char: str = '#') -> List[str]:
    """Apply various border styles to a grid."""
    if not grid:
        return grid
    
    height = len(grid)
    width = max(len(row) for row in grid)
    
    # Pad all rows to same width
    padded_grid = [row.ljust(width) for row in grid]
    
    border_styles = {
        'none': lambda: padded_grid,
        'simple': lambda: [char * width] + padded_grid + [char * width],
        'double': lambda: ['=' * width] + padded_grid + ['=' * width],
        'dashed': lambda: ['-' * width] + padded_grid + ['-' * width],
        'dotted': lambda: ['.' * width] + padded_grid + ['.' * width],
        'thick': lambda: [char * (width + 4)] + [char * 2 + row + char * 2 for row in padded_grid] + [char * (width + 4)],
        'bold': lambda: [char * (width + 2)] + [char + row + char for row in padded_grid] + [char * (width + 2)],
        'fancy': lambda: create_fancy_border(padded_grid, char),
        'rounded': lambda: create_rounded_border(padded_grid, char),
        '3d': lambda: create_3d_border(padded_grid, char),
        'shadow': lambda: create_shadow_border(padded_grid, char),
        'double_line': lambda: ['+' + '=' * width + '+'] + ['|' + row + '|' for row in padded_grid] + ['+' + '=' * width + '+'],
    }
    
    if border_style in border_styles:
        return border_styles[border_style]()
    else:
        return padded_grid


def create_fancy_border(grid: List[str], char: str) -> List[str]:
    """Create a fancy decorative border."""
    width = max(len(row) for row in grid)
    border_line = char * (width + 4)
    
    result = [border_line]
    for row in grid:
        result.append(f"{char} {row.ljust(width)} {char}")
    result.append(border_line)
    
    return result


def create_rounded_border(grid: List[str], char: str) -> List[str]:
    """Create a rounded corner border."""
    width = max(len(row) for row in grid)
    
    # Use Unicode box drawing characters for rounded corners
    h_line = '─' * (width + 2)
    result = [f"╭{h_line}╮"]
    for row in grid:
        result.append(f"│ {row.ljust(width)} │")
    result.append(f"╰{h_line}╯")
    
    return result


def create_3d_border(grid: List[str], char: str) -> List[str]:
    """Create a 3D effect border."""
    width = max(len(row) for row in grid)
    
    result = [char * (width + 2)]
    for row in grid:
        result.append(f"{char}{row.ljust(width)}{char}")
    result.append(char * (width + 2))
    
    # Add shadow effect: indent the frame one column, then draw the shadow under it
    result = [' ' + line for line in result]
    result.append('  ' + char * (width + 1))
    
    return result


def create_shadow_border(grid: List[str], char: str) -> List[str]:
    """Create a shadow effect border."""
    width = max(len(row) for row in grid)
    
    result = []
    for row in grid:
        result.append(f"  {row.ljust(width)}")
    
    # Add shadow lines
    shadow = ' ' * 2 + char * width
    result.append(shadow)
    result.append(' ' * 3 + char * (width - 1))
    
    return result


# =============================================================================
# ADVANCED SHAPES
# =============================================================================

def _star_vertices(points: int, outer_r: float, inner_r: float) -> List[Tuple[float, float]]:
    """Alternating outer/inner vertices of a regular star polygon, first point straight up."""
    verts = []
    for i in range(points * 2):
        angle = -math.pi / 2 + i * math.pi / points
        r = outer_r if i % 2 == 0 else inner_r
        verts.append((r * math.cos(angle), r * math.sin(angle)))
    return verts


def _point_in_polygon(px: float, py: float, poly: List[Tuple[float, float]]) -> bool:
    """Even-odd ray casting test."""
    inside = False
    x1, y1 = poly[-1]
    for x2, y2 in poly:
        if (y1 > py) != (y2 > py):
            x_at_py = (py - y1) * (x2 - x1) / (y2 - y1) + x1
            if px < x_at_py:
                inside = not inside
        x1, y1 = x2, y2
    return inside


def _rasterize_polygon(poly: List[Tuple[float, float]], char: str, supersample: int = 3) -> List[str]:
    """Rasterize a polygon (in square world units) to a tight block of lines.

    x is stretched 2x on output to correct for characters being roughly twice
    as tall as they are wide. A cell is filled when at least half of its
    supersampled points fall inside the polygon.
    """
    x0 = math.floor(min(p[0] for p in poly) * 2) - 1
    x1 = math.ceil(max(p[0] for p in poly) * 2) + 1
    y0 = math.floor(min(p[1] for p in poly)) - 1
    y1 = math.ceil(max(p[1] for p in poly)) + 1

    result = []
    for y in range(y0, y1):
        line = []
        for x in range(x0, x1):
            hits = 0
            for sy in range(supersample):
                for sx in range(supersample):
                    wx = (x + (sx + 0.5) / supersample) / 2.0
                    wy = y + (sy + 0.5) / supersample
                    if _point_in_polygon(wx, wy, poly):
                        hits += 1
            line.append(char if hits * 2 >= supersample * supersample else ' ')
        result.append(''.join(line).rstrip())

    while result and not result[0].strip():
        result.pop(0)
    while result and not result[-1].strip():
        result.pop()
    indent = min((len(l) - len(l.lstrip()) for l in result if l.strip()), default=0)
    return [l[indent:] for l in result]


def draw_star(size: int = 7, char: str = '*') -> List[str]:
    """Draw a filled 5-pointed star, first point straight up."""
    size = min(max(size, 3), 12)
    return _rasterize_polygon(_star_vertices(5, size, size * 0.4), char)


def draw_hexagon(size: int = 8, char: str = '#') -> List[str]:
    """Draw a flat-top/flat-bottom hexagon (slanted corners, straight sides)."""
    size = max(size, 2)
    slant = max(1, size // 2)
    flat_width = size * 2 + 1
    result = []

    for i in range(slant):
        offset = slant - i
        result.append(' ' * offset + char * (flat_width - 2 * offset))
    for _ in range(size):
        result.append(char * flat_width)
    for i in range(slant):
        offset = i + 1
        result.append(' ' * offset + char * (flat_width - 2 * offset))

    return result


def draw_oval(width: int = 40, height: int = 8, char: str = '#') -> List[str]:
    """Draw an oval/ellipse filling a width x height cell box (sampled at cell centres)."""
    width, height = max(width, 1), max(height, 1)
    rx, ry = width / 2, height / 2
    result = []
    for y in range(height):
        line = []
        for x in range(width):
            dx, dy = (x + 0.5 - rx) / rx, (y + 0.5 - ry) / ry
            line.append(char if dx * dx + dy * dy <= 1 else ' ')
        result.append(''.join(line).rstrip())

    # Very narrow or flat boxes can miss every cell centre on an edge row.
    while result and not result[0].strip():
        result.pop(0)
    while result and not result[-1].strip():
        result.pop()
    indent = min((len(l) - len(l.lstrip()) for l in result if l.strip()), default=0)
    return [l[indent:] for l in result] or [char]


def draw_arrow(direction: str = 'right', size: int = 8, char: str = '#') -> List[str]:
    """Draw a shaft-and-arrowhead arrow pointing right/left/up/down, scaled by size."""
    size = max(size, 2)
    head_h = 2 * size - 1
    mid = size - 1

    lines = []
    for i in range(head_h):
        dist = abs(i - mid)
        head_width = size - dist
        pad = size - head_width
        if dist == 0:
            lines.append(char * size + char * head_width)
        else:
            lines.append(' ' * (size + pad) + char * head_width)

    if direction == 'left':
        return [line[::-1] for line in lines]

    if direction in ('up', 'down'):
        width = max(len(line) for line in lines)
        lines = [line.ljust(width) for line in lines]
        columns = [''.join(line[c] for line in lines) for c in range(width)]
        return columns[::-1] if direction == 'up' else columns

    return lines


def draw_pentagon(size: int = 8, char: str = '#') -> List[str]:
    """Draw a regular pentagon, point straight up."""
    size = max(size, 3)
    radius = size * 0.75
    poly = [(radius * math.cos(-math.pi / 2 + i * 2 * math.pi / 5),
             radius * math.sin(-math.pi / 2 + i * 2 * math.pi / 5)) for i in range(5)]
    return _rasterize_polygon(poly, char)


def _dist_to_segment(px: float, py: float, ax: float, ay: float, bx: float, by: float) -> float:
    """Distance from a point to the segment a-b."""
    dx, dy = bx - ax, by - ay
    t = ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)
    t = max(0.0, min(1.0, t))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def draw_butterfly(size: int = 8, char: str = '*') -> List[str]:
    """Draw a butterfly: rounded upper and lower wings, a slim body and two antennae.

    Each cell is tested in square world units (x halved to correct for the
    terminal's tall characters); the wings are mirrored ellipses, kept apart
    from the body by a thin gap.
    """
    size = max(size, 5)
    s = float(size)
    body_rx, body_ry = max(0.35, 0.09 * s), 0.78 * s
    gap = body_rx + 0.35

    result = []
    for y in range(int(-1.25 * s), int(0.95 * s) + 1):
        line = []
        for x in range(int(-2.2 * s), int(2.2 * s) + 1):
            wx, wy = abs(x + 0.5) / 2.0, y + 0.5
            body = (wx / body_rx) ** 2 + (wy / body_ry) ** 2 <= 1
            upper = ((wx - 0.62 * s) / (0.52 * s)) ** 2 + ((wy + 0.32 * s) / (0.58 * s)) ** 2 <= 1
            lower = ((wx - 0.42 * s) / (0.36 * s)) ** 2 + ((wy - 0.46 * s) / (0.40 * s)) ** 2 <= 1
            wing = (upper or lower) and wx > gap
            feeler = _dist_to_segment(wx, wy, 0.1 * s, -0.75 * s, 0.38 * s, -1.15 * s) < 0.3
            line.append(char if body or wing or feeler else ' ')
        result.append(''.join(line).rstrip())

    while result and not result[0].strip():
        result.pop(0)
    while result and not result[-1].strip():
        result.pop()
    indent = min(len(l) - len(l.lstrip()) for l in result if l.strip())
    return [l[indent:] for l in result]


def draw_flower(size: int = 7, char: str = '@') -> List[str]:
    """Draw a five-petal flower with a hollow ring around its centre, on a stem.

    Each petal is an ellipse pointing outward from the centre, tested in
    square world units (x halved to correct for the terminal's tall
    characters) so the flower is not squashed.
    """
    size = max(size, 4)
    radius = float(size)
    stem = max(2, size // 2)
    center_r, ring_r = 0.2 * radius, 0.34 * radius
    petal_d, petal_a, petal_b = 0.62 * radius, 0.40 * radius, 0.25 * radius

    def in_petal(wx: float, wy: float) -> bool:
        for i in range(5):
            ang = -math.pi / 2 + i * 2 * math.pi / 5
            ux, uy = math.cos(ang), math.sin(ang)
            along = wx * ux + wy * uy - petal_d
            across = -wx * uy + wy * ux
            if (along / petal_a) ** 2 + (across / petal_b) ** 2 <= 1:
                return True
        return False

    result = []
    for y in range(int(-radius) - 1, int(radius) + 2 + stem):
        line = []
        for x in range(-int(radius * 2) - 2, int(radius * 2) + 3):
            wx, wy = (x + 0.5) / 2.0, y + 0.5
            r = math.hypot(wx, wy)
            if r <= center_r:
                line.append(char)
            elif r <= ring_r:
                line.append(' ')
            elif in_petal(wx, wy):
                line.append(char)
            elif radius * 0.55 < wy < radius + stem and abs(x + 0.5) <= 1:
                line.append('|')
            else:
                line.append(' ')
        result.append(''.join(line).rstrip())

    while result and not result[0].strip():
        result.pop(0)
    while result and not result[-1].strip():
        result.pop()
    indent = min(len(l) - len(l.lstrip()) for l in result if l.strip())
    return [l[indent:] for l in result]


# =============================================================================
# SMART GENERATION
# =============================================================================

class SmartGenerator:
    """Intelligent ASCII art generator that creates interesting art automatically."""
    
    # Available shapes
    SHAPES = [
        'rectangle', 'circle', 'triangle', 'heart', 'diamond', 'spiral', 'tree',
        'star', 'hexagon', 'oval', 'arrow', 'pentagon', 'butterfly', 'flower',
    ]
    
    # Available fill patterns
    FILL_PATTERNS = [
        'solid', 'empty', 'dotted', 'striped', 'horizontal_stripes', 'vertical_stripes',
        'cross', 'crosshatch', 'diagonal', 'anti_diagonal', 'x_pattern',
        'grid', 'checkerboard', 'dense_checkerboard', 'random', 'sparse_random',
        'dense_random', 'dots', 'stars', 'plus_signs', 'mixed',
        'left_gradient', 'right_gradient', 'top_gradient', 'bottom_gradient',
        'center_gradient', 'dense_gradient', 'spiral_pattern', 'concentric', 'wave', 'zigzag', 'honeycomb'
    ]
    
    # Available border styles
    BORDER_STYLES = [
        'none', 'simple', 'double', 'dashed', 'dotted', 'thick',
        'bold', 'fancy', 'rounded', '3d', 'shadow', 'double_line'
    ]
    
    # Available fonts
    FONTS = ['small', 'block', 'banner', 'shadow']
    
    # Color schemes
    COLOR_SCHEMES = [
        ('red', None),
        ('green', None),
        ('blue', None),
        ('yellow', None),
        ('cyan', None),
        ('magenta', None),
        ('white', None),
        ('light_red', None),
        ('light_green', None),
        ('light_blue', None),
        (None, None),  # No color
    ]
    
    # Interesting combinations
    INTERESTING_COMBINATIONS = [
        {'shape': 'heart', 'fill': 'crosshatch', 'border': 'rounded', 'color': 'light_red'},
        {'shape': 'diamond', 'fill': 'spiral_pattern', 'border': 'fancy', 'color': 'light_blue'},
        {'shape': 'circle', 'fill': 'concentric', 'border': '3d', 'color': 'light_cyan'},
        {'shape': 'tree', 'fill': 'solid', 'border': 'shadow', 'color': 'light_green'},
        {'shape': 'spiral', 'fill': 'random', 'border': 'none', 'color': 'magenta'},
        {'shape': 'rectangle', 'fill': 'honeycomb', 'border': 'thick', 'color': 'yellow'},
    ]
    
    def __init__(self):
        """Initialize the smart generator."""
        self.shape_functions = {
            'rectangle': draw_rectangle,
            'circle': draw_circle,
            'triangle': draw_triangle,
            'heart': draw_heart,
            'diamond': draw_diamond,
            'spiral': generate_spiral,
            'tree': generate_tree,
            'star': draw_star,
            'hexagon': draw_hexagon,
            'oval': draw_oval,
            'arrow': draw_arrow,
            'pentagon': draw_pentagon,
            'butterfly': draw_butterfly,
            'flower': draw_flower,
        }
    
    def generate_interesting_art(self, style: str = 'random', width: int = 30, height: int = 16) -> List[str]:
        """Generate interesting ASCII art based on style preference."""
        styles = {
            'random': self._generate_random_art,
            'minimal': self._generate_minimal_art,
            'complex': self._generate_complex_art,
            'geometric': self._generate_geometric_art,
            'nature': self._generate_nature_art,
            'abstract': self._generate_abstract_art,
        }
        
        if style in styles:
            return styles[style](width, height)
        else:
            return self._generate_random_art(width, height)
    
    def _generate_random_art(self, width: int = 30, height: int = 16) -> List[str]:
        """Generate completely random interesting art."""
        choice = random.choice(['shape', 'text', 'pattern', 'combination', 'animal'])
        
        if choice == 'shape':
            return self._generate_random_shape(width, height)
        elif choice == 'text':
            return self._generate_random_text_art(width, height)
        elif choice == 'pattern':
            return self._generate_random_pattern(width, height)
        elif choice == 'animal':
            return self.generate_animal_art()
        else:
            return self._generate_combination_art(width, height)
    
    def generate_animal_art(self, animal: Optional[str] = None, big: bool = True,
                            setting: Optional[str] = None) -> List[str]:
        """An animal in a coin, frame or scene, colored to suit the setting."""
        art, setting = animal_scene(animal, big, setting)
        color = scene_color(setting)
        return [self._apply_color(line, color) if line else line for line in art]

    def _generate_minimal_art(self, width: int = 30, height: int = 16) -> List[str]:
        """Generate minimal clean art."""
        shape = random.choice(['rectangle', 'circle', 'triangle'])
        fill = random.choice(['empty', 'solid'])
        border = 'none'
        char = random.choice(['#', '*', '-', '.'])
        color = None
        
        return self._generate_shape(shape, min(width, height) // 2, fill, border, char, color)
    
    def _generate_complex_art(self, width: int = 30, height: int = 16) -> List[str]:
        """Generate complex detailed art."""
        shape = random.choice(['spiral', 'diamond', 'heart', 'tree'])
        fill = random.choice(['crosshatch', 'checkerboard', 'spiral_pattern', 'concentric', 'wave'])
        border = random.choice(['fancy', 'rounded', '3d', 'shadow'])
        char = random.choice(['#', '@', '*', '=', '+', '.'])
        color = random.choice(['light_red', 'light_blue', 'light_green', 'light_cyan'])
        
        return self._generate_shape(shape, min(width, height) // 2, fill, border, char, color)
    
    def _generate_geometric_art(self, width: int = 30, height: int = 16) -> List[str]:
        """Generate geometric art."""
        shape = random.choice(['hexagon', 'pentagon', 'star', 'oval'])
        fill = random.choice(['solid', 'empty', 'dotted', 'grid'])
        border = random.choice(['simple', 'double', 'bold'])
        char = random.choice(['#', '*', '=', '+'])
        color = random.choice(['red', 'blue', 'green', 'cyan'])
        
        return self._generate_advanced_shape(shape, min(width, height) // 2, fill, border, char, color)
    
    def _generate_nature_art(self, width: int = 30, height: int = 16) -> List[str]:
        """Generate nature-inspired art."""
        if random.random() < 0.4:
            return self.generate_animal_art()
        shape = random.choice(['tree', 'butterfly', 'flower'])
        fill = random.choice(['solid', 'dotted', 'sparse_random'])
        border = 'none'
        char = random.choice(['*', '@', '#'])
        color = random.choice(['light_green', 'yellow', 'magenta'])
        
        return self._generate_advanced_shape(shape, min(width, height) // 3, fill, border, char, color)
    
    def _generate_abstract_art(self, width: int = 30, height: int = 16) -> List[str]:
        """Generate abstract art."""
        pattern = random.choice(['random', 'sparse_random', 'dense_random', 'mixed', 'honeycomb', 'wave', 'zigzag'])
        char = random.choice(['#', '@', '*', '.', '+', '-', '='])
        color = random.choice([None, 'red', 'blue', 'green', 'cyan', 'magenta'])
        
        return apply_fill_pattern(width, height, pattern, char)
    
    def _generate_random_shape(self, width: int = 30, height: int = 16) -> List[str]:
        """Generate a random shape with interesting settings."""
        # Pick an interesting combination
        if random.random() < 0.3:
            combo = random.choice(self.INTERESTING_COMBINATIONS)
            shape = combo['shape']
            fill = combo['fill']
            border = combo['border']
            color = combo['color']
        else:
            shape = random.choice(self.SHAPES)
            fill = random.choice(self.FILL_PATTERNS)
            border = random.choice(self.BORDER_STYLES)
            color = random.choice([c[0] for c in self.COLOR_SCHEMES])
        
        char = random.choice(['#', '*', '@', '=', '+', '.', '-'])
        
        # Adjust size based on shape
        if shape in ['tree', 'spiral']:
            size = min(width, height) // 2
        else:
            size = min(width, height) // 3
        
        result = self._generate_shape(shape, size, fill, border, char, color)
        return result
    
    def _generate_advanced_shape(self, shape: str, size: int, fill: str, border: str, char: str, color: str) -> List[str]:
        """Generate advanced shapes with patterns."""
        if shape in self.shape_functions:
            func = self.shape_functions[shape]
            
            # Handle different parameters
            if shape == 'rectangle':
                art = func(size * 2, size, char, True)
            elif shape == 'triangle':
                art = func(size, char)
            elif shape == 'circle':
                art = func(size, char)
            elif shape == 'heart':
                art = func(size, char)
            elif shape == 'diamond':
                art = func(size, char)
            elif shape == 'spiral':
                art = func(size * 2, char)
            elif shape == 'tree':
                art = func(size, char)
            elif shape == 'star':
                art = func(size, char)
            elif shape == 'hexagon':
                art = func(size, char)
            elif shape == 'oval':
                art = func(size * 2, size, char)
            elif shape == 'arrow':
                art = func('right', size, char)
            elif shape == 'pentagon':
                art = func(size, char)
            elif shape == 'butterfly':
                art = func(size, char)
            elif shape == 'flower':
                art = func(size, char)
            else:
                art = [f"Unknown shape: {shape}"]

            art = _normalize_lines(art)

            # Apply fill pattern, masked to the shape's own silhouette
            art = mask_fill_pattern(art, fill, char)

            # Apply border
            if border != 'none':
                art = apply_border(art, border, char)

            # Apply color
            if color:
                art = [self._apply_color(line, color) for line in art]

            return art
        else:
            return [f"Unknown shape: {shape}"]

    def _generate_shape(self, shape: str, size: int, fill: str, border: str, char: str, color: str) -> List[str]:
        """Generate a shape with the specified parameters."""
        if shape in self.shape_functions:
            func = self.shape_functions[shape]

            # Handle different parameters
            if shape == 'rectangle':
                art = func(size * 2, size, char, fill != 'empty')
            elif shape == 'triangle':
                art = func(size, char)
            elif shape == 'circle':
                art = func(size, char)
            elif shape == 'heart':
                art = func(size, char)
            elif shape == 'diamond':
                art = func(size, char)
            elif shape == 'spiral':
                art = func(size * 2, char)
            elif shape == 'tree':
                art = func(size, char)
            elif shape == 'arrow':
                art = func('right', size, char)
            elif shape == 'oval':
                art = func(size * 2, size, char)
            else:
                art = func(size, char) if shape in ['star', 'hexagon', 'pentagon', 'butterfly', 'flower'] else [f"Unknown: {shape}"]

            art = _normalize_lines(art)

            # Apply fill pattern, masked to the shape's own silhouette
            art = mask_fill_pattern(art, fill, char)

            # Apply border
            if border != 'none':
                art = apply_border(art, border, char)
            
            # Apply color
            if color:
                art = [self._apply_color(line, color) for line in art]
            
            return art
        else:
            return [f"Unknown shape: {shape}"]
    
    def _generate_random_text_art(self, width: int = 30, height: int = 16) -> List[str]:
        """Generate random text art."""
        words = ['HELLO', 'WORLD', 'ART', 'ASCII', 'COOL', 'MISTRAL', 'PYTHON', 'LOVE']
        text = random.choice(words)
        font = random.choice(self.FONTS)
        color = random.choice([None, 'red', 'blue', 'green', 'cyan', 'magenta', 'yellow'])
        
        art = _normalize_lines(text_to_ascii(text, font))
        if color:
            art = [self._apply_color(line, color) for line in art]

        return art

    def _generate_random_pattern(self, width: int = 30, height: int = 16) -> List[str]:
        """Generate random pattern."""
        pattern = random.choice(['checkerboard', 'gradient', 'spiral'])

        if pattern == 'checkerboard':
            art = generate_checkerboard(min(width, height))
        elif pattern == 'gradient':
            art = generate_gradient(width, height)
        elif pattern == 'spiral':
            art = generate_spiral(min(width, height), '#')
        else:
            art = apply_fill_pattern(width, height, pattern)

        art = _normalize_lines(art)
        color = random.choice([None, 'red', 'blue', 'green', 'cyan'])
        if color:
            art = [self._apply_color(line, color) for line in art]
        
        return art
    
    def _generate_combination_art(self, width: int = 30, height: int = 16) -> List[str]:
        """Generate combination of multiple elements."""
        elements = []
        
        # Add 2-3 elements
        for _ in range(random.randint(2, 3)):
            choice = random.choice(['shape', 'text'])
            
            if choice == 'shape':
                shape = random.choice(['heart', 'diamond', 'star', 'hexagon'])
                size = min(width // 3, height // 3)
                fill = random.choice(['solid', 'empty', 'dotted'])
                char = random.choice(['#', '*', '@'])
                color = random.choice([None, 'red', 'blue', 'green'])
                
                if shape == 'rectangle':
                    art = draw_rectangle(size * 2, size, char, fill == 'solid')
                elif shape == 'circle':
                    art = draw_circle(size, char)
                elif shape == 'heart':
                    art = draw_heart(size, char)
                elif shape == 'diamond':
                    art = draw_diamond(size, char)
                elif shape == 'star':
                    art = draw_star(size, char)
                elif shape == 'hexagon':
                    art = draw_hexagon(size, char)
                else:
                    art = [f"Unknown: {shape}"]

                art = _normalize_lines(art)
                if color:
                    art = [self._apply_color(line, color) for line in art]

                elements.append(art)
            else:
                text = random.choice(['HI', 'OK', 'YES', 'NO', 'A', 'B'])
                font = random.choice(['small', 'block'])
                color = random.choice([None, 'red', 'blue'])

                art = _normalize_lines(text_to_ascii(text, font))
                if color:
                    art = [self._apply_color(line, color) for line in art]
                
                elements.append(art)
        
        # Combine elements
        return self._combine_elements(elements)
    
    def _combine_elements(self, elements: List[List[str]]) -> List[str]:
        """Combine multiple elements into a single art piece."""
        if not elements:
            return []
        
        # Simple vertical combination
        result = []
        for i, element in enumerate(elements):
            if i > 0:
                result.append('')  # Add spacing
            result.extend(element)
        
        return result
    
    def generate_from_command(self, command: str) -> List[str]:
        """Generate art from a natural language command with smart defaults."""
        command_lower = command.lower().strip()
        
        # Check for smart commands
        if any(word in command_lower for word in ['surprise', 'surprise me', 'random art', 'interesting', 'amazing']):
            return self.generate_interesting_art()
        
        if any(word in command_lower for word in ['minimal', 'simple', 'clean']):
            return self.generate_interesting_art('minimal')
        
        if any(word in command_lower for word in ['complex', 'detailed', 'elaborate']):
            return self.generate_interesting_art('complex')
        
        if any(word in command_lower for word in ['geometric', 'geometry']):
            return self.generate_interesting_art('geometric')
        
        if any(word in command_lower for word in ['nature', 'tree', 'flower', 'butterfly']):
            return self.generate_interesting_art('nature')
        
        if any(word in command_lower for word in ['abstract', 'pattern', 'design']):
            return self.generate_interesting_art('abstract')
        
        # Default to random
        return self.generate_interesting_art()
    
    def _apply_color(self, text: str, color: str) -> str:
        """Apply ANSI color to text."""
        colors = {
            'black': '\033[30m',
            'red': '\033[31m',
            'green': '\033[32m',
            'yellow': '\033[33m',
            'blue': '\033[34m',
            'magenta': '\033[35m',
            'cyan': '\033[36m',
            'white': '\033[37m',
            'light_black': '\033[90m',
            'light_red': '\033[91m',
            'light_green': '\033[92m',
            'light_yellow': '\033[93m',
            'light_blue': '\033[94m',
            'light_magenta': '\033[95m',
            'light_cyan': '\033[96m',
            'light_white': '\033[97m',
            'reset': '\033[0m',
        }
        
        if color in colors:
            return f"{colors[color]}{text}{colors['reset']}"
        return text


# Global smart generator instance
smart_gen = SmartGenerator()


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_available_fill_patterns() -> List[str]:
    """Get list of available fill patterns."""
    return SmartGenerator.FILL_PATTERNS


def get_available_border_styles() -> List[str]:
    """Get list of available border styles."""
    return SmartGenerator.BORDER_STYLES


def get_available_shapes() -> List[str]:
    """Get list of available shapes."""
    return list(SmartGenerator().shape_functions.keys())
