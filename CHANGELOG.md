# Changelog

All notable changes to this project are listed here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses
[Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- `convert image` options `auto`, `contrast N`, `gamma N`, `dither`, `invert`, `ramp NAME`, `edges`, `braille` and `crop L T W H`, in any order after the path.
- `style braille` and `style shaded` for shapes: the shape is redrawn in Unicode Braille dots, in the same lines and columns, with smoother edges. `shaded` also shades the inside, lit from the top left. For example `draw a heart size 4 style shaded color red`.
- A color list on one shape, as in `make a rectangle 8x4 color red and blue` or `color red, blue, green`: the colors cycle one per line, like `rainbow`. It used to keep only the first color.
- A color named before the shape is applied: `draw a red heart`, `make a pink banner with text HI`.
- Browser version: a **Copy as image** button that copies the drawing as a PNG, for sharing in WhatsApp, Telegram and other chat apps. A picture keeps the colours and the shape on any screen, including a phone, where the same drawing pasted as text loses its colours and wraps. Browsers that cannot copy images download the file instead.

### Changed

- Fill patterns keep the parts of a shape that are one character wide. The tip of a star's leg, the point of a triangle or a stretch of the spiral used to vanish where the pattern had a gap (`draw a star 5 style dotted` lost one of its two feet).
- Banners and boxes accept every color the shapes do, including `rainbow` and the `light_*` colors, which they used to ignore.
- `convert image` resizes with LANCZOS and draws transparent areas as white instead of black.
- `convert image` output is at most 400 lines tall. A very tall image, or a thin `crop`, is made narrower to keep its proportions, where it used to print thousands of lines.
- `convert image` reports an option with a bad value (`gamma -1`, `crop` with three numbers, `ramp` without a name) instead of answering that the image was not found.
- Browser version: **Copy text** no longer includes trailing spaces on each line or blank lines at the start and end.

Ideas for what comes next are in [ROADMAP.md](ROADMAP.md).

## [1.0.0] - 2026-10-25

First public release.

### Added

- English commands for shapes, text, patterns, colors and styles, such as `draw a heart size 4 color rainbow`. Several commands can be joined with "and".
- 14 shapes: rectangle, circle, triangle, heart, diamond, spiral, tree, star, hexagon, oval, arrow, pentagon, butterfly and flower.
- Text to ASCII with four named fonts (`small`, `block`, `banner`, `shadow`) and, when `pyfiglet` is installed, any other FIGlet font (for example `slant`). Without `pyfiglet`, built-in 5-line fonts are used.
- 32 fill patterns, always applied inside the shape's own outline, plus border styles, banners and boxes.
- Colors, including `rainbow`, which cycles one color per line.
- Random emoji faces with 13 moods (`draw a sad emoji`) and nine animals, drawn as a coin, a framed portrait or a themed scene. `face`, `smiley` and `smile` work as synonyms of `emoji`.
- Image to ASCII conversion, with optional 24-bit color per character (`convert image photo.png width 80 color`). It needs Pillow.
- Mood words you can teach (`teach ecstatic as happy`). They are saved between sessions.
- Menu mode, intelligent mode and one-shot commands, with an animated startup banner. `--no-animation` turns the animation off.
- A browser version that runs the same Python code through Pyodide, published on GitHub Pages. Nothing is uploaded.
- Standalone executables for Windows, macOS (Apple Silicon) and Linux, attached to every `v*` release.
- The `ascii-art-generator` command (and the short alias `ascii-generator`), installable with pipx, uv or pip. `--version` shows which copy of the code is running.
- Continuous integration on Windows, Linux and macOS with Python 3.12, 3.13 and 3.14.

### Changed

- The project is now called ASCII Art Generator. It was called ASCII Generator during development, and `ascii-generator` is kept as an alias for the command.

[Unreleased]: https://github.com/JoaoTomas991/ascii-art-generator/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/JoaoTomas991/ascii-art-generator/releases/tag/v1.0.0
