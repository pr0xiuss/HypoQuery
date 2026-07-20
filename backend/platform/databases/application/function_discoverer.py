from abc import ABC
from abc import abstractmethod

import psycopg


class FunctionDiscoverer(ABC):
    """
    Discovers database functions.
    """

    @abstractmethod
    def discover(
        self,
        connection: psycopg.Connection,
    ) -> list[str]:
        """
        Returns user-defined functions.
        """