import { Loader2 } from "lucide-react";
import "../../styles/Organizations.css";

export default function DeleteProjectDialog({
  project,
  onClose,
  onConfirm,
  isDeleting,
}) {
  return (
    <div className="dialog-overlay" onClick={onClose}>
      <div className="dialog-card" onClick={(e) => e.stopPropagation()}>
        <h2 className="font-display text-lg font-semibold text-paper">
          Delete project?
        </h2>
        <p className="mt-2 text-sm text-fog">
          This will permanently delete{" "}
          <span className="text-paper">{project.name}</span> and every
          environment and database connection inside it. This cannot be
          undone.
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
              "Delete Project"
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
