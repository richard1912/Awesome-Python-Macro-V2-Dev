from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional
from uuid import uuid4

from src.core.macro_service import MacroService
from src.models.action import Action
from src.models.macro import Macro
from src.recorder.input_capture import InputCaptureManager
from src.recorder.keyboard_handler import KeyboardHandler
from src.recorder.mouse_handler import MouseHandler
from src.utils.screenshot_service import ScreenshotService
from src.utils.validation import ValidationError


@dataclass
class RecordingSession:
    session_id: str
    macro_id: str


class RecordingService:
    def __init__(
        self,
        *,
        capture_manager: InputCaptureManager,
        macro_service: MacroService,
        screenshot_service: ScreenshotService,
        keyboard_handler: Optional[KeyboardHandler] = None,
        mouse_handler: Optional[MouseHandler] = None,
    ) -> None:
        self.capture_manager = capture_manager
        self.macro_service = macro_service
        self.screenshot_service = screenshot_service
        self.keyboard_handler = keyboard_handler or KeyboardHandler()
        self.mouse_handler = mouse_handler or MouseHandler()
        self._session: Optional[RecordingSession] = None

    def start_recording(
        self,
        *,
        name: str,
        description: str | None = None,
        tags: Optional[Iterable[str]] = None,
        playback_speed: float = 1.0,
    ) -> RecordingSession:
        if self._session is not None:
            raise ValidationError("Recording already in progress")
        macro = self.macro_service.create_macro(
            name=name,
            description=description or "",
            tags=list(tags or []),
            playback_speed=playback_speed,
        )
        self._session = RecordingSession(session_id=str(uuid4()), macro_id=macro.id)
        self.capture_manager.start(self._handle_event)
        return self._session

    def stop_recording(self, session_id: Optional[str] = None) -> Optional[Macro]:
        if self._session is None:
            return None
        if session_id is not None and session_id != self._session.session_id:
            raise ValidationError("Unknown session identifier")
        self.capture_manager.stop(self._handle_event)
        macro = self.macro_service.get_macro(self._session.macro_id)
        self._session = None
        return macro

    def _handle_event(self, event: dict) -> None:
        if self._session is None:
            return
        macro_id = self._session.macro_id
        kind = event.get("kind", "mouse")
        if kind == "keyboard":
            action = self.keyboard_handler.create_action(macro_id, event)
        elif kind == "mouse":
            action = self.mouse_handler.create_action(macro_id, event)
        elif kind == "delay":
            action = Action.delay(
                macro_id=macro_id,
                duration_ms=float(event.get("duration", event.get("timestamp", 0.0))),
                timestamp_ms=float(event.get("timestamp", 0.0)),
            )
        else:
            return
        self.screenshot_service.attach(action)
        self.macro_service.add_action(macro_id, action)

    def status(self) -> str:
        if self._session is None:
            return "idle"
        return f"recording:{self._session.macro_id}"


__all__ = ["RecordingService", "RecordingSession"]
