---
name: ascii-art
description: Reference catalog of the shapes, fonts, colors, fill patterns and border styles of this ASCII art generator. Use it whenever you generate/draw ASCII art, add a new shape, or explain the project's command syntax.
---

# ASCII Art Generator catalog

A reference based on the project's real code (not invented). Use it to stay
consistent with what already exists before generating examples or adding new
features.

## Where everything lives

- `ascii_art_generator/ascii_art.py` — base shapes, fonts, patterns, banners/boxes, animations, ANSI colors.
- `ascii_art_generator/smart_generator.py` — advanced shapes (star, hexagon, oval, arrow, pentagon, butterfly, flower), fill patterns and rich borders, "smart" generation (`smart_gen`).
- `ascii_art_generator/cli.py` — `ENCommandParser`, which turns English (natural-language) commands into the parameters of the functions below. It is the only parser used by `ASCIIArtCLI` (the old `PTCommandParser`, which was never wired into the app, was removed).
- `ascii_art_generator/animal_scenes.py` — `animal_scene(name, big, setting)`: an animal on a coin (`$NAME`), in a frame or in a themed scene (meadow, rain, snow, beach, space, forest); returns `(lines, kind)` and `scene_color(kind)` suggests the color. Used by `smart_gen.generate_animal_art()`.
- `ascii_art_generator/emoji_art.py` — `emoji_face(mood)`: a large face (11 lines, plain ASCII) composed of a head, eyes, brows, a mouth and extras (hearts, tears, `zZ`, sparkles); 13 moods (happy, laugh, wink, sad, angry, surprised, cool, love, sleepy, calm, dizzy, starstruck, silly). `mood` also accepts the parser's moods (`MOOD_FACES`: happy/sad/angry/calm/sleepy), so `draw a sad emoji` gives a sad face. Returns `(lines, mood)` and `emoji_color(mood)` suggests the color. `random_emoji(big=True)` uses it; `big=False` returns the one-line kaomoji.
- `ascii_art_generator/install_info.py` — `describe()` (`--version`) and `stale_copy_warning()` (a warning when the installed command is an older copy of the source folder; see `run.py`).
- `ascii_art_generator/learned_words.py` / `console.py` — persistence of the taught moods (`~/.config/ascii_generator/learned_words.json`); UTF-8 setup for stdout.
- `ascii_art_generator/intro.py` — animated startup banner and animated menu, standard library only. `show_intro()` plays the entrance (rainbow logo, `━` rule, subtitle typed letter by letter); `banner_lines()` returns `(logo, [rule, subtitle, rule])` as plain text; `title_lines()` draws `ASCII` with the `solid` font (an alias of pyfiglet's `banner`, or the built-in `block` without pyfiglet), stretched horizontally by inserting a blank after every second column so the strokes stay thin, and centered on the rule; `LiveLines(targets, min_cols)` is the thread that redraws lines that are already printed (ESC 7 / cursor-up / ESC 8) while `input()` blocks. It turns itself off outside a terminal, with `TERM=dumb`, with `--no-animation` or `ASCII_GENERATOR_NO_ANIMATION=1`, and when the terminal is narrower than the widest line.
- `ascii_art_generator/web_bridge.py` — `run_command(text)`: runs a command through the same pipeline as the CLI, captures `stdout` and returns it (with ANSI codes) as a `str`; it handles `teach`, commands it does not understand, `q`/`exit`/`menu`, and refuses sizes above 300. Used only by the web page.
- `web/` + `scripts/build_web.py` — static browser version (`index.html`, `style.css`, `app.js`): runs the package inside Pyodide and converts ANSI to HTML. `python3 scripts/build_web.py [--serve]` (or `make web`) builds `_site/`; `.github/workflows/pages.yml` publishes it to GitHub Pages.
- `ascii_art_generator/image_art.py` — `image_to_ascii(path, width, ramp, color, invert)`, converts a real image file (PNG/JPG/...) to ASCII art with a brightness ramp. The only module in the project with a third-party dependency (Pillow — see `.claude/skills/generator-core/SKILL.md`).

## Geometric shapes

| Shape | Function | File | Main parameters |
|---|---|---|---|
| Rectangle | `draw_rectangle(width, height, char, filled)` | ascii_art.py | width, height, char, filled |
| Triangle | `draw_triangle(height, char, direction)` | ascii_art.py | height, char, direction: up/down/left/right |
| Circle | `draw_circle(radius, char)` | ascii_art.py | radius, char (corrects the terminal aspect ratio — see the note below) |
| Heart | `draw_heart(size, char)` | ascii_art.py | size: 1–12 in the function, default 6; the parser limits it to 1–8 (generated algorithmically, scales with the size) |
| Diamond | `draw_diamond(size, char)` | ascii_art.py | size, char |
| Tree | `generate_tree(height, char)` | ascii_art.py | height, char |
| Spiral | `generate_spiral(size, char)` | ascii_art.py | size, char (an Archimedean spiral traced on the grid, not a solid fill) |
| Star | `draw_star(size, char)` | smart_generator.py | size 3–12, default 7; 5 points, point up |
| Hexagon | `draw_hexagon(size, char)` | smart_generator.py | minimum size 2, default 8 |
| Oval | `draw_oval(width, height, char)` | smart_generator.py | width, height (default 40x8); samples the center of each cell; in a command it accepts `30x8` or a single number (the width, with height = width // 5) |
| Arrow | `draw_arrow(direction, size, char)` | smart_generator.py | direction: right/left/up/down, size |
| Pentagon | `draw_pentagon(size, char)` | smart_generator.py | size, default 8; a regular pentagon with the point up |
| Butterfly | `draw_butterfly(size, char)` | smart_generator.py | minimum size 5; upper and lower wings, body and antennae |
| Flower | `draw_flower(size, char)` | smart_generator.py | minimum size 4; 5 elliptical petals, a hollow ring and a `\|` stem (the stem ignores `char`); corrects the aspect ratio |

**Terminal aspect ratio**: characters are ~2x taller than they are wide, so
`draw_circle` and `draw_flower` scan the `x` axis at double resolution and
divide by 2 before the distance calculation. Without this the shape comes out
"oval"/stretched vertically instead of round. When you create a new shape based
on radial distance, repeat this correction. The star and the pentagon use
`_rasterize_polygon(poly, char)` (smart_generator.py), which rasterizes a
polygon in square units and stretches `x` by 2; `draw_heart` samples the
implicit curve `(x²+y²-1)³ - x²y³ ≤ 0` on the same grid (a grid of `5*size+1`
rows and ~2.1x as many columns; the empty rows at the tips are trimmed, so the
final drawing has 6, 11, 16, 21, 25, 30... lines).

## Patterns

- `generate_gradient(width, height)` — a character-density gradient
- `generate_checkerboard(size, chars)` — a checkerboard
- Random art: `random`, `art` and `painting` (e.g. `make random art`, `make a painting 20x10 color red`) go to `ASCIIArtCLI._random_art()` → `smart_gen.generate_interesting_art("random", w, h)` (`random_abstract` no longer exists; it was pure noise with no structure). The size is only a hint for the generator, not an exact dimension. An explicit color replaces the one the generator picks. `abstract`/`pattern`/`design` are something else: the `abstract` style of intelligent mode (`generate_from_command`), with no size or color
- `random_animal()` (a simple drawing; the "random animal" command/menu entry uses `smart_gen.generate_animal_art()` → `animal_scenes.animal_scene()`: a `$NAME` coin, a frame or a scene, with random decoration/color) / `random_emoji()` — random generators of animals (cat, dog, owl, penguin, fish, bear, rabbit, `crow` the crow/jackdaw, `raven` the raven) and emojis. Each animal with its own drawing also has a bigger version in `ANIMALS_BIG` (same keys as `ANIMALS`), used when the command includes `big`/`large`/`huge`/`giant` (`ENCommandParser.BIG_WORDS` → `params['big']` → `get_animal_art(name, big)`), e.g. `draw a big cat`. `random animal`/`draw an animal` uses the big drawing by default (`big=True`); `a random animal`/`a random emoji` are read as an animal/emoji, not as random art

## Text to ASCII

`text_to_ascii(text, font)` with 4 font names: `small`, `block`, `banner`, `shadow` (plus the alias `solid` → pyfiglet's `banner` font, used only by the logo). If the terminal is narrower than one letter, pyfiglet raises `CharNotPrinted`; `_figlet_to_ascii` catches it and renders again without line wrapping.

- **With `pyfiglet` installed** (the main path): `_figlet_to_ascii()` maps those names to real FIGlet fonts through `FIGLET_FONT_ALIASES` (`small`→`small`, `block`→`block`, `banner`→`banner3`, `shadow`→`shadow`) and also accepts any other FIGlet font name (`slant`, `big`, `doom`, `ansi_shadow`, ... — 500+). An unknown name → the `small` font. It supports digits, lowercase and punctuation; the height varies by font (do not assume 5 lines). It wraps lines at the terminal width.
- **Without `pyfiglet`** (the fallback): the built-in `FONTS` in ascii_art.py, 5 lines tall, only A-Z (some fonts also `!` and `?`), one blank column between letters; characters without a glyph appear as `?` (`_MISSING_GLYPH`).

## Banners and boxes

- `create_banner(text, width, char)` — a strip with a border and centered text
- `create_box(text, width, char)` — a box around text (supports multiple lines)

## Colors (ANSI) — `get_color_code(color_name)`

`black, red, green, yellow, blue, magenta, cyan, white` + `bright_*` variants.
`ENCommandParser` accepts synonyms (`crimson/ruby→red`, `azure/cobalt→blue`, `purple/violet→magenta`, `pink→light_red`, etc.).

`rainbow`/`multicolor`/`multicolour` is a special color value: instead of a
single ANSI code, it cycles through `RAINBOW_COLORS` (`cli.py`), a different
color for each line of the art (e.g. `draw a heart size 4 color rainbow`). It
is handled inside `ASCIIArtCLI._apply_color`, not in `get_color_code`.

## Moods (teachable)

`ENCommandParser.MOOD_SYNONYMS`/`MOOD_EFFECTS` in cli.py — a mood recognized
anywhere in the command (not only after the shape, unlike color/font/fill)
applies a default color, only if the user did not specify `color` explicitly:

| Mood | Built-in synonyms | Default color |
|---|---|---|
| happy | happy, joyful, cheerful | yellow |
| sad | sad, unhappy, gloomy | blue |
| angry | angry, mad, furious | red |
| calm | calm, peaceful, relaxed | green |
| sleepy | sleepy, tired, drowsy | cyan |

New synonyms can be taught at runtime, without editing code, with
`teach <word> as <mood>` in intelligent mode (e.g. `teach ecstatic as happy`).
They persist in `~/.config/ascii_generator/learned_words.json`
(`ascii_art_generator/learned_words.py`) and are loaded in every later session.
`teach` only accepts a `<mood>` from the 5 above — it does not create new
moods/effects, only synonyms for the existing ones.

## Fill

Basic (`get_fill_style_pattern` in ascii_art.py): `empty, solid, dotted, striped_h, striped_v, crosshatch, plus, star, random, gradient`.

Advanced (`SmartGenerator.FILL_PATTERNS` in smart_generator.py — 32 patterns):
`solid, empty, dotted, striped, horizontal_stripes, vertical_stripes, cross, crosshatch, diagonal, anti_diagonal, x_pattern, grid, checkerboard, dense_checkerboard, random, sparse_random, dense_random, dots, stars, plus_signs, mixed, left_gradient, right_gradient, top_gradient, bottom_gradient, center_gradient, dense_gradient, spiral_pattern, concentric, wave, zigzag, honeycomb`.

The 6 `*_gradient` patterns use `create_directional_gradient` — a smooth
density ramp (`GRADIENT_RAMP = ' .:-=+*#%@'`), not a binary half/half cut.
`dense_gradient` is the left-to-right one, but with
`DENSE_GRADIENT_RAMP = '=+*#%@'` (only the heavy half), for shapes with no
empty or nearly empty cells. A bare `gradient` is a synonym of
`left_gradient`.

**Applied through the silhouette mask**: when one of these patterns (≠ `solid`)
is applied to a shape (through `_apply_style_to_art` in cli.py, or
`_generate_shape`/`_generate_advanced_shape` in smart_generator.py), the
texture only replaces the cells where the shape had already drawn a
character — `mask_fill_pattern` (smart_generator.py) takes care of this. Never
go back to calling `art = apply_fill_pattern(...)` directly on a shape: that
replaces the whole silhouette with a generic rectangle (a bug that was already
fixed once).

## Borders

Basic (`get_border_chars` in ascii_art.py): `simple, double, dashed, wavy, bold, light, star, plus`.

Advanced (`SmartGenerator.BORDER_STYLES`): `none, simple, double, dashed, dotted, thick, bold, fancy, rounded, 3d, shadow, double_line`.

`apply_border` always keeps the shape's content (there were versions of
`bold`/`thick`/`double_line`/`3d` that erased it) and the frame is as wide as
the lines plus the margins (`fancy`, `rounded` and `thick` +4; `bold` and
`double_line` +2; `3d` +3, counting the shadow offset). The `empty` fill does
not use the box rectangle: `mask_fill_pattern` draws the outline of the
silhouette itself.

## Image to ASCII

`image_to_ascii(path, width=100, ramp='standard', color=False, invert=False)`
in `image_art.py` converts a real image file to ASCII, mapping each pixel's
brightness (the luminance formula `0.299R+0.587G+0.114B`) to a character of
`ASCII_RAMPS`: `standard` (10 levels), `detailed` (a long ramp, more
gradation), `blocks` (Unicode blocks `░▒▓█`). With `color=True`, each
character is wrapped in a 24-bit ANSI code (`\033[38;2;R;G;Bm`) with the
pixel's real color, instead of plain text. It corrects the terminal aspect
ratio when deriving the sampled height (`_ASPECT_CORRECTION = 0.55`).

Command: `convert image <path> [width N] [color]` (e.g. `convert image
/tmp/photo.png width 80 color`) — recognized in `ENCommandParser._parse_image_command`,
which runs BEFORE the generic tokenizer (which lower-cases everything) so that
the original case of the file path is preserved.

The only place in the project with a third-party dependency (Pillow, in
`requirements.txt`) — see the exception documented in
`.claude/skills/generator-core/SKILL.md`.

## Animations

`spinner_animation(duration)` and `progress_bar(duration, char)` — blocking, they run in the terminal (they do not return a string).

## Command syntax (natural language, English)

`ENCommandParser` extracts number(s), character, color, font and style from free text, and supports compound commands separated by `"and"` (each part is parsed independently by `_parse_single_command`, through `_split_compound_command`). Valid examples:

```
draw a rectangle 10x5
make a circle with radius 8 color blue
write HELLO
write HELLO with font banner
draw a heart size 2
make a rectangle 8x4 with color cyan style dotted
make a spiral 20
make an emoji
make a banner with text COOL
make a circle with radius 5 color blue and a rectangle 10x5 color red
draw a heart size 4 color rainbow
draw a star 8 color yellow
make an oval 30x8 color green
draw a triangle 5
convert image /tmp/photo.png width 80 color
```

A bare number goes to the key the executor reads: `height` (`triangle`,
`tree`), `width`+`height` (`rectangle`, `oval`), `radius` (`circle`) and `size`
(`heart`, `diamond`, `spiral`, `star`, `hexagon`, `pentagon`, `butterfly`,
`flower`, `arrow`). If the key the parser writes does not match the one read
in `execute_parsed_command`, the number is silently ignored.

### Known limitations of `ENCommandParser`

- **The `"and"` separator is word-based.** A color list on a single shape (`"with color red and blue"`) is read as a one-part compound command: it applies the first color, drops the second and prints a `[1/1]` header — there is no way to disambiguate without quotes/named parameters.

## When adding a new shape/style

1. Implement the generator function in `ascii_art.py` (base shapes) or `smart_generator.py` (advanced shapes/patterns).
2. Register synonyms in `ENCommandParser.SHAPE_SYNONYMS` in `cli.py` — watch out for duplicate keys in the dict (a repeated key silently replaces the earlier one instead of adding to it).
3. Add/adjust the mapping in `shape_to_command` and the `params` logic in `parse_command` (EN) that builds the `{'command': ..., 'params': {...}}` dict.
4. If the generator function is used inside `smart_generator.py` (fills/borders/`smart_gen`), wrap it in `_normalize_lines(...)` before treating it as a list of lines — functions in `ascii_art.py` return a `str` (`'\n'.join(...)`), while those in `smart_generator.py` return `List[str]`; iterating a `str` gives characters, not lines.
5. Update this skill with the new entry in the relevant table/list.
6. Test with a real command before calling it done.
