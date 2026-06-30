from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Inventory:
    product_id: int
    warehouse_name: str
    stock_quantity: int
    last_updated: datetime
