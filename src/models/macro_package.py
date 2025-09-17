from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List
from uuid import uuid4

from src.models.macro import Macro


@dataclass
class MacroPackage:
    id: str
    name: str
    created_at: datetime
    macros: List[Macro] = field(default_factory=list)
    description: str = ""

    @classmethod
    def create(
        cls, *, name: str, macros: Iterable[Macro], description: str = ""
    ) -> "MacroPackage":
        return cls(
            id=str(uuid4()),
            name=name,
            created_at=datetime.now(timezone.utc),
            macros=list(macros),
            description=description,
        )

    def contains_macro(self, macro_id: str) -> bool:
        return any(macro.id == macro_id for macro in self.macros)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "description": self.description,
            "macros": [macro.to_dict() for macro in self.macros],
        }

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "MacroPackage":
        return cls(
            id=payload["id"],
            name=payload["name"],
            created_at=datetime.fromisoformat(payload["created_at"]),
            macros=[Macro.from_dict(data) for data in payload.get("macros", [])],
            description=payload.get("description", ""),
        )


__all__ = ["MacroPackage"]
