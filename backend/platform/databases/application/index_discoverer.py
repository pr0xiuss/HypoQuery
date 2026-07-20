from abc import ABC
from abc import abstractmethod

import psycopg


class IndexDiscoverer(ABC):
    """
    Discovers database indexes.
    """

    @abstractmethod
    def discover(
        self,
        connection: psycopg.Connection,
    ) -> list[str]:
        """
        Returns user-defined indexes.
        """