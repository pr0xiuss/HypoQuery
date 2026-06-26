import random
from datetime import datetime

from faker import Faker

from infrastructure.postgres.scripts.common.constants import (
    CITY_MAPPING,
    COUNTRY_DISTRIBUTION,
    FAKER_LOCALES,
)
from infrastructure.postgres.scripts.models.customer import Customer


class CustomerDataGenerator:

    def __init__(self):
        self.fakers = {
            country: Faker(locale)
            for country, locale in FAKER_LOCALES.items()
        }

        self.countries = list(COUNTRY_DISTRIBUTION.keys())
        self.weights = list(COUNTRY_DISTRIBUTION.values())

    def generate(self) -> Customer:

        country = random.choices(
            self.countries,
            weights=self.weights,
            k=1,
        )[0]

        faker = self.fakers[country]

        first_name = faker.first_name()
        last_name = faker.last_name()

        email = (
            f"{first_name.lower()}."
            f"{last_name.lower()}"
            f"{random.randint(1000,9999)}@gmail.com"
        )

        city = random.choice(CITY_MAPPING[country])

        created_at = faker.date_time_between(
            start_date="-5y",
            end_date="now",
        )

        return Customer(
            first_name=first_name,
            last_name=last_name,
            email=email,
            city=city,
            country=country,
            created_at=created_at,
        )