from abc import ABC
from abc import abstractmethod

import psycopg


class DatabaseStatisticsDiscoverer(ABC):
    """
    Discovers database-level statistics.
    """

    @abstractmethod
    def discover(
        self,
        connection: psycopg.Connection,
    ) -> dict[str, int]:
        """
        Returns database statistics.
        """