import importlib
import sys
import shutil
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
    shutil.move(str(si), str(backup))

    try:
        # Ensure the module is not cached from previous imports and that the project root
        # is on sys.path so `importlib.import_module("goog")` finds the top-level module.
        sys.modules.pop("goog", None)
        sys.path.insert(0, str(repo_root))
        with pytest.raises(FileNotFoundError):
            importlib.import_module("goog")
    finally:
        # restore file and clean up module cache and sys.path
        shutil.move(str(backup), str(si))
        sys.modules.pop("goog", None)
        try:
            sys.path.remove(str(repo_root))
        except ValueError:
            pass
