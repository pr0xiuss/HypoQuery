class ResourceError(Exception):
    """
    Base class for resource-related exceptions.
    """


class ResourceNotFoundError(ResourceError):
    """
    Raised when a requested resource cannot be found.
    """


class ResourceAlreadyExistsError(ResourceError):
    """
    Raised when attempting to create a duplicate resource.
    """