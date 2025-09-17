from __future__ import annotations

from src.cli.cli_interface import CLIResponse
from src.core.macro_service import MacroService
from src.player.playback_service import PlaybackService


class PlaybackCommandSet:
    prefix = "playback"

    def __init__(self, playback_service: PlaybackService, macro_service: MacroService) -> None:
        self.playback_service = playback_service
        self.macro_service = macro_service

    def commands(self) -> dict[str, callable]:
        return {"run": self.run}

    def run(self, macro_id: str) -> CLIResponse:
        macro = self.macro_service.get_macro(macro_id)
        if not macro:
            return CLIResponse(ok=False, message=f"Unknown macro: {macro_id}")
        self.playback_service.play_macro(macro)
        return CLIResponse(ok=True, message=f"Played {macro.name}")


__all__ = ["PlaybackCommandSet"]
