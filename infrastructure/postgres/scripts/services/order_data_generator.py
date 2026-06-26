import random
from datetime import datetime
from decimal import Decimal

from infrastructure.postgres.scripts.common.constants import ORDER_STATUSES
from infrastructure.postgres.scripts.models.order import Order


class OrderDataGenerator:

    def generate(self, customer_id: int) -> Order:

        return Order(
            customer_id=customer_id,
            status=random.choice(ORDER_STATUSES),
            total_amount=Decimal(
                round(
                    random.uniform(100, 50000),
                    2,
                )
            ),
            created_at=datetime.now(),
        )