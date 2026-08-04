from fastapi.testclient import TestClient


def test_create_database_connection(
    client: TestClient,
    environment,
):
    response = client.post(
        f"/api/v1/environments/{environment.id}/database-connections",
        json={
            "name": "Local PostgreSQL",
            "host": "localhost",
            "port": 5432,
            "database_name": "postgres",
            "username": "postgres",
            "password": "pr0xy",
            "ssl_enabled": False,
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["environment_id"] == str(environment.id)
    assert body["name"] == "Local PostgreSQL"
    assert body["host"] == "localhost"