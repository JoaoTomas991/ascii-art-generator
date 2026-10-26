# Roadmap

Ideas for what could come after 1.0. There are no dates, and nothing here is a promise. If one of these matters to you, or you have a different idea, open an issue.

## Braille art

Right now the drawings are outlines made of ASCII characters. A Braille character packs a grid of 2 by 4 dots into one cell, which is enough for shading and a lot more detail, the way many image-to-text converters work. It would come in three steps, and each one is useful alone:

1. A Braille mode for `convert image`, with dithering, so a photo turns into a shaded picture.
2. A small pixel drawing engine with shading, used first for emoji faces.
3. The animals redrawn on that engine.

Braille is Unicode and not ASCII, and it needs a font that has the Braille glyphs, so it would be opt-in (something like `style braille`) and the classic ASCII output would stay the default. It also needs testing on Windows terminals.

## Sharing to WhatsApp and Telegram

Pasting ASCII art into a chat app often breaks it: the font is proportional, long lines wrap, and ANSI colors show up as garbage. Better copy support would include:

- A `copy` output mode that strips ANSI codes and trims trailing spaces.
- Wrapping the art in a monospace block (triple backticks for Telegram, WhatsApp and Markdown chats) so the alignment survives.
- A width limit that fits a phone screen, so the art does not wrap.
- A copy-to-clipboard button in the web version that uses these rules.

## ASCII animation

The terminal output is static apart from the spinner and the progress bar. The idea is to animate the art itself:

- Frame-based animations for the existing shapes and animals, such as a blinking face, a beating heart or a spinning star.
- A `play` command with options for speed and loop count.
- Export to an animated format for sharing, such as a GIF, which the project does not support today (see the known limitations).
- The same animations in the web version.

## A more dynamic text block

Text to ASCII works, but the result is fixed once it is drawn. Ideas to make it more dynamic:

- Per-word and per-letter colors, and gradients across the text.
- Alignment (left, center, right) and a fixed output width, with automatic wrapping of long text.
- Multi-line text with a mix of fonts in the same block.
- Animated text effects, such as typewriter, wave or rainbow cycling.
- Text inside shapes and boxes, with the text fitted to the shape.

## Better image to ASCII

`convert image` maps brightness to a character ramp. It could produce better pictures:

- Contrast, brightness and gamma controls, plus automatic contrast stretching.
- Edge detection, so outlines stay sharp.
- Dithering (Floyd-Steinberg) for smoother shading.
- Aspect-ratio correction per font, and a choice of character ramps.
- Better color handling, with palette reduction for terminals that lack 24-bit color.
- Support for transparency and for animated images (see the ASCII animation section).
- The Braille mode described above is the other half of this work.

## Smaller fixes

- A color list on a single shape, as in `make a rectangle with color red and blue`, is read as two commands and the second color is dropped. See the known limitations in [docs/usage.md](docs/usage.md#known-limitations).
