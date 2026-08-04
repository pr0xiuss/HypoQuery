from abc import ABC
from abc import abstractmethod

import psycopg


class IndexStatisticsDiscoverer(ABC):
    """
    Discovers index-level statistics.
    """

    @abstractmethod
    def discover(
        self,
        connection: psycopg.Connection,
    ) -> list[dict[str, int | str]]:
        """
        Returns index statistics.
        """