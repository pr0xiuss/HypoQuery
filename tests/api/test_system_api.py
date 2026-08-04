def test_system_endpoint(
    client,
):
    """
    System endpoint responds successfully.
    """

    response = client.get(
        "/api/v1/system",
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True