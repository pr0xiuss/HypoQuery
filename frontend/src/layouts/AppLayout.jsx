import { Link, Outlet, useLocation, useNavigate, useParams } from "react-router-dom";
import {
  Building2,
  FolderKanban,
  Layers3,
  Sparkles,
  BookOpen,
  Activity,
  Settings,
  User,
  Database,
  LogOut,
} from "lucide-react";
import { logoutUser } from "../services/authService";
import { invalidateSession } from "../services/api";
import { useOrganization } from "../hooks/useOrganizations";
import { useProject } from "../hooks/useProjects";
import { useEnvironment } from "../hooks/useEnvironments";
import { useDatabaseConnection } from "../hooks/useDatabaseConnections";
import { useApi } from "../hooks/useApis";
import { clearTokens } from "../utils/auth";
import Breadcrumbs from "../components/layout/Breadcrumbs";
import NotificationBell from "../components/notifications/NotificationBell";
import { useQueryClient } from "@tanstack/react-query";
import "../styles/AppLayout.css";

// Organizations is always reachable. Projects and Environments are nested
// resources — their target route depends on which org/project you're
// currently inside, so they're computed per-render instead of being static.

// Static path-segment → label map for breadcrumbs.
const BREADCRUMB_LABELS = {
  organizations: "Organizations",
  projects: "Projects",
  environments: "Environments",
  "database-connections": "Database Connections",
  apis: "APIs",
  settings: "Settings",
};

function useBreadcrumbItems(dynamicLabels) {
  const { pathname } = useLocation();
  const segments = pathname.split("/").filter(Boolean);
  return segments.map((segment, i) => {
    let label = dynamicLabels[segment] || BREADCRUMB_LABELS[segment];
    if (!label) {
      if (segment === "new") {
        const parent = segments[i - 1];
        if (parent === "environments") label = "Create Environment";
        else if (parent === "database-connections") label = "New Connection";
        else if (parent === "apis") label = "Register API";
        else label = "Create Project";
      } else if (segment === "edit") {
        const parent = segments[i - 2];
        if (parent === "database-connections") label = "Edit Connection";
        else if (parent === "apis") label = "Edit API";
        else label = "Edit Environment";
      } else {
        label = segment;
      }
    }
    return { label, to: "/" + segments.slice(0, i + 1).join("/") };
  });
}

export default function AppLayout() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const { organizationId, projectId, environmentId, connectionId, apiId } = useParams();
  const { data: organization } = useOrganization(organizationId);
  const { data: project } = useProject(organizationId, projectId);
  const { data: environment } = useEnvironment(
    organizationId,
    projectId,
    environmentId
  );
  const { data: connection } = useDatabaseConnection(
    organizationId,
    projectId,
    environmentId,
    connectionId
  );
  const { data: api } = useApi(
    organizationId,
    projectId,
    environmentId,
    apiId
  );

  const dynamicLabels = {
    ...(organizationId && { [organizationId]: organization?.name || "…" }),
    ...(projectId && { [projectId]: project?.name || "…" }),
    ...(environmentId && { [environmentId]: environment?.name || "…" }),
    ...(connectionId && { [connectionId]: connection?.name || "…" }),
    ...(apiId && { [apiId]: api?.name || "…" }),
  };
  const breadcrumbItems = useBreadcrumbItems(dynamicLabels);

  // Projects/Environments are nested resources — only enabled once you're
  // inside the org/project they belong to.
  const projectsTo = organizationId
    ? `/organizations/${organizationId}/projects`
    : null;
  const environmentsTo =
    organizationId && projectId
      ? `/organizations/${organizationId}/projects/${projectId}/environments`
      : null;

  async function handleLogout() {
    // Bump this first, synchronously — any refresh already in flight will
    // see a mismatched epoch when it resolves and discard its result.
    invalidateSession();
    try {
      await logoutUser();
    } catch {
      // Ignore network errors — clear local session either way.
    } finally {
      clearTokens();
      queryClient.clear();
      navigate("/login", { replace: true });
    }
  }

  return (
    <div className="app-shell">
      <aside className="app-sidebar">
        <div className="app-sidebar-brand">
          <div className="flex h-7 w-7 items-center justify-center rounded-md bg-signal">
            <Database className="h-4 w-4 text-paper" strokeWidth={2.5} />
          </div>
          <span className="font-display text-base font-semibold tracking-tight text-paper">
            HypoQuery
          </span>
        </div>

        <nav className="app-sidebar-nav">
          <Link to="/organizations" className="app-nav-item app-nav-item-active">
            <Building2 className="h-4 w-4" strokeWidth={2} />
            Organizations
          </Link>

          {projectsTo ? (
            <Link to={projectsTo} className="app-nav-item app-nav-item-active">
              <FolderKanban className="h-4 w-4" strokeWidth={2} />
              Projects
            </Link>
          ) : (
            <span
              className="app-nav-item app-nav-item-disabled"
              title="Select an organization first"
            >
              <FolderKanban className="h-4 w-4" strokeWidth={2} />
              Projects
            </span>
          )}

          {environmentsTo ? (
            <Link to={environmentsTo} className="app-nav-item app-nav-item-active">
              <Layers3 className="h-4 w-4" strokeWidth={2} />
              Environments
            </Link>
          ) : (
            <span
              className="app-nav-item app-nav-item-disabled"
              title="Select a project first"
            >
              <Layers3 className="h-4 w-4" strokeWidth={2} />
              Environments
            </span>
          )}

          <Link to="/dashboard" className="app-nav-item app-nav-item-active">
            <Activity className="h-4 w-4" strokeWidth={2} />
            Dashboard
          </Link>

          <Link to="/workloads" className="app-nav-item app-nav-item-active">
            <Layers3 className="h-4 w-4" strokeWidth={2} />
            Workloads
          </Link>

          <Link to="/queries" className="app-nav-item app-nav-item-active">
            <BookOpen className="h-4 w-4" strokeWidth={2} />
            Queries
          </Link>

          <Link to="/operations" className="app-nav-item app-nav-item-active">
            <Sparkles className="h-4 w-4" strokeWidth={2} />
            Operations
          </Link>
        </nav>

        <div className="app-sidebar-footer">
          <Link to="/settings" className="app-nav-item app-nav-item-active">
            <Settings className="h-4 w-4" strokeWidth={2} />
            Settings
          </Link>
          <span className="app-nav-item app-nav-item-disabled">
            <User className="h-4 w-4" strokeWidth={2} />
            Profile
            <span className="app-nav-soon">Soon</span>
          </span>
          <button className="app-nav-item app-nav-item-active app-logout-btn" onClick={handleLogout}>
            <LogOut className="h-4 w-4" strokeWidth={2} />
            Log out
          </button>
        </div>
      </aside>

      <div className="app-main">
        <header className="app-topnav">
          <Breadcrumbs items={breadcrumbItems} />
          <div className="flex items-center space-x-4">
            <NotificationBell />
          </div>
        </header>

        <main className="app-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
