from __future__ import annotations

import pytest

from src.hotkeys.hotkey_service import HotkeyService
from src.models.hotkey import Hotkey, HotkeyActionType
from src.utils.windows_api import WindowsAPIWrapper
from src.utils.validation import ValidationError


def test_hotkey_registration_and_trigger():
    api = WindowsAPIWrapper()
    service = HotkeyService(windows_api=api)
    calls = []
    hotkey = Hotkey.create(
        key_combination="Ctrl+Shift+F9",
        action_type=HotkeyActionType.START_RECORDING,
        is_global=True,
    )
    service.register(hotkey, callback=lambda hk: calls.append(hk.key_combination))

    assert service.is_registered("Ctrl+Shift+F9")
    service.trigger("Ctrl+Shift+F9")
    assert calls == ["Ctrl+Shift+F9"]


def test_hotkey_conflict_detection():
    api = WindowsAPIWrapper()
    service = HotkeyService(windows_api=api)
    service.register(
        Hotkey.create(
            key_combination="Ctrl+Alt+R",
            action_type=HotkeyActionType.START_RECORDING,
            is_global=True,
        )
    )

    with pytest.raises(ValidationError):
        service.register(
            Hotkey.create(
                key_combination="Ctrl+Alt+R",
                action_type=HotkeyActionType.PLAY_MACRO,
                is_global=True,
            )
        )
