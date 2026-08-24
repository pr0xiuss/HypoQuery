import { useQuery } from "@tanstack/react-query";
import {
  getDashboard,
  getWorkloads,
  getQueries,
  getQueryDetail,
  getOperations,
  getOperationDetail,
} from "../services/productService";

export function useDashboard() {
  return useQuery({
    queryKey: ["dashboard"],
    queryFn: () => getDashboard(),
  });
}

export function useWorkloads(limit = 100, offset = 0) {
  return useQuery({
    queryKey: ["workloads", limit, offset],
    queryFn: () => getWorkloads(limit, offset),
  });
}

export function useQueries(fingerprintId, limit = 100, offset = 0) {
  return useQuery({
    queryKey: ["queries", fingerprintId, limit, offset],
    queryFn: () => getQueries(fingerprintId, limit, offset),
  });
}

export function useQueryDetail(queryId) {
  return useQuery({
    queryKey: ["queryDetail", queryId],
    queryFn: () => getQueryDetail(queryId),
    enabled: !!queryId,
  });
}

export function useOperations(limit = 100, offset = 0) {
  return useQuery({
    queryKey: ["operations", limit, offset],
    queryFn: () => getOperations(limit, offset),
  });
}

export function useOperationDetail(operationId) {
  return useQuery({
    queryKey: ["operationDetail", operationId],
    queryFn: () => getOperationDetail(operationId),
    enabled: !!operationId,
  });
}
