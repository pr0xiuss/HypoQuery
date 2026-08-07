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
        user_id: UUID,
    ) -> OrganizationResponse:
        """
        Returns an organization if the user has access.
        """
        raise NotImplementedError

    @abstractmethod
    def list(
        self,
        user_id: UUID,
    ) -> list[OrganizationResponse]:
        """
        Returns organizations accessible to the user.
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
        user_id: UUID,
        request: UpdateOrganizationRequest,
    ) -> OrganizationResponse:
        """
        Updates an organization if the user has access.
        """
        raise NotImplementedError
    