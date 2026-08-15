# ASCII Generator - Configuração do Agente

## Visão Geral do Projeto
Gerador de ASCII Art que cria arte a partir de texto, formas geométricas e padrões. A CLI entende comandos em **inglês** em linguagem natural (via `ENCommandParser`).

## Comportamento Geral
- **Idioma**: Responde sempre em **Português de Portugal** (PT-PT) — isto aplica-se à tua comunicação como agente, não à linguagem dos comandos da CLI (que é inglês, ver acima)
- **Tom**: Técnico, direto e amigável (sem emojis)
- **Estilo**: Soluções mínimas, focadas e bem testadas
- **Segurança**: Nunca executes código destrutivo, apagues ficheiros ou faças commit/push sem autorização explícita

## Estrutura do Código
- `ascii_art_generator/ascii_art.py` — geração de formas, texto e padrões
- `ascii_art_generator/cli.py` — interface de linha de comandos e `ENCommandParser` (parsing de linguagem natural em inglês)
- `ascii_art_generator/smart_generator.py` — formas avançadas, padrões de preenchimento/borda, geração "inteligente"/aleatória
- `ascii_art_generator/main.py` — ponto de entrada
- `run.py` / `start.sh` — scripts de arranque

## Capacidades do Projeto
O projeto suporta:
- **Formas geométricas**: retângulo, círculo, triângulo, coração, diamante, espiral, árvore, estrela, hexágono, oval, seta, pentágono, borboleta, flor
- **Texto para ASCII**: conversão de texto com múltiplas fontes (small, block, banner, shadow)
- **Padrões**: gradiente, tabuleiro (checkerboard), aleatório, abstrato
- **Animações**: spinner, barra de progresso
- **Banners e Caixas**: com texto personalizado
- **Estilos**:
  - **Cores**: red, green, blue, yellow, cyan, magenta, white, black (e variantes `bright_*`/`light_*`)
  - **Preenchimento**: solid, empty, dotted, striped, crosshatch, checkerboard, gradient, random, entre outros (30 padrões em `smart_generator.py`)
  - **Bordas**: simple, double, dashed, wavy, bold, light, fancy, rounded, entre outras

Ver a skill `ascii-art` (`.claude/skills/ascii-art/SKILL.md`) para o catálogo completo com funções/ficheiros/assinaturas.

## Fluxo de Trabalho Padrão
1. Analisa o comando do utilizador
2. Extrai forma/texto e parâmetros
3. Executa com os parâmetros extraídos
4. Mostra o resultado com formatação adequada
5. Testa sempre depois de implementar alterações

## Exemplos de Comandos Válidos
```
draw a rectangle 10x5
make a circle with radius 8
draw a heart size 2
write HELLO
make a rectangle 8x4 with color cyan
```

## Limitações Conhecidas
- `ENCommandParser` **não suporta comandos compostos** ("a circle ... and a rectangle ...") — só a primeira forma é desenhada, e os parâmetros da segunda parte podem contaminar a primeira. Ver `.claude/skills/ascii-art/SKILL.md` para detalhe.
- `"write TEXT with font X"` é frágil quando `X` coincide com o nome de uma forma (ex.: `banner`).
- `"style X"` está mapeado para `font`, não para `fill` — usa `fill X` para pedir um preenchimento.
- Não suporta animações GIF (apenas terminal)
- Cores dependem de suporte ANSI do terminal
- Fontes limitadas às definições atuais (small, block, banner, shadow)
