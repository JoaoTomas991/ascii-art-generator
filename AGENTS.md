# AGENTS.md

Instructions for coding agents (Codex, Cursor, Copilot, Claude Code, etc.) working in this repository. For Claude Code-specific conventions, see [CLAUDE.md](CLAUDE.md); for the full catalog of shapes/fonts/colors/styles, see [.claude/skills/ascii-art/SKILL.md](.claude/skills/ascii-art/SKILL.md).

Claude Code users also have: [.claude/skills/generator-core/SKILL.md](.claude/skills/generator-core/SKILL.md) (conventions/pitfalls before editing core code), [.claude/skills/generator-test-battery/SKILL.md](.claude/skills/generator-test-battery/SKILL.md) (the regression battery itself — what to check after any change to `ascii_art_generator/*.py`), [.claude/skills/adr/SKILL.md](.claude/skills/adr/SKILL.md) (how to record significant architecture decisions in `docs/adr/`), and two orchestration skills that run the subagents below in parallel and merge their reports: [.claude/skills/pre-commit/SKILL.md](.claude/skills/pre-commit/SKILL.md) (`generator-tester` + `pitfall-reviewer`, before committing a change to `ascii_art_generator/*.py`) and [.claude/skills/release-check/SKILL.md](.claude/skills/release-check/SKILL.md) (all four subagents, before a release).

Four subagents in `.claude/agents/`: [generator-tester](.claude/agents/generator-tester.md) (runs the battery above in an isolated context, reports pass/fail — invoke after any change to `ascii_art_generator/*.py`), [shape-coverage-auditor](.claude/agents/shape-coverage-auditor.md) (exhaustively drives every declared shape/color/font synonym through the real pipeline to find dead ends and duplicate synonym keys — use before a release or after adding several shapes), [docs-sync-auditor](.claude/agents/docs-sync-auditor.md) (cross-checks README/CLAUDE/AGENTS/ascii-art skill claims against the actual code — use before publishing the repo), and [pitfall-reviewer](.claude/agents/pitfall-reviewer.md) (specialized review for this codebase's 6 recurring bug patterns — use before committing a change to `ascii_art_generator/*.py`).

## Overview

A Python ASCII Art generator: geometric shapes, text converted into ASCII letters, patterns, and terminal animations, driven by natural-language English commands (`ENCommandParser`) or an interactive menu.

## Environment

- Python 3.12+ (`setup.py` requires it; `cli.py` uses a backslash inside an f-string expression)
- Standard library only, with one deliberate exception: `ascii_art_generator/image_art.py`
  (image-to-ASCII conversion, `convert image ...`) needs Pillow, declared in
  `requirements.txt` (`pip install -r requirements.txt` or `make install`) and
  as the `images` extra in `setup.py` (`pip install -e ".[images]"`; `".[all]"`
  adds pyfiglet).
- Optional: pyfiglet, used by `text_to_ascii()` in `ascii_art.py` for FIGlet
  fonts (deferred import; falls back to the built-in fonts when missing).
- Everything else needs nothing installed; run directly with `python3`.

## Running

```bash
python3 run.py                              # interactive menu
python3 run.py --intelligent                # intelligent mode (natural language)
python3 run.py --version                    # which code is running (editable / installed copy / checkout, git branch)
python3 run.py "draw a rectangle 10x5"       # direct command, non-interactive
python3 run.py --no-animation               # skip the animated banner (or ASCII_GENERATOR_NO_ANIMATION=1, or TERM=dumb)
make web                                    # build the browser version into _site/ and serve it on :8000
```

The banner and menu animation (`intro.py`) only run on an interactive terminal; piped output gets a static banner. The browser version (`web/`) runs the same package through Pyodide: `scripts/build_web.py` zips the package next to the page, and `web_bridge.run_command()` is the only entry point the page calls.

See [README.md](README.md) for an overview and [docs/usage.md](docs/usage.md) for all modes and examples.

## Testing

```bash
make test
```

Runs a smoke test against the main imports (`ascii_art.py`) and the command parser (`ENCommandParser`). There is no automated test suite (pytest/unittest) — when changing behavior, always validate with real commands via `python3 run.py "..."` before considering the work done.

## Code structure

```
ascii_art_generator/
├── ascii_art.py        # base shapes, fonts, patterns, banners, animations
├── cli.py              # ENCommandParser + command-line interface (ASCIIArtCLI, Menu)
├── smart_generator.py  # advanced shapes, fill/border patterns, random generation
├── animal_scenes.py    # random animal composed as a coin / frame / themed scene
├── emoji_art.py        # random emoji face composed from head, eyes, brows, mouth and extras
├── image_art.py        # image-to-ASCII conversion (the one module that needs Pillow)
├── learned_words.py    # persistence for user-taught mood synonyms
├── console.py          # UTF-8 stdout setup shared by the entry points
├── install_info.py     # `--version` info and stale installed-copy warning
├── intro.py            # animated startup banner + LiveLines (keeps menu lines animating while input() waits)
├── web_bridge.py       # run_command(): runs a command, returns its output as text (used by the web page)
└── main.py             # menu entry point (the packaged `ascii-art-generator` command is `run.py:main`)

web/                    # static browser version: index.html, style.css, app.js (runs the package in Pyodide)
scripts/build_web.py    # builds web/ + the zipped package into _site/ (`make web`, .github/workflows/pages.yml)
```

- **Base** shapes/patterns live in `ascii_art.py`; **advanced** shapes/patterns (star, hexagon, oval, arrow, pentagon, butterfly, flower, the 32 fill patterns, the 12 rich border styles) live in `smart_generator.py`.
- `ENCommandParser` in `cli.py` is the **only** command parser used by the app (`ASCIIArtCLI.__init__` instantiates it directly). Don't build an alternative parser without actually wiring it into the CLI — the project used to carry a dead `PTCommandParser` (never instantiated) that was removed for exactly that reason.

## Code conventions

- No external dependencies, with two deliberate, documented exceptions:
  `image_art.py`/Pillow and the optional pyfiglet import in `text_to_ascii()`
  (see Environment above and `docs/adr/0002-figlet-fonts-via-pyfiglet.md`).
  Don't add another third-party library without an equally clear, explicit
  reason. The browser page loads Pyodide (and installs Pillow and pyfiglet
  inside it) from a CDN at runtime; that is not a Python dependency of the
  package, which stays standard-library only.
- `intro.py` and `web_bridge.py` are standard library only too. `LiveLines`
  redraws printed lines by cursor offset (ESC 7/8 + cursor-up), so it assumes
  no printed line wraps; it switches itself off when the terminal is narrower
  than the widest line. Keep that assumption if you change the menu layout.
- Shape functions take their size from the command's bare number: the parser
  stores it as `height` for `triangle`/`tree`, `width`+`height` for `oval` and
  `rectangle`, `radius` for `circle` and `size` for everything else. The key
  must match what `execute_parsed_command` reads (see the pitfall list).
- Generator functions are inconsistent about return type: most `ascii_art.py` functions return a single `'\n'`-joined `str`, while `smart_generator.py`'s own shape functions (`draw_star`, `draw_hexagon`, ...) return `List[str]`. Anything in `smart_generator.py` that consumes a shape function's output must call `_normalize_lines(art)` first — iterating a `str` yields characters, not lines, which silently corrupts art into one character per line. This bit us once already; don't reintroduce it.
- Command synonyms (shapes, colors, fonts, fill patterns, borders) are centralized in `ENCommandParser`'s `*_SYNONYMS` dicts, with a reverse `*_to_key` lookup table built in `__init__`. A word used as a synonym in more than one dict key will silently lose earlier entries (Python dict literals don't merge duplicate keys) — grep for the word across `SHAPE_SYNONYMS` before adding it.
- When adding a new shape/style: implement the generator function, register synonyms in `ENCommandParser.SHAPE_SYNONYMS`, map it in `shape_to_command`, test with a real command, and update the `ascii-art` skill.
- Compound commands (`"a circle ... and a rectangle ..."`) are split by `_split_compound_command` and parsed per-part by `_parse_single_command` — always extract numbers/params from the individual part, never from the full original command string, or values will leak between shapes.

## Known limitations

- The `"and"` compound-command splitter is word-based: a color list on a single shape (`"with color red and blue"`) is read as a compound command with one part: the first color is applied, the second is silently dropped and a spurious `[1/1]` header is printed.

## Safety and changes

- Never delete files, commit, or push without the user's explicit authorization.
- Always test with a real command (`python3 run.py "..."` or `make test`) before considering a change complete.
