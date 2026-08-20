import { useMemo, useState } from "react";
import { useParams, Link } from "react-router-dom";
import {
  Pencil,
  Plus,
  Trash2,
  TriangleAlert,
  Eye,
  Search,
  Server,
  Code2,
  CheckCircle2,
  Sparkles,
} from "lucide-react";
import { useEnvironment } from "../hooks/useEnvironments";
import { useApis, useCreateApi, useDeleteApi, useUpdateApi } from "../hooks/useApis";
import { useToast } from "../components/toast/ToastProvider";
import { ConnectionStatusBadge } from "../components/db_conn/ConnectionBadges";
import ApiFormDialog from "../components/apis/ApiFormDialog";
import DeleteApiDialog from "../components/apis/DeleteApiDialog";
import ApiDiscoveryDialog from "../components/apis/ApiDiscoveryDialog";
import EnvironmentTabs from "../components/envs/EnvironmentTabs";
import { FRAMEWORK_OPTIONS, formatFrameworkLabel } from "../utils/apiFrameworks";
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

export default function ApisList() {
  const { organizationId, projectId, environmentId } = useParams();
  const [searchTerm, setSearchTerm] = useState("");
  const [frameworkFilter, setFrameworkFilter] = useState("ALL");
  const [statusFilter, setStatusFilter] = useState("ALL");

  const [isCreateOpen, setCreateOpen] = useState(false);
  const [editingApi, setEditingApi] = useState(null);
  const [pendingDelete, setPendingDelete] = useState(null);
  const [discoveringApi, setDiscoveringApi] = useState(null);

  const { showToast } = useToast();
  const { data: environment } = useEnvironment(organizationId, projectId, environmentId);
  const {
    data: apis,
    isLoading,
    isError,
    error,
    refetch,
  } = useApis(organizationId, projectId, environmentId);

  const createApi = useCreateApi(organizationId, projectId, environmentId);
  const updateApi = useUpdateApi(organizationId, projectId, environmentId);
  const deleteApi = useDeleteApi(organizationId, projectId, environmentId);

  const basePath = `/organizations/${organizationId}/projects/${projectId}/environments/${environmentId}`;

  // Filtered APIs
  const filteredApis = useMemo(() => {
    if (!apis) return [];
    const q = searchTerm.trim().toLowerCase();

    return apis.filter((api) => {
      const matchesSearch =
        !q ||
        api.name?.toLowerCase().includes(q) ||
        api.slug?.toLowerCase().includes(q) ||
        api.base_url?.toLowerCase().includes(q) ||
        api.description?.toLowerCase().includes(q) ||
        api.version?.toLowerCase().includes(q);

      const matchesFramework =
        frameworkFilter === "ALL" || api.framework === frameworkFilter;

      const matchesStatus =
        statusFilter === "ALL" ||
        (statusFilter === "ACTIVE" && api.is_active) ||
        (statusFilter === "INACTIVE" && !api.is_active);

      return matchesSearch && matchesFramework && matchesStatus;
    });
  }, [apis, searchTerm, frameworkFilter, statusFilter]);

  // Statistics
  const totalCount = apis?.length ?? 0;
  const activeCount = apis?.filter((a) => a.is_active).length ?? 0;
  const distinctFrameworks = new Set(apis?.map((a) => a.framework) || []).size;

  const stats = [
    {
      key: "total",
      icon: Server,
      label: "Total APIs",
      value: isLoading ? "—" : String(totalCount),
      helper: totalCount === 0 ? "No APIs registered" : `${totalCount} registered`,
    },
    {
      key: "active",
      icon: CheckCircle2,
      label: "Active APIs",
      value: isLoading ? "—" : String(activeCount),
      helper: `${activeCount} of ${totalCount} active`,
    },
    {
      key: "frameworks",
      icon: Code2,
      label: "Frameworks",
      value: isLoading ? "—" : String(distinctFrameworks),
      helper: `${distinctFrameworks} unique framework${distinctFrameworks === 1 ? "" : "s"}`,
    },
  ];

  return (
    <div>
      <EnvironmentTabs active="apis" />

      {/* Page header */}
      <div className="orgs-header">
        <div>
          <h1 className="font-display text-2xl font-semibold text-paper">APIs</h1>
          <p className="mt-1 text-sm text-fog">
            Application APIs registered against {environment?.name || "this environment"}.
          </p>
        </div>
        <button className="orgs-primary-btn" onClick={() => setCreateOpen(true)}>
          <Plus className="h-4 w-4" />
          Register API
        </button>
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

      {/* Search & Filters */}
      <div className="flex flex-wrap gap-3 my-6 items-center">
        {/* Search */}
        <div className="flex-1 min-w-[220px] relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-fog" />
          <input
            type="text"
            placeholder="Search APIs by name, URL, version…"
            className="dialog-input !pl-9"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>

        {/* Framework Filter */}
        <select
          className="dialog-input !w-auto"
          value={frameworkFilter}
          onChange={(e) => setFrameworkFilter(e.target.value)}
        >
          <option value="ALL">All Frameworks</option>
          {FRAMEWORK_OPTIONS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>

        {/* Status Filter */}
        <select
          className="dialog-input !w-auto"
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
        >
          <option value="ALL">All Statuses</option>
          <option value="ACTIVE">Active</option>
          <option value="INACTIVE">Inactive</option>
        </select>
      </div>

      {/* Loading */}
      {isLoading && (
        <div className="apis-table-wrap">
          <table className="apis-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Framework</th>
                <th>Base URL</th>
                <th>Version</th>
                <th>Status</th>
                <th>Created</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {[1, 2, 3].map((i) => (
                <tr key={i}>
                  <td colSpan={7}>
                    <div className="orgs-skeleton apis-skeleton-row" />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Error */}
      {isError && (
        <div className="orgs-error-state">
          <TriangleAlert className="h-5 w-5 text-danger" />
          <div>
            <p className="text-sm font-medium text-paper">Couldn&apos;t load APIs</p>
            <p className="mt-1 text-sm text-fog">
              {error?.friendlyMessage || "Please try again."}
            </p>
          </div>
          <button className="orgs-secondary-btn" onClick={() => refetch()}>
            Retry
          </button>
        </div>
      )}

      {/* Empty state (No APIs registered at all) */}
      {!isLoading && !isError && apis && apis.length === 0 && (
        <div className="orgs-empty-state">
          <Server className="h-8 w-8 text-fog" strokeWidth={1.5} />
          <p className="mt-3 text-sm font-medium text-paper">
            No APIs have been registered yet.
          </p>
          <p className="mt-1 max-w-sm text-xs text-fog">
            Register your first application service to discover and manage its endpoints.
          </p>
          <button className="orgs-primary-btn mt-4" onClick={() => setCreateOpen(true)}>
            <Plus className="h-4 w-4" />
            Register API
          </button>
        </div>
      )}

      {/* Filtered empty state */}
      {!isLoading &&
        !isError &&
        apis &&
        apis.length > 0 &&
        filteredApis.length === 0 && (
          <div className="orgs-empty-state py-12">
            <Search className="h-8 w-8 text-fog" strokeWidth={1.5} />
            <p className="mt-3 text-sm font-medium text-paper">
              No APIs match your search and filter criteria.
            </p>
            <button
              className="orgs-secondary-btn mt-4 text-xs"
              onClick={() => {
                setSearchTerm("");
                setFrameworkFilter("ALL");
                setStatusFilter("ALL");
              }}
            >
              Reset Filters
            </button>
          </div>
        )}

      {/* API Table */}
      {!isLoading && !isError && filteredApis.length > 0 && (
        <div className="apis-table-wrap">
          <table className="apis-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Framework</th>
                <th>Base URL</th>
                <th>Version</th>
                <th>Status</th>
                <th>Created</th>
                <th style={{ textAlign: "right" }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredApis.map((api) => (
                <tr key={api.id}>
                  {/* Name */}
                  <td>
                    <div className="flex flex-col">
                      <Link
                        to={`${basePath}/apis/${api.id}`}
                        className="apis-table-name hover:text-signal transition-colors"
                      >
                        {api.name}
                      </Link>
                      {api.description && (
                        <span className="text-[11px] text-fog truncate max-w-[200px]" title={api.description}>
                          {api.description}
                        </span>
                      )}
                    </div>
                  </td>

                  {/* Framework */}
                  <td>
                    <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-xs font-medium bg-white/5 border border-white/5 text-paper">
                      <Code2 className="h-3 w-3 text-signal" />
                      {formatFrameworkLabel(api.framework)}
                    </span>
                  </td>

                  {/* Base URL */}
                  <td>
                    <span className="apis-table-mono text-fog" title={api.base_url}>
                      {api.base_url}
                    </span>
                  </td>

                  {/* Version */}
                  <td>
                    <span className="text-xs text-paper">{api.version || "—"}</span>
                  </td>

                  {/* Status */}
                  <td>
                    <ConnectionStatusBadge active={api.is_active} />
                  </td>

                  {/* Created */}
                  <td>
                    <span className="text-xs text-fog">{formatDate(api.created_at)}</span>
                  </td>

                  {/* Actions */}
                  <td>
                    <div className="apis-table-actions justify-end">
                      <Link
                        to={`${basePath}/apis/${api.id}`}
                        className="orgs-secondary-btn project-card-icon-btn"
                        title="View API details & endpoints"
                      >
                        <Eye className="h-3.5 w-3.5" />
                      </Link>
                      <button
                        className="orgs-secondary-btn project-card-icon-btn"
                        onClick={() => setDiscoveringApi(api)}
                        title="Discover endpoints"
                      >
                        <Sparkles className="h-3.5 w-3.5 text-signal" />
                      </button>
                      <button
                        className="orgs-secondary-btn project-card-icon-btn"
                        onClick={() => setEditingApi(api)}
                        title="Edit API"
                      >
                        <Pencil className="h-3.5 w-3.5" />
                      </button>
                      <button
                        className="orgs-secondary-btn project-card-icon-btn hover:!border-danger/30 hover:!text-danger"
                        onClick={() => setPendingDelete(api)}
                        title="Delete API"
                      >
                        <Trash2 className="h-3.5 w-3.5" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Create Dialog */}
      {isCreateOpen && (
        <ApiFormDialog
          mode="create"
          onClose={() => setCreateOpen(false)}
          onSubmit={async (values) => {
            await createApi.mutateAsync(values);
            setCreateOpen(false);
            showToast("API registered successfully.", { type: "success" });
          }}
          isSubmitting={createApi.isPending}
          submitError={createApi.error?.friendlyMessage}
        />
      )}

      {/* Edit Dialog */}
      {editingApi && (
        <ApiFormDialog
          mode="edit"
          api={editingApi}
          onClose={() => setEditingApi(null)}
          onSubmit={async (values) => {
            await updateApi.mutateAsync({ apiId: editingApi.id, payload: values });
            setEditingApi(null);
            showToast("API updated successfully.", { type: "success" });
          }}
          isSubmitting={updateApi.isPending}
          submitError={updateApi.error?.friendlyMessage}
        />
      )}

      {/* Delete Dialog */}
      {pendingDelete && (
        <DeleteApiDialog
          api={pendingDelete}
          onClose={() => setPendingDelete(null)}
          onConfirm={async () => {
            await deleteApi.mutateAsync(pendingDelete.id);
            showToast("API deleted successfully.", { type: "success" });
            setPendingDelete(null);
          }}
          isDeleting={deleteApi.isPending}
        />
      )}

      {/* Discovery Dialog */}
      {discoveringApi && (
        <ApiDiscoveryDialog
          organizationId={organizationId}
          projectId={projectId}
          environmentId={environmentId}
          apiId={discoveringApi.id}
          onClose={() => setDiscoveringApi(null)}
        />
      )}
    </div>
  );
}
