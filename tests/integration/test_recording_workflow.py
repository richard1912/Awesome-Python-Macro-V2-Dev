from __future__ import annotations

from src.core.macro_service import MacroService
from src.recorder.input_capture import InputCaptureManager
from src.recorder.recording_service import RecordingService
from src.storage.json_storage import JSONStorageManager
from src.utils.screenshot_service import ScreenshotService


def test_recording_workflow_persists_macro(tmp_path):
    storage = JSONStorageManager(base_path=tmp_path / "data")
    macro_service = MacroService(storage_manager=storage)
    capture_manager = InputCaptureManager()
    recording = RecordingService(
        capture_manager=capture_manager,
        macro_service=macro_service,
        screenshot_service=ScreenshotService(),
    )

    session = recording.start_recording(name="Workflow Macro")

    capture_manager.emit({"kind": "keyboard", "state": "press", "key": "x", "timestamp": 0.0})
    capture_manager.emit({"kind": "mouse", "state": "click", "button": "left", "x": 1, "y": 2, "timestamp": 25})
    capture_manager.emit({"kind": "delay", "duration": 50, "timestamp": 75})

    macro = recording.stop_recording(session.session_id)

    reloaded = macro_service.get_macro(macro.id)
    assert reloaded is not None
    assert reloaded.total_duration_ms == macro.total_duration_ms
    assert len(reloaded.actions) == 3
    assert storage.macro_path(macro.id).exists()
