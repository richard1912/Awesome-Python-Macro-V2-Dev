from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Optional

from src.models.macro import Macro
from src.models.user_settings import UserSettings
from src.utils import file_utils


class JSONStorageManager:
    """Persist macros and settings as JSON documents."""

    def __init__(self, *, base_path: Path) -> None:
        self.base_path = base_path
        self.macros_path = self.base_path / "macros"
        self.settings_path = self.base_path / "settings"
        file_utils.ensure_directory(self.macros_path)
        file_utils.ensure_directory(self.settings_path)

    # Macro operations -------------------------------------------------
    def macro_path(self, macro_id: str) -> Path:
        return self.macros_path / f"{macro_id}.json"

    def save_macro(self, macro: Macro) -> Path:
        path = self.macro_path(macro.id)
        file_utils.atomic_write_json(path, macro.to_dict())
        return path

    def load_macro(self, macro_id: str) -> Optional[Macro]:
        path = self.macro_path(macro_id)
        if not path.exists():
            return None
        payload = file_utils.read_json(path)
        return Macro.from_dict(payload)

    def delete_macro(self, macro_id: str) -> None:
        file_utils.remove_file(self.macro_path(macro_id))

    def iter_macros(self) -> Iterator[Macro]:
        for path in file_utils.list_json_files(self.macros_path):
            yield Macro.from_dict(file_utils.read_json(path))

    def list_macros(self) -> List[Macro]:
        return list(self.iter_macros())

    # Settings ---------------------------------------------------------
    def settings_file(self) -> Path:
        return self.settings_path / "user_settings.json"

    def load_settings(self) -> UserSettings:
        path = self.settings_file()
        if not path.exists():
            return UserSettings()
        return UserSettings.from_dict(file_utils.read_json(path))

    def save_settings(self, settings: UserSettings) -> Path:
        path = self.settings_file()
        file_utils.atomic_write_json(path, settings.to_dict())
        return path


__all__ = ["JSONStorageManager"]
