from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from backend.platform.notifications.domain.notification import Notification, NotificationType


class NotificationRepository(ABC):
    @abstractmethod
    def save(self, notification: Notification) -> Notification:
        pass

    @abstractmethod
    def get(self, notification_id: UUID) -> Optional[Notification]:
        pass

    @abstractmethod
    def get_by_idempotency_key(self, job_id: UUID, notification_type: NotificationType, execution_id: UUID) -> Optional[Notification]:
        pass

    @abstractmethod
    def list_for_user(self, user_id: UUID, limit: int = 50, offset: int = 0) -> List[Notification]:
        pass

    @abstractmethod
    def count_unread_for_user(self, user_id: UUID) -> int:
        pass
