"""Prompt assembly for LLM submission.

Builds a structured prompt with explicit weighting between the diff
(maximum priority) and the full file content (medium priority),
as specified in RF-01 of the PRD.
"""

import re

# Arquivos acima deste limite (sem diff) usam modo análise leve
_MAX_LINES_FULL_REVIEW: int = 300

# Linhas de contexto ao redor de cada hunk do diff
_CONTEXT_LINES: int = 20


def _sanitize_user_content(text: str) -> str:
    """Sanitiza conteúdo do usuário para prevenir prompt injection.

    Delimita claramente dados do usuário vs instruções do sistema,
    removendo padrões que poderiam ser interpretados como instruções.
    """
    sanitized = text.replace("```", "` ` `")
    text_lower = sanitized.lower()
    for marker in ["[system]", "[inst]", "<<sys>>", "<</sys>>", "[/inst]"]:
        idx = text_lower.find(marker)
        while idx != -1:
            sanitized = sanitized[:idx] + sanitized[idx + len(marker) :]
            text_lower = sanitized.lower()
            idx = text_lower.find(marker)
    return sanitized


def _extract_context_from_diff(diff: str, full_code: str) -> str:
    """Extrai apenas as linhas relevantes do arquivo baseado no diff.

    Pega as linhas alteradas + _CONTEXT_LINES ao redor de cada hunk.

    Args:
        diff: Saída do git diff.
        full_code: Código completo do arquivo.

    Returns:
        Trecho relevante do código com números de linha.
    """
    lines = full_code.splitlines()
    total = len(lines)
    relevant: set[int] = set()

    # Extrai números de linha dos hunks (@@ -X,Y +X,Y @@)
    for match in re.finditer(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", diff):
        start = int(match.group(1))
        count = int(match.group(2)) if match.group(2) else 1
        for i in range(
            max(0, start - _CONTEXT_LINES - 1),
            min(total, start + count + _CONTEXT_LINES),
        ):
            relevant.add(i)

    if not relevant:
        return full_code

    # Monta o trecho com números de linha
    sorted_lines = sorted(relevant)
    parts: list[str] = []
    prev = -2
    for i in sorted_lines:
        if i - prev > 1 and parts:
            parts.append("...")
        parts.append(f"{i + 1:>4} | {lines[i]}")
        prev = i

    return "\n".join(parts)


_REPORT_TEMPLATE: str = """\
## Template de Resposta (siga exatamente, seja conciso — uma linha por item)

## 🐞 Bugs
(Linha X: descrição do bug e sugestão de correção)

## 🔐 Segurança
(Linha X: vulnerabilidade encontrada e como corrigir)

## 🧹 Code Smells
(Linha X: problema de qualidade e sugestão)

## ⚡ Performance
(Linha X: problema de performance e alternativa)

## ⚠️ Security Hotspots
(Linha X: ponto que requer revisão manual e motivo)"""

_REFACTOR_SECTION: str = (
    "\n\n## Código Refatorado\n"
    "[START]\n(código refatorado APENAS das linhas alteradas e ao redor)\n[END]"
)


def build_prompt(diff: str, full_code: str, rules: str, file_path: str) -> str:
    """Assemble the complete prompt for the LLM.

    Quando há diff: manda diff + contexto ao redor (não o arquivo inteiro).
    Quando não há diff e arquivo pequeno: manda completo.
    Quando não há diff e arquivo grande: manda completo sem pedir refatoração.

    Args:
        diff: Git diff output for the file (may be empty).
        full_code: Full content of the file under analysis.
        rules: Company rules string.
        file_path: File name/path for context.

    Returns:
        Formatted prompt string.
    """
    full_code = _sanitize_user_content(full_code)
    diff = _sanitize_user_content(diff) if diff else diff

    line_count = full_code.count("\n") + 1
    light_mode = not diff and line_count > _MAX_LINES_FULL_REVIEW

    if diff:
        # Com diff: manda diff + contexto relevante, sem pedir código refatorado
        context = _extract_context_from_diff(diff, full_code)
        code_section = (
            "## Diff das Alterações (FOCO PRINCIPAL)\n"
            f"```diff\n{diff}\n```\n\n"
            "## Contexto do Código (linhas ao redor das alterações)\n"
            f"```\n{context}\n```\n\n"
        )
        refactor = (
            "\n\n## Sugestões de Correção\n"
            "Para cada problema, indique a linha e como corrigir em uma frase."
        )
    else:
        # Sem diff: manda arquivo completo
        code_section = f"## Arquivo Completo\n```\n{full_code}\n```\n\n"
        refactor = "" if light_mode else _REFACTOR_SECTION

    return (
        f"Você é um auditor de código sênior. Analise o arquivo '{file_path}' "
        f"com base nas regras abaixo.\n"
        f"Responda de forma CONCISA: uma linha por item, sempre com número da linha.\n\n"
        f"## Regras da Empresa\n{rules}\n\n"
        f"{code_section}"
        f"{_REPORT_TEMPLATE}{refactor}"
    )
