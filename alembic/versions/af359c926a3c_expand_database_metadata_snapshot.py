"""expand database metadata snapshot

Revision ID: af359c926a3c
Revises: 13140371c78c
Create Date: 2026-07-26 13:15:34.225245

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'af359c926a3c'
down_revision: Union[str, Sequence[str], None] = '13140371c78c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "database_metadata",
        sa.Column(
            "database_size",
            sa.BigInteger(),
            nullable=True,
        ),
    )

    op.add_column(
        "database_metadata",
        sa.Column(
            "settings",
            sa.JSON(),
            nullable=True,
        ),
    )

    op.add_column(
        "database_metadata",
        sa.Column(
            "replication",
            sa.JSON(),
            nullable=True,
        ),
    )

    op.add_column(
        "database_metadata",
        sa.Column(
            "database_statistics",
            sa.JSON(),
            nullable=True,
        ),
    )

    op.add_column(
        "database_metadata",
        sa.Column(
            "table_statistics",
            sa.JSON(),
            nullable=True,
        ),
    )

    op.add_column(
        "database_metadata",
        sa.Column(
            "index_statistics",
            sa.JSON(),
            nullable=True,
        ),
    )

    op.add_column(
        "database_metadata",
        sa.Column(
            "connection_statistics",
            sa.JSON(),
            nullable=True,
        ),
    )

    op.add_column(
        "database_metadata",
        sa.Column(
            "lock_statistics",
            sa.JSON(),
            nullable=True,
        ),
    )

    op.add_column(
        "database_metadata",
        sa.Column(
            "last_refreshed",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column(
        "database_metadata",
        "last_refreshed",
    )

    op.drop_column(
        "database_metadata",
        "lock_statistics",
    )

    op.drop_column(
        "database_metadata",
        "connection_statistics",
    )

    op.drop_column(
        "database_metadata",
        "index_statistics",
    )

    op.drop_column(
        "database_metadata",
        "table_statistics",
    )

    op.drop_column(
        "database_metadata",
        "database_statistics",
    )

    op.drop_column(
        "database_metadata",
        "replication",
    )

    op.drop_column(
        "database_metadata",
        "settings",
    )

    op.drop_column(
        "database_metadata",
        "database_size",
    )
