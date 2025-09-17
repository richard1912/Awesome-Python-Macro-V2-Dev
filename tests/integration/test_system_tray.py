from __future__ import annotations

from src.core.macro_service import MacroService
from src.player.playback_service import PlaybackService
from src.storage.json_storage import JSONStorageManager
from src.ui.system_tray import SystemTrayManager


class DummyPlayback(PlaybackService):
    def __init__(self) -> None:
        super().__init__(sleep=lambda _: None)
        self.played: list[str] = []

    def play_macro(self, macro, **kwargs):  # type: ignore[override]
        self.played.append(macro.id)
        return super().play_macro(macro, **kwargs)


def test_system_tray_lists_macros_and_triggers_playback(tmp_path, qapp):
    storage = JSONStorageManager(base_path=tmp_path / "data")
    macro_service = MacroService(storage_manager=storage)
    macro = macro_service.create_macro(name="Tray Macro")
    playback = DummyPlayback()

    tray = SystemTrayManager(macro_service=macro_service, playback_service=playback)
    entries = tray.build_quick_actions()
    assert any(entry.label == "Tray Macro" for entry in entries)

    tray.trigger_action(macro.id)
    assert playback.played == [macro.id]
