from datetime import datetime, timedelta

from backend.execution.runtime.clock import Clock
from backend.platform.scheduler.domain.schedule import Schedule


class ScheduleCalculator:
    """
    Calculates the next run time for a Schedule based on its interval.
    """

    def __init__(self, clock: Clock):
        self._clock = clock

    def calculate_next_run(self, schedule: Schedule) -> datetime:
        """
        Calculates the next run time from the current clock time.
        Using current clock time instead of last_run_at prevents rapid back-to-back 
        executions if the scheduler falls behind.
        """
        now = self._clock.now()
        
        # Ensure minimum interval protection
        interval = max(schedule.interval_seconds, 1)
        return now + timedelta(seconds=interval)
