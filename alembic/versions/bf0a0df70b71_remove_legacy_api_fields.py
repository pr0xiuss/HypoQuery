"""remove legacy api fields

Revision ID: bf0a0df70b71
Revises: 4c39328426a2
Create Date: 2026-08-19 17:24:14.227257
"""

from typing import Sequence
from typing import Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bf0a0df70b71"
down_revision: Union[str, Sequence[str], None] = "4c39328426a2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Remove legacy API fields."""

    op.drop_column(
        "apis",
        "service_name",
    )

    op.drop_column(
        "apis",
        "framework_version",
    )

    op.drop_column(
        "apis",
        "repository_url",
    )

    op.drop_column(
        "apis",
        "openapi_url",
    )

    op.drop_column(
        "apis",
        "health_endpoint",
    )

    op.drop_column(
        "apis",
        "authentication_type",
    )


def downgrade() -> None:
    """Restore legacy API fields."""

    op.add_column(
        "apis",
        sa.Column(
            "service_name",
            sa.String(length=100),
            nullable=True,
        ),
    )

    op.add_column(
        "apis",
        sa.Column(
            "framework_version",
            sa.String(length=50),
            nullable=True,
        ),
    )

    op.add_column(
        "apis",
        sa.Column(
            "repository_url",
            sa.String(length=500),
            nullable=True,
        ),
    )

    op.add_column(
        "apis",
        sa.Column(
            "openapi_url",
            sa.String(length=500),
            nullable=True,
        ),
    )

    op.add_column(
        "apis",
        sa.Column(
            "health_endpoint",
            sa.String(length=255),
            nullable=True,
        ),
    )

    op.add_column(
        "apis",
        sa.Column(
            "authentication_type",
            sa.String(length=50),
            nullable=True,
        ),
    )