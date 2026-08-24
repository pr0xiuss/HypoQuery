from backend.shared.db import get_connection
from infrastructure.postgres.scripts.workload.workload import Workload


def main():

    connection = get_connection()

    workload = Workload(connection)

    workload.execute()

    connection.close()


if __name__ == "__main__":
    main()
