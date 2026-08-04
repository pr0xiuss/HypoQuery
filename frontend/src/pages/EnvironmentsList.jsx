import { useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import {
  AlertTriangle,
  Calendar,
  CheckCircle2,
  Clock,
  Layers3,
  Plug,
  Plus,
  Search,
  TriangleAlert,
  XCircle,
} from "lucide-react";
import { useProject } from "../hooks/useProjects";
import { useEnvironments } from "../hooks/useEnvironments";
import EnvironmentTypeBadge from "../components/envs/EnvironmentTypeBadge";
import "../styles/Organizations.css";
import "../styles/dashboard.css";
import "../styles/Environments.css";

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

export default function EnvironmentsList() {
  const { organizationId, projectId } = useParams();
  const [search, setSearch] = useState("");

  const { data: project } = useProject(organizationId, projectId);
  const { data: environments, isLoading, isError, error, refetch } =
    useEnvironments(organizationId, projectId);

  const filtered = useMemo(() => {
    if (!environments) return [];
    const q = search.trim().toLowerCase();
    if (!q) return environments;
    return environments.filter((e) => e.name.toLowerCase().includes(q));
  }, [environments, search]);

  const total = environments?.length ?? 0;

  // Healthy/Warning/Offline are placeholders until connection health exists.
  const stats = [
    {
      key: "total",
      icon: Layers3,
      label: "Total Environments",
      value: isLoading ? "—" : String(total),
      helper: total === 0 ? "No environments yet" : `${total} total`,
    },
    { key: "healthy", icon: CheckCircle2, label: "Healthy", value: "0", helper: "Health checks coming soon" },
    { key: "warning", icon: AlertTriangle, label: "Warning", value: "0", helper: "Health checks coming soon" },
    { key: "offline", icon: XCircle, label: "Offline", value: "0", helper: "Health checks coming soon" },
  ];

  const basePath = `/organizations/${organizationId}/projects/${projectId}`;

  return (
    <div>
      {/* Page header */}
      <div className="orgs-header">
        <div>
          <h1 className="font-display text-2xl font-semibold text-paper">
            Environments
          </h1>
          <p className="mt-1 text-sm text-fog">
            Manage deployment environments for {project?.name || "this project"}.
          </p>
        </div>
        <Link to={`${basePath}/environments/new`} className="orgs-primary-btn">
          <Plus className="h-4 w-4" />
          Create Environment
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
          placeholder="Search environments…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      {/* Loading */}
      {isLoading && (
        <div className="environments-grid">
          {[1, 2, 3].map((i) => (
            <div key={i} className="environment-card">
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
              Couldn&apos;t load environments
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
      {!isLoading && !isError && environments && environments.length === 0 && (
        <div className="orgs-empty-state">
          <Layers3 className="h-8 w-8 text-fog" strokeWidth={1.5} />
          <p className="mt-3 text-sm font-medium text-paper">
            No environments created yet.
          </p>
          <p className="mt-1 max-w-sm text-sm text-fog">
            Create your first deployment environment.
          </p>
          <Link to={`${basePath}/environments/new`} className="orgs-primary-btn mt-4">
            <Plus className="h-4 w-4" />
            Create Environment
          </Link>
        </div>
      )}

      {/* No search results */}
      {!isLoading &&
        !isError &&
        environments &&
        environments.length > 0 &&
        filtered.length === 0 && (
          <div className="orgs-empty-state">
            <Search className="h-8 w-8 text-fog" strokeWidth={1.5} />
            <p className="mt-3 text-sm font-medium text-paper">
              No environments match &quot;{search}&quot;.
            </p>
          </div>
        )}

      {/* Environment cards */}
      {!isLoading && !isError && filtered.length > 0 && (
        <div className="environments-grid">
          {filtered.map((environment) => (
            <Link
              key={environment.id}
              to={`${basePath}/environments/${environment.id}`}
              className="environment-card"
            >
              <div className="environment-card-header">
                <div className="environment-card-icon">
                  <Layers3 className="h-4 w-4 text-signal" />
                </div>
                <div className="min-w-0 flex-1">
                  <p className="environment-card-name">{environment.name}</p>
                  <div className="environment-card-badges">
                    <EnvironmentTypeBadge type={environment.type} />
                    <span className="environment-status-pill">
                      <span className="environment-status-dot" />
                      Unmonitored
                    </span>
                  </div>
                </div>
              </div>

              {environment.description && (
                <p className="environment-card-description" title={environment.description}>
                  {environment.description}
                </p>
              )}

              <div className="environment-card-meta">
                <span className="environment-card-meta-item">
                  <Plug className="h-3.5 w-3.5" />
                  0 connections
                </span>
                <span className="environment-card-meta-item">
                  <Calendar className="h-3.5 w-3.5" />
                  {formatDate(environment.created_at)}
                </span>
                <span className="environment-card-meta-item">
                  <Clock className="h-3.5 w-3.5" />
                  {formatDate(environment.updated_at)}
                </span>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
