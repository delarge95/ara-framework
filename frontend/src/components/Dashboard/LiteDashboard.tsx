import React from "react";
import { GlassCard } from "../ui/GlassCard";
import {
  HardDrive,
  DollarSign,
  Activity,
  PlayCircle,
  PauseCircle,
  Zap,
} from "lucide-react";

const BudgetAlert: React.FC<{
  service: string;
  used: number;
  limit: number;
  unit: string;
  cost: string;
  healthy?: boolean;
}> = ({ service, used, limit, unit, cost, healthy }) => {
  const percent = (used / limit) * 100;

  return (
    <GlassCard className="relative overflow-hidden group">
      <div className="absolute top-0 left-0 w-1 h-full bg-gradient-to-b from-green-400 to-transparent opacity-50" />
      <div className="flex justify-between items-start mb-4">
        <div>
          <h4 className="font-bold text-white">{service}</h4>
          <span className="text-xs text-slate-400">{cost}</span>
        </div>
        {healthy && (
          <div className="w-2 h-2 bg-green-500 rounded-full shadow-[0_0_8px_rgba(16,185,129,0.6)]"></div>
        )}
      </div>

      <div className="mb-2">
        <div className="flex justify-between text-xs mb-1">
          <span className="text-slate-300">
            {used.toLocaleString()} {unit}
          </span>
          <span className="text-slate-500">{limit.toLocaleString()} limit</span>
        </div>
        <div className="h-1.5 bg-black/50 rounded-full overflow-hidden">
          <div
            style={{ width: `${percent}%` }}
            className={`h-full rounded-full ${
              percent > 80 ? "bg-red-500" : "bg-green-500"
            }`}
          ></div>
        </div>
      </div>
    </GlassCard>
  );
};

const ModelStatus: React.FC<{
  name: string;
  role: string;
  status: "ready" | "loading" | "offline";
  latency?: string;
  progress?: number;
}> = ({ name, role, status, latency, progress }) => {
  return (
    <div className="flex items-center justify-between p-4 bg-white/5 rounded-lg border border-white/5 hover:border-white/10 transition-colors">
      <div className="flex items-center gap-4">
        <div
          className={`p-2 rounded-full ${
            status === "ready"
              ? "bg-green-500/20 text-green-400"
              : "bg-amber-500/20 text-amber-400"
          }`}
        >
          {status === "ready" ? (
            <PlayCircle size={20} />
          ) : (
            <Activity size={20} className="animate-pulse" />
          )}
        </div>
        <div>
          <div className="font-mono text-sm font-bold text-slate-200">
            {name}
          </div>
          <div className="text-xs text-slate-500">{role}</div>
        </div>
      </div>
      <div className="text-right">
        {status === "ready" ? (
          <div className="text-xs font-mono text-green-400">{latency}</div>
        ) : (
          <div className="text-xs font-mono text-amber-400">
            {progress}% loaded
          </div>
        )}
        <div className="text-[10px] text-slate-600 uppercase tracking-wider">
          {status}
        </div>
      </div>
    </div>
  );
};

export const LiteDashboard: React.FC = () => {
  return (
    <div className="space-y-8 animate-fade-in">
      <header className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <h1 className="text-4xl font-serif text-white">ARA Lite</h1>
          <span className="text-xs bg-green-900/40 text-green-400 border border-green-500/30 px-2 py-1 rounded font-mono">
            Student 0.2
          </span>
        </div>
        <p className="text-slate-400 max-w-2xl">
          Optimized local execution environment. Zero hidden costs. Focus on
          learning, not billing.
        </p>
      </header>

      {/* Budget Transparency */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <BudgetAlert
          service="Anthropic Edu"
          used={12500}
          limit={50000}
          unit="tokens"
          cost="$5.00/mo cap"
          healthy
        />
        <BudgetAlert
          service="Perplexity"
          used={140}
          limit={7000}
          unit="queries"
          cost="Included"
          healthy
        />
        <GlassCard className="relative">
          <div className="flex justify-between items-start">
            <div className="flex items-center gap-2 text-ara-primary mb-4">
              <HardDrive size={20} />
              <span className="font-bold text-white">Local Hardware</span>
            </div>
            <span className="text-xs text-amber-500 bg-amber-900/20 px-2 py-0.5 rounded border border-amber-500/20">
              HIGH LOAD
            </span>
          </div>
          <div className="space-y-4">
            <div>
              <div className="flex justify-between text-xs text-slate-400 mb-1">
                <span>VRAM Usage (RTX 4090)</span>
                <span className="text-white">21.2 / 24 GB</span>
              </div>
              <div className="h-1.5 bg-black/50 rounded-full overflow-hidden">
                <div className="h-full bg-amber-500 w-[88%]"></div>
              </div>
            </div>
            <div className="text-xs text-slate-500 font-mono">
              Swap active: 1.2GB (NVMe SSD)
            </div>
          </div>
        </GlassCard>
      </div>

      {/* Warm Pool */}
      <div>
        <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <Zap size={18} className="text-amber-500" /> Warm Pool Status
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <ModelStatus
            name="Phi-3.5 Mini"
            role="Logic & Glue Layer"
            status="ready"
            latency="45ms"
          />
          <ModelStatus
            name="Qwen 2.5 Coder"
            role="Real-time Coding Assist"
            status="loading"
            progress={78}
          />
        </div>
      </div>
    </div>
  );
};
