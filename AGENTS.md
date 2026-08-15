# AGENTS.md

Instructions for coding agents (Codex, Cursor, Copilot, Claude Code, etc.) working in this repository. For Claude Code-specific conventions, see [CLAUDE.md](CLAUDE.md); for the full catalog of shapes/fonts/colors/styles, see [.claude/skills/ascii-art/SKILL.md](.claude/skills/ascii-art/SKILL.md).

Claude Code users also have: [.claude/skills/generator-core/SKILL.md](.claude/skills/generator-core/SKILL.md) (conventions/pitfalls before editing core code), [.claude/skills/generator-test-battery/SKILL.md](.claude/skills/generator-test-battery/SKILL.md) (the regression battery itself — what to check after any change to `ascii_art_generator/*.py`), the [generator-tester](.claude/agents/generator-tester.md) subagent (runs that same battery in an isolated context and reports pass/fail), and [.claude/skills/adr/SKILL.md](.claude/skills/adr/SKILL.md) (how to record significant architecture decisions in `docs/adr/`).

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
- Generator functions are inconsistent about return type: most `ascii_art.py` functions return a single `'\n'`-joined `str`, while `smart_generator.py`'s own shape functions (`draw_star`, `draw_hexagon`, ...) return `List[str]`. Anything in `smart_generator.py` that consumes a shape function's output must call `_normalize_lines(art)` first — iterating a `str` yields characters, not lines, which silently corrupts art into one character per line. This bit us once already; don't reintroduce it.
- Command synonyms (shapes, colors, fonts, fill patterns, borders) are centralized in `ENCommandParser`'s `*_SYNONYMS` dicts, with a reverse `*_to_key` lookup table built in `__init__`. A word used as a synonym in more than one dict key will silently lose earlier entries (Python dict literals don't merge duplicate keys) — grep for the word across `SHAPE_SYNONYMS` before adding it.
- When adding a new shape/style: implement the generator function, register synonyms in `ENCommandParser.SHAPE_SYNONYMS`, map it in `shape_to_command`, test with a real command, and update the `ascii-art` skill.
- Compound commands (`"a circle ... and a rectangle ..."`) are split by `_split_compound_command` and parsed per-part by `_parse_single_command` — always extract numbers/params from the individual part, never from the full original command string, or values will leak between shapes.

## Known limitations

- The `"and"` compound-command splitter is word-based: a color list on a single shape (`"with color red and blue"`) can be misread as two shapes, since there's no quoting to disambiguate.

## Safety and changes

- Never delete files, commit, or push without the user's explicit authorization.
- Always test with a real command (`python3 run.py "..."` or `make test`) before considering a change complete.
