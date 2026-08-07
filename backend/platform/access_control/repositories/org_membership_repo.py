from abc import ABC
from abc import abstractmethod
from uuid import UUID

from backend.platform.access_control.domain.org_membership import (
    OrganizationMembership,
)


class OrganizationMembershipRepository(
    ABC,
):
    """
    Repository interface for organization memberships.
    """

    @abstractmethod
    def create(
        self,
        membership: OrganizationMembership,
    ) -> OrganizationMembership:
        """
        Persist a new organization membership.
        """

    @abstractmethod
    def get_by_id(
        self,
        membership_id: UUID,
    ) -> OrganizationMembership | None:
        """
        Retrieve a membership by its identifier.
        """

    @abstractmethod
    def list_by_organization(
        self,
        organization_id: UUID,
    ) -> list[OrganizationMembership]:
        """
        Return all memberships belonging to an organization.
        """

    @abstractmethod
    def list_by_user(
        self,
        user_id: UUID,
    ) -> list[OrganizationMembership]:
        """
        Return all organizations accessible by a user.
        """

    @abstractmethod
    def get_membership(
        self,
        organization_id: UUID,
        user_id: UUID,
    ) -> OrganizationMembership | None:
        """
        Retrieve a user's membership for an organization.
        """

    @abstractmethod
    def delete(
        self,
        membership_id: UUID,
    ) -> None:
        """
        Delete a membership.
        """