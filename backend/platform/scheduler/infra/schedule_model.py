import uuid
from datetime import datetime, UTC

from sqlalchemy import Boolean, Column, DateTime, Integer, String, JSON
from sqlalchemy.dialects.postgresql import UUID

from backend.platform.shared.database import Base


def _now() -> datetime:
    return datetime.now(UTC)


class ScheduleModel(Base):
    """
    SQLAlchemy model for persisting background schedules.
    """
    __tablename__ = "schedules"

    schedule_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    job_type = Column(String(100), nullable=False)
    payload = Column(JSON, nullable=False, default=dict)
    
    interval_seconds = Column(Integer, nullable=False)
    is_enabled = Column(Boolean, nullable=False, default=True)
    
    next_run_at = Column(DateTime(timezone=True), nullable=False)
    last_run_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), default=_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=_now, onupdate=_now, nullable=False)
