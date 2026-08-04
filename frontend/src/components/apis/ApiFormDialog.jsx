import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Loader2 } from "lucide-react";
import { FRAMEWORK_OPTIONS, FRAMEWORK_VALUES } from "../../utils/apiFrameworks";
import "../../styles/Organizations.css";

const apiSchema = z.object({
  name: z.string().min(1, "Name is required"),
  framework: z.enum(FRAMEWORK_VALUES, {
    errorMap: () => ({ message: "Select a framework" }),
  }),
  base_url: z.string().min(1, "Base URL is required"),
  version: z.string().optional(),
  description: z.string().optional(),
  is_active: z.boolean().optional(),
});

/**
 * mode: "create" | "edit"
 * api: required when mode === "edit", used to prefill the form.
 * Slug is backend-generated and never shown or requested here.
 */
export default function ApiFormDialog({
  mode = "create",
  api,
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
    resolver: zodResolver(apiSchema),
    defaultValues: {
      name: api?.name || "",
      framework: api?.framework || "",
      base_url: api?.base_url || "",
      version: api?.version || "",
      description: api?.description || "",
      is_active: api ? api.is_active : true,
    },
  });

  return (
    <div className="dialog-overlay" onClick={onClose}>
      <div className="dialog-card" onClick={(e) => e.stopPropagation()}>
        <h2 className="font-display text-lg font-semibold text-paper">
          {isEdit ? "Edit API" : "Register API"}
        </h2>
        <p className="mt-1 text-sm text-fog">
          {isEdit
            ? "Update this API's details."
            : "Register an application API for this environment."}
        </p>

        {submitError && <div className="dialog-error">{submitError}</div>}

        <form className="mt-5" onSubmit={handleSubmit(onSubmit)} noValidate>
          <div className="dialog-field">
            <label className="dialog-label" htmlFor="api-name">
              Name
            </label>
            <input
              id="api-name"
              type="text"
              autoFocus
              placeholder="Billing Service"
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
              placeholder="https://api.example.com"
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
              className="dialog-input"
              {...register("version")}
            />
          </div>

          <div className="dialog-field">
            <label className="dialog-label" htmlFor="api-description">
              Description <span className="text-fog">(optional)</span>
            </label>
            <textarea
              id="api-description"
              rows={3}
              placeholder="What this API is for"
              className="dialog-input"
              {...register("description")}
            />
          </div>

          <div className="dialog-field dialog-checkbox-field">
            <label className="dialog-checkbox-label" htmlFor="api-active">
              <input id="api-active" type="checkbox" {...register("is_active")} />
              Active
            </label>
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
                  {isEdit ? "Saving…" : "Registering…"}
                </>
              ) : isEdit ? (
                "Save Changes"
              ) : (
                "Register API"
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
