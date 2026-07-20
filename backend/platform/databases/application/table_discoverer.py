from abc import ABC
from abc import abstractmethod

import psycopg


class TableDiscoverer(ABC):
    """
    Discovers database tables.
    """

    @abstractmethod
    def discover(
        self,
        connection: psycopg.Connection,
    ) -> list[str]:
        """
        Discover all tables in the database.
        """
        raise NotImplementedError