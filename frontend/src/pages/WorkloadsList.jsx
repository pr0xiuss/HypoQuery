import { Link } from "react-router-dom";
import { useWorkloads } from "../hooks/useProduct";
import { Layers3, ChevronRight, Clock, AlertTriangle, Database } from "lucide-react";

export default function WorkloadsList() {
  const { data, isLoading, error } = useWorkloads();

  if (isLoading) {
    return (
      <div className="max-w-7xl mx-auto p-8 animate-pulse">
        <div className="flex items-center justify-between mb-8">
          <div>
            <div className="h-8 w-48 bg-surface rounded-lg mb-2"></div>
            <div className="h-4 w-96 bg-surface rounded"></div>
          </div>
          <div className="h-12 w-32 bg-surface rounded-xl"></div>
        </div>
        <div className="bg-surface border border-divider rounded-2xl overflow-hidden h-96"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-7xl mx-auto p-8">
        <div className="bg-red-500/10 border border-red-500/20 rounded-2xl p-8 text-center">
          <AlertTriangle className="h-12 w-12 text-red-400 mx-auto mb-4" />
          <h3 className="text-xl font-bold text-red-400 mb-2">Failed to load workloads</h3>
          <p className="text-red-400/80 max-w-md mx-auto">
            Unable to reach the HypoQuery API. Please try again later.
          </p>
        </div>
      </div>
    );
  }

  const workloads = data?.workloads || [];
  const totalCount = data?.total_count || 0;

  return (
    <div className="max-w-7xl mx-auto p-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="mb-8 flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <h1 className="text-3xl font-display font-bold text-white tracking-tight">Workloads</h1>
          <p className="text-secondary mt-1.5 text-sm max-w-xl">
            Explore query fingerprints and understand which workloads consume your PostgreSQL system.
          </p>
        </div>
        
        <div className="bg-surface/60 backdrop-blur border border-white/5 rounded-xl px-5 py-3 shadow-lg flex items-center">
          <div className="p-2 bg-indigo-500/10 rounded-lg mr-4">
            <Layers3 className="h-5 w-5 text-indigo-400" />
          </div>
          <div>
            <p className="text-[10px] uppercase font-bold tracking-wider text-secondary">Total Workloads</p>
            <p className="text-2xl font-bold text-white leading-none mt-1">{totalCount}</p>
          </div>
        </div>
      </div>

      <div className="bg-surface/40 backdrop-blur-md border border-white/5 rounded-2xl overflow-hidden shadow-xl shadow-black/20 relative">
        {workloads.length === 0 ? (
          <div className="p-16 text-center">
            <div className="h-20 w-20 bg-signal/10 rounded-2xl flex items-center justify-center mx-auto mb-6 rotate-3 border border-signal/20">
              <Database className="h-10 w-10 text-signal" />
            </div>
            <h3 className="text-xl font-bold text-white mb-2">No Workloads Found</h3>
            <p className="text-secondary max-w-md mx-auto">
              There are no workloads tracked by the system yet. Run your benchmark or application to generate deterministic optimization history.
            </p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-white/5 bg-surface/80">
                  <th className="px-6 py-4 text-xs font-semibold text-secondary uppercase tracking-wider whitespace-nowrap">Fingerprint</th>
                  <th className="px-6 py-4 text-xs font-semibold text-secondary uppercase tracking-wider w-full">SQL Snippet</th>
                  <th className="px-6 py-4 text-xs font-semibold text-secondary uppercase tracking-wider whitespace-nowrap">Executions</th>
                  <th className="px-6 py-4 text-xs font-semibold text-secondary uppercase tracking-wider whitespace-nowrap">Last Executed</th>
                  <th className="px-6 py-4"></th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {workloads.map((w) => (
                  <tr key={w.fingerprint_id} className="hover:bg-white/[0.03] transition-colors group">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="font-mono text-xs text-indigo-300 bg-indigo-500/10 border border-indigo-500/20 px-2.5 py-1 rounded-md shadow-inner">
                        {w.fingerprint_id}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <div className="relative max-w-[200px] sm:max-w-xs md:max-w-md lg:max-w-lg">
                        <span className="text-sm font-mono text-paper truncate block bg-black/20 px-2 py-1 rounded border border-white/5">
                          {w.query_text_snippet}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="inline-flex items-center text-sm font-bold text-white bg-white/10 px-2.5 py-0.5 rounded-full border border-white/10">
                        {w.execution_count}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center text-sm font-medium text-secondary group-hover:text-paper transition-colors">
                        <Clock className="w-4 h-4 mr-2 opacity-70" />
                        {new Date(w.last_executed_at).toLocaleString(undefined, { 
                          month: 'short', day: 'numeric',
                          hour: '2-digit', minute: '2-digit'
                        })}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right">
                      <Link
                        to={`/queries?fingerprint_id=${w.fingerprint_id}`}
                        className="inline-flex items-center justify-center text-sm font-semibold text-white bg-signal hover:bg-signal-hover px-4 py-1.5 rounded-lg transition-all duration-300 shadow-[0_0_15px_rgba(62,111,242,0.2)] hover:shadow-[0_0_20px_rgba(62,111,242,0.4)] transform hover:-translate-y-0.5"
                      >
                        View Queries <ChevronRight className="w-4 h-4 ml-1.5" />
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
