import random
from datetime import datetime

from infrastructure.postgres.scripts.common.constants import PRODUCT_EVENT_TYPES
from infrastructure.postgres.scripts.models.product_event import ProductEvent


class ProductEventDataGenerator:

    DEVICES = [
        "Desktop",
        "Mobile",
        "Tablet",
    ]

    BROWSERS = [
        "Chrome",
        "Firefox",
        "Edge",
        "Safari",
    ]

    def generate(self, product_id: int) -> ProductEvent:

        event_type = random.choice(PRODUCT_EVENT_TYPES)

        metadata = {
            "device": random.choice(self.DEVICES),
            "browser": random.choice(self.BROWSERS),
            "session_duration": random.randint(5, 1800),
            "country": random.choice(
                [
                    "India",
                    "USA",
                    "Germany",
                    "Canada",
                    "Australia",
                ]
            ),
        }

        return ProductEvent(
            product_id=product_id,
            event_type=event_type,
            event_metadata=metadata,
            created_at=datetime.now(),
        )