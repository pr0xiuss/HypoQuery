import logging

from backend.platform.notifications.application.delivery_port import NotificationDeliveryPort
from backend.platform.notifications.domain.notification import Notification

logger = logging.getLogger(__name__)


class LoggingNotificationDeliveryAdapter(NotificationDeliveryPort):
    """
    Adapter that logs notifications instead of sending real emails/webhooks.
    Used for testing, development, and Batch 5 verification.
    """

    def deliver(self, notification: Notification) -> None:
        logger.info(
            f"[NOTIFICATION DELIVERY] To: User {notification.user_id} | "
            f"Type: {notification.notification_type.value} | "
            f"Title: {notification.title} | "
            f"Message: {notification.message}"
        )
