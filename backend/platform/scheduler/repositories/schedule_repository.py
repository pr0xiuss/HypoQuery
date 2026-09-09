from abc import ABC, abstractmethod
from typing import Optional, List, Tuple
from uuid import UUID
from datetime import datetime

from backend.platform.scheduler.domain.schedule import Schedule


class ScheduleRepository(ABC):
    """
    Persistence contract for background schedules.
    """

    @abstractmethod
    def save(self, schedule: Schedule) -> Schedule:
        """
        Create or update a schedule.
        """

    @abstractmethod
    def get(self, schedule_id: UUID) -> Optional[Schedule]:
        """
        Retrieve a schedule by ID.
        """

    @abstractmethod
    def delete(self, schedule_id: UUID) -> None:
        """
        Delete a schedule by ID.
        """

    @abstractmethod
    def list_schedules(
        self, limit: int = 100, offset: int = 0
    ) -> Tuple[List[Schedule], int]:
        """
        List schedules with pagination.
        Returns (schedules, total_count).
        """

    @abstractmethod
    def get_due_schedules(self, now: datetime, batch_size: int = 50) -> List[Schedule]:
        """
        Fetch schedules that are enabled and due to run (next_run_at <= now).
        Implementations should use pessimistic locking (e.g. FOR UPDATE SKIP LOCKED)
        to prevent concurrent schedulers from claiming the same schedules.
        """
