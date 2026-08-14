# ASCII Generator - Agent Configuration

## Visao Geral do Projeto
Este e um gerador de ASCII Art que cria arte a partir de texto, formas geometricas e padroes. O sistema entende comandos em portugues natural.

## Instrucoes para o Agente

### Comportamento Geral
- **Idioma**: Responde sempre em **Portugues de Portugal** (PT-PT)
- **Tom**: Tecnico, direto e amigavel (sem emojis)
- **Estilo**: Solucoes minimas, focadas e bem testadas
- **Seguranca**: Nunca executes codigo destrutivo, apaga ficheiros ou faz commit/push sem autorizacao explicita

### Capacidades do Projeto
O projeto suporta:
- **Formas geometricas**: retangulo, circulo, triangulo, coracao, diamante, espiral, arvore
- **Texto para ASCII**: Conversao de texto com múltiples fontes
- **Padroes**: gradiente, tabuleiro (checkerboard), aleatorio, abstrato
- **Animacoes**: spinner, barra de progresso
- **Banners e Caixas**: Com texto personalizado
- **Estilos**:
  - **Fontes**: small (padrao), block, banner, shadow
  - **Cores**: vermelho, verde, azul, amarelo, ciano, magenta, branco, preto (e variants claras)
  - **Preenchimento**: solido, vazio, pontilhado, listrado, xadrez, cruz, estrela, gradiente, aleatorio
  - **Bordas**: simples, dupla, tracejada, ondulada, negrito, fino, estrela, cruz

### Processamento de Comandos
- **Comandos simples**: "desenha um retangulo 10x5"
- **Comandos com estilos**: "faz um circulo com cor azul estilo pontilhado"
- **Comandos compostos**: "faz um circulo e um retangulo"
- **Parametros espaciais**: cor, fonte, estilo, borda

### Fluxo de Trabalho Padrao
1. **Analise o comando** do utilizador
2. **Parseia** para estrutura de dados
3. **Executa** com os parametros extraidos
4. **Mostra resultado** com formatao adequada
5. **Testa** se necessario

### Exemplos de Comandos Validos
```
# Formas basicas
desenha um retangulo 10x5
desenha um circulo com raio 8
faz um coracao de tamanho 3

# Com estilos
desenha um retangulo com estilo pontilhado cor verde
escreve OLA com fonte banner cor azul

# Compostos
faz um circulo e um retangulo
faz um circulo com cor azul e um retangulo 10x5 com cor vermelha

# Banners e Caixas
faz um banner com texto ASCII ART cor amarela borda estrela
cria uma caixa com texto TESTE

# Animacoes
mostra uma animacao spinner
mostra barra de progresso
```

### Regras de Parsing
- **Idioma**: Suporta PT-PT e PT-BR (com e sem acentos)
- **Sinonimos**: Múltiplas palavras para a mesma acao (ex: desenha/faz/cria)
- **Comandos compostos**: Usam "e", "com", "tambem" para separar
- **Parametros**: cor, fonte, estilo, borda, preenchimento

### Testes e Validacao
- Sempre **testa** depois de implementar
- Usa comandos reais do utilizador para validar
- Mostra o resultado final ao utilizador
- Se o comando nao for reconhecido, sugere alternativas

### Limitacoes Conhecidas
- Nao suporta animações GIF (apenas terminal)
- Cores dependem de suporte ANSI do terminal
- Fontes limitadas a definicoes atuais (small, block, banner, shadow)

---
*Projeto: ASCII Generator*
*Versao: 1.0*
*Data: 2026-08-02*
