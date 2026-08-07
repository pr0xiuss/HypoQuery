"""complete api discovery refactor

Revision ID: 4c39328426a2
Revises: 167ee445c9ab
Create Date: 2026-08-07 17:33:41.614905
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4c39328426a2"
down_revision: Union[str, Sequence[str], None] = "167ee445c9ab"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


api_framework_enum = sa.Enum(
    "FASTAPI",
    "DJANGO",
    "FLASK",
    "EXPRESS",
    "SPRING_BOOT",
    "ASP_NET",
    "GO",
    "LARAVEL",
    "OTHER",
    name="apiframwork",
)


def upgrade() -> None:
    """Upgrade schema."""

    api_framework_enum.create(
        op.get_bind(),
        checkfirst=True,
    )

    op.add_column(
        "apis",
        sa.Column(
            "method",
            sa.String(length=16),
            nullable=False,
        ),
    )

    op.add_column(
        "apis",
        sa.Column(
            "path",
            sa.String(length=500),
            nullable=False,
        ),
    )

    op.alter_column(
        "apis",
        "description",
        existing_type=sa.VARCHAR(length=500),
        nullable=True,
    )

    op.execute(
        """
        ALTER TABLE apis
        ALTER COLUMN framework
        TYPE apiframwork
        USING framework::apiframwork
        """
    )

    op.alter_column(
        "apis",
        "version",
        existing_type=sa.VARCHAR(length=50),
        nullable=True,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.alter_column(
        "apis",
        "version",
        existing_type=sa.VARCHAR(length=50),
        nullable=False,
    )

    op.execute(
        """
        ALTER TABLE apis
        ALTER COLUMN framework
        TYPE VARCHAR(50)
        USING framework::text
        """
    )

    op.alter_column(
        "apis",
        "description",
        existing_type=sa.VARCHAR(length=500),
        nullable=False,
    )

    op.drop_column(
        "apis",
        "path",
    )

    op.drop_column(
        "apis",
        "method",
    )

    api_framework_enum.drop(
        op.get_bind(),
        checkfirst=True,
    )