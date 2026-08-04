from uuid import UUID
from uuid import uuid4

import psycopg

from backend.platform.databases.application.constraint_discoverer import (
    ConstraintDiscoverer,
)
from backend.platform.databases.domain.db_constraint import (
    DatabaseConstraint,
)


class PostgresConstraintDiscoverer(
    ConstraintDiscoverer,
):
    """
    PostgreSQL implementation of constraint discovery.
    """

    def discover(
        self,
        connection: psycopg.Connection,
        connection_id: UUID,
    ) -> list[DatabaseConstraint]:

        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT
                    table_schema,
                    table_name,
                    constraint_name,
                    constraint_type
                FROM information_schema.table_constraints
                WHERE table_schema NOT IN (
                    'pg_catalog',
                    'information_schema'
                )
                ORDER BY
                    table_schema,
                    table_name,
                    constraint_name;
                """
            )

            rows = cursor.fetchall()
            print("ROws:- ",rows)
            constraints = [
                DatabaseConstraint(
                    id=uuid4(),
                    connection_id=connection_id,
                    schema_name=row[0],
                    table_name=row[1],
                    name=row[2],
                    constraint_type=row[3],
                )
                for row in rows
            ]

            constraints = [
                c
                for c in constraints
                if not (
                    c.constraint_type == "CHECK"
                    and c.name.startswith("2200_")
                    and c.name.endswith("_not_null")
                )
            ]

            return constraints