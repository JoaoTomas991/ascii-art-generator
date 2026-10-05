---
name: ascii-art
description: Catálogo de referência das formas, fontes, cores, padrões de preenchimento e estilos de borda deste gerador de ASCII Art. Usar sempre que fores gerar/desenhar arte ASCII, adicionar uma forma nova, ou explicar a sintaxe de comandos do projeto.
---

# Catálogo do ASCII Generator

Referência com base no código real do projeto (não invenção) — usa isto para
garantir consistência com o que já existe antes de gerar exemplos ou adicionar
funcionalidades novas.

## Onde vive cada coisa

- `ascii_art_generator/ascii_art.py` — formas base, fontes, padrões, banners/caixas, animações, cores ANSI.
- `ascii_art_generator/smart_generator.py` — formas avançadas (estrela, hexágono, oval, seta, pentágono, borboleta, flor), padrões de preenchimento e bordas ricas, geração "inteligente" (`smart_gen`).
- `ascii_art_generator/cli.py` — `ENCommandParser`, que converte comandos em inglês (linguagem natural) nos parâmetros das funções abaixo. É o único parser usado pela `ASCIIArtCLI` (o antigo `PTCommandParser`, nunca ligado à aplicação, foi removido).
- `ascii_art_generator/image_art.py` — `image_to_ascii(path, width, ramp, color, invert)`, converte um ficheiro de imagem real (PNG/JPG/...) em ASCII art por rampa de brilho. Único módulo do projeto com dependência de terceiros (Pillow — ver `.claude/skills/generator-core/SKILL.md`).

## Formas geométricas

| Forma | Função | Ficheiro | Parâmetros principais |
|---|---|---|---|
| Retângulo | `draw_rectangle(width, height, char, filled)` | ascii_art.py | width, height, char, filled |
| Triângulo | `draw_triangle(height, char, direction)` | ascii_art.py | height, char, direction: up/down/left/right |
| Círculo | `draw_circle(radius, char)` | ascii_art.py | radius, char (corrige aspect-ratio do terminal — ver nota abaixo) |
| Coração | `draw_heart(size, char)` | ascii_art.py | size: 1–12, default 6 (gerado algoritmicamente, escala com o tamanho) |
| Diamante | `draw_diamond(size, char)` | ascii_art.py | size, char |
| Árvore | `generate_tree(height, char)` | ascii_art.py | height, char |
| Espiral | `generate_spiral(size, char)` | ascii_art.py | size, char (espiral de Arquimedes traçada na grelha, não um preenchimento sólido) |
| Estrela | `draw_star(...)` | smart_generator.py | — |
| Hexágono | `draw_hexagon(...)` | smart_generator.py | — |
| Oval | `draw_oval(...)` | smart_generator.py | — |
| Seta | `draw_arrow(...)` | smart_generator.py | — |
| Pentágono | `draw_pentagon(...)` | smart_generator.py | — |
| Borboleta | `draw_butterfly(...)` | smart_generator.py | — |
| Flor | `draw_flower(...)` | smart_generator.py | — (corrige aspect-ratio do terminal) |

**Aspect-ratio do terminal**: os carateres são ~2x mais altos que largos, por
isso `draw_circle`, `draw_star` e `draw_flower` fazem o scan do eixo `x` a
resolução dupla e dividem por 2 antes do cálculo de distância — sem isto a
forma sai "ovalada"/esticada na vertical em vez de redonda. Ao criar uma
forma nova baseada em distância radial, replica esta correção.

## Padrões

- `generate_gradient(width, height)` — degradê de densidade de caracteres
- `generate_checkerboard(size, chars)` — tabuleiro/xadrez
- `random_abstract(width, height)` — arte abstrata aleatória
- `random_animal()` / `random_emoji()` — geradores aleatórios de animais (gato, cão, coruja, pinguim, peixe, urso, coelho, corvo) e emojis. Cada animal com desenho próprio tem também uma versão maior em `ANIMALS_BIG` (mesmas chaves que `ANIMALS`), usada quando o comando inclui `big`/`large`/`huge`/`giant` (`ENCommandParser.BIG_WORDS` → `params['big']` → `get_animal_art(name, big)` / `random_animal(big)`), ex. `draw a big cat`

## Texto para ASCII

`text_to_ascii(text, font)` com 4 nomes de fonte: `small`, `block`, `banner`, `shadow`.

- **Com `pyfiglet` instalado** (caminho principal): `_figlet_to_ascii()` mapeia esses nomes para fontes FIGlet reais via `FIGLET_FONT_ALIASES` (`small`→`small`, `block`→`block`, `banner`→`banner3`, `shadow`→`shadow`) e aceita também qualquer outro nome de fonte FIGlet (`slant`, `big`, `doom`, `ansi_shadow`, ... — 500+). Nome desconhecido → fonte `small`. Suporta dígitos, minúsculas e pontuação; a altura varia por fonte (não assumir 5 linhas). Quebra linha à largura do terminal.
- **Sem `pyfiglet`** (fallback): fontes internas `FONTS` em ascii_art.py, 5 linhas de altura, só A-Z (algumas fontes também `!` e `?`), uma coluna de espaço entre letras; caracteres sem glifo aparecem como `?` (`_MISSING_GLYPH`).

## Banners e caixas

- `create_banner(text, width, char)` — faixa com borda e texto centrado
- `create_box(text, width, char)` — caixa à volta de texto (suporta multi-linha)

## Cores (ANSI) — `get_color_code(color_name)`

`black, red, green, yellow, blue, magenta, cyan, white` + variantes `bright_*`.
O `ENCommandParser` aceita sinónimos (`crimson/ruby→red`, `azure/cobalt→blue`, `purple/violet→magenta`, `pink→light_red`, etc.).

`rainbow`/`multicolor`/`multicolour` é um valor de cor especial: em vez de um
único código ANSI, cicla `RAINBOW_COLORS` (`cli.py`) uma cor diferente por
linha da arte (ex: `draw a heart size 4 color rainbow`). Tratado dentro de
`ASCIIArtCLI._apply_color`, não em `get_color_code`.

## Moods (ensináveis)

`ENCommandParser.MOOD_SYNONYMS`/`MOOD_EFFECTS` em cli.py — um mood reconhecido
em qualquer posição do comando (não só depois da forma, ao contrário de
cor/fonte/fill) aplica uma cor por omissão, só se o utilizador não tiver
especificado `color` explicitamente:

| Mood | Sinónimos embutidos | Cor por omissão |
|---|---|---|
| happy | happy, joyful, cheerful | yellow |
| sad | sad, unhappy, gloomy | blue |
| angry | angry, mad, furious | red |
| calm | calm, peaceful, relaxed | green |
| sleepy | sleepy, tired, drowsy | cyan |

Novos sinónimos podem ser ensinados em runtime, sem editar código, com
`teach <word> as <mood>` no modo inteligente (ex: `teach ecstatic as happy`).
Ficam persistidos em `~/.config/ascii_generator/learned_words.json`
(`ascii_art_generator/learned_words.py`) e carregados em todas as sessões
seguintes. `teach` só aceita um `<mood>` de entre os 5 acima — não cria
moods/efeitos novos, só sinónimos para os existentes.

## Preenchimento (fill)

Básico (`get_fill_style_pattern` em ascii_art.py): `empty, solid, dotted, striped_h, striped_v, crosshatch, plus, star, random, gradient`.

Avançado (`SmartGenerator.FILL_PATTERNS` em smart_generator.py — 31 padrões):
`solid, empty, dotted, striped, horizontal_stripes, vertical_stripes, cross, crosshatch, diagonal, anti_diagonal, x_pattern, grid, checkerboard, dense_checkerboard, random, sparse_random, dense_random, dots, stars, plus_signs, mixed, left_gradient, right_gradient, top_gradient, bottom_gradient, center_gradient, spiral_pattern, concentric, wave, zigzag, honeycomb`.

Os 5 `*_gradient` usam `create_directional_gradient` — uma rampa de
densidade suave (`GRADIENT_RAMP = ' .:-=+*#%@'`), não um corte binário
metade/metade.

**Aplicação mascarada pela silhueta**: quando um destes padrões (≠ `solid`)
é aplicado a uma forma (via `_apply_style_to_art` em cli.py, ou
`_generate_shape`/`_generate_advanced_shape` em smart_generator.py), a
textura só substitui as células onde a forma já tinha desenhado um
carácter — `mask_fill_pattern` (smart_generator.py) trata disto. Nunca
voltar a fazer `art = apply_fill_pattern(...)` diretamente sobre uma forma:
isso substitui a silhueta inteira por um retângulo genérico (bug já
corrigido uma vez).

## Bordas

Básico (`get_border_chars` em ascii_art.py): `simple, double, dashed, wavy, bold, light, star, plus`.

Avançado (`SmartGenerator.BORDER_STYLES`): `none, simple, double, dashed, dotted, thick, bold, fancy, rounded, 3d, shadow, double_line`.

## Imagem para ASCII

`image_to_ascii(path, width=100, ramp='standard', color=False, invert=False)`
em `image_art.py` converte um ficheiro de imagem real em ASCII, mapeando o
brilho de cada píxel (fórmula de luminância `0.299R+0.587G+0.114B`) para um
carácter de `ASCII_RAMPS`: `standard` (10 níveis), `detailed` (rampa longa,
mais gradação), `blocks` (blocos Unicode `░▒▓█`). Com `color=True`, cada
carácter é envolto em código ANSI 24-bit (`\033[38;2;R;G;Bm`) da cor real do
píxel, em vez de texto simples. Corrige o aspect-ratio do terminal ao
derivar a altura amostrada (`_ASPECT_CORRECTION = 0.55`).

Comando: `convert image <caminho> [width N] [color]` (ex: `convert image
/tmp/foto.png width 80 color`) — reconhecido em `ENCommandParser._parse_image_command`,
que corre ANTES do tokenizer genérico (que faz lower-case de tudo) para
preservar o caso original do caminho do ficheiro.

Único ponto do projeto com dependência de terceiros (Pillow, em
`requirements.txt`) — ver a exceção documentada em
`.claude/skills/generator-core/SKILL.md`.

## Animações

`spinner_animation(duration)` e `progress_bar(duration, char)` — bloqueantes, correm no terminal (não devolvem string).

## Sintaxe de comandos (linguagem natural, inglês)

O `ENCommandParser` extrai número(s), caracter, cor, fonte e estilo do texto livre, e suporta comandos compostos separados por `"and"` (cada parte é parseada independentemente por `_parse_single_command`, via `_split_compound_command`). Exemplos válidos:

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
convert image /tmp/photo.png width 80 color
```

### Limitações conhecidas do `ENCommandParser`

- **O separador `"and"` é baseado em palavras.** Uma lista de cores numa única forma (`"with color red and blue"`) pode ser lida por engano como duas formas — não há forma de desambiguar sem aspas/parâmetros nomeados.

## Ao adicionar uma forma/estilo novo

1. Implementar a função geradora em `ascii_art.py` (formas base) ou `smart_generator.py` (formas avançadas/padrões).
2. Registar sinónimos em `ENCommandParser.SHAPE_SYNONYMS` em `cli.py` — cuidado com chaves duplicadas no dict (uma chave repetida substitui silenciosamente a anterior em vez de a somar).
3. Adicionar/ajustar o mapeamento em `shape_to_command` e a lógica de `params` em `parse_command` (EN) que constrói o dict `{'command': ..., 'params': {...}}`.
4. Se a função geradora for usada dentro de `smart_generator.py` (fills/bordas/`smart_gen`), envolve-a em `_normalize_lines(...)` antes de a tratar como lista de linhas — funções de `ascii_art.py` devolvem `str` (`'\n'.join(...)`), enquanto as de `smart_generator.py` devolvem `List[str]`; iterar uma `str` dá caracteres, não linhas.
5. Atualizar esta skill com a nova entrada na tabela/lista relevante.
6. Testar com um comando real antes de dar como concluído.
