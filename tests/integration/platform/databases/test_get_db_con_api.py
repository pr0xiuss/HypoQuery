from fastapi.testclient import TestClient


def test_get_database_connection(
    client: TestClient,
    database_connection,
):
    response = client.get(
        f"/api/v1/database-connections/{database_connection.id}",
    )

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == str(database_connection.id)
    assert body["name"] == database_connection.name