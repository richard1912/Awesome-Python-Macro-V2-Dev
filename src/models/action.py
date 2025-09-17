from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4

from src.models.screenshot import Screenshot


class ActionType(str, Enum):
    KEYBOARD_PRESS = "keyboard_press"
    KEYBOARD_RELEASE = "keyboard_release"
    MOUSE_CLICK = "mouse_click"
    MOUSE_MOVE = "mouse_move"
    MOUSE_SCROLL = "mouse_scroll"
    DELAY = "delay"


@dataclass
class Action:
    id: str
    macro_id: str
    action_type: ActionType
    timestamp: float
    key_code: Optional[str] = None
    key_name: Optional[str] = None
    modifier_keys: List[str] = field(default_factory=list)
    mouse_button: Optional[str] = None
    x_coordinate: Optional[int] = None
    y_coordinate: Optional[int] = None
    scroll_direction: Optional[str] = None
    delay_duration: Optional[float] = None
    comment: Optional[str] = None
    screenshot: Optional[Screenshot] = None

    @property
    def timestamp_ms(self) -> float:
        return float(self.timestamp)

    @property
    def timestamp_seconds(self) -> float:
        return self.timestamp_ms / 1000.0

    @classmethod
    def keyboard_event(
        cls,
        *,
        macro_id: str,
        key_name: str,
        key_code: Optional[str] = None,
        is_press: bool,
        timestamp_ms: float = 0.0,
        modifiers: Optional[List[str]] = None,
    ) -> "Action":
        action_type = ActionType.KEYBOARD_PRESS if is_press else ActionType.KEYBOARD_RELEASE
        return cls(
            id=str(uuid4()),
            macro_id=macro_id,
            action_type=action_type,
            timestamp=timestamp_ms,
            key_code=key_code or key_name.upper(),
            key_name=key_name,
            modifier_keys=list(modifiers or []),
        )

    @classmethod
    def mouse_click(
        cls,
        *,
        macro_id: str,
        button: str,
        x: int,
        y: int,
        timestamp_ms: float,
    ) -> "Action":
        if x < 0 or y < 0:
            from src.utils.validation import ValidationError  # local import to avoid cycle

            raise ValidationError("Coordinates must be non-negative")
        return cls(
            id=str(uuid4()),
            macro_id=macro_id,
            action_type=ActionType.MOUSE_CLICK,
            timestamp=timestamp_ms,
            mouse_button=button,
            x_coordinate=x,
            y_coordinate=y,
        )

    @classmethod
    def mouse_move(
        cls,
        *,
        macro_id: str,
        x: int,
        y: int,
        timestamp_ms: float,
    ) -> "Action":
        if x < 0 or y < 0:
            from src.utils.validation import ValidationError

            raise ValidationError("Coordinates must be non-negative")
        return cls(
            id=str(uuid4()),
            macro_id=macro_id,
            action_type=ActionType.MOUSE_MOVE,
            timestamp=timestamp_ms,
            x_coordinate=x,
            y_coordinate=y,
        )

    @classmethod
    def mouse_scroll(
        cls,
        *,
        macro_id: str,
        direction: str,
        amount: int,
        timestamp_ms: float,
    ) -> "Action":
        return cls(
            id=str(uuid4()),
            macro_id=macro_id,
            action_type=ActionType.MOUSE_SCROLL,
            timestamp=timestamp_ms,
            scroll_direction=f"{direction}:{amount}",
        )

    @classmethod
    def delay(
        cls,
        *,
        macro_id: str,
        duration_ms: float,
        timestamp_ms: float | None = None,
    ) -> "Action":
        return cls(
            id=str(uuid4()),
            macro_id=macro_id,
            action_type=ActionType.DELAY,
            timestamp=timestamp_ms if timestamp_ms is not None else 0.0,
            delay_duration=duration_ms,
        )

    def clone(self, *, macro_id: Optional[str] = None) -> "Action":
        payload = self.to_dict()
        payload["id"] = str(uuid4())
        payload["macro_id"] = macro_id or self.macro_id
        return Action.from_dict(payload)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "macro_id": self.macro_id,
            "action_type": self.action_type.value,
            "timestamp": self.timestamp,
            "key_code": self.key_code,
            "key_name": self.key_name,
            "modifier_keys": list(self.modifier_keys),
            "mouse_button": self.mouse_button,
            "x_coordinate": self.x_coordinate,
            "y_coordinate": self.y_coordinate,
            "scroll_direction": self.scroll_direction,
            "delay_duration": self.delay_duration,
            "comment": self.comment,
            "screenshot": self.screenshot.to_dict() if self.screenshot else None,
        }

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "Action":
        screenshot_payload = payload.get("screenshot")
        screenshot = Screenshot.from_dict(screenshot_payload) if screenshot_payload else None
        return cls(
            id=payload["id"],
            macro_id=payload["macro_id"],
            action_type=ActionType(payload["action_type"]),
            timestamp=float(payload.get("timestamp", 0.0)),
            key_code=payload.get("key_code"),
            key_name=payload.get("key_name"),
            modifier_keys=list(payload.get("modifier_keys", [])),
            mouse_button=payload.get("mouse_button"),
            x_coordinate=payload.get("x_coordinate"),
            y_coordinate=payload.get("y_coordinate"),
            scroll_direction=payload.get("scroll_direction"),
            delay_duration=payload.get("delay_duration"),
            comment=payload.get("comment"),
            screenshot=screenshot,
        )


__all__ = ["Action", "ActionType"]
