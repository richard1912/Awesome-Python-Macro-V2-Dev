from __future__ import annotations

from pathlib import Path

from src.core.macro_service import MacroService
from src.export_import.package_service import PackageService
from src.models.action import Action
from src.storage.json_storage import JSONStorageManager


def test_export_import_roundtrip(tmp_path):
    storage = JSONStorageManager(base_path=tmp_path / "data")
    service = MacroService(storage_manager=storage)
    package_service = PackageService(storage_manager=storage)
    macro = service.create_macro(name="Exported", tags=["share"])
    service.add_action(
        macro.id,
        Action.keyboard_event(
            macro_id=macro.id,
            key_name="x",
            key_code="KeyX",
            is_press=True,
            timestamp_ms=0,
        ),
    )

    package_path = package_service.export_macros([macro.id], destination=tmp_path / "pkg.zip")
    service.delete_macro(macro.id)
    assert service.get_macro(macro.id) is None

    imported = package_service.import_package(package_path)
    assert any(item.name == "Exported" for item in imported)
    assert service.get_macro(imported[0].id) is not None
    assert package_path.exists()
