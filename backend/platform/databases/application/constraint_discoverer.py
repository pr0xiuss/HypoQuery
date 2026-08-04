from abc import ABC
from abc import abstractmethod
from uuid import UUID

import psycopg

from backend.platform.databases.domain.db_constraint import (
    DatabaseConstraint,
)


class ConstraintDiscoverer(
    ABC,
):
    """
    Discovers database constraints.
    """

    @abstractmethod
    def discover(
        self,
        connection: psycopg.Connection,
        connection_id: UUID,
    ) -> list[DatabaseConstraint]:
        """
        Discover all constraints.
        """
        raise NotImplementedError