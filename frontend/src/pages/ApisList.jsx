import { useState } from "react";
import { useParams } from "react-router-dom";
import { Pencil, Plug, Plus, Trash2, TriangleAlert } from "lucide-react";
import { useEnvironment } from "../hooks/useEnvironments";
import { useApis, useCreateApi, useDeleteApi, useUpdateApi } from "../hooks/useApis";
import { useToast } from "../components/toast/ToastProvider";
import { ConnectionStatusBadge } from "../components/db_conn/ConnectionBadges";
import ApiFormDialog from "../components/apis/ApiFormDialog";
import DeleteApiDialog from "../components/apis/DeleteApiDialog";
import EnvironmentTabs from "../components/envs/EnvironmentTabs";
import { formatFrameworkLabel } from "../utils/apiFrameworks";
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
  const [isCreateOpen, setCreateOpen] = useState(false);
  const [editingApi, setEditingApi] = useState(null);
  const [pendingDelete, setPendingDelete] = useState(null);

  const { showToast } = useToast();
  const { data: environment } = useEnvironment(organizationId, projectId, environmentId);
  const { data: apis, isLoading, isError, error, refetch } = useApis(
    organizationId,
    projectId,
    environmentId
  );
  const createApi = useCreateApi(organizationId, projectId, environmentId);
  const updateApi = useUpdateApi(organizationId, projectId, environmentId);
  const deleteApi = useDeleteApi(organizationId, projectId, environmentId);

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
                <th></th>
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

      {/* Empty state */}
      {!isLoading && !isError && apis && apis.length === 0 && (
        <div className="orgs-empty-state">
          <Plug className="h-8 w-8 text-fog" strokeWidth={1.5} />
          <p className="mt-3 text-sm font-medium text-paper">
            No APIs have been registered yet.
          </p>
          <button className="orgs-primary-btn mt-4" onClick={() => setCreateOpen(true)}>
            <Plus className="h-4 w-4" />
            Register API
          </button>
        </div>
      )}

      {/* Table */}
      {!isLoading && !isError && apis && apis.length > 0 && (
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
                <th></th>
              </tr>
            </thead>
            <tbody>
              {apis.map((api) => (
                <tr key={api.id}>
                  <td>
                    <span className="apis-table-name">{api.name}</span>
                  </td>
                  <td>{formatFrameworkLabel(api.framework)}</td>
                  <td className="apis-table-mono">{api.base_url}</td>
                  <td>{api.version || "—"}</td>
                  <td>
                    <ConnectionStatusBadge active={api.is_active} />
                  </td>
                  <td>{formatDate(api.created_at)}</td>
                  <td>
                    <div className="apis-table-actions">
                      <button
                        className="orgs-secondary-btn project-card-icon-btn"
                        onClick={() => setEditingApi(api)}
                        title="Edit API"
                      >
                        <Pencil className="h-4 w-4" />
                      </button>
                      <button
                        className="orgs-secondary-btn project-card-icon-btn"
                        onClick={() => setPendingDelete(api)}
                        title="Delete API"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

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
    </div>
  );
}
