import time
from datetime import UTC, datetime

from backend.execution.runtime.clock import Clock


class SystemClock(Clock):
    """
    Production clock implementation.
    """

    def now(self) -> datetime:
        return datetime.now(UTC)

    def monotonic(self) -> float:
        return time.perf_counter()