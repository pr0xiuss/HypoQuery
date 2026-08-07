from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from backend.platform.access_control.domain.org_role import (
    OrganizationRole,
)


@dataclass(
    slots=True,
)
class OrganizationMembership:
    """
    Domain entity representing a user's membership
    within an organization.
    """

    id: UUID

    organization_id: UUID

    user_id: UUID

    role: OrganizationRole

    created_at: datetime

    updated_at: datetime