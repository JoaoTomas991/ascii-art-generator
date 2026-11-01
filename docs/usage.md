# Usage

Everything is driven by plain English commands. Install first (see [installation.md](installation.md)),
or use the [browser version](https://joaotomas991.github.io/ascii-art-generator/), which needs no install.

## Three ways to run it

There are three ways to drive the generator, shown below with the installed
`ascii-art-generator` command. Running from a clone without installing is covered in
[installation.md](installation.md#running-without-installing).

### Menu mode (interactive)

```bash
ascii-art-generator
```

Shows an animated banner and a menu with the basic shapes, patterns, text, image conversion, random generators and animations, laid out in up to three columns so it fits on a normal terminal. The other shapes (star, hexagon, oval, arrow, pentagon, butterfly, flower) are reached by typing a command in intelligent mode.

### Intelligent mode (natural language, inside the menu)

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

### Direct command (single line, non-interactive)

```bash
ascii-art-generator "draw a rectangle 10x5"
ascii-art-generator "make a circle with radius 8 color blue"
ascii-art-generator "write HELLO with font banner"
```

## In the browser

Open <https://joaotomas991.github.io/ascii-art-generator/>, type the same commands or click an example, and
convert an image from your computer; nothing is uploaded. **Copy text** copies the drawing as plain text. **Copy for WhatsApp, Telegram…** wraps it in triple backticks, which WhatsApp, Telegram, Discord and Slack show in a monospace font, so the drawing keeps its shape when you paste it; wide drawings can still wrap on a narrow phone screen, and the page tells you when that is likely. After you run a command, **Copy link** copies a URL
like `https://joaotomas991.github.io/ascii-art-generator/?cmd=draw+a+heart` that opens the page with that
command already run. The first visit downloads about 10 MB of Python runtime. For how the page is built and
published, see [development.md](development.md#browser-version).

## What it can do

- Shapes: rectangle, circle, triangle, heart, diamond, spiral, tree, star, hexagon, oval, arrow, pentagon, butterfly, flower
- Text to ASCII: 4 named fonts (`small`, `block`, `banner`, `shadow`), rendered with real FIGlet fonts when pyfiglet is installed, which also accepts any other FIGlet font name (e.g. `write HELLO with font slant`). Without pyfiglet, simpler built-in 5-line fonts are used
- Patterns: gradient, checkerboard, abstract/random art
- Random generators: emojis and animals. A random emoji is a big face composed from a head, eyes, brows, a mouth and extras (13 moods, from happy and wink to angry and sleepy; see `emoji_art.py`), about the size of a big animal. Naming a mood (`draw a sad emoji`) picks a matching face. A random animal is composed as a coin, a framed portrait or a themed scene (meadow, rain, snow, beach, space, forest), e.g. a "$DOG" coin; see `animal_scenes.py`. Naming a specific animal (cat, dog, rabbit, bear, fish, penguin, owl, crow, raven) always draws that animal, while asking for "an animal" or "a creature" picks one of them at random. Add `big`/`large`/`huge`/`giant` for a bigger, more detailed drawing (e.g. `draw a big cat`)
- Banners and boxes with custom text
- Terminal animations: spinner, progress bar, and an animated startup banner whose rainbow keeps moving while the menu waits for your choice
- Browser version: the same generator running on a web page, see [In the browser](#in-the-browser)
- Styling: color (ANSI: red, green, blue, yellow, cyan, magenta, white, black + `bright_*` variants, plus `rainbow`/`multicolor`, which cycles a color per line), up to 32 fill patterns (always applied inside the shape's own silhouette, never replacing it), and several border styles. See [`.claude/skills/ascii-art/SKILL.md`](../.claude/skills/ascii-art/SKILL.md) for the full catalog with functions and files
- Moods (teachable): `happy`, `sad`, `angry`, `calm`, `sleepy`, recognized anywhere in a command and applied as a default color (unless you already gave one explicitly). Teach new synonyms with `teach <word> as <mood>` (e.g. `teach ecstatic as happy`), either in intelligent mode or as a direct one-shot command; taught words persist across sessions in `~/.config/ascii_generator/learned_words.json`. See [`docs/adr/0001-taught-mood-synonyms.md`](adr/0001-taught-mood-synonyms.md) for why this is deliberately a small, taught dictionary rather than automatic word detection or NLP.
- Image to ASCII: `convert image <path> [width N] [color]` converts a real image file (PNG/JPG/...) into ASCII art using a brightness ramp, with an option for true 24-bit color per character (requires Pillow; see [Requirements](installation.md#requirements)).

## Example commands

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

## Known limitations

- No GIF animations (terminal only); colors depend on the terminal's ANSI support.
- The `"and"` compound-command splitter is word-based, so a color list like `"with color red and blue"` on a single shape is read as a one-part compound command: the second color is dropped.
- The menu animation redraws lines that are already on screen, so it needs an interactive terminal at least 66 columns wide, and it only animates the lines still visible. The whole banner and menu fit in about 24 rows at 69 columns or more (3 menu columns), and about 29 rows at 66 to 68 columns (2 columns). Otherwise the banner is drawn static.
- The browser version refuses any size above 300, so a typo cannot freeze the tab.
- `teach` can only alias a new word to one of the 5 built-in moods, and it cannot create a new mood or a new visual effect.
