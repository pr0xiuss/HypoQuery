import { Link, useNavigate, useParams } from "react-router-dom";
import { ChevronLeft, Server } from "lucide-react";
import { useCreateApi } from "../hooks/useApis";
import { useEnvironment } from "../hooks/useEnvironments";
import { useToast } from "../components/toast/ToastProvider";
import ApiForm from "../components/apis/ApiForm";
import EnvironmentTabs from "../components/envs/EnvironmentTabs";
import "../styles/Organizations.css";
import "../styles/dashboard.css";
import "../styles/Projects.css";
import "../styles/Environments.css";
import "../styles/Apis.css";

export default function CreateApi() {
  const { organizationId, projectId, environmentId } = useParams();
  const navigate = useNavigate();
  const { showToast } = useToast();
  const { data: environment } = useEnvironment(organizationId, projectId, environmentId);
  const createApi = useCreateApi(organizationId, projectId, environmentId);

  const basePath = `/organizations/${organizationId}/projects/${projectId}/environments/${environmentId}`;

  return (
    <div>
      <EnvironmentTabs active="apis" />

      <Link to={`${basePath}/apis`} className="dashboard-back-link">
        <ChevronLeft className="h-4 w-4" />
        Back to APIs
      </Link>

      <div className="dashboard-card create-project-card">
        <div className="create-project-card-header">
          <div className="dashboard-stat-icon">
            <Server className="h-4 w-4 text-signal" />
          </div>
          <div>
            <p className="dashboard-card-title">Register API</p>
            <p className="text-sm text-fog">in {environment?.name || "this environment"}</p>
          </div>
        </div>

        <div className="mt-5">
          <ApiForm
            onSubmit={async (values) => {
              await createApi.mutateAsync(values);
              showToast("API registered successfully.", {
                type: "success",
              });
              navigate(`${basePath}/apis`, { replace: true });
            }}
            isSubmitting={createApi.isPending}
            submitError={createApi.error?.friendlyMessage}
            submitLabel="Register API"
            savingLabel="Registering…"
            cancelTo={`${basePath}/apis`}
          />
        </div>
      </div>
    </div>
  );
}
