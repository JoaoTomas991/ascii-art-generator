# 0005. Random emoji is a composed face, as big as a big animal

Date: 2026-10-05
Status: Accepted

## Context

`random_emoji()` picked one of 15 hand-typed one-line kaomoji such as
`(^_^)` or `(≧▽≦)`. Next to `random animal`, which draws an 11-line composed
scene, it looked tiny and repetitive. Many of the kaomoji also used
non-ASCII characters, which is why `console.py` has to set up UTF-8 output.

The request was for a random emoji with the same default size as the random
animal, and somewhat better looking.

## Decision

A new module, `ascii_art_generator/emoji_art.py`, composes a face from a
round head (21 columns by 11 rows) plus eyes, brows, a mouth and optional
extras such as hearts, tears, `zZ` or sparkles. It is plain ASCII and has no
dependency on the other modules, like `animal_scenes.py`.

- Each of 13 face moods (happy, laugh, wink, sad, angry, surprised, cool,
  love, sleepy, calm, dizzy, starstruck, silly) lists the eyes, brows,
  mouths and extras that fit it. A random face picks a mood first and the
  parts second, so the expression is always coherent.
- `random_emoji(big=True)` returns the composed face by default.
  `random_emoji(big=False)` keeps the old one-line kaomoji, which the menu
  showcase still uses.
- The parser's moods (happy, sad, angry, calm, sleepy) map to face moods
  through `MOOD_FACES`, so `draw a sad emoji` gives a sad face. A face
  without a mood gets a color that suits it.
- The face is drawn on its own, without a coin, frame or scene. At 11 lines
  it is already about as tall as a big animal drawing.

## Alternatives considered

- Drawing a dozen complete faces by hand would give no more variety than the
  old list, and each new expression would need another full drawing.
- Choosing eyes, brows and mouth independently at random would produce
  contradictory faces, such as angry brows over a wide smile.
- Using real Unicode emoji characters would depend on the terminal's font and
  would not keep the project's ASCII-art look.

## Consequences

- `random_emoji()` now returns an 11-line string instead of one line. Code
  that expects a single line has to pass `big=False`.
- Adding an expression means adding parts to `emoji_art.py`, not drawing a
  whole face. The regression battery now expects a composed face for
  `make an emoji` instead of a non-ASCII kaomoji.
- The five parser moods are listed twice: in `MOOD_SYNONYMS` in `cli.py` and
  in `MOOD_FACES`. A mood added to the parser but not to `MOOD_FACES` gets a
  random face, because `_random_emoji` ignores moods it does not know.
  `emoji_face()` itself raises `ValueError` for an unknown mood name.
- When the command names a mood, the parser's color for that mood wins over
  the color suggested by `emoji_color`. The suggestion only applies to
  commands without a mood and to the menu.
