import { Activity, CheckCircle2, Clock, Gauge, XCircle } from "lucide-react";
import { useDatabaseConnectionHealth } from "../../hooks/useDatabaseConnections";
import { formatPostgresVersion } from "../../utils/formatPostgresVersion";

function formatDateTime(isoString) {
  if (!isoString) return "—";
  try {
    return new Intl.DateTimeFormat(undefined, {
      dateStyle: "medium",
      timeStyle: "short",
    }).format(new Date(isoString));
  } catch {
    return isoString;
  }
}

export default function ConnectionHealthTab({
  organizationId,
  projectId,
  environmentId,
  connectionId,
}) {
  const {
    data: health,
    isFetching,
    isError,
    error,
    refetch,
  } = useDatabaseConnectionHealth(organizationId, projectId, environmentId, connectionId);

  return (
    <div>
      <div className="dashboard-card">
        <div className="overview-refresh-row overview-refresh-row-inline">
          <p className="dashboard-card-title overview-refresh-title">
            Connection Health
          </p>
          <button
            className="orgs-primary-btn"
            onClick={() => refetch()}
            disabled={isFetching}
          >
            <Activity className={`h-4 w-4 ${isFetching ? "animate-pulse" : ""}`} />
            {isFetching ? "Checking…" : "Run Health Check"}
          </button>
        </div>

        {!health && !isError && !isFetching && (
          <p className="mt-4 text-sm text-fog">
            Run a health check to see this connection&apos;s current status.
          </p>
        )}

        {isError && (
          <div className="dialog-error mt-4">
            {error?.friendlyMessage || "Failed to check connection health."}
          </div>
        )}

        {health && (
          <div className="dashboard-stats-grid dashboard-stats-grid-3 mt-5">
            <div className="dashboard-stat-card">
              <div className="dashboard-stat-icon">
                {health.healthy ? (
                  <CheckCircle2 className="h-4 w-4 text-ok" />
                ) : (
                  <XCircle className="h-4 w-4 text-danger" />
                )}
              </div>
              <p className="dashboard-stat-label">Status</p>
              <p className="dashboard-stat-value">
                {health.healthy ? "Healthy" : "Unhealthy"}
              </p>
            </div>

            <div className="dashboard-stat-card">
              <div className="dashboard-stat-icon">
                <Gauge className="h-4 w-4 text-signal" />
              </div>
              <p className="dashboard-stat-label">Latency</p>
              <p className="dashboard-stat-value">
                {health.latency_ms != null ? `${health.latency_ms.toFixed(2)} ms` : "—"}
              </p>
            </div>

            <div className="dashboard-stat-card">
              <div className="dashboard-stat-icon">
                <Clock className="h-4 w-4 text-signal" />
              </div>
              <p className="dashboard-stat-label">Checked At</p>
              <p className="dashboard-stat-value overview-health-timestamp">
                {formatDateTime(health.checked_at)}
              </p>
            </div>
          </div>
        )}

        {health?.postgres_version && (
          <p className="mt-4 text-xs text-fog" title={health.postgres_version}>
            {formatPostgresVersion(health.postgres_version)}
          </p>
        )}

        {health && !health.healthy && health.error && (
          <div className="dialog-error mt-4">{health.error}</div>
        )}
      </div>
    </div>
  );
}
