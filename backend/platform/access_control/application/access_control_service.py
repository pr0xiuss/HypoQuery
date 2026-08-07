from abc import ABC
from abc import abstractmethod
from uuid import UUID

from backend.platform.access_control.domain.org_membership import (
    OrganizationMembership,
)


class AccessControlService(
    ABC,
):
    """
    Application service responsible for
    organization access control.
    """

    @abstractmethod
    def create_owner_membership(
        self,
        organization_id: UUID,
        user_id: UUID,
    ) -> OrganizationMembership:
        """
        Creates the owner membership for a newly
        created organization.
        """

    @abstractmethod
    def get_user_memberships(
        self,
        user_id: UUID,
    ) -> list[OrganizationMembership]:
        """
        Returns every organization membership
        for a user.
        """

    @abstractmethod
    def has_access(
        self,
        organization_id: UUID,
        user_id: UUID,
    ) -> bool:
        """
        Returns whether the user has access
        to the organization.
        """

    @abstractmethod
    def ensure_organization_access(
        self,
        organization_id: UUID,
        user_id: UUID,
    ) -> None:
        """
        Raises an exception if the user is not a member
        of the organization.
        """