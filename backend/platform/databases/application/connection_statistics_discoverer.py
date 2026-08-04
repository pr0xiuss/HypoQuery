from abc import ABC
from abc import abstractmethod

import psycopg


class ConnectionStatisticsDiscoverer(ABC):
    """
    Discovers connection-level statistics.
    """

    @abstractmethod
    def discover(
        self,
        connection: psycopg.Connection,
    ) -> dict[str, int]:
        """
        Returns connection statistics.
        """