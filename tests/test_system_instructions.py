import importlib
import sys
from pathlib import Path

import pytest


def test_import_fails_when_system_instructions_missing(tmp_path, monkeypatch):
    """If `system_instructions.txt` is missing, importing `goog` should raise FileNotFoundError."""
    # Ensure a GEMINI_API_KEY is present so import-time checks don't fail earlier
    monkeypatch.setenv("GEMINI_API_KEY", "testkey")

    repo_root = Path(__file__).resolve().parents[1]
    si = repo_root / "system_instructions.txt"
    assert si.exists(), "test requires an existing system_instructions.txt in the repo root"

    backup = tmp_path / "system_instructions.txt.bak"
    si.replace(backup)

    try:
        sys.modules.pop("goog", None)
        sys.path.insert(0, str(repo_root))
        module = importlib.import_module("goog")
        with pytest.raises(FileNotFoundError):
            module.init_ai_client()
    finally:
        # restore file and clean up module cache and sys.path
        backup.replace(si)
        sys.modules.pop("goog", None)
        sys.path.remove(str(repo_root))
