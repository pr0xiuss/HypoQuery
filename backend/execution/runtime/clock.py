from abc import ABC, abstractmethod
from datetime import datetime


class Clock(ABC):
    """
    Provides access to wall-clock and monotonic time.
    """

    @abstractmethod
    def now(self) -> datetime:
        pass

    @abstractmethod
    def monotonic(self) -> float:
        pass