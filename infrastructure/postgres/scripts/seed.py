from infrastructure.postgres.scripts.common.db import get_connection

from infrastructure.postgres.scripts.repositories.customer_repo import (
    CustomerRepository,
)
from infrastructure.postgres.scripts.repositories.product_repo import (
    ProductRepository,
)

from infrastructure.postgres.scripts.seeders.customer_seeder import (
    CustomerSeeder,
)
from infrastructure.postgres.scripts.seeders.product_seeder import (
    ProductSeeder,
)
from infrastructure.postgres.scripts.seeders.inventory_seeder import InventorySeeder
from infrastructure.postgres.scripts.repositories.inventory_repo import InventoryRepository
from infrastructure.postgres.scripts.seeders.order_seeder import OrderSeeder
from infrastructure.postgres.scripts.repositories.order_repo import OrderRepository
from infrastructure.postgres.scripts.seeders.review_seeder import ReviewSeeder
from infrastructure.postgres.scripts.repositories.review_repo import ReviewRepository
from infrastructure.postgres.scripts.seeders.product_event_seeder import ProductEventSeeder
from infrastructure.postgres.scripts.repositories.product_event_repo import ProductEventRepository

def main():

    connection = get_connection()

    CustomerSeeder(CustomerRepository(connection)).run()
    ProductSeeder(ProductRepository(connection)).run()
    InventorySeeder(InventoryRepository(connection),ProductRepository(connection),).run()
    OrderSeeder(OrderRepository(connection),CustomerRepository(connection),).run()
    ReviewSeeder(ReviewRepository(connection),CustomerRepository(connection),ProductRepository(connection)).run()
    ProductEventSeeder(ProductEventRepository(connection),ProductRepository(connection),).run()

    connection.close()


if __name__ == "__main__":
    main()