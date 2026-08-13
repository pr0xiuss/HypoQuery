import { CheckCircle2, Info, XCircle } from "lucide-react";
import "../../styles/Organizations.css";

export default function ApiDiscoveryResult({ result, onClose }) {
  const appliedCount = result?.applied?.length || 0;
  const skippedCount = result?.skipped?.length || 0;
  const failedCount = result?.failed?.length || 0;

  const totalCount = appliedCount + skippedCount + failedCount;

  return (
    <div>
      <h2 className="font-display text-lg font-semibold text-paper">
        Discovery Complete
      </h2>
      <p className="mt-1 text-sm text-fog">
        The synchronization process has finished. Here is the summary of changes.
      </p>

      <div className="mt-6 grid grid-cols-3 gap-4">
        {/* Applied */}
        <div className="dashboard-card text-center p-4">
          <CheckCircle2 className="h-6 w-6 text-signal mx-auto mb-2" />
          <div className="text-2xl font-bold text-paper">{appliedCount}</div>
          <div className="text-xs text-fog uppercase font-medium tracking-wider mt-1">
            Applied
          </div>
        </div>

        {/* Skipped */}
        <div className="dashboard-card text-center p-4">
          <Info className="h-6 w-6 text-blue-400 mx-auto mb-2" />
          <div className="text-2xl font-bold text-paper">{skippedCount}</div>
          <div className="text-xs text-fog uppercase font-medium tracking-wider mt-1">
            Skipped
          </div>
        </div>

        {/* Failed */}
        <div className="dashboard-card text-center p-4">
          <XCircle className="h-6 w-6 text-danger mx-auto mb-2" />
          <div className="text-2xl font-bold text-paper">{failedCount}</div>
          <div className="text-xs text-fog uppercase font-medium tracking-wider mt-1">
            Failed
          </div>
        </div>
      </div>

      <div className="mt-6 text-sm text-fog border border-dashed border-white/10 rounded-lg p-4">
        <p>
          A total of <strong>{totalCount}</strong> endpoints were processed during discovery.
          New or updated endpoints are now available in the Endpoints list.
        </p>
      </div>

      <div className="mt-6 flex justify-end">
        <button type="button" className="orgs-primary-btn" onClick={onClose}>
          Done
        </button>
      </div>
    </div>
  );
}
