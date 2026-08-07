from datetime import datetime, UTC
from uuid import uuid4
from uuid import UUID

from backend.platform.access_control.application.access_control_service import AccessControlService
from backend.platform.access_control.domain.org_membership import OrganizationMembership
from backend.platform.access_control.domain.org_role import OrganizationRole
from backend.platform.access_control.repositories.org_membership_repo import OrganizationMembershipRepository
from backend.platform.shared.exceptions import ResourceNotFoundError

class AccessControlServiceImpl(
    AccessControlService,
):
    """
    Default implementation of the access control service.
    """

    def __init__(
        self,
        repository: OrganizationMembershipRepository,
    ) -> None:
        self._repository = repository

    def create_owner_membership(
        self,
        organization_id: UUID,
        user_id: UUID,
    ) -> OrganizationMembership:
        membership = OrganizationMembership(
            id=uuid4(),
            organization_id=organization_id,
            user_id=user_id,
            role=OrganizationRole.OWNER,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )

        return self._repository.create(
            membership,
        )

    def get_user_memberships(
        self,
        user_id: UUID,
    ) -> list[OrganizationMembership]:
        return self._repository.list_by_user(
            user_id,
        )

    def has_access(
        self,
        organization_id: UUID,
        user_id: UUID,
    ) -> bool:
        membership = self._repository.get_membership(
            organization_id=organization_id,
            user_id=user_id,
        )

        return membership is not None

    def ensure_organization_access(
        self,
        organization_id: UUID,
        user_id: UUID,
    ) -> None:
        if not self._repository.exists(
            organization_id=organization_id,
            user_id=user_id,
        ):
            raise ResourceNotFoundError(
                "Organization",
                str(organization_id),
            )