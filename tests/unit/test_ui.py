from __future__ import annotations

from src.core.macro_service import MacroService
from src.hotkeys.hotkey_service import HotkeyService
from src.models.hotkey import Hotkey, HotkeyActionType
from src.models.user_settings import UserSettings
from src.player.playback_service import PlaybackService
from src.storage.json_storage import JSONStorageManager
from src.ui.hotkey_dialog import HotkeyDialog
from src.ui.main_window import MainWindow
from src.ui.macro_editor_dialog import MacroEditorDialog
from src.ui.settings_dialog import SettingsDialog
from src.utils.windows_api import WindowsAPIWrapper


def test_main_window_refreshes_macro_list(tmp_path, qapp):
    storage = JSONStorageManager(base_path=tmp_path / "data")
    macro_service = MacroService(storage_manager=storage)
    macro_service.create_macro(name="UI Macro")
    window = MainWindow(
        macro_service=macro_service,
        playback_service=PlaybackService(sleep=lambda _: None),
        hotkey_service=HotkeyService(windows_api=WindowsAPIWrapper()),
    )
    window.refresh_macro_list()
    assert window.macro_list_widget.count == 1


def test_macro_editor_updates_macro(tmp_path, qapp):
    storage = JSONStorageManager(base_path=tmp_path / "data")
    macro_service = MacroService(storage_manager=storage)
    macro = macro_service.create_macro(name="Editor Macro")
    editor = MacroEditorDialog(macro_service=macro_service)
    editor.load_macro(macro)
    editor.update_name("Updated Name")
    editor.apply_changes()
    assert macro_service.get_macro(macro.id).name == "Updated Name"


def test_settings_dialog_persists_values(qapp):
    settings = UserSettings()
    dialog = SettingsDialog(settings=settings)
    dialog.set_preference("ui.theme", "dark")
    dialog.apply()
    assert settings.get_value("ui.theme") == "dark"


def test_hotkey_dialog_registers_hotkeys(qapp):
    service = HotkeyService(windows_api=WindowsAPIWrapper())
    dialog = HotkeyDialog(service=service)
    dialog.assign_hotkey(
        Hotkey.create(
            key_combination="Ctrl+Shift+H",
            action_type=HotkeyActionType.SHOW_WINDOW,
            is_global=True,
        )
    )
    assert service.is_registered("Ctrl+Shift+H")
