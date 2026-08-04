class ResourceError(Exception):
    """
    Base class for resource-related exceptions.
    """
    def __init__(
        self,
        resource: str,
        identifier: str,
    ) -> None:
        super().__init__(
            f"{resource} '{identifier}' was not found."
        )
        self.resource = resource
        self.identifier = identifier

class ResourceNotFoundError(ResourceError):
    """
    Raised when a requested resource cannot be found.
    """


class ResourceAlreadyExistsError(ResourceError):
    """
    Raised when attempting to create a duplicate resource.
    """