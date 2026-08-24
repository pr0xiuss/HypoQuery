"""create_execution_events_table

Revision ID: 71115762bc50
Revises: bf0a0df70b71
Create Date: 2026-08-24 20:19:08.415793

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '71115762bc50'
down_revision: Union[str, Sequence[str], None] = 'bf0a0df70b71'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'execution_events',
        sa.Column('event_id', sa.UUID(), nullable=False),
        sa.Column('execution_id', sa.UUID(), nullable=False),
        sa.Column('trace_id', sa.UUID(), nullable=False),
        sa.Column('event_type', sa.String(length=100), nullable=False),
        sa.Column('event_version', sa.String(length=20), nullable=False),
        sa.Column('occurred_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('payload', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.PrimaryKeyConstraint('event_id')
    )
    op.create_index('ix_execution_events_execution_id', 'execution_events', ['execution_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('ix_execution_events_execution_id', table_name='execution_events')
    op.drop_table('execution_events')
