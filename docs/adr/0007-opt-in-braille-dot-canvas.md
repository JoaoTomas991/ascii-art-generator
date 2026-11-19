# 0007. Braille drawings are opt-in and come from one dot canvas

Date: 2026-11-10
Status: Accepted

## Context

The drawings are made of whole characters, so curves and diagonals come out
as staircases and a shape is either filled or empty. The request was for art
with more detail and shading.

A Unicode Braille character holds a grid of 2 by 4 dots. Drawing with dots
gives twice the horizontal and four times the vertical detail in the same
space, and a dot pattern can stand for a shade of grey. `convert image`
already had a Braille mode, with its own code for packing dots into
characters.

Braille is not ASCII. It needs a font that has the Braille glyphs, and it has
not been tested on Windows terminals.

## Decision

Braille output is opt-in, and the classic ASCII drawings stay the default.

A new module, `ascii_art_generator/pixel_canvas.py`, holds a `PixelCanvas`: a
grid of dots that prints as Braille characters. It is standard library only,
and it owns the dot-to-character table (`BRAILLE_BITS`), which `image_art.py`
now imports instead of keeping its own copy.

Shapes get two new style values, parsed like fill patterns:

- `style braille` redraws the shape in dots, with smoother edges.
- `style shaded` does the same and shades the inside, lit from the top left,
  with an ordered dither and a solid rim.

A shape is not drawn again from its geometry. The existing generator draws
its ASCII version, and the canvas blends between the centres of the
character cells (bilinear interpolation) and keeps the dots that are at
least half covered. The Braille version therefore has the same number of
lines and columns as the ASCII one.

## Alternatives considered

- Making Braille the default would break the project's ASCII look and fail
  on terminals and fonts without the glyphs.
- Writing a geometric definition for each of the 14 shapes would give exact
  curves, but it is 14 new drawings to keep in step with the ASCII ones
  (sizes, directions, proportions), for a gain that is small at these sizes.
- Drawing the ASCII shape at twice the size and packing it down fails for
  shapes whose size is capped, such as the heart.
- Random dithering for the shading gives a noisy, different picture on every
  run. The ordered pattern is even and repeatable.

## Consequences

- Every shape, including ones added later, gets the Braille styles for free,
  and borders and colors apply as before because the size does not change.
- The smoothing can only work with what the ASCII drawing has. A shape that
  is one character wide becomes a thin stroke, and sharp corners come out
  slightly rounded.
- Blank cells are the Braille blank (U+2800), not a space, so the columns
  stay aligned in fonts where the two have different widths. Text copied
  from a Braille drawing carries those characters.
- The canvas is the base for the next steps on the roadmap, the emoji faces
  and the animals drawn with shading. They will need drawing primitives
  (ellipses, lines) that the canvas does not have yet.
- `braille` and `shaded` sit in `FILL_PATTERN_SYNONYMS` but are not fill
  patterns: `_apply_style_to_art` handles them before `mask_fill_pattern`.
  They are not among the 32 patterns of `smart_generator.py`.
