from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional
from uuid import uuid4


class HotkeyActionType(str, Enum):
    START_RECORDING = "start_recording"
    STOP_RECORDING = "stop_recording"
    PLAY_MACRO = "play_macro"
    SHOW_WINDOW = "show_window"
    HIDE_WINDOW = "hide_window"
    MINIMIZE_TO_TRAY = "minimize_to_tray"

    @property
    def requires_macro(self) -> bool:
        return self is HotkeyActionType.PLAY_MACRO


@dataclass
class Hotkey:
    id: str
    key_combination: str
    action_type: HotkeyActionType
    macro_id: Optional[str] = None
    is_enabled: bool = True
    is_global: bool = True
    conflict_resolution: str = "prompt_user"

    @classmethod
    def create(
        cls,
        *,
        key_combination: str,
        action_type: HotkeyActionType,
        macro_id: Optional[str] = None,
        is_global: bool = True,
    ) -> "Hotkey":
        return cls(
            id=str(uuid4()),
            key_combination=key_combination,
            action_type=action_type,
            macro_id=macro_id,
            is_enabled=True,
            is_global=is_global,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "key_combination": self.key_combination,
            "action_type": self.action_type.value,
            "macro_id": self.macro_id,
            "is_enabled": self.is_enabled,
            "is_global": self.is_global,
            "conflict_resolution": self.conflict_resolution,
        }

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "Hotkey":
        return cls(
            id=payload["id"],
            key_combination=payload["key_combination"],
            action_type=HotkeyActionType(payload["action_type"]),
            macro_id=payload.get("macro_id"),
            is_enabled=payload.get("is_enabled", True),
            is_global=payload.get("is_global", True),
            conflict_resolution=payload.get("conflict_resolution", "prompt_user"),
        )


__all__ = ["Hotkey", "HotkeyActionType"]
