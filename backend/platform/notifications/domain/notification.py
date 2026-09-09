from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any, Dict, Optional
from uuid import UUID, uuid4


class NotificationType(Enum):
    JOB_COMPLETED = "job_completed"
    JOB_FAILED = "job_failed"
    JOB_RETRYING = "job_retrying"


@dataclass(frozen=True, slots=True)
class Notification:
    """
    Domain model for a user-facing notification.
    """
    user_id: UUID
    notification_type: NotificationType
    
    # Core identifying factors
    job_id: Optional[UUID] = None
    execution_id: Optional[UUID] = None
    
    # Content
    title: str = ""
    message: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # State
    is_read: bool = False
    
    # Identity and audit
    notification_id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def mark_read(self) -> "Notification":
        return Notification(
            user_id=self.user_id,
            notification_type=self.notification_type,
            job_id=self.job_id,
            execution_id=self.execution_id,
            title=self.title,
            message=self.message,
            metadata=self.metadata,
            is_read=True,
            notification_id=self.notification_id,
            created_at=self.created_at
        )
