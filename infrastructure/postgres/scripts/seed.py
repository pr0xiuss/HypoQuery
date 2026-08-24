from backend.shared.db import get_connection

from backend.repositories.customer_repo import (
    CustomerRepository,
)
from backend.repositories.product_repo import (
    ProductRepository,
)

from infrastructure.postgres.scripts.seeders.customer_seeder import (
    CustomerSeeder,
)
from infrastructure.postgres.scripts.seeders.product_seeder import (
    ProductSeeder,
)
from infrastructure.postgres.scripts.seeders.inventory_seeder import InventorySeeder
from backend.repositories.inventory_repo import (
    InventoryRepository,
)
from infrastructure.postgres.scripts.seeders.order_seeder import OrderSeeder
from backend.repositories.order_repo import OrderRepository
from infrastructure.postgres.scripts.seeders.review_seeder import ReviewSeeder
from backend.repositories.review_repo import ReviewRepository
from infrastructure.postgres.scripts.seeders.product_event_seeder import (
    ProductEventSeeder,
)
from backend.repositories.product_event_repo import (
    ProductEventRepository,
)


def main():

    connection = get_connection()

    CustomerSeeder(CustomerRepository(connection)).run()
    ProductSeeder(ProductRepository(connection)).run()
    InventorySeeder(
        InventoryRepository(connection),
        ProductRepository(connection),
    ).run()
    OrderSeeder(
        OrderRepository(connection),
        CustomerRepository(connection),
    ).run()
    ReviewSeeder(
        ReviewRepository(connection),
        CustomerRepository(connection),
        ProductRepository(connection),
    ).run()
    ProductEventSeeder(
        ProductEventRepository(connection),
        ProductRepository(connection),
    ).run()

    connection.close()


if __name__ == "__main__":
    main()
