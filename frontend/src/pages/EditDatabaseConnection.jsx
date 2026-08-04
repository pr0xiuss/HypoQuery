import { Link, useNavigate, useParams } from "react-router-dom";
import { ChevronLeft, Database, TriangleAlert } from "lucide-react";
import {
  useDatabaseConnection,
  useUpdateDatabaseConnection,
} from "../hooks/useDatabaseConnections";
import { useToast } from "../components/toast/ToastProvider";
import DatabaseConnectionForm from "../components/db_conn/DatabaseConnectionForm";
import EnvironmentTabs from "../components/envs/EnvironmentTabs";
import "../styles/Organizations.css";
import "../styles/dashboard.css";
import "../styles/Projects.css";
import "../styles/Environments.css";

export default function EditDatabaseConnection() {
  const { organizationId, projectId, environmentId, connectionId } = useParams();
  const navigate = useNavigate();
  const { showToast } = useToast();

  const {
    data: connection,
    isLoading,
    isError,
    error,
    refetch,
  } = useDatabaseConnection(organizationId, projectId, environmentId, connectionId);
  const updateConnection = useUpdateDatabaseConnection(
    organizationId,
    projectId,
    environmentId
  );

  const basePath = `/organizations/${organizationId}/projects/${projectId}/environments/${environmentId}`;
  const detailsPath = `${basePath}/database-connections/${connectionId}`;

  return (
    <div>
      <EnvironmentTabs active="connections" />

      <Link to={detailsPath} className="dashboard-back-link">
        <ChevronLeft className="h-4 w-4" />
        Back to Connection
      </Link>

      {isLoading && (
        <div className="dashboard-skeleton-card create-project-card">
          <div className="orgs-skeleton dashboard-skeleton-icon" />
          <div className="orgs-skeleton dashboard-skeleton-title" />
          <div className="orgs-skeleton dashboard-skeleton-text" />
        </div>
      )}

      {isError && (
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

      {connection && (
        <div className="dashboard-card create-project-card">
          <div className="create-project-card-header">
            <div className="dashboard-stat-icon">
              <Database className="h-4 w-4 text-signal" />
            </div>
            <div>
              <p className="dashboard-card-title">Edit Connection</p>
              <p className="text-sm text-fog">{connection.name}</p>
            </div>
          </div>

          <div className="mt-5">
            <DatabaseConnectionForm
              defaultValues={{
                name: connection.name,
                host: connection.host,
                port: connection.port,
                database_name: connection.database_name,
                username: connection.username,
                password: "",
                ssl_enabled: connection.ssl_enabled,
              }}
              onSubmit={async (values) => {
                await updateConnection.mutateAsync({
                  connectionId,
                  payload: values,
                });
                showToast("Database connection updated successfully.", {
                  type: "success",
                });
                navigate(detailsPath, { replace: true });
              }}
              isSubmitting={updateConnection.isPending}
              submitError={updateConnection.error?.friendlyMessage}
              submitLabel="Save Changes"
              savingLabel="Saving…"
              cancelTo={detailsPath}
            />
          </div>
        </div>
      )}
    </div>
  );
}
