"""
complete api discovery refactor

Revision ID: 4c39328426a2
Revises: 167ee445c9ab
Create Date: 2026-08-07 17:33:41.614905
"""

from typing import Sequence
from typing import Union

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

    bind = op.get_bind()

    # ------------------------------------------------------------------
    # API framework enum
    # ------------------------------------------------------------------

    api_framework_enum.create(
        bind,
        checkfirst=True,
    )

    op.execute(
        """
        ALTER TABLE apis
        ALTER COLUMN framework
        TYPE apiframwork
        USING framework::apiframwork
        """
    )

    # ------------------------------------------------------------------
    # API metadata changes
    # ------------------------------------------------------------------

    op.alter_column(
        "apis",
        "description",
        existing_type=sa.VARCHAR(length=500),
        nullable=True,
    )

    op.alter_column(
        "apis",
        "version",
        existing_type=sa.VARCHAR(length=50),
        nullable=True,
    )

    # ------------------------------------------------------------------
    # API endpoints
    # ------------------------------------------------------------------

    op.create_table(
        "api_endpoints",
        sa.Column(
            "id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "api_id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "method",
            sa.String(length=16),
            nullable=False,
        ),
        sa.Column(
            "path",
            sa.String(length=500),
            nullable=False,
        ),
        sa.Column(
            "handler",
            sa.String(length=500),
            nullable=False,
        ),
        sa.Column(
            "source_file",
            sa.String(length=1000),
            nullable=True,
        ),
        sa.Column(
            "line_number",
            sa.Integer(),
            nullable=True,
        ),
        sa.Column(
            "summary",
            sa.String(length=500),
            nullable=True,
        ),
        sa.Column(
            "description",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "tags",
            sa.JSON(),
            nullable=False,
        ),
        sa.Column(
            "version",
            sa.String(length=50),
            nullable=True,
        ),
        sa.Column(
            "authentication_required",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
        sa.PrimaryKeyConstraint(
            "id",
        ),
        sa.ForeignKeyConstraint(
            ["api_id"],
            ["apis.id"],
            ondelete="CASCADE",
        ),
        sa.UniqueConstraint(
            "api_id",
            "method",
            "path",
            name="uq_api_endpoints_api_method_path",
        ),
    )

    op.create_index(
        "ix_api_endpoints_api_id",
        "api_endpoints",
        ["api_id"],
    )

    op.create_index(
        "ix_api_endpoints_api_method_path",
        "api_endpoints",
        ["api_id", "method", "path"],
    )


def downgrade() -> None:
    """Downgrade schema."""

    # The endpoint table may not exist if the database was
    # previously migrated using an older version of this revision.
    op.execute(
        """
        DROP TABLE IF EXISTS api_endpoints CASCADE
        """
    )

    # Remove endpoint-specific fields that belonged to the
    # previous API registration model.
    op.drop_column(
        "apis",
        "path",
    )

    op.drop_column(
        "apis",
        "method",
    )

    # Restore the original API column definitions.
    op.alter_column(
        "apis",
        "version",
        existing_type=sa.VARCHAR(length=50),
        nullable=False,
    )

    op.alter_column(
        "apis",
        "description",
        existing_type=sa.VARCHAR(length=500),
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

    api_framework_enum.drop(
        op.get_bind(),
        checkfirst=True,
    )