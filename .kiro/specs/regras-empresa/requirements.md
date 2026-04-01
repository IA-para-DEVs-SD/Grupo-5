# Documento de Requisitos: Template de Regras da Empresa

## Introdução

Este documento especifica os requisitos para a criação de um template de regras de análise (`regras_empresa.example.md`) que serve como ponto de partida para times configurarem o KiroSonar com suas próprias convenções de código.

## Glossário

- **Regras_Template**: Arquivo `regras_empresa.example.md` na raiz do repositório contendo convenções de exemplo
- **Regras_Ativas**: Arquivo `regras_empresa.md` criado pelo usuário a partir do template, carregado automaticamente pelo `config.py`
- **DEFAULT_RULES**: Constante fallback em `config.py` usada quando nenhum arquivo de regras existe

## Requisitos

### Requisito 1: Arquivo de Exemplo na Raiz do Repositório

**User Story:** Como tech lead, quero ter um template de regras de exemplo no repositório, para que meu time tenha um ponto de partida para configurar as convenções de código.

#### Critérios de Aceite

1. GIVEN o repositório do KiroSonar, WHEN o desenvolvedor clona o projeto, THEN SHALL existir um arquivo `regras_empresa.example.md` na raiz
2. GIVEN o arquivo de exemplo, WHEN o desenvolvedor o lê, THEN SHALL conter instruções claras de como copiar para `regras_empresa.md`
3. GIVEN o arquivo de exemplo, THEN SHALL estar escrito em português Brasil

### Requisito 2: Seções Obrigatórias do Template

**User Story:** Como tech lead, quero que o template cubra as principais áreas de qualidade de código, para que meu time tenha diretrizes completas.

#### Critérios de Aceite

1. GIVEN o arquivo `regras_empresa.example.md`, THEN SHALL conter a seção "Padrões de Código" com regras sobre SOLID, complexidade, DRY e type hints
2. GIVEN o arquivo `regras_empresa.example.md`, THEN SHALL conter a seção "Nomenclatura" com convenções de naming (snake_case, PascalCase, UPPER_SNAKE_CASE)
3. GIVEN o arquivo `regras_empresa.example.md`, THEN SHALL conter a seção "Arquitetura" com regras sobre responsabilidade única e separação de camadas
4. GIVEN o arquivo `regras_empresa.example.md`, THEN SHALL conter a seção "Segurança" com regras sobre sanitização de input, encoding e path traversal

### Requisito 3: Documentação de Uso

**User Story:** Como desenvolvedor, quero saber como usar regras customizadas, para que eu consiga configurar o KiroSonar para o meu time.

#### Critérios de Aceite

1. GIVEN o README.md, THEN SHALL documentar como copiar o template para `regras_empresa.md`
2. GIVEN o README.md, THEN SHALL documentar a flag `--rules` para caminho alternativo
3. GIVEN o README.md, THEN SHALL informar que `DEFAULT_RULES` são usadas como fallback
