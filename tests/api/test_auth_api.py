from uuid import uuid4
from backend.platform.auth.infra.jwt_service_impl import JWTServiceImpl

def test_register_endpoint_exists(
    client,
):
    """
    Register endpoint is available.
    """

    uid = uuid4().hex

    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": f"user_{uid}",
            "email": f"{uid}@example.com",
            "password": "super-secret-password",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["username"] == f"user_{uid}"
    assert body["email"] == f"{uid}@example.com"


def test_login_endpoint_exists(
    client,
):
    """
    Login endpoint is available.
    """

    response = client.post(
        "/api/v1/auth/login",
        json={
            "identifier": "john",
            "password": "super-secret-password",
        },
    )

    assert response.status_code in (
        200,
        400,
        401,
    )

    if response.status_code == 200:
        body = response.json()

        assert "access_token" in body
        assert "refresh_token" in body
        assert "expires_in" in body
        assert body["token_type"] == "Bearer"

    
def test_refresh_endpoint_exists(
    client,
):
    """
    Refresh endpoint is available.
    """

    jwt_service = JWTServiceImpl(
        secret_key="this-is-a-very-long-test-secret-key-765432123",
        algorithm="HS256",
        expires_in_minutes=60,
    )

    refresh_token = jwt_service.create_refresh_token(
        uuid4(),
    )

    response = client.post(
        "/api/v1/auth/refresh",
        json={
            "refresh_token": refresh_token,
        },
    )

    assert response.status_code in (
        200,
        401,
    )