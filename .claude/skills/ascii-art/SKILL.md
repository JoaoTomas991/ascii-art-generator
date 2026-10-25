---
name: ascii-art
description: Catálogo de referência das formas, fontes, cores, padrões de preenchimento e estilos de borda deste gerador de ASCII Art. Usar sempre que fores gerar/desenhar arte ASCII, adicionar uma forma nova, ou explicar a sintaxe de comandos do projeto.
---

# Catálogo do ASCII Art Generator

Referência com base no código real do projeto (não invenção) — usa isto para
garantir consistência com o que já existe antes de gerar exemplos ou adicionar
funcionalidades novas.

## Onde vive cada coisa

- `ascii_art_generator/ascii_art.py` — formas base, fontes, padrões, banners/caixas, animações, cores ANSI.
- `ascii_art_generator/smart_generator.py` — formas avançadas (estrela, hexágono, oval, seta, pentágono, borboleta, flor), padrões de preenchimento e bordas ricas, geração "inteligente" (`smart_gen`).
- `ascii_art_generator/cli.py` — `ENCommandParser`, que converte comandos em inglês (linguagem natural) nos parâmetros das funções abaixo. É o único parser usado pela `ASCIIArtCLI` (o antigo `PTCommandParser`, nunca ligado à aplicação, foi removido).
- `ascii_art_generator/animal_scenes.py` — `animal_scene(name, big, setting)`: animal numa moeda (`$NOME`), moldura ou cena temática (meadow, rain, snow, beach, space, forest); devolve `(linhas, tipo)` e `scene_color(tipo)` sugere a cor. Usado por `smart_gen.generate_animal_art()`.
- `ascii_art_generator/emoji_art.py` — `emoji_face(mood)`: cara grande (11 linhas, ASCII puro) composta por cabeça, olhos, sobrancelhas, boca e extras (corações, lágrimas, `zZ`, brilhos); 13 humores (happy, laugh, wink, sad, angry, surprised, cool, love, sleepy, calm, dizzy, starstruck, silly). `mood` aceita também os humores do parser (`MOOD_FACES`: happy/sad/angry/calm/sleepy), por isso `draw a sad emoji` dá uma cara triste. Devolve `(linhas, humor)` e `emoji_color(humor)` sugere a cor. `random_emoji(big=True)` usa-o; `big=False` devolve o kaomoji de uma linha.
- `ascii_art_generator/install_info.py` — `describe()` (`--version`) e `stale_copy_warning()` (aviso quando o comando instalado é uma cópia mais antiga da pasta de origem; ver `run.py`).
- `ascii_art_generator/learned_words.py` / `console.py` — persistência dos moods ensinados (`~/.config/ascii_generator/learned_words.json`); configuração UTF-8 do stdout.
- `ascii_art_generator/intro.py` — banner de arranque animado e menu animado, só biblioteca padrão. `show_intro()` toca a entrada (logo em arco-íris, régua `━`, subtítulo escrito letra a letra); `banner_lines()` devolve `(logo, [régua, subtítulo, régua])` em texto simples; `title_lines()` desenha `ASCII` com a fonte `solid` (alias do `banner` do pyfiglet, ou `block` interna sem pyfiglet) esticada 2x na horizontal; `LiveLines(targets, min_cols)` é a thread que redesenha linhas já impressas (ESC 7 / cursor-up / ESC 8) enquanto `input()` bloqueia. Desliga-se sozinha fora de um terminal, com `TERM=dumb`, com `--no-animation` ou `ASCII_GENERATOR_NO_ANIMATION=1`, e quando o terminal é mais estreito do que a linha mais larga.
- `ascii_art_generator/web_bridge.py` — `run_command(texto)`: corre um comando pelo mesmo pipeline do CLI, captura o `stdout` e devolve-o (com códigos ANSI) como `str`; trata `teach`, comandos que não percebe, `q`/`exit`/`menu` e recusa tamanhos acima de 300. Usado só pela página web.
- `web/` + `scripts/build_web.py` — versão estática para browser (`index.html`, `style.css`, `app.js`): corre o pacote dentro do Pyodide, converte ANSI em HTML. `python3 scripts/build_web.py [--serve]` (ou `make web`) gera `_site/`; `.github/workflows/pages.yml` publica no GitHub Pages.
- `ascii_art_generator/image_art.py` — `image_to_ascii(path, width, ramp, color, invert)`, converte um ficheiro de imagem real (PNG/JPG/...) em ASCII art por rampa de brilho. Único módulo do projeto com dependência de terceiros (Pillow — ver `.claude/skills/generator-core/SKILL.md`).

## Formas geométricas

| Forma | Função | Ficheiro | Parâmetros principais |
|---|---|---|---|
| Retângulo | `draw_rectangle(width, height, char, filled)` | ascii_art.py | width, height, char, filled |
| Triângulo | `draw_triangle(height, char, direction)` | ascii_art.py | height, char, direction: up/down/left/right |
| Círculo | `draw_circle(radius, char)` | ascii_art.py | radius, char (corrige aspect-ratio do terminal — ver nota abaixo) |
| Coração | `draw_heart(size, char)` | ascii_art.py | size: 1–12 na função, default 6; o parser limita a 1–8 (gerado algoritmicamente, escala com o tamanho) |
| Diamante | `draw_diamond(size, char)` | ascii_art.py | size, char |
| Árvore | `generate_tree(height, char)` | ascii_art.py | height, char |
| Espiral | `generate_spiral(size, char)` | ascii_art.py | size, char (espiral de Arquimedes traçada na grelha, não um preenchimento sólido) |
| Estrela | `draw_star(size, char)` | smart_generator.py | size 3–12, default 7; 5 pontas, ponta para cima |
| Hexágono | `draw_hexagon(size, char)` | smart_generator.py | size mínimo 2, default 8 |
| Oval | `draw_oval(width, height, char)` | smart_generator.py | width, height (default 40x8); amostra o centro de cada célula; no comando aceita `30x8` ou um só número (largura, com altura = largura // 5) |
| Seta | `draw_arrow(direction, size, char)` | smart_generator.py | direction: right/left/up/down, size |
| Pentágono | `draw_pentagon(size, char)` | smart_generator.py | size, default 8; pentágono regular com a ponta para cima |
| Borboleta | `draw_butterfly(size, char)` | smart_generator.py | size mínimo 5; asas superiores e inferiores, corpo e antenas |
| Flor | `draw_flower(size, char)` | smart_generator.py | size mínimo 4; 5 pétalas elípticas, anel oco e caule `\|` (o caule ignora `char`); corrige aspect-ratio |

**Aspect-ratio do terminal**: os carateres são ~2x mais altos que largos, por
isso `draw_circle` e `draw_flower` fazem o scan do eixo `x` a
resolução dupla e dividem por 2 antes do cálculo de distância — sem isto a
forma sai "ovalada"/esticada na vertical em vez de redonda. Ao criar uma
forma nova baseada em distância radial, replica esta correção. A estrela e o
pentágono usam `_rasterize_polygon(poly, char)` (smart_generator.py), que
rasteriza um polígono em unidades quadradas e estica o `x` 2x; `draw_heart`
amostra a curva implícita `(x²+y²-1)³ - x²y³ ≤ 0` na mesma grelha
(grelha de `5*size+1` linhas e ~2,1x de colunas; as linhas vazias das pontas são cortadas, por isso o desenho final tem 6, 11, 16, 21, 25, 30... linhas).

## Padrões

- `generate_gradient(width, height)` — degradê de densidade de caracteres
- `generate_checkerboard(size, chars)` — tabuleiro/xadrez
- Arte aleatória: `random`, `art` e `painting` (ex. `make random art`, `make a painting 20x10 color red`) vão para `ASCIIArtCLI._random_art()` → `smart_gen.generate_interesting_art("random", w, h)` (já não existe `random_abstract`; era ruído puro sem estrutura). O tamanho é só uma indicação para o gerador, não uma dimensão exata. Cor explícita substitui a que o gerador escolher. `abstract`/`pattern`/`design` são outra coisa: estilo `abstract` do modo inteligente (`generate_from_command`), sem tamanho nem cor
- `random_animal()` (desenho simples; o comando/menu "random animal" usa `smart_gen.generate_animal_art()` → `animal_scenes.animal_scene()`: moeda `$NOME`, moldura ou cena, com decoração/cor aleatórias) / `random_emoji()` — geradores aleatórios de animais (gato, cão, coruja, pinguim, peixe, urso, coelho, corvo/gralha `crow`, corvo-real `raven`) e emojis. Cada animal com desenho próprio tem também uma versão maior em `ANIMALS_BIG` (mesmas chaves que `ANIMALS`), usada quando o comando inclui `big`/`large`/`huge`/`giant` (`ENCommandParser.BIG_WORDS` → `params['big']` → `get_animal_art(name, big)`), ex. `draw a big cat`. O `random animal`/`draw an animal` usa o desenho grande por omissão (`big=True`); `a random animal`/`a random emoji` são lidos como animal/emoji, não como arte aleatória

## Texto para ASCII

`text_to_ascii(text, font)` com 4 nomes de fonte: `small`, `block`, `banner`, `shadow` (mais o alias `solid` → fonte `banner` do pyfiglet, usado só pelo logo). Se o terminal for mais estreito do que uma letra, o pyfiglet lança `CharNotPrinted`; `_figlet_to_ascii` apanha-o e volta a renderizar sem quebra de linha.

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

Avançado (`SmartGenerator.FILL_PATTERNS` em smart_generator.py — 32 padrões):
`solid, empty, dotted, striped, horizontal_stripes, vertical_stripes, cross, crosshatch, diagonal, anti_diagonal, x_pattern, grid, checkerboard, dense_checkerboard, random, sparse_random, dense_random, dots, stars, plus_signs, mixed, left_gradient, right_gradient, top_gradient, bottom_gradient, center_gradient, dense_gradient, spiral_pattern, concentric, wave, zigzag, honeycomb`.

Os 6 `*_gradient` usam `create_directional_gradient` — uma rampa de
densidade suave (`GRADIENT_RAMP = ' .:-=+*#%@'`), não um corte binário
metade/metade. `dense_gradient` é o da esquerda para a direita, mas com
`DENSE_GRADIENT_RAMP = '=+*#%@'` (só a metade pesada), para formas sem
células vazias ou quase vazias. `gradient` sozinho é sinónimo de
`left_gradient`.

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

`apply_border` mantém sempre o conteúdo da forma (já houve versões de
`bold`/`thick`/`double_line`/`3d` que o apagavam) e a moldura tem a largura
das linhas mais as margens (`fancy`, `rounded` e `thick` +4; `bold` e
`double_line` +2; `3d` +3, contando o recuo da sombra). O fill `empty` não usa o retângulo da caixa: `mask_fill_pattern`
desenha o contorno da própria silhueta.

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
draw a star 8 color yellow
make an oval 30x8 color green
draw a triangle 5
convert image /tmp/photo.png width 80 color
```

Um número solto vai para a chave que o executor lê: `height` (`triangle`,
`tree`), `width`+`height` (`rectangle`, `oval`), `radius` (`circle`) e `size`
(`heart`, `diamond`, `spiral`, `star`, `hexagon`, `pentagon`, `butterfly`,
`flower`, `arrow`). Se a chave escrita pelo parser não coincidir com a lida
em `execute_parsed_command`, o número é ignorado em silêncio.

### Limitações conhecidas do `ENCommandParser`

- **O separador `"and"` é baseado em palavras.** Uma lista de cores numa única forma (`"with color red and blue"`) é lida como um comando composto de uma só parte: aplica a primeira cor, descarta a segunda e imprime um cabeçalho `[1/1]` — não há forma de desambiguar sem aspas/parâmetros nomeados.

## Ao adicionar uma forma/estilo novo

1. Implementar a função geradora em `ascii_art.py` (formas base) ou `smart_generator.py` (formas avançadas/padrões).
2. Registar sinónimos em `ENCommandParser.SHAPE_SYNONYMS` em `cli.py` — cuidado com chaves duplicadas no dict (uma chave repetida substitui silenciosamente a anterior em vez de a somar).
3. Adicionar/ajustar o mapeamento em `shape_to_command` e a lógica de `params` em `parse_command` (EN) que constrói o dict `{'command': ..., 'params': {...}}`.
4. Se a função geradora for usada dentro de `smart_generator.py` (fills/bordas/`smart_gen`), envolve-a em `_normalize_lines(...)` antes de a tratar como lista de linhas — funções de `ascii_art.py` devolvem `str` (`'\n'.join(...)`), enquanto as de `smart_generator.py` devolvem `List[str]`; iterar uma `str` dá caracteres, não linhas.
5. Atualizar esta skill com a nova entrada na tabela/lista relevante.
6. Testar com um comando real antes de dar como concluído.
