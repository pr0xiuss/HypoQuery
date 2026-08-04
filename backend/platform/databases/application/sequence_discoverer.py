from abc import ABC
from abc import abstractmethod
from backend.platform.databases.domain.db_sequence import DatabaseSequence
import psycopg
from uuid import UUID


class SequenceDiscoverer(ABC):
    """
    Discovers database sequences.
    """

    @abstractmethod
    def discover(
        self,
        connection: psycopg.Connection,
        connection_id: UUID,
    ) -> list[DatabaseSequence]:
        """
        Returns user-defined sequences.
        """