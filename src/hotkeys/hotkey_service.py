from __future__ import annotations

from typing import Callable, Dict, Optional

from src.models.hotkey import Hotkey, HotkeyActionType
from src.utils.validation import ValidationError
from src.utils.windows_api import HotkeyRegistration, WindowsAPIWrapper


class HotkeyService:
    def __init__(self, *, windows_api: WindowsAPIWrapper) -> None:
        self.windows_api = windows_api
        self._hotkeys: Dict[str, tuple[Hotkey, Optional[Callable[[Hotkey], None]]]] = {}
        self._action_handlers: Dict[HotkeyActionType, Callable[[Hotkey], None]] = {}

    def register(
        self, hotkey: Hotkey, callback: Optional[Callable[[Hotkey], None]] = None
    ) -> HotkeyRegistration:
        if self.is_registered(hotkey.key_combination):
            raise ValidationError(f"Hotkey already registered: {hotkey.key_combination}")
        registration = self.windows_api.register_hotkey(hotkey.key_combination)
        self._hotkeys[hotkey.key_combination] = (hotkey, callback)
        return registration

    def unregister(self, key_combination: str) -> None:
        if key_combination in self._hotkeys:
            self.windows_api.unregister_hotkey(key_combination)
            self._hotkeys.pop(key_combination, None)

    def is_registered(self, key_combination: str) -> bool:
        return key_combination in self._hotkeys

    def register_action_handler(
        self, action: HotkeyActionType, handler: Callable[[Hotkey], None]
    ) -> None:
        self._action_handlers[action] = handler

    def trigger(self, key_combination: str) -> None:
        entry = self._hotkeys.get(key_combination)
        if not entry:
            return
        hotkey, callback = entry
        if callback:
            callback(hotkey)
        handler = self._action_handlers.get(hotkey.action_type)
        if handler:
            handler(hotkey)


__all__ = ["HotkeyService"]
