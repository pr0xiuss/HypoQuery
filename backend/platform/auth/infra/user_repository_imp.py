from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy import or_
from backend.platform.auth.domain.user import User
from backend.platform.auth.infra.user_model import UserModel
from backend.platform.auth.repositories.user_repository import UserRepository


class UserRepositoryImpl(UserRepository):
    """
    SQLAlchemy implementation of the user repository.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def save(
        self,
        user: User,
    ) -> User:
        model = UserModel(
            id=user.id,
            username=user.username,
            email=user.email,
            password_hash=user.password_hash,
            is_active=user.is_active,
            is_verified=user.is_verified,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

        try:
            merged_model = self._session.merge(model)
            self._session.commit()
            self._session.refresh(merged_model)

        except:
            self._session.rollback()
            raise
        return self._to_domain(merged_model)

    def get_by_id(
        self,
        user_id: UUID,
    ) -> User | None:
        model = self._session.get(
            UserModel,
            user_id,
        )

        if model is None:
            return None

        return self._to_domain(model)

    def get_by_email(
        self,
        email: str,
    ) -> User | None:
        statement = select(UserModel).where(
            UserModel.email == email,
        )

        model = self._session.scalar(statement)

        if model is None:
            return None

        return self._to_domain(model)

    def get_by_username(
        self,
        username: str,
    ) -> User | None:
        statement = select(UserModel).where(
            UserModel.username == username,
        )

        model = self._session.scalar(statement)

        if model is None:
            return None

        return self._to_domain(model)

    @staticmethod
    def _to_domain(
        model: UserModel,
    ) -> User:
        return User(
            id=model.id,
            username=model.username,
            email=model.email,
            password_hash=model.password_hash,
            is_active=model.is_active,
            is_verified=model.is_verified,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
    
    def get_by_identifier(
        self,
        identifier: str,
    ) -> User | None:
        statement = select(UserModel).where(
            or_(
                UserModel.email == identifier,
                UserModel.username == identifier,
            )
        )

        model = self._session.scalar(statement)

        if model is None:
            return None

        return self._to_domain(model)