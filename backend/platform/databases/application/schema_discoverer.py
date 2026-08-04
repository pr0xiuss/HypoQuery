from abc import ABC
from abc import abstractmethod
from backend.platform.databases.domain.db_schema import DatabaseSchema
import psycopg
from uuid import UUID


class SchemaDiscoverer(ABC):
    """
    Discovers database schemas.
    """

    @abstractmethod
    def discover(
        self,
        connection: psycopg.Connection,
        connection_id: UUID,
    ) -> list[DatabaseSchema]:
        """
        Returns the available schemas.
        """