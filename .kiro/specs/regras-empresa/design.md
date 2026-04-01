# Design: Template de Regras da Empresa

## Visão Geral

Arquivo `regras_empresa.example.md` na raiz do repositório que serve como template para times configurarem suas regras de análise no KiroSonar. O arquivo é copiado pelo usuário para `regras_empresa.md`, que é detectado automaticamente pelo módulo `config.py`.

## Fluxo de Uso

```
regras_empresa.example.md  →  (cópia manual)  →  regras_empresa.md  →  config.load_rules()  →  prompt_builder.build_prompt()
```

## Estrutura do Template

O arquivo contém 4 seções em Markdown:

1. **Padrões de Código** — SOLID, complexidade, DRY, type hints, docstrings, tratamento de exceções
2. **Nomenclatura** — snake_case, PascalCase, UPPER_SNAKE_CASE, nomes descritivos em inglês
3. **Arquitetura** — SRP, sem imports circulares, separação I/O vs lógica, sem globais mutáveis
4. **Segurança** — sem eval/exec, sanitização de inputs, encoding UTF-8, prevenção de path traversal

## Integração com Módulos Existentes

- `config.py` já carrega `regras_empresa.md` automaticamente via `load_rules()`
- Nenhuma alteração de código necessária — apenas criação do template e documentação
- O `.example.md` é versionado; o `regras_empresa.md` do usuário é ignorado via `.gitignore`
