import api from "./api";

export async function registerUser({ username, email, password }) {
  const { data } = await api.post("/api/v1/auth/register", {
    username,
    email,
    password,
  });
  return data;
}

export async function loginUser({ identifier, password }) {
  const { data } = await api.post("/api/v1/auth/login", {
    identifier,
    password,
  });
  return data;
}

export async function logoutUser() {
  await api.post("/api/v1/auth/logout");
}
