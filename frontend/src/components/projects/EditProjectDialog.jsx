import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Loader2 } from "lucide-react";
import "../../styles/Organizations.css";

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

export default function EditProjectDialog({
  project,
  onClose,
  onSubmit,
  isSubmitting,
  submitError,
}) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    resolver: zodResolver(projectSchema),
    defaultValues: {
      name: project?.name || "",
      description: project?.description || "",
    },
  });

  return (
    <div className="dialog-overlay" onClick={onClose}>
      <div className="dialog-card" onClick={(e) => e.stopPropagation()}>
        <h2 className="font-display text-lg font-semibold text-paper">
          Edit Project
        </h2>
        <p className="mt-1 text-sm text-fog">
          Update this project&apos;s name and description.
        </p>

        {submitError && <div className="dialog-error">{submitError}</div>}

        <form className="mt-5" onSubmit={handleSubmit(onSubmit)} noValidate>
          <div className="dialog-field">
            <label className="dialog-label" htmlFor="edit-project-name">
              Project Name
            </label>
            <input
              id="edit-project-name"
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
            <label className="dialog-label" htmlFor="edit-project-description">
              Description <span className="text-fog">(optional)</span>
            </label>
            <textarea
              id="edit-project-description"
              rows={3}
              placeholder="What this project is for"
              className={`dialog-input ${errors.description ? "dialog-input-error" : ""}`}
              {...register("description")}
            />
            {errors.description && (
              <p className="dialog-error-text">{errors.description.message}</p>
            )}
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
                  Saving…
                </>
              ) : (
                "Save Changes"
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
