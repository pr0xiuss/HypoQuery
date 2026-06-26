from infrastructure.postgres.scripts.common.exceptions import ValidationError
from infrastructure.postgres.scripts.repositories.inventory_repo import (
    InventoryRepository,
)
from infrastructure.postgres.scripts.repositories.product_repo import (
    ProductRepository,
)
from infrastructure.postgres.scripts.seeders.base_seeder import BaseSeeder
from infrastructure.postgres.scripts.services.inventory_data_generator import (
    InventoryDataGenerator,
)


class InventorySeeder(BaseSeeder):

    def __init__(
        self,
        repository: InventoryRepository,
        product_repository: ProductRepository,
    ):
        super().__init__(repository)

        self.generator = InventoryDataGenerator()
        self.product_repository = product_repository

    def generate(self):

        inventory = []

        product_ids = self.product_repository.get_all_product_ids()

        for product_id in product_ids:
            inventory.append(
                self.generator.generate(product_id)
            )

        return inventory

    def persist(self, inventory):

        self.repository.insert_many(
            inventory
        )

    def validate(self):

        expected = len(
            self.product_repository.get_all_product_ids()
        )

        actual = self.repository.count()

        if expected != actual:
            raise ValidationError(
                f"Expected {expected} inventory rows but found {actual}"
            )