import api from "./api";

const basePath = (organizationId, projectId, environmentId) =>
  `/api/v1/organizations/${organizationId}/projects/${projectId}/environments/${environmentId}/apis`;

export async function listApis(organizationId, projectId, environmentId) {
  const { data } = await api.get(basePath(organizationId, projectId, environmentId));
  return data;
}

export async function getApi(organizationId, projectId, environmentId, apiId) {
  const { data } = await api.get(
    `${basePath(organizationId, projectId, environmentId)}/${apiId}`
  );
  return data;
}

export async function createApi(organizationId, projectId, environmentId, payload) {
  const { data } = await api.post(
    basePath(organizationId, projectId, environmentId),
    payload
  );
  return data;
}

export async function updateApi(
  organizationId,
  projectId,
  environmentId,
  apiId,
  payload
) {
  const { data } = await api.put(
    `${basePath(organizationId, projectId, environmentId)}/${apiId}`,
    payload
  );
  return data;
}

export async function deleteApi(organizationId, projectId, environmentId, apiId) {
  await api.delete(`${basePath(organizationId, projectId, environmentId)}/${apiId}`);
}
