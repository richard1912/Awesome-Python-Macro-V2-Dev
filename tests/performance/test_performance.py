from __future__ import annotations

from src.core.macro_service import MacroService
from src.models.action import Action
from src.player.playback_service import PlaybackService
from src.storage.json_storage import JSONStorageManager


def test_playback_timing_accuracy(tmp_path):
    storage = JSONStorageManager(base_path=tmp_path / "data")
    macro_service = MacroService(storage_manager=storage)
    macro = macro_service.create_macro(name="Timing")
    macro_service.add_action(macro.id, Action.delay(macro_id=macro.id, duration_ms=0))
    macro_service.add_action(macro.id, Action.delay(macro_id=macro.id, duration_ms=10))
    macro_service.add_action(macro.id, Action.delay(macro_id=macro.id, duration_ms=20))

    playback = PlaybackService(sleep=lambda _: None)
    steps = list(playback.iter_steps(macro))
    expected_delays = [0, 0.01, 0.02]

    for step, expected in zip(steps, expected_delays):
        assert abs(step.delay_seconds - expected) < 0.01


def test_macro_iteration_is_lazy(tmp_path):
    storage = JSONStorageManager(base_path=tmp_path / "data")
    service = MacroService(storage_manager=storage)

    for index in range(100):
        service.create_macro(name=f"Macro {index}")

    iterator = service.iter_macros()
    assert not isinstance(iterator, list)
    count = sum(1 for _ in iterator)
    assert count == 100
