from abc import ABC
from abc import abstractmethod

import psycopg


class ViewDiscoverer(ABC):
    """
    Discovers database views.
    """

    @abstractmethod
    def discover(
        self,
        connection: psycopg.Connection,
    ) -> list[str]:
        """
        Returns user views.
        """