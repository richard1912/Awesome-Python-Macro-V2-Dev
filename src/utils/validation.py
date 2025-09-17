from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Iterable

if TYPE_CHECKING:  # pragma: no cover - type checking only
    from src.models.action import Action
    from src.models.hotkey import Hotkey
    from src.models.macro import Macro
    from src.models.schedule import Schedule


class ValidationError(Exception):
    """Raised when a model fails validation."""


@dataclass(frozen=True)
class ValidationIssue:
    field: str
    message: str


def _raise(field: str, message: str) -> None:
    raise ValidationError(f"{field}: {message}")


def validate_macro(macro: "Macro") -> None:
    if not macro.name.strip():
        _raise("name", "Macro name cannot be empty")
    if macro.playback_speed <= 0 or macro.playback_speed > 10.0:
        _raise("playback_speed", "Playback speed must be between 0 and 10")
    if macro.loop_count < 0:
        _raise("loop_count", "Loop count must be positive")
    if macro.loop_interval < 0:
        _raise("loop_interval", "Loop interval must be positive")
    for action in macro.actions:
        validate_action(action)


def validate_action(action: "Action") -> None:
    if action.timestamp < 0:
        _raise("timestamp", "Timestamp cannot be negative")
    if action.x_coordinate is not None and action.x_coordinate < 0:
        _raise("x_coordinate", "X coordinate must be non-negative")
    if action.y_coordinate is not None and action.y_coordinate < 0:
        _raise("y_coordinate", "Y coordinate must be non-negative")
    if action.action_type.value.startswith("keyboard") and not action.key_name:
        _raise("key_name", "Keyboard events must include key name")
    if action.action_type.name == "MOUSE_CLICK" and action.mouse_button is None:
        _raise("mouse_button", "Mouse click must define a button")
    if action.delay_duration is not None and action.delay_duration < 0:
        _raise("delay_duration", "Delay must be positive")


def validate_hotkey(hotkey: "Hotkey") -> None:
    if not hotkey.key_combination:
        _raise("key_combination", "Hotkey must define a key combination")
    if hotkey.action_type.requires_macro and not hotkey.macro_id:
        _raise("macro_id", "Hotkey requires macro reference")


def validate_schedule(schedule: "Schedule") -> None:
    if not schedule.name:
        _raise("name", "Schedule name required")
    if schedule.start_time is None:
        _raise("start_time", "Schedule requires start time")


def ensure_unique_name(existing: Iterable[str], candidate: str) -> None:
    lowered = {name.lower() for name in existing}
    if candidate.lower() in lowered:
        _raise("name", "Name must be unique")


__all__ = [
    "ValidationError",
    "ValidationIssue",
    "validate_macro",
    "validate_action",
    "validate_hotkey",
    "validate_schedule",
    "ensure_unique_name",
]
