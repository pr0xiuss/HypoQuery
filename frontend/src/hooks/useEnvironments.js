import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  createEnvironment,
  deleteEnvironment,
  getEnvironment,
  listEnvironments,
  updateEnvironment,
} from "../services/environmentService";

const listKey = (organizationId, projectId) => [
  "organizations",
  organizationId,
  "projects",
  projectId,
  "environments",
];

export function useEnvironments(organizationId, projectId) {
  return useQuery({
    queryKey: listKey(organizationId, projectId),
    queryFn: () => listEnvironments(organizationId, projectId),
    enabled: Boolean(organizationId) && Boolean(projectId),
  });
}

export function useEnvironment(organizationId, projectId, environmentId) {
  return useQuery({
    queryKey: [...listKey(organizationId, projectId), environmentId],
    queryFn: () => getEnvironment(organizationId, projectId, environmentId),
    enabled:
      Boolean(organizationId) && Boolean(projectId) && Boolean(environmentId),
  });
}

export function useCreateEnvironment(organizationId, projectId) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload) =>
      createEnvironment(organizationId, projectId, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: listKey(organizationId, projectId),
      });
    },
  });
}

export function useUpdateEnvironment(organizationId, projectId) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ environmentId, payload }) =>
      updateEnvironment(organizationId, projectId, environmentId, payload),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({
        queryKey: listKey(organizationId, projectId),
      });
      queryClient.invalidateQueries({
        queryKey: [...listKey(organizationId, projectId), variables.environmentId],
      });
    },
  });
}

export function useDeleteEnvironment(organizationId, projectId) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (environmentId) =>
      deleteEnvironment(organizationId, projectId, environmentId),
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: listKey(organizationId, projectId),
      });
    },
  });
}
