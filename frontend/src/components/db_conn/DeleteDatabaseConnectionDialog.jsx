import { Loader2 } from "lucide-react";
import "../../styles/Organizations.css";

export default function DeleteDatabaseConnectionDialog({
  connection,
  onClose,
  onConfirm,
  isDeleting,
}) {
  return (
    <div className="dialog-overlay" onClick={onClose}>
      <div className="dialog-card" onClick={(e) => e.stopPropagation()}>
        <h2 className="font-display text-lg font-semibold text-paper">
          Delete Database Connection?
        </h2>
        <p className="mt-2 text-sm text-fog">
          This will permanently delete{" "}
          <span className="text-paper">{connection.name}</span>. This action
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
              "Delete"
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
