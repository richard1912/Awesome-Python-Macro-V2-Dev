from __future__ import annotations

from datetime import datetime, timezone

import pytest

from src.models.action import Action
from src.models.hotkey import Hotkey, HotkeyActionType
from src.models.macro import Macro
from src.models.macro_package import MacroPackage
from src.models.schedule import Schedule
from src.models.user_settings import SettingValueError, UserSettings


def test_macro_serialization_roundtrip():
    macro = Macro.create(name="Roundtrip", tags=["demo"])
    macro.add_action(Action.keyboard_event(macro_id=macro.id, key_name="a", key_code="KeyA", is_press=True))
    payload = macro.to_dict()
    loaded = Macro.from_dict(payload)

    assert loaded.name == macro.name
    assert len(loaded.actions) == 1
    assert loaded.actions[0].key_name == "a"


def test_action_validation(raises_validation_error):
    def _create_invalid() -> None:
        Action.mouse_click(macro_id="macro", button="left", x=-1, y=100, timestamp_ms=0)

    raises_validation_error(_create_invalid)


def test_hotkey_factory():
    hotkey = Hotkey.create(
        key_combination="Ctrl+Shift+F5",
        action_type=HotkeyActionType.PLAY_MACRO,
        macro_id="macro",
        is_global=True,
    )
    assert hotkey.key_combination == "Ctrl+Shift+F5"
    assert hotkey.is_global


def test_schedule_next_run_calculation():
    now = datetime(2024, 1, 1, tzinfo=timezone.utc)
    schedule = Schedule.create(
        macro_id="macro",
        name="Morning",
        start_time=now,
        recurrence_type="once",
    )
    assert schedule.next_run == now

    schedule = Schedule.create(
        macro_id="macro",
        name="Daily",
        start_time=now,
        recurrence_type="daily",
    )
    assert schedule.next_run == now


def test_macro_package_contains_macros():
    macro = Macro.create(name="Packaged")
    package = MacroPackage.create(name="Bundle", macros=[macro])
    assert package.contains_macro(macro.id)


def test_user_settings_validation():
    settings = UserSettings()
    settings.set_value("ui.theme", "dark")
    assert settings.get_value("ui.theme") == "dark"

    with pytest.raises(SettingValueError):
        settings.require("missing.key")
