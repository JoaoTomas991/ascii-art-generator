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
| Espiral | `generate_spiral(size, char)` | ascii_art.py | size, char |
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
- `random_face()` / `random_animal()` / `random_emoji()` — geradores aleatórios de faces, animais (gato, cão, coruja, pinguim, peixe, urso, coelho, corvo) e emojis

## Texto para ASCII

`text_to_ascii(text, font)` com 4 fontes disponíveis (`FONTS` em ascii_art.py):
`small`, `block`, `banner`, `shadow` — cada uma com 5 linhas de altura, letras A-Z (algumas fontes também `!` e `?`).

## Banners e caixas

- `create_banner(text, width, char)` — faixa com borda e texto centrado
- `create_box(text, width, char)` — caixa à volta de texto (suporta multi-linha)

## Cores (ANSI) — `get_color_code(color_name)`

`black, red, green, yellow, blue, magenta, cyan, white` + variantes `bright_*`.
O `ENCommandParser` aceita sinónimos (`crimson/ruby→red`, `azure/cobalt→blue`, `purple/violet→magenta`, `pink→light_red`, etc.).

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

O `ENCommandParser` extrai número(s), caracter, cor, fonte e estilo do texto livre. Exemplos válidos:

```
draw a rectangle 10x5
make a circle with radius 8 color blue
write HELLO
draw a heart size 2
make a rectangle 8x4 with color cyan
```

### Limitações conhecidas do `ENCommandParser`

- **Sem suporte a comandos compostos.** `"a circle ... and a rectangle ..."` só desenha a primeira forma; os tokens da segunda parte são absorvidos como parâmetros errados da primeira (números e cor podem ficar trocados). Não uses "and" para combinar duas formas num único comando.
- **`"write TEXT with font X"` é frágil.** Se `X` coincidir com o nome de uma forma (ex.: `banner`), o comando é interpretado como criar essa forma em vez de converter texto. E mesmo sem colisão, o sufixo "with font X" pode ser absorvido para dentro do texto convertido.
- **`"style X"` está mapeado para `font`, não para `fill`.** Para pedir um preenchimento (dotted, striped, ...) em inglês, usa `fill X` em vez de `style X`.

## Ao adicionar uma forma/estilo novo

1. Implementar a função geradora em `ascii_art.py` (formas base) ou `smart_generator.py` (formas avançadas/padrões).
2. Registar sinónimos em `ENCommandParser.SHAPE_SYNONYMS` em `cli.py`.
3. Adicionar/ajustar o mapeamento em `shape_to_command` e a lógica de `params` em `parse_command` (EN) que constrói o dict `{'command': ..., 'params': {...}}`.
4. Atualizar esta skill com a nova entrada na tabela/lista relevante.
5. Testar com um comando real antes de dar como concluído.
