from sqlalchemy.orm import Session

from backend.platform.access_control.application.access_control_service import (
    AccessControlService,
)
from backend.platform.access_control.application.access_control_service_impl import (
    AccessControlServiceImpl,
)
from backend.platform.access_control.infra.org_membership_repo_impl import (
    OrganizationMembershipRepositoryImpl,
)
from backend.platform.access_control.repositories.org_membership_repo import (
    OrganizationMembershipRepository,
)


def get_organization_membership_repository(
    session: Session,
) -> OrganizationMembershipRepository:
    """
    Returns the organization membership repository.
    """

    return OrganizationMembershipRepositoryImpl(
        session=session,
    )


def get_access_control_service(
    session: Session,
) -> AccessControlService:
    """
    Returns the access control application service.
    """

    repository = get_organization_membership_repository(
        session=session,
    )

    return AccessControlServiceImpl(
        repository=repository,
    )