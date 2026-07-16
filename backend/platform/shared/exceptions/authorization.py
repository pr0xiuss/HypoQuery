class AuthorizationError(Exception):
    """
    Base class for all authorization exceptions.
    """


class PermissionDeniedError(AuthorizationError):
    """
    Raised when a user lacks the required permission.
    """


class OrganizationAccessDeniedError(AuthorizationError):
    """
    Raised when a user attempts to access an organization
    they do not belong to.
    """


class ProjectAccessDeniedError(AuthorizationError):
    """
    Raised when a user attempts to access a project
    they do not have access to.
    """


class EnvironmentAccessDeniedError(AuthorizationError):
    """
    Raised when a user attempts to access an environment
    they do not have access to.
    """