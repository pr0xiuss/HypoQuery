from infrastructure.postgres.scripts.models.inventory import Inventory
from infrastructure.postgres.scripts.repositories.base_repo import BaseRepository


class InventoryRepository(BaseRepository):

    TABLE_NAME = "inventory"

    def insert_many(
        self,
        inventory_items: list[Inventory],
    ):

        query = """
        INSERT INTO inventory(
            product_id,
            warehouse_name,
            stock_quantity,
            last_updated
        )
        VALUES (%s,%s,%s,%s)
        """

        values = [
            (
                item.product_id,
                item.warehouse_name,
                item.stock_quantity,
                item.last_updated,
            )
            for item in inventory_items
        ]

        with self.connection.cursor() as cursor:
            cursor.executemany(
                query,
                values,
            )
