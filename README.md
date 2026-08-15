# ASCII Generator

A Python ASCII Art generator: draws geometric shapes, converts text into ASCII letters, generates patterns, and runs simple terminal animations — all through natural-language (English) commands or an interactive menu.

## Requirements

- Python 3.10+
- No external dependencies (standard library only)

## Installation

```bash
git clone https://github.com/JoaoTomas991/ascii_generator.git
cd ascii_generator
```

Nothing to install — just run it directly with `python3`.

## Usage

There are three ways to use the generator:

### 1. Menu mode (interactive)

```bash
python3 run.py
# or
make run
```

Shows a menu with all available shapes, patterns, text, and animations.

### 2. Intelligent mode (natural language, inside the menu)

From the menu, choose `i` to enter intelligent mode and type commands freely in English:

```bash
python3 run.py --intelligent
# or
make intelligent
```

### 3. Direct command (single line, non-interactive)

```bash
python3 run.py "draw a rectangle 10x5"
python3 run.py "make a circle with radius 8 color blue"
python3 run.py "write HELLO with font banner"
```

There are also shortcuts in the `Makefile`:

```bash
make command-draw      # draw a rectangle 10x5
make command-circle    # make a circle with radius 8
make command-heart     # draw a heart
make command-tree      # create a tree with height 10
make command-banner    # make a banner with text ASCII ART
make command-text      # write HELLO with font banner
```

Alternative: `./start.sh` opens a small startup menu (menu mode, intelligent mode, direct command, or help).

## Capabilities

- **Shapes**: rectangle, circle, triangle, heart, diamond, spiral, tree, star, hexagon, oval, arrow, pentagon, butterfly, flower
- **Text to ASCII**: 4 fonts — `small`, `block`, `banner`, `shadow`
- **Patterns**: gradient, checkerboard, abstract/random art
- **Random generators**: faces, animals (cat, dog, rabbit, bear, fish, penguin, owl, crow), emojis
- **Banners and boxes** with custom text
- **Terminal animations**: spinner, progress bar
- **Styling**: color (ANSI: red, green, blue, yellow, cyan, magenta, white, black + `bright_*` variants), up to 31 fill patterns, and several border styles — see `.claude/skills/ascii-art/SKILL.md` for the full catalog with functions and files

### Example commands

```
draw a rectangle 10x5
make a circle with radius 8 color blue
draw a heart size 2
write HELLO
make a rectangle 8x4 with color cyan
```

### Known limitations

- The English command parser (`ENCommandParser`) **does not support compound commands** — `"a circle ... and a rectangle ..."` only draws the first shape.
- `"write TEXT with font X"` can misbehave if `X` matches the name of a shape (e.g. `banner`).
- `"style X"` maps to the font, not the fill — use `fill X` to request a fill pattern instead.
- No GIF animations (terminal only); colors depend on the terminal's ANSI support.

## Project structure

```
ascii_art_generator/
├── ascii_art.py        # base shapes, fonts, patterns, banners, animations
├── cli.py              # ENCommandParser + command-line interface
├── smart_generator.py  # advanced shapes, fill/border patterns, random generation
└── main.py             # entry point

run.py       # startup script (menu / intelligent / direct command)
start.sh     # interactive startup menu
Makefile     # run and test shortcuts
```

## Testing

```bash
make test
```

Runs a smoke test against the main imports and the command parser.

## Developing with Claude Code

The project includes `CLAUDE.md` with agent conventions, and a skill (`.claude/skills/ascii-art/SKILL.md`) with the full catalog of shapes, fonts, colors, fill patterns, and borders — check them before adding a new shape or style.
