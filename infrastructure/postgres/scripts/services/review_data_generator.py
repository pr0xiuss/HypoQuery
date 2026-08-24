import random
from datetime import datetime

from infrastructure.postgres.scripts.common.constants import REVIEW_TEMPLATES
from backend.models.review import Review


class ReviewDataGenerator:

    def generate(
        self,
        customer_id: int,
        product_id: int,
    ) -> Review:

        return Review(
            customer_id=customer_id,
            product_id=product_id,
            rating=random.choices(
                [1, 2, 3, 4, 5],
                weights=[5, 10, 20, 35, 30],
                k=1,
            )[0],
            review_text=random.choice(REVIEW_TEMPLATES),
            created_at=datetime.now(),
        )
