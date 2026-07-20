from abc import ABC
from abc import abstractmethod
from uuid import UUID

from backend.platform.databases.domain.db_connection import (
    DatabaseConnection,
)


class DatabaseConnectionRepository(ABC):
    """
    Repository for database connections.
    """

    @abstractmethod
    def save(
        self,
        connection: DatabaseConnection,
    ) -> DatabaseConnection:
        """
        Persists a database connection.
        """

    @abstractmethod
    def get_by_id(
        self,
        connection_id: UUID,
    ) -> DatabaseConnection | None:
        """
        Returns a database connection by id.
        """

    @abstractmethod
    def list_by_environment(
        self,
        environment_id: UUID,
    ) -> list[DatabaseConnection]:
        """
        Returns all database connections
        belonging to an environment.
        """

    @abstractmethod
    def delete(
        self,
        connection_id: UUID,
    ) -> None:
        """
        Deletes a database connection.
        """