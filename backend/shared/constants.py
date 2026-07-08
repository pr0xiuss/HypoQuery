HIGH_SHARED_READ_BLOCKS = 100

TEMP_WRITTEN_BLOCKS_THRESHOLD = 0

LARGE_SORT_COST = 1000.0

LARGE_NESTED_LOOP_ROWS = 10_000

LARGE_HASH_AGGREGATE_ROWS = 10_000

CARDINALITY_MISMATCH_FACTOR = 10.0

HIGH_COST_NODE_THRESHOLD = 10_000.0

DEEP_EXECUTION_PLAN_DEPTH = 10

LARGE_TABLE_SCAN_ROWS = 100_000

DEFAULT_BATCH_SIZE = 1000

CUSTOMER_COUNT = 1000

COUNTRY_DISTRIBUTION = {
    "India": 0.55,
    "United States": 0.15,
    "Germany": 0.10,
    "United Kingdom": 0.10,
    "Canada": 0.05,
    "Australia": 0.05,
}

CITY_MAPPING = {
    "India": [
        "Delhi",
        "Mumbai",
        "Bangalore",
        "Hyderabad",
        "Chennai",
    ],
    "United States": [
        "New York",
        "Chicago",
        "Austin",
        "Seattle",
        "Boston",
    ],
    "Germany": [
        "Berlin",
        "Munich",
        "Hamburg",
        "Frankfurt",
    ],
    "United Kingdom": [
        "London",
        "Manchester",
        "Liverpool",
        "Birmingham",
    ],
    "Canada": [
        "Toronto",
        "Vancouver",
        "Montreal",
    ],
    "Australia": [
        "Sydney",
        "Melbourne",
        "Brisbane",
    ],
}

FAKER_LOCALES = {
    "India": "en_IN",
    "United States": "en_US",
    "Germany": "de_DE",
    "United Kingdom": "en_GB",
    "Canada": "en_CA",
    "Australia": "en_AU",
}

PRODUCT_CATEGORIES = {
    "Electronics": {
        "brands": [
            "Apple",
            "Samsung",
            "Sony",
            "LG",
            "Dell",
        ],
        "products": [
            "Laptop",
            "Smartphone",
            "Monitor",
            "TV",
            "Headphones",
            "Keyboard",
            "Mouse",
        ],
    },
    "Fashion": {
        "brands": [
            "Nike",
            "Adidas",
            "Puma",
            "Levis",
        ],
        "products": [
            "Shoes",
            "Jacket",
            "T-Shirt",
            "Jeans",
            "Cap",
        ],
    },
    "Books": {
        "brands": [
            "Penguin",
            "OReilly",
            "Pearson",
        ],
        "products": [
            "Python Guide",
            "SQL Handbook",
            "Algorithms",
            "System Design",
        ],
    },
    "Furniture": {
        "brands": [
            "IKEA",
            "Urban Ladder",
            "Nilkamal",
        ],
        "products": [
            "Chair",
            "Table",
            "Desk",
            "Bookshelf",
        ],
    },
    "Groceries": {
        "brands": [
            "Nestle",
            "Amul",
            "Tata",
            "Britannia",
        ],
        "products": [
            "Coffee",
            "Milk",
            "Biscuits",
            "Rice",
        ],
    },
}

WAREHOUSES = [
    "Mumbai Warehouse",
    "Delhi Warehouse",
    "Bangalore Warehouse",
    "Hyderabad Warehouse",
    "Chennai Warehouse",
]

ORDER_STATUSES = [
    "PENDING",
    "PROCESSING",
    "SHIPPED",
    "DELIVERED",
    "CANCELLED",
]

REVIEW_TEMPLATES = [
    "Excellent product. Highly recommended.",
    "Good value for money.",
    "Average quality.",
    "Very satisfied with the purchase.",
    "Would definitely buy again.",
    "Packaging could have been better.",
    "Product arrived on time.",
    "Not worth the price.",
    "Exceeded my expectations.",
    "Works exactly as described.",
]

PRODUCT_EVENT_TYPES = [
    "PRODUCT_VIEWED",
    "PRODUCT_CLICKED",
    "PRODUCT_ADDED_TO_CART",
    "PRODUCT_REMOVED_FROM_CART",
    "PRODUCT_PURCHASED",
    "PRODUCT_WISHLISTED",
]
