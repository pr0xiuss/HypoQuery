import React from "react";
import { useDashboard } from "../hooks/useProduct";
import { Activity, Layers3, Zap } from "lucide-react";

export default function Dashboard() {
  const { data: dashboard, isLoading, error } = useDashboard();

  if (isLoading) {
    return <div className="p-8 text-secondary">Loading dashboard...</div>;
  }

  if (error) {
    return <div className="p-8 text-red-500">Failed to load dashboard</div>;
  }

  const stats = dashboard?.stats || { total_workloads: 0, active_queries: 0, optimizations_applied: 0 };

  return (
    <div className="max-w-7xl mx-auto p-8">
      <div className="mb-8">
        <h1 className="text-2xl font-display font-semibold text-paper">Dashboard</h1>
        <p className="text-secondary mt-1">Platform overview and workload intelligence.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-surface border border-divider rounded-xl p-6">
          <div className="flex items-center gap-4">
            <div className="h-10 w-10 rounded-lg bg-signal/10 flex items-center justify-center">
              <Layers3 className="h-5 w-5 text-signal" />
            </div>
            <div>
              <p className="text-sm text-secondary font-medium">Total Workloads</p>
              <h2 className="text-3xl font-bold text-paper mt-1">{stats.total_workloads}</h2>
            </div>
          </div>
        </div>

        <div className="bg-surface border border-divider rounded-xl p-6">
          <div className="flex items-center gap-4">
            <div className="h-10 w-10 rounded-lg bg-blue-500/10 flex items-center justify-center">
              <Activity className="h-5 w-5 text-blue-500" />
            </div>
            <div>
              <p className="text-sm text-secondary font-medium">Active Queries</p>
              <h2 className="text-3xl font-bold text-paper mt-1">{stats.active_queries}</h2>
            </div>
          </div>
        </div>

        <div className="bg-surface border border-divider rounded-xl p-6">
          <div className="flex items-center gap-4">
            <div className="h-10 w-10 rounded-lg bg-green-500/10 flex items-center justify-center">
              <Zap className="h-5 w-5 text-green-500" />
            </div>
            <div>
              <p className="text-sm text-secondary font-medium">Optimizations Applied</p>
              <h2 className="text-3xl font-bold text-paper mt-1">{stats.optimizations_applied}</h2>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
