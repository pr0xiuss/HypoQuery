import random

from infrastructure.postgres.scripts.common.config import CONFIG
from infrastructure.postgres.scripts.common.exceptions import ValidationError
from infrastructure.postgres.scripts.repositories.product_event_repo import (
    ProductEventRepository,
)
from infrastructure.postgres.scripts.repositories.product_repo import (
    ProductRepository,
)
from infrastructure.postgres.scripts.seeders.base_seeder import BaseSeeder
from infrastructure.postgres.scripts.services.product_event_data_generator import (
    ProductEventDataGenerator,
)


class ProductEventSeeder(BaseSeeder):

    def __init__(
        self,
        repository: ProductEventRepository,
        product_repository: ProductRepository,
    ):
        super().__init__(repository)

        self.product_repository = product_repository
        self.generator = ProductEventDataGenerator()

    def generate(self):

        events = []

        product_ids = self.product_repository.get_all_product_ids()

        for _ in range(CONFIG.product_events):

            events.append(
                self.generator.generate(
                    random.choice(product_ids)
                )
            )

        return events

    def persist(self, events):

        self.repository.insert_many(events)

    def validate(self):

        count = self.repository.count()

        if count != CONFIG.product_events:
            raise ValidationError(
                f"Expected {CONFIG.product_events} events but found {count}"
            )