import { useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import {
  Activity,
  Building2,
  Calendar,
  ChevronLeft,
  Clock,
  Database,
  FolderKanban,
  Layers3,
  Pencil,
  Plus,
  Settings as SettingsIcon,
  Trash2,
  TriangleAlert,
  UserPlus,
  Users,
} from "lucide-react";
import {
  useDeleteOrganization,
  useOrganization,
  useUpdateOrganization,
} from "../hooks/useOrganizations";
import { useProjects } from "../hooks/useProjects";
import { useToast } from "../components/toast/ToastProvider";
import OrganizationFormDialog from "../components/orgs/OrganizationFormDialog";
import DeleteOrganizationDialog from "../components/orgs/DeleteOrganizationDialog";
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

export default function OrganizationDetails() {
  const { organizationId } = useParams();
  const navigate = useNavigate();
  const { showToast } = useToast();
  const [isEditOpen, setEditOpen] = useState(false);
  const [isDeleteOpen, setDeleteOpen] = useState(false);

  const {
    data: organization,
    isLoading,
    isError,
    error,
    refetch,
  } = useOrganization(organizationId);
  const updateOrganization = useUpdateOrganization(organizationId);
  const deleteOrganization = useDeleteOrganization();

  // Real count for the one stat that already has a backend module.
  const { data: projects, isLoading: isProjectsLoading } =
    useProjects(organizationId);
  const projectCount = projects?.length ?? 0;

  const stats = [
    {
      key: "projects",
      icon: FolderKanban,
      label: "Projects",
      value: isProjectsLoading ? "—" : String(projectCount),
      helper: projectCount === 0 ? "No projects yet" : `${projectCount} total`,
    },
    { key: "members", icon: Users, label: "Members", value: "0", helper: "No members yet" },
    { key: "environments", icon: Layers3, label: "Environments", value: "0", helper: "No environments yet" },
    { key: "connections", icon: Database, label: "Database Connections", value: "0", helper: "No connections yet" },
  ];

  const isNotFound = isError && error?.response?.status === 404;

  return (
    <div>
      <Link to="/organizations" className="dashboard-back-link">
        <ChevronLeft className="h-4 w-4" />
        Organizations
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

      {/* 404 */}
      {isNotFound && (
        <div className="orgs-empty-state">
          <Building2 className="h-8 w-8 text-fog" strokeWidth={1.5} />
          <p className="mt-3 text-sm font-medium text-paper">
            Organization not found.
          </p>
          <p className="mt-1 max-w-sm text-sm text-fog">
            This organization may have been deleted, or you may not have
            access to it.
          </p>
        </div>
      )}

      {/* Other errors */}
      {isError && !isNotFound && (
        <div className="orgs-error-state">
          <TriangleAlert className="h-5 w-5 text-danger" />
          <div>
            <p className="text-sm font-medium text-paper">
              Couldn&apos;t load this organization
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
      {!isLoading && !isError && !organization && (
        <div className="orgs-empty-state">
          <Building2 className="h-8 w-8 text-fog" strokeWidth={1.5} />
          <p className="mt-3 text-sm font-medium text-paper">
            Organization not found.
          </p>
        </div>
      )}

      {/* Loaded */}
      {organization && (
        <>
          {/* Header */}
          <div className="dashboard-detail-header">
            <div className="flex gap-4">
              <div className="dashboard-detail-icon">
                <Building2 className="h-6 w-6 text-signal" />
              </div>
              <div className="min-w-0">
                <div className="flex flex-wrap items-center gap-2">
                  <h1 className="font-display text-2xl font-semibold text-paper">
                    {organization.name}
                  </h1>
                  {organization.slug && (
                    <span className="dashboard-detail-slug">{organization.slug}</span>
                  )}
                </div>
                {organization.description && (
                  <p className="mt-2 max-w-2xl text-sm leading-relaxed text-fog">
                    {organization.description}
                  </p>
                )}
                <div className="dashboard-detail-meta">
                  <span className="dashboard-detail-meta-item">
                    <Calendar className="h-3.5 w-3.5" />
                    Created {formatDate(organization.created_at)}
                  </span>
                  <span className="dashboard-detail-meta-item">
                    <Clock className="h-3.5 w-3.5" />
                    Updated {formatDate(organization.updated_at)}
                  </span>
                </div>
              </div>
            </div>

            <div className="dashboard-detail-header-actions">
              <button className="orgs-secondary-btn" onClick={() => setEditOpen(true)}>
                <Pencil className="h-4 w-4" />
                Edit Organization
              </button>
              <button
                className="orgs-secondary-btn dashboard-danger-btn"
                onClick={() => setDeleteOpen(true)}
              >
                <Trash2 className="h-4 w-4" />
                Delete Organization
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

          {/* Quick Actions */}
          <div className="dashboard-card">
            <p className="dashboard-card-title">Quick Actions</p>
            <div className="dashboard-quick-actions-grid">
              <Link
                to={`/organizations/${organizationId}/projects/new`}
                className="dashboard-quick-action-btn dashboard-quick-action-btn-enabled"
              >
                <Plus className="h-4 w-4" />
                <span>Create Project</span>
              </Link>
              <button className="dashboard-quick-action-btn" disabled>
                <UserPlus className="h-4 w-4" />
                <span>Invite Member</span>
                <span className="dashboard-soon-badge">Coming Soon</span>
              </button>
              <button className="dashboard-quick-action-btn" disabled>
                <Layers3 className="h-4 w-4" />
                <span>Add Database Connection</span>
                <span className="dashboard-soon-badge">Coming Soon</span>
              </button>
              <button className="dashboard-quick-action-btn" disabled>
                <SettingsIcon className="h-4 w-4" />
                <span>Organization Settings</span>
                <span className="dashboard-soon-badge">Coming Soon</span>
              </button>
            </div>
          </div>

          {/* Organization Information */}
          <div className="dashboard-card">
            <p className="dashboard-card-title">Organization Information</p>
            <div className="dashboard-info-grid">
              <InfoRow label="Organization ID" value={organization.id} mono />
              <InfoRow label="Name" value={organization.name} />
              <InfoRow label="Slug" value={organization.slug} mono />
              <InfoRow
                label="Description"
                value={organization.description || "No description provided"}
              />
              <InfoRow label="Created At" value={formatDate(organization.created_at)} />
              <InfoRow label="Updated At" value={formatDate(organization.updated_at)} />
            </div>
          </div>

          {/* Upcoming modules */}
          <div className="dashboard-modules-grid">
            <ModuleCard
              icon={FolderKanban}
              title="Projects"
              message={
                projectCount > 0
                  ? `${projectCount} project${projectCount === 1 ? "" : "s"} in this organization.`
                  : "Projects will appear here."
              }
              linkTo={`/organizations/${organizationId}/projects`}
              linkLabel="View Projects"
            />
            <ModuleCard
              icon={Users}
              title="Members"
              message="Organization members will appear here."
            />
            <ModuleCard
              icon={Activity}
              title="Activity"
              message="Recent organization activity will appear here."
            />
          </div>
        </>
      )}

      {isEditOpen && (
        <OrganizationFormDialog
          mode="edit"
          organization={organization}
          onClose={() => setEditOpen(false)}
          onSubmit={async (values) => {
            await updateOrganization.mutateAsync(values);
            setEditOpen(false);
            showToast("Organization updated.", { type: "success" });
          }}
          isSubmitting={updateOrganization.isPending}
          submitError={updateOrganization.error?.friendlyMessage}
        />
      )}

      {isDeleteOpen && organization && (
        <DeleteOrganizationDialog
          organization={organization}
          onClose={() => setDeleteOpen(false)}
          onConfirm={async () => {
            await deleteOrganization.mutateAsync(organizationId);
            showToast(`"${organization.name}" was deleted.`, { type: "success" });
            navigate("/organizations");
          }}
          isDeleting={deleteOrganization.isPending}
        />
      )}
    </div>
  );
}

function InfoRow({ label, value, mono }) {
  return (
    <div className="dashboard-info-row">
      <span className="dashboard-info-label">{label}</span>
      <span
        className={`dashboard-info-value ${mono ? "dashboard-info-value-mono" : ""}`}
        title={typeof value === "string" ? value : undefined}
      >
        {value || "—"}
      </span>
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