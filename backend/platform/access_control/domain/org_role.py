from enum import Enum


class OrganizationRole(
    str,
    Enum,
):
    """
    Roles a user can hold within an organization.
    """

    OWNER = "OWNER"
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"
    VIEWER = "VIEWER"