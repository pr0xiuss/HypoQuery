from abc import ABC
from abc import abstractmethod
from uuid import UUID


class DatabaseSecretService(ABC):
    """
    Stores and retrieves encrypted database credentials.
    """

    @abstractmethod
    def create(
        self,
        password: str,
    ) -> UUID:
        """
        Stores a database password and returns its identifier.
        """

    @abstractmethod
    def get(
        self,
        secret_id: UUID,
    ) -> str:
        """
        Returns the decrypted password.
        """

    @abstractmethod
    def delete(
        self,
        secret_id: UUID,
    ) -> None:
        """
        Deletes a stored secret.
        """