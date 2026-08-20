import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Link } from "react-router-dom";
import { Loader2 } from "lucide-react";

const ENVIRONMENT_TYPES = ["DEVELOPMENT", "TESTING", "STAGING", "PRODUCTION"];

const environmentSchema = z.object({
  name: z
    .string()
    .min(2, "Environment name must be at least 2 characters")
    .max(100, "Environment name must be at most 100 characters"),
  type: z.enum(ENVIRONMENT_TYPES, {
    errorMap: () => ({ message: "Select an environment type" }),
  }),
  description: z
    .string()
    .max(500, "Description must be at most 500 characters")
    .optional(),
});

/**
 * defaultValues: { name, type, description } — pass the existing
 * environment's fields here to reuse this exact form for editing.
 */
export default function EnvironmentForm({
  defaultValues,
  onSubmit,
  isSubmitting,
  submitError,
  submitLabel,
  savingLabel,
  cancelTo,
}) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    resolver: zodResolver(environmentSchema),
    defaultValues: defaultValues || { name: "", type: "", description: "" },
  });

  return (
    <>
      {submitError && <div className="dialog-error">{submitError}</div>}

      <form onSubmit={handleSubmit(onSubmit)} noValidate>
        <div className="dialog-field">
          <label className="dialog-label" htmlFor="env-name">
            Environment Name
          </label>
          <input
            id="env-name"
            type="text"
            autoFocus
            placeholder="Production"
            className={`dialog-input ${errors.name ? "dialog-input-error" : ""}`}
            {...register("name")}
          />
          {errors.name && (
            <p className="dialog-error-text">{errors.name.message}</p>
          )}
        </div>

        <div className="dialog-field">
          <label className="dialog-label" htmlFor="env-type">
            Environment Type
          </label>
          <select
            id="env-type"
            className={`dialog-input ${errors.type ? "dialog-input-error" : ""}`}
            {...register("type")}
          >
            <option value="">Select a type</option>
            {ENVIRONMENT_TYPES.map((type) => (
              <option key={type} value={type}>
                {type[0].toUpperCase() + type.slice(1)}
              </option>
            ))}
          </select>
          {errors.type && (
            <p className="dialog-error-text">{errors.type.message}</p>
          )}
        </div>

        <div className="dialog-field">
          <label className="dialog-label" htmlFor="env-description">
            Description <span className="text-fog">(optional)</span>
          </label>
          <textarea
            id="env-description"
            rows={3}
            placeholder="What this environment is for"
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
                {savingLabel}
              </>
            ) : (
              submitLabel
            )}
          </button>
          <Link to={cancelTo} className="orgs-secondary-btn">
            Cancel
          </Link>
        </div>
      </form>
    </>
  );
}
