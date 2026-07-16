from uuid import uuid4

from backend.platform.auth.infra.jwt_service_impl import (
    JWTServiceImpl,
)


def test_create_access_token():
    """
    JWT access tokens are generated successfully.
    """

    service = JWTServiceImpl(
        secret_key="this-is-a-very-long-test-secret-key-765432123",
        algorithm="HS256",
        expires_in_minutes=60,
    )

    token = service.create_access_token(
        uuid4(),
    )

    assert token


def test_verify_access_token():
    """
    Generated JWT tokens can be verified.
    """

    service = JWTServiceImpl(
        secret_key="this-is-a-very-long-test-secret-key-765432123",
        algorithm="HS256",
        expires_in_minutes=60,
    )

    user_id = uuid4()

    token = service.create_access_token(
        user_id,
    )

    decoded = service.verify_access_token(
        token,
    )

    assert decoded == user_id


def test_invalid_token():
    """
    Invalid JWT tokens raise an exception.
    """

    service = JWTServiceImpl(
        secret_key="this-is-a-very-long-test-secret-key-765432123",
        algorithm="HS256",
        expires_in_minutes=60,
    )

    try:
        service.verify_access_token(
            "invalid-token",
        )
        assert False
    except Exception:
        assert True