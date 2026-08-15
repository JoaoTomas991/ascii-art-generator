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

## Formas geométricas

| Forma | Função | Ficheiro | Parâmetros principais |
|---|---|---|---|
| Retângulo | `draw_rectangle(width, height, char, filled)` | ascii_art.py | width, height, char, filled |
| Triângulo | `draw_triangle(height, char, direction)` | ascii_art.py | height, char, direction: up/down/left/right |
| Círculo | `draw_circle(radius, char)` | ascii_art.py | radius, char |
| Coração | `draw_heart(size, char)` | ascii_art.py | size: 1–3 apenas (padrões fixos) |
| Diamante | `draw_diamond(size, char)` | ascii_art.py | size, char |
| Árvore | `generate_tree(height, char)` | ascii_art.py | height, char |
| Espiral | `generate_spiral(size, char)` | ascii_art.py | size, char (espiral de Arquimedes traçada na grelha, não um preenchimento sólido) |
| Estrela | `draw_star(...)` | smart_generator.py | — |
| Hexágono | `draw_hexagon(...)` | smart_generator.py | — |
| Oval | `draw_oval(...)` | smart_generator.py | — |
| Seta | `draw_arrow(...)` | smart_generator.py | — |
| Pentágono | `draw_pentagon(...)` | smart_generator.py | — |
| Borboleta | `draw_butterfly(...)` | smart_generator.py | — |
| Flor | `draw_flower(...)` | smart_generator.py | — |

## Padrões

- `generate_gradient(width, height)` — degradê de densidade de caracteres
- `generate_checkerboard(size, chars)` — tabuleiro/xadrez
- `random_abstract(width, height)` — arte abstrata aleatória
- `random_face()` / `random_animal()` / `random_emoji()` — geradores aleatórios de faces, animais (gato, cão, coruja, pinguim, peixe, urso, coelho, corvo) e emojis (`face`/`emoji` são chaves de forma distintas em `ENCommandParser.SHAPE_SYNONYMS` — "emoji"/"emoticon" já não caem em `random_face`)

## Texto para ASCII

`text_to_ascii(text, font)` com 4 fontes disponíveis (`FONTS` em ascii_art.py):
`small`, `block`, `banner`, `shadow` — cada uma com 5 linhas de altura, letras A-Z (algumas fontes também `!` e `?`).

## Banners e caixas

- `create_banner(text, width, char)` — faixa com borda e texto centrado
- `create_box(text, width, char)` — caixa à volta de texto (suporta multi-linha)

## Cores (ANSI) — `get_color_code(color_name)`

`black, red, green, yellow, blue, magenta, cyan, white` + variantes `bright_*`.
O `ENCommandParser` aceita sinónimos (`crimson/ruby→red`, `azure/cobalt→blue`, `purple/violet→magenta`, `pink→light_red`, etc.).

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

## Bordas

Básico (`get_border_chars` em ascii_art.py): `simple, double, dashed, wavy, bold, light, star, plus`.

Avançado (`SmartGenerator.BORDER_STYLES`): `none, simple, double, dashed, dotted, thick, bold, fancy, rounded, 3d, shadow, double_line`.

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
