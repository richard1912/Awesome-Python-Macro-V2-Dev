from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional
from uuid import uuid4

from src.models.action import Action


@dataclass
class Macro:
    id: str
    name: str
    description: str
    created_at: datetime
    modified_at: datetime
    version: int
    tags: List[str]
    is_favorite: bool
    playback_speed: float
    loop_count: int
    loop_interval: float
    actions: List[Action] = field(default_factory=list)

    @classmethod
    def create(
        cls,
        *,
        name: str,
        description: str = "",
        tags: Optional[Iterable[str]] = None,
        playback_speed: float = 1.0,
    ) -> "Macro":
        now = datetime.now(timezone.utc)
        return cls(
            id=str(uuid4()),
            name=name,
            description=description,
            created_at=now,
            modified_at=now,
            version=1,
            tags=list(tags or []),
            is_favorite=False,
            playback_speed=playback_speed,
            loop_count=1,
            loop_interval=0.0,
        )

    def add_action(self, action: Action) -> None:
        self.actions.append(action)
        self.touch()

    def touch(self) -> None:
        self.modified_at = datetime.now(timezone.utc)
        self.version += 1

    @property
    def total_duration_ms(self) -> float:
        if not self.actions:
            return 0.0
        return max(action.timestamp_ms for action in self.actions)

    def mark_favorite(self, is_favorite: bool) -> None:
        self.is_favorite = is_favorite
        self.touch()

    def update_metadata(
        self,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[Iterable[str]] = None,
        playback_speed: Optional[float] = None,
    ) -> None:
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if tags is not None:
            self.tags = list(tags)
        if playback_speed is not None:
            self.playback_speed = playback_speed
        self.touch()

    def duplicate(self, *, new_name: str) -> "Macro":
        clone = Macro.create(name=new_name, description=self.description, tags=self.tags)
        clone.playback_speed = self.playback_speed
        clone.loop_count = self.loop_count
        clone.loop_interval = self.loop_interval
        for action in self.actions:
            clone.add_action(action.clone(macro_id=clone.id))
        return clone

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "modified_at": self.modified_at.isoformat(),
            "version": self.version,
            "tags": self.tags,
            "is_favorite": self.is_favorite,
            "playback_speed": self.playback_speed,
            "loop_count": self.loop_count,
            "loop_interval": self.loop_interval,
            "actions": [action.to_dict() for action in self.actions],
        }

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "Macro":
        macro = cls(
            id=payload["id"],
            name=payload["name"],
            description=payload.get("description", ""),
            created_at=datetime.fromisoformat(payload["created_at"]),
            modified_at=datetime.fromisoformat(payload["modified_at"]),
            version=payload.get("version", 1),
            tags=list(payload.get("tags", [])),
            is_favorite=payload.get("is_favorite", False),
            playback_speed=float(payload.get("playback_speed", 1.0)),
            loop_count=int(payload.get("loop_count", 1)),
            loop_interval=float(payload.get("loop_interval", 0.0)),
        )
        for action_payload in payload.get("actions", []):
            macro.actions.append(Action.from_dict(action_payload))
        return macro


__all__ = ["Macro"]
