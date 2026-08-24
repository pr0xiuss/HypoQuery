from backend.shared.settings import CONFIG
from infrastructure.postgres.scripts.common.exceptions import ValidationError
from backend.repositories.customer_repo import (
    CustomerRepository,
)
from backend.repositories.order_repo import (
    OrderRepository,
)
from backend.seeders.base_seeder import BaseSeeder
from infrastructure.postgres.scripts.services.order_data_generator import (
    OrderDataGenerator,
)


class OrderSeeder(BaseSeeder):

    def __init__(
        self,
        repository: OrderRepository,
        customer_repository: CustomerRepository,
    ):
        super().__init__(repository)

        self.customer_repository = customer_repository
        self.generator = OrderDataGenerator()

    def generate(self):

        orders = []

        customer_ids = self.customer_repository.get_all_customer_ids()

        while len(orders) < CONFIG.orders:

            customer = customer_ids[len(orders) % len(customer_ids)]

            orders.append(self.generator.generate(customer))

        return orders

    def persist(self, orders):

        self.repository.insert_many(orders)

    def validate(self):

        count = self.repository.count()

        if count != CONFIG.orders:
            raise ValidationError(f"Expected {CONFIG.orders} orders but found {count}")
