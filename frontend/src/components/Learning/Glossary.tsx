import React, { useState, useMemo } from "react";
import { GlassCard } from "../ui/GlassCard";
import {
  Search,
  Book,
  Shield,
  Cpu,
  GitBranch,
  Zap,
  Terminal,
  Server,
} from "lucide-react";

type Category = "core" | "infra" | "security" | "ai" | "tools";

const dictionary: { term: string; def: string; cat: Category }[] = [
  // Core Concepts
  {
    term: "Agent Drift",
    cat: "core",
    def: "The tendency of autonomous AI agents to lose context or deviate from original architectural patterns over long sessions, often introducing regressions.",
  },
  {
    term: "Vibe Coding",
    cat: "core",
    def: "A development paradigm where the human provides high-level intent/aesthetics ('vibes') while the AI handles syntax. Shifts role from Writer to Architect.",
  },
  {
    term: "Thinking Models",
    cat: "core",
    def: "LLMs (e.g., o1, Kimi k2) that use inference-time compute to generate hidden 'chains of thought' before outputting, improving math/logic performance.",
  },
  {
    term: "Human Gates",
    cat: "core",
    def: "Mandatory checkpoints in the orchestration flow where a human must approve an action (e.g., deploy, delete DB) before the AI proceeds.",
  },
  {
    term: "Zero-Friction UX",
    cat: "core",
    def: "A design philosophy in ARA where complex AI operations (indexing, warming) happen in the background without blocking the user interface.",
  },
  {
    term: "Agentic Loop",
    cat: "core",
    def: "A cyclical process where an AI agent plans, executes, observes results, and corrects itself (OODA loop) until a goal is met.",
  },
  {
    term: "Compound AI",
    cat: "core",
    def: "System architecture combining multiple specialized models (e.g., one for logic, one for creativity) to solve complex tasks better than a single monolithic model.",
  },

  // Infrastructure & Protocols
  {
    term: "MCP (Model Context Protocol)",
    cat: "infra",
    def: "Open standard (USB-C for AI) connecting LLMs to local data sources (Postgres, Git) securely without fragile glue code.",
  },
  {
    term: "Warm Pool",
    cat: "infra",
    def: "Strategy of keeping specific models loaded in RAM/VRAM to prevent the 10-30s latency penalty of cold starts during switching.",
  },
  {
    term: "Adaptive Router",
    cat: "infra",
    def: "ARA's decision engine that routes prompts to the cheapest/fastest model capable of the task, utilizing caching and novelty detection.",
  },
  {
    term: "Latency P95",
    cat: "infra",
    def: "A metric indicating that 95% of requests are faster than this value. ARA targets <50ms P95 for router decisions.",
  },
  {
    term: "SSE (Server-Sent Events)",
    cat: "infra",
    def: "One-way streaming protocol used by MCP to send real-time updates from tools to the host (LLM) without polling.",
  },
  {
    term: "JSON-RPC",
    cat: "infra",
    def: "Lightweight remote procedure call protocol used within MCP for message formatting between clients and servers.",
  },

  // Security
  {
    term: "TOCTOU",
    cat: "security",
    def: "Time-Of-Check to Time-Of-Use. A race condition where system state changes between security check and execution. ARA uses Optimistic Locking to fix this.",
  },
  {
    term: "Package Hallucination",
    cat: "security",
    def: "Attack vector where AI suggests non-existent library names, which attackers then register with malicious code. ARAShield blocks this.",
  },
  {
    term: "Optimistic Locking",
    cat: "security",
    def: "Concurrency control method where a transaction verifies data hasn't changed (via hash) before committing, preventing overwrite conflicts.",
  },
  {
    term: "ARAShield",
    cat: "security",
    def: "The security subsystem that verifies dependencies, scans generated code for vulnerabilities (SAST), and manages PII sanitization.",
  },
  {
    term: "Audit Log",
    cat: "security",
    def: "An immutable, append-only record of all critical actions and approvals within the system, essential for enterprise compliance.",
  },
  {
    term: "SAST",
    cat: "security",
    def: "Static Application Security Testing. Analyzing source code for security vulnerabilities without executing it (e.g., Semgrep).",
  },
  {
    term: "PII Sanitization",
    cat: "security",
    def: "Process of detecting and removing Personally Identifiable Information (emails, SSNs) from prompts before sending them to external LLMs.",
  },

  // AI & Models
  {
    term: "RAG",
    cat: "ai",
    def: "Retrieval-Augmented Generation. Enhancing model output by injecting relevant external data (docs, codebase) into the context window.",
  },
  {
    term: "CoT (Chain of Thought)",
    cat: "ai",
    def: "Prompting technique encouraging the model to explain its reasoning step-by-step, drastically reducing logical errors.",
  },
  {
    term: "Quantization",
    cat: "ai",
    def: "Reducing model precision (e.g., from FP16 to INT4) to lower memory usage and increase speed with minimal accuracy loss.",
  },
  {
    term: "Context Window",
    cat: "ai",
    def: "The amount of text (tokens) a model can 'see' at once. Gemini 2.5 Pro has 2M+, allowing it to ingest entire codebases.",
  },
  {
    term: "Embeddings",
    cat: "ai",
    def: "Vector representations of text. ARA uses GTE-Large embeddings to calculate semantic similarity for routing and retrieval.",
  },
  {
    term: "MoE (Mixture of Experts)",
    cat: "ai",
    def: "Architecture using multiple specialized sub-models (experts). Only relevant experts activate per token, increasing efficiency (e.g., Mixtral, Qwen).",
  },
  {
    term: "Fine-tuning",
    cat: "ai",
    def: "Process of training a pre-trained model on a smaller, specific dataset to specialize it for a task (e.g., coding, medical).",
  },
  {
    term: "Hallucination",
    cat: "ai",
    def: "When an LLM generates factually incorrect or nonsensical information confidently. A primary risk in automated workflows.",
  },
  {
    term: "KV Cache",
    cat: "ai",
    def: "Key-Value Cache. Storing intermediate attention computations to speed up token generation, critical for long-context inference.",
  },

  // Tools & Frameworks (New Category)
  {
    term: "Ollama",
    cat: "tools",
    def: "Tool for running LLMs locally. Powers ARA Lite's backend, enabling students to run models like Phi-3.5 on consumer hardware.",
  },
  {
    term: "ClickHouse",
    cat: "tools",
    def: "Columnar database used in ARA Pro for storing high-volume telemetry logs and immutable audit trails efficiently.",
  },
  {
    term: "LightGBM",
    cat: "tools",
    def: "Gradient boosting framework used by ARA's Novelty Classifier to decide if a prompt needs a 'Thinking' model or a fast cache hit.",
  },
  {
    term: "Jaeger",
    cat: "tools",
    def: "Distributed tracing system used to monitor the lifecycle of a request across ARA's microservices (Router -> MCP -> Model).",
  },
  {
    term: "Prometheus",
    cat: "tools",
    def: "Monitoring system that collects metrics (cache hit rate, latency) from ARA's components for the dashboard.",
  },
  {
    term: "Semgrep",
    cat: "tools",
    def: "Fast, open-source static analysis tool used by ARAShield to detect bugs and security vulnerabilities in generated code.",
  },
  {
    term: "Redis",
    cat: "tools",
    def: "In-memory data structure store used by ARA for the Semantic Cache layer to return sub-millisecond responses for repeated prompts.",
  },
  {
    term: "Terraform",
    cat: "tools",
    def: "Infrastructure as Code tool. ARA generates Terraform scripts to deploy the infrastructure it designs.",
  },
  {
    term: "GTE-Large",
    cat: "tools",
    def: "A specific embedding model used by ARA for semantic search, chosen for its high performance on retrieval benchmarks.",
  },
];

export const Glossary: React.FC = () => {
  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState<Category | "all">("all");

  const filteredTerms = useMemo(() => {
    return dictionary.filter((item) => {
      const matchesSearch =
        item.term.toLowerCase().includes(search.toLowerCase()) ||
        item.def.toLowerCase().includes(search.toLowerCase());
      const matchesFilter = filter === "all" || item.cat === filter;
      return matchesSearch && matchesFilter;
    });
  }, [search, filter]);

  return (
    <div className="animate-fade-in max-w-5xl mx-auto pb-20">
      <header className="mb-10">
        <h1 className="text-4xl font-serif text-white mb-4">
          Glossary & Tools
        </h1>
        <p className="text-slate-400">
          Comprehensive definition of terms, tools, and protocols used in the
          ARA Ecosystem.
        </p>
      </header>

      <div className="sticky top-20 z-30 bg-ara-bg/90 backdrop-blur-md py-4 mb-8 border-b border-white/10">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="relative flex-1">
            <Search
              className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500"
              size={18}
            />
            <input
              type="text"
              placeholder="Search terms (e.g., 'Ollama', 'Latency')..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full bg-black/40 border border-white/10 rounded-lg py-2 pl-10 pr-4 text-slate-200 focus:outline-none focus:border-ara-primary/50 transition-colors"
            />
          </div>
          <div className="flex gap-2 overflow-x-auto pb-2 md:pb-0 custom-scrollbar">
            {[
              { id: "all", label: "All", icon: Book },
              { id: "core", label: "Core", icon: Zap },
              { id: "infra", label: "Infra", icon: Server },
              { id: "security", label: "Security", icon: Shield },
              { id: "ai", label: "AI Models", icon: GitBranch },
              { id: "tools", label: "Stack", icon: Terminal },
            ].map((btn) => (
              <button
                key={btn.id}
                onClick={() => setFilter(btn.id as any)}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all whitespace-nowrap ${
                  filter === btn.id
                    ? "bg-white/10 text-white border border-white/20"
                    : "text-slate-500 hover:text-slate-300 hover:bg-white/5"
                }`}
              >
                <btn.icon size={14} />
                {btn.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {filteredTerms.map((item, idx) => (
          <GlassCard
            key={idx}
            className="hover:bg-white/5 transition-all group border-l-2 border-l-transparent hover:border-l-ara-primary"
          >
            <div className="flex justify-between items-start mb-2">
              <h3 className="text-lg font-bold text-white group-hover:text-ara-primary transition-colors">
                {item.term}
              </h3>
              <Badge cat={item.cat} />
            </div>
            <p className="text-slate-400 leading-relaxed text-sm">{item.def}</p>
          </GlassCard>
        ))}
      </div>

      {filteredTerms.length === 0 && (
        <div className="text-center py-20 text-slate-500">
          No terms found matching "{search}"
        </div>
      )}
    </div>
  );
};

const Badge = ({ cat }: { cat: Category }) => {
  const styles = {
    core: "text-ara-primary bg-ara-primary/10 border-ara-primary/20",
    infra: "text-purple-400 bg-purple-900/20 border-purple-500/20",
    security: "text-blue-400 bg-blue-900/20 border-blue-500/20",
    ai: "text-green-400 bg-green-900/20 border-green-500/20",
    tools: "text-amber-400 bg-amber-900/20 border-amber-500/20",
  };

  return (
    <span
      className={`text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded border ${styles[cat]}`}
    >
      {cat}
    </span>
  );
};
