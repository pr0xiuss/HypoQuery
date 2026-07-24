import { useNavigate, useParams } from "react-router-dom";
import { ChevronLeft, Layers3 } from "lucide-react";
import { Link } from "react-router-dom";
import { useCreateEnvironment } from "../hooks/useEnvironments";
import { useProject } from "../hooks/useProjects";
import { useToast } from "../components/toast/ToastProvider";
import EnvironmentForm from "../components/envs/EnvironmentForm";
import "../styles/Organizations.css";
import "../styles/dashboard.css";
import "../styles/Projects.css";

export default function CreateEnvironment() {
  const { organizationId, projectId } = useParams();
  const navigate = useNavigate();
  const { showToast } = useToast();
  const { data: project } = useProject(organizationId, projectId);
  const createEnvironment = useCreateEnvironment(organizationId, projectId);

  const basePath = `/organizations/${organizationId}/projects/${projectId}`;

  return (
    <div>
      <Link to={`${basePath}/environments`} className="dashboard-back-link">
        <ChevronLeft className="h-4 w-4" />
        Environments
      </Link>

      <div className="dashboard-card create-project-card">
        <div className="create-project-card-header">
          <div className="dashboard-stat-icon">
            <Layers3 className="h-4 w-4 text-signal" />
          </div>
          <div>
            <p className="dashboard-card-title">Create Environment</p>
            <p className="text-sm text-fog">in {project?.name || "this project"}</p>
          </div>
        </div>

        <div className="mt-5">
          <EnvironmentForm
            onSubmit={async (values) => {
              const environment = await createEnvironment.mutateAsync(values);
              showToast(`"${environment.name}" was created.`, { type: "success" });
              navigate(`${basePath}/environments`, { replace: true });
            }}
            isSubmitting={createEnvironment.isPending}
            submitError={createEnvironment.error?.friendlyMessage}
            submitLabel="Create Environment"
            savingLabel="Creating…"
            cancelTo={`${basePath}/environments`}
          />
        </div>
      </div>
    </div>
  );
}
