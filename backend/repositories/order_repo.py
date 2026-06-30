from infrastructure.postgres.scripts.models.order import Order
from infrastructure.postgres.scripts.repositories.base_repo import BaseRepository


class OrderRepository(BaseRepository):

    TABLE_NAME = "orders"

    def insert_many(
        self,
        orders: list[Order],
    ):

        query = """
        INSERT INTO orders(
            customer_id,
            status,
            total_amount,
            created_at
        )
        VALUES (%s,%s,%s,%s)
        """

        values = [
            (
                order.customer_id,
                order.status,
                order.total_amount,
                order.created_at,
            )
            for order in orders
        ]

        with self.connection.cursor() as cursor:
            cursor.executemany(
                query,
                values,
            )
