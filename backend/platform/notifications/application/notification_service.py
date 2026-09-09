import logging
from typing import Optional
from uuid import UUID

from backend.platform.notifications.application.delivery_port import NotificationDeliveryPort
from backend.platform.notifications.domain.notification import Notification, NotificationType
from backend.platform.notifications.repositories.notification_repository import NotificationRepository
from backend.platform.notifications.repositories.preference_repository import NotificationPreferenceRepository
from backend.platform.scheduler.domain.job import Job, JobStatus
from backend.platform.scheduler.repositories.job_repository import JobRepository

logger = logging.getLogger(__name__)


class NotificationService:
    """
    Application service for managing and generating notifications.
    """

    def __init__(
        self,
        notification_repository: NotificationRepository,
        preference_repository: NotificationPreferenceRepository,
        delivery_port: NotificationDeliveryPort,
        job_repository: JobRepository,
    ):
        self._notification_repository = notification_repository
        self._preference_repository = preference_repository
        self._delivery_port = delivery_port
        self._job_repository = job_repository

    def handle_event_outcome(
        self,
        job_id: UUID,
        notification_type: NotificationType,
        execution_id: UUID,
        error_message: str | None = None
    ) -> None:
        """
        Evaluates a semantic outcome and generates a notification if applicable.
        Designed to be called by NotificationSubscriber independently of DB state.
        """
        # Check idempotency first to avoid redundant delivery or queries
        existing = self._notification_repository.get_by_idempotency_key(job_id, notification_type, execution_id)
        if existing:
            logger.debug(f"Notification already exists for Job {job_id}, attempt {execution_id}, type {notification_type.value}.")
            return

        job = self._job_repository.get(job_id)
        if not job:
            logger.warning(f"Job {job_id} not found for notification generation.")
            return

        user_id_str = job.payload.get("user_id")
        if not user_id_str:
            logger.debug(f"Job {job.job_id} has no user_id in payload. Skipping notification.")
            return
            
        try:
            user_id = UUID(user_id_str)
        except ValueError:
            logger.warning(f"Job {job.job_id} has invalid user_id {user_id_str}. Skipping notification.")
            return

        # Evaluate preferences
        preference = self._preference_repository.get_by_user_and_type(user_id, notification_type)
        if preference and not preference.is_enabled:
            logger.debug(f"User {user_id} has disabled {notification_type.value} notifications.")
            return

        # Generate the notification
        title, message = self._generate_content(job, notification_type, error_message)
        notification = Notification(
            user_id=user_id,
            notification_type=notification_type,
            job_id=job.job_id,
            execution_id=execution_id,
            title=title,
            message=message,
            metadata={
                "job_name": job.name,
                "job_type": job.job_type.value,
            }
        )

        # Persist and Deliver
        try:
            saved_notification = self._notification_repository.save(notification)
            self._delivery_port.deliver(saved_notification)
        except Exception as e:
            logger.error(f"Failed to generate or deliver notification for Job {job.job_id}: {e}", exc_info=True)
            raise

    def _generate_content(self, job: Job, n_type: NotificationType, error_message: str | None) -> tuple[str, str]:
        job_name = job.name or str(job.job_id)
        error_text = error_message or "Unknown error"
        if n_type == NotificationType.JOB_COMPLETED:
            return (
                f"Job Completed: {job_name}",
                f"Your background job '{job_name}' has successfully completed."
            )
        elif n_type == NotificationType.JOB_FAILED:
            return (
                f"Job Failed: {job_name}",
                f"Your background job '{job_name}' has permanently failed. Error: {error_text}"
            )
        elif n_type == NotificationType.JOB_RETRYING:
            return (
                f"Job Retrying: {job_name}",
                f"Your background job '{job_name}' failed and is scheduled to retry. Error: {error_text}"
            )
        return "Notification", "New notification received."
