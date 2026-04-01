"""Geração e salvamento de relatórios em Markdown."""

import os
import re
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ReportEntry:
    """Representa um relatório encontrado na pasta relatorios/."""

    name: str
    generated_at: datetime
    size_bytes: int


def generate_report_name(file_path: str) -> str:
    """Gera o nome do arquivo de relatório baseado no arquivo analisado.

    Usa apenas o nome do arquivo (sem diretórios) para manter o nome curto.

    Args:
        file_path: Caminho do arquivo original (ex: 'app/Services/BankImageService.php').

    Returns:
        Nome do relatório (ex: 'relatorios/BankImageService_20260401_173000.md').
    """
    basename = os.path.basename(file_path)
    name_without_ext = os.path.splitext(basename)[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join("relatorios", f"{name_without_ext}_{timestamp}.md")


def _clean_llm_output(content: str) -> str:
    """Remove logs e artefatos do kiro-cli da resposta da LLM.

    Args:
        content: Resposta bruta da LLM que pode conter logs de tools.

    Returns:
        Conteúdo limpo, apenas Markdown.
    """
    lines = content.splitlines(keepends=True)
    clean_lines: list[str] = []

    for line in lines:
        stripped = line.strip()

        # Pula linhas vazias de quote do kiro-cli
        if stripped == ">":
            continue

        # Pula linhas que começam com "> " (quotes do kiro-cli)
        if stripped.startswith("> ") and not stripped.startswith("> ##"):
            continue

        # Pula logs de ferramentas do kiro-cli
        if re.match(
            r"^(Getting symbols|Searching|Reading file|Batch fs_read"
            r"|↱ Operation|✓ Successfully|✓ Found|⋮|- (Completed|Summary)"
            r"|\d+l$)",
            stripped,
        ):
            continue

        if "(using tool:" in stripped:
            continue

        clean_lines.append(line)

    return "".join(clean_lines).strip() + "\n"


def list_reports(reports_dir: str = "relatorios") -> list[ReportEntry]:
    """Lista os relatórios existentes na pasta relatorios/.

    Ordenados por data (mais recente primeiro).

    Args:
        reports_dir: Caminho da pasta de relatórios.

    Returns:
        Lista de ReportEntry ordenada por data decrescente.
    """
    if not os.path.isdir(reports_dir):
        return []

    entries = []
    for name in os.listdir(reports_dir):
        full_path = os.path.join(reports_dir, name)
        if not os.path.isfile(full_path):
            continue
        stat = os.stat(full_path)
        entries.append(
            ReportEntry(
                name=name,
                generated_at=datetime.fromtimestamp(stat.st_mtime),
                size_bytes=stat.st_size,
            )
        )

    entries.sort(key=lambda e: e.generated_at, reverse=True)
    return entries


def save_report(content: str, file_path: str) -> str:
    """Salva o relatório da análise em um arquivo Markdown.

    Args:
        content: String Markdown retornada pela LLM.
        file_path: Caminho do arquivo original analisado.

    Returns:
        Caminho absoluto do arquivo de relatório salvo.
    """
    content = _clean_llm_output(content)
    report_name = generate_report_name(file_path)
    os.makedirs(os.path.dirname(report_name), exist_ok=True)
    with open(report_name, "w", encoding="utf-8") as f:
        f.write(content)
    return os.path.abspath(report_name)
