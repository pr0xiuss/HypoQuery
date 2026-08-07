from abc import ABC
from abc import abstractmethod


class TransactionManager(
    ABC,
):
    """
    Coordinates database transactions across
    multiple repositories.
    """

    @abstractmethod
    def commit(
        self,
    ) -> None:
        """
        Commit the current transaction.
        """

    @abstractmethod
    def rollback(
        self,
    ) -> None:
        """
        Roll back the current transaction.
        """

    @abstractmethod
    def flush(
        self,
    ) -> None:
        """
        Flush pending changes.
        """