"""
ASCII Generator - Smart Generator

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
        'thick': lambda: [char * 2 * width] + [char * 2 + ' ' * (width * 2 - 4) + char * 2 for _ in padded_grid] + [char * 2 * width],
        'bold': lambda: [char * width] + [char + ' ' * (width - 2) + char for _ in padded_grid] + [char * width],
        'fancy': lambda: create_fancy_border(padded_grid, char),
        'rounded': lambda: create_rounded_border(padded_grid, char),
        '3d': lambda: create_3d_border(padded_grid, char),
        'shadow': lambda: create_shadow_border(padded_grid, char),
        'double_line': lambda: ['+' + '=' * (width - 2) + '+'] + ['|' + ' ' * (width - 2) + '|' for _ in padded_grid] + ['+' + '=' * (width - 2) + '+'],
    }
    
    if border_style in border_styles:
        return border_styles[border_style]()
    else:
        return padded_grid


def create_fancy_border(grid: List[str], char: str) -> List[str]:
    """Create a fancy decorative border."""
    width = max(len(row) for row in grid)
    border_line = char * width
    
    result = [border_line]
    for row in grid:
        result.append(f"{char} {row.ljust(width - 2)} {char}")
    result.append(border_line)
    
    return result


def create_rounded_border(grid: List[str], char: str) -> List[str]:
    """Create a rounded corner border."""
    width = max(len(row) for row in grid)
    
    # Use Unicode box drawing characters for rounded corners
    h_line = '─' * (width - 2)
    result = [f"╭{h_line}╮"]
    for row in grid:
        result.append(f"│ {row.ljust(width - 2)} │")
    result.append(f"╰{h_line}╯")
    
    return result


def create_3d_border(grid: List[str], char: str) -> List[str]:
    """Create a 3D effect border."""
    width = max(len(row) for row in grid)
    
    result = [char * width]
    for row in grid:
        result.append(f"{char}{' ' * (width - 2)}{char}")
    result.append(char * width)
    
    # Add shadow effect
    shadow_line = ' ' + char * (width - 1)
    for i in range(len(result)):
        if i == len(result) - 1:
            result.append(shadow_line)
        else:
            result[i] = ' ' + result[i]
    
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


def draw_star(size: int = 7, char: str = '*') -> List[str]:
    """Draw a filled 4-pointed star (concave sparkle shape, distinct from a diamond)."""
    size = min(max(size, 3), 12)
    outer_r = size
    inner_r = size * 0.42
    poly = _star_vertices(4, outer_r, inner_r)

    width = size * 4 + 3
    height = size * 2 + 3
    cx, cy = width / 2, height / 2
    supersample = 3

    result = []
    for y in range(height):
        line = []
        for x in range(width):
            hits = 0
            for sy in range(supersample):
                for sx in range(supersample):
                    # x is halved to correct for characters being roughly
                    # twice as tall as they are wide.
                    wx = (x + (sx + 0.5) / supersample - cx) / 2.0
                    wy = y + (sy + 0.5) / supersample - cy
                    if _point_in_polygon(wx, wy, poly):
                        hits += 1
            line.append(char if hits * 2 >= supersample * supersample else ' ')
        result.append(''.join(line).rstrip())

    while result and not result[0].strip():
        result.pop(0)
    while result and not result[-1].strip():
        result.pop()
    return result


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
    """Draw an oval/ellipse shape."""
    result = []
    center_x, center_y = width // 2, height // 2
    
    for y in range(height):
        line = []
        for x in range(width):
            # Ellipse equation
            if ((x - center_x) ** 2 * height ** 2 + (y - center_y) ** 2 * width ** 2) <= (width * height / 2) ** 2:
                line.append(char)
            else:
                line.append(' ')
        result.append(''.join(line))
    
    return result


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
    """Draw a pentagon (triangular roof over a rectangular body)."""
    size = max(size, 3)
    width = 2 * size - 1
    result = []

    for i in range(size):
        stars = 2 * i + 1
        offset = (width - stars) // 2
        result.append(' ' * offset + char * stars)

    body_height = max(2, size // 2)
    for _ in range(body_height):
        result.append(char * width)

    return result


def draw_butterfly(size: int = 8, char: str = '*') -> List[str]:
    """Draw a butterfly shape."""
    result = []
    
    # Upper wings
    for y in range(size):
        spaces = size - y - 1
        stars = 2 * y + 1
        line = ' ' * spaces + char * stars + ' ' * (2 * (size - y)) + char * stars
        result.append(line)
    
    # Body
    result.append(' ' * size + char * 3)
    result.append(' ' * (size + 1) + char)
    
    # Lower wings
    for y in range(size - 1, -1, -1):
        spaces = size - y - 1
        stars = 2 * y + 1
        line = ' ' * spaces + char * stars + ' ' * (2 * (size - y)) + char * stars
        result.append(line)
    
    return result


def draw_flower(size: int = 7, char: str = '@') -> List[str]:
    """Draw a flower shape.

    x is scanned at double resolution and halved before the distance check
    to compensate for terminal characters being roughly twice as tall as
    they are wide - otherwise the ring of petals renders egg-shaped instead
    of round (same correction as draw_circle/draw_star).
    """
    result = []

    # Petals
    for y in range(size * 2 + 1):
        line = []
        for x in range(size * 4 + 1):
            dx = (x - size * 2) / 2
            dy = y - size
            dist = math.sqrt(dx * dx + dy * dy)
            if abs(dist - size) < 1.5:
                line.append(char)
            else:
                line.append(' ')
        result.append(''.join(line))

    return result


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
