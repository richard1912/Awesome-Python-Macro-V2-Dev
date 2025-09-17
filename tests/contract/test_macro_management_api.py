from __future__ import annotations

from src.core.macro_service import MacroService
from src.models.action import Action


def test_macro_management_crud_and_search(storage_manager):
    service = MacroService(storage_manager=storage_manager)
    macro = service.create_macro(name="Login", description="Demo", tags=["auth"])
    service.mark_favorite(macro.id, True)
    service.add_action(
        macro.id,
        Action.keyboard_event(
            macro_id=macro.id,
            key_name="l",
            key_code="KeyL",
            is_press=True,
            timestamp_ms=0,
        ),
    )
    duplicate = service.duplicate_macro(macro.id, new_name="Login Copy")

    assert duplicate.name == "Login Copy"
    assert duplicate.id != macro.id
    assert service.get_macro(duplicate.id) is not None

    results = service.search_macros("login")
    assert {item.id for item in results} == {macro.id, duplicate.id}

    service.delete_macro(macro.id)
    assert service.get_macro(macro.id) is None


def test_macro_management_validates_uniqueness(storage_manager):
    service = MacroService(storage_manager=storage_manager)
    service.create_macro(name="Unique Name")

    assert service.is_name_taken("Unique Name")
    assert not service.is_name_taken("Another")
