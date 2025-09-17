from __future__ import annotations

from typing import Dict, List

from src.models.action import Action


class KeyboardHandler:
    def create_action(self, macro_id: str, event: Dict[str, object]) -> Action:
        key_name = str(event.get("key", ""))
        is_press = event.get("state", "press") == "press"
        timestamp = float(event.get("timestamp", 0.0))
        modifiers: List[str] = list(event.get("mods", []))
        return Action.keyboard_event(
            macro_id=macro_id,
            key_name=key_name,
            key_code=str(event.get("key_code", key_name.upper() or "Key")),
            is_press=is_press,
            timestamp_ms=timestamp,
            modifiers=modifiers,
        )


__all__ = ["KeyboardHandler"]
