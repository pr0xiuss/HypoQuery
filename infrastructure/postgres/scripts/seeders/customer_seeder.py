from infrastructure.postgres.scripts.common.config import CONFIG
from infrastructure.postgres.scripts.common.exceptions import ValidationError
from infrastructure.postgres.scripts.repositories.customer_repo import (
    CustomerRepository,
)
from infrastructure.postgres.scripts.seeders.base_seeder import BaseSeeder
from infrastructure.postgres.scripts.services.customer_data_generator import (
    CustomerDataGenerator,
)


class CustomerSeeder(BaseSeeder):

    def __init__(self, repository: CustomerRepository):
        super().__init__(repository.connection)

        self.repository = repository
        self.generator = CustomerDataGenerator()

    def generate(self):

        customers = []

        for _ in range(CONFIG.customers):
            customers.append(
                self.generator.generate()
            )

        return customers

    def persist(self, customers):

        self.repository.insert_many(customers)

    def validate(self):

        count = self.repository.count()

        if count != CONFIG.customers:
            raise ValidationError(
                f"Expected {CONFIG.customers} customers but found {count}"
            )