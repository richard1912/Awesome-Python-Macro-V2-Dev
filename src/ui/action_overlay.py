from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from src.models.action import Action


@dataclass
class OverlayState:
    action_id: str
    coordinates: Tuple[int, int]


class ActionOverlay(QWidget):
    """Semi-transparent overlay highlighting macro actions during playback."""

    def __init__(self) -> None:
        super().__init__(
            None,
            Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowDoesNotAcceptFocus,
        )
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowTitle("Macro Action Overlay")
        self.resize(200, 120)

        self._label = QLabel("", self)
        self._label.setAlignment(Qt.AlignCenter)
        self._label.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.addWidget(self._label)

        self.current_overlay: Optional[OverlayState] = None

    def show_action(self, action: Action) -> None:
        x = action.x_coordinate or 0
        y = action.y_coordinate or 0
        self.current_overlay = OverlayState(action_id=action.id, coordinates=(x, y))
        description = action.action_type.name.replace("_", " ").title()
        self._label.setText(f"{description}\n({x}, {y})")
        self.move(max(x - self.width() // 2, 0), max(y - self.height() // 2, 0))
        self.show()
        self.raise_()

    def hide(self) -> None:  # type: ignore[override]
        self.current_overlay = None
        super().hide()

    def paintEvent(self, event) -> None:  # type: ignore[override]
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        color = QColor(45, 140, 255, 170)
        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 16, 16)
        super().paintEvent(event)


__all__ = ["ActionOverlay", "OverlayState"]
