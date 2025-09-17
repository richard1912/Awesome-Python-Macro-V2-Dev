from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Protocol


@dataclass
class CLIResponse:
    ok: bool
    message: str = ""


class CommandSet(Protocol):
    prefix: str

    def commands(self) -> Dict[str, Callable[..., CLIResponse]]:
        ...


class CLIInterface:
    def __init__(self) -> None:
        self._commands: Dict[str, Callable[..., CLIResponse]] = {}

    def register_commands(self, command_set: CommandSet) -> None:
        for name, handler in command_set.commands().items():
            key = f"{command_set.prefix} {name}".strip()
            self._commands[key] = handler

    def execute(self, command: str, **kwargs) -> CLIResponse:
        handler = self._commands.get(command)
        if handler is None:
            return CLIResponse(ok=False, message=f"Unknown command: {command}")
        return handler(**kwargs)


__all__ = ["CLIInterface", "CLIResponse", "CommandSet"]
