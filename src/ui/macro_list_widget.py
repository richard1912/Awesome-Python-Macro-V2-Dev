from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional

from PySide6.QtCore import QEvent, Qt, Signal
from PySide6.QtWidgets import (
    QAbstractItemView,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMenu,
    QPushButton,
    QStyle,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from src.models.macro import Macro


@dataclass
class MacroListItem:
    id: str
    name: str
    is_favorite: bool


class MacroListWidget(QWidget):
    """Interactive macro list with filtering and favorite controls."""

    macro_selected = Signal(str)
    macro_activated = Signal(str)
    favorite_toggled = Signal(str, bool)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._items: Dict[str, MacroListItem] = {}
        self._ordered_ids: List[str] = []

        self._search_input = QLineEdit(self)
        self._search_input.setPlaceholderText("Search macros…")
        self._search_input.textChanged.connect(self._refresh_visible_items)

        self._favorites_only_button = QToolButton(self)
        self._favorites_only_button.setCheckable(True)
        self._favorites_only_button.setToolTip("Show only favorite macros")
        self._favorites_only_button.setText("★")
        self._favorites_only_button.setStyleSheet("font-size: 16px;")
        self._favorites_only_button.toggled.connect(self._refresh_visible_items)

        self._clear_search_button = QPushButton(self)
        self._clear_search_button.setText("Clear")
        self._clear_search_button.setToolTip("Clear search text")
        self._clear_search_button.clicked.connect(self.clear_search)

        search_bar = QHBoxLayout()
        search_bar.addWidget(QLabel("Filter:", self))
        search_bar.addWidget(self._search_input)
        search_bar.addWidget(self._favorites_only_button)
        search_bar.addWidget(self._clear_search_button)

        self._list_widget = QListWidget(self)
        self._list_widget.setObjectName("macroList")
        self._list_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        self._list_widget.itemSelectionChanged.connect(self._handle_selection_change)
        self._list_widget.itemActivated.connect(self._handle_item_activated)
        self._list_widget.setAlternatingRowColors(True)

        self._empty_state = QFrame(self)
        empty_layout = QVBoxLayout(self._empty_state)
        empty_layout.setContentsMargins(0, 24, 0, 24)
        empty_label = QLabel("No macros available yet.", self._empty_state)
        empty_label.setAlignment(Qt.AlignCenter)
        empty_hint = QLabel("Create a macro to get started.", self._empty_state)
        empty_hint.setAlignment(Qt.AlignCenter)
        empty_layout.addWidget(empty_label)
        empty_layout.addWidget(empty_hint)
        self._empty_state.hide()

        container = QVBoxLayout(self)
        container.addLayout(search_bar)
        container.addWidget(self._list_widget)
        container.addWidget(self._empty_state)
        container.setStretch(1, 1)

        self._list_widget.viewport().installEventFilter(self)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def set_macros(self, macros: Iterable[Macro]) -> None:
        """Populate the widget with macros sorted by name."""
        items = [
            MacroListItem(id=macro.id, name=macro.name, is_favorite=macro.is_favorite)
            for macro in macros
        ]
        items.sort(key=lambda item: item.name.lower())
        self._items = {item.id: item for item in items}
        self._refresh_visible_items()

    @property
    def items(self) -> List[MacroListItem]:
        return [self._items[item_id] for item_id in self._ordered_ids]

    @property
    def count(self) -> int:
        return len(self._ordered_ids)

    @property
    def selected_macro_id(self) -> Optional[str]:
        current = self._list_widget.currentItem()
        if current is None:
            return None
        return str(current.data(Qt.UserRole))

    def select_macro(self, macro_id: str) -> None:
        for index in range(self._list_widget.count()):
            item = self._list_widget.item(index)
            if item.data(Qt.UserRole) == macro_id:
                self._list_widget.setCurrentItem(item)
                return

    def clear_selection(self) -> None:
        self._list_widget.clearSelection()

    def clear_search(self) -> None:
        self._search_input.clear()

    def set_search_text(self, text: str) -> None:
        self._search_input.setText(text)

    def update_favorite_state(self, macro_id: str, is_favorite: bool) -> None:
        if macro_id not in self._items:
            return
        self._items[macro_id].is_favorite = is_favorite
        self._refresh_visible_items(preserve_selection=True)

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------
    def _handle_selection_change(self) -> None:
        macro_id = self.selected_macro_id
        if macro_id:
            self.macro_selected.emit(macro_id)

    def _handle_item_activated(self, item: QListWidgetItem) -> None:
        macro_id = str(item.data(Qt.UserRole))
        self.macro_activated.emit(macro_id)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _refresh_visible_items(self, preserve_selection: bool = False) -> None:
        previously_selected = self.selected_macro_id if preserve_selection else None
        filter_text = self._search_input.text().strip().lower()
        favorites_only = self._favorites_only_button.isChecked()

        self._list_widget.blockSignals(True)
        self._list_widget.clear()
        self._ordered_ids = []

        favorite_icon = self.style().standardIcon(QStyle.SP_DialogYesButton)
        for item in self._items.values():
            searchable = item.name.lower()
            if filter_text and filter_text not in searchable:
                continue
            if favorites_only and not item.is_favorite:
                continue
            list_item = QListWidgetItem(self._format_label(item))
            list_item.setData(Qt.UserRole, item.id)
            list_item.setData(Qt.UserRole + 1, item.is_favorite)
            if item.is_favorite:
                list_item.setIcon(favorite_icon)
            self._list_widget.addItem(list_item)
            self._ordered_ids.append(item.id)

        self._list_widget.blockSignals(False)

        has_items = self._list_widget.count() > 0
        self._list_widget.setVisible(has_items)
        self._empty_state.setVisible(not has_items)

        if previously_selected:
            self.select_macro(previously_selected)

    def _format_label(self, item: MacroListItem) -> str:
        prefix = "★ " if item.is_favorite else "  "
        return f"{prefix}{item.name}"

    def eventFilter(self, watched, event):  # type: ignore[override]
        if watched is self._list_widget.viewport() and event.type() == QEvent.ContextMenu:
            item = self._list_widget.itemAt(event.pos())
            if item is not None:
                macro_id = str(item.data(Qt.UserRole))
                is_favorite = bool(item.data(Qt.UserRole + 1))
                menu = QMenu(self)
                label = "Remove from favorites" if is_favorite else "Add to favorites"
                toggle_action = menu.addAction(label)
                chosen = menu.exec(event.globalPos())  # type: ignore[attr-defined]
                if chosen is toggle_action:
                    self.favorite_toggled.emit(macro_id, not is_favorite)
            event.accept()
            return True
        return super().eventFilter(watched, event)


__all__ = ["MacroListWidget", "MacroListItem"]
