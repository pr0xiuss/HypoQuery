from abc import ABC
from abc import abstractmethod

import psycopg


class SchemaDiscoverer(ABC):
    """
    Discovers database schemas.
    """

    @abstractmethod
    def discover(
        self,
        connection: psycopg.Connection,
    ) -> list[str]:
        """
        Returns the available schemas.
        """