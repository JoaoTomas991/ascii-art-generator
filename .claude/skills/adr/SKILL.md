---
name: adr
description: Write Architecture Decision Records (ADRs) for significant, hard-to-reverse design decisions in this project (e.g. replacing an algorithm, removing a component, choosing a parsing strategy). Use when a decision like that is made, not for routine bug fixes.
---

# Architecture Decision Records

## When to write one

A decision deserves an ADR when it is:

- **Architectural** — affects how a whole component works or is structured
  (a parsing strategy, which module owns a responsibility, an algorithm
  choice), not a one-line bug fix.
- **Hard to reverse** or **non-obvious** — a future reader (including you,
  in a future session) would otherwise have to reconstruct the "why" from
  git blame.

Routine bug fixes, typos, and doc updates do NOT need an ADR.

## Where they live

`docs/adr/NNNN-short-title.md`, numbered sequentially with 4-digit
zero-padding, kebab-case title. Check `docs/adr/` for the highest existing
number before creating a new one — never reuse or renumber.

Keep `docs/adr/README.md` as a one-line-per-entry index, newest first:
`- [0002](0002-short-title.md) — one-line summary`.

## Template

```markdown
# NNNN. Title

Date: YYYY-MM-DD
Status: Accepted

## Context
What problem or question forced this decision? What was actually happening
(symptom, constraint, prior behavior)?

## Decision
What was chosen, stated as a plain declarative sentence.

## Alternatives considered
Other options and why they were not chosen (even briefly — one line each is
fine).

## Consequences
What this makes easier, what it makes harder, what to watch out for later.
```

`Status` is one of: `Proposed`, `Accepted`, `Deprecated`, `Superseded by
NNNN`. Only write `Accepted` for decisions that have actually been
implemented, not ones still being discussed.

## Style

- One decision per ADR. If a change bundles multiple independent decisions,
  write multiple ADRs.
- Keep it short — a paragraph per section is usually enough. This is a
  decision record, not a design doc.
- Never edit an old ADR's Decision/Context after the fact to reflect new
  information — write a new ADR that supersedes it, and update the old
  one's Status to point at the new one.
