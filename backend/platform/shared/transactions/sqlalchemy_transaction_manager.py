from sqlalchemy.orm import Session

from backend.platform.shared.transactions.transaction_manager import (
    TransactionManager,
)


class SQLAlchemyTransactionManager(
    TransactionManager,
):
    """
    SQLAlchemy implementation of the transaction
    manager.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def commit(
        self,
    ) -> None:
        self._session.commit()

    def rollback(
        self,
    ) -> None:
        self._session.rollback()

    def flush(
        self,
    ) -> None:
        self._session.flush()