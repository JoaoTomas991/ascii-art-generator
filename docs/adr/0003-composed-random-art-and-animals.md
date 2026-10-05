# 0003. Random generators compose art instead of picking fixed drawings or noise

Date: 2026-10-05
Status: Accepted

## Context

The "random" generators were not interesting:

- `random_abstract()` filled a grid with characters drawn independently from
  a 16-symbol set. It was pure noise with no shape or structure to
  recognise, and every run looked the same as the last.
- `random_animal()` picked one of 9 fixed drawings, so it repeated itself
  quickly.
- `random_face()` produced three-character kaomoji and overlapped with
  `random_emoji()`, which does the same job better.
- Intelligent mode already had `SmartGenerator.generate_interesting_art()`
  with several structured styles, but it never used animals at all
  (`random_animal` was imported and unused), so the two features were
  disconnected.

The wish was for results closer to a "dog coin": a recognisable animal in a
setting that gives it character.

## Decision

Random art and random animals are produced by composing existing pieces, not
by sampling characters or picking one drawing:

- `random_face()` and `random_abstract()` are removed. `random art`, `art`
  and `painting` call `smart_gen.generate_interesting_art('random', w, h)`
  through `ASCIIArtCLI._random_art()`.
- A new module, `ascii_art_generator/animal_scenes.py`, composes an animal
  drawing with a setting: a coin (`$DOG`), a framed portrait, or a themed
  scene (meadow, rain, snow, beach, space, forest) with its own sky,
  weather, scenery and ground. Each setting adds random decoration and a
  matching color.
- `random animal` / `draw an animal`, the menu item and the `nature` and
  `random` styles of the smart generator all use it
  (`SmartGenerator.generate_animal_art()`).
- Composed animals use the large drawing by default (`big=True`): more
  characters means more room for detail. Animals requested by name keep
  their existing small default.
- In the parser, `random` is an adjective when a later token names an animal
  or emoji, so `a random animal` is not swallowed by plain random art.
  `art` and `painting` map to `random_art`; `abstract`, `pattern` and
  `design` stay on the smart generator's `abstract` style.

## Alternatives considered

- Keeping `random_abstract` and improving the noise (smoothing, symmetry)
  would still leave it without a subject, and it duplicates what the smart
  generator already does.
- Adding more fixed animal drawings only would raise variety slowly, one
  hand-drawn animal at a time. The repetition comes from the lack of
  composition, not just from the number of animals.
- Putting the composition inside `smart_generator.py`, where `apply_border`
  and friends live, was rejected because the module is already large. A
  separate module with no dependency on it also avoids a circular import.
- Honoring `WxH` strictly for `random art` was not done. The generator
  chooses shapes and scenes whose size derives from `min(w, h)`, so the size
  is a hint. Cropping would have to deal with ANSI-colored lines.

## Consequences

- Random output is varied and recognisable, and works the same in the menu,
  one-shot commands and intelligent mode.
- `random art 20x10` no longer yields 20x10 characters (only about 1 in 11
  runs does); this is a behavior change from the old noise generator.
- `ascii_art.random_animal()` still exists but only the demo uses it.
- The sprites and themes are data in one file, so adding a theme or a coin
  caption does not touch the parser.
- Review pass found that `shape_to_command` in `cli.py` had `'abstract'`
  twice (the later entry won), which is why `art`/`painting` never reached
  random art. Word-aware routing now lives next to the other special cases
  (`specific_animal`); when adding a shape word, check for duplicate keys.
