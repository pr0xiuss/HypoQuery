import { useState } from "react";
import { Search, MapPin, TriangleAlert } from "lucide-react";
import { useApiEndpoints } from "../../hooks/useApis";

export default function ApiEndpointList({
  organizationId,
  projectId,
  environmentId,
  apiId,
  onDiscover,
}) {
  const [searchTerm, setSearchTerm] = useState("");
  const [methodFilter, setMethodFilter] = useState("ALL");

  const { data: endpoints, isLoading, isError, error, refetch } = useApiEndpoints(
    organizationId,
    projectId,
    environmentId,
    apiId
  );

  const getMethodColor = (method) => {
    switch (method?.toUpperCase()) {
      case "GET":
        return "text-blue-400 bg-blue-400/10 border-blue-400/20";
      case "POST":
        return "text-green-400 bg-green-400/10 border-green-400/20";
      case "PUT":
        return "text-yellow-400 bg-yellow-400/10 border-yellow-400/20";
      case "PATCH":
        return "text-orange-400 bg-orange-400/10 border-orange-400/20";
      case "DELETE":
        return "text-red-400 bg-red-400/10 border-red-400/20";
      default:
        return "text-fog bg-white/5 border-white/10";
    }
  };

  const filteredEndpoints = endpoints?.filter((ep) => {
    const matchesSearch =
      ep.path.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (ep.summary && ep.summary.toLowerCase().includes(searchTerm.toLowerCase()));
    const matchesMethod = methodFilter === "ALL" || ep.method.toUpperCase() === methodFilter;
    return matchesSearch && matchesMethod;
  });

  if (isLoading) {
    return (
      <div className="py-8 text-center text-fog text-sm">
        <div className="animate-pulse">Loading endpoints...</div>
      </div>
    );
  }

  if (isError) {
    return (
      <div className="orgs-error-state p-6 rounded-lg border border-white/5">
        <TriangleAlert className="h-5 w-5 text-danger" />
        <div>
          <p className="text-sm font-medium text-paper">Couldn&apos;t load endpoints</p>
          <p className="mt-1 text-sm text-fog">
            {error?.friendlyMessage || "Please try again."}
          </p>
        </div>
        <button className="orgs-secondary-btn" onClick={() => refetch()}>
          Retry
        </button>
      </div>
    );
  }

  if (!endpoints || endpoints.length === 0) {
    return (
      <div className="orgs-empty-state py-12">
        <MapPin className="h-8 w-8 text-fog" strokeWidth={1.5} />
        <p className="mt-3 text-sm font-medium text-paper">
          No endpoints have been discovered yet.
        </p>
        <button className="orgs-primary-btn mt-4" onClick={onDiscover}>
          <Search className="h-4 w-4" />
          Discover Endpoints
        </button>
      </div>
    );
  }

  return (
    <div>
      {/* Filters */}
      <div className="flex flex-wrap gap-4 mb-4">
        <div className="flex-1 min-w-[200px] relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-fog" />
          <input
            type="text"
            placeholder="Search paths or summaries..."
            className="dialog-input !pl-9"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        <select
          className="dialog-input !w-auto"
          value={methodFilter}
          onChange={(e) => setMethodFilter(e.target.value)}
        >
          <option value="ALL">All Methods</option>
          <option value="GET">GET</option>
          <option value="POST">POST</option>
          <option value="PUT">PUT</option>
          <option value="PATCH">PATCH</option>
          <option value="DELETE">DELETE</option>
        </select>
      </div>

      {/* Table */}
      {filteredEndpoints.length === 0 ? (
        <div className="py-8 text-center text-sm text-fog border border-dashed border-white/10 rounded-lg">
          No endpoints match your filters.
        </div>
      ) : (
        <div className="apis-table-wrap">
          <table className="apis-table">
            <thead>
              <tr>
                <th>Method</th>
                <th>Path</th>
                <th>Summary</th>
                <th>Auth</th>
                <th>Tags</th>
              </tr>
            </thead>
            <tbody>
              {filteredEndpoints.map((ep) => (
                <tr key={ep.id}>
                  <td>
                    <span
                      className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium border ${getMethodColor(
                        ep.method
                      )}`}
                    >
                      {ep.method.toUpperCase()}
                    </span>
                  </td>
                  <td className="apis-table-mono text-paper font-medium">{ep.path}</td>
                  <td className="max-w-[200px] truncate" title={ep.summary}>
                    {ep.summary || "—"}
                  </td>
                  <td>
                    {ep.authentication_required ? (
                      <span className="text-signal text-xs font-medium">Required</span>
                    ) : (
                      <span className="text-fog text-xs">None</span>
                    )}
                  </td>
                  <td>
                    {ep.tags && ep.tags.length > 0 ? (
                      <div className="flex flex-wrap gap-1">
                        {ep.tags.slice(0, 2).map((tag, idx) => (
                          <span
                            key={idx}
                            className="inline-block bg-white/5 text-fog text-[10px] px-1.5 py-0.5 rounded"
                          >
                            {tag}
                          </span>
                        ))}
                        {ep.tags.length > 2 && (
                          <span className="inline-block bg-white/5 text-fog text-[10px] px-1.5 py-0.5 rounded">
                            +{ep.tags.length - 2}
                          </span>
                        )}
                      </div>
                    ) : (
                      "—"
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
