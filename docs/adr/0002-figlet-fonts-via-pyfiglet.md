# 0002. Text-to-ASCII renders through pyfiglet, with built-in fonts as fallback

Date: 2026-09-29
Status: Accepted

## Context

The four built-in fonts (`small`, `block`, `banner`, `shadow`) in
`ascii_art.py` were effectively the same hand-written 5x5 grid: `font banner`
and `font small` produced identical output, letters were drawn with the
letter itself and had no spacing between them (`HEEEEEL`), and anything
outside A-Z (digits, lowercase, most punctuation) silently rendered as blank
space. `write ABC 2026!` dropped "2026" entirely. This was the main reason
text output looked poor.

## Decision

`text_to_ascii()` renders through pyfiglet (FIGlet fonts) when it is
importable. The project's four font names map to real FIGlet fonts via
`FIGLET_FONT_ALIASES` (`banner` → `banner3`, the others by the same name),
and any other FIGlet font name is accepted as-is; an unknown name falls back
to `small`. The import is deferred into `_figlet_to_ascii()`, mirroring
Pillow in `image_art.py`, so pyfiglet is optional: without it, the built-in
`FONTS` are still used, now with one column between letters and a visible
`?` glyph for unsupported characters instead of blank space.

## Alternatives considered

- Hand-writing better built-in fonts would keep the stdlib-only rule, but
  reproducing even a handful of good fonts with full character coverage is
  a lot of data to maintain for a worse result than FIGlet's established
  fonts.
- The `art` package bundles FIGlet-style fonts too, but also a large set of
  decorations and random text that overlaps with what this project already
  does.
- Vendoring `.flf` font files with a stdlib FIGlet parser would need no
  dependency, but it reimplements FIGlet smushing rules. pyfiglet already
  does that and is packaged for Debian (`python3-pyfiglet`) and PyPI.

## Consequences

- This is the project's second third-party dependency (after Pillow),
  isolated to one function and optional.
- Text art height now varies by font. Callers must not assume 5 lines, and a
  `font` value may be a FIGlet-only name absent from `FONTS`.
- Output differs depending on whether pyfiglet is installed, so the
  regression battery's text checks need to hold under both paths.
- FIGlet output wraps at the terminal width (`shutil.get_terminal_size`).
