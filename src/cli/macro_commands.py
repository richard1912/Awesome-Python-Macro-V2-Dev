from __future__ import annotations

from src.cli.cli_interface import CLIResponse
from src.core.macro_service import MacroService


class MacroCommandSet:
    prefix = "macro"

    def __init__(self, macro_service: MacroService) -> None:
        self.macro_service = macro_service

    def commands(self) -> dict[str, callable]:
        return {"create": self.create}

    def create(self, name: str, description: str | None = None) -> CLIResponse:
        macro = self.macro_service.create_macro(name=name, description=description or "")
        return CLIResponse(ok=True, message=f"Created macro {macro.name}")


__all__ = ["MacroCommandSet"]
