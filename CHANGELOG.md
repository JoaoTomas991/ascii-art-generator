# Changelog

All notable changes to this project are listed here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses
[Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- `convert image` options `auto`, `contrast N`, `gamma N`, `dither`, `invert` and `ramp NAME`, in any order after the path.

### Changed

- `convert image` resizes with LANCZOS and draws transparent areas as white instead of black.

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
