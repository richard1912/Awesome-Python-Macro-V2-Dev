from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from src.models.screenshot import Screenshot


class ScreenshotService:
    """Provides lightweight screenshot handling for tests and automation."""

    def __init__(self, enabled: bool = True) -> None:
        self.enabled = enabled

    def capture_for_action(self, macro_id: str, action_id: str) -> Optional[Screenshot]:
        if not self.enabled:
            return None
        return Screenshot.create_placeholder(
            macro_id=macro_id,
            action_id=action_id,
            captured_at=datetime.now(timezone.utc),
        )

    def attach(self, action: "Action") -> None:
        from src.models.action import Action  # local import to avoid cycle

        if not isinstance(action, Action):  # pragma: no cover - safety guard
            return
        screenshot = self.capture_for_action(action.macro_id, action.id)
        action.screenshot = screenshot


__all__ = ["ScreenshotService"]
