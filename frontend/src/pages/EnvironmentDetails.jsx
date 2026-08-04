import { useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import {
  Calendar,
  ChevronLeft,
  Clock,
  Layers3,
  Pencil,
  Plug,
  Plus,
  Server,
  Trash2,
  TriangleAlert,
} from "lucide-react";
import {
  useDeleteEnvironment,
  useEnvironment,
} from "../hooks/useEnvironments";
import { useDatabaseConnections } from "../hooks/useDatabaseConnections";
import { useApis } from "../hooks/useApis";
import { useToast } from "../components/toast/ToastProvider";
import EnvironmentTypeBadge from "../components/envs/EnvironmentTypeBadge";
import DeleteEnvironmentDialog from "../components/envs/DeleteEnvironmentDialog";
import EnvironmentTabs from "../components/envs/EnvironmentTabs";
import "../styles/Organizations.css";
import "../styles/dashboard.css";
import "../styles/Environments.css";

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

export default function EnvironmentDetails() {
  const { organizationId, projectId, environmentId } = useParams();
  const navigate = useNavigate();
  const { showToast } = useToast();
  const [isDeleteOpen, setDeleteOpen] = useState(false);

  const {
    data: environment,
    isLoading,
    isError,
    error,
    refetch,
  } = useEnvironment(organizationId, projectId, environmentId);
  const deleteEnvironment = useDeleteEnvironment(organizationId, projectId);
  const { data: connections } = useDatabaseConnections(
    organizationId,
    projectId,
    environmentId
  );
  const connectionCount = connections?.length ?? 0;
  const { data: apis } = useApis(organizationId, projectId, environmentId);
  const apiCount = apis?.length ?? 0;

  const basePath = `/organizations/${organizationId}/projects/${projectId}`;
  const isNotFound = isError && error?.response?.status === 404;

  return (
    <div>
      <EnvironmentTabs active="overview" />

      <Link to={`${basePath}/environments`} className="dashboard-back-link">
        <ChevronLeft className="h-4 w-4" />
        Environments
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
          <Layers3 className="h-8 w-8 text-fog" strokeWidth={1.5} />
          <p className="mt-3 text-sm font-medium text-paper">
            Environment not found.
          </p>
          <p className="mt-1 max-w-sm text-sm text-fog">
            This environment may have been deleted, or you may not have
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
              Couldn&apos;t load this environment
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
      {environment && (
        <>
          {/* Header */}
          <div className="dashboard-detail-header">
            <div className="flex gap-4">
              <div className="dashboard-detail-icon">
                <Layers3 className="h-6 w-6 text-signal" />
              </div>
              <div className="min-w-0">
                <div className="flex flex-wrap items-center gap-2">
                  <h1 className="font-display text-2xl font-semibold text-paper">
                    {environment.name}
                  </h1>
                  <EnvironmentTypeBadge type={environment.type} />
                </div>
                {environment.description && (
                  <p className="mt-2 max-w-2xl text-sm leading-relaxed text-fog">
                    {environment.description}
                  </p>
                )}
                <div className="dashboard-detail-meta">
                  <span className="dashboard-detail-meta-item">
                    <Calendar className="h-3.5 w-3.5" />
                    Created {formatDate(environment.created_at)}
                  </span>
                  <span className="dashboard-detail-meta-item">
                    <Clock className="h-3.5 w-3.5" />
                    Updated {formatDate(environment.updated_at)}
                  </span>
                </div>
              </div>
            </div>

            <div className="dashboard-detail-header-actions">
              <Link
                to={`${basePath}/environments/${environmentId}/edit`}
                className="orgs-secondary-btn"
              >
                <Pencil className="h-4 w-4" />
                Edit Environment
              </Link>
              <button
                className="orgs-secondary-btn dashboard-danger-btn"
                onClick={() => setDeleteOpen(true)}
              >
                <Trash2 className="h-4 w-4" />
                Delete Environment
              </button>
            </div>
          </div>

          {/* Information */}
          <div className="dashboard-card">
            <p className="dashboard-card-title">Environment Information</p>
            <div className="dashboard-info-grid">
              <InfoRow label="Name" value={environment.name} />
              <InfoRow
                label="Description"
                value={environment.description || "No description provided"}
              />
              <InfoRow label="Environment Type" value={environment.type} />
              <InfoRow label="Created" value={formatDate(environment.created_at)} />
              <InfoRow label="Last Updated" value={formatDate(environment.updated_at)} />
            </div>
          </div>

          {/* Modules */}
          <div className="dashboard-modules-grid">
            <div className="dashboard-module-card">
              <div className="dashboard-module-card-header">
                <Plug className="h-4 w-4 text-fog" />
                <span className="text-sm font-medium text-paper">
                  Database Connections
                </span>
              </div>
              <div className="dashboard-module-empty">
                <Plug className="h-6 w-6 text-fog" strokeWidth={1.5} />
                <p className="mt-2 text-sm text-fog">
                  {connectionCount > 0
                    ? `${connectionCount} connection${connectionCount === 1 ? "" : "s"} configured.`
                    : "No database connections added yet."}
                </p>
                <Link
                  to={`${basePath}/environments/${environmentId}/database-connections/new`}
                  className="environment-add-connection-btn"
                >
                  <Plus className="h-3.5 w-3.5" />
                  Add Connection
                </Link>
                {connectionCount > 0 && (
                  <Link
                    to={`${basePath}/environments/${environmentId}/database-connections`}
                    className="dashboard-module-link"
                  >
                    View Connections →
                  </Link>
                )}
              </div>
            </div>

            <div className="dashboard-module-card">
              <div className="dashboard-module-card-header">
                <Server className="h-4 w-4 text-fog" />
                <span className="text-sm font-medium text-paper">APIs</span>
              </div>
              <div className="dashboard-module-empty">
                <Server className="h-6 w-6 text-fog" strokeWidth={1.5} />
                <p className="mt-2 text-sm text-fog">
                  {apiCount > 0
                    ? `${apiCount} API${apiCount === 1 ? "" : "s"} registered.`
                    : "No APIs have been registered yet."}
                </p>
                <Link
                  to={`${basePath}/environments/${environmentId}/apis`}
                  className="environment-add-connection-btn"
                >
                  <Plus className="h-3.5 w-3.5" />
                  Register API
                </Link>
                {apiCount > 0 && (
                  <Link
                    to={`${basePath}/environments/${environmentId}/apis`}
                    className="dashboard-module-link"
                  >
                    View APIs →
                  </Link>
                )}
              </div>
            </div>
          </div>
        </>
      )}

      {isDeleteOpen && environment && (
        <DeleteEnvironmentDialog
          environment={environment}
          onClose={() => setDeleteOpen(false)}
          onConfirm={async () => {
            await deleteEnvironment.mutateAsync(environmentId);
            showToast(`"${environment.name}" was deleted.`, { type: "success" });
            navigate(`${basePath}/environments`);
          }}
          isDeleting={deleteEnvironment.isPending}
        />
      )}
    </div>
  );
}

function InfoRow({ label, value }) {
  return (
    <div className="dashboard-info-row">
      <span className="dashboard-info-label">{label}</span>
      <span
        className="dashboard-info-value"
        title={typeof value === "string" ? value : undefined}
      >
        {value || "—"}
      </span>
    </div>
  );
}