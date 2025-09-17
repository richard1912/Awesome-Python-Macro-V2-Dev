from __future__ import annotations

from src.hotkeys.hotkey_service import HotkeyService
from src.models.hotkey import Hotkey, HotkeyActionType
from src.utils.windows_api import WindowsAPIWrapper


def test_hotkey_integration_routes_actions():
    api = WindowsAPIWrapper()
    service = HotkeyService(windows_api=api)
    triggered = []

    service.register_action_handler(
        HotkeyActionType.PLAY_MACRO, lambda hotkey: triggered.append(hotkey.action_type)
    )

    hotkey = Hotkey.create(
        key_combination="Ctrl+Shift+F5",
        action_type=HotkeyActionType.PLAY_MACRO,
        macro_id="macro-1",
        is_global=True,
    )
    service.register(hotkey)

    service.trigger("Ctrl+Shift+F5")
    assert triggered == [HotkeyActionType.PLAY_MACRO]
