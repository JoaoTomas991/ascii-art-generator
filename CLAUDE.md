# ASCII Generator - Configuração do Agente

## Visão Geral do Projeto
Gerador de ASCII Art que cria arte a partir de texto, formas geométricas e padrões. O sistema entende comandos em português natural.

## Comportamento Geral
- **Idioma**: Responde sempre em **Português de Portugal** (PT-PT)
- **Tom**: Técnico, direto e amigável (sem emojis)
- **Estilo**: Soluções mínimas, focadas e bem testadas
- **Segurança**: Nunca executes código destrutivo, apagues ficheiros ou faças commit/push sem autorização explícita

## Estrutura do Código
- `ascii_art_generator/ascii_art.py` — geração de formas, texto e padrões
- `ascii_art_generator/cli.py` — interface de linha de comandos
- `ascii_art_generator/smart_generator.py` — geração "inteligente"/aleatória
- `ascii_art_generator/main.py` — ponto de entrada
- `run.py` / `start.sh` — scripts de arranque

## Capacidades do Projeto
O projeto suporta:
- **Formas geométricas**: retângulo, círculo, triângulo, coração, diamante, espiral, árvore
- **Texto para ASCII**: conversão de texto com múltiplas fontes (small, block, banner, shadow)
- **Padrões**: gradiente, tabuleiro (checkerboard), aleatório, abstrato
- **Animações**: spinner, barra de progresso
- **Banners e Caixas**: com texto personalizado
- **Estilos**:
  - **Cores**: vermelho, verde, azul, amarelo, ciano, magenta, branco, preto (e variantes claras)
  - **Preenchimento**: sólido, vazio, pontilhado, listrado, xadrez, cruz, estrela, gradiente, aleatório
  - **Bordas**: simples, dupla, tracejada, ondulada, negrito, fino, estrela, cruz

## Processamento de Comandos
- **Comandos simples**: "desenha um retangulo 10x5"
- **Comandos com estilos**: "faz um circulo com cor azul estilo pontilhado"
- **Comandos compostos**: "faz um circulo e um retangulo"
- **Parâmetros aceites**: cor, fonte, estilo, borda

## Fluxo de Trabalho Padrão
1. Analisa o comando do utilizador
2. Extrai forma/texto e parâmetros
3. Executa com os parâmetros extraídos
4. Mostra o resultado com formatação adequada
5. Testa sempre depois de implementar alterações

## Exemplos de Comandos Válidos
```
desenha um retangulo 10x5
desenha um circulo com raio 8
faz um coracao de tamanho 3
desenha um retangulo com estilo pontilhado cor verde
escreve OLA com fonte banner cor azul
faz um circulo e um retangulo
faz um circulo com cor azul e um retangulo 10x5 com cor vermelha
faz um banner com texto ASCII ART cor amarela borda estrela
```

## Regras de Parsing
- Suporta PT-PT e PT-BR (com e sem acentos)
- Múltiplas palavras para a mesma ação (ex: desenha/faz/cria)
- Comandos compostos usam "e", "com", "também" para separar

## Limitações Conhecidas
- Não suporta animações GIF (apenas terminal)
- Cores dependem de suporte ANSI do terminal
- Fontes limitadas às definições atuais (small, block, banner, shadow)
