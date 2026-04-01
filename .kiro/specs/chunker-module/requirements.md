# Documento de Requisitos: Chunker Module

## Introdução

Este documento especifica os requisitos para o módulo `chunker.py`, responsável por dividir arquivos grandes em trechos lógicos para análise individual pela LLM. Resolve o problema de timeout em arquivos com mais de 300 linhas que excedem a capacidade de processamento da LLM em uma única chamada.

## Glossário

- **Chunk**: Trecho de código extraído de um arquivo grande para análise individual
- **Fronteira**: Linha que marca o início de uma função, método ou classe — ponto seguro para dividir
- **Overlap**: Linhas do chunk anterior incluídas no início do próximo para manter contexto
- **Light Mode**: Modo de análise sem código refatorado, apenas relatório com sugestões por linha

## Requisitos

### Requisito 1: Divisão por Fronteiras de Função/Classe

**User Story:** Como desenvolvedor, quero que arquivos grandes sejam divididos automaticamente em trechos lógicos, para que a análise não dê timeout.

#### Critérios de Aceite

1. GIVEN um arquivo com mais de 300 linhas e sem diff, WHEN o chunker processa o arquivo, THEN SHALL dividir em chunks de ~100 linhas cortando em fronteiras de função/método/classe
2. GIVEN um arquivo com 300 linhas ou menos, WHEN o chunker processa o arquivo, THEN SHALL retornar o arquivo inteiro como um único chunk
3. GIVEN um arquivo PHP com métodos indentados (`public function`), WHEN o chunker processa, THEN SHALL reconhecer as fronteiras corretamente
4. GIVEN um arquivo Python com `def`/`class`, WHEN o chunker processa, THEN SHALL reconhecer as fronteiras corretamente
5. GIVEN um arquivo JS com `function`/`class`/arrow functions, WHEN o chunker processa, THEN SHALL reconhecer as fronteiras corretamente

### Requisito 2: Overlap entre Chunks

**User Story:** Como desenvolvedor, quero que cada trecho inclua contexto do trecho anterior, para que a IA entenda variáveis e imports usados.

#### Critérios de Aceite

1. GIVEN chunks divididos por fronteiras, WHEN o segundo chunk é gerado, THEN SHALL incluir as últimas 20 linhas do chunk anterior como contexto
2. GIVEN o primeiro chunk, THEN SHALL não ter overlap (é o início do arquivo)
3. GIVEN chunks com overlap, THEN SHALL marcar o overlap com comentário indicativo

### Requisito 3: Fallback para Código sem Funções

**User Story:** Como desenvolvedor, quero que arquivos sem funções (código solto) também sejam divididos de forma inteligente, para que a análise funcione em qualquer tipo de arquivo.

#### Critérios de Aceite

1. GIVEN um arquivo sem fronteiras de função/classe, WHEN o chunker processa, THEN SHALL dividir por tamanho cortando em linhas seguras (linhas em branco, `}`, `end`)
2. GIVEN o fallback por tamanho, THEN SHALL nunca cortar no meio de um bloco if/for/while quando houver linha segura próxima
3. GIVEN o fallback por tamanho, THEN SHALL aplicar overlap de 20 linhas entre chunks
