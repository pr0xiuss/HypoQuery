from abc import ABC
from abc import abstractmethod

from backend.platform.databases.dto.create_db_connection_request import (
    CreateDatabaseConnectionRequest,
)


class DatabaseConnectionValidator(ABC):
    """
    Validates a database connection before it is registered.
    """

    @abstractmethod
    def validate(
        self,
        request: CreateDatabaseConnectionRequest,
    ) -> None:
        """
        Raises an exception if the database connection
        cannot be established.
        """