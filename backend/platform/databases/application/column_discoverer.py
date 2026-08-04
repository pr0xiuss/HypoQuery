from abc import ABC
from abc import abstractmethod
from uuid import UUID

import psycopg

from backend.platform.databases.domain.db_column import (
    DatabaseColumn,
)


class ColumnDiscoverer(ABC):
    """
    Discovers database columns.
    """

    @abstractmethod
    def discover(
        self,
        connection: psycopg.Connection,
        connection_id: UUID,
    ) -> list[DatabaseColumn]:
        """
        Discover all columns.
        """
        raise NotImplementedError