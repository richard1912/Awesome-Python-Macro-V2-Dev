from __future__ import annotations

from typing import Iterable, Optional

from src.core.macro_service import MacroService
from src.models.macro import Macro


class MacroEditorDialog:
    def __init__(self, *, macro_service: MacroService) -> None:
        self.macro_service = macro_service
        self._macro: Optional[Macro] = None
        self._pending_name: Optional[str] = None
        self._pending_tags: Optional[Iterable[str]] = None

    def load_macro(self, macro: Macro) -> None:
        self._macro = macro
        self._pending_name = macro.name
        self._pending_tags = macro.tags

    def update_name(self, name: str) -> None:
        self._pending_name = name

    def update_tags(self, tags: Iterable[str]) -> None:
        self._pending_tags = list(tags)

    def apply_changes(self) -> None:
        if not self._macro:
            return
        self.macro_service.update_macro_metadata(
            self._macro.id,
            name=self._pending_name,
            tags=self._pending_tags,
        )


__all__ = ["MacroEditorDialog"]
