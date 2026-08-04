"""add columns metadata to database metadata

Revision ID: ba10f6a9caf3
Revises: af359c926a3c
Create Date: 2026-08-03 20:26:11.040251

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ba10f6a9caf3'
down_revision: Union[str, Sequence[str], None] = 'af359c926a3c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "database_metadata",
        sa.Column(
            "columns",
            postgresql.JSON(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::json"),
        ),
    )

    op.alter_column(
        "database_metadata",
        "columns",
        server_default=None,
    )   
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "database_metadata",
        "columns",
    )
    # ### end Alembic commands ###
