from __future__ import annotations

from datetime import datetime, timedelta, timezone

from src.core.macro_service import MacroService
from src.models.action import Action
from src.scheduler.scheduling_service import SchedulingService
from src.storage.json_storage import JSONStorageManager


class DummyPlaybackService:
    def __init__(self) -> None:
        self.played: list[str] = []

    def play_macro(self, macro, **kwargs):  # pragma: no cover - simple stub
        self.played.append(macro.id)


def test_scheduling_runs_due_macros(tmp_path):
    storage = JSONStorageManager(base_path=tmp_path / "data")
    macro_service = MacroService(storage_manager=storage)
    playback = DummyPlaybackService()
    clock_time = datetime.now(timezone.utc)

    service = SchedulingService(
        macro_service=macro_service,
        playback_service=playback,
        time_provider=lambda: clock_time,
    )

    macro = macro_service.create_macro(name="Scheduled")
    macro_service.add_action(macro.id, Action.delay(macro_id=macro.id, duration_ms=10))

    service.create_schedule(
        macro_id=macro.id,
        name="Morning",
        start_time=clock_time + timedelta(seconds=5),
        recurrence_type="once",
    )

    service.run_pending()
    assert playback.played == []

    clock_time = clock_time + timedelta(seconds=6)
    service.run_pending()
    assert playback.played == [macro.id]
