from infrastructure.postgres.scripts.models.review import Review
from infrastructure.postgres.scripts.repositories.base_repo import BaseRepository


class ReviewRepository(BaseRepository):

    TABLE_NAME = "reviews"

    def insert_many(
        self,
        reviews: list[Review],
    ):

        query = """
        INSERT INTO reviews(
            customer_id,
            product_id,
            rating,
            review_text,
            created_at
        )
        VALUES (%s,%s,%s,%s,%s)
        """

        values = [
            (
                review.customer_id,
                review.product_id,
                review.rating,
                review.review_text,
                review.created_at,
            )
            for review in reviews
        ]

        with self.connection.cursor() as cursor:
            cursor.executemany(
                query,
                values,
            )