import { Hash, Loader2, Rows, ShieldCheck, TriangleAlert, X } from "lucide-react";
import { useTableDetails } from "../../hooks/useDatabaseConnections";
import "../../styles/Organizations.css";
import "../../styles/dashboard.css";
import "../../styles/Apis.css";

export default function TableDetailsDialog({
  organizationId,
  projectId,
  environmentId,
  connectionId,
  schema,
  tableName,
  onClose,
}) {
  const {
    data: table,
    isLoading,
    isError,
    error,
    refetch,
  } = useTableDetails(organizationId, projectId, environmentId, connectionId, schema, tableName);

  return (
    <div className="dialog-overlay" onClick={onClose}>
      <div className="dialog-card table-details-card" onClick={(e) => e.stopPropagation()}>
        <div className="table-details-header">
          <div>
            <h2 className="font-display text-lg font-semibold text-paper">
              {tableName}
            </h2>
            <p className="mt-1 text-sm text-fog">Schema: {schema}</p>
          </div>
          <button className="table-details-close" onClick={onClose} aria-label="Close">
            <X className="h-4 w-4" />
          </button>
        </div>

        {isLoading && (
          <div className="table-details-loading">
            <Loader2 className="h-5 w-5 animate-spin text-fog" />
          </div>
        )}

        {isError && (
          <div className="orgs-error-state mt-4">
            <TriangleAlert className="h-5 w-5 text-danger" />
            <div>
              <p className="text-sm font-medium text-paper">
                Couldn&apos;t load table details
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

        {table && (
          <>
            <div className="dashboard-info-grid mt-5">
              <div className="dashboard-info-row">
                <span className="dashboard-info-label">Table Name</span>
                <span className="dashboard-info-value">{table.name}</span>
              </div>
              <div className="dashboard-info-row">
                <span className="dashboard-info-label">Schema</span>
                <span className="dashboard-info-value">{table.schema}</span>
              </div>
            </div>

            <p className="table-details-section-title">
              <Hash className="h-3.5 w-3.5" />
              Indexes
            </p>
            {table.indexes && table.indexes.length > 0 ? (
              <div className="apis-table-wrap">
                <table className="apis-table">
                  <thead>
                    <tr>
                      <th>Name</th>
                      <th>Method</th>
                      <th>Unique</th>
                      <th>Primary</th>
                    </tr>
                  </thead>
                  <tbody>
                    {table.indexes.map((index) => (
                      <tr key={index.name}>
                        <td>{index.name}</td>
                        <td>{index.method}</td>
                        <td>{index.unique ? "Yes" : "No"}</td>
                        <td>{index.primary ? "Yes" : "No"}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <p className="text-sm text-fog">No indexes found</p>
            )}

            <p className="table-details-section-title">
              <Rows className="h-3.5 w-3.5" />
              Columns
            </p>
            {table.columns && table.columns.length > 0 ? (
              <div className="apis-table-wrap">
                <table className="apis-table">
                  <thead>
                    <tr>
                      <th>Name</th>
                      <th>Data Type</th>
                      <th>Nullable</th>
                      <th>Default</th>
                    </tr>
                  </thead>
                  <tbody>
                    {table.columns.map((column) => (
                      <tr key={column.name}>
                        <td>{column.name}</td>
                        <td>{column.data_type}</td>
                        <td>{column.nullable ? "Yes" : "No"}</td>
                        <td>{column.default_value ?? "—"}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <p className="text-sm text-fog">No columns found</p>
            )}

            <p className="table-details-section-title">
              <ShieldCheck className="h-3.5 w-3.5" />
              Constraints
            </p>
            {table.constraints && table.constraints.length > 0 ? (
              <div className="apis-table-wrap">
                <table className="apis-table">
                  <thead>
                    <tr>
                      <th>Name</th>
                      <th>Type</th>
                      <th>Definition</th>
                    </tr>
                  </thead>
                  <tbody>
                    {table.constraints.map((constraint) => (
                      <tr key={constraint.name}>
                        <td>{constraint.name}</td>
                        <td>{constraint.constraint_type}</td>
                        <td>{constraint.definition || "—"}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <p className="text-sm text-fog">No constraints found</p>
            )}
          </>
        )}
      </div>
    </div>
  );
}
