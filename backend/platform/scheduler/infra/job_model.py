from sqlalchemy import Column, String, DateTime, JSON, Integer
from sqlalchemy.dialects.postgresql import UUID
from datetime import UTC, datetime

from backend.platform.shared.database import Base


class JobModel(Base):
    """
    SQLAlchemy model for application-level background jobs.
    """
    __tablename__ = "jobs"

    job_id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(255), nullable=False)
    job_type = Column(String(100), nullable=False)
    
    # Store payload as JSONB
    payload = Column(JSON, nullable=False, default=dict)
    
    project_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    environment_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    
    status = Column(String(50), nullable=False, index=True)
    
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))
    
    execution_id = Column(UUID(as_uuid=True), nullable=True)
    error_message = Column(String, nullable=True)

    attempt_count = Column(Integer, nullable=False, default=0, server_default="0")
    max_attempts = Column(Integer, nullable=False, default=3, server_default="3")
    last_attempt_at = Column(DateTime(timezone=True), nullable=True)
    next_attempt_at = Column(DateTime(timezone=True), nullable=True)
