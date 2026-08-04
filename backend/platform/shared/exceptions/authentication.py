from backend.platform.shared.exceptions.resource import (
    ResourceAlreadyExistsError,
)

class AuthenticationError(Exception):
    """
    Base class for all authentication exceptions.
    """


class InvalidCredentialsError(AuthenticationError):
    """
    Raised when the supplied credentials are invalid.
    """


class UserAlreadyExistsError(ResourceAlreadyExistsError):
    """
    Raised when attempting to register an existing user.
    """


class UserNotVerifiedError(AuthenticationError):
    """
    Raised when the user has not verified their email.
    """


class AccountDisabledError(AuthenticationError):
    """
    Raised when the user account has been disabled.
    """