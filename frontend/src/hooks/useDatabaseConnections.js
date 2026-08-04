import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  createDatabaseConnection,
  deleteDatabaseConnection,
  getDatabaseConnection,
  getDatabaseConnectionHealth,
  getDatabaseConnectionOverview,
  getExtensions,
  getFunctions,
  getIndexes,
  getSchemas,
  getSequences,
  getTable,
  getTables,
  getTriggers,
  getViews,
  listDatabaseConnections,
  refreshDatabaseConnectionMetadata,
  updateDatabaseConnection,
} from "../services/databaseConnectionService";

const listKey = (organizationId, projectId, environmentId) => [
  "organizations",
  organizationId,
  "projects",
  projectId,
  "environments",
  environmentId,
  "database-connections",
];

export function useDatabaseConnections(organizationId, projectId, environmentId) {
  return useQuery({
    queryKey: listKey(organizationId, projectId, environmentId),
    queryFn: () => listDatabaseConnections(organizationId, projectId, environmentId),
    enabled: Boolean(organizationId) && Boolean(projectId) && Boolean(environmentId),
  });
}

export function useDatabaseConnection(
  organizationId,
  projectId,
  environmentId,
  connectionId
) {
  return useQuery({
    queryKey: [...listKey(organizationId, projectId, environmentId), connectionId],
    queryFn: () =>
      getDatabaseConnection(organizationId, projectId, environmentId, connectionId),
    enabled:
      Boolean(organizationId) &&
      Boolean(projectId) &&
      Boolean(environmentId) &&
      Boolean(connectionId),
  });
}

export function useCreateDatabaseConnection(organizationId, projectId, environmentId) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload) =>
      createDatabaseConnection(organizationId, projectId, environmentId, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: listKey(organizationId, projectId, environmentId),
      });
    },
  });
}

export function useUpdateDatabaseConnection(organizationId, projectId, environmentId) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ connectionId, payload }) =>
      updateDatabaseConnection(
        organizationId,
        projectId,
        environmentId,
        connectionId,
        payload
      ),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({
        queryKey: listKey(organizationId, projectId, environmentId),
      });
      queryClient.invalidateQueries({
        queryKey: [
          ...listKey(organizationId, projectId, environmentId),
          variables.connectionId,
        ],
      });
    },
  });
}

export function useDeleteDatabaseConnection(organizationId, projectId, environmentId) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (connectionId) =>
      deleteDatabaseConnection(organizationId, projectId, environmentId, connectionId),
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: listKey(organizationId, projectId, environmentId),
      });
    },
  });
}

const overviewKey = (organizationId, projectId, environmentId, connectionId) => [
  ...listKey(organizationId, projectId, environmentId),
  connectionId,
  "overview",
];

/** Reads the stored metadata snapshot only — never triggers discovery itself. */
export function useDatabaseConnectionOverview(
  organizationId,
  projectId,
  environmentId,
  connectionId
) {
  return useQuery({
    queryKey: overviewKey(organizationId, projectId, environmentId, connectionId),
    queryFn: () =>
      getDatabaseConnectionOverview(organizationId, projectId, environmentId, connectionId),
    enabled:
      Boolean(organizationId) &&
      Boolean(projectId) &&
      Boolean(environmentId) &&
      Boolean(connectionId),
    retry: (failureCount, error) =>
      error?.response?.status !== 404 && failureCount < 2,
  });
}

const connectionKey = (organizationId, projectId, environmentId, connectionId) => [
  ...listKey(organizationId, projectId, environmentId),
  connectionId,
];

export function useRefreshDatabaseConnectionMetadata(
  organizationId,
  projectId,
  environmentId
) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (connectionId) =>
      refreshDatabaseConnectionMetadata(organizationId, projectId, environmentId, connectionId),
    onSuccess: (_data, connectionId) => {
      // Invalidates overview, health, and every Explorer resource in one
      // shot — they all share this same [..., connectionId] key prefix.
      queryClient.invalidateQueries({
        queryKey: connectionKey(organizationId, projectId, environmentId, connectionId),
      });
    },
  });
}

/**
 * On-demand health check — starts disabled; call refetch() from a button
 * rather than fetching automatically on mount.
 */
export function useDatabaseConnectionHealth(
  organizationId,
  projectId,
  environmentId,
  connectionId
) {
  return useQuery({
    queryKey: [
      ...listKey(organizationId, projectId, environmentId),
      connectionId,
      "health",
    ],
    queryFn: () =>
      getDatabaseConnectionHealth(organizationId, projectId, environmentId, connectionId),
    enabled: false,
    retry: false,
  });
}

// --- Explorer ---
// Each hook takes `enabled` so only the currently active Explorer sub-tab
// actually fetches — the others stay idle until selected.

export function useSchemas(organizationId, projectId, environmentId, connectionId, enabled) {
  return useQuery({
    queryKey: [...connectionKey(organizationId, projectId, environmentId, connectionId), "schemas"],
    queryFn: () => getSchemas(organizationId, projectId, environmentId, connectionId),
    enabled: Boolean(enabled),
  });
}

export function useTables(organizationId, projectId, environmentId, connectionId, enabled) {
  return useQuery({
    queryKey: [...connectionKey(organizationId, projectId, environmentId, connectionId), "tables"],
    queryFn: () => getTables(organizationId, projectId, environmentId, connectionId),
    enabled: Boolean(enabled),
  });
}

export function useTableDetails(
  organizationId,
  projectId,
  environmentId,
  connectionId,
  schemaName,
  tableName
) {
  return useQuery({
    queryKey: [
      ...connectionKey(organizationId, projectId, environmentId, connectionId),
      "tables",
      schemaName,
      tableName,
    ],
    queryFn: () =>
      getTable(organizationId, projectId, environmentId, connectionId, schemaName, tableName),
    enabled: Boolean(schemaName) && Boolean(tableName),
  });
}

export function useViews(organizationId, projectId, environmentId, connectionId, enabled) {
  return useQuery({
    queryKey: [...connectionKey(organizationId, projectId, environmentId, connectionId), "views"],
    queryFn: () => getViews(organizationId, projectId, environmentId, connectionId),
    enabled: Boolean(enabled),
  });
}

export function useFunctions(organizationId, projectId, environmentId, connectionId, enabled) {
  return useQuery({
    queryKey: [...connectionKey(organizationId, projectId, environmentId, connectionId), "functions"],
    queryFn: () => getFunctions(organizationId, projectId, environmentId, connectionId),
    enabled: Boolean(enabled),
  });
}

export function useIndexes(organizationId, projectId, environmentId, connectionId, enabled) {
  return useQuery({
    queryKey: [...connectionKey(organizationId, projectId, environmentId, connectionId), "indexes"],
    queryFn: () => getIndexes(organizationId, projectId, environmentId, connectionId),
    enabled: Boolean(enabled),
  });
}

export function useTriggers(organizationId, projectId, environmentId, connectionId, enabled) {
  return useQuery({
    queryKey: [...connectionKey(organizationId, projectId, environmentId, connectionId), "triggers"],
    queryFn: () => getTriggers(organizationId, projectId, environmentId, connectionId),
    enabled: Boolean(enabled),
  });
}

export function useSequences(organizationId, projectId, environmentId, connectionId, enabled) {
  return useQuery({
    queryKey: [...connectionKey(organizationId, projectId, environmentId, connectionId), "sequences"],
    queryFn: () => getSequences(organizationId, projectId, environmentId, connectionId),
    enabled: Boolean(enabled),
  });
}

export function useExtensions(organizationId, projectId, environmentId, connectionId, enabled) {
  return useQuery({
    queryKey: [...connectionKey(organizationId, projectId, environmentId, connectionId), "extensions"],
    queryFn: () => getExtensions(organizationId, projectId, environmentId, connectionId),
    enabled: Boolean(enabled),
  });
}