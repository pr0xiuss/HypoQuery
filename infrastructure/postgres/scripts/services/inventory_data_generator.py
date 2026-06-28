import random
from datetime import datetime

from infrastructure.postgres.scripts.common.constants import WAREHOUSES
from infrastructure.postgres.scripts.models.inventory import Inventory


class InventoryDataGenerator:

    def generate(self, product_id: int) -> Inventory:

        return Inventory(
            product_id=product_id,
            warehouse_name=random.choice(WAREHOUSES),
            stock_quantity=random.randint(0, 1000),
            last_updated=datetime.now(),
        )
