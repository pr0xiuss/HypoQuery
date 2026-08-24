import React from "react";
import { Link } from "react-router-dom";
import { useWorkloads } from "../hooks/useProduct";
import { Layers3, ChevronRight, Clock } from "lucide-react";

export default function WorkloadsList() {
  const { data, isLoading, error } = useWorkloads();

  if (isLoading) {
    return <div className="p-8 text-secondary">Loading workloads...</div>;
  }

  if (error) {
    return <div className="p-8 text-red-500">Failed to load workloads</div>;
  }

  const workloads = data?.workloads || [];

  return (
    <div className="max-w-7xl mx-auto p-8">
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-display font-semibold text-paper">Workloads</h1>
          <p className="text-secondary mt-1">Manage and inspect query workloads across environments.</p>
        </div>
      </div>

      <div className="bg-surface border border-divider rounded-xl overflow-hidden">
        {workloads.length === 0 ? (
          <div className="p-12 text-center">
            <Layers3 className="h-12 w-12 text-divider mx-auto mb-4" />
            <h3 className="text-lg font-medium text-paper">No Workloads Found</h3>
            <p className="text-secondary mt-1">There are no workloads tracked by the system yet.</p>
          </div>
        ) : (
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-divider bg-surface-hover/50">
                <th className="px-6 py-4 text-xs font-semibold text-secondary uppercase tracking-wider">Fingerprint</th>
                <th className="px-6 py-4 text-xs font-semibold text-secondary uppercase tracking-wider">Snippet</th>
                <th className="px-6 py-4 text-xs font-semibold text-secondary uppercase tracking-wider">Executions</th>
                <th className="px-6 py-4 text-xs font-semibold text-secondary uppercase tracking-wider">Last Executed</th>
                <th className="px-6 py-4"></th>
              </tr>
            </thead>
            <tbody className="divide-y divide-divider">
              {workloads.map((w) => (
                <tr key={w.fingerprint_id} className="hover:bg-surface-hover transition-colors">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="font-mono text-sm text-paper bg-surface-hover px-2 py-1 rounded">
                      {w.fingerprint_id}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <span className="text-sm font-mono text-secondary truncate max-w-xs block">
                      {w.query_text_snippet}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="text-sm font-medium text-paper">{w.execution_count}</span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center text-sm text-secondary">
                      <Clock className="w-4 h-4 mr-2" />
                      {new Date(w.last_executed_at).toLocaleString()}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right">
                    <Link
                      to={`/queries?fingerprint_id=${w.fingerprint_id}`}
                      className="inline-flex items-center text-sm font-medium text-signal hover:text-signal-hover transition-colors"
                    >
                      View Queries <ChevronRight className="w-4 h-4 ml-1" />
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
