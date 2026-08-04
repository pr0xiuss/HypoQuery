import { useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import {
  Activity,
  Calendar,
  ChevronLeft,
  Clock,
  Compass,
  Database,
  Gauge,
  LayoutDashboard,
  ListChecks,
  Pencil,
  RefreshCw,
  Trash2,
  TriangleAlert,
} from "lucide-react";
import {
  useDatabaseConnection,
  useDeleteDatabaseConnection,
  useRefreshDatabaseConnectionMetadata,
} from "../hooks/useDatabaseConnections";
import { useToast } from "../components/toast/ToastProvider";
import {
  ConnectionStatusBadge,
  SslBadge,
} from "../components/db_conn/ConnectionBadges";
import DeleteDatabaseConnectionDialog from "../components/db_conn/DeleteDatabaseConnectionDialog";
import ConnectionOverviewTab from "../components/db_conn/ConnectionOverviewTab";
import ConnectionHealthTab from "../components/db_conn/ConnectionHealthTab";
import ConnectionExplorerTab from "../components/db_conn/ConnectionExplorerTab";
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

export default function DatabaseConnectionDetails() {
  const { organizationId, projectId, environmentId, connectionId } = useParams();
  const navigate = useNavigate();
  const { showToast } = useToast();
  const [isDeleteOpen, setDeleteOpen] = useState(false);
  const [activeTab, setActiveTab] = useState("overview");

  const {
    data: connection,
    isLoading,
    isError,
    error,
    refetch,
  } = useDatabaseConnection(organizationId, projectId, environmentId, connectionId);
  const deleteConnection = useDeleteDatabaseConnection(
    organizationId,
    projectId,
    environmentId
  );
  const refreshMetadata = useRefreshDatabaseConnectionMetadata(
    organizationId,
    projectId,
    environmentId
  );

  const handleRefreshMetadata = async () => {
    try {
      await refreshMetadata.mutateAsync(connectionId);
      showToast("Database metadata refreshed successfully.", { type: "success" });
      // Only invalidate — the hook's onSuccess already invalidates every
      // metadata-dependent query (overview, health, and every Explorer
      // resource), and each mounted hook refetches on its own.
    } catch (err) {
      showToast(err.friendlyMessage || "Failed to refresh database metadata.", {
        type: "error",
      });
    }
  };

  const basePath = `/organizations/${organizationId}/projects/${projectId}/environments/${environmentId}`;
  const isNotFound = isError && error?.response?.status === 404;

  return (
    <div>
      <EnvironmentTabs active="connections" />

      <Link to={`${basePath}/database-connections`} className="dashboard-back-link">
        <ChevronLeft className="h-4 w-4" />
        Database Connections
      </Link>

      {/* Loading */}
      {isLoading && (
        <div className="dashboard-skeleton-card">
          <div className="orgs-skeleton dashboard-skeleton-icon" />
          <div className="orgs-skeleton dashboard-skeleton-title" />
          <div className="orgs-skeleton dashboard-skeleton-text" />
        </div>
      )}

      {/* Not found */}
      {isNotFound && (
        <div className="orgs-empty-state">
          <Database className="h-8 w-8 text-fog" strokeWidth={1.5} />
          <p className="mt-3 text-sm font-medium text-paper">
            Database connection not found.
          </p>
          <p className="mt-1 max-w-sm text-sm text-fog">
            This connection may have been deleted, or you may not have
            access to it.
          </p>
        </div>
      )}

      {/* Other errors */}
      {isError && !isNotFound && (
        <div className="orgs-error-state">
          <TriangleAlert className="h-5 w-5 text-danger" />
          <div>
            <p className="text-sm font-medium text-paper">
              Couldn&apos;t load this connection
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

      {/* Loaded */}
      {connection && (
        <>
          {/* Header */}
          <div className="dashboard-detail-header">
            <div className="flex gap-4">
              <div className="dashboard-detail-icon">
                <Database className="h-6 w-6 text-signal" />
              </div>
              <div className="min-w-0">
                <div className="flex flex-wrap items-center gap-2">
                  <h1 className="font-display text-2xl font-semibold text-paper">
                    {connection.name}
                  </h1>
                  <ConnectionStatusBadge active={connection.is_active} />
                  <SslBadge enabled={connection.ssl_enabled} />
                </div>
                <div className="dashboard-detail-meta">
                  <span className="dashboard-detail-meta-item">
                    <Calendar className="h-3.5 w-3.5" />
                    Created {formatDate(connection.created_at)}
                  </span>
                  <span className="dashboard-detail-meta-item">
                    <Clock className="h-3.5 w-3.5" />
                    Updated {formatDate(connection.updated_at)}
                  </span>
                </div>
              </div>
            </div>

            <div className="dashboard-detail-header-actions">
              <button
                className="orgs-secondary-btn"
                onClick={handleRefreshMetadata}
                disabled={refreshMetadata.isPending}
              >
                <RefreshCw
                  className={`h-4 w-4 ${refreshMetadata.isPending ? "animate-spin" : ""}`}
                />
                {refreshMetadata.isPending ? "Refreshing…" : "Refresh Metadata"}
              </button>
              <Link
                to={`${basePath}/database-connections/${connectionId}/edit`}
                className="orgs-secondary-btn"
              >
                <Pencil className="h-4 w-4" />
                Edit
              </Link>
              <button
                className="orgs-secondary-btn dashboard-danger-btn"
                onClick={() => setDeleteOpen(true)}
              >
                <Trash2 className="h-4 w-4" />
                Delete
              </button>
            </div>
          </div>

          {/* Tabs — local state, not routed, per spec ("do not create new navigation") */}
          <div className="environment-tabs">
            <button
              className={`environment-tab ${activeTab === "overview" ? "environment-tab-active" : ""}`}
              onClick={() => setActiveTab("overview")}
            >
              <LayoutDashboard className="h-4 w-4" />
              Overview
            </button>
            <button
              className={`environment-tab ${activeTab === "details" ? "environment-tab-active" : ""}`}
              onClick={() => setActiveTab("details")}
            >
              <ListChecks className="h-4 w-4" />
              Details
            </button>
            <button
              className={`environment-tab ${activeTab === "health" ? "environment-tab-active" : ""}`}
              onClick={() => setActiveTab("health")}
            >
              <Activity className="h-4 w-4" />
              Health
            </button>
            <button
              className={`environment-tab ${activeTab === "explorer" ? "environment-tab-active" : ""}`}
              onClick={() => setActiveTab("explorer")}
            >
              <Compass className="h-4 w-4" />
              Explorer
            </button>
            <button
              className={`environment-tab ${activeTab === "monitoring" ? "environment-tab-active" : ""}`}
              onClick={() => setActiveTab("monitoring")}
            >
              <Gauge className="h-4 w-4" />
              Monitoring
            </button>
          </div>

          {activeTab === "overview" && (
            <ConnectionOverviewTab
              organizationId={organizationId}
              projectId={projectId}
              environmentId={environmentId}
              connectionId={connectionId}
              onRefresh={handleRefreshMetadata}
              isRefreshing={refreshMetadata.isPending}
            />
          )}

          {activeTab === "details" && (
            // Information — password is intentionally never shown.
            // Unchanged from before this became a tab.
            <div className="dashboard-card">
              <p className="dashboard-card-title">Connection Information</p>
              <div className="dashboard-info-grid">
                <InfoRow label="Name" value={connection.name} />
                <InfoRow label="Host" value={connection.host} mono />
                <InfoRow label="Port" value={String(connection.port)} mono />
                <InfoRow label="Database Name" value={connection.database_name} mono />
                <InfoRow label="Username" value={connection.username} mono />
                <InfoRow
                  label="SSL Enabled"
                  value={connection.ssl_enabled ? "Yes" : "No"}
                />
                <InfoRow
                  label="Status"
                  value={connection.is_active ? "Active" : "Inactive"}
                />
                <InfoRow label="Created At" value={formatDate(connection.created_at)} />
                <InfoRow label="Updated At" value={formatDate(connection.updated_at)} />
              </div>
            </div>
          )}

          {activeTab === "health" && (
            <ConnectionHealthTab
              organizationId={organizationId}
              projectId={projectId}
              environmentId={environmentId}
              connectionId={connectionId}
            />
          )}

          {activeTab === "explorer" && (
            <ConnectionExplorerTab
              organizationId={organizationId}
              projectId={projectId}
              environmentId={environmentId}
              connectionId={connectionId}
            />
          )}

          {activeTab === "monitoring" && (
            <div className="dashboard-module-card">
              <div className="dashboard-module-card-header">
                <Gauge className="h-4 w-4 text-fog" />
                <span className="text-sm font-medium text-paper">Monitoring</span>
              </div>
              <div className="dashboard-module-empty">
                <Gauge className="h-6 w-6 text-fog" strokeWidth={1.5} />
                <p className="mt-2 text-sm text-fog">Coming in a future release</p>
              </div>
            </div>
          )}
        </>
      )}

      {isDeleteOpen && connection && (
        <DeleteDatabaseConnectionDialog
          connection={connection}
          onClose={() => setDeleteOpen(false)}
          onConfirm={async () => {
            await deleteConnection.mutateAsync(connectionId);
            showToast("Database connection deleted successfully.", {
              type: "success",
            });
            navigate(`${basePath}/database-connections`);
          }}
          isDeleting={deleteConnection.isPending}
        />
      )}
    </div>
  );
}

function InfoRow({ label, value, mono }) {
  return (
    <div className="dashboard-info-row">
      <span className="dashboard-info-label">{label}</span>
      <span
        className={`dashboard-info-value ${mono ? "dashboard-info-value-mono" : ""}`}
        title={typeof value === "string" ? value : undefined}
      >
        {value || "—"}
      </span>
    </div>
  );
}
