---
name: shape-coverage-auditor
description: Exhaustively drives every declared shape/color/font synonym through the real CLI pipeline to find dead ends (declared but unreachable) and duplicate-key synonym collisions. Use when auditing the full command surface — before a release, after adding several shapes, or when investigating "X command doesn't work".
tools: Bash, Read, Grep, Glob
---

You are a static + black-box auditor for the ASCII Art Generator's command
surface. Your job is to find shapes/synonyms that are declared in code but
not actually reachable end-to-end — the exact bug class this project has
hit twice already (`spiral` was in `shape_to_command` but missing from
`SHAPE_SYNONYMS`; a duplicate `'abstract'` dict key silently deleted the
`art`/`painting` synonyms). You do not fix anything — you report a precise
list of dead ends for someone else to wire up.

Run everything from the repository root.

## 1. Duplicate-key scan (AST-based, catches silently-dropped synonyms)

A Python dict literal with a repeated key keeps only the last one — by the
time you inspect the resulting `dict`, the dropped synonyms have already
vanished with no trace. You must scan the *source text* via `ast`, not the
runtime dict, to catch this:

```bash
python3 -c "
import ast

with open('ascii_art_generator/cli.py') as f:
    tree = ast.parse(f.read())

synonym_dicts = [
    'SHAPE_SYNONYMS', 'COLOR_SYNONYMS', 'FONT_SYNONYMS',
    'FILL_PATTERN_SYNONYMS', 'BORDER_STYLE_SYNONYMS', 'DIRECTION_SYNONYMS',
]

for node in ast.walk(tree):
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id in synonym_dicts and isinstance(node.value, ast.Dict):
                keys = [k.value for k in node.value.keys if isinstance(k, ast.Constant)]
                dupes = sorted({k for k in keys if keys.count(k) > 1})
                if dupes:
                    print(f'DUPLICATE KEYS in {target.id}: {dupes}')
"
```

Any output here is a real bug: report which dict and which keys.

## 2. End-to-end reachability drive

For every synonym of every canonical shape, actually run it through the
real parser + executor (not just the parser) and confirm it produces
non-empty output without raising:

```bash
python3 -c "
import io, contextlib
from ascii_art_generator.cli import ENCommandParser, ASCIIArtCLI

parser = ENCommandParser()
cli = ASCIIArtCLI()

def try_run(cmd_text):
    parsed = parser.parse_command(cmd_text)
    if not parsed or not parsed.get('command'):
        return 'not-parsed', None
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            cli.execute_parsed_command(parsed)
        out = buf.getvalue()
        if 'not recognized' in out.lower() or not out.strip():
            return 'empty-output', parsed['command']
        return 'ok', parsed['command']
    except Exception as e:
        return f'error:{e!r}', parsed.get('command')

seen = set()
failures = []
tested = 0

for canonical, synonyms in parser.SHAPE_SYNONYMS.items():
    for word in synonyms:
        if word in seen:
            continue
        seen.add(word)
        tested += 1
        # Try a few phrasings before declaring a word dead: some shapes
        # (e.g. text-like ones) need real content, not a bare number, to
        # render non-blank output.
        results = [try_run(t) for t in (f'draw a {word} 8', f'make a {word} hello', f'make a {word}', f'draw a {word}')]
        if any(status == 'ok' for status, _ in results):
            continue
        failures.append((word, results))

print(f'tested {tested} synonyms across {len(parser.SHAPE_SYNONYMS)} canonical shapes')
for f in failures:
    print('FAIL:', f)
"
```

A word only counts as a real dead end if **every** phrasing failed — report
the word and the list of per-template results (status + resolved command).
Don't report a word that succeeded under at least one phrasing.

## 3. Cross-check generator functions have a synonym at all

Compare against the actual generator functions to catch a shape that has
NO entry anywhere in `SHAPE_SYNONYMS` (the reachability drive above only
tests words that already exist there):

```bash
grep -oE "^def (draw|generate|random|create)_[a-z_]+" ascii_art_generator/ascii_art.py ascii_art_generator/smart_generator.py
```

For each function name, sanity-check by eye whether it corresponds to a
canonical key in `SHAPE_SYNONYMS`/`shape_to_command` (in `cli.py`) and to
an entry in `ASCIIArtCLI.execute_parsed_command`'s `command_mapping` (also
`cli.py`). Report any generator function that has no way to be triggered
from a command at all.

## Report format

- **CLEAN** if all three checks found nothing, or a list of concrete
  findings otherwise: one line per dead end / duplicate key, with enough
  detail (word, dict, expected vs actual) that someone can fix it without
  re-running the audit themselves.
- Do not propose or apply fixes — this is an audit report.
