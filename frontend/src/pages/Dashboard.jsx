import { Link } from "react-router-dom";
import { useDashboard, useWorkloads, useOperations } from "../hooks/useProduct";
import { 
  Activity, 
  Layers3, 
  Zap, 
  Database,
  ChevronRight,
  Clock,
  CheckCircle2,
  XCircle,
  Loader2,
  AlertTriangle
} from "lucide-react";

function getStatusIcon(status) {
  switch (status?.toLowerCase()) {
    case "completed": return <CheckCircle2 className="w-4 h-4 text-green-500" />;
    case "failed": return <XCircle className="w-4 h-4 text-red-500" />;
    case "running":
    case "in_progress": return <Loader2 className="w-4 h-4 text-signal animate-spin" />;
    default: return <span className="w-2 h-2 rounded-full bg-secondary"></span>;
  }
}

function getStatusClass(status) {
  switch (status?.toLowerCase()) {
    case "completed": return "text-green-400 bg-green-500/10 border-green-500/20";
    case "failed": return "text-red-400 bg-red-500/10 border-red-500/20";
    case "running":
    case "in_progress": return "text-signal bg-signal/10 border-signal/20";
    default: return "text-secondary bg-surface-hover border-divider";
  }
}

export default function Dashboard() {
  const { data: dashboard, isLoading: isDashLoading, error: dashError } = useDashboard();
  const { data: workloadsData, isLoading: isWorkloadsLoading } = useWorkloads(5, 0);
  const { data: operationsData, isLoading: isOpsLoading } = useOperations(5, 0);

  if (isDashLoading) {
    return (
      <div className="max-w-7xl mx-auto p-8 animate-pulse">
        <div className="h-10 w-64 bg-surface rounded-lg mb-2"></div>
        <div className="h-4 w-96 bg-surface rounded mb-10"></div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
          {[1, 2, 3].map(i => (
            <div key={i} className="h-32 bg-surface rounded-2xl border border-divider"></div>
          ))}
        </div>
      </div>
    );
  }

  if (dashError) {
    return (
      <div className="max-w-7xl mx-auto p-8">
        <div className="bg-red-500/10 border border-red-500/20 rounded-2xl p-8 text-center">
          <AlertTriangle className="h-12 w-12 text-red-400 mx-auto mb-4" />
          <h3 className="text-xl font-bold text-red-400 mb-2">Platform Connection Failed</h3>
          <p className="text-red-400/80 max-w-md mx-auto">
            Unable to reach the HypoQuery API. Please ensure the deterministic optimization engine and backend services are running.
          </p>
        </div>
      </div>
    );
  }

  const stats = dashboard?.stats || { total_workloads: 0, active_queries: 0, optimizations_applied: 0 };
  const workloads = workloadsData?.workloads || [];
  const operations = operationsData?.operations || [];

  return (
    <div className="max-w-7xl mx-auto p-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="mb-10">
        <h1 className="text-3xl font-display font-bold text-white tracking-tight">Dashboard</h1>
        <p className="text-secondary mt-1.5 text-sm">PostgreSQL workload intelligence and optimization overview.</p>
      </div>

      {stats.total_workloads === 0 && operations.length === 0 ? (
        <div className="bg-gradient-to-b from-surface/80 to-surface/40 backdrop-blur-xl border border-white/5 rounded-3xl p-16 text-center shadow-2xl relative overflow-hidden group">
          <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-signal/10 via-transparent to-transparent opacity-50 group-hover:opacity-100 transition-opacity duration-1000"></div>
          <div className="relative z-10">
            <div className="h-20 w-20 bg-signal/10 rounded-2xl flex items-center justify-center mx-auto mb-6 rotate-3 group-hover:rotate-6 transition-transform duration-500 border border-signal/20">
              <Database className="h-10 w-10 text-signal" />
            </div>
            <h2 className="text-2xl font-bold text-white mb-3">No Workload Data Yet</h2>
            <p className="text-secondary max-w-lg mx-auto leading-relaxed mb-8">
              Run an analysis against a connected PostgreSQL environment to begin building your workload intelligence baseline. Real-time metrics will appear here automatically.
            </p>
            <div className="inline-flex items-center px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-sm text-secondary">
              <span className="w-2 h-2 rounded-full bg-signal animate-pulse mr-3"></span>
              Waiting for telemetry...
            </div>
          </div>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
            <div className="bg-gradient-to-br from-surface to-surface/80 border border-white/5 rounded-2xl p-6 shadow-xl relative overflow-hidden group">
              <div className="absolute top-0 right-0 p-24 bg-signal/5 rounded-full blur-[60px] -mr-12 -mt-12 group-hover:bg-signal/10 transition-colors duration-500"></div>
              <div className="relative z-10">
                <div className="flex items-center justify-between mb-4">
                  <p className="text-xs text-secondary uppercase tracking-wider font-bold">Total Workloads</p>
                  <div className="p-2 rounded-lg bg-white/5 border border-white/5 group-hover:bg-signal/10 group-hover:border-signal/20 transition-all duration-300">
                    <Layers3 className="h-4 w-4 text-secondary group-hover:text-signal transition-colors" />
                  </div>
                </div>
                <h2 className="text-4xl font-display font-bold text-white tracking-tight">{stats.total_workloads}</h2>
              </div>
            </div>

            <div className="bg-gradient-to-br from-surface to-surface/80 border border-white/5 rounded-2xl p-6 shadow-xl relative overflow-hidden group">
              <div className="absolute top-0 right-0 p-24 bg-blue-500/5 rounded-full blur-[60px] -mr-12 -mt-12 group-hover:bg-blue-500/10 transition-colors duration-500"></div>
              <div className="relative z-10">
                <div className="flex items-center justify-between mb-4">
                  <p className="text-xs text-secondary uppercase tracking-wider font-bold">Active Queries</p>
                  <div className="p-2 rounded-lg bg-white/5 border border-white/5 group-hover:bg-blue-500/10 group-hover:border-blue-500/20 transition-all duration-300">
                    <Activity className="h-4 w-4 text-secondary group-hover:text-blue-400 transition-colors" />
                  </div>
                </div>
                <h2 className="text-4xl font-display font-bold text-white tracking-tight">{stats.active_queries}</h2>
              </div>
            </div>

            <div className="bg-gradient-to-br from-surface to-surface/80 border border-white/5 rounded-2xl p-6 shadow-xl relative overflow-hidden group">
              <div className="absolute top-0 right-0 p-24 bg-emerald-500/5 rounded-full blur-[60px] -mr-12 -mt-12 group-hover:bg-emerald-500/10 transition-colors duration-500"></div>
              <div className="relative z-10">
                <div className="flex items-center justify-between mb-4">
                  <p className="text-xs text-secondary uppercase tracking-wider font-bold">Optimizations Found</p>
                  <div className="p-2 rounded-lg bg-white/5 border border-white/5 group-hover:bg-emerald-500/10 group-hover:border-emerald-500/20 transition-all duration-300">
                    <Zap className="h-4 w-4 text-secondary group-hover:text-emerald-400 transition-colors" />
                  </div>
                </div>
                <h2 className="text-4xl font-display font-bold text-white tracking-tight">{stats.optimizations_applied}</h2>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Top Workloads */}
            <div className="flex flex-col space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-bold text-white flex items-center">
                  <Layers3 className="w-5 h-5 mr-2 text-indigo-400" />
                  Top Workloads
                </h3>
                <Link to="/workloads" className="text-xs font-semibold text-signal hover:text-signal-hover transition-colors flex items-center">
                  View All <ChevronRight className="w-3.5 h-3.5 ml-0.5" />
                </Link>
              </div>
              
              <div className="bg-surface/50 border border-white/5 rounded-2xl overflow-hidden shadow-lg">
                {isWorkloadsLoading ? (
                  <div className="p-6 space-y-4">
                    {[1, 2, 3].map(i => <div key={i} className="h-12 bg-white/5 rounded-lg animate-pulse"></div>)}
                  </div>
                ) : workloads.length > 0 ? (
                  <div className="divide-y divide-white/5">
                    {workloads.map((w) => (
                      <Link 
                        key={w.fingerprint_id} 
                        to={`/queries?fingerprint_id=${w.fingerprint_id}`}
                        className="flex items-center justify-between p-4 hover:bg-white/5 transition-colors group/row"
                      >
                        <div className="flex flex-col overflow-hidden mr-4">
                          <span className="text-xs font-mono text-indigo-300/80 mb-1 truncate">{w.fingerprint_id}</span>
                          <span className="text-sm text-paper font-mono truncate bg-surface px-2 py-1 rounded border border-white/5 inline-block w-fit max-w-[200px] sm:max-w-[300px]">
                            {w.query_text_snippet}
                          </span>
                        </div>
                        <div className="text-right flex-shrink-0">
                          <div className="text-xs text-secondary mb-1">Executions</div>
                          <div className="text-sm font-bold text-white bg-white/10 px-2 py-0.5 rounded-full inline-block">
                            {w.execution_count}
                          </div>
                        </div>
                      </Link>
                    ))}
                  </div>
                ) : (
                  <div className="p-8 text-center text-sm text-secondary">
                    No recent workloads detected.
                  </div>
                )}
              </div>
            </div>

            {/* Recent Operations */}
            <div className="flex flex-col space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-bold text-white flex items-center">
                  <Activity className="w-5 h-5 mr-2 text-blue-400" />
                  Recent Operations
                </h3>
                <Link to="/operations" className="text-xs font-semibold text-signal hover:text-signal-hover transition-colors flex items-center">
                  View All <ChevronRight className="w-3.5 h-3.5 ml-0.5" />
                </Link>
              </div>
              
              <div className="bg-surface/50 border border-white/5 rounded-2xl overflow-hidden shadow-lg">
                {isOpsLoading ? (
                  <div className="p-6 space-y-4">
                    {[1, 2, 3].map(i => <div key={i} className="h-12 bg-white/5 rounded-lg animate-pulse"></div>)}
                  </div>
                ) : operations.length > 0 ? (
                  <div className="divide-y divide-white/5">
                    {operations.map((op) => (
                      <div key={op.operation_id} className="flex items-center justify-between p-4 hover:bg-white/5 transition-colors">
                        <div className="flex items-center">
                          <div className="mr-4">
                            {getStatusIcon(op.status)}
                          </div>
                          <div className="flex flex-col">
                            <span className="text-sm font-bold text-white">{op.type}</span>
                            <span className="text-xs text-secondary flex items-center mt-0.5">
                              <Clock className="w-3 h-3 mr-1" />
                              {new Date(op.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                            </span>
                          </div>
                        </div>
                        <div>
                          <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider border ${getStatusClass(op.status)}`}>
                            {op.status}
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="p-8 text-center text-sm text-secondary">
                    No recent pipeline operations found.
                  </div>
                )}
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
