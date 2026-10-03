# ASCII Generator

A Python ASCII Art generator: draws geometric shapes, converts text into ASCII letters, generates patterns, and runs simple terminal animations — all through natural-language (English) commands or an interactive menu.

## Requirements

- Python 3.12+ (needed because `cli.py` uses a backslash inside an f-string
  expression, a syntax only legal since PEP 701)
- Standard library only, with one deliberate exception: image-to-ASCII
  conversion (`convert image ...`) needs [Pillow](https://pypi.org/project/Pillow/)
  to decode image files. Everything else has no external dependencies.

## Installation

Works the same on Windows, Linux, and macOS:

```bash
git clone https://github.com/JoaoTomas991/ascii_generator.git
cd ascii_generator
pip install -e .
```

That installs an `ascii-generator` command on your `PATH` — a native launcher
on each platform (`ascii-generator.exe` on Windows), so you never have to work
out which Python binary to call. It is the recommended way to use the project.

To also enable image-to-ASCII conversion, install Pillow:

```bash
pip install -r requirements.txt
```

Nothing has to be installed to use shapes, text, patterns, or animations — you
can always run the scripts in place instead (see
[Running without installing](#running-without-installing) below).

## Usage

There are three ways to drive the generator, shown below with the installed
`ascii-generator` command. The two sections after them cover running from a
clone without installing, and the Unix-only shortcuts.

### 1. Menu mode (interactive)

```bash
ascii-generator
```

Shows a menu with all available shapes, patterns, text, and animations.

### 2. Intelligent mode (natural language, inside the menu)

From the menu, choose `i` to enter intelligent mode and type commands freely in English:

```bash
ascii-generator --intelligent
```

### 3. Direct command (single line, non-interactive)

```bash
ascii-generator "draw a rectangle 10x5"
ascii-generator "make a circle with radius 8 color blue"
ascii-generator "write HELLO with font banner"
```

### Running without installing

`run.py` is the same entry point and works straight from a clone. The catch is
that the interpreter has a different name per platform — there is no single
command that works everywhere:

```bash
python3 run.py "draw a heart"   # Linux, macOS
python run.py "draw a heart"    # Windows
```

On Windows, a bare `python3` is usually the Microsoft Store stub, which prints
an install prompt instead of running anything. This is the reason
`pip install -e .` above is the recommended path.

### Unix-only shortcuts

The `Makefile` and `start.sh` are conveniences for Linux and macOS; `make` is
not available on Windows by default, and `start.sh` needs a POSIX shell. The
`Makefile` calls `python3`, overridable with `make run PYTHON=python`;
`start.sh` probes `python3`, `python`, and `py` and uses the first one that is
actually 3.12+.

```bash
make run               # menu mode
make intelligent       # intelligent mode
make command-draw      # draw a rectangle 10x5
make command-circle    # make a circle with radius 8
make command-heart     # draw a heart
make command-tree      # create a tree with height 10
make command-banner    # make a banner with text ASCII ART
make command-text      # write HELLO with font banner
```

`./start.sh` opens a small startup menu (menu mode, intelligent mode, direct
command, or help).

## Capabilities

- **Shapes**: rectangle, circle, triangle, heart, diamond, spiral, tree, star, hexagon, oval, arrow, pentagon, butterfly, flower
- **Text to ASCII**: 4 fonts — `small`, `block`, `banner`, `shadow`
- **Patterns**: gradient, checkerboard, abstract/random art
- **Random generators**: faces, emojis, animals — naming a specific animal (cat, dog, rabbit, bear, fish, penguin, owl, crow, raven) always draws that animal; asking for "an animal"/"a creature" instead picks one of them at random
- **Banners and boxes** with custom text
- **Terminal animations**: spinner, progress bar
- **Styling**: color (ANSI: red, green, blue, yellow, cyan, magenta, white, black + `bright_*` variants, plus `rainbow`/`multicolor` which cycles a color per line), up to 31 fill patterns (always applied inside the shape's own silhouette, never replacing it), and several border styles — see `.claude/skills/ascii-art/SKILL.md` for the full catalog with functions and files
- **Moods (teachable)**: `happy`, `sad`, `angry`, `calm`, `sleepy` — recognized anywhere in a command and applied as a default color (unless you already gave one explicitly). Teach new synonyms with `teach <word> as <mood>` (e.g. `teach ecstatic as happy`), either in intelligent mode or as a direct one-shot command; taught words persist across sessions in `~/.config/ascii_generator/learned_words.json`. See [`docs/adr/0001-taught-mood-synonyms.md`](docs/adr/0001-taught-mood-synonyms.md) for why this is deliberately a small, taught dictionary rather than automatic word detection or NLP.
- **Image to ASCII**: `convert image <path> [width N] [color]` converts a real image file (PNG/JPG/...) into ASCII art using a brightness ramp, with an option for true 24-bit color per character (requires Pillow — see Requirements).

### Example commands

```
draw a rectangle 10x5
make a circle with radius 8 color blue
draw a heart size 2
write HELLO
make a rectangle 8x4 with color cyan
make a rectangle 8x4 with color cyan style dotted
make a spiral 20
make an emoji
make a circle with radius 5 color blue and a rectangle 10x5 color red
draw a happy dog
teach ecstatic as happy
draw an ecstatic heart
draw a heart size 4 color rainbow
convert image /tmp/photo.png width 80 color
```

### Known limitations

- No GIF animations (terminal only); colors depend on the terminal's ANSI support.
- The `"and"` compound-command splitter is word-based, so a color list like `"with color red and blue"` on a single shape may get misread as two shapes.
- `teach` can only alias a new word to one of the 5 built-in moods — it cannot create a new mood or a new visual effect.

## Project structure

```
ascii_art_generator/
├── ascii_art.py        # base shapes, fonts, patterns, banners, animations
├── cli.py              # ENCommandParser + command-line interface
├── smart_generator.py  # advanced shapes, fill/border patterns, random generation
├── image_art.py        # image-to-ASCII conversion (the one module that needs Pillow)
├── learned_words.py    # persistence for user-taught mood synonyms
├── console.py          # UTF-8 stdout setup shared by the entry points
└── main.py             # entry point

run.py             # startup script (menu / intelligent / direct command)
setup.py           # packaging; provides the "ascii-generator" command
start.sh           # interactive startup menu (Unix only)
Makefile           # run and test shortcuts (Unix only)
requirements.txt   # Pillow, needed only for image-to-ASCII conversion
docs/adr/          # architecture decision records
```

## Testing

On Linux and macOS:

```bash
make test
```

Everywhere, including Windows, the same two checks without `make`:

```bash
python -c "from ascii_art_generator.ascii_art import draw_rectangle, draw_circle, draw_heart, draw_diamond, text_to_ascii; print('Import tests: OK')"
python -c "from ascii_art_generator.cli import ENCommandParser; p = ENCommandParser(); print('Parser tests: OK')"
```

Runs a smoke test against the main imports and the command parser. CI runs
these on Windows, Linux, and macOS against Python 3.12, 3.13, and 3.14 — see
[`.github/workflows/ci.yml`](.github/workflows/ci.yml).
