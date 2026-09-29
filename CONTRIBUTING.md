# Contributing to ASCII Generator

Obrigado por quereres contribuir para o **ASCII Generator**.

Este é um projeto pessoal, mantido por um único colaborador. As contribuições externas são bem-vindas, mas todas as alterações devem ser propostas através de issues e pull requests para manter o projeto organizado.

## Como começar

1. Cria um fork do repositório.
2. Clona o teu fork:

   ```bash
   git clone https://github.com/SEU_UTILIZADOR/ascii_generator.git
   cd ascii_generator
   ```

3. Adiciona o repositório original como `upstream`:

   ```bash
   git remote add upstream https://github.com/JoaoTomas991/ascii_generator.git
   ```

4. Cria um ambiente virtual e instala as dependências:

   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

   No Windows, a ativação pode ser feita com:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

## Requisitos técnicos

- Python **3.12 ou superior**
- `pip`
- Pillow, através de `requirements.txt`, quando forem utilizadas funcionalidades de conversão de imagens

## Issues

Antes de começares uma alteração significativa, abre uma issue para explicar a proposta. Isto ajuda a evitar trabalho duplicado e permite discutir a solução antes da implementação.

Ao abrir uma issue:

- Usa um título claro e específico.
- Explica o problema ou a melhoria pretendida.
- Inclui passos para reproduzir um erro, quando aplicável.
- Adiciona exemplos de comandos e resultados esperados.
- Indica a versão do Python utilizada.

## Branches

A branch principal é `main`. Não devem ser feitas alterações diretamente nessa branch através de contribuições externas.

Cria uma branch descritiva a partir de `main`:

```bash
git fetch upstream
git checkout main
git rebase upstream/main
git checkout -b tipo/nome-da-alteracao
```

Convenções recomendadas:

- `feature/nova-funcionalidade`
- `fix/correcao-do-erro`
- `docs/atualizacao-da-documentacao`
- `test/adicao-de-testes`
- `refactor/melhoria-do-codigo`

## Desenvolvimento

O código principal está em `ascii_art_generator/`. Antes de enviares alterações:

```bash
make test
```

Também deves testar manualmente os comandos relacionados com a alteração. Por exemplo:

```bash
python3 run.py "draw a rectangle 10x5"
python3 run.py "write HELLO"
```

Se alterares a conversão de imagens, testa também com uma imagem real e confirma que a dependência Pillow está instalada.

## Padrões de código

- Usa Python 3.12+.
- Segue as convenções da PEP 8.
- Usa nomes claros para variáveis, funções e classes.
- Mantém as funções focadas e simples.
- Adiciona docstrings a funções e classes públicas.
- Evita adicionar dependências externas sem discutir primeiro numa issue.
- Atualiza o README ou a documentação quando o comportamento do projeto mudar.
- Mantém a compatibilidade com as funcionalidades existentes, salvo quando a alteração for explicitamente incompatível.

Quando fizer sentido, usa ferramentas de formatação, linting e verificação de tipos no código alterado. O projeto deve continuar sem erros nos testes existentes.

## Pull requests

As alterações devem ser submetidas através de uma pull request dirigida à branch `main`.

Uma pull request deve:

- Ter um título claro.
- Explicar o que foi alterado e porquê.
- Referenciar a issue relacionada, por exemplo `Closes #12`.
- Incluir testes realizados.
- Atualizar a documentação, se necessário.
- Ser limitada a uma alteração coerente, evitando misturar funcionalidades sem relação.

Exemplo de estrutura para a descrição:

```markdown
## Resumo
Descreve brevemente a alteração.

## Issue relacionada
Closes #12

## Testes
- [ ] `make test`
- [ ] Testes manuais realizados
- [ ] Documentação atualizada, quando aplicável

## Notas
Indica limitações, decisões ou possíveis impactos.
```

### Revisão e aprovação

Uma revisão de código é a análise da pull request antes de ela ser integrada na branch `main`. Durante a revisão podem ser verificados:

- Correção do comportamento implementado.
- Qualidade e legibilidade do código.
- Testes suficientes e bem direcionados.
- Compatibilidade com Python 3.12+.
- Ausência de alterações desnecessárias.
- Atualização da documentação.

Como o projeto é mantido atualmente por uma só pessoa, não existe um número mínimo fixo de revisores. O mantenedor pode rever e aprovar a pull request sozinho. À medida que o projeto tiver mais colaboradores, esta regra poderá ser alterada para exigir, por exemplo, uma aprovação de outro colaborador antes do merge.

Não faças merge de uma pull request enquanto existirem alterações importantes por resolver ou testes a falhar.

## Commits

Usa mensagens no formato **Conventional Commits**:

```text
<tipo>(<âmbito>): <descrição>
```

Tipos recomendados:

- `feat`: nova funcionalidade
- `fix`: correção de um erro
- `docs`: documentação
- `test`: testes
- `refactor`: alteração interna sem mudança de comportamento
- `chore`: manutenção ou configuração
- `perf`: melhoria de desempenho

Exemplos:

```text
feat(shapes): add pentagon drawing support
fix(cli): handle quoted command arguments
docs: update installation instructions
test(parser): cover compound commands
```

Escreve as mensagens no imperativo, de forma curta e específica. Evita mensagens como `update`, `changes` ou `fix stuff`.

## Dependências

As dependências devem ser adicionadas apenas quando forem necessárias. Cada nova dependência deve:

- Ser justificada na pull request.
- Ser adicionada a `requirements.txt`.
- Ser compatível com Python 3.12+.
- Ser documentada no README, quando afetar a instalação ou utilização.

## Alterações arquiteturais

Para alterações relevantes na arquitetura ou no comportamento geral do projeto:

1. Abre uma issue para discutir a proposta.
2. Explica as alternativas consideradas.
3. Atualiza ou cria um Architecture Decision Record em `docs/adr/`, quando aplicável.
4. Atualiza a documentação relacionada.

## Relatórios de segurança

Não publiques informação sensível, credenciais ou detalhes de uma vulnerabilidade de segurança numa issue pública. Como ainda não existe um canal privado definido para o projeto, contacta o proprietário do repositório através de um canal privado disponível antes de divulgar publicamente o problema.

## Licença

As contribuições serão distribuídas sob a mesma licença escolhida para o projeto. Antes de aceitar contribuições externas, adiciona um ficheiro `LICENSE` ao repositório para definir claramente os termos legais de utilização e redistribuição.

Obrigado por contribuíres para o ASCII Generator!