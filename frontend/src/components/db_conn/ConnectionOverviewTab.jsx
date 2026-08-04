import {
  ArrowDownToLine,
  CheckCircle2,
  Clock,
  Database,
  Eye,
  FunctionSquare,
  HardDrive,
  Hash,
  Lock,
  MinusCircle,
  PlusCircle,
  Puzzle,
  RefreshCw,
  Table2,
  Target,
  TriangleAlert,
  Unlock,
  Users,
  XCircle,
  Zap,
} from "lucide-react";
import {
  useDatabaseConnectionOverview,
  useRefreshDatabaseConnectionMetadata,
} from "../../hooks/useDatabaseConnections";
import { useToast } from "../toast/ToastProvider";
import { formatBytes } from "../../utils/formatBytes";
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

function StatCard({ icon: Icon, label, value, title }) {
  const displayValue =
    typeof value === "number" ? value.toLocaleString() : value;
  const isLong = typeof displayValue === "string" && displayValue.length > 10;

  return (
    <div className="dashboard-stat-card" title={title}>
      <div className="dashboard-stat-icon">
        <Icon className="h-4 w-4 text-signal" />
      </div>
      <p className="dashboard-stat-label">{label}</p>
      <p className={`dashboard-stat-value ${isLong ? "dashboard-stat-value-compact" : ""}`}>
        {displayValue}
      </p>
    </div>
  );
}

function SectionTitle({ children }) {
  return <p className="overview-section-title">{children}</p>;
}

export default function ConnectionOverviewTab({
  organizationId,
  projectId,
  environmentId,
  connectionId,
}) {
  const { showToast } = useToast();
  const {
    data: overview,
    isLoading,
    isError,
    error,
    refetch,
  } = useDatabaseConnectionOverview(organizationId, projectId, environmentId, connectionId);
  const refreshMetadata = useRefreshDatabaseConnectionMetadata(
    organizationId,
    projectId,
    environmentId
  );

  const isNotFoundMetadata = isError && error?.response?.status === 404;

  const handleRefresh = async () => {
    try {
      await refreshMetadata.mutateAsync(connectionId);
      showToast("Database metadata refreshed successfully.", { type: "success" });
      refetch();
    } catch (err) {
      showToast(err.friendlyMessage || "Failed to refresh database metadata.", {
        type: "error",
      });
    }
  };

  // Loading
  if (isLoading) {
    return (
      <div className="dashboard-stats-grid">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="dashboard-stat-card">
            <div className="orgs-skeleton dashboard-skeleton-icon" />
            <div className="orgs-skeleton dashboard-skeleton-text" />
          </div>
        ))}
      </div>
    );
  }

  // No metadata snapshot yet
  if (isNotFoundMetadata) {
    return (
      <div className="orgs-empty-state">
        <Database className="h-8 w-8 text-fog" strokeWidth={1.5} />
        <p className="mt-3 text-sm font-medium text-paper">
          No metadata snapshot has been generated yet.
        </p>
        <p className="mt-1 max-w-sm text-sm text-fog">
          Refresh metadata to discover schemas, tables, and statistics for
          this connection.
        </p>
        <button
          className="orgs-primary-btn mt-4"
          onClick={handleRefresh}
          disabled={refreshMetadata.isPending}
        >
          <RefreshCw
            className={`h-4 w-4 ${refreshMetadata.isPending ? "animate-spin" : ""}`}
          />
          {refreshMetadata.isPending ? "Refreshing…" : "Refresh Metadata"}
        </button>
      </div>
    );
  }

  // Other errors
  if (isError) {
    return (
      <div className="orgs-error-state">
        <TriangleAlert className="h-5 w-5 text-danger" />
        <div>
          <p className="text-sm font-medium text-paper">
            Couldn&apos;t load database overview
          </p>
          <p className="mt-1 text-sm text-fog">
            {error?.friendlyMessage || "Please try again."}
          </p>
        </div>
        <button className="orgs-secondary-btn" onClick={() => refetch()}>
          Retry
        </button>
      </div>
    );
  }

  if (!overview) return null;

  const objects = [
    { key: "schemas", label: "Schemas", icon: HardDrive, value: overview.schemas },
    { key: "tables", label: "Tables", icon: Table2, value: overview.tables },
    { key: "views", label: "Views", icon: Eye, value: overview.views },
    { key: "functions", label: "Functions", icon: FunctionSquare, value: overview.functions },
    { key: "indexes", label: "Indexes", icon: Hash, value: overview.indexes },
    { key: "triggers", label: "Triggers", icon: Zap, value: overview.triggers },
    { key: "sequences", label: "Sequences", icon: RefreshCw, value: overview.sequences },
    { key: "extensions", label: "Extensions", icon: Puzzle, value: overview.extensions },
  ];

  const dbStats = [
    { key: "committed", label: "Transactions Committed", icon: CheckCircle2, value: overview.database_statistics?.transactions_committed },
    { key: "rolledback", label: "Transactions Rolled Back", icon: XCircle, value: overview.database_statistics?.transactions_rolled_back },
    { key: "blocksread", label: "Blocks Read", icon: ArrowDownToLine, value: overview.database_statistics?.blocks_read },
    { key: "blockshit", label: "Blocks Hit", icon: Target, value: overview.database_statistics?.blocks_hit },
    { key: "returned", label: "Tuples Returned", icon: Table2, value: overview.database_statistics?.tuples_returned },
    { key: "fetched", label: "Tuples Fetched", icon: ArrowDownToLine, value: overview.database_statistics?.tuples_fetched },
    { key: "inserted", label: "Tuples Inserted", icon: PlusCircle, value: overview.database_statistics?.tuples_inserted },
    { key: "updated", label: "Tuples Updated", icon: RefreshCw, value: overview.database_statistics?.tuples_updated },
    { key: "deleted", label: "Tuples Deleted", icon: MinusCircle, value: overview.database_statistics?.tuples_deleted },
  ];

  const connectionStats = [
    { key: "total_connections", label: "Total Connections", icon: Users, value: overview.connection_statistics?.total_connections },
    { key: "active_connections", label: "Active Connections", icon: CheckCircle2, value: overview.connection_statistics?.active_connections },
    { key: "idle_connections", label: "Idle Connections", icon: Clock, value: overview.connection_statistics?.idle_connections },
    { key: "waiting_connections", label: "Waiting Connections", icon: TriangleAlert, value: overview.connection_statistics?.waiting_connections },
  ];

  const lockStats = [
    { key: "total_locks", label: "Total Locks", icon: Lock, value: overview.lock_statistics?.total_locks },
    { key: "granted_locks", label: "Granted Locks", icon: Unlock, value: overview.lock_statistics?.granted_locks },
    { key: "waiting_locks", label: "Waiting Locks", icon: Clock, value: overview.lock_statistics?.waiting_locks },
  ];

  return (
    <div>
      {/* Refresh action */}
      <div className="overview-refresh-row">
        <button
          className="orgs-secondary-btn"
          onClick={handleRefresh}
          disabled={refreshMetadata.isPending}
        >
          <RefreshCw
            className={`h-4 w-4 ${refreshMetadata.isPending ? "animate-spin" : ""}`}
          />
          {refreshMetadata.isPending ? "Refreshing…" : "Refresh Metadata"}
        </button>
      </div>

      {/* Section 1 — General Information */}
      <SectionTitle>General Information</SectionTitle>
      <div className="dashboard-stats-grid dashboard-stats-grid-3">
        <StatCard
          icon={Database}
          label="PostgreSQL Version"
          value={formatPostgresVersion(overview.postgres_version)}
          title={overview.postgres_version}
        />
        <StatCard icon={HardDrive} label="Database Size" value={formatBytes(overview.database_size)} />
        <StatCard icon={Clock} label="Last Refreshed" value={formatDateTime(overview.last_refreshed)} />
      </div>

      {/* Section 2 — Database Objects */}
      <SectionTitle>Database Objects</SectionTitle>
      <div className="overview-objects-grid">
        {objects.map(({ key, label, icon, value }) => (
          <StatCard key={key} icon={icon} label={label} value={value ?? "—"} />
        ))}
      </div>

      {/* Section 3 — Database Statistics */}
      <SectionTitle>Database Statistics</SectionTitle>
      <div className="overview-objects-grid">
        {dbStats.map(({ key, label, icon, value }) => (
          <StatCard key={key} icon={icon} label={label} value={value ?? "—"} />
        ))}
      </div>

      {/* Section 4 — Connection Statistics */}
      <SectionTitle>Connection Statistics</SectionTitle>
      <div className="dashboard-stats-grid">
        {connectionStats.map(({ key, label, icon, value }) => (
          <StatCard key={key} icon={icon} label={label} value={value ?? "—"} />
        ))}
      </div>

      {/* Section 5 — Lock Statistics */}
      <SectionTitle>Lock Statistics</SectionTitle>
      <div className="dashboard-stats-grid dashboard-stats-grid-3">
        {lockStats.map(({ key, label, icon, value }) => (
          <StatCard key={key} icon={icon} label={label} value={value ?? "—"} />
        ))}
      </div>
    </div>
  );
}
