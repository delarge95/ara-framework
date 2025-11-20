import React, { useState } from "react";
import { GlassCard } from "../ui/GlassCard";
import {
  GitBranch,
  Shield,
  Zap,
  Activity,
  Server,
  Lock,
  RefreshCw,
  Clock,
  AlertTriangle,
  Terminal,
  Database,
  ArrowRight,
  CheckCircle,
} from "lucide-react";

export const Architecture: React.FC = () => {
  const [activeTab, setActiveTab] = useState<"pro" | "lite">("pro");

  return (
    <div className="animate-fade-in max-w-7xl mx-auto pb-20">
      <header className="mb-12 border-b border-white/10 pb-8">
        <h1 className="text-5xl font-serif text-white mb-4">
          System Architecture & Specs
        </h1>
        <p className="text-slate-400 max-w-4xl text-lg font-light leading-relaxed">
          Detailed technical specifications for the{" "}
          <strong>ARA 2.2 Orchestration Framework</strong>. This documentation
          covers the transition from theoretical models to production-grade
          implementation, including "honest autopsies" of previous failures and
          the exact code logic used in the current deployment.
        </p>
      </header>

      {/* Tab Switcher */}
      <div className="flex gap-8 mb-10 border-b border-white/10">
        <button
          onClick={() => setActiveTab("pro")}
          className={`pb-4 px-2 text-base font-medium transition-all relative flex items-center gap-2 ${
            activeTab === "pro"
              ? "text-ara-primary"
              : "text-slate-500 hover:text-slate-300"
          }`}
        >
          <Zap size={18} />
          ARA 2.2 (Pro SaaS)
          {activeTab === "pro" && (
            <div className="absolute bottom-0 left-0 w-full h-0.5 bg-ara-primary shadow-[0_0_10px_rgba(210,105,30,0.5)]"></div>
          )}
        </button>
        <button
          onClick={() => setActiveTab("lite")}
          className={`pb-4 px-2 text-base font-medium transition-all relative flex items-center gap-2 ${
            activeTab === "lite"
              ? "text-green-400"
              : "text-slate-500 hover:text-slate-300"
          }`}
        >
          <Server size={18} />
          ARA Lite 0.2 (Student/Local)
          {activeTab === "lite" && (
            <div className="absolute bottom-0 left-0 w-full h-0.5 bg-green-400 shadow-[0_0_10px_rgba(16,185,129,0.5)]"></div>
          )}
        </button>
      </div>

      {activeTab === "pro" ? <ProSpecs /> : <LiteSpecs />}
    </div>
  );
};

const ProSpecs = () => (
  <div className="space-y-16">
    <section>
      <h2 className="text-2xl font-serif text-white mb-6 flex items-center gap-3">
        <AlertTriangle className="text-red-500" />
        Critical Autopsy: Why ARA 2.1 Failed
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <GlassCard className="border-l-2 border-red-500/50">
          <h3 className="font-bold text-red-400 mb-2">
            Failure #1: Telemetry as an "Idea"
          </h3>
          <p className="text-sm text-slate-400 mb-4">
            We treated telemetry as a "nice to have". In production, without P95
            latency tracking per-phase, we couldn't prove the "Router
            Cache-First" actually saved time. The system was a black box.
          </p>
          <div className="text-xs bg-red-900/20 p-2 rounded border border-red-500/20 text-red-300">
            <strong>Fix 2.2:</strong> Telemetry Engine is now the core. Alerting
            on cache_hit_rate less than 90%.
          </div>
        </GlassCard>
        <GlassCard className="border-l-2 border-red-500/50">
          <h3 className="font-bold text-red-400 mb-2">
            Failure #2: "Stale" Routing
          </h3>
          <p className="text-sm text-slate-400 mb-4">
            Model benchmarks change weekly. Our router used hardcoded TTL. When
            Claude 4.5 improved, ARA continued routing to GPT-5 for 24h, wasting
            money and performance.
          </p>
          <div className="text-xs bg-red-900/20 p-2 rounded border border-red-500/20 text-red-300">
            <strong>Fix 2.2:</strong> Event-driven invalidation. Router updates
            instantly via Model Card signals.
          </div>
        </GlassCard>
      </div>
    </section>

    <section>
      <h2 className="text-2xl font-serif text-white mb-6 flex items-center gap-3">
        <GitBranch className="text-ara-primary" />
        Adaptive Router 2.2: Implementation
      </h2>
      <p className="text-slate-400 mb-6 max-w-3xl">
        The heart of ARA 2.2 is a "Cache-First" decision engine. It doesn't just
        pick a model; it decides if computation is even necessary. It uses a
        LightGBM classifier to detect "Novelty" in prompts.
      </p>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
          <div className="bg-[#0d1117] rounded-lg border border-white/10 overflow-hidden my-4 font-mono text-xs shadow-inner">
            <div className="bg-white/5 px-4 py-2 border-b border-white/5 flex items-center gap-2 text-slate-400">
              <Terminal size={12} />
              <span>/core/router/AdaptiveRouter.ts</span>
            </div>
            <div className="p-4 overflow-x-auto text-slate-300 leading-relaxed">
              <pre>{`class AdaptiveRouter {
  private cache = new LRUCache({ max: 10_000, ttl: 900_000 }); 
  private classifier: NoveltyDetector;

  async route(task: Task): Promise<RoutingDecision> {
    const features = this._extractFeatures(task);
    
    if (this.classifier.predictNovelty(features) > 0.85) {
      return await this._routeWithGemini(task);
    }

    const cacheKey = this._computeCacheKey(task);
    const cached = this.cache.get(cacheKey);
    if (cached) return cached;

    const decision = await this._localRoute(task);
    this._updateCache(cacheKey, decision).catch(console.error);
    
    return decision;
  }
}`}</pre>
            </div>
          </div>
        </div>
        <div className="space-y-4">
          <div className="bg-black/40 p-4 rounded border border-white/10">
            <div className="text-ara-primary font-mono text-xs mb-1">
              LATENCY GOAL
            </div>
            <div className="text-2xl font-bold text-white">15ms</div>
            <div className="text-slate-500 text-xs">
              For cache hits (94% of traffic)
            </div>
          </div>
          <div className="bg-black/40 p-4 rounded border border-white/10">
            <div className="text-ara-primary font-mono text-xs mb-1">
              ALGORITHM
            </div>
            <div className="text-xl font-bold text-white">LightGBM</div>
            <div className="text-slate-500 text-xs">
              Gradient boosting for novelty scoring
            </div>
          </div>
          <div className="bg-black/40 p-4 rounded border border-white/10">
            <div className="text-ara-primary font-mono text-xs mb-1">
              SECURITY
            </div>
            <div className="text-xl font-bold text-white">HMAC</div>
            <div className="text-slate-500 text-xs">
              Prevents cache poisoning attacks
            </div>
          </div>
        </div>
      </div>
    </section>

    <section>
      <h2 className="text-2xl font-serif text-white mb-6 flex items-center gap-3">
        <Shield className="text-blue-400" />
        ARAShield: Supply Chain Defense
      </h2>
      <GlassCard className="bg-blue-900/10 border-blue-500/20">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-bold text-white">
            The "Package Hallucination" Threat
          </h3>
          <span className="text-xs bg-blue-500/20 text-blue-300 px-2 py-1 rounded">
            Active Protection
          </span>
        </div>
        <p className="text-sm text-slate-300 mb-4">
          LLMs often suggest libraries that don't exist. Attackers register
          these names with malicious code. ARAShield uses a{" "}
          <strong>Two-Tier Verification</strong> system to prevent this.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-mono">
          <div className="bg-black/50 p-3 rounded border border-white/10">
            <div className="text-blue-400 font-bold mb-1">
              TIER 1: FAST PATH (10ms)
            </div>
            Local Regex Whitelist of top 5000 packages (React, Lodash,
            Pandas...).
            <br />
            <span className="text-green-500">
              if (whitelist.has(pkg)) return ALLOW;
            </span>
          </div>
          <div className="bg-black/50 p-3 rounded border border-white/10">
            <div className="text-blue-400 font-bold mb-1">
              TIER 2: DEEP VERIFY (Async)
            </div>
            Gemini agent checks Registry API, license, and recent CVEs.
            <br />
            <span className="text-amber-500">
              if (!registry.exists(pkg)) return BLOCK;
            </span>
          </div>
        </div>
      </GlassCard>
    </section>
  </div>
);

const LiteSpecs = () => (
  <div className="space-y-16">
    <section>
      <h2 className="text-2xl font-serif text-white mb-6 flex items-center gap-3">
        <Server className="text-green-400" />
        Lite 0.2 Philosophy: "Honest Bootstrap"
      </h2>
      <p className="text-slate-400 mb-6 leading-relaxed">
        ARA Lite 0.1 failed because it relied on "hacks" (reverse engineering
        Copilot, batching queries illegally).
        <strong>Lite 0.2 is strictly legal and predictable.</strong> It assumes
        the user has zero budget but decent hardware (8GB+ RAM).
      </p>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-4 bg-green-900/10 border border-green-500/20 rounded-lg">
          <h3 className="font-bold text-green-400 mb-2">Local First</h3>
          <p className="text-xs text-slate-400">
            Ollama (Phi-3.5, Qwen) handles 90% of tasks. Zero marginal cost.
          </p>
        </div>
        <div className="p-4 bg-green-900/10 border border-green-500/20 rounded-lg">
          <h3 className="font-bold text-green-400 mb-2">Strict Budget</h3>
          <p className="text-xs text-slate-400">
            Hard cap on paid APIs ($5/mo Anthropic Edu). No surprise bills.
          </p>
        </div>
        <div className="p-4 bg-green-900/10 border border-green-500/20 rounded-lg">
          <h3 className="font-bold text-green-400 mb-2">No Hacks</h3>
          <p className="text-xs text-slate-400">
            Uses only documented, official endpoints. No risk of account bans.
          </p>
        </div>
      </div>
    </section>

    <section>
      <h2 className="text-2xl font-serif text-white mb-6 flex items-center gap-3">
        <Database className="text-slate-300" />
        Approved Tool Stack (Lite)
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <GlassCard className="p-4 text-center">
          <div className="font-bold text-white mb-1">Ollama</div>
          <div className="text-xs text-green-400 mb-2">Backbone</div>
          <p className="text-xs text-slate-400">
            Runs local models via API. Standard interface.
          </p>
        </GlassCard>
        <GlassCard className="p-4 text-center">
          <div className="font-bold text-white mb-1">Phi-3.5</div>
          <div className="text-xs text-green-400 mb-2">Logic & Glue</div>
          <p className="text-xs text-slate-400">
            Microsoft's tiny giant. 3.8B params. Fast on CPU.
          </p>
        </GlassCard>
        <GlassCard className="p-4 text-center">
          <div className="font-bold text-white mb-1">Perplexity</div>
          <div className="text-xs text-amber-400 mb-2">Research Only</div>
          <p className="text-xs text-slate-400">
            Used strictly for web search. No batching allowed.
          </p>
        </GlassCard>
        <GlassCard className="p-4 text-center">
          <div className="font-bold text-white mb-1">Claude Edu</div>
          <div className="text-xs text-red-400 mb-2">Emergency</div>
          <p className="text-xs text-slate-400">
            The "Professor". Used only when local models get stuck.
          </p>
        </GlassCard>
      </div>
    </section>
  </div>
);
