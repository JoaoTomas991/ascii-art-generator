# 0001. Mood vocabulary grows via user-taught synonyms, not NLP

Date: 2026-08-15
Status: Accepted

## Context

Testing intelligent mode with "happy dog" showed that "happy" is silently
ignored: `ENCommandParser` only has closed synonym dictionaries for
shape/color/font/fill/border, with no concept of mood or emotion at all.
The user wanted this fixed, and wanted the vocabulary to "evolve over time
and learn other words" rather than stay a fixed, code-only dictionary
forever.

This is also the project's first need for any on-disk persistence — until
now the app has been fully stateless between runs.

## Decision

Add a small, closed set of built-in moods (happy, sad, angry, calm,
sleepy), each mapped to a default color effect. Grow the vocabulary through
an explicit, single-line command in intelligent mode —
`teach <word> as <mood>` — which can only alias a new word onto one of the
existing built-in moods (it cannot invent a new mood or a new effect).
Taught synonyms are persisted per-user in
`~/.config/ascii_generator/learned_words.json` (via a new, isolated
`ascii_art_generator/learned_words.py`) and reloaded on every future
session.

## Alternatives considered

- **Automatic prompting on any unrecognized word** ("I don't know X, is it
  a mood?"): rejected — risks false positives on typos/unrelated words, and
  would inherit an existing `EOFError` busy-loop bug in
  `run_intelligent_mode`'s `input()` loop (no `except EOFError` today) if
  triggered from piped/non-interactive stdin.
- **Semantic similarity via word embeddings** (e.g. word2vec/GloVe) to guess
  that "ecstatic" ≈ "happy" without being told: rejected — the project is
  stdlib-only by convention (`generator-core` skill), and a model that
  guesses silently would be harder to reason about than the project's
  existing deterministic, lookup-table style.
- **Per-project (repo-committed) storage instead of per-user home
  directory**: rejected per explicit user preference — the vocabulary is
  tied to the person using the tool, not the checkout.

## Consequences

- Easier: the mood feature reuses the existing `color` param /
  `_apply_color` rendering path unchanged; `teach` is simple to test
  manually via piped stdin and to reason about (no hidden guessing).
- Harder: `teach` can only extend existing moods, not create new
  mood/effect pairs — adding a genuinely new mood (and its own visual
  effect) still requires a code change to `MOOD_SYNONYMS`/`MOOD_EFFECTS`.
- Watch out for: this is the first file I/O the project performs outside
  the repo; `learned_words.json` is a small trust boundary (hand-editable)
  and is treated defensively (malformed content is ignored, not raised) on
  load, unlike the rest of the codebase's internal-trust style.
