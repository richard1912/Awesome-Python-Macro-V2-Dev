from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Iterable, Iterator


def ensure_directory(path: Path) -> None:
    """Ensure the directory at *path* exists."""
    path.mkdir(parents=True, exist_ok=True)


def atomic_write_json(path: Path, payload: dict) -> None:
    """Write *payload* atomically to *path* as JSON."""
    ensure_directory(path.parent)
    fd, temp_path = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)
        os.replace(temp_path, path)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def list_json_files(directory: Path) -> Iterator[Path]:
    ensure_directory(directory)
    yield from sorted(directory.glob("*.json"))


def remove_file(path: Path) -> None:
    if path.exists():
        path.unlink()


def write_text(path: Path, content: str) -> None:
    ensure_directory(path.parent)
    path.write_text(content, encoding="utf-8")


__all__ = [
    "ensure_directory",
    "atomic_write_json",
    "read_json",
    "list_json_files",
    "remove_file",
    "write_text",
]
