import uuid
from datetime import datetime, UTC

from sqlalchemy import Boolean, Column, DateTime, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from backend.platform.shared.database import Base


def _now() -> datetime:
    return datetime.now(UTC)


class NotificationPreferenceModel(Base):
    """
    SQLAlchemy model for user notification preferences.
    """
    __tablename__ = "notification_preferences"

    preference_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    notification_type = Column(String(50), nullable=False)
    
    is_enabled = Column(Boolean, nullable=False, default=True)
    
    created_at = Column(DateTime(timezone=True), default=_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=_now, onupdate=_now, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            'user_id', 'notification_type',
            name='uix_notification_pref_user_type'
        ),
    )
