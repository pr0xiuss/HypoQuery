from abc import ABC
from abc import abstractmethod
from uuid import UUID

from backend.platform.organizations.domain.organization import Organization


class OrganizationRepository(ABC):
    """
    Repository contract for organization persistence.
    """

    @abstractmethod
    def save(
        self,
        organization: Organization,
    ) -> Organization:
        """
        Persist an organization.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_id(
        self,
        organization_id: UUID,
    ) -> Organization | None:
        """
        Retrieve an organization by its identifier.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_slug(
        self,
        slug: str,
    ) -> Organization | None:
        """
        Retrieve an organization by its slug.
        """
        raise NotImplementedError

    @abstractmethod
    def list_all(
        self,
    ) -> list[Organization]:
        """
        Retrieve all organizations.
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
        organization: Organization,
    ) -> Organization:
        """
        Update an organization.
        """
        raise NotImplementedError