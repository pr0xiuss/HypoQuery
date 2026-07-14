from fastapi.testclient import TestClient


def test_root_endpoint_returns_success(
    client: TestClient,
) -> None:
    response = client.get("/api/v1/")

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert "data" in body
    assert "meta" in body
    assert "errors" in body


def test_root_endpoint_returns_application_information(
    client: TestClient,
) -> None:
    response = client.get("/api/v1/")

    body = response.json()

    assert body["data"]["name"] == "HypoQuery"
    assert "version" in body["data"]
    assert "environment" in body["data"]