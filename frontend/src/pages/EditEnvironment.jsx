import { Link, useNavigate, useParams } from "react-router-dom";
import { ChevronLeft, Layers3, TriangleAlert } from "lucide-react";
import {
  useEnvironment,
  useUpdateEnvironment,
} from "../hooks/useEnvironments";
import { useToast } from "../components/toast/ToastProvider";
import EnvironmentForm from "../components/envs/EnvironmentForm";
import "../styles/Organizations.css";
import "../styles/dashboard.css";
import "../styles/Projects.css";

export default function EditEnvironment() {
  const { organizationId, projectId, environmentId } = useParams();
  const navigate = useNavigate();
  const { showToast } = useToast();

  const {
    data: environment,
    isLoading,
    isError,
    error,
    refetch,
  } = useEnvironment(organizationId, projectId, environmentId);
  const updateEnvironment = useUpdateEnvironment(organizationId, projectId);

  const basePath = `/organizations/${organizationId}/projects/${projectId}`;
  const detailsPath = `${basePath}/environments/${environmentId}`;

  return (
    <div>
      <Link to={detailsPath} className="dashboard-back-link">
        <ChevronLeft className="h-4 w-4" />
        Back to Environment
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

      {environment && (
        <div className="dashboard-card create-project-card">
          <div className="create-project-card-header">
            <div className="dashboard-stat-icon">
              <Layers3 className="h-4 w-4 text-signal" />
            </div>
            <div>
              <p className="dashboard-card-title">Edit Environment</p>
              <p className="text-sm text-fog">{environment.name}</p>
            </div>
          </div>

          <div className="mt-5">
            <EnvironmentForm
              defaultValues={{
                name: environment.name,
                type: environment.type,
                description: environment.description || "",
              }}
              onSubmit={async (values) => {
                await updateEnvironment.mutateAsync({
                  environmentId,
                  payload: values,
                });
                showToast("Environment updated.", { type: "success" });
                navigate(detailsPath, { replace: true });
              }}
              isSubmitting={updateEnvironment.isPending}
              submitError={updateEnvironment.error?.friendlyMessage}
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
