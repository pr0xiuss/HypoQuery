from psycopg import Connection

from infrastructure.postgres.scripts.models.customer import Customer


class CustomerRepository:

    def __init__(self, connection: Connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def insert_many(self, customers: list[Customer]) -> None:

        query = """
        INSERT INTO customers(
            first_name,
            last_name,
            email,
            city,
            country,
            created_at
        )
        VALUES (%s,%s,%s,%s,%s,%s)
        """

        values = [
            (
                c.first_name,
                c.last_name,
                c.email,
                c.city,
                c.country,
                c.created_at,
            )
            for c in customers
        ]

        self.cursor.executemany(query, values)

    def count(self):

        self.cursor.execute(
            "SELECT COUNT(*) FROM customers"
        )

        return self.cursor.fetchone()[0]