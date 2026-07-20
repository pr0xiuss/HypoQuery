from abc import ABC
from abc import abstractmethod

import psycopg


class DatabaseSettingsDiscoverer(ABC):
    """
    Discovers PostgreSQL database settings.
    """

    @abstractmethod
    def discover(
        self,
        connection: psycopg.Connection,
    ) -> dict[str, str]:
        """
        Returns PostgreSQL configuration settings.
        """