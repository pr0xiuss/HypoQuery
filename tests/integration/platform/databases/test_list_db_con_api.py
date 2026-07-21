from fastapi.testclient import TestClient


def test_list_database_connections(
    client: TestClient,
    database_connection,
):
    response = client.get(
        f"/api/v1/environments/{database_connection.environment_id}/database-connections",
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body) >= 1

    assert any(
        connection["id"] == str(database_connection.id)
        for connection in body
    )