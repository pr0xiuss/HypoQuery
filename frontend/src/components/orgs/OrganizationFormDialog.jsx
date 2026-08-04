import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Loader2 } from "lucide-react";
import "../../styles/Organizations.css";

const organizationSchema = z.object({
  name: z.string().min(2, "Name must be at least 2 characters"),
  description: z.string().optional(),
});

/**
 * mode: "create" | "edit"
 * organization: required when mode === "edit", used to prefill the form
 * onSubmit(values): called with the form values on submit
 */
export default function OrganizationFormDialog({
  mode = "create",
  organization,
  onClose,
  onSubmit,
  isSubmitting,
  submitError,
}) {
  const isEdit = mode === "edit";

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    resolver: zodResolver(organizationSchema),
    defaultValues: {
      name: organization?.name || "",
      description: organization?.description || "",
    },
  });

  return (
    <div className="dialog-overlay" onClick={onClose}>
      <div className="dialog-card" onClick={(e) => e.stopPropagation()}>
        <h2 className="font-display text-lg font-semibold text-paper">
          {isEdit ? "Edit Organization" : "Create Organization"}
        </h2>
        <p className="mt-1 text-sm text-fog">
          {isEdit
            ? "Update this organization's name and description."
            : "Organizations are the top level of your account hierarchy."}
        </p>

        {submitError && <div className="dialog-error">{submitError}</div>}

        <form className="mt-5" onSubmit={handleSubmit(onSubmit)} noValidate>
          <div className="dialog-field">
            <label className="dialog-label" htmlFor="org-name">
              Name
            </label>
            <input
              id="org-name"
              type="text"
              autoFocus
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
                  {isEdit ? "Saving…" : "Creating…"}
                </>
              ) : isEdit ? (
                "Save Changes"
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
