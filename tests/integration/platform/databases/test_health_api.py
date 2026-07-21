from fastapi.testclient import TestClient


def test_database_connection_health(
    client: TestClient,
    database_connection,
):
    response = client.get(
        f"/api/v1/database-connections/{database_connection.id}/health",
    )

    assert response.status_code == 200

    body = response.json()

    assert "healthy" in body