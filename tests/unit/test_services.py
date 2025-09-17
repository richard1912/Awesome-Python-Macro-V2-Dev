from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from src.core.macro_service import MacroService
from src.export_import.package_service import PackageService
from src.models.action import Action
from src.player.playback_service import PlaybackService
from src.scheduler.scheduling_service import SchedulingService
from src.storage.json_storage import JSONStorageManager


def test_macro_service_updates_metadata(tmp_path):
    storage = JSONStorageManager(base_path=tmp_path / "data")
    service = MacroService(storage_manager=storage)
    macro = service.create_macro(name="Editable")

    service.update_macro_metadata(macro.id, description="Updated", tags=["edited"], playback_speed=1.5)
    updated = service.get_macro(macro.id)
    assert updated.description == "Updated"
    assert updated.tags == ["edited"]
    assert updated.playback_speed == 1.5
    assert updated.version == macro.version + 1


def test_playback_service_step_generation(tmp_path):
    storage = JSONStorageManager(base_path=tmp_path / "data")
    service = MacroService(storage_manager=storage)
    macro = service.create_macro(name="Iterator")
    service.add_action(macro.id, Action.delay(macro_id=macro.id, duration_ms=100))
    service.add_action(macro.id, Action.delay(macro_id=macro.id, duration_ms=50))

    playback = PlaybackService(sleep=lambda _: None)
    steps = list(playback.iter_steps(macro, playback_speed=2.0))
    assert len(steps) == 2
    assert steps[0].delay_seconds == 0
    assert steps[1].delay_seconds == pytest.approx(0.05, rel=1e-3)


def test_package_service_metadata(tmp_path):
    storage = JSONStorageManager(base_path=tmp_path / "data")
    macro_service = MacroService(storage_manager=storage)
    package_service = PackageService(storage_manager=storage)
    macro = macro_service.create_macro(name="Meta")

    package_path = package_service.export_macros([macro.id])
    info = package_service.inspect(package_path)
    assert info.macro_count == 1


def test_scheduling_service_toggle(tmp_path):
    storage = JSONStorageManager(base_path=tmp_path / "data")
    macro_service = MacroService(storage_manager=storage)
    playback = PlaybackService(sleep=lambda _: None)
    service = SchedulingService(
        macro_service=macro_service,
        playback_service=playback,
        time_provider=lambda: datetime.now(timezone.utc),
    )
    macro = macro_service.create_macro(name="Schedule")
    schedule = service.create_schedule(
        macro_id=macro.id,
        name="Night",
        start_time=datetime.now(timezone.utc) + timedelta(seconds=5),
        recurrence_type="once",
    )

    service.toggle(schedule.id, enabled=False)
    assert not service.get_schedule(schedule.id).is_enabled
