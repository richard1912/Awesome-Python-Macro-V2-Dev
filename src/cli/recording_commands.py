from __future__ import annotations

from src.cli.cli_interface import CLIResponse
from src.recorder.recording_service import RecordingService


class RecordingCommandSet:
    prefix = "recording"

    def __init__(self, recording_service: RecordingService) -> None:
        self.recording_service = recording_service

    def commands(self) -> dict[str, callable]:
        return {
            "status": self.status,
            "start": self.start,
            "stop": self.stop,
        }

    def status(self) -> CLIResponse:
        return CLIResponse(ok=True, message=self.recording_service.status())

    def start(self, name: str) -> CLIResponse:
        session = self.recording_service.start_recording(name=name)
        return CLIResponse(ok=True, message=f"recording {session.macro_id}")

    def stop(self) -> CLIResponse:
        macro = self.recording_service.stop_recording()
        return CLIResponse(ok=True, message=f"saved {macro.id if macro else 'nothing'}")


__all__ = ["RecordingCommandSet"]
