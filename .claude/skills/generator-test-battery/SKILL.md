---
name: generator-test-battery
description: The ASCII Art Generator's regression test battery — setup check, representative commands, and a smart-mode stress test. Use whenever ascii_art_generator/ascii_art.py, cli.py, smart_generator.py, or main.py has changed, to verify nothing broke.
---

# Generator regression battery

Run everything below from the repository root and note which checks pass or
fail. This skill only defines *what to check* — what to do with a failure
(fix it inline, or just report it) depends on who invoked this skill, not
on the skill itself.

## 1. Setup check

```bash
python3 -c "import ascii_art_generator.cli; import ascii_art_generator.smart_generator; import ascii_art_generator.ascii_art; import ascii_art_generator.main"
```

Must succeed with no output. If it fails, stop — nothing else can be
meaningfully tested until imports work.

```bash
make test
```

Must print "All tests passed!".

## 2. Regression commands

Run each via `python3 run.py "<command>"` and check the property in the
table. A command fails if it crashes (non-zero exit / traceback) or its
output visibly violates the property.

| Command | Must hold |
|---|---|
| `draw a rectangle 10x5` | 5 rows of `#`, each 10 chars wide |
| `make a circle with radius 8 color blue` | renders a circle, ANSI blue color codes present |
| `draw a heart size 2` | renders a heart, no crash |
| `write HELLO` | output spells HELLO in block letters — no leaked words like "WITH" or "FONT" |
| `write HELLO with font banner` | same as above — must NOT render a banner box with the default "ASCII" text (that would mean the font name collided with the shape parser again) |
| `make a rectangle 8x4 with color cyan style dotted` | output must be a dotted pattern (alternating `#`/space), not a solid block (that would mean "style" leaked to the wrong param again) |
| `make a spiral 20` | must NOT be a solid block of one repeated character on every row — rows should differ from each other and contain blank runs (a real spiral has gaps) |
| `make an emoji` | output must be a composed ASCII face about as tall as a big animal (around 11 lines, with a round head outline and eyes/mouth inside), not a one-line kaomoji; `draw a sad emoji` must give a sad face (brows `__/` and `\__`) |
| `make a banner with text COOL` | the word COOL must appear in the rendered banner, not the default "ASCII" |
| `create a box with text HI` | the word HI must appear in the box |
| `make a circle with radius 5 color blue and a rectangle 10x5 color red` | output must contain TWO distinct shapes (a circle-like block AND a 10x5 rectangle block), each with its own color — if only one shape appears, compound-command support is broken |
| `draw a heart and a diamond and a star` | output must contain three distinct shapes |

## 3. Smart-mode stress test

Run this exact script and check for any traceback, any `type(art) != list`,
or any line containing an embedded newline:

```bash
python3 -c "
from ascii_art_generator.smart_generator import smart_gen
cmds = ['surprise me', 'make something interesting', 'create a geometric design', 'generate a nature scene', 'make something minimal', 'create a complex pattern', 'draw something abstract']
errors = corrupted = 0
for _ in range(100):
    for cmd in cmds:
        try:
            art = smart_gen.generate_from_command(cmd)
            if not isinstance(art, list) or any(not isinstance(l, str) for l in art):
                corrupted += 1; print('BAD TYPE', cmd, type(art))
            elif any(chr(10) in l for l in art):
                corrupted += 1; print('EMBEDDED NEWLINE', cmd)
        except Exception as e:
            errors += 1; print('ERROR', cmd, repr(e))
print('done. errors=', errors, 'corrupted=', corrupted)
"
```

`errors` and `corrupted` must both be `0`.

## Interpreting results

For each check above: **PASS** if the described property holds, **FAIL**
otherwise (crash, non-zero exit, or output that visibly violates the
property). This skill stops at reporting pass/fail per check — whether to
fix a failure now or hand it off is the invoking agent's call, not this
skill's.
