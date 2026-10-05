"""
Command Line Interface for ASCII Generator
"""

import sys
import time
import re
from typing import Callable, Dict, Any, Optional, Tuple, List

from .ascii_art import (
    text_to_ascii, draw_rectangle, draw_triangle, draw_circle,
    draw_heart, draw_diamond, generate_gradient, generate_checkerboard,
    generate_spiral, generate_tree, random_abstract,
    random_animal, random_emoji, create_banner, create_box,
    get_available_fonts, spinner_animation, progress_bar,
    get_color_code, get_border_chars, get_fill_style_pattern,
    get_animal_art, KNOWN_ANIMAL_WORDS
)
from .smart_generator import (
    smart_gen, apply_fill_pattern, apply_border, mask_fill_pattern,
    draw_star, draw_hexagon, draw_oval, draw_arrow, draw_pentagon,
    draw_butterfly, draw_flower, get_available_fill_patterns,
    get_available_border_styles, get_available_shapes
)
from .image_art import image_to_ascii
from .learned_words import load_learned_moods, save_learned_mood
from .console import enable_utf8_output


def setup_console() -> None:
    """Make Windows consoles render ANSI colors and Unicode output (no-op elsewhere).

    Legacy Windows consoles (cmd.exe, older PowerShell hosts) print raw
    escape codes unless virtual terminal processing is switched on, and
    redirected output defaults to the ANSI code page, which can't encode
    the Unicode emojis/box characters this generator prints.
    """
    if sys.platform != 'win32':
        return
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding='utf-8')
        except (AttributeError, ValueError):
            pass
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        enable_virtual_terminal_processing = 0x0004
        for std_handle in (-11, -12):  # STD_OUTPUT_HANDLE, STD_ERROR_HANDLE
            handle = kernel32.GetStdHandle(std_handle)
            mode = ctypes.c_uint32()
            if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
                kernel32.SetConsoleMode(handle, mode.value | enable_virtual_terminal_processing)
    except (AttributeError, OSError):
        pass


class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Cycle used by the 'rainbow'/'multicolor' color, one shade per line of art.
RAINBOW_COLORS = ['red', 'yellow', 'green', 'cyan', 'blue', 'magenta']


class Menu:
    """Interactive menu system."""
    
    def __init__(self, title: str = "ASCII Generator"):
        self.title = title
        self.items: Dict[str, Dict[str, Any]] = {}
        self.exit_option = ('q', 'Quit')
    
    def add_item(self, key: str, label: str, action: Callable,
                 description: str = "", category: str = "Main") -> None:
        self.items[key] = {
            'key': key, 'label': label, 'action': action,
            'description': description, 'category': category
        }
    
    def display(self) -> None:
        """Display the menu."""
        print(f"\n{Colors.HEADER}{'=' * 60}{Colors.ENDC}")
        print(f"{Colors.HEADER}{self.title:^60}{Colors.ENDC}")
        print(f"{Colors.HEADER}{'=' * 60}{Colors.ENDC}")
        
        categories = {}
        for key, item in sorted(self.items.items()):
            category = item['category']
            if category not in categories:
                categories[category] = []
            categories[category].append((key, item))
        
        for category, items in categories.items():
            if category != "Main":
                print(f"\n{Colors.OKBLUE}{category}{Colors.ENDC}")
                print("-" * len(category))
            
            for key, item in items:
                label = item['label']
                desc = item['description']
                if desc:
                    print(f"  {Colors.OKGREEN}[{key}]{Colors.ENDC} {label:20} - {desc}")
                else:
                    print(f"  {Colors.OKGREEN}[{key}]{Colors.ENDC} {label}")
        
        print(f"\n{Colors.WARNING}[{self.exit_option[0]}]{Colors.ENDC} {self.exit_option[1]}")
        print()
    
    def run(self) -> None:
        """Run the menu loop."""
        while True:
            self.display()
            choice = input(f"{Colors.BOLD}Enter your choice: {Colors.ENDC}").strip()
            
            if choice.lower() == self.exit_option[0].lower():
                print(f"\n{Colors.OKGREEN}Goodbye!{Colors.ENDC}")
                break
            
            if choice in self.items:
                try:
                    self.items[choice]['action']()
                    input(f"\n{Colors.WARNING}Press Enter to continue...{Colors.ENDC}")
                except Exception as e:
                    print(f"{Colors.FAIL}Error: {e}{Colors.ENDC}")
                    time.sleep(2)
            else:
                print(f"{Colors.FAIL}Invalid choice.{Colors.ENDC}")
                time.sleep(1)


class ENCommandParser:
    """Parser for English natural language commands."""
    
    # Action verbs
    ACTION_VERBS = {
        'draw', 'drawing', 'drew',
        'make', 'makes', 'made', 'create', 'creates', 'created', 'build', 'builds', 'built',
        'write', 'writes', 'wrote', 'type', 'types', 'typed', 'print', 'prints', 'printed',
        'show', 'shows', 'showed', 'display', 'displays', 'displayed',
        'generate', 'generates', 'generated', 'produce', 'produces', 'produced',
        'convert', 'converts', 'converted', 'transform', 'transforms', 'transformed'
    }
    
    # Synonyms for shapes
    SHAPE_SYNONYMS = {
        # Basic shapes
        'rectangle': ['rectangle', 'rect', 'square', 'box'],
        'triangle': ['triangle', 'tri', 'pyramid'],
        'circle': ['circle', 'circ', 'ball', 'wheel'],
        'heart': ['heart'],
        'diamond': ['diamond', 'rhombus'],
        'tree': ['tree', 'christmas', 'pine'],
        'star': ['star'],
        'hexagon': ['hexagon', 'hex'],
        'oval': ['oval', 'ellipse'],
        'arrow': ['arrow'],
        'pentagon': ['pentagon'],
        'butterfly': ['butterfly'],
        'flower': ['flower'],
        'spiral': ['spiral', 'snail', 'volute'],
        # Patterns
        'gradient': ['gradient', 'degrade'],
        'checkerboard': ['checkerboard', 'chessboard'],
        'random': ['random'],
        # Random
        'emoji': ['emoji', 'emoticon'],
        # 'animal'/'creature' pick a fully random animal; every other word
        # here names one specific animal and is recognized even when it has
        # no bespoke drawing of its own - see get_animal_art in ascii_art.py
        # for the fallback that picks a plausible substitute in that case.
        'animal': ['animal', 'creature'] + KNOWN_ANIMAL_WORDS,
        # Text
        'text': ['text', 'word', 'phrase', 'letter', 'name'],
        'banner': ['banner'],
        'box': ['box'],
        # Smart commands
        'smart': ['smart', 'surprise', 'surprise me', 'random art', 'interesting', 'amazing'],
        'minimal': ['minimal', 'simple', 'clean'],
        'complex': ['complex', 'detailed', 'elaborate'],
        'geometric': ['geometric', 'geometry'],
        'nature': ['nature'],
        'abstract': ['abstract', 'art', 'painting', 'pattern', 'design'],
    }
    
    # Direction synonyms for triangle
    DIRECTION_SYNONYMS = {
        'up': ['up', 'upward'],
        'down': ['down', 'downward'],
        'left': ['left'],
        'right': ['right'],
    }
    
    # Special parameters
    SPECIAL_PARAMS = {
        'filled': ['filled', 'full', 'solid', 'yes'],
        'empty': ['empty', 'hollow', 'no'],
    }
    
    # Combination words for compound commands
    COMBINATION_WORDS = {
        'and', 'with', 'also', 'plus', 'then',
        'comma'
    }
    
    # Size adjectives that ask for the bigger animal drawings (ANIMALS_BIG)
    BIG_WORDS = {'big', 'large', 'huge', 'giant'}

    # Font synonyms
    FONT_SYNONYMS = {
        'small': ['small', 'tiny'],
        'block': ['block'],
        'banner': ['banner'],
        'shadow': ['shadow']
    }
    
    # Color synonyms
    COLOR_SYNONYMS = {
        'red': ['red', 'crimson', 'ruby'],
        'green': ['green', 'emerald'],
        'blue': ['blue', 'azure', 'cobalt'],
        'yellow': ['yellow', 'gold', 'amber'],
        'cyan': ['cyan', 'turquoise'],
        'magenta': ['magenta', 'purple', 'violet'],
        'white': ['white'],
        'black': ['black'],
        'light_red': ['light_red', 'lightred', 'pink'],
        'light_green': ['light_green', 'lightgreen'],
        'light_blue': ['light_blue', 'lightblue'],
        'light_yellow': ['light_yellow', 'lightyellow'],
        'light_cyan': ['light_cyan', 'lightcyan'],
        'light_magenta': ['light_magenta', 'lightmagenta'],
        'rainbow': ['rainbow', 'multicolor', 'multicolour'],
    }

    # Mood synonyms (built-in). Teachable via the "teach <word> as <mood>"
    # command in intelligent mode; learned synonyms persist across sessions
    # (see learned_words.py).
    MOOD_SYNONYMS = {
        'happy': ['happy', 'joyful', 'cheerful'],
        'sad': ['sad', 'unhappy', 'gloomy'],
        'angry': ['angry', 'mad', 'furious'],
        'calm': ['calm', 'peaceful', 'relaxed'],
        'sleepy': ['sleepy', 'tired', 'drowsy'],
    }

    # Default visual effect for each mood, applied only when the user
    # hasn't already specified that parameter explicitly.
    MOOD_EFFECTS = {
        'happy': {'color': 'yellow'},
        'sad': {'color': 'blue'},
        'angry': {'color': 'red'},
        'calm': {'color': 'green'},
        'sleepy': {'color': 'cyan'},
    }

    # Fill pattern synonyms
    FILL_PATTERN_SYNONYMS = {
        'solid': ['solid', 'filled', 'full'],
        'empty': ['empty', 'hollow'],
        'dotted': ['dotted', 'dots'],
        'striped': ['striped', 'stripes'],
        'horizontal_stripes': ['horizontal_stripes', 'horizontal', 'h_stripes'],
        'vertical_stripes': ['vertical_stripes', 'vertical', 'v_stripes'],
        'crosshatch': ['crosshatch', 'hatched'],
        'cross': ['cross'],
        'diagonal': ['diagonal'],
        'anti_diagonal': ['anti_diagonal', 'anti-diagonal'],
        'x_pattern': ['x_pattern', 'x-pattern', 'x'],
        'grid': ['grid'],
        'checkerboard': ['checkerboard', 'chessboard'],
        'dense_checkerboard': ['dense_checkerboard', 'dense-checkerboard'],
        'random': ['random'],
        'sparse_random': ['sparse_random', 'sparse-random'],
        'dense_random': ['dense_random', 'dense-random'],
        'dots': ['dots'],
        'stars': ['stars'],
        'plus_signs': ['plus_signs', 'plus-signs', 'pluses'],
        'mixed': ['mixed'],
        'left_gradient': ['left_gradient', 'left-gradient'],
        'right_gradient': ['right_gradient', 'right-gradient'],
        'top_gradient': ['top_gradient', 'top-gradient'],
        'bottom_gradient': ['bottom_gradient', 'bottom-gradient'],
        'center_gradient': ['center_gradient', 'center-gradient'],
        'spiral_pattern': ['spiral_pattern', 'spiral-pattern'],
        'concentric': ['concentric'],
        'wave': ['wave'],
        'zigzag': ['zigzag'],
        'honeycomb': ['honeycomb'],
        'plus': ['plus', 'cross'],
        'gradient': ['gradient'],
    }
    
    # Border style synonyms
    BORDER_STYLE_SYNONYMS = {
        'simple': ['simple', 'normal'],
        'double': ['double'],
        'dashed': ['dashed'],
        'dotted': ['dotted'],
        'wavy': ['wavy'],
        'bold': ['bold', 'thick'],
        'light': ['light', 'thin'],
        'thick': ['thick'],
        'fancy': ['fancy', 'decorative'],
        'rounded': ['rounded', 'curved'],
        '3d': ['3d', 'three-d', 'threed'],
        'shadow': ['shadow'],
        'double_line': ['double_line', 'double-line', 'box'],
        'star': ['star'],
        'plus': ['plus', 'cross'],
    }
    
    def __init__(self):
        """Initialize the parser."""
        self.action_to_key = {}
        for action in self.ACTION_VERBS:
            self.action_to_key[action.lower()] = 'action'
        
        # Create reverse mappings for quick lookup
        self.shape_to_key = {}
        for key, synonyms in self.SHAPE_SYNONYMS.items():
            for syn in synonyms:
                self.shape_to_key[syn.lower()] = key
        
        self.direction_to_key = {}
        for key, synonyms in self.DIRECTION_SYNONYMS.items():
            for syn in synonyms:
                self.direction_to_key[syn.lower()] = key
        
        self.font_to_key = {}
        for key, synonyms in self.FONT_SYNONYMS.items():
            for syn in synonyms:
                self.font_to_key[syn.lower()] = key
        
        self.color_to_key = {}
        for key, synonyms in self.COLOR_SYNONYMS.items():
            for syn in synonyms:
                self.color_to_key[syn.lower()] = key
        
        self.fill_to_key = {}
        for key, synonyms in self.FILL_PATTERN_SYNONYMS.items():
            for syn in synonyms:
                self.fill_to_key[syn.lower()] = key
        
        self.border_to_key = {}
        for key, synonyms in self.BORDER_STYLE_SYNONYMS.items():
            for syn in synonyms:
                self.border_to_key[syn.lower()] = key

        self.mood_to_key = {}
        for key, synonyms in self.MOOD_SYNONYMS.items():
            for syn in synonyms:
                self.mood_to_key[syn.lower()] = key
        for word, canonical in load_learned_moods().items():
            if canonical in self.MOOD_SYNONYMS:
                self.mood_to_key[word.lower()] = canonical

    def teach_mood(self, word: str, canonical: str) -> bool:
        """Register a new mood synonym at runtime and persist it.

        Returns False (and does nothing) if `canonical` isn't a known mood.
        """
        word = word.lower().strip()
        canonical = canonical.lower().strip()
        if not word or canonical not in self.MOOD_SYNONYMS:
            return False
        self.mood_to_key[word] = canonical
        save_learned_mood(word, canonical)
        return True

    def _remove_accents(self, text: str) -> str:
        """Remove accents from text (not typically needed for English)."""
        return text
    
    def parse_command(self, command: str) -> Optional[Dict[str, Any]]:
        """Parse a natural language command and return structured data."""
        if not command or not command.strip():
            return None

        # Checked against the original (not lower-cased) command: a file
        # path is often case-sensitive, and the generic tokenizer below
        # lower-cases everything it sees.
        image_command = self._parse_image_command(command)
        if image_command:
            return image_command

        command_lower = command.lower().strip()

        # Check for intelligent mode exit commands
        if command_lower in ['menu', 'm', 'exit', 'quit', 'q', 'back']:
            return {'command': command_lower, 'action': command_lower}

        # Split compound commands ("a circle ... and a rectangle ...")
        parts = self._split_compound_command(command)
        if len(parts) > 1:
            parsed_parts = [p for p in (self._parse_single_command(part) for part in parts) if p]
            if parsed_parts:
                return {'command': 'compound', 'params': {}, 'compound': True, 'parts': parsed_parts}
            return None

        return self._parse_single_command(command)

    def _parse_image_command(self, command: str) -> Optional[Dict[str, Any]]:
        """Parse 'convert image <path> [width N] [color]' style commands.

        Kept separate from _parse_single_command's generic tokenizer
        because a file path must keep its original case and can contain
        characters (dots, slashes) that command word matching isn't meant
        to handle.
        """
        match = re.match(
            r'^\s*(?:convert\s+)?image(?:\s+to\s+ascii)?\s+(.+)$',
            command.strip(), re.IGNORECASE,
        )
        if not match:
            return None

        remainder = match.group(1).strip()

        color = False
        color_match = re.search(r'\s+(?:with\s+)?colou?r\s*$', remainder, re.IGNORECASE)
        if color_match:
            remainder = remainder[:color_match.start()].strip()
            color = True

        width = 100
        width_match = re.search(r'\s+width\s+(\d+)\s*$', remainder, re.IGNORECASE)
        if width_match:
            width = int(width_match.group(1))
            remainder = remainder[:width_match.start()].strip()

        path = remainder.strip('"\'')
        if not path:
            return None

        return {
            'raw': command,
            'command': 'image_to_ascii',
            'params': {'path': path, 'width': width, 'color': color},
        }

    def _split_compound_command(self, command: str) -> List[str]:
        """Split a compound command like 'X and Y' into individual command strings."""
        text = re.sub(r'\s*,\s*', ' and ', command)
        words = text.split()
        words_lower = [w.lower() for w in words]

        # Words that mean "and" is joining parameter values, not two shapes
        # (e.g. "with color red and blue"), so we shouldn't split there.
        param_keywords = {
            'color', 'colour', 'font', 'style', 'fill', 'filled', 'pattern',
            'border', 'edge', 'size', 'width', 'height', 'radius', 'base',
            'diameter', 'direction', 'dir', 'text',
        }

        split_positions = [
            i for i, word in enumerate(words_lower)
            if word == 'and' and not (i + 1 < len(words_lower) and words_lower[i + 1] in param_keywords)
        ]

        if not split_positions:
            return [command]

        parts = []
        start = 0
        for pos in split_positions:
            segment = words[start:pos]
            if segment:
                parts.append(' '.join(segment))
            start = pos + 1
        if start < len(words):
            parts.append(' '.join(words[start:]))

        return parts if len(parts) > 1 else [command]

    def _parse_single_command(self, command: str) -> Optional[Dict[str, Any]]:
        """Parse a single (non-compound) command."""
        command_lower = command.lower().strip()
        if not command_lower:
            return None

        # Extract numbers first (scoped to this part only)
        numbers = self.extract_numbers(command_lower)

        # Tokenize command
        tokens = command_lower.split()

        # Mood words are adjectives that typically come *before* the shape
        # ("happy dog", "a happy heart"), so scan all tokens regardless of
        # position - same idea as the number extraction above - rather than
        # only looking after the shape word like most other parameters.
        mood_key = next((self.mood_to_key[t] for t in tokens if t in self.mood_to_key), None)

        # Find action verb
        action = None
        action_idx = -1
        for i, token in enumerate(tokens):
            if token in self.ACTION_VERBS:
                action = token
                action_idx = i
                break

        if action is None:
            # Try to infer action from first token
            if tokens:
                action = tokens[0]
                action_idx = 0

        # Find shape/object
        shape = None
        shape_idx = -1
        shape_word = None  # literal token matched (e.g. "dog"), before synonym normalization

        # Text-oriented verbs always mean "the object is text", even if a
        # later word happens to coincide with a shape/font name (e.g. "write
        # HELLO with font banner" must not be read as drawing a banner).
        if action in ['write', 'type', 'print', 'convert']:
            shape = 'text'
            text_start = action_idx + 1
            if text_start < len(tokens):
                # Only treat a leading 'a'/'an'/'the' as an article to skip
                # when something follows it - otherwise a genuine one-word
                # payload that collides with an article ("write A") would
                # be swallowed and nothing would be left to capture.
                if tokens[text_start] in ['a', 'an', 'the'] and text_start + 1 < len(tokens):
                    text_start += 1
                shape_idx = text_start

        if shape is None and action_idx >= 0:
            # Look for shape in remaining tokens
            for i in range(action_idx + 1, len(tokens)):
                token = tokens[i]
                if token in self.shape_to_key:
                    shape = self.shape_to_key[token]
                    shape_word = token
                    shape_idx = i
                    break

                # Check for "a/an/the" prefix
                if i > 0 and tokens[i-1] in ['a', 'an', 'the']:
                    if token in self.shape_to_key:
                        shape = self.shape_to_key[token]
                        shape_word = token
                        shape_idx = i
                        break

        # If still no shape, try to find it differently
        if shape is None:
            for i, token in enumerate(tokens):
                if token in self.shape_to_key:
                    shape = self.shape_to_key[token]
                    shape_word = token
                    shape_idx = i
                    break
        
        # Extract parameters
        params = {}
        
        if shape_idx >= 0 and shape_idx + 1 < len(tokens):
            # Get remaining tokens after shape
            remaining = tokens[shape_idx + 1:]
            
            i = 0
            while i < len(remaining):
                token = remaining[i]
                
                # Check for "with", "of", "in", "using" etc.
                if token in ['with', 'of', 'in', 'using', 'for', 'as']:
                    i += 1
                    continue
                
                # Check for parameters with values
                if i + 1 < len(remaining):
                    next_token = remaining[i + 1]
                    
                    # Check for size/dimension parameters
                    if token in ['size', 'width', 'height', 'radius', 'base', 'diameter']:
                        if next_token.isdigit():
                            params[token] = int(next_token)
                            i += 2
                            continue
                        else:
                            i += 1
                            continue
                    
                    # Check for color
                    elif token in ['color', 'colour']:
                        if next_token in self.color_to_key:
                            params['color'] = self.color_to_key[next_token]
                        else:
                            params['color'] = next_token
                        i += 2
                        continue
                    
                    # Check for font
                    elif token == 'font':
                        if next_token in self.font_to_key:
                            params['font'] = self.font_to_key[next_token]
                        else:
                            params['font'] = next_token
                        i += 2
                        continue

                    # Check for fill style (e.g. "style dotted")
                    elif token in ['fill', 'filled', 'pattern', 'style']:
                        if next_token in self.fill_to_key:
                            params['fill'] = self.fill_to_key[next_token]
                        else:
                            params['fill'] = next_token
                        i += 2
                        continue
                    
                    # Check for border
                    elif token in ['border', 'edge']:
                        if next_token in self.border_to_key:
                            params['border'] = self.border_to_key[next_token]
                        else:
                            params['border'] = next_token
                        i += 2
                        continue
                    
                    # Check for direction
                    elif token in ['direction', 'dir', 'pointing', 'facing']:
                        if next_token in self.direction_to_key:
                            params['direction'] = self.direction_to_key[next_token]
                        else:
                            params['direction'] = next_token
                        i += 2
                        continue
                
                # Check for standalone parameters
                if token in ['solid', 'filled', 'empty', 'hollow']:
                    params['fill'] = token
                    i += 1
                    continue
                
                if token in self.color_to_key:
                    params['color'] = self.color_to_key[token]
                    i += 1
                    continue
                
                if token in self.font_to_key:
                    params['font'] = self.font_to_key[token]
                    i += 1
                    continue
                
                if token in self.fill_to_key:
                    params['fill'] = self.fill_to_key[token]
                    i += 1
                    continue
                
                if token in self.border_to_key:
                    params['border'] = self.border_to_key[token]
                    i += 1
                    continue

                i += 1
        
        # Map shape to command name
        shape_to_command = {
            'rectangle': 'rectangle',
            'square': 'rectangle',
            'box': 'rectangle',
            'triangle': 'triangle',
            'pyramid': 'triangle',
            'circle': 'circle',
            'ball': 'circle',
            'wheel': 'circle',
            'heart': 'heart',
            'diamond': 'diamond',
            'rhombus': 'diamond',
            'spiral': 'spiral',
            'snail': 'spiral',
            'volute': 'spiral',
            'tree': 'tree',
            'christmas_tree': 'tree',
            'star': 'star',
            'hexagon': 'hexagon',
            'hex': 'hexagon',
            'oval': 'oval',
            'ellipse': 'oval',
            'arrow': 'arrow',
            'pentagon': 'pentagon',
            'butterfly': 'butterfly',
            'flower': 'flower',
            'gradient': 'gradient',
            'degrade': 'gradient',
            'checkerboard': 'checkerboard',
            'chessboard': 'checkerboard',
            'random': 'random_art',
            'abstract': 'random_art',
            'art': 'random_art',
            'painting': 'random_art',
            'emoji': 'random_emoji',
            'emoticon': 'random_emoji',
            'animal': 'random_animal',
            'creature': 'random_animal',
            'text': 'text_to_ascii',
            'banner': 'banner',
            'box': 'box',
            # Smart commands
            'smart': 'smart',
            'surprise': 'surprise',
            'surprise me': 'surprise',
            'random art': 'random',
            'interesting': 'interesting',
            'amazing': 'amazing',
            'minimal': 'minimal',
            'simple': 'minimal',
            'clean': 'minimal',
            'complex': 'complex',
            'detailed': 'complex',
            'elaborate': 'complex',
            'geometric': 'geometric',
            'geometry': 'geometric',
            'nature': 'nature',
            'abstract': 'abstract',
            'pattern': 'abstract',
            'design': 'abstract',
        }
        
        command_name = shape_to_command.get(shape, shape) if shape else None

        # "dog"/"cat"/etc. are synonyms for the generic 'animal' shape key,
        # but unlike "animal"/"creature" they name one specific animal —
        # route those to specific_animal so e.g. "dog" always draws a dog
        # instead of a random pick among all animals.
        if shape == 'animal' and shape_word not in (None, 'animal', 'creature'):
            command_name = 'specific_animal'

        # Build params with numbers
        final_params = params.copy()
        if command_name == 'specific_animal' and 'animal' not in final_params:
            final_params['animal'] = shape_word
        # "a big cat" / "a large dog" -> the bigger drawing (ANIMALS_BIG)
        if command_name in ('specific_animal', 'random_animal') and \
                any(t in self.BIG_WORDS for t in tokens):
            final_params['big'] = True
        if numbers:
            if command_name in ['rectangle']:
                if len(numbers) >= 2:
                    final_params['width'] = numbers[0]
                    final_params['height'] = numbers[1]
                elif len(numbers) == 1:
                    final_params['width'] = numbers[0]
                    final_params['height'] = numbers[0]
            elif command_name == 'circle':
                if numbers:
                    final_params['radius'] = numbers[0]
            elif command_name in ['triangle', 'diamond', 'tree', 'spiral']:
                if numbers:
                    final_params['size'] = numbers[0]
            elif command_name == 'heart':
                if numbers:
                    final_params['size'] = min(max(numbers[0], 1), 8)
            elif command_name in ['checkerboard', 'gradient', 'random_art']:
                if numbers:
                    final_params['size'] = numbers[0]

        # Apply the mood's default color, unless the user already gave one
        if mood_key:
            final_params.setdefault('mood', mood_key)
            if 'color' not in final_params:
                effect = self.MOOD_EFFECTS.get(mood_key, {})
                if 'color' in effect:
                    final_params['color'] = effect['color']

        # Add char if not specified
        if 'char' not in final_params:
            final_params['char'] = '#'
        
        # Handle text commands: capture everything up to the next recognized
        # keyword (e.g. "write HELLO with font small" -> text="HELLO",
        # rather than swallowing "with font small" into the text itself).
        if command_name == 'text_to_ascii' and 'text' not in final_params:
            # For write/type/print/convert, shape_idx was already advanced
            # past the verb (and any article) to the first content token.
            # For "draw a text HELLO"-style commands, shape found via the
            # generic shape_to_key scan, shape_idx still points AT the
            # "text"/"word"/... keyword itself, so content starts one past it.
            if action in ['write', 'type', 'print', 'convert']:
                text_start = shape_idx if shape_idx >= 0 else len(tokens)
            else:
                text_start = shape_idx + 1 if shape_idx >= 0 else len(tokens)
            if text_start < len(tokens):
                # Only treat a leading 'a'/'an'/'the' as an article to skip
                # when something follows it - otherwise a genuine one-word
                # payload that collides with an article ("write A") would
                # be swallowed and nothing would be left to capture.
                if tokens[text_start] in ['a', 'an', 'the'] and text_start + 1 < len(tokens):
                    text_start += 1
                stop_words = {'with', 'font', 'style', 'color', 'colour',
                               'fill', 'filled', 'pattern', 'border', 'edge'}
                text_end = text_start
                while text_end < len(tokens) and tokens[text_end] not in stop_words:
                    text_end += 1
                if text_end == text_start:
                    text_end = len(tokens)
                final_params['text'] = ' '.join(tokens[text_start:text_end]).upper()

        # Handle banner/box commands: same idea, skipping the shape word
        # itself and the optional "with text" marker before capturing.
        if command_name in ('banner', 'box') and 'text' not in final_params:
            text_start = shape_idx + 1
            while text_start < len(tokens) and tokens[text_start] in ('with', 'text', 'a', 'an', 'the'):
                # As above: don't swallow a one-word payload that collides
                # with an article ("with text A") when it's all that's left.
                if tokens[text_start] in ('a', 'an', 'the') and text_start + 1 >= len(tokens):
                    break
                text_start += 1
            stop_words = {'color', 'colour', 'font', 'style', 'fill', 'filled',
                          'pattern', 'border', 'edge', 'width', 'char', 'character'}
            text_end = text_start
            while text_end < len(tokens) and tokens[text_end] not in stop_words:
                text_end += 1
            if text_end > text_start:
                final_params['text'] = ' '.join(tokens[text_start:text_end]).upper()

        # Build result dict
        result = {
            'raw': command,
            'command': command_name,
            'params': final_params,
        }
        
        return result if command_name else None
    
    def extract_numbers(self, text: str) -> list:
        """Extract all numbers from text."""
        import re
        # Patterns: 10, 10x5, 10 x 5, 10-5, 10:5, 10,5
        patterns = [
            r'(\d+)\s*x\s*(\d+)',  # 10x5 or 10 x 5
            r'(\d+)[-:](\d+)',       # 10-5 or 10:5
            r'(\d+),(\d+)',         # 10,5
        ]
        numbers = []
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                numbers.extend([int(n) for n in match])
        
        # Isolated numbers
        isolated = re.findall(r'\b(\d+)\b', text)
        for num in isolated:
            if int(num) not in numbers:
                numbers.append(int(num))
        
        return numbers
    
    def extract_char(self, text: str) -> Optional[str]:
        """Extract a drawing character from text."""
        import re
        # Patterns: "with #", "using *", "char @"
        patterns = [
            r'[wW]ith\s+["\']?([#*O@+=\-_\.\s])["\']?',
            r'[uU]sing\s+["\']?([#*O@+=\-_\.\s])["\']?',
            r'[cC]har\s+["\']?([#*O@+=\-_\.\s])["\']?',
            r'character\s+["\']?([#*O@+=\-_\.\s])["\']?',
            r'symbol\s+["\']?([#*O@+=\-_\.\s])["\']?',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                char = match.group(1)
                if char and char != ' ':
                    return char
        return None


class ASCIIArtCLI:
    """Main CLI class for ASCII Generator."""
    
    def __init__(self):
        self.menu = Menu("ASCII Generator")
        self.setup_menu()
        self.parser = ENCommandParser()
        self.intelligent_mode = False
    
    def setup_menu(self) -> None:
        """Setup all menu items."""
        self.menu.add_item('t', 'Text to ASCII', self.menu_text_to_ascii,
                          'Convert text to ASCII art', 'Text & Fonts')
        self.menu.add_item('r', 'Rectangle', self.menu_rectangle,
                          'Draw a rectangle', 'Shapes')
        self.menu.add_item('tr', 'Triangle', self.menu_triangle,
                           'Draw a triangle', 'Shapes')
        self.menu.add_item('c', 'Circle', self.menu_circle,
                           'Draw a circle', 'Shapes')
        self.menu.add_item('h', 'Heart', self.menu_heart,
                           'Draw a heart', 'Shapes')
        self.menu.add_item('d', 'Diamond', self.menu_diamond,
                           'Draw a diamond', 'Shapes')
        self.menu.add_item('tree', 'Tree', self.menu_tree,
                           'Draw a Christmas tree', 'Shapes')
        self.menu.add_item('g', 'Gradient', self.menu_gradient,
                           'Generate a gradient', 'Patterns')
        self.menu.add_item('cb', 'Checkerboard', self.menu_checkerboard,
                           'Generate a checkerboard', 'Patterns')
        self.menu.add_item('s', 'Spiral', self.menu_spiral,
                           'Generate a spiral', 'Patterns')
        self.menu.add_item('ra', 'Random Art', self.menu_random_art,
                           'Generate random art', 'Random')
        self.menu.add_item('a', 'Random Animal', self.menu_random_animal,
                           'Generate a random animal', 'Random')
        self.menu.add_item('e', 'Random Emoji', self.menu_random_emoji,
                           'Generate a random emoji', 'Random')
        self.menu.add_item('b', 'Banner', self.menu_banner,
                           'Create a banner', 'Text & Fonts')
        self.menu.add_item('box', 'Text Box', self.menu_box,
                           'Create a text box', 'Text & Fonts')
        self.menu.add_item('img', 'Image to ASCII', self.menu_image_to_ascii,
                           'Convert an image file to ASCII art', 'Text & Fonts')
        self.menu.add_item('spin', 'Spinner', lambda: spinner_animation(2.0),
                           'Show a spinner', 'Animations')
        self.menu.add_item('pb', 'Progress Bar', lambda: progress_bar(3.0),
                           'Show progress bar', 'Animations')
        self.menu.add_item('show', 'Showcase', self.menu_showcase,
                           'Display showcase', 'Main')
        self.menu.add_item('i', 'Intelligent Mode', self._activate_intelligent_mode,
                           'Speak in natural English!', 'Main')
        self.menu.add_item('?', 'Help', self.menu_help,
                           'Show help', 'Main')
    
    def menu_text_to_ascii(self) -> None:
        """Text to ASCII menu."""
        print(f"\n{Colors.OKBLUE}=== Text to ASCII ==={Colors.ENDC}")
        print(f"Available fonts: {', '.join(get_available_fonts())} "
              "(any FIGlet font name, e.g. slant, also works if pyfiglet is installed)")
        text = input("Enter text: ").strip() or "ASCII"
        font = input("Font (small) [small]: ").strip() or 'small'
        print(f"\n{Colors.OKGREEN}{text_to_ascii(text, font)}{Colors.ENDC}")
    
    def menu_rectangle(self) -> None:
        """Rectangle menu."""
        print(f"\n{Colors.OKBLUE}=== Rectangle ==={Colors.ENDC}")
        try:
            width = int(input("Width: ") or "40")
            height = int(input("Height: ") or "8")
            char = input("Character [#]: ") or "#"
            filled = input("Filled? (y/n) [y]: ").lower() or "y"
            print(f"\n{Colors.OKGREEN}{draw_rectangle(width, height, char, filled == 'y')}{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.FAIL}Invalid input.{Colors.ENDC}")
    
    def menu_triangle(self) -> None:
        """Triangle menu."""
        print(f"\n{Colors.OKBLUE}=== Triangle ==={Colors.ENDC}")
        print("Directions: up, down, left, right")
        try:
            height = int(input("Height: ") or "8")
            char = input("Character [*]: ") or "*"
            direction = input("Direction [up]: ").strip() or "up"
            print(f"\n{Colors.OKGREEN}{draw_triangle(height, char, direction)}{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.FAIL}Invalid input.{Colors.ENDC}")
    
    def menu_circle(self) -> None:
        """Circle menu."""
        print(f"\n{Colors.OKBLUE}=== Circle ==={Colors.ENDC}")
        try:
            radius = int(input("Radius: ") or "8")
            char = input("Character [O]: ") or "O"
            print(f"\n{Colors.OKGREEN}{draw_circle(radius, char)}{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.FAIL}Invalid input.{Colors.ENDC}")
    
    def menu_heart(self) -> None:
        """Heart menu."""
        print(f"\n{Colors.OKBLUE}=== Heart ==={Colors.ENDC}")
        try:
            size = int(input("Size (1-12) [6]: ") or "6")
            char = input("Character [*]: ") or "*"
            print(f"\n{Colors.OKGREEN}{draw_heart(size, char)}{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.FAIL}Invalid input.{Colors.ENDC}")
    
    def menu_diamond(self) -> None:
        """Diamond menu."""
        print(f"\n{Colors.OKBLUE}=== Diamond ==={Colors.ENDC}")
        try:
            size = int(input("Size: ") or "8")
            char = input("Character [*]: ") or "*"
            print(f"\n{Colors.OKGREEN}{draw_diamond(size, char)}{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.FAIL}Invalid input.{Colors.ENDC}")
    
    def menu_tree(self) -> None:
        """Tree menu."""
        print(f"\n{Colors.OKBLUE}=== Christmas Tree ==={Colors.ENDC}")
        try:
            height = int(input("Height: ") or "8")
            char = input("Character [*]: ") or "*"
            print(f"\n{Colors.OKGREEN}{generate_tree(height, char)}{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.FAIL}Invalid input.{Colors.ENDC}")
    
    def menu_gradient(self) -> None:
        """Gradient menu."""
        print(f"\n{Colors.OKBLUE}=== Gradient ==={Colors.ENDC}")
        try:
            width = int(input("Width: ") or "32")
            height = int(input("Height: ") or "8")
            print(f"\n{Colors.OKGREEN}{generate_gradient(width, height)}{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.FAIL}Invalid input.{Colors.ENDC}")
    
    def menu_checkerboard(self) -> None:
        """Checkerboard menu."""
        print(f"\n{Colors.OKBLUE}=== Checkerboard ==={Colors.ENDC}")
        try:
            size = int(input("Size: ") or "12")
            chars = input("Characters [# ]: ") or "# "
            print(f"\n{Colors.OKGREEN}{generate_checkerboard(size, chars)}{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.FAIL}Invalid input.{Colors.ENDC}")
    
    def menu_spiral(self) -> None:
        """Spiral menu."""
        print(f"\n{Colors.OKBLUE}=== Spiral ==={Colors.ENDC}")
        try:
            size = int(input("Size [18]: ") or "18")
            char = input("Character [*]: ") or "*"
            print(f"\n{Colors.OKGREEN}{generate_spiral(size, char)}{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.FAIL}Invalid input.{Colors.ENDC}")
    
    def menu_random_art(self) -> None:
        """Random art menu."""
        print(f"\n{Colors.OKBLUE}=== Random Art ==={Colors.ENDC}")
        try:
            width = int(input("Width: ") or "48")
            height = int(input("Height: ") or "14")
            print(f"\n{Colors.OKGREEN}{random_abstract(width, height)}{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.FAIL}Invalid input.{Colors.ENDC}")
    
    def menu_random_animal(self) -> None:
        """Random animal menu."""
        print(f"\n{Colors.OKBLUE}=== Random Animal ==={Colors.ENDC}")
        print(f"\n{Colors.OKGREEN}{random_animal()}{Colors.ENDC}")
    
    def menu_random_emoji(self) -> None:
        """Random emoji menu."""
        print(f"\n{Colors.OKBLUE}=== Random Emoji ==={Colors.ENDC}")
        print(f"\n{Colors.OKGREEN}{random_emoji()}{Colors.ENDC}")
    
    def menu_banner(self) -> None:
        """Banner menu."""
        print(f"\n{Colors.OKBLUE}=== Banner ==={Colors.ENDC}")
        text = input("Text: ").strip() or "HELLO"
        try:
            width = int(input("Width [50]: ") or "50")
            char = input("Border char [=]: ") or "="
            print(f"\n{Colors.OKGREEN}{create_banner(text, width, char)}{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.FAIL}Invalid input.{Colors.ENDC}")
    
    def menu_box(self) -> None:
        """Box menu."""
        print(f"\n{Colors.OKBLUE}=== Text Box ==={Colors.ENDC}")
        text = input("Text: ").strip() or "Hello\nWorld"
        char = input("Border char [#]: ") or "#"
        print(f"\n{Colors.OKGREEN}{create_box(text, None, char)}{Colors.ENDC}")

    def menu_image_to_ascii(self) -> None:
        """Image to ASCII menu."""
        print(f"\n{Colors.OKBLUE}=== Image to ASCII ==={Colors.ENDC}")
        path = input("Image path: ").strip()
        if not path:
            print(f"{Colors.FAIL}No path given.{Colors.ENDC}")
            return
        try:
            width = int(input("Width [100]: ") or "100")
        except ValueError:
            width = 100
        color = (input("Color? (y/n) [n]: ").strip().lower() or "n") == "y"
        self._render_image({'path': path, 'width': width, 'color': color})

    def _activate_intelligent_mode(self) -> None:
        """Activate intelligent mode."""
        self.intelligent_mode = True
        print(f"{Colors.OKGREEN}Activating intelligent mode...{Colors.ENDC}")
        time.sleep(0.5)
        self.run_intelligent_mode()
    
    def _print_specific_animal(self, animal_name: str, color: Optional[str] = None,
                               big: bool = False) -> None:
        """Print ASCII art for a specific animal by name.

        Falls back to a plausible substitute (see get_animal_art) with an
        explanatory note when there's no bespoke drawing for animal_name,
        instead of failing outright.
        """
        art, has_dedicated_art = get_animal_art(animal_name, big)
        if not has_dedicated_art:
            print(f"{Colors.WARNING}No dedicated drawing for '{animal_name}' yet - here is a similar one:{Colors.ENDC}")
        print(f"\n{self._apply_color(art, color)}")

    def _render_image(self, params: Dict[str, Any]) -> None:
        """Convert an image file to ASCII art and print it (see image_art.py)."""
        path = params.get('path', '')
        width = params.get('width', 100)
        color = params.get('color', False)
        try:
            art = image_to_ascii(path, width=width, color=color)
        except ImportError as exc:
            print(f"{Colors.FAIL}{exc}{Colors.ENDC}")
        except FileNotFoundError:
            print(f"{Colors.FAIL}Image not found: {path}{Colors.ENDC}")
        except Exception as exc:
            print(f"{Colors.FAIL}Could not read image '{path}': {exc}{Colors.ENDC}")
        else:
            print(f"\n{art}\n")

    def menu_showcase(self) -> None:
        """Display showcase."""
        print(f"\n{Colors.HEADER}=== ASCII Art Showcase ==={Colors.ENDC}\n")
        print(f"{Colors.OKBLUE}Text to ASCII:{Colors.ENDC}")
        print(text_to_ascii("HELLO"))
        print()
        print(f"{Colors.OKBLUE}Shapes:{Colors.ENDC}")
        print(draw_heart(2, '*'))
        print(draw_diamond(3, '*'))
        print()
        print(f"{Colors.OKBLUE}Tree:{Colors.ENDC}")
        print(generate_tree(4))
        print()
        print(f"{Colors.OKBLUE}Random:{Colors.ENDC}")
        print(f"Animal: {random_animal()}")
        print(f"Emoji: {random_emoji()}")
        print()
        print(f"{Colors.OKBLUE}Banner:{Colors.ENDC}")
        print(create_banner("ASCII ART", 40))
        print()
    
    def menu_help(self) -> None:
        """Display help."""
        print(f"\n{Colors.HEADER}=== Help ==={Colors.ENDC}")
        print("""
ASCII Generator - Generate ASCII art from text, shapes and patterns

Features:
- Convert text to ASCII art with different fonts
- Draw geometric shapes (rectangle, triangle, circle, heart, diamond, star, hexagon, oval, arrow, pentagon, butterfly, flower)
- Generate patterns (gradient, checkerboard, spiral, crosshatch, honeycomb, wave, zigzag)
- Create random art, animals and emojis
- Generate banners and text boxes
- Display animations (spinner, progress bar)

Usage:
- Type a menu option to select it
- Type 'q' to quit
- Follow the instructions for each function

INTELLIGENT MODE (type 'i' to activate):
- draw a heart -> generates a heart
- make a rectangle 10x5 with # -> draws rectangle 10x5 with #
- create a circle with radius 8 -> creates circle with radius 8
- write "HELLO" in ASCII -> converts HELLO to ASCII art
- show examples -> displays the showcase
- surprise me -> generates interesting random art
- help -> shows this help
        """)
    
    def _create_custom_banner(self, text: str, width: int = 50, char: str = '=', 
                                color: Optional[str] = None, border_style: Optional[str] = None) -> str:
        """Create a custom banner with color and border style support."""
        # Get border characters based on style
        if border_style:
            top_char, bottom_char, left_char, right_char = get_border_chars(border_style)
        else:
            top_char = bottom_char = left_char = right_char = char
        
        padding = (width - len(text) - 2) // 2
        border = top_char * width
        lines = [
            border,
            left_char + ' ' * (width - 2) + right_char,
            left_char + ' ' * padding + text + ' ' * (width - padding - len(text) - 2) + right_char,
            left_char + ' ' * (width - 2) + right_char,
            bottom_char * width
        ]
        result = '\n'.join(lines)
        
        # Apply color
        if color:
            color_code = get_color_code(color)
            result = color_code + result + get_color_code('reset')
        
        return result

    def _create_custom_box(self, text: str, border_char: str = '#', 
                           color: Optional[str] = None, border_style: Optional[str] = None) -> str:
        """Create a custom box with color and border style support."""
        # Get border characters based on style
        if border_style:
            top_char, bottom_char, left_char, right_char = get_border_chars(border_style)
        else:
            top_char = bottom_char = left_char = right_char = border_char
        
        lines = text.split('\n')
        width = max(len(line) for line in lines) + 4
        
        border = top_char * width
        result = [border]
        for line in lines:
            padding = width - len(line) - 3
            result.append(left_char + ' ' + line + ' ' * padding + right_char)
        result.append(bottom_char * width)
        
        output = '\n'.join(result)
        
        # Apply color
        if color:
            color_code = get_color_code(color)
            output = color_code + output + get_color_code('reset')
        
        return output

    def _apply_color(self, content: str, color: Optional[str] = None) -> str:
        """Apply color to content if specified."""
        if color:
            if color.lower() in ('rainbow', 'multicolor', 'multicolour'):
                lines = content.split('\n')
                return '\n'.join(
                    self._apply_color(line, RAINBOW_COLORS[i % len(RAINBOW_COLORS)])
                    for i, line in enumerate(lines)
                )
            # Use smart generator's color mapping which includes light colors
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
            color_code = color_map.get(color.lower(), '\033[0m')
            return color_code + content + '\033[0m'
        return content
    
    def execute_parsed_command(self, command_dict: Dict[str, Any]) -> None:
        """Execute a parsed command dictionary."""
        command = command_dict.get('command', '')
        params = command_dict.get('params', {})
        
        # Handle compound commands
        if command == 'compound':
            parts = command_dict.get('parts', [])
            print(f"\n{Colors.OKBLUE}=== Compound Command ==={Colors.ENDC}")
            for i, part in enumerate(parts, 1):
                print(f"\n{Colors.OKBLUE}[{i}/{len(parts)}]{Colors.ENDC}")
                self.execute_parsed_command(part)
            return
        
        # Handle smart generation commands
        if command in ['smart', 'surprise', 'random', 'interesting', 'amazing', 'minimal', 'complex', 'geometric', 'nature', 'abstract']:
            art = smart_gen.generate_from_command(command)
            joined = '\n'.join(art)
            # smart_gen already colors its own output line-by-line when it
            # picks a color; wrapping that in another color here nests ANSI
            # codes and the inner reset kills the outer color early. Only
            # apply the default green wrap when the art has no color of its
            # own.
            if '\033[' in joined:
                print(f"\n{joined}")
            else:
                print(f"\n{Colors.OKGREEN}{joined}{Colors.ENDC}")
            return
        
        # Extract style parameters for smart patterns
        fill_pattern = params.get('fill', params.get('pattern', 'solid'))
        border = params.get('border', 'none')
        char = params.get('char', '#')
        color = params.get('color')
        font = params.get('font', 'small')
        border_style = params.get('border_style', border)
        
        # Add new shapes to command mapping
        def render_shape(shape_name, *args):
            shape_func = {
                'rectangle': draw_rectangle,
                'triangle': draw_triangle,
                'circle': draw_circle,
                'heart': draw_heart,
                'diamond': draw_diamond,
                'tree': generate_tree,
                'spiral': generate_spiral,
                'star': draw_star,
                'hexagon': draw_hexagon,
                'oval': draw_oval,
                'arrow': draw_arrow,
                'pentagon': draw_pentagon,
                'butterfly': draw_butterfly,
                'flower': draw_flower,
            }.get(shape_name)
            if shape_func:
                art = shape_func(*args)
                rendered = self._apply_style_to_art(art, params)
                print(f"\n{'\n'.join(rendered)}")
        
        command_mapping = {
            'text_to_ascii': lambda: print(f"\n{self._apply_color(text_to_ascii(params.get('text', 'ASCII'), font), color)}"),
            'rectangle': lambda: render_shape('rectangle', params.get('width', 40), params.get('height', 8), char, params.get('filled', True)),
            'triangle': lambda: render_shape('triangle', params.get('height', 8), char, params.get('direction', 'up')),
            'circle': lambda: render_shape('circle', params.get('radius', 8), char),
            'heart': lambda: render_shape('heart', params.get('size', 6), char),
            'diamond': lambda: render_shape('diamond', params.get('size', 8), char),
            'tree': lambda: render_shape('tree', params.get('height', 8), char),
            'star': lambda: render_shape('star', params.get('size', 7), char),
            'hexagon': lambda: render_shape('hexagon', params.get('size', 8), char),
            'oval': lambda: render_shape('oval', params.get('width', 40), params.get('height', 8), char),
            'arrow': lambda: render_shape('arrow', params.get('direction', 'right'), params.get('size', 8), char),
            'pentagon': lambda: render_shape('pentagon', params.get('size', 8), char),
            'butterfly': lambda: render_shape('butterfly', params.get('size', 8), char),
            'flower': lambda: render_shape('flower', params.get('size', 7), char),
            'gradient': lambda: print(f"\n{self._apply_color(generate_gradient(params.get('width', 32), params.get('height', 8)), color)}"),
            'checkerboard': lambda: print(f"\n{self._apply_color(generate_checkerboard(params.get('size', 12), params.get('chars', '# ')), color)}"),
            'spiral': lambda: render_shape('spiral', params.get('size', 18), char),
            'random_art': lambda: print(f"\n{self._apply_color(random_abstract(params.get('width', 48), params.get('height', 14)), color)}"),
            'random_animal': lambda: print(f"\n{self._apply_color(random_animal(params.get('big', False)), color)}"),
            'random_emoji': lambda: print(f"\n{self._apply_color(random_emoji(), color)}"),
            'banner': lambda: print(f"\n{self._create_custom_banner(params.get('text', 'ASCII'), params.get('width', 50), params.get('char', '='), color, border_style)}"),
            'box': lambda: print(f"\n{self._create_custom_box(params.get('text', 'Hello\nWorld'), params.get('char', '#'), color, border_style)}"),
            'spinner': lambda: spinner_animation(params.get('duration', 2.0)),
            'progress_bar': lambda: progress_bar(params.get('duration', 3.0)),
            'showcase': self.menu_showcase,
            'help': self.menu_help,
            'quit': lambda: None,
            'specific_animal': lambda: self._print_specific_animal(params.get('animal', 'crow'), color, params.get('big', False)),
            'image_to_ascii': lambda: self._render_image(params),
        }
        
        if command in command_mapping:
            command_mapping[command]()
        else:
            print(f"{Colors.FAIL}Command not recognized: {command}{Colors.ENDC}")
    
    def _apply_style_to_art(self, art: List[str], params: Dict[str, Any]) -> List[str]:
        """Apply fill pattern, border, and color to art based on params."""
        if not art:
            return art
        
        fill_pattern = params.get('fill', params.get('pattern', 'solid'))
        border = params.get('border', 'none')
        char = params.get('char', '#')
        color = params.get('color')
        
        # Convert to list if it's a single string
        if isinstance(art, str):
            art = art.split('\n')
        
        # Apply fill pattern, masked to the shape's own silhouette (a naive
        # whole-grid swap would replace e.g. a hexagon with a plain rectangle)
        if fill_pattern != 'solid' and isinstance(art, list) and art:
            art = mask_fill_pattern(art, fill_pattern, char)

        # Apply border if specified
        if border != 'none' and isinstance(art, list) and art:
            art = apply_border(art, border, char)
        
        # Apply color. Colorize the whole block in one call (rather than
        # each line separately) so 'rainbow' can cycle a color per line -
        # calling _apply_color per line would give every line the same
        # single-element cycle position instead of a gradient down the shape.
        if color and isinstance(art, list) and art:
            art = self._apply_color('\n'.join(art), color).split('\n')

        return art
    
    def run_intelligent_mode(self) -> None:
        """Run the CLI in intelligent mode (natural language)."""
        print(f"\n{Colors.HEADER}")
        print("  _____ _   _ _   _  ____ _____ _____ ____")
        print(" / ____| \\ | | \\ | |/ ___|_   _|_   _|  _ \\")
        print("| |    |  \\| |  \\| | |   | | | | | | | |_) |")
        print("| |___ | |\\  | |\\  | |___| | | | | | |  _ <")
        print(" \\____||_| \\_|_| \\_|\\____|_| |_| |_| |_| \\_\\" + f"{Colors.ENDC}")
        
        print(f"\n{Colors.OKBLUE}=== INTELLIGENT MODE ==={Colors.ENDC}")
        print(f"{Colors.OKBLUE}Type in natural English (e.g., 'draw a heart' or 'make a rectangle 10x5'){Colors.ENDC}")
        print(f"{Colors.OKBLUE}Type 'teach <word> as <mood>' to teach a new mood synonym (e.g. 'teach ecstatic as happy').{Colors.ENDC}")
        print(f"{Colors.OKBLUE}Type 'menu' to return to menu or 'q' to quit.{Colors.ENDC}\n")
        
        while True:
            try:
                user_input = input(f"{Colors.BOLD}What would you like? {Colors.ENDC}").strip()
                
                if not user_input:
                    continue
                
                # Check for mode switch commands
                if user_input.lower() in ['menu', 'm']:
                    print(f"{Colors.OKGREEN}Returning to menu...{Colors.ENDC}")
                    self.intelligent_mode = False
                    break
                
                if user_input.lower() in ['q', 'quit', 'exit']:
                    print(f"\n{Colors.OKGREEN}Goodbye!{Colors.ENDC}")
                    sys.exit(0)

                if user_input.lower().startswith('teach '):
                    self._handle_teach_command(user_input)
                    continue

                # Parse the command
                parsed = self.parser.parse_command(user_input)
                
                if parsed:
                    command = parsed.get('command')
                    if command == 'quit':
                        print(f"\n{Colors.OKGREEN}Goodbye!{Colors.ENDC}")
                        sys.exit(0)
                    self.execute_parsed_command(parsed)
                    print()  # Add spacing
                else:
                    # Try to give helpful suggestions
                    print(f"{Colors.WARNING}Could not understand. Try this:{Colors.ENDC}")
                    self._suggest_commands(user_input)
                    
            except KeyboardInterrupt:
                print(f"\n{Colors.WARNING}Use 'q' to quit or 'menu' to return to menu.{Colors.ENDC}")
            except Exception as e:
                print(f"{Colors.FAIL}Error: {e}{Colors.ENDC}")
    
    def _handle_teach_command(self, user_input: str) -> None:
        """Handle 'teach <word> as <mood>' - registers a new mood synonym."""
        body = user_input[len('teach '):].strip()
        known_moods = ', '.join(sorted(self.parser.MOOD_SYNONYMS))

        if ' as ' not in body:
            print(f"{Colors.WARNING}Usage: teach <word> as <mood>{Colors.ENDC}")
            print(f"  Known moods: {known_moods}")
            return

        word, _, mood = body.partition(' as ')
        word = word.strip()
        mood = mood.strip()

        if self.parser.teach_mood(word, mood):
            print(f"{Colors.OKGREEN}Learned: '{word}' now means mood '{mood}'.{Colors.ENDC}")
        else:
            print(f"{Colors.FAIL}Unknown mood '{mood}'. Known moods: {known_moods}{Colors.ENDC}")

    def _suggest_commands(self, user_input: str) -> None:
        """Suggest possible commands based on user input."""
        suggestions = []
        text_lower = user_input.lower()
        
        # Check for known shapes
        for shape_key, synonyms in self.parser.SHAPE_SYNONYMS.items():
            for syn in synonyms:
                if syn.lower() in text_lower:
                    suggestions.append(f"- Try: 'draw a {syn}'")
                    break
        
        # Check for actions
        if any(v in text_lower for v in ['help', '?']):
            suggestions.append("- Type 'help' to see the help")
        
        if any(v in text_lower for v in ['quit', 'exit']):
            suggestions.append("- Type 'q' or 'quit' to exit")
        
        if any(v in text_lower for v in ['menu']):
            suggestions.append("- Type 'menu' to return to main menu")
        
        if not suggestions:
            suggestions = [
                "- Example: 'draw a heart'",
                "- Example: 'make a rectangle 10x5'",
                "- Example: 'write HELLO in ASCII'",
                "- Example: 'show examples'",
                "- Type 'help' to see all options"
            ]
        
        for suggestion in suggestions[:3]:  # Show max 3 suggestions
            print(f"  {suggestion}")
    
    def run(self) -> None:
        """Run the CLI."""
        print(f"\n{Colors.HEADER}")
        print("  _____ _   _ _   _  ____ _____ _____ ____")
        print(" / ____| \\ | | \\ | |/ ___|_   _|_   _|  _ \\")
        print("| |    |  \\| |  \\| | |   | | | | | | | |_) |")
        print("| |___ | |\\  | |\\  | |___| | | | | | |  _ <")
        print(" \\____||_| \\_|_| \\_|\\____|_| |_| |_| |_| \\_\\" + f"{Colors.ENDC}")
        # Check if we should start in intelligent mode
        if self.intelligent_mode:
            self.run_intelligent_mode()
        else:
            self.menu.run()


def main():
    """Main entry point."""
    setup_console()
    enable_utf8_output()
    cli = ASCIIArtCLI()
    cli.run()


if __name__ == "__main__":
    main()
