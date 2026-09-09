"""add index to execution_events platform_job_id

Revision ID: 58af12f9c22b
Revises: 6c4e78737d0a
Create Date: 2026-08-25 17:39:30.974895

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '58af12f9c22b'
down_revision: Union[str, Sequence[str], None] = '6c4e78737d0a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE INDEX ix_execution_events_platform_job_id ON execution_events ((payload->'metadata'->>'platform_job_id'))")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP INDEX ix_execution_events_platform_job_id")
