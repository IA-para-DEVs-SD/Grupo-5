# Tarefas: Chunker Module

## Tarefa 1: Implementar divisão por fronteiras
- [x] Criar `src/chunker.py` com regex multilinguagem
- [x] Implementar `split_into_chunks()` com target de ~100 linhas
- [x] Suportar Python (`def`, `class`), PHP (`public function`), JS (`function`, `class`)

## Tarefa 2: Implementar overlap
- [x] Adicionar 20 linhas de overlap entre chunks consecutivos
- [x] Marcar overlap com comentário indicativo

## Tarefa 3: Implementar fallback por tamanho
- [x] Criar `_chunk_by_size()` para arquivos sem funções
- [x] Cortar em linhas seguras (linhas em branco, `}`, `end`)
- [x] Aplicar overlap no fallback

## Tarefa 4: Integrar no CLI
- [x] Chamar chunker em `_analyze_file()` quando arquivo grande e sem diff
- [x] Analisar chunks em paralelo com `ThreadPoolExecutor`
- [x] Concatenar resultados no relatório final
- [x] Mostrar progresso por chunk concluído
