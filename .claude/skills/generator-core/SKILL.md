---
name: generator-core
description: Conventions and known pitfalls for changing the ASCII Generator's core code (ascii_art_generator/ascii_art.py, cli.py, smart_generator.py, main.py). Load before adding or editing a shape, pattern, or the ENCommandParser.
---

# Generator core — conventions & pitfalls

This project has no automated test suite, and its history includes several
subtle bugs caused by the same two or three mistakes. Read this before
touching `ascii_art_generator/`.

## Architecture

- `ascii_art.py` — base shapes/fonts/patterns/banners/animations. Most
  functions return a single `'\n'`-joined `str`.
- `smart_generator.py` — advanced shapes (star, hexagon, oval, arrow,
  pentagon, butterfly, flower), 31 fill patterns, 12 border styles, and
  `smart_gen` random generation. Its own shape functions return `List[str]`.
- `cli.py` — `ENCommandParser` (the ONLY command parser wired into the app —
  `ASCIIArtCLI.__init__` instantiates it directly) plus `ASCIIArtCLI`/`Menu`.

## The #1 pitfall: `str` vs `List[str]`

`ascii_art.py` functions return `str`; `smart_generator.py` functions return
`List[str]`. Anything in `smart_generator.py` that consumes a shape
function's output (fill/border/color application, `_generate_shape`,
`_generate_advanced_shape`, `_generate_random_pattern`,
`_generate_combination_art`, ...) MUST call `_normalize_lines(art)` right
after invoking the shape function, before treating the result as a list of
lines. Iterating a `str` yields characters, not lines — this silently
corrupts output into one character per line, and was the root cause of a
real bug where every `smart`/`surprise`/`geometric`/`nature` command was
broken.

## Editing `ENCommandParser` (cli.py)

- `SHAPE_SYNONYMS` is a plain dict literal — a duplicate key silently
  **replaces** the earlier one instead of merging. Grep for a word across
  the whole dict before adding it as a new synonym.
- Compound commands (`"X and Y"`) go through `_split_compound_command` →
  `_parse_single_command` per part. Always derive numbers/params from the
  individual part string, never from the original full command — mixing
  them was the root cause of a real "second shape steals the first shape's
  number" bug.
- `shape_to_command` maps the canonical shape key to the `command` name used
  by `ASCIIArtCLI.execute_parsed_command`'s `command_mapping`. If you add a
  shape, both dicts need an entry, and `command_mapping`/`render_shape` in
  `cli.py` needs to know how to call its generator function (positional
  args, in the exact order the function expects).
- The "Build params with numbers" block in `_parse_single_command` decides
  which `final_params` key (`width`/`height`, `radius`, or `size`) a bare
  number goes into, based on `command_name`. This key MUST match what
  `execute_parsed_command`'s `command_mapping` reads via `params.get(...)`
  for that shape, or the number is silently dropped (this happened to
  `spiral`: numbers were stored under `radius` but read from `size`).

## Adding a new shape/style — checklist

1. Implement the generator function in `ascii_art.py` (base) or
   `smart_generator.py` (advanced/pattern). Pick `str` vs `List[str]`
   consistent with that file's existing convention, and normalize at every
   call site per the pitfall above.
2. Register synonyms in `ENCommandParser.SHAPE_SYNONYMS`.
3. Map the canonical key in `shape_to_command`; add/adjust the
   number→param-key logic in the "Build params with numbers" block.
4. Wire it into `ASCIIArtCLI.execute_parsed_command`'s `command_mapping`
   (and `render_shape`'s `shape_func` dict, if it's a plain shape).
5. Update `.claude/skills/ascii-art/SKILL.md` with the new entry.
6. **Run the `generator-test-battery`** before considering the change
   done — this project has no automated test suite, so it's the only
   regression safety net against the pitfalls above. Either invoke the
   `generator-test-battery` skill directly (inline, if you want to fix
   anything it finds yourself) or delegate to the `generator-tester`
   subagent (isolated context, returns a plain pass/fail report — use this
   when you just want confirmation without spending main-conversation
   context on the run).
7. Before committing, consider the other audit subagents: `pitfall-reviewer`
   (reviews the diff for this project's 5 recurring bug patterns — cheap,
   worth running on most changes), `shape-coverage-auditor` (exhaustive
   reachability sweep across every synonym — worth it after adding several
   shapes or before a release), and `docs-sync-auditor` (catches drift
   between the docs and the code — worth it before publishing).

## No external dependencies

Standard library only. Don't add a third-party package without a clear,
explicit reason.
