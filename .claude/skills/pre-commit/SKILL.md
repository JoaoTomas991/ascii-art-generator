---
name: pre-commit
description: Orchestrates the checks to run before committing or opening a PR that touches ascii_art_generator/*.py — runs the generator-tester and pitfall-reviewer subagents in parallel and merges their reports into one verdict. Use whenever a change to the generator's code is about to be committed.
---

# Pre-commit check

Runs the two per-change subagents together and turns their reports into
one go/no-go verdict. It never commits or pushes by itself — CLAUDE.md
requires the user's explicit authorization for that.

## 1. Decide whether it applies

```bash
git status --short
git diff HEAD --stat -- ascii_art_generator/
```

If nothing under `ascii_art_generator/` changed (docs, skills, CI only),
skip the agents and say so: there is nothing for them to check.

Then pick the interpreter: the project needs Python >= 3.12 (`setup.py`)
and `cli.py` doesn't even import on 3.11. If `python3 --version` is older,
find a 3.12+ one (`python3.12`, `python3.13`, ...) and tell each agent to
use it in place of `python3` (and `make test PYTHON=<it>`); otherwise
every check fails with a SyntaxError that says nothing about the change.

## 2. Launch both agents in parallel

In **one** message, with `run_in_background: false` (the verdict depends
on both), launch:

- `generator-tester` — "Run the regression battery on the current working
  tree and report PASS/FAIL."
- `pitfall-reviewer` — "Review the pending diff (`git diff HEAD --
  ascii_art_generator/`) for the six known bug patterns."

Their checks are independent (one runs the CLI, the other reads the diff),
so running them one after the other only costs time.

## 3. Merge the reports

Report to the user, most important first:

| Check | Result |
|---|---|
| Regression battery (`generator-tester`) | PASS / FAIL + failing checks |
| Known bug patterns (`pitfall-reviewer`) | PASS / findings |

- **Both PASS** → the change is ready to commit; ask the user for
  authorization unless they already gave it for this change.
- **Any FAIL or finding** → do not commit. Fix it (loading
  `generator-core` first), then rerun **both** agents: a fix is a new
  change and can break what passed before.

Keep the final summary short: the table, plus one line per failure or
finding with the command or file:line needed to reproduce it.
