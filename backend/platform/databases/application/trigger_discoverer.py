from abc import ABC
from abc import abstractmethod

import psycopg


class TriggerDiscoverer(ABC):
    """
    Discovers database triggers.
    """

    @abstractmethod
    def discover(
        self,
        connection: psycopg.Connection,
    ) -> list[str]:
        """
        Returns user-defined triggers.
        """