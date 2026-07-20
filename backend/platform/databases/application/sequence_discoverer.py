from abc import ABC
from abc import abstractmethod

import psycopg


class SequenceDiscoverer(ABC):
    """
    Discovers database sequences.
    """

    @abstractmethod
    def discover(
        self,
        connection: psycopg.Connection,
    ) -> list[str]:
        """
        Returns user-defined sequences.
        """