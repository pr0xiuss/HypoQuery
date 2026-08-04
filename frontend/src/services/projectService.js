import api from "./api";

// NOTE: exact nesting not yet confirmed against the backend's finished
// Projects endpoints — adjust the base path below if it differs.
const basePath = (organizationId) =>
  `/api/v1/organizations/${organizationId}/projects`;

export async function listProjects(organizationId) {
  const { data } = await api.get(basePath(organizationId));
  return data;
}

export async function getProject(organizationId, projectId) {
  const { data } = await api.get(`${basePath(organizationId)}/${projectId}`);
  return data;
}

export async function createProject(organizationId, payload) {
  const { data } = await api.post(basePath(organizationId), payload);
  return data;
}

export async function updateProject(organizationId, projectId, payload) {
  const { data } = await api.put(
    `${basePath(organizationId)}/${projectId}`,
    payload
  );
  return data;
}

export async function deleteProject(organizationId, projectId) {
  await api.delete(`${basePath(organizationId)}/${projectId}`);
}
