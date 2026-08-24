import React from "react";
import { useParams, Link } from "react-router-dom";
import { useQueryDetail } from "../hooks/useProduct";
import { ArrowLeft, Clock, Zap, CheckCircle, Database, ChevronRight, Activity } from "lucide-react";

export default function QueryDetails() {
  const { queryId } = useParams();
  const { data: query, isLoading, error } = useQueryDetail(queryId);

  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh]">
        <div className="w-10 h-10 border-4 border-signal border-t-transparent rounded-full animate-spin mb-4"></div>
        <div className="text-secondary font-medium">Loading query details...</div>
      </div>
    );
  }

  if (error || !query) {
    return (
      <div className="p-8 max-w-2xl mx-auto mt-10 bg-red-500/10 border border-red-500/20 rounded-xl text-red-400 flex items-center">
        <div className="p-3 bg-red-500/20 rounded-lg mr-4">
          <Database className="w-6 h-6" />
        </div>
        <div>
          <h3 className="font-semibold text-lg">Failed to load query details</h3>
          <p className="text-sm opacity-80 mt-1">Check your connection or try again later.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto p-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="mb-8">
        <Link
          to="/queries"
          className="inline-flex items-center text-sm font-medium text-secondary hover:text-white transition-colors mb-6 bg-surface px-3 py-1.5 rounded-full border border-white/5 hover:border-white/20"
        >
          <ArrowLeft className="w-4 h-4 mr-1.5" />
          Back to Queries
        </Link>
        
        <div className="flex items-center flex-wrap gap-4 mb-2">
          <h1 className="text-3xl font-display font-bold text-white tracking-tight">
            Query Details
          </h1>
          {query.has_optimizations ? (
            <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 shadow-[0_0_15px_rgba(99,102,241,0.15)]">
              <Zap className="w-3.5 h-3.5 mr-1.5" />
              Recommendations Available
            </span>
          ) : (
            <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 shadow-[0_0_15px_rgba(16,185,129,0.15)]">
              <CheckCircle className="w-3.5 h-3.5 mr-1.5" />
              Optimal
            </span>
          )}
        </div>
        <div className="flex items-center gap-2 text-secondary font-mono text-sm">
          <span>ID:</span>
          <span className="text-indigo-300 bg-indigo-500/10 border border-indigo-500/20 px-2 py-0.5 rounded shadow-inner">
            {query.query_id}
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-8">
          <div className="bg-surface/40 backdrop-blur-md border border-white/5 rounded-2xl overflow-hidden shadow-xl shadow-black/20 group">
            <div className="px-6 py-4 border-b border-white/5 bg-gradient-to-r from-surface to-surface-hover flex items-center justify-between">
              <h3 className="text-sm font-semibold text-white flex items-center">
                <div className="p-1.5 bg-blue-500/10 rounded-md mr-2.5">
                  <Database className="w-4 h-4 text-blue-400" />
                </div>
                SQL Statement
              </h3>
              <div className="flex space-x-1.5">
                <div className="w-2.5 h-2.5 rounded-full bg-red-500/80"></div>
                <div className="w-2.5 h-2.5 rounded-full bg-yellow-500/80"></div>
                <div className="w-2.5 h-2.5 rounded-full bg-green-500/80"></div>
              </div>
            </div>
            <div className="p-6 overflow-x-auto bg-[#090b10] relative">
              <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 to-purple-500/5 pointer-events-none"></div>
              <pre className="text-sm font-mono text-blue-300 relative z-10 leading-relaxed">
                {query.query_text}
              </pre>
            </div>
          </div>
        </div>

        <div className="space-y-6">
          <div className="bg-surface/60 backdrop-blur-xl border border-white/5 rounded-2xl p-6 shadow-xl relative overflow-hidden">
            <div className="absolute top-0 right-0 p-32 bg-blue-500/5 rounded-full blur-[80px] -mr-16 -mt-16 pointer-events-none"></div>
            
            <h3 className="text-sm font-bold text-white mb-6 flex items-center">
              <Activity className="w-4 h-4 mr-2 text-indigo-400" />
              Execution Summary
            </h3>
            
            <div className="space-y-6 relative z-10">
              <div className="group/stat">
                <p className="text-[10px] text-secondary uppercase tracking-widest font-bold mb-1.5">Execution Time</p>
                <div className="flex items-center text-2xl font-display font-semibold text-white">
                  <div className="p-2 bg-yellow-500/10 rounded-lg mr-3 group-hover/stat:bg-yellow-500/20 transition-colors">
                    <Zap className="w-5 h-5 text-yellow-500" />
                  </div>
                  {query.execution_time_ms.toFixed(2)} <span className="text-sm text-secondary ml-1 font-normal">ms</span>
                </div>
              </div>
              
              <div className="group/stat">
                <p className="text-[10px] text-secondary uppercase tracking-widest font-bold mb-1.5">Timestamp</p>
                <div className="flex items-center text-sm font-medium text-slate-200">
                  <div className="p-1.5 bg-white/5 rounded-md mr-3 group-hover/stat:bg-white/10 transition-colors">
                    <Clock className="w-4 h-4 text-secondary" />
                  </div>
                  {new Date(query.timestamp).toLocaleString(undefined, { 
                    month: 'long', day: 'numeric', year: 'numeric',
                    hour: '2-digit', minute: '2-digit', second: '2-digit'
                  })}
                </div>
              </div>

              <div>
                <p className="text-[10px] text-secondary uppercase tracking-widest font-bold mb-2">Workload Fingerprint</p>
                <div className="text-xs font-mono text-blue-300 bg-blue-500/10 border border-blue-500/20 px-3 py-2 rounded-lg inline-block truncate max-w-full shadow-inner cursor-pointer hover:bg-blue-500/20 transition-colors">
                  {query.fingerprint_id}
                </div>
              </div>
            </div>
          </div>

          {query.has_optimizations ? (
            <div className="bg-gradient-to-br from-indigo-500/10 to-purple-500/10 border border-indigo-500/20 rounded-2xl p-6 shadow-xl relative overflow-hidden group">
              <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/20 to-purple-500/20 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              
              <div className="relative z-10">
                <div className="flex items-center mb-4">
                  <div className="p-2 bg-indigo-500/20 rounded-lg mr-3">
                    <Zap className="w-5 h-5 text-indigo-400" />
                  </div>
                  <h3 className="text-sm font-bold text-white">Optimizations Ready</h3>
                </div>
                
                <p className="text-sm text-indigo-200/80 mb-6 leading-relaxed">
                  The deterministic engine generated <strong className="text-white bg-white/10 px-1.5 py-0.5 rounded">{query.total_recommendations}</strong> potential recommendations for this query execution.
                </p>
                
                <button className="w-full flex items-center justify-between py-3 px-5 bg-indigo-500 hover:bg-indigo-400 text-white rounded-xl text-sm font-semibold transition-all duration-300 shadow-[0_0_15px_rgba(99,102,241,0.3)] hover:shadow-[0_0_25px_rgba(99,102,241,0.5)] transform hover:-translate-y-0.5">
                  View Recommendations
                  <ChevronRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          ) : (
            <div className="bg-gradient-to-br from-emerald-500/5 to-teal-500/5 border border-emerald-500/10 rounded-2xl p-6 shadow-xl relative overflow-hidden">
              <div className="relative z-10">
                <div className="flex items-center mb-4">
                  <div className="p-2 bg-emerald-500/10 rounded-lg mr-3">
                    <CheckCircle className="w-5 h-5 text-emerald-400" />
                  </div>
                  <h3 className="text-sm font-bold text-white">Query is Optimal</h3>
                </div>
                
                <p className="text-sm text-emerald-200/70 leading-relaxed">
                  The deterministic engine analyzed this query and found no further recommendations. The query structure is already optimal.
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
