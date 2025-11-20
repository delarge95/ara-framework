import React from "react";
import { ModelData } from "../../types";
import { GlassCard } from "../ui/GlassCard";

const modelsData: ModelData[] = [
  {
    rank: 1,
    name: "GPT-5.1 Thinking",
    provider: "OpenAI",
    context: "500k",
    gpqa: "88.1%",
    swe: "76.3%",
    strength: "Adaptive Reasoning, Architecture",
  },
  {
    rank: 2,
    name: "Grok 4.1 Thinking",
    provider: "xAI",
    context: "1M",
    gpqa: "88.4%",
    swe: "75.0%",
    strength: "Real-time Data, Physics/Math",
  },
  {
    rank: 3,
    name: "Gemini 2.5 Pro",
    provider: "Google",
    context: "2M+",
    gpqa: "86.4%",
    swe: "67.2%",
    strength: "Massive Context, Deep Research",
  },
  {
    rank: 4,
    name: "Claude 4.5 Sonnet",
    provider: "Anthropic",
    context: "1M",
    gpqa: "83.4%",
    swe: "77.2%",
    strength: "Vibe Coding, Agentic Reliability",
  },
  {
    rank: 5,
    name: "Kimi k2 Thinking",
    provider: "Moonshot",
    context: "256k",
    gpqa: "86.4%",
    swe: "71.3%",
    strength: "Long Tool Chains, Autonomous Agents",
  },
  {
    rank: 6,
    name: "Qwen 3 Max",
    provider: "Alibaba",
    context: "128k",
    gpqa: "81.4%",
    swe: "69.6%",
    strength: "Multilingual, Cost Efficiency",
  },
  {
    rank: 7,
    name: "DeepSeek V3.1",
    provider: "DeepSeek",
    context: "128k",
    gpqa: "80.1%",
    swe: "N/A",
    strength: "Backend Boilerplate, Price ($0.30/M)",
  },
];

export const Leaderboard: React.FC = () => {
  return (
    <div className="animate-fade-in">
      <div className="max-w-5xl mx-auto">
        <h2 className="text-3xl font-serif mb-4 text-white">
          Strategic Ranking{" "}
          <span className="text-ara-primary text-lg font-sans font-normal ml-2">
            (Nov 2025)
          </span>
        </h2>
        <p className="text-slate-400 mb-8 max-w-3xl text-lg font-light">
          Based on frontier benchmarks:{" "}
          <span className="text-slate-200">GPQA Diamond</span> (Extreme Science)
          and <span className="text-slate-200">SWE-bench Verified</span>{" "}
          (Software Engineering). Data extracted from{" "}
          <em>Strategic Research Report Nov 2025</em> &{" "}
          <em>ARA 2.2 Model Matrix</em>.
        </p>

        <GlassCard className="overflow-hidden p-0">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-white/5 border-b border-white/10 text-xs uppercase tracking-wider text-slate-400">
                  <th className="p-5 font-medium">Rank</th>
                  <th className="p-5 font-medium">Model</th>
                  <th className="p-5 font-medium">Specialty</th>
                  <th className="p-5 font-medium font-mono">Context</th>
                  <th className="p-5 font-medium font-mono text-green-500">
                    GPQA
                  </th>
                  <th className="p-5 font-medium font-mono text-blue-400">
                    SWE-bench
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {modelsData.map((m) => (
                  <tr
                    key={m.name}
                    className="hover:bg-white/5 transition-colors group"
                  >
                    <td className="p-5 font-mono text-ara-primary font-bold text-lg opacity-70 group-hover:opacity-100">
                      #{m.rank}
                    </td>
                    <td className="p-5">
                      <div className="font-bold text-slate-200">{m.name}</div>
                      <div className="text-xs text-slate-500">{m.provider}</div>
                    </td>
                    <td className="p-5 text-sm text-slate-400 italic">
                      {m.strength}
                    </td>
                    <td className="p-5 font-mono text-xs text-slate-300">
                      {m.context}
                    </td>
                    <td className="p-5 font-mono text-green-400 font-bold">
                      {m.gpqa}
                    </td>
                    <td className="p-5 font-mono text-blue-400 font-bold">
                      {m.swe}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </GlassCard>
      </div>
    </div>
  );
};
