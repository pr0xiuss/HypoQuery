from abc import ABC
from abc import abstractmethod
from uuid import UUID

from backend.platform.organizations.dto.create_organization_request import CreateOrganizationRequest
from backend.platform.organizations.dto.organization_response import OrganizationResponse
from backend.platform.organizations.dto.update_org_request import UpdateOrganizationRequest

class OrganizationService(ABC):
    """
    Application service responsible for organization workflows.
    """

    @abstractmethod
    def create(
        self,
        owner_id: UUID,
        request: CreateOrganizationRequest,
    ) -> OrganizationResponse:
        """
        Create a new organization.
        """
        raise NotImplementedError

    @abstractmethod
    def get(
        self,
        organization_id: UUID,
    ) -> OrganizationResponse | None:
        """
        Retrieve an organization by its identifier.
        """
        raise NotImplementedError

    @abstractmethod
    def list(
        self,
    ) -> list[OrganizationResponse]:
        """
        Retrieve all organizations visible to the current user.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        organization_id: UUID,
    ) -> None:
        """
        Delete an organization.
        """
        raise NotImplementedError

    @abstractmethod
    def update(
        self,
        organization_id: UUID,
        request: UpdateOrganizationRequest,
    ) -> OrganizationResponse | None:
        """
        Update an organization.
        """
        raise NotImplementedError