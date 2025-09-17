from __future__ import annotations

from pathlib import Path


def test_build_script_contains_pyinstaller_command():
    script = Path("scripts/build.py")
    assert script.exists()
    content = script.read_text(encoding="utf-8")
    assert "pyinstaller" in content.lower()
