from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(slots=True)
class Order:
    customer_id: int
    status: str
    total_amount: Decimal
    created_at: datetime
