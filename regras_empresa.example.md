# Regras de Análise — Exemplo

> Este é um template de exemplo. Copie para `regras_empresa.md` na raiz do projeto e adapte às convenções do seu time.

---

## Padrões de Código

- Siga os princípios SOLID em todas as classes e módulos.
- Evite funções com mais de 20 linhas — quebre em funções auxiliares.
- Mantenha complexidade ciclomática baixa (máximo 10 por função).
- Remova código morto, imports não utilizados e variáveis sem uso.
- Evite duplicação de lógica (princípio DRY).
- Use type hints em todas as assinaturas de funções e métodos.
- Documente funções públicas com docstrings descritivas.
- Trate todas as exceções de forma explícita — nunca use `except` genérico sem re-raise.

## Nomenclatura

- Variáveis e funções em `snake_case`.
- Classes em `PascalCase`.
- Constantes em `UPPER_SNAKE_CASE`.
- Nomes devem ser descritivos e em inglês (ex: `get_user_name`, não `pega_nome`).
- Evite abreviações ambíguas (ex: `usr`, `tmp`, `val`).
- Prefixe funções internas/privadas com `_` (ex: `_validate_input`).

## Arquitetura

- Cada módulo deve ter uma única responsabilidade (Single Responsibility Principle).
- Não importe módulos de forma circular.
- Separe lógica de negócio da camada de I/O (leitura de arquivos, chamadas externas).
- Não use variáveis globais mutáveis.
- Mantenha dependências explícitas via injeção de parâmetros, não via estado global.

## Segurança

- Nunca execute entrada do usuário diretamente (ex: `eval()`, `exec()`).
- Valide e sanitize todos os inputs externos antes de processar.
- Não exponha informações sensíveis em mensagens de erro ou logs.
- Use encoding UTF-8 explícito em todas as operações de leitura/escrita de arquivos.
- Valide caminhos de arquivo para prevenir path traversal (ex: `../../etc/passwd`).
