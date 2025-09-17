from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


class SettingValueError(KeyError):
    pass


@dataclass
class UserSettings:
    values: Dict[str, Any] = field(default_factory=dict)

    def set_value(self, key: str, value: Any) -> None:
        self.values[key] = value

    def get_value(self, key: str, default: Any | None = None) -> Any:
        return self.values.get(key, default)

    def require(self, key: str) -> Any:
        if key not in self.values:
            raise SettingValueError(f"Missing setting: {key}")
        return self.values[key]

    def to_dict(self) -> Dict[str, Any]:
        return dict(self.values)

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "UserSettings":
        return cls(values=dict(payload))


__all__ = ["UserSettings", "SettingValueError"]
