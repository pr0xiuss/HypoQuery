"""create apis table

Revision ID: 13140371c78c
Revises: cb502f957eec
Create Date: 2026-07-25 19:07:08.166718

"""
from typing import Sequence, Union
from sqlalchemy.dialects import postgresql
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '13140371c78c'
down_revision: Union[str, Sequence[str], None] = 'cb502f957eec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    api_framework = postgresql.ENUM(
        "FASTAPI",
        "DJANGO",
        "FLASK",
        "EXPRESS",
        "SPRING_BOOT",
        "ASP_NET",
        "GO",
        "LARAVEL",
        "OTHER",
        name="apiframework",
        create_type=False
    )

    api_framework.create(
        op.get_bind(),
        checkfirst=True,
    )

    op.create_table(
        "apis",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "environment_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "name",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "slug",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "description",
            sa.String(length=500),
            nullable=True,
        ),
        sa.Column(
            "framework",
            api_framework,
            nullable=False,
        ),
        sa.Column(
            "base_url",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "version",
            sa.String(length=50),
            nullable=True,
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["environment_id"],
            ["environments.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "environment_id",
            "slug",
            name="uq_api_environment_slug",
        ),
    )

    op.create_index(
        op.f("ix_apis_slug"),
        "apis",
        ["slug"],
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        op.f("ix_apis_slug"),
        table_name="apis",
    )

    op.drop_table("apis")

    api_framework = postgresql.ENUM(
        "FASTAPI",
        "DJANGO",
        "FLASK",
        "EXPRESS",
        "SPRING_BOOT",
        "ASP_NET",
        "GO",
        "LARAVEL",
        "OTHER",
        name="apiframework",
    )

    api_framework.drop(
        op.get_bind(),
        checkfirst=True,
    )
