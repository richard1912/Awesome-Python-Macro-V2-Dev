from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Optional


@dataclass
class CapturedException:
    exception: Exception
    context: Optional[str] = None


class ErrorHandler:
    def __init__(self) -> None:
        self._listeners: List[Callable[[CapturedException], None]] = []

    def add_listener(self, listener: Callable[[CapturedException], None]) -> None:
        self._listeners.append(listener)

    def capture(self, func: Callable[[], None], *, context: Optional[str] = None) -> None:
        try:
            func()
        except Exception as exc:  # pragma: no cover - trivial branch
            captured = CapturedException(exception=exc, context=context)
            for listener in list(self._listeners):
                listener(captured)


__all__ = ["ErrorHandler", "CapturedException"]
