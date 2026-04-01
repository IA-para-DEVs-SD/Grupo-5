"""Carregamento de regras de análise."""

import os
from pathlib import Path

# Caminho do template de regras na raiz do repositório do KiroSonar
EXAMPLE_RULES_FILE: str = str(
    Path(__file__).resolve().parent.parent.parent / "regras_empresa.example.md"
)

DEFAULT_RULES: str = """\
- Siga os princípios SOLID.
- Nomeie variáveis e funções de forma descritiva.
- Evite funções com mais de 20 linhas.
- Não use variáveis globais mutáveis.
- Trate todas as exceções de forma explícita.
- Use type hints em todas as assinaturas.
- Remova código morto e imports não utilizados.
- Evite duplicação de lógica (DRY).
- Mantenha complexidade ciclomática baixa.
- Documente funções públicas com docstrings.
"""

# Arquivos de specs/regras de IA conhecidos, em ordem de prioridade
_KNOWN_SPEC_FILES: list[str] = [
    "regras_empresa.md",
    ".kiro/instructions.md",
    ".kiro/padrao-projeto.md",
    ".cursor/rules",
    ".github/copilot-instructions.md",
    ".clinerules",
]


def _discover_spec_files() -> list[str]:
    """Descobre arquivos de specs/regras de IA existentes no diretório atual.

    Returns:
        Lista de caminhos encontrados, em ordem de prioridade.
    """
    return [f for f in _KNOWN_SPEC_FILES if os.path.isfile(f)]


def load_rules(rules_path: str | None = None) -> str:
    """Carrega as regras de análise.

    Ordem de prioridade:
      1. --rules (caminho explícito)
      2. regras_empresa.md
      3. Specs de IA existentes (.kiro/, .cursor/, .github/, etc)
      4. DEFAULT_RULES (fallback)

    Args:
        rules_path: Caminho explícito para o arquivo de regras.

    Returns:
        Conteúdo das regras concatenadas.
    """
    # 1. Caminho explícito via --rules
    if rules_path:
        if os.path.isfile(rules_path):
            print(f"📏 Regras carregadas de: {rules_path}")
            with open(rules_path, encoding="utf-8") as f:
                return f.read()
        print(f"⚠️  Arquivo de regras não encontrado: {rules_path}")

    # 2 e 3. Descobre specs existentes
    found = _discover_spec_files()
    if found:
        parts: list[str] = []
        for spec in found:
            print(f"📏 Regras detectadas: {spec}")
            with open(spec, encoding="utf-8") as f:
                parts.append(f"# Fonte: {spec}\n{f.read()}")
        return "\n\n".join(parts)

    # 4. Fallback
    print("📏 Nenhum arquivo de regras encontrado. Usando regras padrão.")
    return DEFAULT_RULES
