class ValidationError(Exception):
    """
    Base class for business validation errors.
    """


class DuplicateResourceError(ValidationError):
    """
    Raised when a duplicate resource is detected.
    """


class InvalidStateError(ValidationError):
    """
    Raised when an operation is not valid for the current state.
    """


class BusinessRuleViolationError(ValidationError):
    """
    Raised when a business rule is violated.
    """