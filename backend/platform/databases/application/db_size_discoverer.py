from abc import ABC
from abc import abstractmethod

import psycopg


class DatabaseSizeDiscoverer(ABC):
    """
    Discovers database size information.
    """

    @abstractmethod
    def discover(
        self,
        connection: psycopg.Connection,
    ) -> int:
        """
        Returns the database size in bytes.
        """