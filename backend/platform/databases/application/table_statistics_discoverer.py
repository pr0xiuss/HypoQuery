from abc import ABC
from abc import abstractmethod

import psycopg


class TableStatisticsDiscoverer(ABC):
    """
    Discovers table-level statistics.
    """

    @abstractmethod
    def discover(
        self,
        connection: psycopg.Connection,
    ) -> list[dict[str, int | str]]:
        """
        Returns table statistics.
        """