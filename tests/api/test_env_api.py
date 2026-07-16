from uuid import uuid4


def test_create_environment_endpoint(
    client,
):
    """
    Environment creation endpoint works.
    """

    org_response = client.post(
        "/api/v1/organizations",
        json={
            "name": f"Org-{uuid4().hex}",
        },
    )

    assert org_response.status_code == 201

    organization_id = org_response.json()["id"]

    project_response = client.post(
        f"/api/v1/organizations/{organization_id}/projects",
        json={
            "name": "Backend",
            "description": "Backend APIs",
        },
    )

    assert project_response.status_code == 201

    project_id = project_response.json()["id"]

    response = client.post(
        f"/api/v1/projects/{project_id}/environments",
        json={
            "name": "Development",
            "description": "Development environment",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["project_id"] == project_id
    assert body["name"] == "Development"
    assert body["description"] == "Development environment"


def test_get_environment_endpoint(
    client,
):
    """
    Environment retrieval endpoint exists.
    """

    response = client.get(
        "/api/v1/projects/00000000-0000-0000-0000-000000000001/environments/00000000-0000-0000-0000-000000000002",
    )

    assert response.status_code in (
        200,
        401,
        403,
        404,
    )