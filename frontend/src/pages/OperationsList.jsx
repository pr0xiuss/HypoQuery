import { useOperations } from "../hooks/useProduct";
import { Sparkles, Clock, CheckCircle2, XCircle, Loader2 } from "lucide-react";

export default function OperationsList() {
  const { data, isLoading, error } = useOperations();

  if (isLoading) {
    return <div className="p-8 text-secondary">Loading operations...</div>;
  }

  if (error) {
    return <div className="p-8 text-red-500">Failed to load operations</div>;
  }

  const operations = data?.operations || [];

  const getStatusIcon = (status) => {
    switch (status.toLowerCase()) {
      case "completed":
        return <CheckCircle2 className="w-5 h-5 text-green-500" />;
      case "failed":
        return <XCircle className="w-5 h-5 text-red-500" />;
      case "running":
      case "in_progress":
        return <Loader2 className="w-5 h-5 text-signal animate-spin" />;
      default:
        return <span className="w-2 h-2 rounded-full bg-secondary"></span>;
    }
  };

  const getStatusClass = (status) => {
    switch (status.toLowerCase()) {
      case "completed":
        return "text-green-400 bg-green-500/10 border-green-500/20";
      case "failed":
        return "text-red-400 bg-red-500/10 border-red-500/20";
      case "running":
      case "in_progress":
        return "text-signal bg-signal/10 border-signal/20";
      default:
        return "text-secondary bg-surface-hover border-divider";
    }
  };

  return (
    <div className="max-w-7xl mx-auto p-8">
      <div className="mb-8">
        <h1 className="text-2xl font-display font-semibold text-paper">Operations</h1>
        <p className="text-secondary mt-1">Read-only view of running and historical optimization pipelines.</p>
      </div>

      <div className="bg-surface border border-divider rounded-xl overflow-hidden">
        {operations.length === 0 ? (
          <div className="p-12 text-center">
            <Sparkles className="h-12 w-12 text-divider mx-auto mb-4" />
            <h3 className="text-lg font-medium text-paper">No Operations Found</h3>
            <p className="text-secondary mt-1">There are no pipeline executions to display.</p>
          </div>
        ) : (
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-divider bg-surface-hover/50">
                <th className="px-6 py-4 text-xs font-semibold text-secondary uppercase tracking-wider">Status</th>
                <th className="px-6 py-4 text-xs font-semibold text-secondary uppercase tracking-wider">Operation ID</th>
                <th className="px-6 py-4 text-xs font-semibold text-secondary uppercase tracking-wider">Type</th>
                <th className="px-6 py-4 text-xs font-semibold text-secondary uppercase tracking-wider">Created At</th>
                <th className="px-6 py-4 text-xs font-semibold text-secondary uppercase tracking-wider">Updated At</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-divider">
              {operations.map((op) => (
                <tr key={op.operation_id} className="hover:bg-surface-hover transition-colors">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      {getStatusIcon(op.status)}
                      <span className={`ml-2 px-2 py-0.5 rounded text-xs font-medium border ${getStatusClass(op.status)}`}>
                        {op.status}
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="font-mono text-sm text-paper bg-surface-hover px-2 py-1 rounded">
                      {op.operation_id.substring(0, 8)}...
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="text-sm text-paper">{op.type}</span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center text-sm text-secondary">
                      <Clock className="w-4 h-4 mr-2" />
                      {new Date(op.created_at).toLocaleString()}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center text-sm text-secondary">
                      <Clock className="w-4 h-4 mr-2" />
                      {new Date(op.updated_at).toLocaleString()}
                    </div>
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
