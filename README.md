# ASCII Art Generator

A Python ASCII Art generator: draws geometric shapes, converts text into ASCII letters, generates patterns, and runs simple terminal animations, all through natural-language (English) commands or an interactive menu.

## Requirements

- Python 3.12+ (needed because `cli.py` uses a backslash inside an f-string
  expression, a syntax only legal since PEP 701)
- Standard library only, with one deliberate exception: image-to-ASCII
  conversion (`convert image ...`) needs [Pillow](https://pypi.org/project/Pillow/)
  to decode image files. Everything else has no external dependencies.
- Optional: [pyfiglet](https://pypi.org/project/pyfiglet/) for proper FIGlet
  fonts in text-to-ASCII (`write ...`). Without it, `write` still works using
  the simpler built-in fonts.

## Installation

Works the same on Windows, Linux, and macOS. If you only want to try it
without installing Python, grab a standalone executable instead (see
[Standalone executables](#standalone-executables-no-python-needed)).

The recommended way to install from source is [pipx](https://pipx.pypa.io/)
(or `uv`), which puts the command on your `PATH` in its own isolated
environment and works even where the system Python is locked down:

```bash
git clone https://github.com/JoaoTomas991/ascii-art-generator.git
cd ascii-art-generator
pipx install ".[all]"             # or: uv tool install ".[all]"
```

That installs an `ascii-art-generator` command on your `PATH`, a native launcher
on each platform (`ascii-art-generator.exe` on Windows), so you never have to work
out which Python binary to call. The shorter `ascii-generator` also works as an
alias. `[all]` also enables image-to-ASCII
conversion (Pillow) and FIGlet text fonts (pyfiglet). Use `".[images]"` or
`".[fonts]"` for only one of them, or plain `"."` for neither.

Getting pipx: `sudo apt install pipx` (Debian/Ubuntu), `brew install pipx`
(macOS), `pip install pipx` (Windows).

For development, use an editable install inside a virtual environment:

```bash
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[all]"
```

On Debian, Ubuntu, and Homebrew Python, a plain `pip install` outside a
virtual environment fails with `externally-managed-environment`. Use pipx or
a venv as above. On Debian, `python3 -m venv` may also need
`sudo apt install python3-venv`.

Other ways to get the same dependencies:

```bash
pip install -r requirements.txt
# or
make install
# or, on Debian/Ubuntu (no pip needed)
sudo apt install python3-pil python3-pyfiglet
```

Nothing has to be installed to use shapes, text, patterns, or animations. You
can always run the scripts in place instead (see
[Running without installing](#running-without-installing) below).

## Usage

There are three ways to drive the generator, shown below with the installed
`ascii-art-generator` command. The two sections after them cover running from a
clone without installing, and the Unix-only shortcuts.

### 1. Menu mode (interactive)

```bash
ascii-art-generator
```

Shows an animated banner and a menu with the basic shapes, patterns, text, image conversion, random generators and animations, laid out in up to three columns so it fits on a normal terminal. The other shapes (star, hexagon, oval, arrow, pentagon, butterfly, flower) are reached by typing a command in intelligent mode.

### 2. Intelligent mode (natural language, inside the menu)

From the menu, choose `i` to enter intelligent mode and type commands freely in English:

```bash
ascii-art-generator --intelligent
```

The interactive modes open with an animated banner (plain ANSI, no extra
packages). It is skipped automatically when the output is not a terminal; pass
`--no-animation`, set `ASCII_GENERATOR_NO_ANIMATION=1`, or use `TERM=dumb` to turn it off.

`ascii-art-generator --version` shows which code the command is running (editable
install, installed copy or source checkout, plus the git branch). A regular
install is a snapshot of the sources; if it falls behind the project folder the
command prints a warning on startup. For development, install it editable so it
always follows the folder: `uv tool install --editable .` or `pipx install --editable .`

### 3. Direct command (single line, non-interactive)

```bash
ascii-art-generator "draw a rectangle 10x5"
ascii-art-generator "make a circle with radius 8 color blue"
ascii-art-generator "write HELLO with font banner"
```

### Running without installing

`run.py` is the same entry point and works straight from a clone. The catch is
that the interpreter has a different name per platform, so no single
command works everywhere:

```bash
python3 run.py "draw a heart"   # Linux, macOS
python run.py "draw a heart"    # Windows
```

On Windows, a bare `python3` is usually the Microsoft Store stub, which prints
an install prompt instead of running anything. This is the reason
the installed `ascii-art-generator` command (see Installation) is the recommended path.

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

- Shapes: rectangle, circle, triangle, heart, diamond, spiral, tree, star, hexagon, oval, arrow, pentagon, butterfly, flower
- Text to ASCII: 4 named fonts (`small`, `block`, `banner`, `shadow`; with the current pyfiglet, `banner` falls back to the `small` look because the FIGlet font it points to is not bundled), rendered with real FIGlet fonts when pyfiglet is installed, which also accepts any other FIGlet font name (e.g. `write HELLO with font slant`). Without pyfiglet, simpler built-in 5-line fonts are used
- Patterns: gradient, checkerboard, abstract/random art
- Random generators: emojis and animals. A random emoji is a big face composed from a head, eyes, brows, a mouth and extras (13 moods, from happy and wink to angry and sleepy; see `emoji_art.py`), about the size of a big animal. Naming a mood (`draw a sad emoji`) picks a matching face. A random animal is composed as a coin, a framed portrait or a themed scene (meadow, rain, snow, beach, space, forest), e.g. a "$DOG" coin; see `animal_scenes.py`. Naming a specific animal (cat, dog, rabbit, bear, fish, penguin, owl, crow, raven) always draws that animal, while asking for "an animal" or "a creature" picks one of them at random. Add `big`/`large`/`huge`/`giant` for a bigger, more detailed drawing (e.g. `draw a big cat`)
- Banners and boxes with custom text
- Terminal animations: spinner, progress bar, and an animated startup banner whose rainbow keeps moving while the menu waits for your choice
- Browser version: the same generator running on a web page, see [Try it in the browser](#try-it-in-the-browser)
- Styling: color (ANSI: red, green, blue, yellow, cyan, magenta, white, black + `bright_*` variants, plus `rainbow`/`multicolor`, which cycles a color per line), up to 32 fill patterns (always applied inside the shape's own silhouette, never replacing it), and several border styles. See `.claude/skills/ascii-art/SKILL.md` for the full catalog with functions and files
- Moods (teachable): `happy`, `sad`, `angry`, `calm`, `sleepy`, recognized anywhere in a command and applied as a default color (unless you already gave one explicitly). Teach new synonyms with `teach <word> as <mood>` (e.g. `teach ecstatic as happy`), either in intelligent mode or as a direct one-shot command; taught words persist across sessions in `~/.config/ascii_generator/learned_words.json`. See [`docs/adr/0001-taught-mood-synonyms.md`](docs/adr/0001-taught-mood-synonyms.md) for why this is deliberately a small, taught dictionary rather than automatic word detection or NLP.
- Image to ASCII: `convert image <path> [width N] [color]` converts a real image file (PNG/JPG/...) into ASCII art using a brightness ramp, with an option for true 24-bit color per character (requires Pillow; see Requirements).

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
draw a star 8 color yellow
make an oval 30x8 color green
convert image /tmp/photo.png width 80 color
```

### Known limitations

- No GIF animations (terminal only); colors depend on the terminal's ANSI support.
- The `"and"` compound-command splitter is word-based, so a color list like `"with color red and blue"` on a single shape is read as a one-part compound command: the second color is dropped.
- The menu animation redraws lines that are already on screen, so it needs an interactive terminal at least 66 columns wide, and it only animates the lines still visible. The whole banner and menu fit in about 24 rows at 69 columns or more (3 menu columns), and about 29 rows at 66 to 68 columns (2 columns). Otherwise the banner is drawn static.
- The browser version refuses any size above 300, so a typo cannot freeze the tab.
- `teach` can only alias a new word to one of the 5 built-in moods, and it cannot create a new mood or a new visual effect.

## Running on Windows

The generator itself is plain Python and runs natively on Windows; only the
`start.sh` and `Makefile` helpers need a Unix shell. Use the `py` launcher
(installed with Python from [python.org](https://www.python.org/downloads/windows/))
in PowerShell or Command Prompt instead:

```powershell
git clone https://github.com/JoaoTomas991/ascii-art-generator.git
cd ascii-art-generator

# optional: image-to-ASCII and FIGlet fonts
py -m pip install -r requirements.txt

py run.py                                   # menu mode
py run.py --intelligent                     # intelligent mode
py run.py "draw a heart size 2 color red"   # direct command
```

Notes:

- If `py` isn't found, use `python` instead (`python run.py ...`).
- Colors and Unicode emojis work best in
  [Windows Terminal](https://aka.ms/terminal) (the default on Windows 11).
  The generator also enables ANSI color support in the classic
  `cmd.exe`/PowerShell console on Windows 10+.
- Words taught with `teach` are saved to
  `%USERPROFILE%\.config\ascii_generator\learned_words.json`.
- For `start.sh` / `make` shortcuts, use WSL or Git Bash, or just run the
  equivalent `py run.py ...` command shown above.

macOS works the same as Linux (`python3 run.py`, `make`, `./start.sh`). For
true-color image output (`convert image ... color`), use a terminal with
24-bit color support such as iTerm2.

## Try it in the browser

The `web/` folder is a static page that runs the real generator inside your
browser through [Pyodide](https://pyodide.org) (Python compiled to WebAssembly).
Type the same English commands, pick an example, or convert an image; nothing
is uploaded anywhere. The first visit downloads about 10 MB of Python runtime.

```bash
make web            # builds _site/ and serves it on http://localhost:8000
```

`make web` (or `python3 scripts/build_web.py --serve`) needs no extra packages.
Open `http://localhost:8000/?cmd=draw+a+heart` to start with a command already
run. After you run a command, the page's "Copy link" button copies a link like
that, so you can share a drawing.

To publish it on GitHub Pages, set **Settings > Pages > Source** to "GitHub
Actions" once. After that `.github/workflows/pages.yml` redeploys the site on
every push to `main` that touches `web/`, the package, the build script or the
workflow itself, and it can also be started by hand from the Actions tab.

## Standalone executables (no Python needed)

A GitHub Actions workflow
([`.github/workflows/build-executables.yml`](.github/workflows/build-executables.yml))
uses [PyInstaller](https://pyinstaller.org/) to build a single-file
executable for Windows, macOS and Linux, with Pillow and the FIGlet fonts
bundled in. Each build is smoke-tested before it's published.

To get a build:

- For a released version, push a tag like `v1.0.0`. That attaches the three
  executables to the tag's page under *Releases*.
- For any commit, open the *Actions* tab, then *Build executables* → *Run
  workflow*. When it finishes, download the executables from the run's
  *Artifacts* section (they come zipped).

To run it:

```powershell
# Windows: double-click for the menu, or from PowerShell / cmd:
.\ascii-art-generator-windows.exe "draw a heart size 2 color red"
```

```bash
# macOS / Linux: mark it executable first
chmod +x ascii-art-generator-linux
./ascii-art-generator-linux "draw a heart size 2 color red"
```

Notes:

- The executables aren't code-signed. Windows SmartScreen or antivirus
  software may warn about them (choose *More info* → *Run anyway*). On
  macOS, run `xattr -d com.apple.quarantine ascii-art-generator-macos` once, or
  allow it under *System Settings → Privacy & Security*.
- The macOS build targets Apple Silicon (M1 and later).
- A single-file build unpacks itself on each launch, so it takes a second
  or two to start.

To build one locally instead (PyInstaller can only target the OS it runs on):

```bash
pip install pyinstaller -r requirements.txt
pyinstaller --onefile --name ascii-art-generator --collect-data pyfiglet run.py
# output: dist/ascii-art-generator (dist\ascii-art-generator.exe on Windows)
```

## Project structure

```
ascii_art_generator/
├── ascii_art.py        # base shapes, fonts, patterns, banners, animations
├── cli.py              # ENCommandParser + command-line interface
├── smart_generator.py  # advanced shapes, fill/border patterns, random generation
├── image_art.py        # image-to-ASCII conversion (the one module that needs Pillow)
├── learned_words.py    # persistence for user-taught mood synonyms
├── animal_scenes.py    # random animal in a coin / frame / scene
├── emoji_art.py        # random emoji face composed from head, eyes, brows, mouth and extras
├── console.py          # UTF-8 stdout setup shared by the entry points
├── install_info.py     # `--version` info and stale installed-copy warning
├── intro.py            # animated startup banner and the live menu animation
├── web_bridge.py       # run_command(): runs a command and returns its output (used by the web page)
└── main.py             # entry point

run.py             # startup script (menu / intelligent / direct command)
web/               # static browser version (index.html, style.css, app.js)
scripts/build_web.py  # builds web/ + the zipped package into _site/
setup.py           # packaging; provides the "ascii-art-generator" command
start.sh           # interactive startup menu (Unix only)
Makefile           # run, test and `make web` shortcuts (Unix only)
requirements.txt   # Pillow (image-to-ASCII) and pyfiglet (FIGlet text fonts), both optional
docs/adr/          # architecture decision records
.github/workflows/ # CI (ci.yml), executables (build-executables.yml), GitHub Pages (pages.yml)
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
these on Windows, Linux, and macOS against Python 3.12, 3.13, and 3.14; see
[`.github/workflows/ci.yml`](.github/workflows/ci.yml).

## License

MIT; see [`LICENSE`](LICENSE).
