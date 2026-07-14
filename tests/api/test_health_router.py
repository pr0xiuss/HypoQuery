from fastapi.testclient import TestClient


def test_health_endpoint(
    client: TestClient,
) -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["data"]["status"] == "healthy"


def test_live_endpoint(
    client: TestClient,
) -> None:
    response = client.get("/api/v1/live")

    assert response.status_code == 200

    body = response.json()

    assert body["data"]["status"] == "alive"


def test_ready_endpoint(
    client: TestClient,
) -> None:
    response = client.get("/api/v1/ready")

    assert response.status_code == 200

    body = response.json()

    assert body["data"]["status"] == "ready"