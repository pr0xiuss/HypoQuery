import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  createProject,
  deleteProject,
  getProject,
  listProjects,
  updateProject,
} from "../services/projectService";

export function useProjects(organizationId) {
  return useQuery({
    queryKey: ["organizations", organizationId, "projects"],
    queryFn: () => listProjects(organizationId),
    enabled: Boolean(organizationId),
  });
}

export function useProject(organizationId, projectId) {
  return useQuery({
    queryKey: ["organizations", organizationId, "projects", projectId],
    queryFn: () => getProject(organizationId, projectId),
    enabled: Boolean(organizationId) && Boolean(projectId),
  });
}

export function useCreateProject(organizationId) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload) => createProject(organizationId, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["organizations", organizationId, "projects"],
      });
    },
  });
}

export function useUpdateProject(organizationId) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ projectId, payload }) =>
      updateProject(organizationId, projectId, payload),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({
        queryKey: ["organizations", organizationId, "projects"],
      });
      queryClient.invalidateQueries({
        queryKey: [
          "organizations",
          organizationId,
          "projects",
          variables.projectId,
        ],
      });
    },
  });
}

export function useDeleteProject(organizationId) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (projectId) => deleteProject(organizationId, projectId),
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["organizations", organizationId, "projects"],
      });
    },
  });
}