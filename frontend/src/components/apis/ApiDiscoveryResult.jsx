import { CheckCircle2, Info, XCircle, Layers } from "lucide-react";
import "../../styles/Organizations.css";
import "../../styles/dashboard.css";
import "../../styles/Apis.css";

function getMethodBadgeClass(method) {
  switch (method?.toUpperCase()) {
    case "GET":
      return "text-blue-400 bg-blue-400/10 border-blue-400/20";
    case "POST":
      return "text-green-400 bg-green-400/10 border-green-400/20";
    case "PUT":
      return "text-yellow-400 bg-yellow-400/10 border-yellow-400/20";
    case "PATCH":
      return "text-orange-400 bg-orange-400/10 border-orange-400/20";
    case "DELETE":
      return "text-red-400 bg-red-400/10 border-red-400/20";
    default:
      return "text-fog bg-white/5 border-white/10";
  }
}

function getOperationBadgeClass(op) {
  switch (op?.toLowerCase()) {
    case "create":
      return "text-emerald-400 bg-emerald-400/10 border-emerald-400/20";
    case "update":
      return "text-amber-400 bg-amber-400/10 border-amber-400/20";
    case "archive":
      return "text-purple-400 bg-purple-400/10 border-purple-400/20";
    case "unchanged":
    default:
      return "text-fog bg-white/5 border-white/10";
  }
}

export default function ApiDiscoveryResult({ result, onClose }) {
  const applied = result?.applied || [];
  const skipped = result?.skipped || [];
  const failed = result?.failed || [];

  const appliedCount = applied.length;
  const skippedCount = skipped.length;
  const failedCount = failed.length;
  const totalCount = appliedCount + skippedCount + failedCount;

  return (
    <div className="flex flex-col h-full max-h-[80vh]">
      {/* Header */}
      <div>
        <h2 className="font-display text-lg font-semibold text-paper">
          Discovery Complete
        </h2>
        <p className="mt-1 text-sm text-fog">
          Synchronization finished. Below is the summary of discovered endpoints.
        </p>
      </div>

      {/* Stats Cards */}
      <div className="mt-5 grid grid-cols-3 gap-3">
        <div className="dashboard-card text-center p-3">
          <CheckCircle2 className="h-5 w-5 text-signal mx-auto mb-1" />
          <div className="text-xl font-bold text-paper">{appliedCount}</div>
          <div className="text-[11px] text-fog uppercase font-medium tracking-wider">
            Applied
          </div>
        </div>

        <div className="dashboard-card text-center p-3">
          <Info className="h-5 w-5 text-blue-400 mx-auto mb-1" />
          <div className="text-xl font-bold text-paper">{skippedCount}</div>
          <div className="text-[11px] text-fog uppercase font-medium tracking-wider">
            Skipped
          </div>
        </div>

        <div className="dashboard-card text-center p-3">
          <XCircle className="h-5 w-5 text-danger mx-auto mb-1" />
          <div className="text-xl font-bold text-paper">{failedCount}</div>
          <div className="text-[11px] text-fog uppercase font-medium tracking-wider">
            Failed
          </div>
        </div>
      </div>

      {/* Applied operations breakdown */}
      <div className="mt-4 flex-1 overflow-y-auto min-h-[150px] max-h-[300px] border border-white/10 rounded-lg p-3 space-y-2">
        <div className="flex items-center gap-1.5 text-xs font-semibold text-fog uppercase tracking-wider mb-2">
          <Layers className="h-3.5 w-3.5" />
          Synchronized Operations ({appliedCount})
        </div>

        {applied.length === 0 ? (
          <div className="py-6 text-center text-xs text-fog">
            No endpoints required synchronization updates.
          </div>
        ) : (
          applied.map((plan, index) => {
            const method = plan.route?.method || "—";
            const path = plan.route?.path || "—";
            const summary = plan.route?.summary || plan.route?.handler || "";
            const operation = plan.operation || "applied";

            return (
              <div
                key={index}
                className="flex items-center justify-between gap-3 p-2 rounded bg-white/[0.02] border border-white/5 text-xs"
              >
                <div className="flex items-center gap-2 min-w-0 flex-1">
                  <span
                    className={`px-1.5 py-0.5 rounded text-[10px] font-semibold uppercase border ${getOperationBadgeClass(
                      operation
                    )}`}
                  >
                    {operation}
                  </span>
                  <span
                    className={`px-1.5 py-0.5 rounded text-[10px] font-mono font-semibold border ${getMethodBadgeClass(
                      method
                    )}`}
                  >
                    {method.toUpperCase()}
                  </span>
                  <span className="font-mono text-paper truncate" title={path}>
                    {path}
                  </span>
                </div>
                {summary && (
                  <span className="text-fog text-[11px] truncate max-w-[160px]" title={summary}>
                    {summary}
                  </span>
                )}
              </div>
            );
          })
        )}
      </div>

      {/* Summary Note */}
      <div className="mt-3 text-xs text-fog">
        A total of <strong>{totalCount}</strong> endpoints were processed. The endpoints list has been updated.
      </div>

      {/* Action */}
      <div className="mt-4 flex justify-end">
        <button type="button" className="orgs-primary-btn" onClick={onClose}>
          Done
        </button>
      </div>
    </div>
  );
}
