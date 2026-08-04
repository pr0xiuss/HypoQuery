import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Link, useNavigate, useParams } from "react-router-dom";
import { ChevronLeft, FolderPlus, Loader2 } from "lucide-react";
import { useCreateProject } from "../hooks/useProjects";
import { useOrganization } from "../hooks/useOrganizations";
import { useToast } from "../components/toast/ToastProvider";
import "../styles/Organizations.css";
import "../styles/dashboard.css";
import "../styles/Projects.css";

const projectSchema = z.object({
  name: z
    .string()
    .min(2, "Project name must be at least 2 characters")
    .max(100, "Project name must be at most 100 characters"),
  description: z
    .string()
    .max(500, "Description must be at most 500 characters")
    .optional(),
});

export default function CreateProject() {
  const { organizationId } = useParams();
  const navigate = useNavigate();
  const { showToast } = useToast();
  const { data: organization } = useOrganization(organizationId);
  const createProject = useCreateProject(organizationId);

  const {
    register,
    handleSubmit,
    setError,
    formState: { errors, isSubmitting },
  } = useForm({
    resolver: zodResolver(projectSchema),
    defaultValues: { name: "", description: "" },
  });

  const onSubmit = async (values) => {
    try {
      const project = await createProject.mutateAsync(values);
      showToast(`"${project.name}" was created.`, { type: "success" });
      navigate(`/organizations/${organizationId}/projects/${project.id}`, {
        replace: true,
      });
    } catch (err) {
      // Values are preserved automatically — react-hook-form only clears
      // on an explicit reset(), which we don't call here.
      setError("root", {
        message:
          err.friendlyMessage ||
          "Unable to create the project. Please try again.",
      });
    }
  };

  return (
    <div>
      <Link
        to={`/organizations/${organizationId}/projects`}
        className="dashboard-back-link"
      >
        <ChevronLeft className="h-4 w-4" />
        Projects
      </Link>

      <div className="dashboard-card create-project-card">
        <div className="create-project-card-header">
          <div className="dashboard-stat-icon">
            <FolderPlus className="h-4 w-4 text-signal" />
          </div>
          <div>
            <p className="dashboard-card-title">Create Project</p>
            <p className="text-sm text-fog">
              in {organization?.name || "this organization"}
            </p>
          </div>
        </div>

        {errors.root && (
          <div className="dialog-error mt-4">{errors.root.message}</div>
        )}

        <form className="mt-5" onSubmit={handleSubmit(onSubmit)} noValidate>
          <div className="dialog-field">
            <label className="dialog-label" htmlFor="project-name">
              Project Name
            </label>
            <input
              id="project-name"
              type="text"
              autoFocus
              placeholder="Customer Analytics"
              className={`dialog-input ${errors.name ? "dialog-input-error" : ""}`}
              {...register("name")}
            />
            {errors.name && (
              <p className="dialog-error-text">{errors.name.message}</p>
            )}
          </div>

          <div className="dialog-field">
            <label className="dialog-label" htmlFor="project-description">
              Description <span className="text-fog">(optional)</span>
            </label>
            <textarea
              id="project-description"
              rows={4}
              placeholder="What this project is for"
              className={`dialog-input ${errors.description ? "dialog-input-error" : ""}`}
              {...register("description")}
            />
            {errors.description && (
              <p className="dialog-error-text">{errors.description.message}</p>
            )}
          </div>

          <div className="dialog-actions create-project-actions">
            <button type="submit" className="orgs-primary-btn" disabled={isSubmitting}>
              {isSubmitting ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Creating…
                </>
              ) : (
                "Create Project"
              )}
            </button>
            <Link
              to={`/organizations/${organizationId}/projects`}
              className="orgs-secondary-btn"
            >
              Cancel
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
}
