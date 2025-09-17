from __future__ import annotations

from dataclasses import dataclass
from typing import List

from src.core.macro_service import MacroService
from src.player.playback_service import PlaybackService


@dataclass
class TrayEntry:
    label: str
    macro_id: str


class SystemTrayManager:
    def __init__(self, *, macro_service: MacroService, playback_service: PlaybackService) -> None:
        self.macro_service = macro_service
        self.playback_service = playback_service

    def build_quick_actions(self) -> List[TrayEntry]:
        return [TrayEntry(label=macro.name, macro_id=macro.id) for macro in self.macro_service.list_macros()]

    def trigger_action(self, macro_id: str) -> None:
        macro = self.macro_service.get_macro(macro_id)
        if macro:
            self.playback_service.play_macro(macro)


__all__ = ["SystemTrayManager", "TrayEntry"]
