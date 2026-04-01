# Design: Chunker Module

## Visão Geral

O módulo `src/chunker.py` divide arquivos grandes (>300 linhas) em trechos lógicos para análise paralela pela LLM. Usa regex para detectar fronteiras de função/classe em múltiplas linguagens e aplica overlap de 20 linhas entre chunks consecutivos.

## Fluxo

```
arquivo (>300 linhas) → detecta fronteiras → agrupa em chunks de ~100 linhas → aplica overlap → retorna lista de chunks
```

## Estratégias de Divisão

### 1. Por Fronteiras (padrão)
- Regex detecta: `def`, `function`, `class`, `interface`, `trait`, `enum` com modificadores opcionais (`public`, `private`, `static`, etc)
- Acumula linhas até atingir ~100, depois corta na próxima fronteira
- Nunca corta no meio de uma função

### 2. Por Tamanho (fallback)
- Ativado quando não há fronteiras suficientes (código solto)
- Procura linhas seguras para cortar: linhas em branco, `}`, `};`, `end`, `?>`
- Busca a linha segura mais próxima do target (100 ± 30 linhas)

## Overlap
- Cada chunk (exceto o primeiro) inclui 20 linhas do chunk anterior
- Marcado com comentário `# ... contexto do trecho anterior ...`
- Garante que a LLM entende variáveis, imports e contexto do trecho

## Integração

- `cli.py` chama `split_into_chunks()` quando arquivo é grande e sem diff
- Se retorna 1 chunk → análise normal
- Se retorna N chunks → analisa em paralelo via `ThreadPoolExecutor` (max 4 workers)
- Resultados são concatenados no relatório final
