from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Optional
from uuid import UUID, uuid4

from backend.platform.notifications.domain.notification import NotificationType


@dataclass(frozen=True, slots=True)
class NotificationPreference:
    """
    User preference for a specific notification type.
    """
    user_id: UUID
    notification_type: NotificationType
    is_enabled: bool
    
    preference_id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def with_status(self, is_enabled: bool) -> "NotificationPreference":
        return NotificationPreference(
            user_id=self.user_id,
            notification_type=self.notification_type,
            is_enabled=is_enabled,
            preference_id=self.preference_id,
            created_at=self.created_at,
            updated_at=datetime.now(UTC)
        )
