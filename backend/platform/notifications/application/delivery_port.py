from abc import ABC, abstractmethod

from backend.platform.notifications.domain.notification import Notification


class NotificationDeliveryPort(ABC):
    """
    Port for delivering notifications externally (e.g., email, webhook).
    """

    @abstractmethod
    def deliver(self, notification: Notification) -> None:
        """
        Deliver a notification to the user.
        """
        pass
