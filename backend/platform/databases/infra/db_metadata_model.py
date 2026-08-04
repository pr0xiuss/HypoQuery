from uuid import uuid4, UUID
from datetime import datetime
from sqlalchemy import JSON, BigInteger, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
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

    database_size: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    settings: Mapped[dict[str, str]] = mapped_column(
        JSON,
    )

    replication: Mapped[dict[str, int | bool]] = mapped_column(
        JSON,
    )


    database_statistics: Mapped[dict] = mapped_column(
        JSON,
    )

    table_statistics: Mapped[list[dict]] = mapped_column(
        JSON,
    )

    index_statistics: Mapped[list[dict]] = mapped_column(
        JSON,
    )

    connection_statistics: Mapped[dict] = mapped_column(
        JSON,
    )

    lock_statistics: Mapped[dict] = mapped_column(
        JSON,
    )

    schemas: Mapped[list[dict]] = mapped_column(
        JSON,
    )

    tables: Mapped[list[dict]] = mapped_column(
        JSON,
    )

    columns: Mapped[list[dict]] = mapped_column(
        JSON,
    )

    constraints: Mapped[list[dict]] = mapped_column(
        JSON,
    )

    views: Mapped[list[dict]] = mapped_column(
        JSON,
    )

    functions: Mapped[list[dict]] = mapped_column(
        JSON,
    )

    indexes: Mapped[list[dict]] = mapped_column(
        JSON,
    )

    triggers: Mapped[list[dict]] = mapped_column(
        JSON,
    )

    sequences: Mapped[list[dict]] = mapped_column(
        JSON,
    )

    extensions: Mapped[list[dict]] = mapped_column(
        JSON,
    )

    last_refreshed: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
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