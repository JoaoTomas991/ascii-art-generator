# Roadmap

Ideas for what could come after 1.0. There are no dates, and nothing here is a promise. If one of these matters to you, or you have a different idea, open an issue.

## Braille art

Right now the drawings are outlines made of ASCII characters. A Braille character packs a grid of 2 by 4 dots into one cell, which is enough for shading and a lot more detail, the way many image-to-text converters work. It would come in three steps, and each one is useful alone:

1. A Braille mode for `convert image`, with dithering, so a photo turns into a shaded picture.
2. A small pixel drawing engine with shading, used first for emoji faces.
3. The animals redrawn on that engine.

Braille is Unicode and not ASCII, and it needs a font that has the Braille glyphs, so it would be opt-in (something like `style braille`) and the classic ASCII output would stay the default. It also needs testing on Windows terminals.

## Smaller fixes

- A color list on a single shape, as in `make a rectangle with color red and blue`, is read as two commands and the second color is dropped. See the known limitations in [docs/usage.md](docs/usage.md#known-limitations).
