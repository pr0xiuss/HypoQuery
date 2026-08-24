import api from "./api";

export async function getDashboard() {
  const { data } = await api.get("/api/v1/dashboard");
  return data;
}

export async function getWorkloads(limit = 100, offset = 0) {
  const { data } = await api.get(`/api/v1/workloads?limit=${limit}&offset=${offset}`);
  return data;
}

export async function getQueries(fingerprintId, limit = 100, offset = 0) {
  const url = fingerprintId 
    ? `/api/v1/queries?fingerprint_id=${encodeURIComponent(fingerprintId)}&limit=${limit}&offset=${offset}` 
    : `/api/v1/queries?limit=${limit}&offset=${offset}`;
  const { data } = await api.get(url);
  return data;
}

export async function getQueryDetail(queryId) {
  const { data } = await api.get(`/api/v1/queries/${queryId}`);
  return data;
}

export async function getOperations(limit = 100, offset = 0) {
  const { data } = await api.get(`/api/v1/operations?limit=${limit}&offset=${offset}`);
  return data;
}

export async function getOperationDetail(operationId) {
  const { data } = await api.get(`/api/v1/operations/${operationId}`);
  return data;
}
