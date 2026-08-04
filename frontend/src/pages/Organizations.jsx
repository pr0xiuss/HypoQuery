import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import {
  Building2,
  Loader2,
  Plus,
  Search,
  Trash2,
  TriangleAlert,
} from "lucide-react";
import {
  useCreateOrganization,
  useDeleteOrganization,
  useOrganizations,
} from "../hooks/useOrganizations";
import "../styles/Organizations.css";
import OrganizationFormDialog from "../components/orgs/OrganizationFormDialog";
import DeleteOrganizationDialog from "../components/orgs/DeleteOrganizationDialog";

const organizationSchema = z.object({
  name: z.string().min(2, "Name must be at least 2 characters"),
  description: z.string().optional(),
});

export default function Organizations() {
  const [search, setSearch] = useState("");
  const [isCreateOpen, setCreateOpen] = useState(false);
  const [pendingDelete, setPendingDelete] = useState(null); // organization or null

  const { data: organizations, isLoading, isError, error, refetch } =
    useOrganizations();
  const createOrganization = useCreateOrganization();
  const deleteOrganization = useDeleteOrganization();

  const filtered = useMemo(() => {
    if (!organizations) return [];
    const q = search.trim().toLowerCase();
    if (!q) return organizations;
    return organizations.filter((org) => org.name.toLowerCase().includes(q));
  }, [organizations, search]);

  return (
    <div>
      {/* Page header */}
      <div className="orgs-header">
        <div>
          <h1 className="font-display text-2xl font-semibold text-paper">
            Organizations
          </h1>
          <p className="mt-1 text-sm text-fog">
            Every organization available to your account.
          </p>
        </div>
        <button className="orgs-primary-btn" onClick={() => setCreateOpen(true)}>
          <Plus className="h-4 w-4" />
          Create Organization
        </button>
      </div>

      {/* Search */}
      <div className="orgs-search">
        <Search className="h-4 w-4 text-fog" />
        <input
          type="text"
          placeholder="Search organizations…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      {/* Loading */}
      {isLoading && (
        <div className="orgs-table">
          {[1, 2, 3].map((i) => (
            <div key={i} className="orgs-row orgs-skeleton-row">
              <div className="orgs-skeleton orgs-skeleton-icon" />
              <div className="orgs-skeleton orgs-skeleton-text" />
              <div className="orgs-skeleton orgs-skeleton-text-short" />
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
              Couldn&apos;t load organizations
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
      {!isLoading && !isError && organizations && organizations.length === 0 && (
        <div className="orgs-empty-state">
          <Building2 className="h-8 w-8 text-fog" strokeWidth={1.5} />
          <p className="mt-3 text-sm font-medium text-paper">
            No organizations found.
          </p>
          <p className="mt-1 max-w-sm text-sm text-fog">
            Create your first organization to start managing projects,
            environments, and database connections.
          </p>
          <button
            className="orgs-primary-btn mt-4"
            onClick={() => setCreateOpen(true)}
          >
            <Plus className="h-4 w-4" />
            Create Organization
          </button>
        </div>
      )}

      {/* No search results (list has data, but the filter matched nothing) */}
      {!isLoading &&
        !isError &&
        organizations &&
        organizations.length > 0 &&
        filtered.length === 0 && (
          <div className="orgs-empty-state">
            <Search className="h-8 w-8 text-fog" strokeWidth={1.5} />
            <p className="mt-3 text-sm font-medium text-paper">
              No organizations match &quot;{search}&quot;.
            </p>
          </div>
        )}

      {/* Table */}
      {!isLoading && !isError && filtered.length > 0 && (
        <div className="orgs-table">
          {filtered.map((org) => (
            <div key={org.id} className="orgs-row">
              <div className="orgs-row-icon">
                <Building2 className="h-4 w-4 text-signal" />
              </div>
              <div className="orgs-row-main">
                <Link to={`/organizations/${org.id}`} className="orgs-row-name">
                  {org.name}
                </Link>
                {org.description && (
                  <p className="orgs-row-description" title={org.description}>
                    {org.description}
                  </p>
                )}
              </div>
              <button
                className="orgs-icon-btn"
                title="Delete organization"
                onClick={() => setPendingDelete(org)}
              >
                <Trash2 className="h-4 w-4" />
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Create dialog */}
      {isCreateOpen && (
        <OrganizationFormDialog
          mode="create"
          onClose={() => setCreateOpen(false)}
          onSubmit={async (values) => {
            await createOrganization.mutateAsync(values);
            setCreateOpen(false);
          }}
          isSubmitting={createOrganization.isPending}
          submitError={createOrganization.error?.friendlyMessage}
        />
      )}

      {/* Delete confirmation */}
      {pendingDelete && (
        <DeleteOrganizationDialog
          organization={pendingDelete}
          onClose={() => setPendingDelete(null)}
          onConfirm={async () => {
            await deleteOrganization.mutateAsync(pendingDelete.id);
            setPendingDelete(null);
          }}
          isDeleting={deleteOrganization.isPending}
        />
      )}
    </div>
  );
}

function CreateOrganizationDialog({ onClose, onCreate, isSubmitting, submitError }) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({ resolver: zodResolver(organizationSchema) });

  return (
    <div className="dialog-overlay" onClick={onClose}>
      <div className="dialog-card" onClick={(e) => e.stopPropagation()}>
        <h2 className="font-display text-lg font-semibold text-paper">
          Create Organization
        </h2>
        <p className="mt-1 text-sm text-fog">
          Organizations are the top level of your account hierarchy.
        </p>

        {submitError && <div className="dialog-error">{submitError}</div>}

        <form className="mt-5" onSubmit={handleSubmit(onCreate)} noValidate>
          <div className="dialog-field">
            <label className="dialog-label" htmlFor="org-name">
              Name
            </label>
            <input
              id="org-name"
              type="text"
              placeholder="Acme Corporation"
              className={`dialog-input ${errors.name ? "dialog-input-error" : ""}`}
              {...register("name")}
            />
            {errors.name && (
              <p className="dialog-error-text">{errors.name.message}</p>
            )}
          </div>

          <div className="dialog-field">
            <label className="dialog-label" htmlFor="org-description">
              Description <span className="text-fog">(optional)</span>
            </label>
            <textarea
              id="org-description"
              rows={3}
              placeholder="What this organization is for"
              className="dialog-input"
              {...register("description")}
            />
          </div>

          <div className="dialog-actions">
            <button
              type="button"
              className="orgs-secondary-btn"
              onClick={onClose}
              disabled={isSubmitting}
            >
              Cancel
            </button>
            <button type="submit" className="orgs-primary-btn" disabled={isSubmitting}>
              {isSubmitting ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Creating…
                </>
              ) : (
                "Create Organization"
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

function ConfirmDeleteDialog({ organization, onClose, onConfirm, isDeleting }) {
  return (
    <div className="dialog-overlay" onClick={onClose}>
      <div className="dialog-card" onClick={(e) => e.stopPropagation()}>
        <h2 className="font-display text-lg font-semibold text-paper">
          Delete organization?
        </h2>
        <p className="mt-2 text-sm text-fog">
          This will permanently delete{" "}
          <span className="text-paper">{organization.name}</span> and every
          project, environment, and database connection inside it. This
          cannot be undone.
        </p>
        <div className="dialog-actions">
          <button
            type="button"
            className="orgs-secondary-btn"
            onClick={onClose}
            disabled={isDeleting}
          >
            Cancel
          </button>
          <button
            type="button"
            className="orgs-danger-btn"
            onClick={onConfirm}
            disabled={isDeleting}
          >
            {isDeleting ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                Deleting…
              </>
            ) : (
              "Delete Organization"
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
