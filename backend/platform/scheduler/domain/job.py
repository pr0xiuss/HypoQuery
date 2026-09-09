from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any, Dict, Optional
from uuid import UUID, uuid4


class JobStatus(Enum):
    """
    Status of an application-level background job.
    """
    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PENDING_RETRY = "pending_retry"


class JobType(Enum):
    """
    Types of background jobs supported by the platform.
    """
    WORKLOAD_ANALYSIS = "workload_analysis"
    DATABASE_SYNC = "database_sync"
    MAINTENANCE = "maintenance"
    # Other job types can be added here as needed


@dataclass(frozen=True, slots=True)
class Job:
    """
    Represents an application-level request for background work.
    
    This is distinct from PipelineExecution, which represents the actual
    running instance within the execution engine.
    """
    name: str
    job_type: JobType
    payload: Dict[str, Any]
    
    # Optional relationships to other domains
    project_id: Optional[UUID] = None
    environment_id: Optional[UUID] = None
    
    # State tracking
    status: JobStatus = JobStatus.PENDING
    
    # Identity and audit
    job_id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    
    # Link to actual execution framework execution ID if applicable
    execution_id: Optional[UUID] = None
    
    error_message: Optional[str] = None

    # Retry tracking
    attempt_count: int = 0
    max_attempts: int = 3
    last_attempt_at: Optional[datetime] = None
    next_attempt_at: Optional[datetime] = None
    
    def with_status(
        self, 
        new_status: JobStatus, 
        execution_id: Optional[UUID] = None,
        error_message: Optional[str] = None
    ) -> "Job":
        """Returns a new Job instance with updated status and audit timestamp."""
        return Job(
            job_id=self.job_id,
            name=self.name,
            job_type=self.job_type,
            payload=self.payload,
            project_id=self.project_id,
            environment_id=self.environment_id,
            status=new_status,
            created_at=self.created_at,
            updated_at=datetime.now(UTC),
            execution_id=execution_id or self.execution_id,
            error_message=error_message or self.error_message,
            attempt_count=self.attempt_count,
            max_attempts=self.max_attempts,
            last_attempt_at=self.last_attempt_at,
            next_attempt_at=self.next_attempt_at
        )

    def with_retry_tracking(
        self,
        attempt_count: int,
        last_attempt_at: Optional[datetime] = None,
        next_attempt_at: Optional[datetime] = None
    ) -> "Job":
        """Returns a new Job instance with updated retry tracking fields."""
        return Job(
            job_id=self.job_id,
            name=self.name,
            job_type=self.job_type,
            payload=self.payload,
            project_id=self.project_id,
            environment_id=self.environment_id,
            status=self.status,
            created_at=self.created_at,
            updated_at=datetime.now(UTC),
            execution_id=self.execution_id,
            error_message=self.error_message,
            attempt_count=attempt_count,
            max_attempts=self.max_attempts,
            last_attempt_at=last_attempt_at,
            next_attempt_at=next_attempt_at
        )
