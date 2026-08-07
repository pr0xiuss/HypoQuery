"""scope project slug uniqueness

Revision ID: 167ee445c9ab
Revises: 9db2ff6baf79
Create Date: 2026-08-06 18:11:57.479058

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "167ee445c9ab"
down_revision: Union[str, Sequence[str], None] = "9db2ff6baf79"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Upgrade schema.
    """

    op.drop_index(
        "ix_projects_slug",
        table_name="projects",
    )

    op.create_index(
        "ix_projects_organization_slug",
        "projects",
        [
            "organization_id",
            "slug",
        ],
        unique=False,
    )

    op.create_unique_constraint(
        "uq_project_organization_slug",
        "projects",
        [
            "organization_id",
            "slug",
        ],
    )


def downgrade() -> None:
    """
    Downgrade schema.
    """

    op.drop_constraint(
        "uq_project_organization_slug",
        "projects",
        type_="unique",
    )

    op.drop_index(
        "ix_projects_organization_slug",
        table_name="projects",
    )

    op.create_index(
        "ix_projects_slug",
        "projects",
        [
            "slug",
        ],
        unique=True,
    )