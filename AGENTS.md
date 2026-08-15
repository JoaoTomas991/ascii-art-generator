# AGENTS.md

Instructions for coding agents (Codex, Cursor, Copilot, Claude Code, etc.) working in this repository. For Claude Code-specific conventions, see [CLAUDE.md](CLAUDE.md); for the full catalog of shapes/fonts/colors/styles, see [.claude/skills/ascii-art/SKILL.md](.claude/skills/ascii-art/SKILL.md).

## Overview

A Python ASCII Art generator: geometric shapes, text converted into ASCII letters, patterns, and terminal animations, driven by natural-language English commands (`ENCommandParser`) or an interactive menu.

## Environment

- Python 3.10+
- No external dependencies (standard library only) — no `requirements.txt`, `setup.py`, or `pyproject.toml`
- Nothing to install; run directly with `python3`

## Running

```bash
python3 run.py                              # interactive menu
python3 run.py --intelligent                # intelligent mode (natural language)
python3 run.py "draw a rectangle 10x5"       # direct command, non-interactive
```

See [README.md](README.md) for all modes and examples.

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
└── main.py             # entry point
```

- **Base** shapes/patterns live in `ascii_art.py`; **advanced** shapes/patterns (star, hexagon, oval, arrow, pentagon, butterfly, flower, the 31 fill patterns, the 12 rich border styles) live in `smart_generator.py`.
- `ENCommandParser` in `cli.py` is the **only** command parser used by the app (`ASCIIArtCLI.__init__` instantiates it directly). Don't build an alternative parser without actually wiring it into the CLI — the project used to carry a dead `PTCommandParser` (never instantiated) that was removed for exactly that reason.

## Code conventions

- No external dependencies — don't add third-party libraries without a clear reason.
- Generator functions return `str` (or `List[str]`) instead of printing directly, except the animations (`spinner_animation`, `progress_bar`), which are blocking and write to stdout.
- Command synonyms (shapes, colors, fonts, fill patterns, borders) are centralized in `ENCommandParser`'s `*_SYNONYMS` dicts, with a reverse `*_to_key` lookup table built in `__init__`.
- When adding a new shape/style: implement the generator function, register synonyms in `ENCommandParser.SHAPE_SYNONYMS`, map it in `shape_to_command`, test with a real command, and update the `ascii-art` skill.

## Known limitations (do not fix without an explicit request)

- `ENCommandParser` **does not support compound commands** — `"a circle ... and a rectangle ..."` only draws the first shape; tokens from the second part leak into the first shape's parameters.
- `"write TEXT with font X"` is fragile: if `X` matches the name of a shape (e.g. `banner`), the command is interpreted as creating that shape instead; even without a collision, the suffix can get absorbed into the converted text.
- `"style X"` maps to `font`, not `fill` — use `fill X` to request a fill pattern.

## Safety and changes

- Never delete files, commit, or push without the user's explicit authorization.
- Always test with a real command (`python3 run.py "..."` or `make test`) before considering a change complete.
