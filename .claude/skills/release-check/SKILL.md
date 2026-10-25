---
name: release-check
description: Orchestrates the full audit to run before cutting a release (a v* tag) or publishing the repo — runs generator-tester, shape-coverage-auditor and docs-sync-auditor in parallel, plus pitfall-reviewer on everything since the last release, and merges their reports into one release verdict. Use when the user asks whether main is ready to release, or before tagging.
---

# Release check

The broader counterpart of the `pre-commit` skill: instead of one pending
change, it audits the whole state of the branch being released (normally
`main`). It never tags, pushes or creates a release by itself.

## 1. Pin what's being released

```bash
git fetch origin
git status --short          # must be clean: audit committed code only
git log --oneline -1
git describe --tags --abbrev=0 2>/dev/null || echo "no previous tag"
```

Audit the commit you just printed. If the tree isn't clean, stop and ask
the user whether to commit, stash or audit something else.

Pick the interpreter the same way as in `pre-commit`: if `python3
--version` is older than 3.12, tell every agent to use a 3.12+ one
(`python3.12`, ...) in place of `python3`.

## 2. Launch the agents in parallel

In **one** message, with `run_in_background: false`, launch:

- `generator-tester` — regression battery on the current tree.
- `shape-coverage-auditor` — every declared shape/color/font synonym
  through the real pipeline.
- `docs-sync-auditor` — README/docs/CLAUDE/AGENTS/`ascii-art` skill claims
  against the code.
- `pitfall-reviewer` — the six known bug patterns, on
  `git diff <last-tag>..HEAD -- ascii_art_generator/`. With no previous
  tag there is no meaningful range: skip this agent and say so in the
  report (each PR should already have had it via `pre-commit`).

All four only read the code or run the CLI, so they don't interfere.

## 3. Merge the reports

| Check | Result |
|---|---|
| Regression battery | PASS / FAIL |
| Shape/synonym coverage | dead ends, duplicate keys |
| Docs in sync | drift found |
| Known bug patterns since last tag | PASS / findings / skipped |

Classify every finding:

- **Blocks the release** — battery FAIL, an unreachable shape, a
  pitfall-reviewer finding, or an example command in the docs that
  doesn't work.
- **Doesn't block** — stale counts or wording in the docs that don't
  mislead a user.

Verdict: **ready** only when nothing blocks. Otherwise list the blocking
items with how to reproduce each, and ask the user which to fix before
releasing. Fixes go through the normal flow (a branch, the `pre-commit`
skill, a PR), and the release check is rerun on the result.
