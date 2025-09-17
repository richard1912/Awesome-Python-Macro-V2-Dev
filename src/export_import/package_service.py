from __future__ import annotations

import json
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

from src.models.macro import Macro
from src.storage.json_storage import JSONStorageManager
from src.utils import file_utils


@dataclass
class PackageInfo:
    macro_count: int


class PackageService:
    def __init__(self, *, storage_manager: JSONStorageManager) -> None:
        self.storage = storage_manager
        self.package_dir = self.storage.base_path / "packages"
        file_utils.ensure_directory(self.package_dir)

    def export_macros(self, macro_ids: Iterable[str], destination: Path | None = None) -> Path:
        macros: List[Macro] = []
        for macro_id in macro_ids:
            macro = self.storage.load_macro(macro_id)
            if macro:
                macros.append(macro)
        if destination is None:
            destination = self.package_dir / "macro-package.zip"
        file_utils.ensure_directory(destination.parent)
        with zipfile.ZipFile(destination, "w") as archive:
            for macro in macros:
                archive.writestr(f"macros/{macro.id}.json", json.dumps(macro.to_dict(), indent=2))
        return destination

    def import_package(self, package_path: Path) -> List[Macro]:
        imported: List[Macro] = []
        with zipfile.ZipFile(package_path, "r") as archive:
            for name in archive.namelist():
                if not name.startswith("macros/"):
                    continue
                payload = json.loads(archive.read(name).decode("utf-8"))
                macro = Macro.from_dict(payload)
                self.storage.save_macro(macro)
                imported.append(macro)
        return imported

    def inspect(self, package_path: Path) -> PackageInfo:
        with zipfile.ZipFile(package_path, "r") as archive:
            count = len([name for name in archive.namelist() if name.startswith("macros/")])
        return PackageInfo(macro_count=count)


__all__ = ["PackageService", "PackageInfo"]
