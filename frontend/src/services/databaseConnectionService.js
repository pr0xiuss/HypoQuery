import api from "./api";

const basePath = (organizationId, projectId, environmentId) =>
  `/api/v1/organizations/${organizationId}/projects/${projectId}/environments/${environmentId}/database-connections`;

export async function listDatabaseConnections(organizationId, projectId, environmentId) {
  const { data } = await api.get(basePath(organizationId, projectId, environmentId));
  return data;
}

export async function getDatabaseConnection(
  organizationId,
  projectId,
  environmentId,
  connectionId
) {
  const { data } = await api.get(
    `${basePath(organizationId, projectId, environmentId)}/${connectionId}`
  );
  return data;
}

export async function createDatabaseConnection(
  organizationId,
  projectId,
  environmentId,
  payload
) {
  const { data } = await api.post(
    basePath(organizationId, projectId, environmentId),
    payload
  );
  return data;
}

export async function updateDatabaseConnection(
  organizationId,
  projectId,
  environmentId,
  connectionId,
  payload
) {
  const { data } = await api.put(
    `${basePath(organizationId, projectId, environmentId)}/${connectionId}`,
    payload
  );
  return data;
}

export async function deleteDatabaseConnection(
  organizationId,
  projectId,
  environmentId,
  connectionId
) {
  await api.delete(
    `${basePath(organizationId, projectId, environmentId)}/${connectionId}`
  );
}

export async function getDatabaseConnectionOverview(
  organizationId,
  projectId,
  environmentId,
  connectionId
) {
  const { data } = await api.get(
    `${basePath(organizationId, projectId, environmentId)}/${connectionId}/overview`
  );
  return data;
}

export async function refreshDatabaseConnectionMetadata(
  organizationId,
  projectId,
  environmentId,
  connectionId
) {
  const { data } = await api.post(
    `${basePath(organizationId, projectId, environmentId)}/${connectionId}/refresh`
  );
  return data;
}

export async function getDatabaseConnectionHealth(
  organizationId,
  projectId,
  environmentId,
  connectionId
) {
  const { data } = await api.get(
    `${basePath(organizationId, projectId, environmentId)}/${connectionId}/health`
  );
  return data;
}

// --- Explorer ---

export async function getSchemas(organizationId, projectId, environmentId, connectionId) {
  const { data } = await api.get(
    `${basePath(organizationId, projectId, environmentId)}/${connectionId}/schemas`
  );
  return data;
}

export async function getTables(organizationId, projectId, environmentId, connectionId) {
  const { data } = await api.get(
    `${basePath(organizationId, projectId, environmentId)}/${connectionId}/tables`
  );
  return data;
}

export async function getTable(
  organizationId,
  projectId,
  environmentId,
  connectionId,
  schemaName,
  tableName
) {
  const { data } = await api.get(
    `${basePath(organizationId, projectId, environmentId)}/${connectionId}/tables/${schemaName}/${tableName}`
  );
  return data;
}

export async function getViews(organizationId, projectId, environmentId, connectionId) {
  const { data } = await api.get(
    `${basePath(organizationId, projectId, environmentId)}/${connectionId}/views`
  );
  return data;
}

export async function getFunctions(organizationId, projectId, environmentId, connectionId) {
  const { data } = await api.get(
    `${basePath(organizationId, projectId, environmentId)}/${connectionId}/functions`
  );
  return data;
}

export async function getIndexes(organizationId, projectId, environmentId, connectionId) {
  const { data } = await api.get(
    `${basePath(organizationId, projectId, environmentId)}/${connectionId}/indexes`
  );
  return data;
}

export async function getTriggers(organizationId, projectId, environmentId, connectionId) {
  const { data } = await api.get(
    `${basePath(organizationId, projectId, environmentId)}/${connectionId}/triggers`
  );
  return data;
}

export async function getSequences(organizationId, projectId, environmentId, connectionId) {
  const { data } = await api.get(
    `${basePath(organizationId, projectId, environmentId)}/${connectionId}/sequences`
  );
  return data;
}

export async function getExtensions(organizationId, projectId, environmentId, connectionId) {
  const { data } = await api.get(
    `${basePath(organizationId, projectId, environmentId)}/${connectionId}/extensions`
  );
  return data;
}