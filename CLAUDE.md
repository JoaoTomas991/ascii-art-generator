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
- `ascii_art_generator/image_art.py` — conversão de imagem real (PNG/JPG/...) para ASCII por rampa de brilho; dependência de terceiros Pillow (ver `requirements.txt`); a outra dependência opcional é o `pyfiglet`, importado só dentro de `text_to_ascii()` em `ascii_art.py`
- `ascii_art_generator/animal_scenes.py` — animal aleatório numa moeda, moldura ou cena temática
- `ascii_art_generator/emoji_art.py` — cara de emoji grande composta por cabeça, olhos, sobrancelhas, boca e extras
- `ascii_art_generator/learned_words.py` — persistência dos sinónimos de mood ensinados (`teach`)
- `ascii_art_generator/console.py` / `install_info.py` — UTF-8 no stdout; `--version` e aviso de cópia instalada desatualizada
- `ascii_art_generator/intro.py` — banner de arranque animado (`show_intro`, `banner_lines`) e `LiveLines`, a thread que continua a animar linhas já impressas enquanto o menu espera por `input()`; só biblioteca padrão
- `ascii_art_generator/web_bridge.py` — `run_command(texto)`: corre um comando e devolve o que ele imprime (com ANSI) como `str`; usado pela versão web
- `ascii_art_generator/main.py` — ponto de entrada
- `run.py` / `start.sh` — scripts de arranque (`run.py --no-animation` desliga a animação)
- `web/` + `scripts/build_web.py` — versão estática para browser (Pyodide); `make web` constrói `_site/` e serve em `localhost:8000`; `.github/workflows/pages.yml` publica no GitHub Pages

## Skills e Subagentes deste Projeto
- `.claude/skills/ascii-art/SKILL.md` — catálogo completo de formas/fontes/cores/estilos
- `.claude/skills/generator-core/SKILL.md` — convenções e armadilhas ao editar `ascii_art_generator/*.py` (consulta antes de mexer no core)
- `.claude/skills/generator-test-battery/SKILL.md` — a bateria de testes de regressão em si (o quê testar); pode ser invocada inline ou pelo subagent abaixo
- `.claude/agents/generator-tester.md` — subagent fino que invoca a skill acima num contexto isolado e devolve só um relatório PASS/FAIL; invoca-o sempre depois de alterar `ascii_art.py`, `cli.py`, `smart_generator.py`, `intro.py`, `web_bridge.py` ou `main.py`
- `.claude/agents/shape-coverage-auditor.md` — subagent que testa exaustivamente todos os sinónimos declarados (todas as formas/cores/fontes) contra o pipeline real, para apanhar formas mortas/inalcançáveis e chaves duplicadas nos dicionários de sinónimos. Usa antes de um release ou depois de adicionar várias formas.
- `.claude/agents/docs-sync-auditor.md` — subagent que compara as afirmações em README/CLAUDE/AGENTS/skill `ascii-art` (contagens, listas, exemplos, limitações) contra o código real e reporta desvios. Usa antes de publicar o repositório ou cortar um release.
- `.claude/agents/pitfall-reviewer.md` — subagent de revisão especializado nos 6 padrões de bug já vistos neste projeto (mismatch `str`/`List[str]`, chaves duplicadas, mismatch de argumentos, mismatch de chave de parâmetro, off-by-one na captura de texto, dicionários de dados duplicados entre ficheiros). Invoca-o antes de commit/PR que toque em `ascii_art_generator/*.py`.
- `.claude/skills/adr/SKILL.md` — como documentar decisões de arquitetura significativas em `docs/adr/`
- `.claude/skills/pre-commit/SKILL.md` — orquestra `generator-tester` + `pitfall-reviewer` em paralelo e junta os relatórios num veredicto; usa antes de commit/PR que toque em `ascii_art_generator/*.py`
- `.claude/skills/release-check/SKILL.md` — orquestra `generator-tester`, `shape-coverage-auditor`, `docs-sync-auditor` (e `pitfall-reviewer` desde a última tag) em paralelo; usa antes de um release (tag `v*`) ou de publicar o repositório

## Capacidades do Projeto
O projeto suporta:
- **Formas geométricas**: retângulo, círculo, triângulo, coração, diamante, espiral, árvore, estrela (5 pontas), hexágono, oval, seta, pentágono, borboleta, flor. Um número solto no comando dá o tamanho da forma (`draw a star 8`, `draw a triangle 5`); o oval aceita `30x8`
- **Texto para ASCII**: conversão de texto com múltiplas fontes (small, block, banner, shadow), (nota: `banner` aponta para a fonte FIGlet `banner3`, que a versão atual do pyfiglet não traz, por isso `write ... with font banner` acaba na `small`; mais o alias `solid`, a fonte `banner` do pyfiglet usada no logo), renderizadas com fontes FIGlet reais via `pyfiglet` (opcional; aceita também qualquer outro nome de fonte FIGlet, ex. `slant`) e com fallback para as fontes internas de 5 linhas se o pyfiglet não estiver instalado
- **Padrões**: gradiente, tabuleiro (checkerboard), aleatório, abstrato
- **Animações**: spinner, barra de progresso
- **Banners e Caixas**: com texto personalizado
- **Estilos**:
  - **Cores**: red, green, blue, yellow, cyan, magenta, white, black (e variantes `bright_*`/`light_*`), mais `rainbow`/`multicolor` (cicla uma cor por linha)
  - **Preenchimento**: solid, empty, dotted, striped, crosshatch, checkerboard, gradient (rampa de densidade real, não binária), random, entre outros (32 padrões em `smart_generator.py`, incluindo `dense_gradient`, que usa só a metade pesada da rampa) — sempre aplicado só dentro da silhueta da forma (`mask_fill_pattern`), nunca substituindo-a por um retângulo
  - **Bordas**: simple, double, dashed, wavy, bold, light, fancy, rounded, entre outras (12 em `smart_generator.py`); todas preservam o conteúdo da forma e têm a moldura com a largura das linhas. O preenchimento `empty` desenha o contorno da silhueta, não o retângulo da caixa
- **Moods**: happy, sad, angry, calm, sleepy — cada um aplica uma cor por omissão (a menos que o utilizador já tenha indicado `color`). Novos sinónimos podem ser ensinados em runtime no modo inteligente com `teach <word> as <mood>`, e ficam persistidos entre sessões em `~/.config/ascii_generator/learned_words.json`
- **Banner e menu animados**: o menu é um banner (logo `ASCII` em fonte pesada esticada na horizontal, subtítulo `G E N E R A T O R`) mais as categorias em até 3 colunas; o logo, o subtítulo e a linha `━` por cima do prompt animam em arco-íris enquanto o menu espera. A animação só corre num terminal interativo e desliga-se com `--no-animation`, `ASCII_GENERATOR_NO_ANIMATION=1` ou `TERM=dumb`; em terminais com menos de 66 colunas fica estática, e só anima as linhas que ainda estão visíveis (banner e menu cabem em cerca de 24 linhas com 69 colunas ou mais, e em cerca de 29 linhas com 66 a 68 colunas, quando o menu passa a 2 colunas)
- **Versão web**: `web/` corre o gerador a sério no browser com Pyodide (sem servidor); `make web` para experimentar localmente; `?cmd=` na URL corre um comando ao abrir; tamanhos acima de 300 são recusados para não bloquear o separador
- **Imagem para ASCII**: `convert image <caminho> [width N] [color]` converte um ficheiro de imagem real (PNG/JPG/...) numa rampa de brilho ASCII, com opção de cor real 24-bit por carácter (`ascii_art_generator/image_art.py`, requer Pillow — `pip install -r requirements.txt`)

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
make a rectangle 8x4 with color cyan style dotted
make a spiral 20
make an emoji
make a circle with radius 5 color blue and a rectangle 10x5 color red
teach ecstatic as happy
draw an ecstatic heart
draw a heart size 4 color rainbow
draw a star 8 color yellow
make an oval 30x8 color green
draw a big cat color yellow
convert image /tmp/photo.png width 80 color
```

## Limitações Conhecidas
- Não suporta animações GIF (apenas terminal)
- Cores dependem de suporte ANSI do terminal
- Sem `pyfiglet` instalado, as fontes ficam limitadas às definições internas (small, block, banner, shadow: só A-Z e alguma pontuação; caracteres em falta aparecem como `?`)
- A animação do menu usa a posição relativa das linhas já impressas: se o utilizador escrever no prompt uma linha mais comprida do que o terminal, o texto quebra e a animação pode desenhar uma linha fora do sítio até ao Enter
- O separador de comandos compostos (`"and"`) é baseado em palavras — uma lista de cores numa única forma (`"with color red and blue"`) pode ser lida por engano como duas formas
