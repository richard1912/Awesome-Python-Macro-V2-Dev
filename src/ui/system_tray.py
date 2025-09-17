from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QMenu, QStyle, QSystemTrayIcon, QWidget

from src.core.macro_service import MacroService
from src.player.playback_service import PlaybackService


@dataclass
class TrayEntry:
    label: str
    macro_id: str


class SystemTrayManager(QObject):
    """Create and manage a system tray menu for quick macro access."""

    macro_triggered = Signal(str)

    def __init__(
        self,
        *,
        macro_service: MacroService,
        playback_service: PlaybackService,
        parent: Optional[QObject] = None,
    ) -> None:
        super().__init__(parent)
        self.macro_service = macro_service
        self.playback_service = playback_service
        self._entries: List[TrayEntry] = []
        self._window: Optional[QWidget] = None
        self.tray_icon: Optional[QSystemTrayIcon] = None
        self._menu: Optional[QMenu] = None
        self.is_available = False
        self._create_tray_icon()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def bind_window(self, window: QWidget) -> None:
        self._window = window
        self._rebuild_menu()

    def build_quick_actions(self) -> List[TrayEntry]:
        macros = sorted(self.macro_service.list_macros(), key=lambda macro: macro.name.lower())
        self._entries = [TrayEntry(label=macro.name, macro_id=macro.id) for macro in macros]
        self._rebuild_menu()
        return list(self._entries)

    def trigger_action(self, macro_id: str) -> None:
        macro = self.macro_service.get_macro(macro_id)
        if macro is None:
            return
        self.playback_service.play_macro(macro)
        self.macro_triggered.emit(macro_id)

    def show_notification(self, title: str, message: str) -> None:
        if self.tray_icon is not None and self.is_available:
            self.tray_icon.showMessage(title, message, QSystemTrayIcon.Information, 3000)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _create_tray_icon(self) -> None:
        app = QApplication.instance()
        if app is None or not QSystemTrayIcon.isSystemTrayAvailable():
            self.is_available = False
            return
        self.tray_icon = QSystemTrayIcon(self)
        icon = app.style().standardIcon(QStyle.SP_ComputerIcon)
        if not icon.isNull():
            self.tray_icon.setIcon(icon)
        self.tray_icon.setToolTip("Awesome Python Macro")
        self._menu = QMenu()
        self.tray_icon.setContextMenu(self._menu)
        self.tray_icon.activated.connect(self._on_tray_activated)
        self.tray_icon.show()
        self.is_available = True
        self._rebuild_menu()

    def _rebuild_menu(self) -> None:
        if self._menu is None:
            return
        self._menu.clear()
        for entry in self._entries:
            action = QAction(entry.label, self._menu)
            action.triggered.connect(lambda checked=False, mid=entry.macro_id: self.trigger_action(mid))
            self._menu.addAction(action)
        if self._window is not None:
            if self._entries:
                self._menu.addSeparator()
            show_action = QAction("Show Window", self._menu)
            show_action.triggered.connect(self._show_window)
            self._menu.addAction(show_action)
            hide_action = QAction("Hide Window", self._menu)
            hide_action.triggered.connect(self._hide_window)
            self._menu.addAction(hide_action)
        if self._menu.actions():
            self._menu.addSeparator()
        quit_action = QAction("Quit", self._menu)
        app = QApplication.instance()
        if app is not None:
            quit_action.triggered.connect(app.quit)
        self._menu.addAction(quit_action)

    def _on_tray_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason == QSystemTrayIcon.Trigger and self._window is not None:
            self._show_window()

    def _show_window(self) -> None:
        if self._window is None:
            return
        self._window.show()
        self._window.raise_()
        self._window.activateWindow()

    def _hide_window(self) -> None:
        if self._window is None:
            return
        self._window.hide()


__all__ = ["SystemTrayManager", "TrayEntry"]
