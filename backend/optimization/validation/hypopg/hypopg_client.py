from __future__ import annotations

from psycopg import Connection

from backend.optimization.validation.hypopg.hypothetical_index import (
    HypotheticalIndex,
)


class HypoPGClient:
    """
    Low-level client responsible only for communicating
    with the HypoPG extension.
    """

    def __init__(
        self,
        connection: Connection,
    ) -> None:

        self._connection = connection

    def create_index(
        self,
        statement: str,
    ) -> HypotheticalIndex:

        with self._connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT *
                FROM hypopg_create_index(%s);
                """,
                (
                    statement,
                ),
            )

            oid, name = cursor.fetchone()

        return HypotheticalIndex(
            oid=oid,
            name=name,
            definition=statement,
        )

    def reset(
        self,
    ) -> None:

        with self._connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT hypopg_reset();
                """
            )

    def extension_available(
        self,
    ) -> bool:

        with self._connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT EXISTS (
                    SELECT 1
                    FROM pg_extension
                    WHERE extname='hypopg'
                );
                """
            )

            return cursor.fetchone()[0]