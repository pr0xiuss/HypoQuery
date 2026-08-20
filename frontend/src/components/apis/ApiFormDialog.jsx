import ApiForm from "./ApiForm";
import "../../styles/Organizations.css";

/**
 * Modal dialog for registering and editing APIs.
 *
 * Parameters:
 * - mode: "create" | "edit"
 * - api: existing API object when mode === "edit"
 * - onClose: () => void
 * - onSubmit: (values) => Promise<void>
 * - isSubmitting: boolean
 * - submitError: string | null
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

        <div className="mt-5">
          <ApiForm
            defaultValues={
              api
                ? {
                    name: api.name,
                    framework: api.framework,
                    base_url: api.base_url,
                    version: api.version || "",
                    description: api.description || "",
                    is_active: api.is_active,
                  }
                : undefined
            }
            onSubmit={onSubmit}
            isSubmitting={isSubmitting}
            submitError={submitError}
            submitLabel={isEdit ? "Save Changes" : "Register API"}
            savingLabel={isEdit ? "Saving…" : "Registering…"}
            onCancel={onClose}
          />
        </div>
      </div>
    </div>
  );
}
