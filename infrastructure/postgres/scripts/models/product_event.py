from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class ProductEvent:
    product_id: int
    event_type: str
    event_metadata: dict
    created_at: datetime
