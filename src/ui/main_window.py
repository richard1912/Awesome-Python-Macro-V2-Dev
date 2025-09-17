from __future__ import annotations

from src.core.macro_service import MacroService
from src.hotkeys.hotkey_service import HotkeyService
from src.player.playback_service import PlaybackService
from src.ui.macro_list_widget import MacroListWidget


class MainWindow:
    def __init__(
        self,
        *,
        macro_service: MacroService,
        playback_service: PlaybackService,
        hotkey_service: HotkeyService,
    ) -> None:
        self.macro_service = macro_service
        self.playback_service = playback_service
        self.hotkey_service = hotkey_service
        self.macro_list_widget = MacroListWidget()

    def refresh_macro_list(self) -> None:
        self.macro_list_widget.set_macros(self.macro_service.list_macros())

    def play_macro(self, macro_id: str) -> None:
        macro = self.macro_service.get_macro(macro_id)
        if macro:
            self.playback_service.play_macro(macro)


__all__ = ["MainWindow"]
