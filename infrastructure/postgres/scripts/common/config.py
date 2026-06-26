from dataclasses import dataclass

@dataclass(frozen=True)
class SeedConfig:
    customers: int = 1000
    products: int = 5000
    orders: int = 20000
    reviews: int = 10000
    inventory: int = 5000
    product_events: int = 50000


CONFIG = SeedConfig()