from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime

@dataclass(slots=True)
class Product:
    product_name: str
    category: str
    description: str
    price: Decimal
    metadata: dict
    created_at: datetime