import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Link } from "react-router-dom";
import { Loader2 } from "lucide-react";
import { FRAMEWORK_OPTIONS, FRAMEWORK_VALUES } from "../../utils/apiFrameworks";
import "../../styles/Organizations.css";

const apiSchema = z.object({
  name: z
    .string()
    .min(1, "Name is required")
    .max(100, "Name must be at most 100 characters"),
  framework: z.enum(FRAMEWORK_VALUES, {
    errorMap: () => ({ message: "Select a framework" }),
  }),
  base_url: z
    .string()
    .min(1, "Base URL is required")
    .max(500, "Base URL must be at most 500 characters"),
  version: z
    .string()
    .max(50, "Version must be at most 50 characters")
    .optional()
    .or(z.literal("")),
  description: z
    .string()
    .max(500, "Description must be at most 500 characters")
    .optional()
    .or(z.literal("")),
  is_active: z.boolean().default(true),
});

/**
 * Reusable form component for registering and editing APIs.
 *
 * Parameters:
 * - defaultValues: { name, framework, base_url, version, description, is_active }
 * - onSubmit: (values) => Promise<void> | void
 * - isSubmitting: boolean
 * - submitError: string | null
 * - submitLabel: string
 * - savingLabel: string
 * - cancelTo?: string (URL for standalone pages)
 * - onCancel?: () => void (Callback for modal dialogs)
 */
export default function ApiForm({
  defaultValues,
  onSubmit,
  isSubmitting = false,
  submitError = null,
  submitLabel = "Register API",
  savingLabel = "Registering…",
  cancelTo,
  onCancel,
}) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    resolver: zodResolver(apiSchema),
    defaultValues: {
      name: defaultValues?.name || "",
      framework: defaultValues?.framework || "",
      base_url: defaultValues?.base_url || "",
      version: defaultValues?.version || "",
      description: defaultValues?.description || "",
      is_active: defaultValues?.is_active !== undefined ? defaultValues.is_active : true,
    },
  });

  return (
    <>
      {submitError && <div className="dialog-error">{submitError}</div>}

      <form onSubmit={handleSubmit(onSubmit)} noValidate>
        <div className="dialog-field">
          <label className="dialog-label" htmlFor="api-name">
            API Name
          </label>
          <input
            id="api-name"
            type="text"
            autoFocus
            placeholder="Authentication Service"
            className={`dialog-input ${errors.name ? "dialog-input-error" : ""}`}
            {...register("name")}
          />
          {errors.name && <p className="dialog-error-text">{errors.name.message}</p>}
        </div>

        <div className="dialog-field">
          <label className="dialog-label" htmlFor="api-framework">
            Framework
          </label>
          <select
            id="api-framework"
            className={`dialog-input ${errors.framework ? "dialog-input-error" : ""}`}
            {...register("framework")}
          >
            <option value="">Select a framework</option>
            {FRAMEWORK_OPTIONS.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
          {errors.framework && (
            <p className="dialog-error-text">{errors.framework.message}</p>
          )}
        </div>

        <div className="dialog-field">
          <label className="dialog-label" htmlFor="api-base-url">
            Base URL
          </label>
          <input
            id="api-base-url"
            type="text"
            placeholder="https://auth.company.com"
            className={`dialog-input ${errors.base_url ? "dialog-input-error" : ""}`}
            {...register("base_url")}
          />
          {errors.base_url && (
            <p className="dialog-error-text">{errors.base_url.message}</p>
          )}
        </div>

        <div className="dialog-field">
          <label className="dialog-label" htmlFor="api-version">
            Version <span className="text-fog">(optional)</span>
          </label>
          <input
            id="api-version"
            type="text"
            placeholder="v1"
            className={`dialog-input ${errors.version ? "dialog-input-error" : ""}`}
            {...register("version")}
          />
          {errors.version && (
            <p className="dialog-error-text">{errors.version.message}</p>
          )}
        </div>

        <div className="dialog-field">
          <label className="dialog-label" htmlFor="api-description">
            Description <span className="text-fog">(optional)</span>
          </label>
          <textarea
            id="api-description"
            rows={3}
            placeholder="Authentication & identity management service"
            className={`dialog-input ${errors.description ? "dialog-input-error" : ""}`}
            {...register("description")}
          />
          {errors.description && (
            <p className="dialog-error-text">{errors.description.message}</p>
          )}
        </div>

        <div className="dialog-field dialog-checkbox-field">
          <label className="dialog-checkbox-label" htmlFor="api-active">
            <input id="api-active" type="checkbox" {...register("is_active")} />
            Active
          </label>
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
          {cancelTo ? (
            <Link to={cancelTo} className="orgs-secondary-btn">
              Cancel
            </Link>
          ) : onCancel ? (
            <button
              type="button"
              className="orgs-secondary-btn"
              onClick={onCancel}
              disabled={isSubmitting}
            >
              Cancel
            </button>
          ) : null}
        </div>
      </form>
    </>
  );
}
