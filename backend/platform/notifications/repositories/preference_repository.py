from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from backend.platform.notifications.domain.notification import NotificationType
from backend.platform.notifications.domain.preference import NotificationPreference


class NotificationPreferenceRepository(ABC):
    @abstractmethod
    def save(self, preference: NotificationPreference) -> NotificationPreference:
        pass

    @abstractmethod
    def get_by_user_and_type(self, user_id: UUID, notification_type: NotificationType) -> Optional[NotificationPreference]:
        pass

    @abstractmethod
    def list_for_user(self, user_id: UUID) -> List[NotificationPreference]:
        pass
