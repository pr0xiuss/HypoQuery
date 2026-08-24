from backend.shared.settings import CONFIG
from infrastructure.postgres.scripts.common.exceptions import ValidationError
from backend.repositories.product_repo import (
    ProductRepository,
)
from backend.seeders.base_seeder import BaseSeeder
from infrastructure.postgres.scripts.services.product_data_generator import (
    ProductDataGenerator,
)


class ProductSeeder(BaseSeeder):

    def __init__(
        self,
        repository: ProductRepository,
    ):
        super().__init__(repository)

        self.generator = ProductDataGenerator()

    def generate(self):

        products = []

        for _ in range(CONFIG.products):
            products.append(self.generator.generate())

        return products

    def persist(
        self,
        products,
    ):

        self.repository.insert_many(products)

    def validate(self):

        count = self.repository.count()

        if count != CONFIG.products:
            raise ValidationError(
                f"Expected {CONFIG.products} products but found {count}"
            )
