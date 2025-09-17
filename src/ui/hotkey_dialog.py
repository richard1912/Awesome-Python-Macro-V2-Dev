from __future__ import annotations

from typing import Dict, Optional

from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from src.core.macro_service import MacroService
from src.hotkeys.hotkey_service import HotkeyService
from src.models.hotkey import Hotkey, HotkeyActionType
from src.utils.validation import ValidationError


class HotkeyDialog(QDialog):
    """Manage registration of global and application hotkeys."""

    def __init__(
        self,
        *,
        service: HotkeyService,
        macro_service: Optional[MacroService] = None,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("Hotkey Manager")
        self.resize(560, 420)

        self.service = service
        self.macro_service = macro_service
        self._assigned: Dict[str, Hotkey] = {}

        layout = QVBoxLayout(self)

        self._table = QTableWidget(0, 4, self)
        self._table.setHorizontalHeaderLabels(["Key", "Action", "Macro", "Scope"])
        self._table.horizontalHeader().setStretchLastSection(True)
        self._table.verticalHeader().setVisible(False)
        layout.addWidget(self._table)

        form_layout = QFormLayout()
        self._key_input = QLineEdit(self)
        self._key_input.setPlaceholderText("Ctrl+Shift+M")
        self._action_combo = QComboBox(self)
        for action in HotkeyActionType:
            self._action_combo.addItem(action.name.replace("_", " ").title(), action)
        self._action_combo.currentIndexChanged.connect(self._update_macro_combo_state)

        self._macro_combo = QComboBox(self)
        self._macro_combo.addItem("-- None --", None)

        self._global_checkbox = QCheckBox("Global hotkey", self)
        self._global_checkbox.setChecked(True)

        form_layout.addRow("Key combination", self._key_input)
        form_layout.addRow("Action", self._action_combo)
        form_layout.addRow("Macro", self._macro_combo)
        form_layout.addRow("Scope", self._global_checkbox)

        layout.addLayout(form_layout)

        buttons_row = QHBoxLayout()
        self._register_button = QPushButton("Register", self)
        self._register_button.clicked.connect(self._register_from_inputs)
        self._remove_button = QPushButton("Remove Selected", self)
        self._remove_button.clicked.connect(self._remove_selected)
        buttons_row.addWidget(self._register_button)
        buttons_row.addWidget(self._remove_button)
        layout.addLayout(buttons_row)

        close_buttons = QDialogButtonBox(QDialogButtonBox.Close, self)
        close_buttons.rejected.connect(self.reject)
        close_buttons.accepted.connect(self.accept)
        layout.addWidget(close_buttons)

        self.refresh_macros()
        self._update_macro_combo_state()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def refresh_macros(self) -> None:
        current = self._macro_combo.currentData()
        self._macro_combo.blockSignals(True)
        self._macro_combo.clear()
        self._macro_combo.addItem("-- None --", None)
        if self.macro_service is not None:
            for macro in self.macro_service.list_macros():
                self._macro_combo.addItem(macro.name, macro.id)
        index = self._macro_combo.findData(current)
        if index >= 0:
            self._macro_combo.setCurrentIndex(index)
        self._macro_combo.blockSignals(False)

    def assign_hotkey(self, hotkey: Hotkey) -> None:
        self.service.register(hotkey)
        self._assigned[hotkey.key_combination] = hotkey
        self._update_table()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _register_from_inputs(self) -> None:
        key = self._key_input.text().strip()
        if not key:
            QMessageBox.warning(self, "Validation", "Key combination is required")
            return
        action = self._current_action()
        if action is None:
            QMessageBox.warning(self, "Validation", "Select an action for this hotkey")
            return
        macro_id = self._macro_combo.currentData()
        if action.requires_macro and not macro_id:
            QMessageBox.warning(self, "Validation", "Select a macro for this hotkey")
            return
        try:
            hotkey = Hotkey.create(
                key_combination=key,
                action_type=action,
                macro_id=macro_id,
                is_global=self._global_checkbox.isChecked(),
            )
            self.assign_hotkey(hotkey)
        except ValidationError as exc:
            QMessageBox.warning(self, "Registration failed", str(exc))
            return
        self._key_input.clear()

    def _remove_selected(self) -> None:
        row = self._table.currentRow()
        if row < 0:
            return
        key_item = self._table.item(row, 0)
        if key_item is None:
            return
        key = key_item.text()
        self.service.unregister(key)
        self._assigned.pop(key, None)
        self._update_table()

    def _update_macro_combo_state(self) -> None:
        action = self._current_action()
        needs_macro = action.requires_macro if action else False
        self._macro_combo.setEnabled(needs_macro)

    def _update_table(self) -> None:
        self._table.setRowCount(len(self._assigned))
        for row, hotkey in enumerate(self._assigned.values()):
            self._table.setItem(row, 0, QTableWidgetItem(hotkey.key_combination))
            self._table.setItem(row, 1, QTableWidgetItem(hotkey.action_type.name))
            macro_label = hotkey.macro_id or "-"
            self._table.setItem(row, 2, QTableWidgetItem(macro_label))
            scope = "Global" if hotkey.is_global else "Application"
            self._table.setItem(row, 3, QTableWidgetItem(scope))

    def _current_action(self) -> Optional[HotkeyActionType]:
        data = self._action_combo.currentData()
        if data is None:
            return None
        if isinstance(data, HotkeyActionType):
            return data
        try:
            return HotkeyActionType(str(data))
        except ValueError:
            return None


__all__ = ["HotkeyDialog"]
