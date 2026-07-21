from uuid import uuid4, UUID
from datetime import datetime
from sqlalchemy import JSON, DateTime, func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from backend.platform.shared.database import Base


class DatabaseMetadataModel(Base):
    __tablename__ = "database_metadata"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    connection_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "database_connections.id",
            ondelete="CASCADE",
        ),
        unique=True,
        nullable=False,
    )

    postgres_version: Mapped[str]

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

    schemas: Mapped[list[str]] = mapped_column(
        JSON,
    )

    tables: Mapped[list[str]] = mapped_column(
        JSON,
    )

    views: Mapped[list[str]] = mapped_column(
        JSON,
    )

    functions: Mapped[list[str]] = mapped_column(
        JSON,
    )

    indexes: Mapped[list[str]] = mapped_column(
        JSON,
    )

    triggers: Mapped[list[str]] = mapped_column(
        JSON,
    )

    sequences: Mapped[list[str]] = mapped_column(
        JSON,
    )

    extensions: Mapped[list[str]] = mapped_column(
        JSON,
    )