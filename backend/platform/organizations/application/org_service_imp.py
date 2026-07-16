from datetime import UTC, datetime
from uuid import UUID
from uuid import uuid4

from backend.platform.organizations.application.organization_service import (
    OrganizationService,
)
from backend.platform.organizations.domain.organization import Organization
from backend.platform.organizations.dto.create_organization_request import (
    CreateOrganizationRequest,
)
from backend.platform.organizations.dto.organization_response import (
    OrganizationResponse,
)
from backend.platform.organizations.repositories.organization_repository import (
    OrganizationRepository,
)
from backend.platform.shared.slug import generate_slug
from backend.platform.shared.exceptions.resource import (
    ResourceAlreadyExistsError,
)


class OrganizationServiceImpl(OrganizationService):
    """
    Default implementation of the organization application service.
    """

    def __init__(
        self,
        organization_repository: OrganizationRepository,
    ) -> None:
        self._organization_repository = organization_repository

    def create(
        self,
        owner_id: UUID,
        request: CreateOrganizationRequest,
    ) -> OrganizationResponse:
        now = datetime.now(UTC)

        slug = generate_slug(
            request.name,
        )

        existing = self._organization_repository.get_by_slug(
            slug,
        )

        if existing is not None:
            raise ResourceAlreadyExistsError(
                "An organization with this name already exists.",
            )

        organization = Organization(
            id=uuid4(),
            name=request.name,
            slug=slug,
            created_at=now,
            updated_at=now,
        )

        persisted_organization = self._organization_repository.save(
            organization,
        )

        return OrganizationResponse(
            id=persisted_organization.id,
            name=persisted_organization.name,
            slug=persisted_organization.slug,
            created_at=persisted_organization.created_at,
            updated_at=persisted_organization.updated_at,
        )

    def get(
        self,
        organization_id: UUID,
    ) -> OrganizationResponse | None:
        organization = self._organization_repository.get_by_id(
            organization_id,
        )

        if organization is None:
            return None

        return OrganizationResponse(
            id=organization.id,
            name=organization.name,
            slug=organization.slug,
            created_at=organization.created_at,
            updated_at=organization.updated_at,
        )

    def list(
        self,
    ) -> list[OrganizationResponse]:
        organizations = self._organization_repository.list_all()

        return [
            OrganizationResponse(
                id=organization.id,
                name=organization.name,
                slug=organization.slug,
                created_at=organization.created_at,
                updated_at=organization.updated_at,
            )
            for organization in organizations
        ]