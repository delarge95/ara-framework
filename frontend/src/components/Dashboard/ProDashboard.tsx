import React from "react";
import { GlassCard } from "../ui/GlassCard";
import { Shield, AlertTriangle, GitMerge, Terminal } from "lucide-react";

const GateItem: React.FC<{ id: string; type: string; status: string }> = ({
  id,
  type,
  status,
}) => (
  <div className="flex items-center justify-between py-3 border-b border-white/5 last:border-0">
    <div className="flex items-center gap-3">
      <GitMerge size={16} className="text-slate-500" />
      <div>
        <div className="text-sm font-mono text-slate-300">{id}</div>
        <div className="text-[10px] text-slate-500">{type}</div>
      </div>
    </div>
    <span
      className={`text-xs px-2 py-0.5 rounded border ${
        status === "CRITICAL"
          ? "text-red-400 border-red-500/30 bg-red-900/20"
          : "text-amber-400 border-amber-500/30 bg-amber-900/20"
      }`}
    >
      {status}
    </span>
  </div>
);

export const ProDashboard: React.FC = () => {
  return (
    <div className="space-y-6 animate-fade-in">
      <header className="mb-8 flex justify-between items-end">
        <div>
          <h1 className="text-4xl font-serif text-ara-primary mb-2">
            ARA 2.2 Pro
          </h1>
          <p className="text-slate-400 font-light">
            Orchestration Enterprise • Active Telemetry • Chaos Ready
          </p>
        </div>
        <div className="text-right">
          <div className="text-3xl font-mono text-white">94.2%</div>
          <div className="text-xs text-ara-primary uppercase tracking-widest">
            Router Cache Hit Rate
          </div>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Main Content */}
        <div className="lg:col-span-8">
          <GlassCard title="Router Health & Telemetry" className="h-[400px]">
            <div className="flex items-center justify-center h-full text-slate-500">
              <div className="text-center">
                <div className="text-2xl font-mono text-ara-primary">
                  ✓ SYSTEM HEALTHY
                </div>
                <div className="text-sm mt-2">All systems operational</div>
                <div className="text-xs mt-1">
                  Latency: 12ms • Requests: 8.2K/min
                </div>
              </div>
            </div>
          </GlassCard>
        </div>

        {/* Gate Queue */}
        <div className="lg:col-span-4">
          <GlassCard
            title="Human Gates Queue"
            className="h-[400px] overflow-y-auto"
          >
            <div className="flex justify-between mb-4">
              <div className="text-xs text-slate-500 uppercase">
                Pending Review
              </div>
              <div className="text-xs text-slate-200 font-mono">4 Active</div>
            </div>
            <GateItem id="PR-8942" type="Schema Migration" status="CRITICAL" />
            <GateItem id="DEP-3321" type="Model Promotion" status="WAITING" />
            <GateItem id="SEC-1102" type="Token Expiry" status="WAITING" />
            <GateItem id="PR-8945" type="UI Vibe Check" status="WAITING" />

            <div className="mt-6 p-4 bg-black/40 rounded border border-white/5">
              <div className="flex items-center gap-2 text-ara-primary mb-2">
                <Terminal size={14} />
                <span className="text-xs font-bold uppercase">System Log</span>
              </div>
              <div className="font-mono text-[10px] text-slate-500 space-y-1">
                <p>[14:02:22] Semantic Router rerouted 15% traffic</p>
                <p>[14:02:45] Garbage collection on Node-04</p>
                <p>
                  <span className="text-green-500">
                    [14:03:12] Snapshot created
                  </span>
                </p>
              </div>
            </div>
          </GlassCard>
        </div>

        {/* Security & Chaos */}
        <div className="lg:col-span-6">
          <GlassCard className="border-l-4 border-l-ara-primary">
            <div className="flex items-start justify-between">
              <div>
                <h3 className="text-lg font-medium text-white flex items-center gap-2">
                  <Shield size={20} className="text-ara-primary" /> Threat
                  Monitor
                </h3>
                <p className="text-sm text-slate-400 mt-1">
                  Active Shields:{" "}
                  <span className="text-slate-200 font-mono bg-white/5 px-1 rounded">
                    Semgrep
                  </span>
                  ,{" "}
                  <span className="text-slate-200 font-mono bg-white/5 px-1 rounded">
                    Package-Hallucination
                  </span>
                </p>
              </div>
              <div className="text-right">
                <div className="text-2xl font-serif text-green-400">LOW</div>
                <div className="text-[10px] text-slate-500 uppercase">
                  Threat Level
                </div>
              </div>
            </div>
          </GlassCard>
        </div>

        <div className="lg:col-span-6">
          <GlassCard className="border-l-4 border-l-slate-600">
            <div className="flex items-start justify-between">
              <div>
                <h3 className="text-lg font-medium text-white flex items-center gap-2">
                  <AlertTriangle size={20} className="text-slate-400" /> Chaos
                  Engineering
                </h3>
                <p className="text-sm text-slate-400 mt-1">
                  Last Drill: <span className="text-slate-200">2h ago</span>{" "}
                  (Passed)
                </p>
              </div>
              <button className="bg-white/5 hover:bg-white/10 text-xs text-white px-4 py-2 rounded border border-white/10 transition-colors">
                Schedule Drill
              </button>
            </div>
          </GlassCard>
        </div>
      </div>
    </div>
  );
};
