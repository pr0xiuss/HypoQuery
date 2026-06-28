import random
from decimal import Decimal
from datetime import datetime
from infrastructure.postgres.scripts.common.constants import PRODUCT_CATEGORIES
from infrastructure.postgres.scripts.models.product import Product


class ProductDataGenerator:

    def generate(self) -> Product:

        category = random.choice(list(PRODUCT_CATEGORIES.keys()))

        info = PRODUCT_CATEGORIES[category]

        brand = random.choice(info["brands"])

        item = random.choice(info["products"])

        name = f"{brand} {item}"

        price = Decimal(
            round(
                random.uniform(100, 100000),
                2,
            )
        )

        return Product(
            product_name=name,
            category=category,
            description=f"{brand} {item} from {category} category.",
            price=price,
            metadata={
                "brand": brand,
                "country": random.choice(
                    [
                        "India",
                        "USA",
                        "Germany",
                        "Japan",
                        "China",
                    ]
                ),
                "tier": random.choice(
                    [
                        "Premium",
                        "Standard",
                        "Budget",
                    ]
                ),
                "warranty": random.choice(
                    [
                        "1 Year",
                        "2 Years",
                        "3 Years",
                    ]
                ),
                "features": random.sample(
                    [
                        "Bluetooth",
                        "WiFi",
                        "5G",
                        "OLED",
                        "NFC",
                        "Fast Charging",
                        "Water Resistant",
                    ],
                    k=3,
                ),
            },
            created_at=datetime.now(),
        )
