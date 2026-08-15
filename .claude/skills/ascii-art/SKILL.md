---
name: ascii-art
description: Catálogo de referência das formas, fontes, cores, padrões de preenchimento e estilos de borda deste gerador de ASCII Art. Usar sempre que fores gerar/desenhar arte ASCII, adicionar uma forma nova, ou explicar a sintaxe de comandos PT do projeto.
---

# Catálogo do ASCII Generator

Referência com base no código real do projeto (não invenção) — usa isto para
garantir consistência com o que já existe antes de gerar exemplos ou adicionar
funcionalidades novas.

## Onde vive cada coisa

- `ascii_art_generator/ascii_art.py` — formas base, fontes, padrões, banners/caixas, animações, cores ANSI.
- `ascii_art_generator/smart_generator.py` — formas avançadas (estrela, hexágono, oval, seta, pentágono, borboleta, flor), padrões de preenchimento e bordas ricas, geração "inteligente" (`smart_gen`).
- `ascii_art_generator/cli.py` — `PTCommandParser` (comandos em português) e `ENCommandParser` (inglês), que convertem linguagem natural nos parâmetros das funções abaixo.

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
No parser PT há sinónimos (`vermelho→red`, `azul→blue`, `roxo→magenta`, etc.).

## Preenchimento (fill)

Básico (`get_fill_style_pattern` em ascii_art.py): `empty, solid, dotted, striped_h, striped_v, crosshatch, plus, star, random, gradient`.

Avançado (`SmartGenerator.FILL_PATTERNS` em smart_generator.py — 30 padrões):
`solid, empty, dotted, striped, horizontal_stripes, vertical_stripes, cross, crosshatch, diagonal, anti_diagonal, x_pattern, grid, checkerboard, dense_checkerboard, random, sparse_random, dense_random, dots, stars, plus_signs, mixed, left_gradient, right_gradient, top_gradient, bottom_gradient, center_gradient, spiral_pattern, concentric, wave, zigzag, honeycomb`.

## Bordas

Básico (`get_border_chars` em ascii_art.py): `simple, double, dashed, wavy, bold, light, star, plus`.

Avançado (`SmartGenerator.BORDER_STYLES`): `none, simple, double, dashed, dotted, thick, bold, fancy, rounded, 3d, shadow, double_line`.

## Animações

`spinner_animation(duration)` e `progress_bar(duration, char)` — bloqueantes, correm no terminal (não devolvem string).

## Sintaxe de comandos (linguagem natural)

O `PTCommandParser`/`ENCommandParser` aceitam comandos compostos (separados por "e"/"com"/"and"/"with") e extraem número(s), caracter, cor, fonte, estilo e borda do texto livre. Exemplos válidos:

```
desenha um retangulo 10x5
faz um circulo com raio 8 cor azul
escreve OLA com fonte banner
faz um coracao de tamanho 2
faz um circulo com cor azul e um retangulo 10x5 com cor vermelha
draw a rectangle 10x5 with color blue style dotted
```

## Ao adicionar uma forma/estilo novo

1. Implementar a função geradora em `ascii_art.py` (formas base) ou `smart_generator.py` (formas avançadas/padrões).
2. Registar sinónimos em `PTCommandParser.SHAPE_SYNONYMS` (e `ENCommandParser.SHAPE_SYNONYMS` se aplicável) em `cli.py`.
3. Adicionar branch de parsing em `_parse_single_command` (PT) / `parse_command` (EN) que constrói o dict `{'command': ..., 'params': {...}}`.
4. Atualizar esta skill com a nova entrada na tabela/lista relevante.
5. Testar com um comando real antes de dar como concluído.
