from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
from uuid import uuid4


@dataclass
class Schedule:
    id: str
    macro_id: str
    name: str
    is_enabled: bool
    start_time: datetime
    end_time: Optional[datetime]
    recurrence_type: str
    recurrence_pattern: Dict[str, Any]
    next_run: Optional[datetime]

    @classmethod
    def create(
        cls,
        *,
        macro_id: str,
        name: str,
        start_time: datetime,
        recurrence_type: str,
        recurrence_pattern: Optional[Dict[str, Any]] = None,
        end_time: Optional[datetime] = None,
    ) -> "Schedule":
        return cls(
            id=str(uuid4()),
            macro_id=macro_id,
            name=name,
            is_enabled=True,
            start_time=start_time,
            end_time=end_time,
            recurrence_type=recurrence_type,
            recurrence_pattern=recurrence_pattern or {},
            next_run=start_time,
        )

    def advance(self) -> None:
        if self.recurrence_type == "once":
            self.is_enabled = False
            self.next_run = None
        elif self.recurrence_type == "daily":
            self.next_run = (self.next_run or self.start_time) + timedelta(days=1)
        elif self.recurrence_type == "hourly":
            self.next_run = (self.next_run or self.start_time) + timedelta(hours=1)
        else:
            self.next_run = (self.next_run or self.start_time) + timedelta(minutes=30)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "macro_id": self.macro_id,
            "name": self.name,
            "is_enabled": self.is_enabled,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "recurrence_type": self.recurrence_type,
            "recurrence_pattern": self.recurrence_pattern,
            "next_run": self.next_run.isoformat() if self.next_run else None,
        }

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "Schedule":
        start_time = datetime.fromisoformat(payload["start_time"])
        end_time = (
            datetime.fromisoformat(payload["end_time"]) if payload.get("end_time") else None
        )
        next_run = (
            datetime.fromisoformat(payload["next_run"]) if payload.get("next_run") else None
        )
        return cls(
            id=payload["id"],
            macro_id=payload["macro_id"],
            name=payload["name"],
            is_enabled=payload.get("is_enabled", True),
            start_time=start_time,
            end_time=end_time,
            recurrence_type=payload.get("recurrence_type", "once"),
            recurrence_pattern=payload.get("recurrence_pattern", {}),
            next_run=next_run,
        )


__all__ = ["Schedule"]
