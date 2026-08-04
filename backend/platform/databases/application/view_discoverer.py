from abc import ABC
from abc import abstractmethod
from backend.platform.databases.domain.db_view import DatabaseView
import psycopg
from uuid import UUID

class ViewDiscoverer(ABC):
    """
    Discovers database views.
    """

    @abstractmethod
    def discover(
        self,
        connection: psycopg.Connection,
        connection_id: UUID,
    ) -> list[DatabaseView]:
        """
        Returns user views.
        """