from __future__ import annotations

import pytest

from src.core.macro_service import MacroService
from src.models.action import Action
from src.player.playback_service import PlaybackService


def test_playback_service_preserves_order_and_timing(storage_manager):
    macro_service = MacroService(storage_manager=storage_manager)
    macro = macro_service.create_macro(name="Playback Demo")
    first = Action.keyboard_event(
        macro_id=macro.id,
        key_name="a",
        key_code="KeyA",
        is_press=True,
        timestamp_ms=0,
        modifiers=["ctrl"],
    )
    second = Action.mouse_click(
        macro_id=macro.id,
        button="left",
        x=100,
        y=200,
        timestamp_ms=600,
    )
    macro_service.add_action(macro.id, first)
    macro_service.add_action(macro.id, second)

    collected = []
    delays = []
    playback = PlaybackService(sleep=delays.append)

    playback.play_macro(macro, on_step=collected.append)

    assert [step.action.id for step in collected] == [first.id, second.id]
    assert pytest.approx(sum(delays), rel=1e-3) == pytest.approx(0.6, rel=1e-3)
    assert delays[0] == 0
    assert pytest.approx(delays[1], rel=1e-3) == pytest.approx(0.6, rel=1e-3)


def test_playback_service_supports_looping(storage_manager):
    macro_service = MacroService(storage_manager=storage_manager)
    macro = macro_service.create_macro(name="Loop Demo")
    macro_service.add_action(
        macro.id,
        Action.delay(macro_id=macro.id, duration_ms=250),
    )

    collected = []
    playback = PlaybackService(sleep=lambda _: None)
    playback.play_macro(macro, on_step=collected.append, loop_count=2)

    assert len(collected) == 2
    assert collected[0].sequence_index == 0
    assert collected[1].sequence_index == 1
