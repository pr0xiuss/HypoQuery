from infrastructure.postgres.scripts.common.db import get_connection
from infrastructure.postgres.scripts.repositories.customer_repo import (
    CustomerRepository,
)
from infrastructure.postgres.scripts.seeders.customer_seeder import (
    CustomerSeeder,
)


def main():

    connection = get_connection()

    repository = CustomerRepository(connection)

    seeder = CustomerSeeder(repository)

    seeder.run()

    connection.close()


if __name__ == "__main__":
    main()