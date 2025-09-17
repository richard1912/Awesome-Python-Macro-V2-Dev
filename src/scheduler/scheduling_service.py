from __future__ import annotations

from datetime import datetime, timezone
from typing import Callable, Dict, Optional

from src.core.macro_service import MacroService
from src.models.schedule import Schedule
from src.player.playback_service import PlaybackService


class SchedulingService:
    def __init__(
        self,
        *,
        macro_service: MacroService,
        playback_service: PlaybackService,
        time_provider: Callable[[], datetime] | None = None,
    ) -> None:
        self.macro_service = macro_service
        self.playback_service = playback_service
        self.time_provider = time_provider or (lambda: datetime.now(timezone.utc))
        self._schedules: Dict[str, Schedule] = {}

    def create_schedule(
        self,
        *,
        macro_id: str,
        name: str,
        start_time: datetime,
        recurrence_type: str,
    ) -> Schedule:
        schedule = Schedule.create(
            macro_id=macro_id,
            name=name,
            start_time=start_time,
            recurrence_type=recurrence_type,
        )
        self._schedules[schedule.id] = schedule
        return schedule

    def get_schedule(self, schedule_id: str) -> Optional[Schedule]:
        return self._schedules.get(schedule_id)

    def toggle(self, schedule_id: str, *, enabled: bool) -> None:
        schedule = self.get_schedule(schedule_id)
        if schedule:
            schedule.is_enabled = enabled

    def run_pending(self) -> None:
        now = self.time_provider()
        for schedule in list(self._schedules.values()):
            if not schedule.is_enabled:
                continue
            if schedule.next_run and schedule.next_run <= now:
                macro = self.macro_service.get_macro(schedule.macro_id)
                if macro:
                    self.playback_service.play_macro(macro)
                schedule.advance()


__all__ = ["SchedulingService"]
