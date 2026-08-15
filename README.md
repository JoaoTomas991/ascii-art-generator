# ASCII Generator

Gerador de ASCII Art em Python: cria formas geométricas, converte texto em letras ASCII, gera padrões e animações simples de terminal — tudo através de comandos em linguagem natural (inglês) ou de um menu interativo.

## Requisitos

- Python 3.10+
- Sem dependências externas (só biblioteca standard)

## Instalação

```bash
git clone https://github.com/JoaoTomas991/ascii_generator.git
cd ascii_generator
```

Não há nada para instalar — corre-se diretamente com `python3`.

## Uso

Há três formas de usar o gerador:

### 1. Modo menu (interativo)

```bash
python3 run.py
# ou
make run
```

Mostra um menu com todas as formas, padrões, texto e animações disponíveis.

### 2. Modo inteligente (linguagem natural, dentro do menu)

No menu, escolhe `i` para entrar em modo inteligente e escreve comandos em inglês livremente:

```bash
python3 run.py --intelligent
# ou
make intelligent
```

### 3. Comando direto (uma linha, não interativo)

```bash
python3 run.py "draw a rectangle 10x5"
python3 run.py "make a circle with radius 8 color blue"
python3 run.py "write HELLO with font banner"
```

Também há atalhos no `Makefile`:

```bash
make command-draw      # draw a rectangle 10x5
make command-circle    # make a circle with radius 8
make command-heart     # draw a heart
make command-tree      # create a tree with height 10
make command-banner    # make a banner with text ASCII ART
make command-text      # write HELLO with font banner
```

Alternativa: `./start.sh` abre um pequeno menu de arranque (modo menu, modo inteligente, comando direto ou ajuda).

## Capacidades

- **Formas**: rectangle, circle, triangle, heart, diamond, spiral, tree, star, hexagon, oval, arrow, pentagon, butterfly, flower
- **Texto para ASCII**: 4 fontes — `small`, `block`, `banner`, `shadow`
- **Padrões**: gradient, checkerboard, abstract/random art
- **Aleatórios**: faces, animais (gato, cão, coelho, urso, peixe, pinguim, coruja, corvo), emojis
- **Banners e caixas** com texto personalizado
- **Animações de terminal**: spinner, barra de progresso
- **Estilo**: cor (ANSI: red, green, blue, yellow, cyan, magenta, white, black + variantes `bright_*`), até 31 padrões de preenchimento e várias bordas — ver `.claude/skills/ascii-art/SKILL.md` para o catálogo completo com funções e ficheiros

### Exemplos de comandos

```
draw a rectangle 10x5
make a circle with radius 8 color blue
draw a heart size 2
write HELLO
make a rectangle 8x4 with color cyan
```

### Limitações conhecidas

- Os comandos em inglês (`ENCommandParser`) **não suportam comandos compostos** — `"a circle ... and a rectangle ..."` só desenha a primeira forma.
- `"write TEXT with font X"` pode falhar se `X` coincidir com o nome de uma forma (ex.: `banner`).
- `"style X"` está mapeado para a fonte, não para o preenchimento — usa `fill X` para pedir um padrão de preenchimento.
- Sem animações GIF (só terminal); cores dependem de suporte ANSI do terminal.

## Estrutura do projeto

```
ascii_art_generator/
├── ascii_art.py        # formas base, fontes, padrões, banners, animações
├── cli.py              # ENCommandParser + interface de linha de comandos
├── smart_generator.py  # formas avançadas, padrões de preenchimento/borda, geração aleatória
└── main.py             # ponto de entrada

run.py       # script de arranque (menu / inteligente / comando direto)
start.sh     # menu de arranque interativo
Makefile     # atalhos de execução e testes
```

## Testar

```bash
make test
```

Corre um smoke test aos imports principais e ao parser de comandos.

## Desenvolvimento com Claude Code

O projeto inclui `CLAUDE.md` com as convenções do agente e uma skill (`.claude/skills/ascii-art/SKILL.md`) com o catálogo completo de formas, fontes, cores, preenchimentos e bordas — consulta-os antes de adicionar uma forma ou estilo novo.
