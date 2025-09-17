from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Iterator, List, Optional

from src.models.action import Action
from src.models.macro import Macro
from src.storage.json_storage import JSONStorageManager
from src.utils.validation import ValidationError, ensure_unique_name, validate_macro


class MacroService:
    def __init__(self, *, storage_manager: JSONStorageManager) -> None:
        self.storage = storage_manager
        self._cache: Dict[str, Macro] = {}

    # Creation and retrieval -------------------------------------------------
    def create_macro(
        self,
        *,
        name: str,
        description: str = "",
        tags: Optional[Iterable[str]] = None,
        playback_speed: float = 1.0,
    ) -> Macro:
        ensure_unique_name((macro.name for macro in self.storage.iter_macros()), name)
        macro = Macro.create(name=name, description=description, tags=tags, playback_speed=playback_speed)
        validate_macro(macro)
        self.storage.save_macro(macro)
        self._cache[macro.id] = macro
        return macro

    def get_macro(self, macro_id: str) -> Optional[Macro]:
        if macro_id in self._cache:
            return self._cache[macro_id]
        macro = self.storage.load_macro(macro_id)
        if macro:
            self._cache[macro.id] = macro
        return macro

    def list_macros(self) -> List[Macro]:
        return list(self.iter_macros())

    def iter_macros(self) -> Iterator[Macro]:
        for macro in self.storage.iter_macros():
            cached = self._cache.get(macro.id)
            if cached is None:
                self._cache[macro.id] = macro
                yield macro
            else:
                yield cached

    # Mutations --------------------------------------------------------------
    def add_action(self, macro_id: str, action: Action) -> Action:
        macro = self.get_macro(macro_id)
        if macro is None:
            raise ValidationError(f"Unknown macro: {macro_id}")
        macro.add_action(action)
        validate_macro(macro)
        self.storage.save_macro(macro)
        return action

    def update_macro_metadata(
        self,
        macro_id: str,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[Iterable[str]] = None,
        playback_speed: Optional[float] = None,
    ) -> Macro:
        macro = self.get_macro(macro_id)
        if macro is None:
            raise ValidationError(f"Unknown macro: {macro_id}")
        if name and name != macro.name:
            ensure_unique_name((item.name for item in self.storage.iter_macros() if item.id != macro_id), name)
        updated = Macro.from_dict(macro.to_dict())
        updated.update_metadata(name=name, description=description, tags=tags, playback_speed=playback_speed)
        validate_macro(updated)
        self.storage.save_macro(updated)
        self._cache[macro_id] = updated
        return updated

    def duplicate_macro(self, macro_id: str, *, new_name: str) -> Macro:
        macro = self.get_macro(macro_id)
        if macro is None:
            raise ValidationError(f"Unknown macro: {macro_id}")
        ensure_unique_name((item.name for item in self.storage.iter_macros()), new_name)
        duplicate = macro.duplicate(new_name=new_name)
        validate_macro(duplicate)
        self.storage.save_macro(duplicate)
        return duplicate

    def delete_macro(self, macro_id: str) -> None:
        self.storage.delete_macro(macro_id)
        self._cache.pop(macro_id, None)

    def mark_favorite(self, macro_id: str, is_favorite: bool) -> None:
        macro = self.get_macro(macro_id)
        if macro is None:
            raise ValidationError(f"Unknown macro: {macro_id}")
        macro.mark_favorite(is_favorite)
        self.storage.save_macro(macro)

    # Discovery --------------------------------------------------------------
    def search_macros(self, query: str) -> List[Macro]:
        terms = query.lower().split()
        results = []
        for macro in self.iter_macros():
            haystack = " ".join([macro.name, macro.description, " ".join(macro.tags)]).lower()
            if all(term in haystack for term in terms):
                results.append(macro)
        return results

    def organize(self) -> Dict[str, object]:
        by_tag: Dict[str, List[str]] = {}
        favorites: List[Macro] = []
        for macro in self.iter_macros():
            if macro.is_favorite:
                favorites.append(macro)
            for tag in macro.tags:
                by_tag.setdefault(tag, []).append(macro.id)
        return {"by_tag": by_tag, "favorites": favorites}

    def is_name_taken(self, name: str) -> bool:
        return any(macro.name.lower() == name.lower() for macro in self.iter_macros())


__all__ = ["MacroService"]
