from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QCloseEvent
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFrame,
    QLabel,
    QMainWindow,
    QMenuBar,
    QMessageBox,
    QPushButton,
    QSplitter,
    QStatusBar,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from src.core.macro_service import MacroService
from src.hotkeys.hotkey_service import HotkeyService
from src.models.action import ActionType
from src.models.macro import Macro
from src.models.user_settings import UserSettings
from src.player.playback_service import PlaybackService, PlaybackStep
from src.ui.action_overlay import ActionOverlay
from src.ui.hotkey_dialog import HotkeyDialog
from src.ui.macro_editor_dialog import MacroEditorDialog
from src.ui.macro_list_widget import MacroListWidget
from src.ui.settings_dialog import SettingsDialog

if TYPE_CHECKING:  # pragma: no cover - for typing only
    from src.ui.system_tray import SystemTrayManager
    from src.storage.json_storage import JSONStorageManager


class MainWindow(QMainWindow):
    """PySide6 main window tying together macro playback and management."""

    def __init__(
        self,
        *,
        macro_service: MacroService,
        playback_service: PlaybackService,
        hotkey_service: HotkeyService,
        settings: Optional[UserSettings] = None,
        storage_manager: Optional["JSONStorageManager"] = None,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("Awesome Python Macro")
        self.resize(1080, 720)

        self.macro_service = macro_service
        self.playback_service = playback_service
        self.hotkey_service = hotkey_service
        self.user_settings = settings or UserSettings()
        self._storage_manager = storage_manager
        self._system_tray: Optional[SystemTrayManager] = None

        self.overlay = ActionOverlay()
        self._hotkey_dialog: Optional[HotkeyDialog] = None
        self._settings_dialog: Optional[SettingsDialog] = None

        self._build_menu_bar()
        self._build_tool_bar()
        self._build_central_widget()
        self._build_status_bar()

        self.refresh_macro_list()

    # ------------------------------------------------------------------
    # UI construction helpers
    # ------------------------------------------------------------------
    def _build_menu_bar(self) -> None:
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        file_menu = menu_bar.addMenu("File")
        self._action_new_macro = QAction("New Macro", self)
        self._action_new_macro.triggered.connect(self.create_macro)
        file_menu.addAction(self._action_new_macro)

        self._action_duplicate = QAction("Duplicate Macro", self)
        self._action_duplicate.triggered.connect(self.duplicate_selected_macro)
        file_menu.addAction(self._action_duplicate)

        self._action_delete = QAction("Delete Macro", self)
        self._action_delete.triggered.connect(self.delete_selected_macro)
        file_menu.addAction(self._action_delete)

        file_menu.addSeparator()

        exit_action = QAction("Exit", self)
        app = QApplication.instance()
        if app is not None:
            exit_action.triggered.connect(app.quit)
        else:  # pragma: no cover - fallback for headless tests
            exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        view_menu = menu_bar.addMenu("View")
        self._action_refresh = QAction("Refresh", self)
        self._action_refresh.triggered.connect(self.refresh_macro_list)
        view_menu.addAction(self._action_refresh)

        tools_menu = menu_bar.addMenu("Tools")
        self._action_edit = QAction("Edit Macro", self)
        self._action_edit.triggered.connect(self.edit_selected_macro)
        tools_menu.addAction(self._action_edit)

        self._action_toggle_favorite = QAction("Toggle Favorite", self)
        self._action_toggle_favorite.triggered.connect(self._toggle_selected_favorite)
        tools_menu.addAction(self._action_toggle_favorite)

        tools_menu.addSeparator()

        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.open_settings)
        tools_menu.addAction(settings_action)

        hotkeys_action = QAction("Hotkey Manager", self)
        hotkeys_action.triggered.connect(self.open_hotkey_manager)
        tools_menu.addAction(hotkeys_action)

    def _build_tool_bar(self) -> None:
        tool_bar = QToolBar("Main Toolbar", self)
        tool_bar.setMovable(False)
        tool_bar.setIconSize(tool_bar.iconSize() * 1.2)
        self.addToolBar(Qt.TopToolBarArea, tool_bar)

        self._play_button = QPushButton("Play", self)
        self._play_button.clicked.connect(self._play_selected_macro)
        tool_bar.addWidget(self._play_button)

        self._record_button = QPushButton("Record", self)
        self._record_button.clicked.connect(self._start_quick_recording)
        tool_bar.addWidget(self._record_button)

        tool_bar.addSeparator()

        self._new_button = QPushButton("New", self)
        self._new_button.clicked.connect(self.create_macro)
        tool_bar.addWidget(self._new_button)

        self._edit_button = QPushButton("Edit", self)
        self._edit_button.clicked.connect(self.edit_selected_macro)
        tool_bar.addWidget(self._edit_button)

        self._duplicate_button = QPushButton("Duplicate", self)
        self._duplicate_button.clicked.connect(self.duplicate_selected_macro)
        tool_bar.addWidget(self._duplicate_button)

        self._delete_button = QPushButton("Delete", self)
        self._delete_button.clicked.connect(self.delete_selected_macro)
        tool_bar.addWidget(self._delete_button)

        tool_bar.addSeparator()

        self._favorite_button = QPushButton("Favorite", self)
        self._favorite_button.clicked.connect(self._toggle_selected_favorite)
        tool_bar.addWidget(self._favorite_button)

        self._refresh_button = QPushButton("Refresh", self)
        self._refresh_button.clicked.connect(self.refresh_macro_list)
        tool_bar.addWidget(self._refresh_button)

        tool_bar.addSeparator()

        self._settings_button = QPushButton("Settings", self)
        self._settings_button.clicked.connect(self.open_settings)
        tool_bar.addWidget(self._settings_button)

        self._hotkeys_button = QPushButton("Hotkeys", self)
        self._hotkeys_button.clicked.connect(self.open_hotkey_manager)
        tool_bar.addWidget(self._hotkeys_button)

    def _build_central_widget(self) -> None:
        central = QWidget(self)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(12, 12, 12, 12)

        self.macro_list_widget = MacroListWidget(self)
        self.macro_list_widget.macro_selected.connect(self._on_macro_selected)
        self.macro_list_widget.macro_activated.connect(self.play_macro)
        self.macro_list_widget.favorite_toggled.connect(self._handle_favorite_toggle)

        self._detail_panel = self._build_detail_panel()

        splitter = QSplitter(Qt.Horizontal, central)
        splitter.addWidget(self.macro_list_widget)
        splitter.addWidget(self._detail_panel)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 2)

        layout.addWidget(splitter)
        self.setCentralWidget(central)

    def _build_detail_panel(self) -> QWidget:
        panel = QFrame(self)
        panel.setFrameShape(QFrame.StyledPanel)
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(16, 16, 16, 16)

        self._detail_title = QLabel("Select a macro to view details", panel)
        self._detail_title.setObjectName("detailTitle")
        self._detail_title.setStyleSheet("font-size: 18px; font-weight: bold;")

        self._detail_summary = QLabel("", panel)
        self._detail_summary.setWordWrap(True)
        self._detail_tags = QLabel("", panel)
        self._detail_tags.setWordWrap(True)
        self._detail_statistics = QLabel("", panel)
        self._detail_statistics.setWordWrap(True)

        panel_layout.addWidget(self._detail_title)
        panel_layout.addSpacing(12)
        panel_layout.addWidget(self._detail_summary)
        panel_layout.addWidget(self._detail_tags)
        panel_layout.addWidget(self._detail_statistics)
        panel_layout.addStretch(1)

        return panel

    def _build_status_bar(self) -> None:
        status_bar = QStatusBar(self)
        self.setStatusBar(status_bar)
        self._status_label = QLabel("Ready", self)
        status_bar.addWidget(self._status_label)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def refresh_macro_list(self) -> None:
        macros = self.macro_service.list_macros()
        self.macro_list_widget.set_macros(macros)
        if macros:
            current = self.macro_list_widget.selected_macro_id
            macro_to_show: Optional[Macro]
            if current:
                macro_to_show = self.macro_service.get_macro(current)
            else:
                first = macros[0]
                self.macro_list_widget.select_macro(first.id)
                macro_to_show = first
            self._update_detail_panel(macro_to_show)
        else:
            self._update_detail_panel(None)
        self._update_action_states()
        self._status_label.setText(f"Loaded {len(macros)} macros")
        if self._hotkey_dialog is not None:
            self._hotkey_dialog.refresh_macros()

    def play_macro(self, macro_id: str) -> None:
        macro = self.macro_service.get_macro(macro_id)
        if not macro:
            self._status_label.setText("Macro not found")
            return

        def _on_step(step: PlaybackStep) -> None:
            if step.action.action_type in {
                ActionType.MOUSE_CLICK,
                ActionType.MOUSE_MOVE,
                ActionType.MOUSE_SCROLL,
            }:
                self.overlay.show_action(step.action)
            else:
                self.overlay.hide()

        self._status_label.setText(f"Playing {macro.name}")
        self.playback_service.play_macro(
            macro,
            playback_speed=macro.playback_speed,
            on_step=_on_step,
        )
        self.overlay.hide()
        self._status_label.setText(f"Finished playing {macro.name}")

    def attach_system_tray(self, tray: SystemTrayManager) -> None:
        self._system_tray = tray
        tray.bind_window(self)

    # ------------------------------------------------------------------
    # Action handlers
    # ------------------------------------------------------------------
    def create_macro(self) -> None:
        dialog = MacroEditorDialog(macro_service=self.macro_service, parent=self)
        dialog.prepare_new_macro()
        if dialog.exec() == QDialog.Accepted:
            created = dialog.current_macro
            if created:
                self.refresh_macro_list()
                self.macro_list_widget.select_macro(created.id)
                self._status_label.setText(f"Created macro {created.name}")

    def edit_selected_macro(self) -> None:
        macro_id = self.macro_list_widget.selected_macro_id
        if not macro_id:
            return
        macro = self.macro_service.get_macro(macro_id)
        if not macro:
            return
        dialog = MacroEditorDialog(macro_service=self.macro_service, parent=self)
        dialog.load_macro(macro)
        if dialog.exec() == QDialog.Accepted:
            updated = dialog.current_macro
            if updated:
                self.refresh_macro_list()
                self.macro_list_widget.select_macro(updated.id)
                self._status_label.setText(f"Updated macro {updated.name}")

    def duplicate_selected_macro(self) -> None:
        macro_id = self.macro_list_widget.selected_macro_id
        if not macro_id:
            return
        macro = self.macro_service.get_macro(macro_id)
        if not macro:
            return
        new_name = f"{macro.name} Copy"
        duplicate = self.macro_service.duplicate_macro(macro.id, new_name=new_name)
        self.refresh_macro_list()
        self.macro_list_widget.select_macro(duplicate.id)
        self._status_label.setText(f"Duplicated macro as {duplicate.name}")

    def delete_selected_macro(self, *, confirm: bool = True) -> None:
        macro_id = self.macro_list_widget.selected_macro_id
        if not macro_id:
            return
        macro = self.macro_service.get_macro(macro_id)
        if not macro:
            return
        if confirm:
            answer = QMessageBox.question(
                self,
                "Delete Macro",
                f"Are you sure you want to delete '{macro.name}'?",
            )
            if answer != QMessageBox.Yes:
                return
        self.macro_service.delete_macro(macro_id)
        self.refresh_macro_list()
        self._status_label.setText(f"Deleted macro {macro.name}")

    def open_settings(self) -> None:
        if self._settings_dialog is None:
            self._settings_dialog = SettingsDialog(
                settings=self.user_settings,
                on_apply=self._persist_settings,
                parent=self,
            )
        self._settings_dialog.show()
        self._settings_dialog.raise_()
        self._settings_dialog.activateWindow()

    def open_hotkey_manager(self) -> None:
        if self._hotkey_dialog is None:
            self._hotkey_dialog = HotkeyDialog(
                service=self.hotkey_service,
                macro_service=self.macro_service,
                parent=self,
            )
        self._hotkey_dialog.show()
        self._hotkey_dialog.raise_()
        self._hotkey_dialog.activateWindow()

    def _play_selected_macro(self) -> None:
        macro_id = self.macro_list_widget.selected_macro_id
        if macro_id:
            self.play_macro(macro_id)

    def _toggle_selected_favorite(self) -> None:
        macro_id = self.macro_list_widget.selected_macro_id
        if not macro_id:
            return
        macro = self.macro_service.get_macro(macro_id)
        if not macro:
            return
        new_state = not macro.is_favorite
        self.macro_service.mark_favorite(macro_id, new_state)
        self.macro_list_widget.update_favorite_state(macro_id, new_state)
        state = "added to" if new_state else "removed from"
        self._status_label.setText(f"{macro.name} {state} favorites")

    def _handle_favorite_toggle(self, macro_id: str, is_favorite: bool) -> None:
        self.macro_service.mark_favorite(macro_id, is_favorite)
        self.macro_list_widget.update_favorite_state(macro_id, is_favorite)
        macro = self.macro_service.get_macro(macro_id)
        if macro:
            state = "added to" if is_favorite else "removed from"
            self._status_label.setText(f"{macro.name} {state} favorites")

    def _start_quick_recording(self) -> None:  # pragma: no cover - requires recorder wiring
        self._status_label.setText("Recording started (simulated)")

    def _on_macro_selected(self, macro_id: str) -> None:
        macro = self.macro_service.get_macro(macro_id)
        self._update_detail_panel(macro)
        self._update_action_states()

    def _update_detail_panel(self, macro: Optional[Macro]) -> None:
        if macro is None:
            self._detail_title.setText("Select a macro to view details")
            self._detail_summary.setText("")
            self._detail_tags.setText("")
            self._detail_statistics.setText("")
            return

        self._detail_title.setText(macro.name)
        description = macro.description or "No description provided."
        self._detail_summary.setText(description)
        tags = ", ".join(macro.tags) if macro.tags else "No tags"
        self._detail_tags.setText(f"Tags: {tags}")
        stats = (
            f"Actions: {len(macro.actions)}\n"
            f"Duration: {macro.total_duration_ms:.0f} ms\n"
            f"Playback speed: {macro.playback_speed:.2f}x"
        )
        self._detail_statistics.setText(stats)

    def _update_action_states(self) -> None:
        has_selection = self.macro_list_widget.selected_macro_id is not None
        for widget in [
            self._play_button,
            self._edit_button,
            self._duplicate_button,
            self._delete_button,
            self._favorite_button,
            self._action_edit,
            self._action_duplicate,
            self._action_delete,
            self._action_toggle_favorite,
        ]:
            widget.setEnabled(has_selection)

    def _persist_settings(self, settings: UserSettings) -> None:
        if self._storage_manager is not None:
            self._storage_manager.save_settings(settings)
        self._status_label.setText("Settings saved")

    # ------------------------------------------------------------------
    # Qt event overrides
    # ------------------------------------------------------------------
    def closeEvent(self, event: QCloseEvent) -> None:  # pragma: no cover - requires GUI
        if self._system_tray is not None and getattr(self._system_tray, "is_available", False):
            self.hide()
            event.ignore()
        else:
            super().closeEvent(event)


__all__ = ["MainWindow"]
