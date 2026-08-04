from abc import ABC
from abc import abstractmethod
from backend.platform.databases.domain.db_trigger import DatabaseTrigger
import psycopg
from uuid import UUID


class TriggerDiscoverer(ABC):
    """
    Discovers database triggers.
    """

    @abstractmethod
    def discover(
        self,
        connection: psycopg.Connection,
        connection_id: UUID,
    ) -> list[DatabaseTrigger]:
        """
        Returns user-defined triggers.
        """