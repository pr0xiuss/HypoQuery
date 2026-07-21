from fastapi.testclient import TestClient


def test_refresh_database_metadata(
    client: TestClient,
    database_connection,
):
    response = client.post(
        f"/api/v1/database-connections/{database_connection.id}/refresh",
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Database metadata refreshed successfully."