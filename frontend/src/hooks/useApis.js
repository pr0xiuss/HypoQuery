import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  createApi,
  deleteApi,
  getApi,
  listApis,
  updateApi,
  discoverApis,
  listApiEndpoints,
} from "../services/apiService";

const listKey = (organizationId, projectId, environmentId) => [
  "organizations",
  organizationId,
  "projects",
  projectId,
  "environments",
  environmentId,
  "apis",
];

export function useApis(organizationId, projectId, environmentId) {
  return useQuery({
    queryKey: listKey(organizationId, projectId, environmentId),
    queryFn: () => listApis(organizationId, projectId, environmentId),
    enabled: Boolean(organizationId) && Boolean(projectId) && Boolean(environmentId),
  });
}

export function useApi(organizationId, projectId, environmentId, apiId) {
  return useQuery({
    queryKey: [...listKey(organizationId, projectId, environmentId), apiId],
    queryFn: () => getApi(organizationId, projectId, environmentId, apiId),
    enabled:
      Boolean(organizationId) &&
      Boolean(projectId) &&
      Boolean(environmentId) &&
      Boolean(apiId),
  });
}

export function useCreateApi(organizationId, projectId, environmentId) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload) => createApi(organizationId, projectId, environmentId, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: listKey(organizationId, projectId, environmentId),
      });
    },
  });
}

export function useUpdateApi(organizationId, projectId, environmentId) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ apiId, payload }) =>
      updateApi(organizationId, projectId, environmentId, apiId, payload),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({
        queryKey: listKey(organizationId, projectId, environmentId),
      });
      queryClient.invalidateQueries({
        queryKey: [...listKey(organizationId, projectId, environmentId), variables.apiId],
      });
    },
  });
}

export function useDeleteApi(organizationId, projectId, environmentId) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (apiId) => deleteApi(organizationId, projectId, environmentId, apiId),
    onSuccess: (_data, apiId) => {
      queryClient.invalidateQueries({
        queryKey: listKey(organizationId, projectId, environmentId),
      });
      queryClient.removeQueries({
        queryKey: [...listKey(organizationId, projectId, environmentId), apiId],
      });
    },
  });
}

export function useApiEndpoints(organizationId, projectId, environmentId, apiId) {
  return useQuery({
    queryKey: [...listKey(organizationId, projectId, environmentId), apiId, "endpoints"],
    queryFn: () => listApiEndpoints(organizationId, projectId, environmentId, apiId),
    enabled:
      Boolean(organizationId) &&
      Boolean(projectId) &&
      Boolean(environmentId) &&
      Boolean(apiId),
  });
}

export function useDiscoverApis(organizationId, projectId, environmentId) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ apiId, payload }) =>
      discoverApis(organizationId, projectId, environmentId, apiId, payload),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({
        queryKey: [...listKey(organizationId, projectId, environmentId), variables.apiId],
      });
      queryClient.invalidateQueries({
        queryKey: [...listKey(organizationId, projectId, environmentId), variables.apiId, "endpoints"],
      });
    },
  });
}
