from datetime import datetime
from typing import List, Optional, Tuple
from uuid import UUID

from sqlalchemy.orm import Session

from backend.platform.scheduler.domain.job import Job, JobStatus, JobType
from backend.platform.scheduler.infra.job_model import JobModel
from backend.platform.scheduler.repositories.job_repository import JobRepository


class SqlAlchemyJobRepository(JobRepository):
    """
    SQLAlchemy implementation of the JobRepository.
    """

    def __init__(self, session: Session):
        self._session = session

    def _to_domain(self, model: JobModel) -> Job:
        return Job(
            job_id=model.job_id,
            name=model.name,
            job_type=JobType(model.job_type),
            payload=model.payload,
            project_id=model.project_id,
            environment_id=model.environment_id,
            status=JobStatus(model.status),
            created_at=model.created_at,
            updated_at=model.updated_at,
            execution_id=model.execution_id,
            error_message=model.error_message,
            attempt_count=model.attempt_count,
            max_attempts=model.max_attempts,
            last_attempt_at=model.last_attempt_at,
            next_attempt_at=model.next_attempt_at,
        )

    def _to_model(self, job: Job, existing: Optional[JobModel] = None) -> JobModel:
        model = existing or JobModel(job_id=job.job_id)
        model.name = job.name
        model.job_type = job.job_type.value
        model.payload = job.payload
        model.project_id = job.project_id
        model.environment_id = job.environment_id
        model.status = job.status.value
        model.created_at = job.created_at
        model.updated_at = job.updated_at
        model.execution_id = job.execution_id
        model.error_message = job.error_message
        model.attempt_count = job.attempt_count
        model.max_attempts = job.max_attempts
        model.last_attempt_at = job.last_attempt_at
        model.next_attempt_at = job.next_attempt_at
        return model

    def save(self, job: Job) -> Job:
        model = self._session.query(JobModel).filter_by(job_id=job.job_id).first()
        model = self._to_model(job, model)
        
        self._session.add(model)
        self._session.flush()
        
        return self._to_domain(model)

    def get(self, job_id: UUID) -> Optional[Job]:
        model = self._session.query(JobModel).filter_by(job_id=job_id).first()
        if not model:
            return None
        return self._to_domain(model)

    def get_by_execution_id(self, execution_id: UUID) -> Optional[Job]:
        model = self._session.query(JobModel).filter_by(execution_id=execution_id).first()
        if not model:
            return None
        return self._to_domain(model)

    def list_jobs(self, limit: int = 100, offset: int = 0) -> Tuple[List[Job], int]:
        query = self._session.query(JobModel)
        total_count = query.count()
        
        models = query.order_by(JobModel.created_at.desc()).offset(offset).limit(limit).all()
        return [self._to_domain(m) for m in models], total_count

    def get_jobs_due_for_retry(self, now: datetime, batch_size: int = 10) -> List[Job]:
        """
        Retrieves jobs that are PENDING_RETRY and their next_attempt_at is due.
        Uses FOR UPDATE SKIP LOCKED to prevent concurrent processing.
        """
        models = (
            self._session.query(JobModel)
            .filter(
                JobModel.status == JobStatus.PENDING_RETRY.value,
                JobModel.next_attempt_at <= now
            )
            .with_for_update(skip_locked=True)
            .order_by(JobModel.next_attempt_at.asc())
            .limit(batch_size)
            .all()
        )
        return [self._to_domain(m) for m in models]
