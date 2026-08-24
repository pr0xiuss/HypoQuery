import React from "react";
import { Link, useSearchParams } from "react-router-dom";
import { useQueries } from "../hooks/useProduct";
import { BookOpen, ChevronRight, Clock, Zap, Database } from "lucide-react";

export default function QueriesList() {
  const [searchParams] = useSearchParams();
  const fingerprintId = searchParams.get("fingerprint_id");

  const { data, isLoading, error } = useQueries(fingerprintId);

  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh]">
        <div className="w-10 h-10 border-4 border-signal border-t-transparent rounded-full animate-spin mb-4"></div>
        <div className="text-secondary font-medium">Loading queries...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-8 max-w-2xl mx-auto mt-10 bg-red-500/10 border border-red-500/20 rounded-xl text-red-400 flex items-center">
        <div className="p-3 bg-red-500/20 rounded-lg mr-4">
          <Database className="w-6 h-6" />
        </div>
        <div>
          <h3 className="font-semibold text-lg">Failed to load queries</h3>
          <p className="text-sm opacity-80 mt-1">Check your connection or try again later.</p>
        </div>
      </div>
    );
  }

  const queries = data?.queries || [];

  return (
    <div className="max-w-7xl mx-auto p-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="mb-10">
        <h1 className="text-4xl font-display font-bold bg-gradient-to-r from-blue-400 via-indigo-400 to-purple-400 bg-clip-text text-transparent pb-2">
          Query Executions
        </h1>
        <p className="text-secondary text-lg mt-1 max-w-2xl">
          {fingerprintId ? (
            <span className="flex items-center gap-2">
              Filtering by workload: 
              <span className="font-mono text-xs text-blue-300 bg-blue-500/10 border border-blue-500/20 px-2 py-1 rounded-md shadow-inner">
                {fingerprintId}
              </span>
            </span>
          ) : (
            "Explore and analyze detailed query executions tracked by the deterministic engine."
          )}
        </p>
      </div>

      <div className="bg-surface/40 backdrop-blur-xl border border-white/5 rounded-2xl overflow-hidden shadow-2xl shadow-black/20">
        {queries.length === 0 ? (
          <div className="p-16 text-center">
            <div className="inline-flex p-4 rounded-full bg-surface-hover mb-4 ring-1 ring-white/10 shadow-lg">
              <BookOpen className="h-10 w-10 text-secondary" />
            </div>
            <h3 className="text-xl font-medium text-paper">No Queries Found</h3>
            <p className="text-secondary mt-2 max-w-sm mx-auto">
              There are no query executions tracked for this workload yet.
            </p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-white/5 bg-surface/80">
                  <th className="px-6 py-5 text-xs font-semibold text-secondary uppercase tracking-wider">Query ID</th>
                  <th className="px-6 py-5 text-xs font-semibold text-secondary uppercase tracking-wider">SQL Snippet</th>
                  <th className="px-6 py-5 text-xs font-semibold text-secondary uppercase tracking-wider">Duration</th>
                  <th className="px-6 py-5 text-xs font-semibold text-secondary uppercase tracking-wider">Executed At</th>
                  <th className="px-6 py-5"></th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {queries.map((q) => (
                  <tr key={q.query_id} className="group hover:bg-surface-hover/60 transition-all duration-300">
                    <td className="px-6 py-5 whitespace-nowrap">
                      <span className="font-mono text-xs text-indigo-300 bg-indigo-500/10 border border-indigo-500/20 px-2 py-1 rounded shadow-inner">
                        {q.query_id.substring(0, 8)}
                      </span>
                    </td>
                    <td className="px-6 py-5">
                      <span className="text-sm font-mono text-slate-300 truncate max-w-sm block group-hover:text-blue-200 transition-colors">
                        {q.query_text.substring(0, 80)}{q.query_text.length > 80 ? "..." : ""}
                      </span>
                    </td>
                    <td className="px-6 py-5 whitespace-nowrap">
                      <div className="flex items-center text-sm font-medium text-paper">
                        <Zap className="w-4 h-4 mr-2 text-yellow-500 group-hover:scale-110 transition-transform" />
                        {q.execution_time_ms.toFixed(2)} ms
                      </div>
                    </td>
                    <td className="px-6 py-5 whitespace-nowrap">
                      <div className="flex items-center text-sm text-secondary group-hover:text-slate-300 transition-colors">
                        <Clock className="w-4 h-4 mr-2 opacity-70" />
                        {new Date(q.timestamp).toLocaleString(undefined, { 
                          month: 'short', day: 'numeric', 
                          hour: '2-digit', minute: '2-digit', second: '2-digit' 
                        })}
                      </div>
                    </td>
                    <td className="px-6 py-5 whitespace-nowrap text-right">
                      <Link
                        to={`/queries/${q.query_id}`}
                        className="inline-flex items-center justify-center px-4 py-2 rounded-lg text-sm font-medium text-white bg-white/5 hover:bg-signal hover:text-white border border-white/10 hover:border-signal-hover transition-all duration-300 shadow-sm"
                      >
                        View Details <ChevronRight className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" />
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
