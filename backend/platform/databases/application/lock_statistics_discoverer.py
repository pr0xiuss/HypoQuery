from abc import ABC
from abc import abstractmethod

import psycopg


class LockStatisticsDiscoverer(ABC):
    """
    Discovers lock statistics.
    """

    @abstractmethod
    def discover(
        self,
        connection: psycopg.Connection,
    ) -> dict[str, int]:
        """
        Returns lock statistics.
        """