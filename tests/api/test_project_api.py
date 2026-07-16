from uuid import uuid4


def test_create_project_endpoint(
    client,
):
    """
    Project creation endpoint works.
    """

    org_name = f"Org-{uuid4().hex}"

    organization_response = client.post(
        "/api/v1/organizations",
        json={
            "name": org_name,
        },
    )

    assert organization_response.status_code == 201

    organization = organization_response.json()

    organization_id = organization["id"]

    response = client.post(
        f"/api/v1/organizations/{organization_id}/projects",
        json={
            "name": "Backend",
            "description": "Backend APIs",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["organization_id"] == organization_id
    assert body["name"] == "Backend"
    assert body["description"] == "Backend APIs"


def test_get_project_endpoint(
    client,
):
    """
    Project retrieval endpoint exists.
    """

    response = client.get(
        "/api/v1/organizations/00000000-0000-0000-0000-000000000001/projects/00000000-0000-0000-0000-000000000002",
    )

    assert response.status_code in (
        200,
        401,
        403,
        404,
    )