from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Callable, Iterator

import pytest
from PySide6.QtWidgets import QApplication

from src.storage.json_storage import JSONStorageManager
from src.utils.file_utils import ensure_directory
from src.utils.validation import ValidationError


os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


@pytest.fixture(scope="session")
def qapp() -> QApplication:
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


@pytest.fixture()
def data_dir(tmp_path: Path) -> Path:
    base = tmp_path / "macro_data"
    ensure_directory(base)
    return base


@pytest.fixture()
def storage_manager(data_dir: Path) -> JSONStorageManager:
    return JSONStorageManager(base_path=data_dir)


@pytest.fixture()
def assert_json_roundtrip(data_dir: Path) -> Callable[[Path], None]:
    def _assert_roundtrip(json_path: Path) -> None:
        with json_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        with (data_dir / "roundtrip.json").open("w", encoding="utf-8") as handle:
            json.dump(data, handle)
        with (data_dir / "roundtrip.json").open("r", encoding="utf-8") as handle:
            json.load(handle)

    return _assert_roundtrip


@pytest.fixture()
def raises_validation_error() -> Callable[[Callable[[], None]], None]:
    def _runner(callback: Callable[[], None]) -> None:
        with pytest.raises(ValidationError):
            callback()

    return _runner


@pytest.fixture()
def iter_actions() -> Callable[[Iterator], list]:
    def _collect(iterator: Iterator) -> list:
        return list(iterator)

    return _collect
