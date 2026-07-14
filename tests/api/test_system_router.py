from fastapi.testclient import TestClient


def test_system_endpoint_returns_application_information(
    client: TestClient,
) -> None:
    response = client.get("/api/v1/system")

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True

    data = body["data"]

    assert data["application"] == "HypoQuery"
    assert "version" in data
    assert "environment" in data
    assert "request_id" in data


def test_system_endpoint_returns_request_id_header(
    client: TestClient,
) -> None:
    response = client.get("/api/v1/system")

    assert "X-Request-ID" in response.headers