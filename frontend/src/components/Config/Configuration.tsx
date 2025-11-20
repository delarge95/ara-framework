import React, { useState } from "react";
import { GlassCard } from "../ui/GlassCard";
import { AppMode } from "../../types";
import {
  Cpu,
  Shield,
  Zap,
  Database,
  Server,
  Globe,
  Lock,
  Sliders,
  Save,
  RefreshCw,
  Terminal,
  HardDrive,
  WifiOff,
  DollarSign,
  Box,
} from "lucide-react";

type ConfigSection = "orchestration" | "mcp" | "guardrails" | "resources";
type LiteSection = "hardware" | "local_bridge" | "student_budget" | "tools";

interface ConfigurationProps {
  mode: AppMode;
}

export const Configuration: React.FC<ConfigurationProps> = ({ mode }) => {
  const [activeProSection, setActiveProSection] =
    useState<ConfigSection>("orchestration");
  const [activeLiteSection, setActiveLiteSection] =
    useState<LiteSection>("hardware");

  const isPro = mode === "pro";

  return (
    <div className="animate-fade-in max-w-6xl mx-auto pb-20">
      <header className="mb-10 flex justify-between items-center border-b border-white/10 pb-6">
        <div>
          <h1
            className={`text-4xl font-serif mb-2 ${
              isPro ? "text-ara-primary" : "text-green-400"
            }`}
          >
            {isPro ? "Pro Control Plane" : "Lite Local Config"}
          </h1>
          <p className="text-slate-400">
            {isPro
              ? "Configure Enterprise ARA 2.2 runtime, semantic routing, and security policies."
              : "Manage local hardware resources, Ollama bridges, and student budget caps."}
          </p>
        </div>
        <button
          className={`${
            isPro
              ? "bg-ara-primary hover:bg-amber-600"
              : "bg-green-600 hover:bg-green-700"
          } text-white px-6 py-3 rounded-lg font-medium flex items-center gap-2 transition-colors shadow-lg shadow-black/20`}
        >
          <Save size={18} />
          {isPro ? "Deploy Config" : "Save Local Profile"}
        </button>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Sidebar Navigation */}
        <div className="lg:col-span-3 space-y-2">
          {isPro ? (
            <>
              <NavButton
                active={activeProSection === "orchestration"}
                onClick={() => setActiveProSection("orchestration")}
                icon={Cpu}
                label="Orchestration"
                desc="Router & Caching"
                mode="pro"
              />
              <NavButton
                active={activeProSection === "mcp"}
                onClick={() => setActiveProSection("mcp")}
                icon={Database}
                label="MCP Hub"
                desc="Docker & Data"
                mode="pro"
              />
              <NavButton
                active={activeProSection === "guardrails"}
                onClick={() => setActiveProSection("guardrails")}
                icon={Shield}
                label="Guardrails"
                desc="Security & Gates"
                mode="pro"
              />
              <NavButton
                active={activeProSection === "resources"}
                onClick={() => setActiveProSection("resources")}
                icon={Sliders}
                label="Resources"
                desc="Limits & Billing"
                mode="pro"
              />
            </>
          ) : (
            <>
              <NavButton
                active={activeLiteSection === "hardware"}
                onClick={() => setActiveLiteSection("hardware")}
                icon={HardDrive}
                label="Hardware Profile"
                desc="RAM & Swap Logic"
                mode="lite"
              />
              <NavButton
                active={activeLiteSection === "local_bridge"}
                onClick={() => setActiveLiteSection("local_bridge")}
                icon={Terminal}
                label="Local Bridge"
                desc="Ollama/Llama.cpp"
                mode="lite"
              />
              <NavButton
                active={activeLiteSection === "student_budget"}
                onClick={() => setActiveLiteSection("student_budget")}
                icon={DollarSign}
                label="Student Budget"
                desc="Strict Caps"
                mode="lite"
              />
              <NavButton
                active={activeLiteSection === "tools"}
                onClick={() => setActiveLiteSection("tools")}
                icon={Box}
                label="Local Tools"
                desc="Filesystem Access"
                mode="lite"
              />
            </>
          )}
        </div>

        {/* Main Content */}
        <div className="lg:col-span-9">
          {isPro ? (
            <>
              {activeProSection === "orchestration" && <ProOrchestration />}
              {activeProSection === "mcp" && <ProMCP />}
              {activeProSection === "guardrails" && <ProGuardrails />}
              {activeProSection === "resources" && <ProResources />}
            </>
          ) : (
            <>
              {activeLiteSection === "hardware" && <LiteHardware />}
              {activeLiteSection === "local_bridge" && <LiteBridge />}
              {activeLiteSection === "student_budget" && <LiteBudget />}
              {activeLiteSection === "tools" && <LiteTools />}
            </>
          )}
        </div>
      </div>
    </div>
  );
};

const NavButton = ({ active, onClick, icon: Icon, label, desc, mode }: any) => {
  const activeColor = mode === "pro" ? "bg-ara-primary" : "bg-green-500";
  const activeBorder =
    mode === "pro" ? "border-ara-primary" : "border-green-500";
  const activeBg = mode === "pro" ? "bg-ara-primary/10" : "bg-green-500/10";

  return (
    <button
      onClick={onClick}
      className={`w-full text-left p-4 rounded-xl border transition-all duration-200 flex items-center gap-4 group ${
        active
          ? `${activeBg} ${activeBorder} text-white shadow-lg`
          : "bg-white/5 border-transparent hover:bg-white/10 text-slate-400 hover:text-slate-200"
      }`}
    >
      <div
        className={`p-2 rounded-lg ${
          active
            ? activeColor + " text-white"
            : "bg-white/5 text-slate-500 group-hover:text-slate-300"
        }`}
      >
        <Icon size={20} />
      </div>
      <div>
        <div className="font-bold text-sm">{label}</div>
        <div
          className={`text-xs ${active ? "text-white/80" : "text-slate-600"}`}
        >
          {desc}
        </div>
      </div>
    </button>
  );
};

/* ==================== LITE COMPONENTS ==================== */

const LiteHardware = () => (
  <div className="space-y-6">
    <GlassCard title="Local Hardware Constraints">
      <div className="bg-green-900/10 border border-green-500/20 p-4 rounded-lg mb-6">
        <div className="flex items-center gap-3 mb-2">
          <Cpu size={20} className="text-green-400" />
          <h4 className="font-bold text-white">
            Detected: M2 Pro (32GB Unified)
          </h4>
        </div>
        <p className="text-xs text-slate-400">
          ARA Lite will auto-tune model offloading layers based on this profile.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="text-xs font-bold text-slate-500 uppercase mb-2 block">
            VRAM Allocation Limit
          </label>
          <input
            type="range"
            min="4"
            max="32"
            defaultValue="24"
            className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-green-500 mb-2"
          />
          <div className="flex justify-between text-xs text-slate-300">
            <span>4GB (Phi only)</span>
            <span className="text-green-400 font-bold">24GB (Recommended)</span>
            <span>32GB</span>
          </div>
        </div>

        <div className="bg-black/30 p-4 rounded border border-white/10">
          <label className="text-xs font-bold text-slate-500 uppercase mb-2 block">
            Swapping Strategy
          </label>
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <input type="radio" name="swap" className="accent-green-500" />
              <span className="text-sm text-slate-300">
                Aggressive (Save RAM, High Latency)
              </span>
            </div>
            <div className="flex items-center gap-2">
              <input
                type="radio"
                name="swap"
                className="accent-green-500"
                defaultChecked
              />
              <span className="text-sm text-white font-bold">
                Balanced (Warm Pool for 1 Model)
              </span>
            </div>
          </div>
        </div>
      </div>
    </GlassCard>

    <GlassCard title="Disk Checkpointing" className="border-amber-500/20">
      <div className="flex justify-between items-center">
        <div>
          <h4 className="text-white font-bold">NVMe Context Swap</h4>
          <p className="text-xs text-slate-400 mt-1">
            Write active context to disk when switching models to prevent data
            loss.
          </p>
        </div>
        <ToggleSwitch checked={true} color="green" />
      </div>
      <div className="mt-4 p-3 bg-black/40 rounded border border-white/5 font-mono text-xs text-slate-500">
        ~/.ara/checkpoints/swapfile.bin (Max 4GB)
      </div>
    </GlassCard>
  </div>
);

const LiteBridge = () => (
  <div className="space-y-6">
    <GlassCard title="Ollama Bridge Configuration">
      <div className="grid grid-cols-1 gap-4">
        <div className="p-4 border border-green-500/30 bg-green-900/10 rounded-lg flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
            <div>
              <div className="font-bold text-white">Ollama Service</div>
              <div className="text-xs text-green-400">Connected v0.1.28</div>
            </div>
          </div>
          <div className="text-xs font-mono text-slate-400">
            http://localhost:11434
          </div>
        </div>
      </div>

      <div className="mt-6">
        <h4 className="text-sm font-bold text-white mb-4">
          Active GGUF Models
        </h4>
        <div className="space-y-3">
          <LocalModelRow
            name="phi-3.5-mini-instruct"
            size="2.3GB"
            q="Q4_K_M"
            status="Loaded (VRAM)"
          />
          <LocalModelRow
            name="qwen-2.5-coder-7b"
            size="4.8GB"
            q="Q5_K_M"
            status="Cached (Disk)"
          />
          <LocalModelRow
            name="mistral-nemo"
            size="8.1GB"
            q="Q4_0"
            status="Missing"
          />
        </div>
        <button className="mt-4 w-full py-2 border border-dashed border-slate-600 text-slate-400 rounded hover:border-green-500 hover:text-green-400 transition-colors text-sm">
          + Pull new model from library
        </button>
      </div>
    </GlassCard>
  </div>
);

const LiteBudget = () => (
  <div className="space-y-6">
    <GlassCard title="Strict Budget Controls">
      <div className="flex items-center justify-between mb-6 pb-6 border-b border-white/5">
        <div>
          <div className="flex items-center gap-2">
            <WifiOff size={18} className="text-slate-400" />
            <h4 className="font-bold text-white">Offline-Only Mode</h4>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Block all outbound API calls. Pure local execution.
          </p>
        </div>
        <ToggleSwitch checked={false} color="green" />
      </div>

      <div className="space-y-4">
        <div className="bg-black/40 p-4 rounded border border-white/10">
          <label className="text-xs font-bold text-slate-500 uppercase mb-2 block">
            Emergency API Key (Anthropic Edu)
          </label>
          <div className="flex gap-2">
            <input
              type="password"
              value="sk-ant-api03-..."
              className="flex-1 bg-transparent border-b border-white/20 text-slate-300 text-sm focus:outline-none focus:border-green-500 py-1"
              disabled
            />
            <button className="text-xs text-green-400 font-medium">
              Update
            </button>
          </div>
          <div className="mt-2 flex justify-between text-xs">
            <span className="text-slate-500">Limit: $5.00/mo</span>
            <span className="text-red-400">Used: $1.24</span>
          </div>
        </div>
      </div>
    </GlassCard>
  </div>
);

const LiteTools = () => (
  <div className="space-y-6">
    <GlassCard title="Approved Local Tools">
      <p className="text-sm text-slate-400 mb-4">
        Lite mode only allows local filesystem access and read-only Git
        operations for safety.
      </p>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="p-3 bg-white/5 border border-white/10 rounded flex items-center justify-between">
          <div className="flex items-center gap-3">
            <HardDrive size={18} className="text-slate-300" />
            <span className="text-sm text-slate-200">Local Filesystem</span>
          </div>
          <span className="text-[10px] bg-green-500/20 text-green-400 px-2 py-0.5 rounded">
            Active
          </span>
        </div>
        <div className="p-3 bg-white/5 border border-white/10 rounded flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Terminal size={18} className="text-slate-300" />
            <span className="text-sm text-slate-200">Git (Read-Only)</span>
          </div>
          <span className="text-[10px] bg-green-500/20 text-green-400 px-2 py-0.5 rounded">
            Active
          </span>
        </div>
      </div>
    </GlassCard>
  </div>
);

const LocalModelRow = ({ name, size, q, status }: any) => (
  <div className="flex items-center justify-between p-3 bg-black/30 rounded border border-white/5">
    <div>
      <div className="text-sm font-mono text-slate-200">{name}</div>
      <div className="text-[10px] text-slate-500">
        {size} • {q}
      </div>
    </div>
    <span
      className={`text-xs px-2 py-1 rounded ${
        status.includes("Loaded")
          ? "bg-green-900/20 text-green-400 border border-green-500/20"
          : "bg-white/5 text-slate-500"
      }`}
    >
      {status}
    </span>
  </div>
);

/* ==================== PRO COMPONENTS ==================== */

const ProOrchestration = () => (
  <div className="space-y-6">
    <GlassCard title="Adaptive Routing & Caching">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <div className="bg-black/30 p-4 rounded-lg border border-white/10">
          <label className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2 block">
            Router Mode
          </label>
          <select className="w-full bg-ara-surface text-white border border-white/20 rounded p-2 focus:border-ara-primary outline-none">
            <option>Adaptive (Performance/Cost Balanced)</option>
            <option>Max Intelligence (GPT-5.1 Priority)</option>
            <option>Economy (Local/Cache Priority)</option>
          </select>
        </div>
        <div className="bg-black/30 p-4 rounded-lg border border-white/10">
          <label className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2 block">
            Cache Infrastructure
          </label>
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-slate-300">Redis Semantic Cache</span>
            <ToggleSwitch checked={true} />
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm text-slate-300">
              LightGBM Novelty Detector
            </span>
            <ToggleSwitch checked={true} />
          </div>
        </div>
      </div>

      <h4 className="text-sm font-bold text-white mb-4 flex items-center gap-2">
        <Zap size={16} className="text-ara-primary" />
        Phase-Model Mapping
      </h4>
      <div className="space-y-3">
        <ProModelRow
          phase="Architecture"
          defaultModel="GPT-5.1 Thinking"
          options={["GPT-5.1 Thinking", "Claude 3.5 Sonnet", "DeepSeek R1"]}
        />
        <ProModelRow
          phase="Coding (Agentic)"
          defaultModel="Claude 4.5 Sonnet"
          options={["Claude 4.5 Sonnet", "Kimi k2 Thinking", "GPT-5.1"]}
        />
        <ProModelRow
          phase="Boilerplate"
          defaultModel="DeepSeek V3.1"
          options={["DeepSeek V3.1", "Qwen 2.5 Coder", "MiniMax M2"]}
        />
      </div>
    </GlassCard>
  </div>
);

const ProMCP = () => (
  <div className="space-y-6">
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      <MCPCard name="Filesystem" status="active" type="std:io" />
      <MCPCard name="PostgreSQL" status="active" type="docker" />
      <MCPCard name="GitHub" status="inactive" type="http" />
      <MCPCard name="Slack" status="inactive" type="http" />
      <MCPCard name="Sentry" status="active" type="sse" />
      <MCPCard name="Brave Search" status="inactive" type="api" />
    </div>
    <GlassCard title="Docker Bridge">
      <div className="flex items-center justify-between p-4 border border-white/10 rounded bg-black/40">
        <span className="font-mono text-sm text-slate-300">
          mcp/postgres:latest
        </span>
        <span className="text-xs text-green-400">
          Running (Container ID: a1b2c3d)
        </span>
      </div>
    </GlassCard>
  </div>
);

const ProGuardrails = () => (
  <div className="space-y-6">
    <GlassCard title="ARAShield Enterprise Policies">
      <div className="space-y-4">
        <PolicyRow
          title="Package Hallucination Check"
          desc="Verify every import against npm/pypi registry API"
          checked={true}
          badge="Critical"
        />
        <PolicyRow
          title="PII Scrubber"
          desc="Regex + NER sanitization of logs before telemetry export"
          checked={true}
          badge="Compliance"
        />
      </div>
    </GlassCard>
    <GlassCard title="Human Gate Configuration">
      <div className="space-y-3">
        <GateConfigRow action="Production Deployment" threshold="2 Approvers" />
        <GateConfigRow action="Database Drop/Alter" threshold="Admin Only" />
      </div>
    </GlassCard>
  </div>
);

const ProResources = () => (
  <div className="space-y-6">
    <GlassCard title="Enterprise Budget">
      <div className="mb-4">
        <div className="flex justify-between text-sm mb-2">
          <span className="text-slate-300">Monthly Cap</span>
          <span className="font-mono text-white">$299.00</span>
        </div>
        <div className="h-2 bg-white/10 rounded-full overflow-hidden">
          <div className="h-full bg-ara-primary w-[65%]"></div>
        </div>
      </div>
    </GlassCard>
  </div>
);

/* --- Shared Helpers --- */

const ProModelRow = ({ phase, defaultModel, options }: any) => (
  <div className="flex items-center justify-between p-3 bg-white/5 rounded border border-white/5 hover:border-white/10 transition-colors">
    <span className="text-sm font-mono text-slate-300 w-1/3">{phase}</span>
    <select className="bg-black/50 border border-white/10 rounded px-3 py-1 text-sm text-white focus:border-ara-primary outline-none w-2/3">
      {options.map((opt: string) => (
        <option key={opt} defaultValue={opt === defaultModel ? opt : undefined}>
          {opt}
        </option>
      ))}
    </select>
  </div>
);

const MCPCard = ({ name, status, type }: any) => (
  <GlassCard className="p-4 flex items-center justify-between group cursor-pointer hover:border-ara-primary/50 transition-all">
    <div className="flex items-center gap-3">
      <Server
        size={20}
        className={status === "active" ? "text-white" : "text-slate-600"}
      />
      <div>
        <div className="font-bold text-sm text-slate-200">{name}</div>
        <div className="text-[10px] text-slate-500 uppercase tracking-wider">
          {type}
        </div>
      </div>
    </div>
    <div
      className={`w-2 h-2 rounded-full ${
        status === "active"
          ? "bg-green-500 shadow-[0_0_8px_rgba(16,185,129,0.6)]"
          : "bg-slate-700"
      }`}
    ></div>
  </GlassCard>
);

const PolicyRow = ({ title, desc, checked, badge }: any) => (
  <div className="flex items-center justify-between pb-4 border-b border-white/5 last:border-0 last:pb-0">
    <div>
      <div className="flex items-center gap-2">
        <h4 className="font-medium text-white">{title}</h4>
        {badge && (
          <span className="text-[10px] bg-ara-primary/20 text-ara-primary px-1.5 py-0.5 rounded border border-ara-primary/30">
            {badge}
          </span>
        )}
      </div>
      <p className="text-xs text-slate-400 mt-1">{desc}</p>
    </div>
    <ToggleSwitch checked={checked} />
  </div>
);

const GateConfigRow = ({ action, threshold }: any) => (
  <div className="flex items-center justify-between p-3 bg-white/5 rounded">
    <span className="text-sm text-slate-300">{action}</span>
    <div className="flex items-center gap-2">
      <select className="bg-black border border-white/10 text-xs rounded px-2 py-1 text-slate-300">
        <option>{threshold}</option>
        <option>Auto-Approve</option>
      </select>
    </div>
  </div>
);

const ToggleSwitch = ({
  checked,
  color = "orange",
}: {
  checked: boolean;
  color?: "orange" | "green";
}) => {
  const activeBg = color === "orange" ? "bg-ara-primary" : "bg-green-500";

  return (
    <div
      className={`w-10 h-5 rounded-full relative transition-colors cursor-pointer ${
        checked ? activeBg : "bg-slate-700"
      }`}
    >
      <div
        className={`absolute top-1 w-3 h-3 bg-white rounded-full transition-all duration-200 ${
          checked ? "left-6" : "left-1"
        }`}
      ></div>
    </div>
  );
};
