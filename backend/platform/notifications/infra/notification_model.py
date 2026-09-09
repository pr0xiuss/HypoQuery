import uuid
from datetime import datetime, UTC

from sqlalchemy import Boolean, Column, DateTime, String, JSON, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from backend.platform.shared.database import Base


def _now() -> datetime:
    return datetime.now(UTC)


class NotificationModel(Base):
    """
    SQLAlchemy model for persisting notifications.
    """
    __tablename__ = "notifications"

    notification_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    notification_type = Column(String(50), nullable=False)
    
    # Core identifying factors
    job_id = Column(UUID(as_uuid=True), nullable=True)
    execution_id = Column(UUID(as_uuid=True), nullable=True)
    
    # Content
    title = Column(String(255), nullable=False)
    message = Column(String, nullable=False)
    metadata_ = Column("metadata", JSON, nullable=False, default=dict)
    
    # State
    is_read = Column(Boolean, nullable=False, default=False)
    
    created_at = Column(DateTime(timezone=True), default=_now, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            'job_id', 'notification_type', 'execution_id',
            name='uix_notification_job_type_exec'
        ),
    )
