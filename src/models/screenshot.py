from __future__ import annotations

import base64
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from uuid import uuid4


@dataclass
class Screenshot:
    id: str
    macro_id: str
    action_id: str
    image_data: str
    image_format: str
    width: int
    height: int
    dpi: int
    captured_at: datetime
    file_path: Optional[str] = None

    @classmethod
    def create_placeholder(
        cls,
        macro_id: str,
        action_id: str,
        *,
        width: int = 1,
        height: int = 1,
        dpi: int = 96,
        captured_at: Optional[datetime] = None,
    ) -> "Screenshot":
        captured_at = captured_at or datetime.now(timezone.utc)
        payload = f"{macro_id}:{action_id}:{int(captured_at.timestamp())}"
        image_data = base64.b64encode(payload.encode("utf-8")).decode("ascii")
        return cls(
            id=str(uuid4()),
            macro_id=macro_id,
            action_id=action_id,
            image_data=image_data,
            image_format="png",
            width=width,
            height=height,
            dpi=dpi,
            captured_at=captured_at,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "macro_id": self.macro_id,
            "action_id": self.action_id,
            "image_data": self.image_data,
            "image_format": self.image_format,
            "width": self.width,
            "height": self.height,
            "dpi": self.dpi,
            "captured_at": self.captured_at.isoformat(),
            "file_path": self.file_path,
        }

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "Screenshot":
        return cls(
            id=payload["id"],
            macro_id=payload["macro_id"],
            action_id=payload["action_id"],
            image_data=payload["image_data"],
            image_format=payload.get("image_format", "png"),
            width=payload.get("width", 1),
            height=payload.get("height", 1),
            dpi=payload.get("dpi", 96),
            captured_at=datetime.fromisoformat(payload["captured_at"]),
            file_path=payload.get("file_path"),
        )


__all__ = ["Screenshot"]
