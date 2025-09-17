from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

from src.models.macro import Macro


@dataclass
class MacroListItem:
    id: str
    name: str
    is_favorite: bool


class MacroListWidget:
    def __init__(self) -> None:
        self._items: List[MacroListItem] = []

    def set_macros(self, macros: Iterable[Macro]) -> None:
        self._items = [
            MacroListItem(id=macro.id, name=macro.name, is_favorite=macro.is_favorite)
            for macro in sorted(macros, key=lambda item: item.name.lower())
        ]

    @property
    def items(self) -> List[MacroListItem]:
        return list(self._items)

    @property
    def count(self) -> int:
        return len(self._items)


__all__ = ["MacroListWidget", "MacroListItem"]
