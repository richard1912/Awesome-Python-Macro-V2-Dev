from __future__ import annotations

from typing import Callable, Dict, List


EventPayload = Dict[str, object]
Callback = Callable[[EventPayload], None]


class InputCaptureManager:
    def __init__(self) -> None:
        self._callbacks: List[Callback] = []
        self._active = False

    def start(self, callback: Callback) -> None:
        self._callbacks.append(callback)
        self._active = True

    def stop(self, callback: Callback) -> None:
        if callback in self._callbacks:
            self._callbacks.remove(callback)
        if not self._callbacks:
            self._active = False

    def emit(self, event: EventPayload) -> None:
        if not self._active:
            return
        for callback in list(self._callbacks):
            callback(event)

    @property
    def is_active(self) -> bool:
        return self._active


__all__ = ["InputCaptureManager", "EventPayload", "Callback"]
