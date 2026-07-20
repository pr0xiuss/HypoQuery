from abc import ABC
from abc import abstractmethod

import psycopg


class ExtensionDiscoverer(ABC):
    """
    Discovers installed PostgreSQL extensions.
    """

    @abstractmethod
    def discover(
        self,
        connection: psycopg.Connection,
    ) -> list[str]:
        """
        Returns installed extensions.
        """