def test_root_endpoint(
    client,
):
    """
    Root endpoint responds successfully.
    """

    response = client.get("/api/v1")

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True