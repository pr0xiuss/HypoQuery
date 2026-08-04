from abc import ABC
from abc import abstractmethod
from uuid import UUID
from backend.platform.databases.dto.update_db_connection_request import UpdateDatabaseConnectionRequest
from backend.platform.databases.dto.create_db_connection_request import CreateDatabaseConnectionRequest
from backend.platform.databases.dto.db_connection_response import DatabaseConnectionResponse
from backend.platform.databases.dto.db_health_result import DatabaseHealthResult
from backend.platform.databases.dto.db_overview_response import DatabaseOverviewResponse


class DatabaseConnectionService(ABC):
    """
    Application service responsible for
    database connection management.
    """

    @abstractmethod
    def create(
        self,
        environment_id: UUID,
        request: CreateDatabaseConnectionRequest,
    ) -> DatabaseConnectionResponse:
        """
        Registers a database connection.
        """

    @abstractmethod
    def get(
        self,
        connection_id: UUID,
    ) -> DatabaseConnectionResponse | None:
        """
        Returns a database connection.
        """

    @abstractmethod
    def list(
        self,
        environment_id: UUID,
    ) -> list[DatabaseConnectionResponse]:
        """
        Returns all connections
        for an environment.
        """

    @abstractmethod
    def delete(
        self,
        connection_id: UUID,
    ) -> None:
        """
        Deletes a database connection.
        """

    @abstractmethod
    def refresh_metadata(
        self,
        connection_id: UUID,
    ) -> None:
        raise NotImplementedError


    @abstractmethod
    def check_health(
        self,
        connection_id: UUID,
    ) -> DatabaseHealthResult:
        raise NotImplementedError

    @abstractmethod
    def update(
        self,
        connection_id: UUID,
        request: UpdateDatabaseConnectionRequest,
    ) -> DatabaseConnectionResponse:
        """
        Updates a database connection.
        """

    @abstractmethod
    def get_overview(
        self,
        connection_id: UUID,
    ) -> DatabaseOverviewResponse:
        pass