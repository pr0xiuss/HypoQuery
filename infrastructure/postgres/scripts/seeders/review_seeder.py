import random

from infrastructure.postgres.scripts.common.config import CONFIG
from infrastructure.postgres.scripts.common.exceptions import ValidationError
from infrastructure.postgres.scripts.repositories.customer_repo import CustomerRepository
from infrastructure.postgres.scripts.repositories.product_repo import ProductRepository
from infrastructure.postgres.scripts.repositories.review_repo import ReviewRepository
from infrastructure.postgres.scripts.seeders.base_seeder import BaseSeeder
from infrastructure.postgres.scripts.services.review_data_generator import (
    ReviewDataGenerator,
)


class ReviewSeeder(BaseSeeder):

    def __init__(
        self,
        repository: ReviewRepository,
        customer_repository: CustomerRepository,
        product_repository: ProductRepository,
    ):
        super().__init__(repository)

        self.customer_repository = customer_repository
        self.product_repository = product_repository
        self.generator = ReviewDataGenerator()

    def generate(self):

        reviews = []

        customer_ids = self.customer_repository.get_all_customer_ids()
        product_ids = self.product_repository.get_all_product_ids()

        for _ in range(CONFIG.reviews):

            reviews.append(
                self.generator.generate(
                    random.choice(customer_ids),
                    random.choice(product_ids),
                )
            )

        return reviews

    def persist(self, reviews):

        self.repository.insert_many(
            reviews
        )

    def validate(self):

        count = self.repository.count()

        if count != CONFIG.reviews:
            raise ValidationError(
                f"Expected {CONFIG.reviews} reviews but found {count}"
            )