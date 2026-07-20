from unittest.mock import Mock

import jwt
import pytest

from backend.platform.auth.infra.jwt_service_impl import (
    JWTServiceImpl,
)
from tests.factorries import create_user


def create_jwt_service() -> JWTServiceImpl:
    """
    Creates a JWT service for testing.
    """

    settings = Mock()

    settings.jwt_secret = (
        "this-is-a-very-long-test-secret-key-765432123"
    )
    settings.jwt_algorithm = "HS256"

    return JWTServiceImpl(
        secret_key="this-is-a-very-long-test-secret-key-765432123",
        algorithm="HS256",
        expires_in_minutes=60,
    )


def test_create_access_token():
    """
    JWT access tokens are generated successfully.
    """

    service = create_jwt_service()

    user = create_user()

    token = service.create_access_token(
        user.id,
    )

    assert isinstance(
        token,
        str,
    )


def test_verify_access_token():
    """
    Generated access tokens can be verified.
    """

    service = create_jwt_service()

    user = create_user()

    token = service.create_access_token(
        user.id,
    )

    subject = service.verify_access_token(
        token,
    )

    assert subject == user.id


def test_invalid_token():
    """
    Invalid JWT tokens raise an exception.
    """

    service = create_jwt_service()

    with pytest.raises(
        jwt.InvalidTokenError,
    ):
        service.verify_access_token(
            "invalid-token",
        )


def test_create_refresh_token():
    """
    Refresh tokens are generated successfully.
    """

    service = create_jwt_service()

    user = create_user()

    token = service.create_refresh_token(
        user.id,
    )

    assert isinstance(
        token,
        str,
    )


def test_verify_refresh_token():
    """
    Refresh tokens can be verified.
    """

    service = create_jwt_service()

    user = create_user()

    token = service.create_refresh_token(
        user.id,
    )

    subject = service.verify_refresh_token(
        token,
    )

    assert subject == user.id


def test_access_token_cannot_be_used_as_refresh_token():
    """
    Access tokens cannot be verified as refresh tokens.
    """

    service = create_jwt_service()

    user = create_user()

    access_token = service.create_access_token(
        user.id,
    )

    with pytest.raises(
        jwt.InvalidTokenError,
    ):
        service.verify_refresh_token(
            access_token,
        )


def test_refresh_token_cannot_be_used_as_access_token():
    """
    Refresh tokens cannot be verified as access tokens.
    """

    service = create_jwt_service()

    user = create_user()

    refresh_token = service.create_refresh_token(
        user.id,
    )

    with pytest.raises(
        jwt.InvalidTokenError,
    ):
        service.verify_access_token(
            refresh_token,
        )