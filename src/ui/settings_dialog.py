from __future__ import annotations

from typing import Dict

from src.models.user_settings import UserSettings


class SettingsDialog:
    def __init__(self, *, settings: UserSettings) -> None:
        self.settings = settings
        self._pending: Dict[str, object] = {}

    def set_preference(self, key: str, value: object) -> None:
        self._pending[key] = value

    def apply(self) -> None:
        for key, value in self._pending.items():
            self.settings.set_value(key, value)
        self._pending.clear()


__all__ = ["SettingsDialog"]
