from __future__ import annotations

from src.models.action import Action
from src.ui.action_overlay import ActionOverlay


def test_overlay_highlights_action_coordinates():
    overlay = ActionOverlay()
    action = Action.mouse_click(macro_id="macro", button="left", x=320, y=240, timestamp_ms=100)
    overlay.show_action(action)

    data = overlay.current_overlay
    assert data is not None
    assert data.coordinates == (320, 240)
    assert data.action_id == action.id

    overlay.hide()
    assert overlay.current_overlay is None
