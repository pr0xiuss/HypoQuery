from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Review:
    customer_id: int
    product_id: int
    rating: int
    review_text: str
    created_at: datetime