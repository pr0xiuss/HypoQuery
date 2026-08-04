from abc import ABC
from abc import abstractmethod
from backend.platform.databases.domain.db_function import DatabaseFunction
import psycopg
from uuid import UUID


class FunctionDiscoverer(ABC):
    """
    Discovers database functions.
    """

    @abstractmethod
    def discover(
        self,
        connection: psycopg.Connection,
        connection_id: UUID,
    ) -> list[DatabaseFunction]:
        """
        Returns user-defined functions.
        """