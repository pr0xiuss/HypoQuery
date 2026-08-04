import { useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import {
  Database,
  Pencil,
  Plug,
  Plus,
  Search,
  ShieldCheck,
  Trash2,
  TriangleAlert,
} from "lucide-react";
import { useEnvironment } from "../hooks/useEnvironments";
import {
  useDatabaseConnections,
  useDeleteDatabaseConnection,
} from "../hooks/useDatabaseConnections";
import { useToast } from "../components/toast/ToastProvider";
import {
  ConnectionStatusBadge,
  SslBadge,
} from "../components/db_conn/ConnectionBadges";
import DeleteDatabaseConnectionDialog from "../components/db_conn/DeleteDatabaseConnectionDialog";
import EnvironmentTabs from "../components/envs/EnvironmentTabs";
import "../styles/Organizations.css";
import "../styles/dashboard.css";
import "../styles/Environments.css";
import "../styles/DatabaseConnections.css";

function formatDate(isoString) {
  if (!isoString) return "—";
  try {
    return new Intl.DateTimeFormat("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    }).format(new Date(isoString));
  } catch {
    return isoString;
  }
}

export default function DatabaseConnectionsList() {
  const { organizationId, projectId, environmentId } = useParams();
  const [search, setSearch] = useState("");
  const [pendingDelete, setPendingDelete] = useState(null);

  const { showToast } = useToast();
  const { data: environment } = useEnvironment(organizationId, projectId, environmentId);
  const {
    data: connections,
    isLoading,
    isError,
    error,
    refetch,
  } = useDatabaseConnections(organizationId, projectId, environmentId);
  const deleteConnection = useDeleteDatabaseConnection(
    organizationId,
    projectId,
    environmentId
  );

  const filtered = useMemo(() => {
    if (!connections) return [];
    const q = search.trim().toLowerCase();
    if (!q) return connections;
    return connections.filter((c) => c.name.toLowerCase().includes(q));
  }, [connections, search]);

  const total = connections?.length ?? 0;
  const activeCount = connections?.filter((c) => c.is_active).length ?? 0;
  const sslCount = connections?.filter((c) => c.ssl_enabled).length ?? 0;

  const stats = [
    {
      key: "total",
      icon: Database,
      label: "Total Connections",
      value: isLoading ? "—" : String(total),
      helper: total === 0 ? "No connections yet" : `${total} total`,
    },
    {
      key: "active",
      icon: Plug,
      label: "Active Connections",
      value: isLoading ? "—" : String(activeCount),
      helper: `${activeCount} of ${total} active`,
    },
    {
      key: "ssl",
      icon: ShieldCheck,
      label: "SSL Enabled",
      value: isLoading ? "—" : String(sslCount),
      helper: `${sslCount} of ${total} using SSL`,
    },
  ];

  const basePath = `/organizations/${organizationId}/projects/${projectId}/environments/${environmentId}`;

  return (
    <div>
      <EnvironmentTabs active="connections" />

      {/* Page header */}
      <div className="orgs-header">
        <div>
          <h1 className="font-display text-2xl font-semibold text-paper">
            Database Connections
          </h1>
          <p className="mt-1 text-sm text-fog">
            Connections configured for {environment?.name || "this environment"}.
          </p>
        </div>
        <Link to={`${basePath}/database-connections/new`} className="orgs-primary-btn">
          <Plus className="h-4 w-4" />
          New Connection
        </Link>
      </div>

      {/* Statistics */}
      <div className="dashboard-stats-grid dashboard-stats-grid-3">
        {stats.map(({ key, icon: Icon, label, value, helper }) => (
          <div key={key} className="dashboard-stat-card">
            <div className="dashboard-stat-icon">
              <Icon className="h-4 w-4 text-signal" />
            </div>
            <p className="dashboard-stat-label">{label}</p>
            <p className="dashboard-stat-value">{value}</p>
            <p className="dashboard-stat-helper">{helper}</p>
          </div>
        ))}
      </div>

      {/* Search */}
      <div className="orgs-search">
        <Search className="h-4 w-4 text-fog" />
        <input
          type="text"
          placeholder="Search connections…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      {/* Loading */}
      {isLoading && (
        <div className="connections-grid">
          {[1, 2, 3].map((i) => (
            <div key={i} className="connection-card">
              <div className="orgs-skeleton dashboard-skeleton-icon" />
              <div className="orgs-skeleton dashboard-skeleton-title" />
              <div className="orgs-skeleton dashboard-skeleton-text" />
            </div>
          ))}
        </div>
      )}

      {/* Error */}
      {isError && (
        <div className="orgs-error-state">
          <TriangleAlert className="h-5 w-5 text-danger" />
          <div>
            <p className="text-sm font-medium text-paper">
              Couldn&apos;t load database connections
            </p>
            <p className="mt-1 text-sm text-fog">
              {error?.friendlyMessage || "Please try again."}
            </p>
          </div>
          <button className="orgs-secondary-btn" onClick={() => refetch()}>
            Retry
          </button>
        </div>
      )}

      {/* Empty state */}
      {!isLoading && !isError && connections && connections.length === 0 && (
        <div className="orgs-empty-state">
          <Database className="h-8 w-8 text-fog" strokeWidth={1.5} />
          <p className="mt-3 text-sm font-medium text-paper">
            No database connections found.
          </p>
          <Link
            to={`${basePath}/database-connections/new`}
            className="orgs-primary-btn mt-4"
          >
            <Plus className="h-4 w-4" />
            Create Database Connection
          </Link>
        </div>
      )}

      {/* No search results */}
      {!isLoading &&
        !isError &&
        connections &&
        connections.length > 0 &&
        filtered.length === 0 && (
          <div className="orgs-empty-state">
            <Search className="h-8 w-8 text-fog" strokeWidth={1.5} />
            <p className="mt-3 text-sm font-medium text-paper">
              No connections match &quot;{search}&quot;.
            </p>
          </div>
        )}

      {/* Connection cards */}
      {!isLoading && !isError && filtered.length > 0 && (
        <div className="connections-grid">
          {filtered.map((connection) => (
            <div key={connection.id} className="connection-card">
              <div className="connection-card-header">
                <div className="connection-card-icon">
                  <Database className="h-4 w-4 text-signal" />
                </div>
                <div className="min-w-0 flex-1">
                  <Link
                    to={`${basePath}/database-connections/${connection.id}`}
                    className="connection-card-name"
                  >
                    {connection.name}
                  </Link>
                  <div className="connection-card-badges">
                    <ConnectionStatusBadge active={connection.is_active} />
                    <SslBadge enabled={connection.ssl_enabled} />
                  </div>
                </div>
              </div>

              <dl className="connection-card-details">
                <div>
                  <dt>Host</dt>
                  <dd>{connection.host}</dd>
                </div>
                <div>
                  <dt>Port</dt>
                  <dd>{connection.port}</dd>
                </div>
                <div>
                  <dt>Database</dt>
                  <dd>{connection.database_name}</dd>
                </div>
                <div>
                  <dt>Username</dt>
                  <dd>{connection.username}</dd>
                </div>
              </dl>

              <div className="connection-card-meta">
                <span className="project-card-meta-item">
                  Created {formatDate(connection.created_at)}
                </span>
              </div>

              <div className="project-card-actions">
                <Link
                  to={`${basePath}/database-connections/${connection.id}`}
                  className="orgs-primary-btn project-card-open-btn"
                >
                  View
                </Link>
                <Link
                  to={`${basePath}/database-connections/${connection.id}/edit`}
                  className="orgs-secondary-btn project-card-icon-btn"
                  title="Edit connection"
                >
                  <Pencil className="h-4 w-4" />
                </Link>
                <button
                  className="orgs-secondary-btn project-card-icon-btn"
                  onClick={() => setPendingDelete(connection)}
                  title="Delete connection"
                >
                  <Trash2 className="h-4 w-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {pendingDelete && (
        <DeleteDatabaseConnectionDialog
          connection={pendingDelete}
          onClose={() => setPendingDelete(null)}
          onConfirm={async () => {
            await deleteConnection.mutateAsync(pendingDelete.id);
            showToast("Database connection deleted successfully.", {
              type: "success",
            });
            setPendingDelete(null);
          }}
          isDeleting={deleteConnection.isPending}
        />
      )}
    </div>
  );
}
