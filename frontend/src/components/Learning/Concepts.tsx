import React from "react";
import { GlassCard } from "../ui/GlassCard";
import { Wand2, Network, ShieldCheck } from "lucide-react";

const Badge: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <span className="text-[10px] uppercase font-bold tracking-wider bg-ara-primary/20 text-ara-primary border border-ara-primary/30 px-2 py-1 rounded ml-3">
    {children}
  </span>
);

export const Concepts: React.FC = () => {
  return (
    <div className="animate-fade-in max-w-4xl mx-auto pb-20">
      <h1 className="text-4xl font-serif mb-12 text-white border-b border-white/10 pb-6">
        Frontier Concepts 2025
      </h1>

      <section className="mb-16">
        <h2 className="text-2xl text-ara-primary mb-6 flex items-center gap-3 font-serif">
          <Wand2 size={24} /> Vibe Coding <Badge>New Paradigm</Badge>
        </h2>
        <GlassCard className="p-8">
          <p className="mb-8 text-xl font-light text-slate-300 leading-relaxed">
            "High-level direction over syntax." The programmer relinquishes
            line-by-line authorship in favor of intent management.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6">
            <div className="p-5 bg-black/30 rounded-lg border-l-2 border-blue-500 hover:bg-black/50 transition-colors">
              <h4 className="font-bold mb-2 text-white">1. Vibe Check</h4>
              <p className="text-sm text-slate-400">
                Rapid generation with low-latency models (Grok 4.1) to validate
                UI/UX ideas instantly.
              </p>
            </div>
            <div className="p-5 bg-black/30 rounded-lg border-l-2 border-purple-500 hover:bg-black/50 transition-colors">
              <h4 className="font-bold mb-2 text-white">2. Agentic Loop</h4>
              <p className="text-sm text-slate-400">
                Deep refactoring using "Thinking" models (Claude 3.5, GPT-5.1)
                for structural integrity.
              </p>
            </div>
            <div className="p-5 bg-black/30 rounded-lg border-l-2 border-green-500 hover:bg-black/50 transition-colors">
              <h4 className="font-bold mb-2 text-white">3. Guardrails</h4>
              <p className="text-sm text-slate-400">
                Security validation to prevent "Zombie Code" and package
                hallucinations.
              </p>
            </div>
          </div>
        </GlassCard>
      </section>

      <section>
        <h2 className="text-2xl text-ara-primary mb-6 flex items-center gap-3 font-serif">
          <Network size={24} /> Model Context Protocol (MCP){" "}
          <Badge>Standard</Badge>
        </h2>
        <GlassCard>
          <div className="flex flex-col md:flex-row gap-8 items-center">
            <div className="flex-1">
              <p className="text-slate-300 mb-4 leading-relaxed">
                The industrial standard (USB-C for AI) connecting models with
                data. It eliminates the need for fragile "glue" code.
              </p>
              <ul className="space-y-3 mt-4">
                <li className="flex items-center gap-3 text-sm text-slate-400">
                  <ShieldCheck size={16} className="text-green-500" />
                  <span>Standardized security context</span>
                </li>
                <li className="flex items-center gap-3 text-sm text-slate-400">
                  <ShieldCheck size={16} className="text-green-500" />
                  <span>Universal data connectors (Postgres, Slack, Git)</span>
                </li>
                <li className="flex items-center gap-3 text-sm text-slate-400">
                  <ShieldCheck size={16} className="text-green-500" />
                  <span>Local-first execution preference</span>
                </li>
              </ul>
            </div>
            <div className="w-full md:w-1/3 aspect-square bg-black/40 rounded-full border border-white/5 flex items-center justify-center relative">
              <div className="absolute inset-0 rounded-full border border-ara-primary/20 animate-ping opacity-20"></div>
              <div className="text-center">
                <div className="font-mono text-2xl font-bold text-white">
                  MCP
                </div>
                <div className="text-[10px] text-slate-500 uppercase tracking-widest">
                  Core Protocol
                </div>
              </div>
            </div>
          </div>
        </GlassCard>
      </section>
    </div>
  );
};
