from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from backend.platform.scheduler.domain.job import JobType


@dataclass(frozen=True, slots=True)
class Schedule:
    """
    Domain entity representing a recurring scheduled workload.
    """

    schedule_id: UUID
    name: str
    job_type: JobType
    payload: dict
    interval_seconds: int
    is_enabled: bool
    next_run_at: datetime
    last_run_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def with_next_run(self, next_run_at: datetime, last_run_at: datetime) -> "Schedule":
        """
        Returns a new Schedule instance with advanced run times.
        """
        return Schedule(
            schedule_id=self.schedule_id,
            name=self.name,
            job_type=self.job_type,
            payload=self.payload,
            interval_seconds=self.interval_seconds,
            is_enabled=self.is_enabled,
            next_run_at=next_run_at,
            last_run_at=last_run_at,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def with_status(self, is_enabled: bool) -> "Schedule":
        """
        Returns a new Schedule instance with the updated enabled status.
        """
        return Schedule(
            schedule_id=self.schedule_id,
            name=self.name,
            job_type=self.job_type,
            payload=self.payload,
            interval_seconds=self.interval_seconds,
            is_enabled=is_enabled,
            next_run_at=self.next_run_at,
            last_run_at=self.last_run_at,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
