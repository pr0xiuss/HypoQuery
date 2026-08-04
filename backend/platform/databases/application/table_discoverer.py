from abc import ABC
from abc import abstractmethod
from backend.platform.databases.domain.db_table import DatabaseTable
import psycopg
from uuid import UUID


class TableDiscoverer(ABC):
    """
    Discovers database tables.
    """

    @abstractmethod
    def discover(
        self,
        connection: psycopg.Connection,
        connection_id: UUID,
    ) -> list[DatabaseTable]:
        """
        Discover all tables in the database.
        """
        raise NotImplementedError