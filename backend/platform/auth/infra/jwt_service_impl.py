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

    ACCESS_TOKEN = "access"
    REFRESH_TOKEN = "refresh"

    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
        expires_in_minutes: int = 60,
        refresh_expires_in_days: int = 30,
    ) -> None:
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._expires_in_minutes = expires_in_minutes
        self._refresh_expires_in_days = refresh_expires_in_days

    def create_access_token(
        self,
        user_id: UUID,
    ) -> str:
        expires_at = datetime.now(UTC) + timedelta(
            minutes=self._expires_in_minutes,
        )

        payload = {
            "sub": str(user_id),
            "type": self.ACCESS_TOKEN,
            "exp": expires_at,
        }

        return jwt.encode(
            payload,
            self._secret_key,
            algorithm=self._algorithm,
        )

    def create_refresh_token(
        self,
        user_id: UUID,
    ) -> str:
        expires_at = datetime.now(UTC) + timedelta(
            days=self._refresh_expires_in_days,
        )

        payload = {
            "sub": str(user_id),
            "type": self.REFRESH_TOKEN,
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

        if payload.get("type") != self.ACCESS_TOKEN:
            raise jwt.InvalidTokenError(
                "Invalid access token.",
            )

        return UUID(
            payload["sub"],
        )

    def verify_refresh_token(
        self,
        token: str,
    ) -> UUID:
        payload = jwt.decode(
            token,
            self._secret_key,
            algorithms=[self._algorithm],
        )

        if payload.get("type") != self.REFRESH_TOKEN:
            raise jwt.InvalidTokenError(
                "Invalid refresh token.",
            )

        return UUID(
            payload["sub"],
        )

    def access_token_expires_in(
        self,
    ) -> int:
        """
        Returns the access token lifetime in seconds.
        """

        return self._expires_in_minutes * 60