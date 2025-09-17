"""Build script for creating a standalone executable via PyInstaller."""
from __future__ import annotations

from pathlib import Path


def build_command() -> list[str]:
    return ["pyinstaller", "--name", "awesome_macro", "main.py"]


def main() -> None:
    command = build_command()
    print("Running:", " ".join(command))


if __name__ == "__main__":
    main()
