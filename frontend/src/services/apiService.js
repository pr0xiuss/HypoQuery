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

function formatApiPayload(payload) {
  const formatted = {
    name: payload.name.trim(),
    framework: payload.framework,
    base_url: payload.base_url.trim(),
    is_active: payload.is_active !== undefined ? Boolean(payload.is_active) : true,
  };

  if (payload.description !== undefined) {
    formatted.description = payload.description?.trim() || null;
  }
  if (payload.version !== undefined) {
    formatted.version = payload.version?.trim() || null;
  }

  return formatted;
}

export async function createApi(organizationId, projectId, environmentId, payload) {
  const formattedPayload = formatApiPayload(payload);
  const { data } = await api.post(
    basePath(organizationId, projectId, environmentId),
    formattedPayload
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
  const formattedPayload = formatApiPayload(payload);
  const { data } = await api.put(
    `${basePath(organizationId, projectId, environmentId)}/${apiId}`,
    formattedPayload
  );
  return data;
}

export async function deleteApi(organizationId, projectId, environmentId, apiId) {
  await api.delete(`${basePath(organizationId, projectId, environmentId)}/${apiId}`);
}

export async function discoverApis(
  organizationId,
  projectId,
  environmentId,
  apiId,
  payload
) {
  const { data } = await api.post(
    `${basePath(organizationId, projectId, environmentId)}/${apiId}/discover`,
    payload
  );
  return data;
}

export async function listApiEndpoints(organizationId, projectId, environmentId, apiId) {
  const { data } = await api.get(
    `${basePath(organizationId, projectId, environmentId)}/${apiId}/endpoints`
  );
  return data;
}
