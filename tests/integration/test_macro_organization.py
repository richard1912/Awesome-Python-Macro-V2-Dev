from __future__ import annotations

from src.core.macro_service import MacroService
from src.storage.json_storage import JSONStorageManager


def test_macro_service_organizes_macros(tmp_path):
    storage = JSONStorageManager(base_path=tmp_path / "data")
    service = MacroService(storage_manager=storage)
    first = service.create_macro(name="Email", tags=["communication"])
    second = service.create_macro(name="Login", tags=["auth", "communication"])
    service.mark_favorite(second.id, True)

    organization = service.organize()

    assert set(organization["by_tag"]["communication"]) == {first.id, second.id}
    assert organization["favorites"][0].id == second.id
