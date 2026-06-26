from abc import ABC, abstractmethod

from psycopg import Connection


class BaseRepository(ABC):

    TABLE_NAME = ""

    def __init__(self, connection: Connection):
        self.connection = connection

    @abstractmethod
    def insert_many(self, data):
        pass

    def count(self) -> int:
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"SELECT COUNT(*) FROM {self.TABLE_NAME}"
            )
            return cursor.fetchone()[0]

    def truncate(self) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"TRUNCATE TABLE {self.TABLE_NAME} RESTART IDENTITY CASCADE"
            )