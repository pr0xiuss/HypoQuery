from infrastructure.postgres.scripts.models.customer import Customer
from infrastructure.postgres.scripts.repositories.base_repo import (
    BaseRepository,
)


class CustomerRepository(BaseRepository):

    TABLE_NAME: str = "customers"

    def insert_many(self, customers: list[Customer]) -> None:

        query = """
        INSERT INTO customers (
            first_name,
            last_name,
            email,
            city,
            country,
            created_at
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = [
            (
                customer.first_name,
                customer.last_name,
                customer.email,
                customer.city,
                customer.country,
                customer.created_at,
            )
            for customer in customers
        ]

        with self.connection.cursor() as cursor:
            cursor.executemany(query, values)

    def get_all_customer_ids(self) -> list[int]:

        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT customer_id
                FROM customers
                """)

            return [row[0] for row in cursor.fetchall()]
