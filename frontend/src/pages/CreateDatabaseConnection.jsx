import { Link, useNavigate, useParams } from "react-router-dom";
import { ChevronLeft, Database } from "lucide-react";
import { useCreateDatabaseConnection } from "../hooks/useDatabaseConnections";
import { useEnvironment } from "../hooks/useEnvironments";
import { useToast } from "../components/toast/ToastProvider";
import DatabaseConnectionForm from "../components/db_conn/DatabaseConnectionForm";
import EnvironmentTabs from "../components/envs/EnvironmentTabs";
import "../styles/Organizations.css";
import "../styles/dashboard.css";
import "../styles/Projects.css";
import "../styles/Environments.css";

export default function CreateDatabaseConnection() {
  const { organizationId, projectId, environmentId } = useParams();
  const navigate = useNavigate();
  const { showToast } = useToast();
  const { data: environment } = useEnvironment(organizationId, projectId, environmentId);
  const createConnection = useCreateDatabaseConnection(
    organizationId,
    projectId,
    environmentId
  );

  const basePath = `/organizations/${organizationId}/projects/${projectId}/environments/${environmentId}`;

  return (
    <div>
      <EnvironmentTabs active="connections" />

      <Link to={`${basePath}/database-connections`} className="dashboard-back-link">
        <ChevronLeft className="h-4 w-4" />
        Database Connections
      </Link>

      <div className="dashboard-card create-project-card">
        <div className="create-project-card-header">
          <div className="dashboard-stat-icon">
            <Database className="h-4 w-4 text-signal" />
          </div>
          <div>
            <p className="dashboard-card-title">New Connection</p>
            <p className="text-sm text-fog">in {environment?.name || "this environment"}</p>
          </div>
        </div>

        <div className="mt-5">
          <DatabaseConnectionForm
            onSubmit={async (values) => {
              await createConnection.mutateAsync(values);
              showToast("Database connection created successfully.", {
                type: "success",
              });
              navigate(`${basePath}/database-connections`, { replace: true });
            }}
            isSubmitting={createConnection.isPending}
            submitError={createConnection.error?.friendlyMessage}
            submitLabel="Create"
            savingLabel="Creating…"
            cancelTo={`${basePath}/database-connections`}
          />
        </div>
      </div>
    </div>
  );
}
