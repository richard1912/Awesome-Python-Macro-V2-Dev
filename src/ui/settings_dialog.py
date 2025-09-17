from __future__ import annotations

from typing import Callable, Dict, Optional

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.models.user_settings import UserSettings


class SettingsDialog(QDialog):
    """Editable view of persisted user preferences."""

    def __init__(
        self,
        *,
        settings: UserSettings,
        on_apply: Optional[Callable[[UserSettings], None]] = None,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("Application Settings")
        self.resize(420, 400)

        self.settings = settings
        self._on_apply = on_apply
        self._pending: Dict[str, object] = {}
        self._fields: Dict[str, QLineEdit] = {}

        layout = QVBoxLayout(self)

        self._form_layout = QFormLayout()
        self._form_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)

        form_container = QWidget(self)
        form_container.setLayout(self._form_layout)
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setWidget(form_container)
        layout.addWidget(scroll)

        self._new_key_input = QLineEdit(self)
        self._new_key_input.setPlaceholderText("Preference key")
        self._new_value_input = QLineEdit(self)
        self._new_value_input.setPlaceholderText("Value")
        add_button = QPushButton("Add", self)
        add_button.clicked.connect(self._handle_add_preference)

        add_row = QHBoxLayout()
        add_row.addWidget(self._new_key_input)
        add_row.addWidget(self._new_value_input)
        add_row.addWidget(add_button)
        layout.addLayout(add_row)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.apply)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self._load_from_settings()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def set_preference(self, key: str, value: object) -> None:
        field = self._fields.get(key)
        if field is None:
            field = self._create_field(key, value)
        field.setText(self._stringify(value))
        self._pending[key] = value

    def apply(self) -> None:
        if not self._pending:
            self.accept()
            return
        for key, value in self._pending.items():
            self.settings.set_value(key, value)
        self._pending.clear()
        if self._on_apply:
            self._on_apply(self.settings)
        self.accept()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _load_from_settings(self) -> None:
        for key, value in sorted(self.settings.values.items()):
            self._create_field(key, value)

    def _create_field(self, key: str, value: object) -> QLineEdit:
        field = QLineEdit(self)
        field.setText(self._stringify(value))
        field.editingFinished.connect(lambda key=key, field=field: self._queue_value(key, field.text()))
        label = QLabel(key, self)
        self._form_layout.addRow(label, field)
        self._fields[key] = field
        return field

    def _handle_add_preference(self) -> None:
        key = self._new_key_input.text().strip()
        if not key:
            QMessageBox.warning(self, "Validation", "Preference key is required")
            return
        value = self._new_value_input.text().strip()
        if key in self._fields:
            QMessageBox.warning(self, "Validation", "Preference already exists")
            return
        self._create_field(key, value)
        self._pending[key] = value
        self._new_key_input.clear()
        self._new_value_input.clear()

    def _queue_value(self, key: str, raw_value: str) -> None:
        self._pending[key] = self._coerce(raw_value)

    def _stringify(self, value: object) -> str:
        if isinstance(value, bool):
            return "true" if value else "false"
        return str(value)

    def _coerce(self, raw_value: str) -> object:
        lowered = raw_value.strip().lower()
        if lowered in {"true", "false"}:
            return lowered == "true"
        try:
            return int(raw_value)
        except ValueError:
            pass
        try:
            return float(raw_value)
        except ValueError:
            pass
        return raw_value


__all__ = ["SettingsDialog"]
