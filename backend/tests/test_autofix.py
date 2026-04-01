"""Unit tests for src.autofix module."""

from unittest.mock import MagicMock, patch

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from src.autofix import _validate_path, apply_fix, extract_refactored_code


class TestValidatePath:
    """Tests for _validate_path."""

    @patch("src.autofix.get_repo_root", return_value="/home/user/repo")
    def test_raises_for_path_outside_repo(self, mock_root: MagicMock) -> None:
        with pytest.raises(ValueError, match="Caminho fora do repositório"):
            _validate_path("/etc/passwd")

    @patch("src.autofix.get_repo_root", return_value="/home/user/repo")
    def test_accepts_path_inside_repo(self, mock_root: MagicMock) -> None:
        _validate_path("/home/user/repo/src/app.py")


class TestExtractRefactoredCode:
    """Tests for extract_refactored_code."""

    def test_extracts_code_between_tags(self) -> None:
        response = "## Código\n[START]\nprint('hello')\n[END]\n"
        assert extract_refactored_code(response) == "print('hello')"

    def test_returns_none_when_tags_absent(self) -> None:
        response = "## Bugs\n- Nenhum bug encontrado."
        assert extract_refactored_code(response) is None

    def test_extracts_multiline_code(self) -> None:
        response = "[START]\ndef foo():\n    return 1\n[END]"
        assert extract_refactored_code(response) == "def foo():\n    return 1"

    def test_extracts_code_from_full_response(self) -> None:
        response = "## Bugs\n- None\n\n## Código Refatorado\n[START]\ndef foo():\n    pass\n[END]"
        assert extract_refactored_code(response) == "def foo():\n    pass"

    def test_returns_none_when_no_tags(self) -> None:
        assert extract_refactored_code("## Bugs\n- None") is None

    def test_returns_none_when_only_start_tag(self) -> None:
        assert extract_refactored_code("[START]\ndef foo(): pass") is None

    def test_returns_none_when_only_end_tag(self) -> None:
        assert extract_refactored_code("def foo(): pass\n[END]") is None

    def test_returns_none_on_empty_string(self) -> None:
        assert extract_refactored_code("") is None

    def test_handles_whitespace_around_tags(self) -> None:
        response = "[START]   \ndef bar(): pass\n   [END]"
        result = extract_refactored_code(response)
        assert result is not None
        assert "def bar(): pass" in result

    @given(st.text(min_size=1))
    @settings(max_examples=100)
    def test_never_raises_on_arbitrary_input(self, text: str) -> None:
        """extract_refactored_code must never raise for any string input."""
        result = extract_refactored_code(text)
        assert result is None or isinstance(result, str)


class TestApplyFix:
    """Tests for apply_fix."""

    def test_returns_false_when_no_code_in_response(self, capsys) -> None:
        result = apply_fix("## Bugs\n- None", "file.py")
        assert result is False
        assert "Nenhum código refatorado" in capsys.readouterr().out

    @patch("src.autofix.get_repo_root")
    def test_returns_false_when_user_declines(self, mock_root, tmp_path) -> None:
        mock_root.return_value = str(tmp_path)
        file = tmp_path / "app.py"
        file.write_text("old code")
        response = "[START]\nnew code\n[END]"
        with patch("builtins.input", return_value="n"):
            result = apply_fix(response, str(file))
        assert result is False
        assert file.read_text() == "old code"

    @patch("src.autofix.get_repo_root")
    def test_applies_fix_and_creates_backup_when_user_confirms(self, mock_root, tmp_path) -> None:
        mock_root.return_value = str(tmp_path)
        file = tmp_path / "app.py"
        file.write_text("old code")
        response = "[START]\nnew code\n[END]"
        with patch("builtins.input", return_value="s"):
            result = apply_fix(response, str(file))
        assert result is True
        assert file.read_text() == "new code"
        assert (tmp_path / "app.py.bak").read_text() == "old code"

    @patch("src.autofix.get_repo_root")
    def test_backup_file_created_before_overwrite(self, mock_root, tmp_path) -> None:
        mock_root.return_value = str(tmp_path)
        file = tmp_path / "script.py"
        original = "original content"
        file.write_text(original)
        response = "[START]\nrefactored\n[END]"
        with patch("builtins.input", return_value="s"):
            apply_fix(response, str(file))
        backup = tmp_path / "script.py.bak"
        assert backup.exists()
        assert backup.read_text() == original

    @patch("src.autofix.get_repo_root")
    def test_prints_preview_before_asking(self, mock_root, tmp_path, capsys) -> None:
        mock_root.return_value = str(tmp_path)
        file = tmp_path / "app.py"
        file.write_text("x = 1")
        response = "[START]\ny = 2\n[END]"
        with patch("builtins.input", return_value="n"):
            apply_fix(response, str(file))
        output = capsys.readouterr().out
        assert "y = 2" in output
