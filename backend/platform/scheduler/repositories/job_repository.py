from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional, Tuple
from uuid import UUID

from backend.platform.scheduler.domain.job import Job


class JobRepository(ABC):
    """
    Contract for durable storage of application-level background jobs.
    """

    @abstractmethod
    def save(self, job: Job) -> Job:
        """Saves a new job or updates an existing one."""
        raise NotImplementedError

    @abstractmethod
    def get(self, job_id: UUID) -> Optional[Job]:
        """Retrieves a job by its ID."""
        raise NotImplementedError

    @abstractmethod
    def get_by_execution_id(self, execution_id: UUID) -> Optional[Job]:
        """Retrieves a job by its associated execution ID."""
        raise NotImplementedError

    @abstractmethod
    def list_jobs(self, limit: int = 100, offset: int = 0) -> Tuple[List[Job], int]:
        """
        Lists jobs with pagination.
        Returns a tuple of (jobs, total_count).
        """
        raise NotImplementedError

    @abstractmethod
    def get_jobs_due_for_retry(self, now: datetime, batch_size: int = 10) -> List[Job]:
        """
        Retrieves jobs due for retry, applying pessimistic locking.
        """
        raise NotImplementedError
