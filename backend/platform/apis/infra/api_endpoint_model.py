from pathlib import Path
from uuid import UUID
from uuid import uuid4

from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from backend.platform.shared.database import Base


class ApiEndpointModel(
    Base,
):
    """
    SQLAlchemy persistence model for a discovered API endpoint.
    """

    __tablename__ = "api_endpoints"

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    api_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey(
            "apis.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    method: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
    )

    path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    handler: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    source_file: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    line_number: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    summary: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    tags: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        nullable=False,
        default=list,
    )

    version: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    authentication_required: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )