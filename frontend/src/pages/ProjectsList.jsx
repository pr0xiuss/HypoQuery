import { useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import {
  Calendar,
  Clock,
  Database,
  FolderKanban,
  Layers3,
  Pencil,
  Plus,
  Search,
  Server,
  Trash2,
  TriangleAlert,
} from "lucide-react";
import { useOrganization } from "../hooks/useOrganizations";
import {
  useDeleteProject,
  useProjects,
  useUpdateProject,
} from "../hooks/useProjects";
import { useToast } from "../components/toast/ToastProvider";
import EditProjectDialog from "../components/projects/EditProjectDialog";
import DeleteProjectDialog from "../components/projects/DeleteProjectDialog";
import "../styles/Organizations.css";
import "../styles/dashboard.css";
import "../styles/Projects.css";

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

export default function ProjectsList() {
  const { organizationId } = useParams();
  const [search, setSearch] = useState("");
  const [editingProject, setEditingProject] = useState(null);
  const [pendingDelete, setPendingDelete] = useState(null);

  const { showToast } = useToast();
  const { data: organization } = useOrganization(organizationId);
  const { data: projects, isLoading, isError, error, refetch } =
    useProjects(organizationId);
  const updateProject = useUpdateProject(organizationId);
  const deleteProject = useDeleteProject(organizationId);

  const filtered = useMemo(() => {
    if (!projects) return [];
    const q = search.trim().toLowerCase();
    if (!q) return projects;
    return projects.filter((p) => p.name.toLowerCase().includes(q));
  }, [projects, search]);

  const total = projects?.length ?? 0;

  // Placeholder until Environments/Database Connections modules exist.
  const stats = [
    {
      key: "total",
      icon: FolderKanban,
      label: "Total Projects",
      value: isLoading ? "—" : String(total),
      helper: total === 0 ? "No projects yet" : `${total} total`,
    },
    { key: "dev", icon: Layers3, label: "Development Environments", value: "0", helper: "No environments yet" },
    { key: "prod", icon: Server, label: "Production Environments", value: "0", helper: "No environments yet" },
    { key: "connections", icon: Database, label: "Database Connections", value: "0", helper: "No connections yet" },
  ];

  return (
    <div>
      {/* Page header */}
      <div className="orgs-header">
        <div>
          <h1 className="font-display text-2xl font-semibold text-paper">
            Projects
          </h1>
          <p className="mt-1 text-sm text-fog">
            Every project inside {organization?.name || "this organization"}.
          </p>
        </div>
        <Link
          to={`/organizations/${organizationId}/projects/new`}
          className="orgs-primary-btn"
        >
          <Plus className="h-4 w-4" />
          Create Project
        </Link>
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

      {/* Search */}
      <div className="orgs-search">
        <Search className="h-4 w-4 text-fog" />
        <input
          type="text"
          placeholder="Search projects…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      {/* Loading */}
      {isLoading && (
        <div className="projects-grid">
          {[1, 2, 3].map((i) => (
            <div key={i} className="project-card">
              <div className="orgs-skeleton dashboard-skeleton-icon" />
              <div className="orgs-skeleton dashboard-skeleton-title" />
              <div className="orgs-skeleton dashboard-skeleton-text" />
            </div>
          ))}
        </div>
      )}

      {/* Error */}
      {isError && (
        <div className="orgs-error-state">
          <TriangleAlert className="h-5 w-5 text-danger" />
          <div>
            <p className="text-sm font-medium text-paper">
              Couldn&apos;t load projects
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

      {/* Empty state */}
      {!isLoading && !isError && projects && projects.length === 0 && (
        <div className="orgs-empty-state">
          <FolderKanban className="h-8 w-8 text-fog" strokeWidth={1.5} />
          <p className="mt-3 text-sm font-medium text-paper">
            No projects found.
          </p>
          <p className="mt-1 max-w-sm text-sm text-fog">
            Create your first project to start organizing environments and
            database connections.
          </p>
          <Link
            to={`/organizations/${organizationId}/projects/new`}
            className="orgs-primary-btn mt-4"
          >
            <Plus className="h-4 w-4" />
            Create Project
          </Link>
        </div>
      )}

      {/* No search results */}
      {!isLoading &&
        !isError &&
        projects &&
        projects.length > 0 &&
        filtered.length === 0 && (
          <div className="orgs-empty-state">
            <Search className="h-8 w-8 text-fog" strokeWidth={1.5} />
            <p className="mt-3 text-sm font-medium text-paper">
              No projects match &quot;{search}&quot;.
            </p>
          </div>
        )}

      {/* Project cards */}
      {!isLoading && !isError && filtered.length > 0 && (
        <div className="projects-grid">
          {filtered.map((project) => (
            <div key={project.id} className="project-card">
              <div className="project-card-header">
                <div className="project-card-icon">
                  <FolderKanban className="h-4 w-4 text-signal" />
                </div>
                <div className="min-w-0 flex-1">
                  <Link
                    to={`/organizations/${organizationId}/projects/${project.id}`}
                    className="project-card-name"
                  >
                    {project.name}
                  </Link>
                  {project.slug && (
                    <span className="project-card-slug">{project.slug}</span>
                  )}
                </div>
              </div>

              {project.description && (
                <p className="project-card-description" title={project.description}>
                  {project.description}
                </p>
              )}

              <div className="project-card-meta">
                <span className="project-card-meta-item">
                  <Calendar className="h-3.5 w-3.5" />
                  {formatDate(project.created_at)}
                </span>
                <span className="project-card-meta-item">
                  <Clock className="h-3.5 w-3.5" />
                  {formatDate(project.updated_at)}
                </span>
              </div>

              <div className="project-card-actions">
                <Link
                  to={`/organizations/${organizationId}/projects/${project.id}`}
                  className="orgs-primary-btn project-card-open-btn"
                >
                  Open
                </Link>
                <button
                  className="orgs-secondary-btn project-card-icon-btn"
                  onClick={() => setEditingProject(project)}
                  title="Edit project"
                >
                  <Pencil className="h-4 w-4" />
                </button>
                <button
                  className="orgs-secondary-btn project-card-icon-btn"
                  onClick={() => setPendingDelete(project)}
                  title="Delete project"
                >
                  <Trash2 className="h-4 w-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {editingProject && (
        <EditProjectDialog
          project={editingProject}
          onClose={() => setEditingProject(null)}
          onSubmit={async (values) => {
            await updateProject.mutateAsync({
              projectId: editingProject.id,
              payload: values,
            });
            setEditingProject(null);
            showToast("Project updated.", { type: "success" });
          }}
          isSubmitting={updateProject.isPending}
          submitError={updateProject.error?.friendlyMessage}
        />
      )}

      {pendingDelete && (
        <DeleteProjectDialog
          project={pendingDelete}
          onClose={() => setPendingDelete(null)}
          onConfirm={async () => {
            await deleteProject.mutateAsync(pendingDelete.id);
            showToast(`"${pendingDelete.name}" was deleted.`, {
              type: "success",
            });
            setPendingDelete(null);
          }}
          isDeleting={deleteProject.isPending}
        />
      )}
    </div>
  );
}