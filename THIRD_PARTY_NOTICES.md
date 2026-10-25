# Third-party notices

ASCII Art Generator itself is released under the [MIT License](LICENSE).

Two Claude Code skills written by other people are bundled in `.claude/skills/`. They are development aids, not part of the program: they are not imported by the code, not included in the executables and not needed to use the tool. Each keeps its own license.

## humanizer

- Location: `.claude/skills/humanizer/`
- Source: https://github.com/blader/humanizer (version 3.1.0)
- Author: Siqi Chen
- License: MIT. The full text is in [`.claude/skills/humanizer/LICENSE`](.claude/skills/humanizer/LICENSE).
- Purpose: rewrites text to remove common signs of AI writing. The project uses it when writing prose such as the README, the changelog and release notes.

## architecture-diagram

- Location: `.claude/skills/architecture-diagram/`
- Author: Cocoon AI
- Version: 1.1
- License: MIT, as stated in the header of `.claude/skills/architecture-diagram/SKILL.md`. The upstream copy bundled here does not include a separate license file.
- Purpose: produces dark-themed architecture diagrams as self-contained HTML with inline SVG.
