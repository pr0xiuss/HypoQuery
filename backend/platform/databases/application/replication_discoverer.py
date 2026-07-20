from abc import ABC
from abc import abstractmethod

import psycopg


class ReplicationDiscoverer(ABC):
    """
    Discovers PostgreSQL replication information.
    """

    @abstractmethod
    def discover(
        self,
        connection: psycopg.Connection,
    ) -> dict[str, int | bool]:
        """
        Returns replication information.
        """