from uuid import uuid4

def test_create_organization_endpoint(
    client,
):
    """
    Organization creation endpoint exists.
    """

    response = client.post(
        "/api/v1/organizations",
        json={
            "name": "Acme",
        },
    )

    assert response.status_code in (
        200,
        201,
        401,
        403,
        409,
    )


def test_get_organization_endpoint(
    client,
):
    """
    Organization retrieval endpoint works.
    """

    create_response = client.post(
        "/api/v1/organizations",
        json={
            "name": f"Org-{uuid4().hex}",
        },
    )

    assert create_response.status_code == 201

    organization = create_response.json()

    organization_id = organization["id"]

    response = client.get(
        f"/api/v1/organizations/{organization_id}",
    )

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == organization_id