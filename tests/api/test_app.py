from fastapi.testclient import TestClient


def test_openapi_document_exists(
    client: TestClient,
) -> None:
    response = client.get("/openapi.json")

    assert response.status_code == 200


def test_swagger_ui_exists(
    client: TestClient,
) -> None:
    response = client.get("/docs")

    assert response.status_code == 200


def test_redoc_exists(
    client: TestClient,
) -> None:
    response = client.get("/redoc")

    assert response.status_code == 200