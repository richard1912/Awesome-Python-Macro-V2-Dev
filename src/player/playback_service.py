from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable, Iterable, Iterator, Optional

from src.models.action import Action, ActionType
from src.models.macro import Macro


@dataclass
class PlaybackStep:
    action: Action
    delay_seconds: float
    playback_speed: float
    sequence_index: int


class PlaybackService:
    def __init__(self, *, sleep: Optional[Callable[[float], None]] = None) -> None:
        self._sleep = sleep or time.sleep

    def iter_steps(self, macro: Macro, playback_speed: float = 1.0) -> Iterator[PlaybackStep]:
        last_timestamp = 0.0
        for index, action in enumerate(sorted(macro.actions, key=lambda item: item.timestamp_ms)):
            if action.action_type is ActionType.DELAY and action.delay_duration is not None:
                delay_seconds = 0.0 if index == 0 else action.delay_duration / 1000.0
                last_timestamp = action.timestamp_ms
                yield PlaybackStep(
                    action=action,
                    delay_seconds=delay_seconds,
                    playback_speed=playback_speed,
                    sequence_index=index,
                )
                continue
            raw_delay = max(action.timestamp_ms - last_timestamp, 0.0)
            delay_seconds = (raw_delay / 1000.0) / max(playback_speed, 0.001)
            last_timestamp = action.timestamp_ms
            yield PlaybackStep(
                action=action,
                delay_seconds=delay_seconds,
                playback_speed=playback_speed,
                sequence_index=index,
            )

    def play_macro(
        self,
        macro: Macro,
        *,
        playback_speed: float = 1.0,
        loop_count: int = 1,
        on_step: Optional[Callable[[PlaybackStep], None]] = None,
    ) -> None:
        if loop_count <= 0:
            loop_count = 1
        steps = list(self.iter_steps(macro, playback_speed=playback_speed))
        total = len(steps)
        for loop_index in range(loop_count):
            for base_index, step in enumerate(steps):
                sequence_index = loop_index * total + base_index
                current_step = PlaybackStep(
                    action=step.action,
                    delay_seconds=step.delay_seconds,
                    playback_speed=step.playback_speed,
                    sequence_index=sequence_index,
                )
                if on_step:
                    on_step(current_step)
                self._sleep(step.delay_seconds)


__all__ = ["PlaybackService", "PlaybackStep"]
