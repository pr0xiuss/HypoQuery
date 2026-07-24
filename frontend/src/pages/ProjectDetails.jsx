import { useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import {
  Activity,
  Calendar,
  ChevronLeft,
  Clock,
  Database,
  FileSearch,
  FolderKanban,
  Layers3,
  Lightbulb,
  Pencil,
  Plus,
  Settings as SettingsIcon,
  Trash2,
  TriangleAlert,
} from "lucide-react";
import { useOrganization } from "../hooks/useOrganizations";
import {
  useDeleteProject,
  useProject,
  useUpdateProject,
} from "../hooks/useProjects";
import { useEnvironments } from "../hooks/useEnvironments";
import { useToast } from "../components/toast/ToastProvider";
import EditProjectDialog from "../components/projects/EditProjectDialog";
import DeleteProjectDialog from "../components/projects/DeleteProjectDialog";
import "../styles/Organizations.css";
import "../styles/dashboard.css";

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

// Placeholder until Database Connections / Optimization Reports /
// Recommendations exist on the backend. Environments now has a real count.
function buildStats(environmentCount, isEnvironmentsLoading) {
  return [
    {
      key: "environments",
      icon: Layers3,
      label: "Environments",
      value: isEnvironmentsLoading ? "—" : String(environmentCount),
      helper: environmentCount === 0 ? "No environments yet" : `${environmentCount} total`,
    },
    { key: "connections", icon: Database, label: "Database Connections", value: "0", helper: "No connections yet" },
    { key: "reports", icon: FileSearch, label: "Optimization Reports", value: "0", helper: "No reports yet" },
    { key: "recommendations", icon: Lightbulb, label: "Recommendations", value: "0", helper: "No recommendations yet" },
  ];
}

export default function ProjectDetails() {
  const { organizationId, projectId } = useParams();
  const navigate = useNavigate();
  const { showToast } = useToast();
  const [isEditOpen, setEditOpen] = useState(false);
  const [isDeleteOpen, setDeleteOpen] = useState(false);

  const { data: organization } = useOrganization(organizationId);
  const {
    data: project,
    isLoading,
    isError,
    error,
    refetch,
  } = useProject(organizationId, projectId);
  const updateProject = useUpdateProject(organizationId);
  const deleteProject = useDeleteProject(organizationId);
  const { data: environments, isLoading: isEnvironmentsLoading } =
    useEnvironments(organizationId, projectId);
  const environmentCount = environments?.length ?? 0;
  const stats = buildStats(environmentCount, isEnvironmentsLoading);

  const isNotFound = isError && error?.response?.status === 404;

  return (
    <div>
      <Link
        to={`/organizations/${organizationId}/projects`}
        className="dashboard-back-link"
      >
        <ChevronLeft className="h-4 w-4" />
        Projects
      </Link>

      {/* Loading */}
      {isLoading && (
        <>
          <div className="dashboard-skeleton-card">
            <div className="orgs-skeleton dashboard-skeleton-icon" />
            <div className="orgs-skeleton dashboard-skeleton-title" />
            <div className="orgs-skeleton dashboard-skeleton-text" />
          </div>
          <div className="dashboard-stats-grid">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="dashboard-stat-card">
                <div className="orgs-skeleton dashboard-skeleton-icon" />
                <div className="orgs-skeleton dashboard-skeleton-text" />
              </div>
            ))}
          </div>
        </>
      )}

      {/* Project Not Found */}
      {isNotFound && (
        <div className="orgs-empty-state">
          <FolderKanban className="h-8 w-8 text-fog" strokeWidth={1.5} />
          <p className="mt-3 text-sm font-medium text-paper">
            Project not found.
          </p>
          <p className="mt-1 max-w-sm text-sm text-fog">
            This project may have been deleted, or you may not have access
            to it.
          </p>
        </div>
      )}

      {/* Network / other errors */}
      {isError && !isNotFound && (
        <div className="orgs-error-state">
          <TriangleAlert className="h-5 w-5 text-danger" />
          <div>
            <p className="text-sm font-medium text-paper">
              Couldn&apos;t load this project
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

      {/* Edge case: request succeeded but returned nothing usable */}
      {!isLoading && !isError && !project && (
        <div className="orgs-empty-state">
          <FolderKanban className="h-8 w-8 text-fog" strokeWidth={1.5} />
          <p className="mt-3 text-sm font-medium text-paper">
            Project not found.
          </p>
        </div>
      )}

      {/* Loaded */}
      {project && (
        <>
          {/* Header */}
          <div className="dashboard-detail-header">
            <div className="flex gap-4">
              <div className="dashboard-detail-icon">
                <FolderKanban className="h-6 w-6 text-signal" />
              </div>
              <div className="min-w-0">
                <div className="flex flex-wrap items-center gap-2">
                  <h1 className="font-display text-2xl font-semibold text-paper">
                    {project.name}
                  </h1>
                  {project.slug && (
                    <span className="dashboard-detail-slug">{project.slug}</span>
                  )}
                </div>
                {project.description && (
                  <p className="mt-2 max-w-2xl text-sm leading-relaxed text-fog">
                    {project.description}
                  </p>
                )}
                <div className="dashboard-detail-meta">
                  <span className="dashboard-detail-meta-item">
                    <Calendar className="h-3.5 w-3.5" />
                    Created {formatDate(project.created_at)}
                  </span>
                  <span className="dashboard-detail-meta-item">
                    <Clock className="h-3.5 w-3.5" />
                    Updated {formatDate(project.updated_at)}
                  </span>
                </div>
              </div>
            </div>

            <div className="dashboard-detail-header-actions">
              <button className="orgs-secondary-btn" onClick={() => setEditOpen(true)}>
                <Pencil className="h-4 w-4" />
                Edit Project
              </button>
              <button
                className="orgs-secondary-btn dashboard-danger-btn"
                onClick={() => setDeleteOpen(true)}
              >
                <Trash2 className="h-4 w-4" />
                Delete Project
              </button>
            </div>
          </div>

          {/* Statistics */}
          <div className="dashboard-stats-grid">
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

          {/* Quick Actions — only Create Environment is enabled */}
          <div className="dashboard-card">
            <p className="dashboard-card-title">Quick Actions</p>
            <div className="dashboard-quick-actions-grid">
              <Link
                to={`/organizations/${organizationId}/projects/${projectId}/environments/new`}
                className="dashboard-quick-action-btn dashboard-quick-action-btn-enabled"
              >
                <Plus className="h-4 w-4" />
                <span>Create Environment</span>
              </Link>
              <button className="dashboard-quick-action-btn" disabled>
                <Database className="h-4 w-4" />
                <span>Add Database Connection</span>
                <span className="dashboard-soon-badge">Coming Soon</span>
              </button>
              <button className="dashboard-quick-action-btn" disabled>
                <FileSearch className="h-4 w-4" />
                <span>Run Database Discovery</span>
                <span className="dashboard-soon-badge">Coming Soon</span>
              </button>
              <button className="dashboard-quick-action-btn" disabled>
                <SettingsIcon className="h-4 w-4" />
                <span>Project Settings</span>
                <span className="dashboard-soon-badge">Coming Soon</span>
              </button>
            </div>
          </div>

          {/* Project Information — same layout as Organization Details */}
          <div className="dashboard-card">
            <p className="dashboard-card-title">Project Information</p>
            <div className="dashboard-info-grid">
              <InfoRow label="Project ID" value={project.id} mono />
              <InfoRow
                label="Organization"
                value={organization?.name}
                linkTo={`/organizations/${organizationId}`}
              />
              <InfoRow label="Name" value={project.name} />
              <InfoRow label="Slug" value={project.slug} mono />
              <InfoRow
                label="Description"
                value={project.description || "No description provided"}
              />
              <InfoRow label="Created At" value={formatDate(project.created_at)} />
              <InfoRow label="Updated At" value={formatDate(project.updated_at)} />
            </div>
          </div>

          {/* Upcoming modules */}
          <div className="dashboard-modules-grid">
            <ModuleCard
              icon={Layers3}
              title="Environments"
              message={
                environmentCount > 0
                  ? `${environmentCount} environment${environmentCount === 1 ? "" : "s"} in this project.`
                  : "Environments will appear here."
              }
              linkTo={`/organizations/${organizationId}/projects/${projectId}/environments`}
              linkLabel="View Environments"
            />
            <ModuleCard
              icon={Database}
              title="Database Connections"
              message="Database connections will become available once the Database Connections module is implemented."
            />
            <ModuleCard
              icon={Activity}
              title="Recent Activity"
              message="Recent project activity will become available once activity tracking is implemented."
            />
          </div>
        </>
      )}

      {isEditOpen && (
        <EditProjectDialog
          project={project}
          onClose={() => setEditOpen(false)}
          onSubmit={async (values) => {
            await updateProject.mutateAsync({ projectId, payload: values });
            setEditOpen(false);
            showToast("Project updated.", { type: "success" });
          }}
          isSubmitting={updateProject.isPending}
          submitError={updateProject.error?.friendlyMessage}
        />
      )}

      {isDeleteOpen && project && (
        <DeleteProjectDialog
          project={project}
          onClose={() => setDeleteOpen(false)}
          onConfirm={async () => {
            await deleteProject.mutateAsync(projectId);
            showToast(`"${project.name}" was deleted.`, { type: "success" });
            navigate(`/organizations/${organizationId}/projects`);
          }}
          isDeleting={deleteProject.isPending}
        />
      )}
    </div>
  );
}

function InfoRow({ label, value, mono, linkTo }) {
  return (
    <div className="dashboard-info-row">
      <span className="dashboard-info-label">{label}</span>
      {linkTo && value ? (
        <Link
          to={linkTo}
          className="dashboard-info-value dashboard-info-value-link"
          title={value}
        >
          {value}
        </Link>
      ) : (
        <span
          className={`dashboard-info-value ${mono ? "dashboard-info-value-mono" : ""}`}
          title={typeof value === "string" ? value : undefined}
        >
          {value || "—"}
        </span>
      )}
    </div>
  );
}

function ModuleCard({ icon: Icon, title, message, linkTo, linkLabel }) {
  return (
    <div className="dashboard-module-card">
      <div className="dashboard-module-card-header">
        <Icon className="h-4 w-4 text-fog" />
        <span className="text-sm font-medium text-paper">{title}</span>
      </div>
      <div className="dashboard-module-empty">
        <Icon className="h-6 w-6 text-fog" strokeWidth={1.5} />
        <p className="mt-2 text-sm text-fog">{message}</p>
        {linkTo && (
          <Link to={linkTo} className="dashboard-module-link">
            {linkLabel} →
          </Link>
        )}
      </div>
    </div>
  );
}