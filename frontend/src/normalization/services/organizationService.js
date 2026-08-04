import axiosClient from "../../api/axiosClient";

const BASE_PATH = "/api/v1/organizations";

export async function listOrganizations() {
  const { data } = await axiosClient.get(BASE_PATH);
  return data;
}

export async function getOrganization(organizationId) {
  const { data } = await axiosClient.get(`${BASE_PATH}/${organizationId}`);
  return data;
}

export async function createOrganization(payload) {
  const { data } = await axiosClient.post(BASE_PATH, payload);
  return data;
}

export async function updateOrganization(organizationId, payload) {
  const { data } = await axiosClient.put(
    `${BASE_PATH}/${organizationId}`,
    payload
  );
  return data;
}

export async function deleteOrganization(organizationId) {
  await axiosClient.delete(`${BASE_PATH}/${organizationId}`);
}
