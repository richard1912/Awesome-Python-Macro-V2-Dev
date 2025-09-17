from __future__ import annotations

from src.cli.cli_interface import CLIInterface
from src.cli.recording_commands import RecordingCommandSet
from src.cli.playback_commands import PlaybackCommandSet
from src.cli.macro_commands import MacroCommandSet
from src.core.macro_service import MacroService
from src.player.playback_service import PlaybackService
from src.recorder.input_capture import InputCaptureManager
from src.recorder.recording_service import RecordingService
from src.storage.json_storage import JSONStorageManager
from src.utils.screenshot_service import ScreenshotService


def test_cli_interface_executes_registered_commands(tmp_path):
    storage = JSONStorageManager(base_path=tmp_path / "data")
    macro_service = MacroService(storage_manager=storage)
    recording_service = RecordingService(
        capture_manager=InputCaptureManager(),
        macro_service=macro_service,
        screenshot_service=ScreenshotService(),
    )
    playback_service = PlaybackService(sleep=lambda _: None)

    cli = CLIInterface()
    cli.register_commands(RecordingCommandSet(recording_service))
    cli.register_commands(PlaybackCommandSet(playback_service, macro_service))
    cli.register_commands(MacroCommandSet(macro_service))

    response = cli.execute("macro create", name="CLI Macro")
    assert "CLI Macro" in response.message

    macro_id = macro_service.search_macros("CLI Macro")[0].id
    response = cli.execute("playback run", macro_id=macro_id)
    assert response.ok

    response = cli.execute("recording status")
    assert response.ok
