from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class HotkeyRegistration:
    handle: str
    key_combination: str


class WindowsAPIWrapper:
    """Cross-platform friendly wrapper mimicking Windows hotkey API."""

    def __init__(self) -> None:
        self._counter = 0
        self._registrations: Dict[str, HotkeyRegistration] = {}

    def register_hotkey(self, key_combination: str) -> HotkeyRegistration:
        self._counter += 1
        registration = HotkeyRegistration(handle=f"hk-{self._counter}", key_combination=key_combination)
        self._registrations[key_combination] = registration
        return registration

    def unregister_hotkey(self, key_combination: str) -> None:
        self._registrations.pop(key_combination, None)

    def is_registered(self, key_combination: str) -> bool:
        return key_combination in self._registrations

    def get_registration(self, key_combination: str) -> Optional[HotkeyRegistration]:
        return self._registrations.get(key_combination)


__all__ = ["HotkeyRegistration", "WindowsAPIWrapper"]
