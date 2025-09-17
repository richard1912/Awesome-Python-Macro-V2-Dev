from __future__ import annotations

from typing import List

from src.hotkeys.hotkey_service import HotkeyService
from src.models.hotkey import Hotkey


class HotkeyDialog:
    def __init__(self, *, service: HotkeyService) -> None:
        self.service = service
        self._assigned: List[Hotkey] = []

    def assign_hotkey(self, hotkey: Hotkey) -> None:
        self.service.register(hotkey)
        self._assigned.append(hotkey)


__all__ = ["HotkeyDialog"]
