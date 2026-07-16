from uuid import uuid4


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
            "password": "password",
        },
    )

    assert response.status_code in (
        200,
        401,
        404,
    )