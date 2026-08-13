from datetime import datetime
from uuid import UUID
from uuid import uuid4

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from backend.platform.apis.domain.api_framework import ApiFramework
from backend.platform.shared.database import Base


class ApiModel(
    Base,
):
    """
    SQLAlchemy persistence model for APIs.
    """

    __tablename__ = "apis"

    __table_args__ = (
        UniqueConstraint(
            "environment_id",
            "slug",
            name="uq_api_environment_slug",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    environment_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey(
            "environments.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    slug: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    service_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    framework: Mapped[ApiFramework] = mapped_column(
        Enum(
            ApiFramework,
            name="apiframwork",
            create_type=True,
        ),
        nullable=False,
    )

    framework_version: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    base_url: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    repository_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    openapi_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    health_endpoint: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    authentication_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    version: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
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