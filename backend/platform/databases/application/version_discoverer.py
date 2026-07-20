from abc import ABC
from abc import abstractmethod

import psycopg


class VersionDiscoverer(ABC):
    """
    Discovers PostgreSQL version information.
    """

    @abstractmethod
    def discover(
        self,
        connection: psycopg.Connection,
    ) -> str:
        """
        Returns the PostgreSQL server version.
        """