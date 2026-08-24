from backend.models.product import Product
from backend.repositories.base_repo import BaseRepository
from psycopg.types.json import Json


class ProductRepository(BaseRepository):

    TABLE_NAME: str = "products"

    def insert_many(
        self,
        products: list[Product],
    ) -> None:

        query = """
        INSERT INTO products(
            product_name,
            category,
            description,
            price,
            metadata,
            created_at
        )
        VALUES (%s,%s,%s,%s,%s,%s)
        """

        values = [
            (
                product.product_name,
                product.category,
                product.description,
                product.price,
                Json(product.metadata),
                product.created_at,
            )
            for product in products
        ]

        with self.connection.cursor() as cursor:
            cursor.executemany(
                query,
                values,
            )

    def get_all_product_ids(self) -> list[int]:

        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT product_id
                FROM products
                """)

            return [row[0] for row in cursor.fetchall()]
