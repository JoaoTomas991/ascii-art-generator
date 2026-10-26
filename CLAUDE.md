# ASCII Art Generator - Agent Configuration

## Project Overview
An ASCII art generator that creates art from text, geometric shapes and patterns. The CLI understands natural-language commands in **English** (through `ENCommandParser`).

## General Behavior
- **Language**: everything in this repository is written in English: code, comments, documentation, commit messages and agent instructions. The CLI commands are English too (see above)
- **Tone**: technical, direct and friendly (no emojis)
- **Style**: minimal, focused, well-tested solutions
- **Safety**: never run destructive code, delete files, or commit/push without explicit authorization

## Code Structure
- `ascii_art_generator/ascii_art.py` — shape, text and pattern generation
- `ascii_art_generator/cli.py` — command-line interface and `ENCommandParser` (English natural-language parsing)
- `ascii_art_generator/smart_generator.py` — advanced shapes, fill/border patterns, "smart"/random generation
- `ascii_art_generator/image_art.py` — conversion of a real image (PNG/JPG/...) to ASCII with a brightness ramp; third-party dependency Pillow (see `requirements.txt`); the other optional dependency is `pyfiglet`, imported only inside `text_to_ascii()` in `ascii_art.py`
- `ascii_art_generator/animal_scenes.py` — random animal on a coin, in a frame or in a themed scene
- `ascii_art_generator/emoji_art.py` — large emoji face composed of a head, eyes, brows, a mouth and extras
- `ascii_art_generator/learned_words.py` — persistence of the taught mood synonyms (`teach`)
- `ascii_art_generator/console.py` / `install_info.py` — UTF-8 on stdout; `--version` and the warning about a stale installed copy
- `ascii_art_generator/intro.py` — animated startup banner (`show_intro`, `banner_lines`) and `LiveLines`, the thread that keeps animating lines that are already printed while the menu waits on `input()`; standard library only
- `ascii_art_generator/web_bridge.py` — `run_command(text)`: runs a command and returns what it prints (with ANSI) as a `str`; used by the web version
- `ascii_art_generator/main.py` — entry point
- `run.py` / `start.sh` — startup scripts (`run.py --no-animation` turns the animation off)
- `web/` + `scripts/build_web.py` — static browser version (Pyodide); `make web` builds `_site/` and serves it on `localhost:8000`; `.github/workflows/pages.yml` publishes it to GitHub Pages

## Project Skills and Subagents
- `.claude/skills/ascii-art/SKILL.md` — full catalog of shapes/fonts/colors/styles
- `.claude/skills/generator-core/SKILL.md` — conventions and pitfalls when editing `ascii_art_generator/*.py` (read it before touching the core)
- `.claude/skills/generator-test-battery/SKILL.md` — the regression test battery itself (what to test); can be invoked inline or through the subagent below
- `.claude/agents/generator-tester.md` — thin subagent that invokes the skill above in an isolated context and returns only a PASS/FAIL report; always invoke it after changing `ascii_art.py`, `cli.py`, `smart_generator.py`, `intro.py`, `web_bridge.py` or `main.py`
- `.claude/agents/shape-coverage-auditor.md` — subagent that exhaustively tests every declared synonym (all shapes/colors/fonts) against the real pipeline, to catch dead or unreachable shapes and duplicate keys in the synonym dictionaries. Use it before a release or after adding several shapes.
- `.claude/agents/docs-sync-auditor.md` — subagent that compares the claims in README/docs/CLAUDE/AGENTS/the `ascii-art` skill (counts, lists, examples, limitations) against the real code and reports drift. Use it before publishing the repository or cutting a release.
- `.claude/agents/pitfall-reviewer.md` — review subagent specialized in the 6 bug patterns already seen in this project (`str`/`List[str]` mismatch, duplicate keys, argument mismatch, parameter-key mismatch, off-by-one in text capture, data dictionaries duplicated across files). Invoke it before a commit/PR that touches `ascii_art_generator/*.py`.
- `.claude/skills/adr/SKILL.md` — how to document significant architecture decisions in `docs/adr/`
- `.claude/skills/pre-commit/SKILL.md` — runs `generator-tester` + `pitfall-reviewer` in parallel and merges the reports into one verdict; use it before a commit/PR that touches `ascii_art_generator/*.py`
- `.claude/skills/release-check/SKILL.md` — runs `generator-tester`, `shape-coverage-auditor`, `docs-sync-auditor` (and `pitfall-reviewer` since the last tag) in parallel; use it before a release (`v*` tag) or before publishing the repository
- `.claude/skills/humanizer/SKILL.md` — third-party skill (MIT, see `THIRD_PARTY_NOTICES.md`) that removes common signs of AI writing from prose; use it when writing or reviewing the README, the changelog, release notes and other text meant for readers
- `.claude/skills/architecture-diagram/SKILL.md` — third-party skill (MIT, see `THIRD_PARTY_NOTICES.md`) that produces architecture diagrams as self-contained HTML with inline SVG; GitHub does not render HTML in Markdown, so export a diagram as SVG or PNG into `docs/images/` before linking it from a document

## Project Capabilities
The project supports:
- **Geometric shapes**: rectangle, circle, triangle, heart, diamond, spiral, tree, star (5 points), hexagon, oval, arrow, pentagon, butterfly, flower. A bare number in the command sets the shape size (`draw a star 8`, `draw a triangle 5`); the oval accepts `30x8`
- **Text to ASCII**: text conversion with several fonts (small, block, banner, shadow), plus the alias `solid`, pyfiglet's `banner` font, used for the logo. Rendered with real FIGlet fonts through `pyfiglet` (optional; it also accepts any other FIGlet font name, e.g. `slant`), with a fallback to the built-in 5-line fonts when pyfiglet is not installed
- **Patterns**: gradient, checkerboard, random, abstract
- **Animations**: spinner, progress bar
- **Banners and boxes**: with custom text
- **Styles**:
  - **Colors**: red, green, blue, yellow, cyan, magenta, white, black (and the `bright_*`/`light_*` variants), plus `rainbow`/`multicolor` (cycles one color per line)
  - **Fill**: solid, empty, dotted, striped, crosshatch, checkerboard, gradient (a real density ramp, not binary), random, among others (32 patterns in `smart_generator.py`, including `dense_gradient`, which uses only the heavy half of the ramp). Always applied only inside the shape's silhouette (`mask_fill_pattern`), never replacing it with a rectangle
  - **Borders**: simple, double, dashed, wavy, bold, light, fancy, rounded, among others (12 in `smart_generator.py`); all of them keep the shape's content and the frame is as wide as the lines. The `empty` fill draws the silhouette's outline, not the box rectangle
- **Moods**: happy, sad, angry, calm, sleepy. Each applies a default color (unless the user already gave a `color`). New synonyms can be taught at runtime in intelligent mode with `teach <word> as <mood>`, and they persist between sessions in `~/.config/ascii_generator/learned_words.json`
- **Animated banner and menu**: the menu is a banner (the `ASCII` logo in a heavy font with thin strokes stretched horizontally, and the subtitle `A R T   G E N E R A T O R`) plus the categories in up to 3 columns; the logo, the subtitle and the `━` line above the prompt animate in rainbow colors while the menu waits. The animation only runs in an interactive terminal and is turned off with `--no-animation`, `ASCII_GENERATOR_NO_ANIMATION=1` or `TERM=dumb`; in terminals narrower than 66 columns it stays static, and it only animates the lines that are still visible (banner and menu fit in about 24 lines at 69 columns or more, and in about 29 lines at 66 to 68 columns, where the menu drops to 2 columns)
- **Web version**: `web/` runs the real generator in the browser with Pyodide (no server); `make web` to try it locally; `?cmd=` in the URL runs a command on open; sizes above 300 are refused so the tab does not freeze
- **Image to ASCII**: `convert image <path> [width N] [color] [invert] [auto] [dither] [contrast N] [gamma N] [ramp NAME] [edges] [crop L T W H]` converts a real image file (PNG/JPG/...) into a brightness-ramp ASCII picture, with an option for true 24-bit color per character (`ascii_art_generator/image_art.py`, needs Pillow: `pip install -r requirements.txt`)

See the `ascii-art` skill (`.claude/skills/ascii-art/SKILL.md`) for the full catalog with functions, files and signatures.

## Standard Workflow
1. Analyze the user's command
2. Extract the shape/text and the parameters
3. Run it with the extracted parameters
4. Show the result with suitable formatting
5. Always test after implementing changes

## Valid Command Examples
```
draw a rectangle 10x5
make a circle with radius 8
draw a heart size 2
write HELLO
make a rectangle 8x4 with color cyan
make a rectangle 8x4 with color cyan style dotted
make a spiral 20
make an emoji
make a circle with radius 5 color blue and a rectangle 10x5 color red
teach ecstatic as happy
draw an ecstatic heart
draw a heart size 4 color rainbow
draw a star 8 color yellow
make an oval 30x8 color green
draw a big cat color yellow
convert image /tmp/photo.png width 80 color
```

## Known Limitations
- No GIF animations (terminal only)
- Colors depend on the terminal's ANSI support
- Without `pyfiglet` installed, fonts are limited to the built-in definitions (small, block, banner, shadow: only A-Z and some punctuation; missing characters appear as `?`)
- The menu animation relies on the relative position of the lines already printed: if the user types a line longer than the terminal at the prompt, the text wraps and the animation may draw a line in the wrong place until Enter
- The compound-command separator (`"and"`) is word-based: a color list on a single shape (`"with color red and blue"`) can be wrongly read as two shapes
