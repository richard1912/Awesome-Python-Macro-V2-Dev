from __future__ import annotations

from typing import Dict

from src.models.action import Action


class MouseHandler:
    def create_action(self, macro_id: str, event: Dict[str, object]) -> Action:
        state = event.get("state", "move")
        timestamp = float(event.get("timestamp", 0.0))
        if state == "click":
            return Action.mouse_click(
                macro_id=macro_id,
                button=str(event.get("button", "left")),
                x=int(event.get("x", 0)),
                y=int(event.get("y", 0)),
                timestamp_ms=timestamp,
            )
        if state == "move":
            return Action.mouse_move(
                macro_id=macro_id,
                x=int(event.get("x", 0)),
                y=int(event.get("y", 0)),
                timestamp_ms=timestamp,
            )
        if state == "scroll":
            return Action.mouse_scroll(
                macro_id=macro_id,
                direction=str(event.get("direction", "vertical")),
                amount=int(event.get("amount", 0)),
                timestamp_ms=timestamp,
            )
        if state == "delay":
            return Action.delay(macro_id=macro_id, duration_ms=timestamp)
        return Action.mouse_move(
            macro_id=macro_id,
            x=int(event.get("x", 0)),
            y=int(event.get("y", 0)),
            timestamp_ms=timestamp,
        )


__all__ = ["MouseHandler"]
