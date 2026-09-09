import logging
from typing import Optional
from uuid import UUID

from backend.execution.contracts.events.base import ExecutionEvent
from backend.execution.contracts.events.pipeline import (
    PipelineCompletedEvent,
    PipelineFailedEvent,
)
from backend.execution.contracts.subscriber import Subscriber
from backend.platform.notifications.application.notification_service import NotificationService
from backend.platform.notifications.domain.notification import NotificationType
from backend.platform.scheduler.application.retry_policy import RetryClassifier
from backend.platform.scheduler.domain.job import JobStatus

logger = logging.getLogger(__name__)


class NotificationSubscriber(Subscriber):
    """
    Subscribes to execution events to determine and generate appropriate notifications.
    
    This subscriber explicitly does NOT depend on the state of the Job in the database,
    nor does it depend on the execution order of `JobLifecycleSubscriber`. It uses the
    `RetryClassifier` and execution metadata to deterministically derive the job outcome.
    """

    def __init__(
        self,
        notification_service: NotificationService,
        retry_classifier: RetryClassifier,
    ):
        self._notification_service = notification_service
        self._retry_classifier = retry_classifier

    def handle(self, event: ExecutionEvent) -> None:
        # We only care about high-level outcomes
        if isinstance(event, PipelineCompletedEvent):
            self._handle_completed(event)
        elif isinstance(event, PipelineFailedEvent):
            self._handle_failed(event)

    def _get_platform_job_id(self, event: ExecutionEvent) -> Optional[UUID]:
        if not event.metadata or not event.metadata.metadata:
            return None
        job_id_str = event.metadata.metadata.get("platform_job_id")
        if not job_id_str:
            return None
        try:
            return UUID(job_id_str)
        except ValueError:
            return None

    def _handle_completed(self, event: PipelineCompletedEvent) -> None:
        job_id = self._get_platform_job_id(event)
        if not job_id:
            return

        execution_id = event.metadata.execution_id
        
        try:
            self._notification_service.handle_event_outcome(
                job_id=job_id,
                notification_type=NotificationType.JOB_COMPLETED,
                execution_id=execution_id
            )
        except Exception as e:
            logger.error(f"Failed to generate JOB_COMPLETED notification for job {job_id}: {e}")

    def _handle_failed(self, event: PipelineFailedEvent) -> None:
        job_id = self._get_platform_job_id(event)
        if not job_id:
            return

        execution_id = event.metadata.execution_id
        
        # Read the explicitly injected attempt context from metadata
        metadata = event.metadata.metadata or {}
        attempt_count = metadata.get("job_attempt_count", 1)
        max_attempts = metadata.get("job_max_attempts", 1)
        error_type = event.error_type
        
        is_retryable_error = self._retry_classifier.is_retryable(error_type)
        is_exhausted = attempt_count >= max_attempts

        # If it's retryable and we haven't exhausted attempts, it's a retry.
        if is_retryable_error and not is_exhausted:
            notification_type = NotificationType.JOB_RETRYING
        else:
            notification_type = NotificationType.JOB_FAILED

        try:
            self._notification_service.handle_event_outcome(
                job_id=job_id,
                notification_type=notification_type,
                execution_id=execution_id,
                error_message=event.error
            )
        except Exception as e:
            logger.error(f"Failed to generate {notification_type.value} notification for job {job_id}: {e}")
