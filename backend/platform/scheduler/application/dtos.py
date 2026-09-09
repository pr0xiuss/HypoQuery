from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID
from pydantic import BaseModel, Field

from backend.platform.scheduler.domain.job import JobStatus, JobType


class JobSubmissionRequest(BaseModel):
    """Request to submit a new background job."""
    name: str
    job_type: JobType
    payload: Dict[str, Any] = Field(default_factory=dict)
    project_id: Optional[UUID] = None
    environment_id: Optional[UUID] = None


class JobSummaryDTO(BaseModel):
    """Compact summary of a background job."""
    job_id: UUID
    name: str
    job_type: JobType
    status: JobStatus
    created_at: datetime
    updated_at: datetime
    execution_id: Optional[UUID] = None


class JobDetailDTO(JobSummaryDTO):
    """Detailed view of a background job, including payload."""
    payload: Dict[str, Any]
    project_id: Optional[UUID] = None
    environment_id: Optional[UUID] = None
    error_message: Optional[str] = None


class JobListResponse(BaseModel):
    """Paginated list of jobs."""
    jobs: List[JobSummaryDTO]
    total_count: int
    limit: int
    offset: int


class ScheduleCreateRequest(BaseModel):
    """Request to create a new schedule."""
    name: str
    job_type: JobType
    payload: Dict[str, Any] = Field(default_factory=dict)
    interval_seconds: int = Field(gt=0, description="Interval between runs in seconds.")


class ScheduleUpdateRequest(BaseModel):
    """Request to update an existing schedule."""
    name: Optional[str] = None
    payload: Optional[Dict[str, Any]] = None
    interval_seconds: Optional[int] = Field(default=None, gt=0)
    is_enabled: Optional[bool] = None


class ScheduleDTO(BaseModel):
    """View representation of a schedule."""
    schedule_id: UUID
    name: str
    job_type: JobType
    payload: Dict[str, Any]
    interval_seconds: int
    is_enabled: bool
    next_run_at: datetime
    last_run_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class ScheduleListResponse(BaseModel):
    """Paginated list of schedules."""
    schedules: List[ScheduleDTO]
    total_count: int
    limit: int
    offset: int
