import { useMemo, useState } from "react";
import {
  Database,
  Eye,
  FunctionSquare,
  Hash,
  Layers3,
  ListOrdered,
  Puzzle,
  Search,
  Table2,
  TriangleAlert,
  Zap,
} from "lucide-react";
import {
  useExtensions,
  useFunctions,
  useIndexes,
  useSchemas,
  useSequences,
  useTables,
  useTriggers,
  useViews,
} from "../../hooks/useDatabaseConnections";
import TableDetailsDialog from "./TableDetailsDialog";
import "../../styles/Apis.css";

const EXPLORER_TABS = [
  { key: "schemas", label: "Schemas", icon: Layers3 },
  { key: "tables", label: "Tables", icon: Table2 },
  { key: "views", label: "Views", icon: Eye },
  { key: "functions", label: "Functions", icon: FunctionSquare },
  { key: "indexes", label: "Indexes", icon: Hash },
  { key: "triggers", label: "Triggers", icon: Zap },
  { key: "sequences", label: "Sequences", icon: ListOrdered },
  { key: "extensions", label: "Extensions", icon: Puzzle },
];

const COLUMNS = {
  schemas: [
    { key: "name", header: "Schema" },
    { key: "table_count", header: "Tables" },
    { key: "view_count", header: "Views" },
    { key: "function_count", header: "Functions" },
  ],
  tables: [
    { key: "schema", header: "Schema" },
    { key: "name", header: "Table" },
    { key: "estimated_rows", header: "Estimated Rows" },
    { key: "size_bytes", header: "Size" },
    { key: "column_count", header: "Columns" },
    { key: "index_count", header: "Indexes" },
    { key: "has_primary_key", header: "Primary Key", boolean: true },
  ],
  views: [
    { key: "schema", header: "Schema" },
    { key: "name", header: "View Name" },
  ],
  functions: [
    { key: "schema", header: "Schema" },
    { key: "name", header: "Function" },
    { key: "return_type", header: "Return Type" },
  ],
  indexes: [
    { key: "schema", header: "Schema" },
    { key: "table_name", header: "Table" },
    { key: "name", header: "Index" },
    { key: "method", header: "Method" },
    { key: "unique", header: "Unique", boolean: true },
    { key: "primary", header: "Primary", boolean: true },
  ],
  triggers: [
    { key: "schema", header: "Schema" },
    { key: "table_name", header: "Table" },
    { key: "name", header: "Trigger" },
    { key: "event", header: "Event" },
    { key: "timing", header: "Timing" },
  ],
  sequences: [
    { key: "schema", header: "Schema" },
    { key: "name", header: "Sequence" },
  ],
  extensions: [
    { key: "name", header: "Extension" },
    { key: "version", header: "Version" },
  ],
};

function formatBytes(bytes) {
  if (bytes == null) return "—";

  const units = ["B", "KB", "MB", "GB", "TB"];
  let size = bytes;
  let unit = 0;

  while (size >= 1024 && unit < units.length - 1) {
    size /= 1024;
    unit++;
  }

  return `${size.toFixed(1)} ${units[unit]}`;
}

export default function ConnectionExplorerTab({
  organizationId,
  projectId,
  environmentId,
  connectionId,
}) {
  const [activeExplorerTab, setActiveExplorerTab] = useState("schemas");
  const [search, setSearch] = useState("");
  const [selectedTable, setSelectedTable] = useState(null); // { schema, name }

  // Every resource's hook is called unconditionally (required by the Rules
  // of Hooks); only the active tab's `enabled` flag is true, so only one
  // actually fetches at a time.
  const schemas = useSchemas(organizationId, projectId, environmentId, connectionId, activeExplorerTab === "schemas");
  const tables = useTables(organizationId, projectId, environmentId, connectionId, activeExplorerTab === "tables");
  const views = useViews(organizationId, projectId, environmentId, connectionId, activeExplorerTab === "views");
  const functions = useFunctions(organizationId, projectId, environmentId, connectionId, activeExplorerTab === "functions");
  const indexes = useIndexes(organizationId, projectId, environmentId, connectionId, activeExplorerTab === "indexes");
  const triggers = useTriggers(organizationId, projectId, environmentId, connectionId, activeExplorerTab === "triggers");
  const sequences = useSequences(organizationId, projectId, environmentId, connectionId, activeExplorerTab === "sequences");
  const extensions = useExtensions(organizationId, projectId, environmentId, connectionId, activeExplorerTab === "extensions");

  const queriesByTab = { schemas, tables, views, functions, indexes, triggers, sequences, extensions };
  const { data, isLoading, isError, error, refetch } = queriesByTab[activeExplorerTab];
  const columns = COLUMNS[activeExplorerTab];
  const activeLabel = EXPLORER_TABS.find((t) => t.key === activeExplorerTab).label;

  // Client-side only — never calls the backend while typing.
  const filtered = useMemo(() => {
    if (!data) return [];
    const q = search.trim().toLowerCase();
    if (!q) return data;
    return data.filter((row) =>
      columns.some((col) => String(row[col.key] ?? "").toLowerCase().includes(q))
    );
  }, [data, search, columns]);

  const handleTabChange = (key) => {
    setActiveExplorerTab(key);
    setSearch("");
  };

  return (
    <div>
      {/* Secondary navigation */}
      <div className="environment-tabs explorer-subnav">
        {EXPLORER_TABS.map(({ key, label, icon: Icon }) => (
          <button
            key={key}
            className={`environment-tab ${activeExplorerTab === key ? "environment-tab-active" : ""}`}
            onClick={() => handleTabChange(key)}
          >
            <Icon className="h-4 w-4" />
            {label}
          </button>
        ))}
      </div>

      {/* Client-side search */}
      <div className="orgs-search explorer-search">
        <Search className="h-4 w-4 text-fog" />
        <input
          type="text"
          placeholder={`Search ${activeLabel.toLowerCase()}…`}
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      {/* Loading */}
      {isLoading && (
        <div className="apis-table-wrap">
          <table className="apis-table">
            <thead>
              <tr>
                {columns.map((col) => (
                  <th key={col.key}>{col.header}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {[1, 2, 3].map((i) => (
                <tr key={i}>
                  <td colSpan={columns.length}>
                    <div className="orgs-skeleton apis-skeleton-row" />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Error */}
      {isError && (
        <div className="orgs-error-state">
          <TriangleAlert className="h-5 w-5 text-danger" />
          <div>
            <p className="text-sm font-medium text-paper">
              Couldn&apos;t load {activeLabel.toLowerCase()}
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
      {!isLoading && !isError && data && data.length === 0 && (
        <div className="orgs-empty-state">
          <Database className="h-8 w-8 text-fog" strokeWidth={1.5} />
          <p className="mt-3 text-sm font-medium text-paper">
            No {activeLabel.toLowerCase()} found
          </p>
        </div>
      )}

      {/* No search results */}
      {!isLoading && !isError && data && data.length > 0 && filtered.length === 0 && (
        <div className="orgs-empty-state">
          <Search className="h-8 w-8 text-fog" strokeWidth={1.5} />
          <p className="mt-3 text-sm font-medium text-paper">
            No {activeLabel.toLowerCase()} match &quot;{search}&quot;.
          </p>
        </div>
      )}

      {/* Table */}
      {!isLoading && !isError && filtered.length > 0 && (
        <div className="apis-table-wrap">
          <table className="apis-table">
            <thead>
              <tr>
                {columns.map((col) => (
                  <th key={col.key}>{col.header}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {filtered.map((row, i) => {
                const isTablesTab = activeExplorerTab === "tables";
                return (
                  <tr
                    key={`${row.schema || ""}-${row.name || row.table_name || i}-${i}`}
                    className={isTablesTab ? "explorer-row-clickable" : ""}
                    onClick={
                      isTablesTab
                        ? () => setSelectedTable({ schema: row.schema, name: row.name })
                        : undefined
                    }
                  >
                    {columns.map((col) => (
                      <td key={col.key}>
                        {col.key === "size_bytes"
                          ? formatBytes(row[col.key])
                          : col.boolean
                            ? (row[col.key] ? "Yes" : "No")
                            : row[col.key] ?? "—"}
                      </td>
                    ))}
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}

      {selectedTable && (
        <TableDetailsDialog
          organizationId={organizationId}
          projectId={projectId}
          environmentId={environmentId}
          connectionId={connectionId}
          schema={selectedTable.schema}
          tableName={selectedTable.name}
          onClose={() => setSelectedTable(null)}
        />
      )}
    </div>
  );
}
