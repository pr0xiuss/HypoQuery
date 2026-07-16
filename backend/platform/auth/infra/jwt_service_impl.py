from datetime import UTC
from datetime import datetime
from datetime import timedelta
from uuid import UUID

import jwt

from backend.platform.auth.application.jwt_service import JWTService


class JWTServiceImpl(JWTService):
    """
    Default JWT implementation.
    """

    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
        expires_in_minutes: int = 60,
    ) -> None:
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._expires_in_minutes = expires_in_minutes

    def create_access_token(
        self,
        user_id: UUID,
    ) -> str:
        expires_at = datetime.now(UTC) + timedelta(
            minutes=self._expires_in_minutes,
        )

        payload = {
            "sub": str(user_id),
            "exp": expires_at,
        }

        return jwt.encode(
            payload,
            self._secret_key,
            algorithm=self._algorithm,
        )

    def verify_access_token(
        self,
        token: str,
    ) -> UUID:
        payload = jwt.decode(
            token,
            self._secret_key,
            algorithms=[self._algorithm],
        )

        return UUID(
            payload["sub"],
    )