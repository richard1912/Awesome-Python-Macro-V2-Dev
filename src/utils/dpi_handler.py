from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DPIHandler:
    scale_factor: float = 1.0

    def set_scale(self, factor: float) -> None:
        if factor <= 0:
            raise ValueError("DPI scale must be positive")
        self.scale_factor = factor

    def scale_point(self, x: int, y: int) -> tuple[int, int]:
        return int(x * self.scale_factor), int(y * self.scale_factor)

    def normalize_point(self, x: int, y: int) -> tuple[int, int]:
        return int(x / self.scale_factor), int(y / self.scale_factor)


__all__ = ["DPIHandler"]
