from fastapi.testclient import TestClient


def test_delete_database_connection(
    client: TestClient,
    database_connection,
):
    response = client.delete(
        f"/api/v1/database-connections/{database_connection.id}",
    )

    assert response.status_code == 204

    response = client.get(
        f"/api/v1/database-connections/{database_connection.id}",
    )

    assert response.status_code == 404