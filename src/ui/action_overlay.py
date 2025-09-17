from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

from src.models.action import Action


@dataclass
class OverlayState:
    action_id: str
    coordinates: Tuple[int, int]


class ActionOverlay:
    def __init__(self) -> None:
        self.current_overlay: Optional[OverlayState] = None

    def show_action(self, action: Action) -> None:
        coordinates = (action.x_coordinate or 0, action.y_coordinate or 0)
        self.current_overlay = OverlayState(action_id=action.id, coordinates=coordinates)

    def hide(self) -> None:
        self.current_overlay = None


__all__ = ["ActionOverlay", "OverlayState"]
