from abc import ABC
from abc import abstractmethod
from backend.platform.databases.domain.db_index import DatabaseIndex
import psycopg
from uuid import UUID


class IndexDiscoverer(ABC):
    """
    Discovers database indexes.
    """

    @abstractmethod
    def discover(
        self,
        connection: psycopg.Connection,
        connection_id: UUID,
    ) -> list[DatabaseIndex]:
        """
        Returns user-defined indexes.
        """