from datetime import datetime
from uuid import UUID
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, String, Text, Enum, UniqueConstraint, func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from backend.platform.environments.domain.env_type import EnvironmentType
from backend.platform.shared.database import Base


class EnvironmentModel(Base):
    """
    SQLAlchemy persistence model for environments.
    """

    __tablename__ = "environments"

    __table_args__ = (
        UniqueConstraint(
            "project_id",
            "slug",
            name="uq_environment_project_slug",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    project_id: Mapped[UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    slug: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    environment_type: Mapped[EnvironmentType] = mapped_column(
        Enum(
            EnvironmentType,
            name="environmenttype",
            create_type=True,
        ),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )