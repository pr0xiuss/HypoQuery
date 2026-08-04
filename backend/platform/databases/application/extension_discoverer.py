from abc import ABC
from abc import abstractmethod
from backend.platform.databases.domain.db_extension import DatabaseExtension
import psycopg
from uuid import UUID


class ExtensionDiscoverer(ABC):
    """
    Discovers installed PostgreSQL extensions.
    """

    @abstractmethod
    def discover(
        self,
        connection: psycopg.Connection,
        connection_id: UUID,
    ) -> list[DatabaseExtension]:
        """
        Returns installed extensions.
        """