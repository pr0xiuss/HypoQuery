from psycopg.types.json import Json

from infrastructure.postgres.scripts.models.product_event import ProductEvent
from infrastructure.postgres.scripts.repositories.base_repo import BaseRepository


class ProductEventRepository(BaseRepository):

    TABLE_NAME = "product_events"

    def insert_many(
        self,
        events: list[ProductEvent],
    ):

        query = """
        INSERT INTO product_events(
            product_id,
            event_type,
            event_metadata,
            created_at
        )
        VALUES (%s,%s,%s,%s)
        """

        values = [
            (
                event.product_id,
                event.event_type,
                Json(event.event_metadata),
                event.created_at,
            )
            for event in events
        ]

        with self.connection.cursor() as cursor:
            cursor.executemany(
                query,
                values,
            )
