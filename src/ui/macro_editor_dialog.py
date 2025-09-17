from __future__ import annotations

from typing import Iterable, Optional
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QTextEdit,
    QVBoxLayout,
)

from src.core.macro_service import MacroService
from src.models.macro import Macro


class MacroEditorDialog(QDialog):
    """Dialog for editing macro metadata and playback settings."""

    def __init__(self, *, macro_service: MacroService, parent=None) -> None:
        super().__init__(parent)
        self.setModal(True)
        self.setWindowTitle("Macro Editor")
        self.resize(480, 360)

        self.macro_service = macro_service
        self._macro: Optional[Macro] = None

        self._name_input = QLineEdit(self)
        self._description_input = QTextEdit(self)
        self._description_input.setAcceptRichText(False)
        self._description_input.setPlaceholderText("Describe what this macro does…")
        self._description_input.setTabChangesFocus(True)
        self._tags_input = QLineEdit(self)
        self._tags_input.setPlaceholderText("Comma separated tags")
        self._speed_input = QDoubleSpinBox(self)
        self._speed_input.setRange(0.1, 5.0)
        self._speed_input.setSingleStep(0.1)
        self._speed_input.setValue(1.0)

        form = QFormLayout()
        form.addRow("Name", self._name_input)
        form.addRow("Description", self._description_input)
        form.addRow("Tags", self._tags_input)
        form.addRow("Playback speed", self._speed_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.apply_changes)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(buttons)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    @property
    def current_macro(self) -> Optional[Macro]:
        return self._macro

    def load_macro(self, macro: Macro) -> None:
        self._macro = macro
        self._populate_fields(macro)

    def prepare_new_macro(self, suggested_name: str = "New Macro") -> None:
        name = suggested_name
        counter = 1
        while self.macro_service.is_name_taken(name):
            name = f"{suggested_name} {counter}"
            counter += 1
        self._macro = None
        self._name_input.setText(name)
        self._description_input.clear()
        self._tags_input.clear()
        self._speed_input.setValue(1.0)

    def update_name(self, name: str) -> None:
        self._name_input.setText(name)

    def update_tags(self, tags: Iterable[str]) -> None:
        self._tags_input.setText(", ".join(tag.strip() for tag in tags))

    def update_description(self, description: str) -> None:
        self._description_input.setPlainText(description)

    def update_playback_speed(self, speed: float) -> None:
        self._speed_input.setValue(speed)

    def apply_changes(self) -> None:
        name = self._name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Validation", "Macro name is required")
            return

        description = self._description_input.toPlainText().strip()
        tags = [tag.strip() for tag in self._tags_input.text().split(",") if tag.strip()]
        playback_speed = float(self._speed_input.value())

        if self._macro is None:
            self._macro = self.macro_service.create_macro(
                name=name,
                description=description,
                tags=tags,
                playback_speed=playback_speed,
            )
        else:
            self._macro = self.macro_service.update_macro_metadata(
                self._macro.id,
                name=name,
                description=description,
                tags=tags,
                playback_speed=playback_speed,
            )
        self.accept()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _populate_fields(self, macro: Macro) -> None:
        self._name_input.setText(macro.name)
        self._description_input.setPlainText(macro.description)
        self._tags_input.setText(", ".join(macro.tags))
        self._speed_input.setValue(macro.playback_speed or 1.0)


__all__ = ["MacroEditorDialog"]
