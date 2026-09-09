from typing import Optional

from backend.execution.contracts.events.base import ExecutionEvent
from backend.execution.contracts.events.pipeline import (
    PipelineStartedEvent,
    PipelineCompletedEvent,
    PipelineFailedEvent,
    PipelineCancelledEvent,
)
from backend.execution.contracts.subscriber import Subscriber
from backend.platform.scheduler.domain.job import JobStatus
from backend.platform.scheduler.application.retry_policy import RetryPolicy
from backend.platform.scheduler.repositories.job_repository import JobRepository
from backend.platform.shared.transactions.transaction_manager import TransactionManager


class JobLifecycleSubscriber(Subscriber):
    """
    Subscribes to execution events to transition Job status.
    
    Acts as the bridge from execution framework -> Platform Job state.
    """

    def __init__(
        self,
        job_repository: JobRepository,
        transaction_manager: TransactionManager,
        retry_policy: RetryPolicy,
    ):
        self._job_repository = job_repository
        self._transaction_manager = transaction_manager
        self._retry_policy = retry_policy

    def handle(self, event: ExecutionEvent) -> None:
        if isinstance(event, PipelineStartedEvent):
            self._update_status(event, JobStatus.RUNNING)
        elif isinstance(event, PipelineCompletedEvent):
            self._update_status(event, JobStatus.COMPLETED)
        elif isinstance(event, PipelineFailedEvent):
            self._handle_failure(event)
        elif isinstance(event, PipelineCancelledEvent):
            self._update_status(event, JobStatus.FAILED, error_message=event.reason)

    def _update_status(self, event: ExecutionEvent, status: JobStatus, error_message: str | None = None) -> None:
        if not event.metadata or not event.metadata.execution_id:
            return

        try:
            job = self._job_repository.get_by_execution_id(event.metadata.execution_id)
            if job:
                # Use with_status logic to validate transitions
                try:
                    updated_job = job.with_status(status, error_message=error_message)
                    self._job_repository.save(updated_job)
                    self._transaction_manager.commit()
                except ValueError:
                    # Ignore invalid transitions quietly in background
                    self._transaction_manager.rollback()
        except Exception:
            self._transaction_manager.rollback()
            raise

    def _handle_failure(self, event: PipelineFailedEvent) -> None:
        if not event.metadata or not event.metadata.execution_id:
            return

        try:
            job = self._job_repository.get_by_execution_id(event.metadata.execution_id)
            if job:
                # Increment attempts
                job = job.with_retry_tracking(
                    attempt_count=job.attempt_count + 1,
                    last_attempt_at=event.metadata.timestamp
                )

                # Check retry policy
                next_attempt = self._retry_policy.calculate_next_attempt(job, event.error_type)
                
                if next_attempt:
                    # Will retry
                    job = job.with_status(JobStatus.PENDING_RETRY, error_message=event.error)
                    job = job.with_retry_tracking(
                        attempt_count=job.attempt_count,
                        last_attempt_at=job.last_attempt_at,
                        next_attempt_at=next_attempt
                    )
                else:
                    # Exhausted or not retryable
                    job = job.with_status(JobStatus.FAILED, error_message=event.error)
                
                self._job_repository.save(job)
                self._transaction_manager.commit()
        except Exception:
            self._transaction_manager.rollback()
            raise
