from abc import ABC

from psycopg import Connection


class BaseRepository(ABC):

    def __init__(
        self,
        connection: Connection,
    ):
        self.connection = connection
