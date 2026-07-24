import api from "./api";

// NOTE: exact nesting not yet confirmed against the backend's finished
// Environments endpoints — adjust the base path below if it differs.
const basePath = (organizationId, projectId) =>
  `/api/v1/organizations/${organizationId}/projects/${projectId}/environments`;

export async function listEnvironments(organizationId, projectId) {
  const { data } = await api.get(basePath(organizationId, projectId));
  return data;
}

export async function getEnvironment(organizationId, projectId, environmentId) {
  const { data } = await api.get(
    `${basePath(organizationId, projectId)}/${environmentId}`
  );
  return data;
}

export async function createEnvironment(organizationId, projectId, payload) {
  const { data } = await api.post(basePath(organizationId, projectId), payload);
  return data;
}

export async function updateEnvironment(
  organizationId,
  projectId,
  environmentId,
  payload
) {
  const { data } = await api.put(
    `${basePath(organizationId, projectId)}/${environmentId}`,
    payload
  );
  return data;
}

export async function deleteEnvironment(organizationId, projectId, environmentId) {
  await api.delete(`${basePath(organizationId, projectId)}/${environmentId}`);
}
