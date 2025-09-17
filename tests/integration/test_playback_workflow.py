from __future__ import annotations

from src.core.macro_service import MacroService
from src.models.action import Action
from src.player.playback_service import PlaybackService
from src.storage.json_storage import JSONStorageManager


def test_playback_workflow_executes_macro(tmp_path):
    storage = JSONStorageManager(base_path=tmp_path / "data")
    macro_service = MacroService(storage_manager=storage)
    macro = macro_service.create_macro(name="Workflow")
    macro_service.add_action(
        macro.id,
        Action.keyboard_event(
            macro_id=macro.id,
            key_name="w",
            key_code="KeyW",
            is_press=True,
            timestamp_ms=0,
        ),
    )
    macro_service.add_action(
        macro.id,
        Action.mouse_move(macro_id=macro.id, x=100, y=200, timestamp_ms=250),
    )

    playback = PlaybackService(sleep=lambda _: None)
    steps = []
    playback.play_macro(macro, on_step=steps.append, playback_speed=1.5)

    assert len(steps) == 2
    assert steps[0].action.key_name == "w"
    assert steps[1].action.x_coordinate == 100
    assert steps[0].playback_speed == 1.5
