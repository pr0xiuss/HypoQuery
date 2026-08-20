import React, { useMemo, useState } from "react";
import {
  Search,
  MapPin,
  TriangleAlert,
  Shield,
  ShieldAlert,
  Code,
  FileCode,
  Tag,
  ChevronDown,
  ChevronUp,
} from "lucide-react";
import { useApiEndpoints } from "../../hooks/useApis";
import "../../styles/Organizations.css";
import "../../styles/dashboard.css";
import "../../styles/Apis.css";

const HTTP_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"];

function getMethodBadgeClass(method) {
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
}

export default function ApiEndpointList({
  organizationId,
  projectId,
  environmentId,
  apiId,
  onDiscover,
}) {
  const [searchTerm, setSearchTerm] = useState("");
  const [methodFilter, setMethodFilter] = useState("ALL");
  const [authFilter, setAuthFilter] = useState("ALL");
  const [expandedId, setExpandedId] = useState(null);

  const {
    data: endpoints,
    isLoading,
    isError,
    error,
    refetch,
  } = useApiEndpoints(organizationId, projectId, environmentId, apiId);

  const filteredEndpoints = useMemo(() => {
    if (!endpoints) return [];
    const q = searchTerm.trim().toLowerCase();

    return endpoints.filter((ep) => {
      // Search match
      const matchesSearch =
        !q ||
        ep.path?.toLowerCase().includes(q) ||
        ep.summary?.toLowerCase().includes(q) ||
        ep.description?.toLowerCase().includes(q) ||
        ep.handler?.toLowerCase().includes(q) ||
        ep.tags?.some((t) => t.toLowerCase().includes(q));

      // Method match
      const matchesMethod =
        methodFilter === "ALL" || ep.method?.toUpperCase() === methodFilter;

      // Auth match
      const matchesAuth =
        authFilter === "ALL" ||
        (authFilter === "AUTH" && ep.authentication_required) ||
        (authFilter === "PUBLIC" && !ep.authentication_required);

      return matchesSearch && matchesMethod && matchesAuth;
    });
  }, [endpoints, searchTerm, methodFilter, authFilter]);

  const toggleExpand = (id) => {
    setExpandedId((prev) => (prev === id ? null : id));
  };

  // Loading skeleton
  if (isLoading) {
    return (
      <div className="apis-table-wrap">
        <table className="apis-table">
          <thead>
            <tr>
              <th>Method</th>
              <th>Path</th>
              <th>Summary</th>
              <th>Auth</th>
              <th>Handler / Source</th>
              <th>Tags</th>
            </tr>
          </thead>
          <tbody>
            {[1, 2, 3, 4].map((i) => (
              <tr key={i}>
                <td colSpan={6}>
                  <div className="orgs-skeleton apis-skeleton-row" />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }

  // Error state
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

  // Empty state (no endpoints at all)
  if (!endpoints || endpoints.length === 0) {
    return (
      <div className="orgs-empty-state py-12">
        <MapPin className="h-8 w-8 text-fog" strokeWidth={1.5} />
        <p className="mt-3 text-sm font-medium text-paper">
          No endpoints have been discovered yet.
        </p>
        <p className="mt-1 max-w-sm text-xs text-fog">
          Run discovery against an OpenAPI specification to register and synchronize endpoints.
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
      {/* Controls / Filters bar */}
      <div className="flex flex-wrap items-center gap-3 mb-4">
        {/* Search input */}
        <div className="flex-1 min-w-[220px] relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-fog" />
          <input
            type="text"
            placeholder="Search path, handler, summary, tags…"
            className="dialog-input !pl-9"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>

        {/* Method filter */}
        <select
          className="dialog-input !w-auto"
          value={methodFilter}
          onChange={(e) => setMethodFilter(e.target.value)}
        >
          <option value="ALL">All Methods</option>
          {HTTP_METHODS.map((method) => (
            <option key={method} value={method}>
              {method}
            </option>
          ))}
        </select>

        {/* Authentication filter */}
        <select
          className="dialog-input !w-auto"
          value={authFilter}
          onChange={(e) => setAuthFilter(e.target.value)}
        >
          <option value="ALL">All Auth</option>
          <option value="AUTH">Auth Required</option>
          <option value="PUBLIC">Public</option>
        </select>

        {/* Result count badge */}
        <span className="text-xs text-fog whitespace-nowrap self-center">
          {filteredEndpoints.length} of {endpoints.length} endpoints
        </span>
      </div>

      {/* Filtered empty state */}
      {filteredEndpoints.length === 0 ? (
        <div className="py-10 text-center text-sm text-fog border border-dashed border-white/10 rounded-lg">
          No endpoints match your current search and filter criteria.
          <div className="mt-3">
            <button
              className="orgs-secondary-btn text-xs"
              onClick={() => {
                setSearchTerm("");
                setMethodFilter("ALL");
                setAuthFilter("ALL");
              }}
            >
              Reset Filters
            </button>
          </div>
        </div>
      ) : (
        /* Endpoints Table */
        <div className="apis-table-wrap">
          <table className="apis-table">
            <thead>
              <tr>
                <th style={{ width: "100px" }}>Method</th>
                <th>Path</th>
                <th>Summary</th>
                <th style={{ width: "130px" }}>Auth</th>
                <th>Handler / Source</th>
                <th>Tags</th>
                <th style={{ width: "40px" }}></th>
              </tr>
            </thead>
            <tbody>
              {filteredEndpoints.map((ep) => {
                const isExpanded = expandedId === ep.id;
                const hasExtraDetails =
                  ep.description || ep.source_file || ep.line_number || ep.version;

                return (
                  <React.Fragment key={ep.id}>
                    <tr
                      className={`cursor-pointer hover:bg-white/[0.02] ${
                        isExpanded ? "bg-white/[0.03]" : ""
                      }`}
                      onClick={() => toggleExpand(ep.id)}
                    >
                      {/* Method */}
                      <td>
                        <span
                          className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-mono font-semibold border ${getMethodBadgeClass(
                            ep.method
                          )}`}
                        >
                          {ep.method?.toUpperCase()}
                        </span>
                      </td>

                      {/* Path */}
                      <td>
                        <span className="apis-table-mono text-paper font-medium">
                          {ep.path}
                        </span>
                      </td>

                      {/* Summary */}
                      <td>
                        <span className="text-paper text-xs" title={ep.summary || ep.description}>
                          {ep.summary || "—"}
                        </span>
                      </td>

                      {/* Auth */}
                      <td>
                        {ep.authentication_required ? (
                          <span className="inline-flex items-center gap-1 text-signal text-xs font-medium">
                            <ShieldAlert className="h-3.5 w-3.5" />
                            Required
                          </span>
                        ) : (
                          <span className="inline-flex items-center gap-1 text-fog text-xs">
                            <Shield className="h-3.5 w-3.5 opacity-60" />
                            Public
                          </span>
                        )}
                      </td>

                      {/* Handler / Source */}
                      <td>
                        <div className="text-xs text-fog flex flex-col">
                          {ep.handler ? (
                            <span className="font-mono text-paper flex items-center gap-1">
                              <Code className="h-3 w-3 text-signal" />
                              {ep.handler}
                            </span>
                          ) : null}
                          {ep.source_file ? (
                            <span className="text-[11px] text-fog/80 flex items-center gap-1 mt-0.5">
                              <FileCode className="h-3 w-3" />
                              {ep.source_file}
                              {ep.line_number ? `:${ep.line_number}` : ""}
                            </span>
                          ) : null}
                          {!ep.handler && !ep.source_file && "—"}
                        </div>
                      </td>

                      {/* Tags */}
                      <td>
                        {ep.tags && ep.tags.length > 0 ? (
                          <div className="flex flex-wrap gap-1">
                            {ep.tags.slice(0, 3).map((tag, idx) => (
                              <span
                                key={idx}
                                className="inline-flex items-center gap-0.5 bg-white/5 border border-white/5 text-fog text-[10px] px-1.5 py-0.5 rounded"
                              >
                                <Tag className="h-2.5 w-2.5 opacity-60" />
                                {tag}
                              </span>
                            ))}
                            {ep.tags.length > 3 && (
                              <span className="inline-block bg-white/5 text-fog text-[10px] px-1.5 py-0.5 rounded">
                                +{ep.tags.length - 3}
                              </span>
                            )}
                          </div>
                        ) : (
                          "—"
                        )}
                      </td>

                      {/* Expand Arrow */}
                      <td>
                        {hasExtraDetails ? (
                          <button
                            type="button"
                            className="text-fog hover:text-paper p-1"
                            onClick={(e) => {
                              e.stopPropagation();
                              toggleExpand(ep.id);
                            }}
                          >
                            {isExpanded ? (
                              <ChevronUp className="h-4 w-4" />
                            ) : (
                              <ChevronDown className="h-4 w-4" />
                            )}
                          </button>
                        ) : null}
                      </td>
                    </tr>

                    {/* Expanded details row */}
                    {isExpanded && (
                      <tr className="bg-white/[0.02] border-b border-white/5">
                        <td colSpan={7} className="!p-4">
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                            {ep.description && (
                              <div>
                                <span className="font-medium text-fog block mb-1">
                                  Description
                                </span>
                                <p className="text-paper leading-relaxed">{ep.description}</p>
                              </div>
                            )}
                            {ep.handler && (
                              <div>
                                <span className="font-medium text-fog block mb-1">
                                  Handler Function
                                </span>
                                <code className="text-paper font-mono bg-white/5 px-2 py-1 rounded">
                                  {ep.handler}
                                </code>
                              </div>
                            )}
                            {ep.source_file && (
                              <div>
                                <span className="font-medium text-fog block mb-1">
                                  Source Location
                                </span>
                                <code className="text-paper font-mono bg-white/5 px-2 py-1 rounded">
                                  {ep.source_file}
                                  {ep.line_number ? ` (line ${ep.line_number})` : ""}
                                </code>
                              </div>
                            )}
                            {ep.version && (
                              <div>
                                <span className="font-medium text-fog block mb-1">
                                  Version
                                </span>
                                <span className="text-paper">{ep.version}</span>
                              </div>
                            )}
                          </div>
                        </td>
                      </tr>
                    )}
                  </React.Fragment>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
