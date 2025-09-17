from __future__ import annotations

import pytest

from src.core.macro_service import MacroService
from src.recorder.input_capture import InputCaptureManager
from src.recorder.recording_service import RecordingService
from src.utils.screenshot_service import ScreenshotService
from src.utils.validation import ValidationError


def test_recording_api_creates_macro_with_actions(storage_manager):
    capture_manager = InputCaptureManager()
    screenshot_service = ScreenshotService()
    macro_service = MacroService(storage_manager=storage_manager)
    recording_service = RecordingService(
        capture_manager=capture_manager,
        macro_service=macro_service,
        screenshot_service=screenshot_service,
    )

    session = recording_service.start_recording(
        name="Demo Macro", description="Sample", tags=["login"], playback_speed=1.0
    )

    capture_manager.emit(
        {"kind": "keyboard", "state": "press", "key": "A", "timestamp": 0.0, "mods": ["ctrl"]}
    )
    capture_manager.emit(
        {
            "kind": "keyboard",
            "state": "release",
            "key": "A",
            "timestamp": 12.5,
            "mods": ["ctrl"],
        }
    )
    capture_manager.emit(
        {
            "kind": "mouse",
            "state": "click",
            "button": "left",
            "x": 640,
            "y": 480,
            "timestamp": 75.0,
        }
    )

    macro = recording_service.stop_recording(session.session_id)

    assert macro.name == "Demo Macro"
    assert len(macro.actions) == 3
    assert macro.actions[0].action_type.value == "keyboard_press"
    assert macro.actions[-1].screenshot is not None
    stored = macro_service.get_macro(macro.id)
    assert stored is not None
    assert stored.total_duration_ms >= 75


def test_recording_api_prevents_parallel_sessions(storage_manager):
    capture_manager = InputCaptureManager()
    screenshot_service = ScreenshotService()
    macro_service = MacroService(storage_manager=storage_manager)
    recording_service = RecordingService(
        capture_manager=capture_manager,
        macro_service=macro_service,
        screenshot_service=screenshot_service,
    )

    recording_service.start_recording(name="Primary")

    with pytest.raises(ValidationError):
        recording_service.start_recording(name="Secondary")

    recording_service.stop_recording()
