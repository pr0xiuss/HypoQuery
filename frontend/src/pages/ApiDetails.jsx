import { useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import {
  Calendar,
  ChevronLeft,
  Clock,
  Pencil,
  Server,
  Trash2,
  TriangleAlert,
  Sparkles,
  Code2,
} from "lucide-react";
import { useApi, useDeleteApi, useUpdateApi } from "../hooks/useApis";
import { useToast } from "../components/toast/ToastProvider";
import { ConnectionStatusBadge } from "../components/db_conn/ConnectionBadges";
import { formatFrameworkLabel } from "../utils/apiFrameworks";
import DeleteApiDialog from "../components/apis/DeleteApiDialog";
import ApiFormDialog from "../components/apis/ApiFormDialog";
import ApiEndpointList from "../components/apis/ApiEndpointList";
import ApiDiscoveryDialog from "../components/apis/ApiDiscoveryDialog";
import EnvironmentTabs from "../components/envs/EnvironmentTabs";
import "../styles/Organizations.css";
import "../styles/dashboard.css";
import "../styles/Environments.css";
import "../styles/Apis.css";

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

export default function ApiDetails() {
  const { organizationId, projectId, environmentId, apiId } = useParams();
  const navigate = useNavigate();
  const { showToast } = useToast();

  const [isEditOpen, setEditOpen] = useState(false);
  const [isDeleteOpen, setDeleteOpen] = useState(false);
  const [isDiscoveryOpen, setDiscoveryOpen] = useState(false);

  const {
    data: api,
    isLoading,
    isError,
    error,
    refetch,
  } = useApi(organizationId, projectId, environmentId, apiId);

  const updateApi = useUpdateApi(organizationId, projectId, environmentId);
  const deleteApi = useDeleteApi(organizationId, projectId, environmentId);

  const basePath = `/organizations/${organizationId}/projects/${projectId}/environments/${environmentId}`;
  const isNotFound = isError && error?.response?.status === 404;

  return (
    <div>
      <EnvironmentTabs active="apis" />

      {/* Back link */}
      <Link
        to={`${basePath}/apis`}
        className="dashboard-back-link mb-6 inline-flex items-center gap-1"
      >
        <ChevronLeft className="h-4 w-4" />
        Back to APIs
      </Link>

      {/* Loading Skeleton */}
      {isLoading && (
        <div className="dashboard-skeleton-card">
          <div className="orgs-skeleton dashboard-skeleton-icon" />
          <div className="orgs-skeleton dashboard-skeleton-title" />
          <div className="orgs-skeleton dashboard-skeleton-text" />
        </div>
      )}

      {/* Not found state */}
      {isNotFound && (
        <div className="orgs-empty-state">
          <Server className="h-8 w-8 text-fog" strokeWidth={1.5} />
          <p className="mt-3 text-sm font-medium text-paper">API not found.</p>
          <p className="mt-1 max-w-sm text-sm text-fog">
            This API may have been deleted, or you may not have access to it.
          </p>
          <Link to={`${basePath}/apis`} className="orgs-primary-btn mt-4">
            Return to APIs
          </Link>
        </div>
      )}

      {/* Other error states */}
      {isError && !isNotFound && (
        <div className="orgs-error-state">
          <TriangleAlert className="h-5 w-5 text-danger" />
          <div>
            <p className="text-sm font-medium text-paper">Couldn&apos;t load API</p>
            <p className="mt-1 text-sm text-fog">
              {error?.friendlyMessage || "Please try again."}
            </p>
          </div>
          <button className="orgs-secondary-btn" onClick={() => refetch()}>
            Retry
          </button>
        </div>
      )}

      {/* Loaded API Content */}
      {api && (
        <>
          {/* Header Card */}
          <div className="dashboard-detail-header">
            <div className="flex gap-4">
              <div className="dashboard-detail-icon">
                <Server className="h-6 w-6 text-signal" />
              </div>
              <div className="min-w-0">
                <div className="flex flex-wrap items-center gap-2">
                  <h1 className="font-display text-2xl font-semibold text-paper">
                    {api.name}
                  </h1>
                  <ConnectionStatusBadge active={api.is_active} />
                  <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-medium bg-white/5 border border-white/5 text-paper">
                    <Code2 className="h-3 w-3 text-signal" />
                    {formatFrameworkLabel(api.framework)}
                  </span>
                </div>
                {api.description && (
                  <p className="mt-2 max-w-2xl text-sm leading-relaxed text-fog">
                    {api.description}
                  </p>
                )}
                <div className="dashboard-detail-meta">
                  <span className="dashboard-detail-meta-item">
                    <Calendar className="h-3.5 w-3.5" />
                    Created {formatDate(api.created_at)}
                  </span>
                  <span className="dashboard-detail-meta-item">
                    <Clock className="h-3.5 w-3.5" />
                    Updated {formatDate(api.updated_at)}
                  </span>
                </div>
              </div>
            </div>

            {/* Actions */}
            <div className="dashboard-detail-header-actions">
              <button
                className="orgs-primary-btn"
                onClick={() => setDiscoveryOpen(true)}
              >
                <Sparkles className="h-4 w-4" />
                Discover Endpoints
              </button>
              <button
                className="orgs-secondary-btn"
                onClick={() => setEditOpen(true)}
              >
                <Pencil className="h-4 w-4" />
                Edit
              </button>
              <button
                className="orgs-secondary-btn dashboard-danger-btn"
                onClick={() => setDeleteOpen(true)}
              >
                <Trash2 className="h-4 w-4" />
                Delete
              </button>
            </div>
          </div>

          {/* General Information Card */}
          <div className="dashboard-card mb-8">
            <p className="dashboard-card-title">General Information</p>
            <div className="dashboard-info-grid">
              <InfoRow label="Name" value={api.name} />
              <InfoRow label="Slug" value={api.slug} isMono />
              <InfoRow label="Framework" value={formatFrameworkLabel(api.framework)} />
              <InfoRow label="Base URL" value={api.base_url} isMono />
              <InfoRow label="Version" value={api.version} />
              <InfoRow label="Status" value={api.is_active ? "Active" : "Inactive"} />
              <InfoRow label="Description" value={api.description} />
            </div>
          </div>

          {/* Endpoints Major Section */}
          <div className="dashboard-card">
            <div className="flex justify-between items-center mb-6">
              <div>
                <p className="dashboard-card-title !mb-0">Endpoints</p>
                <p className="text-xs text-fog mt-1">
                  HTTP routes and endpoints registered and synchronized for this API.
                </p>
              </div>
              <button
                className="orgs-secondary-btn text-xs"
                onClick={() => setDiscoveryOpen(true)}
              >
                <Sparkles className="h-3.5 w-3.5 text-signal" />
                Discover Endpoints
              </button>
            </div>

            <ApiEndpointList
              organizationId={organizationId}
              projectId={projectId}
              environmentId={environmentId}
              apiId={apiId}
              onDiscover={() => setDiscoveryOpen(true)}
            />
          </div>
        </>
      )}

      {/* Edit Dialog */}
      {isEditOpen && api && (
        <ApiFormDialog
          mode="edit"
          api={api}
          onClose={() => setEditOpen(false)}
          onSubmit={async (values) => {
            await updateApi.mutateAsync({ apiId: api.id, payload: values });
            setEditOpen(false);
            showToast("API updated successfully.", { type: "success" });
          }}
          isSubmitting={updateApi.isPending}
          submitError={updateApi.error?.friendlyMessage}
        />
      )}

      {/* Delete Dialog */}
      {isDeleteOpen && api && (
        <DeleteApiDialog
          api={api}
          onClose={() => setDeleteOpen(false)}
          onConfirm={async () => {
            await deleteApi.mutateAsync(api.id);
            showToast(`"${api.name}" was deleted.`, { type: "success" });
            navigate(`${basePath}/apis`);
          }}
          isDeleting={deleteApi.isPending}
        />
      )}

      {/* Discovery Dialog */}
      {isDiscoveryOpen && api && (
        <ApiDiscoveryDialog
          apiId={api.id}
          organizationId={organizationId}
          projectId={projectId}
          environmentId={environmentId}
          onClose={() => setDiscoveryOpen(false)}
        />
      )}
    </div>
  );
}

function InfoRow({ label, value, isMono = false }) {
  return (
    <div className="dashboard-info-row">
      <span className="dashboard-info-label">{label}</span>
      <span
        className={`dashboard-info-value ${isMono ? "font-mono text-xs" : ""}`}
        title={typeof value === "string" ? value : undefined}
      >
        {value || "—"}
      </span>
    </div>
  );
}
