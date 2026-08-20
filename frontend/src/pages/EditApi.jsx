import { Link, useNavigate, useParams } from "react-router-dom";
import { ChevronLeft, Server, TriangleAlert } from "lucide-react";
import { useApi, useUpdateApi } from "../hooks/useApis";
import { useToast } from "../components/toast/ToastProvider";
import ApiForm from "../components/apis/ApiForm";
import EnvironmentTabs from "../components/envs/EnvironmentTabs";
import "../styles/Organizations.css";
import "../styles/dashboard.css";
import "../styles/Projects.css";
import "../styles/Environments.css";
import "../styles/Apis.css";

export default function EditApi() {
  const { organizationId, projectId, environmentId, apiId } = useParams();
  const navigate = useNavigate();
  const { showToast } = useToast();

  const {
    data: api,
    isLoading,
    isError,
    error,
    refetch,
  } = useApi(organizationId, projectId, environmentId, apiId);
  const updateApi = useUpdateApi(organizationId, projectId, environmentId);

  const basePath = `/organizations/${organizationId}/projects/${projectId}/environments/${environmentId}`;
  const detailsPath = `${basePath}/apis/${apiId}`;

  return (
    <div>
      <EnvironmentTabs active="apis" />

      <Link to={detailsPath} className="dashboard-back-link">
        <ChevronLeft className="h-4 w-4" />
        Back to API Details
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
              Couldn&apos;t load this API
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

      {api && (
        <div className="dashboard-card create-project-card">
          <div className="create-project-card-header">
            <div className="dashboard-stat-icon">
              <Server className="h-4 w-4 text-signal" />
            </div>
            <div>
              <p className="dashboard-card-title">Edit API</p>
              <p className="text-sm text-fog">{api.name}</p>
            </div>
          </div>

          <div className="mt-5">
            <ApiForm
              defaultValues={{
                name: api.name,
                framework: api.framework,
                base_url: api.base_url,
                version: api.version || "",
                description: api.description || "",
                is_active: api.is_active,
              }}
              onSubmit={async (values) => {
                await updateApi.mutateAsync({
                  apiId,
                  payload: values,
                });
                showToast("API updated successfully.", {
                  type: "success",
                });
                navigate(detailsPath, { replace: true });
              }}
              isSubmitting={updateApi.isPending}
              submitError={updateApi.error?.friendlyMessage}
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
