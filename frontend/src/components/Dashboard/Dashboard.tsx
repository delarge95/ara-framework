import React from "react";
import { AppMode } from "../../types";
import { LiteDashboard } from "./LiteDashboard";
import { ProDashboard } from "./ProDashboard";

interface DashboardProps {
  mode: AppMode;
}

const mockModels = [
  {
    rank: 1,
    name: "GPT-5.1 Thinking",
    provider: "OpenAI",
    context: "128K",
    gpqa: "89.1",
    swe: "73.2",
    strength: "General reasoning",
    type: "cloud",
  },
  {
    rank: 2,
    name: "Claude 4.5 Sonnet",
    provider: "Anthropic",
    context: "200K",
    gpqa: "88.8",
    swe: "71.5",
    strength: "Coding & Analysis",
    type: "cloud",
  },
  {
    rank: 3,
    name: "DeepSeek V3.1",
    provider: "DeepSeek",
    context: "128K",
    gpqa: "87.9",
    swe: "69.8",
    strength: "Cost efficiency",
    type: "cloud",
  },
  {
    rank: 4,
    name: "Qwen 2.5 Coder 32B",
    provider: "Alibaba",
    context: "32K",
    gpqa: "86.3",
    swe: "67.4",
    strength: "Code generation",
    type: "cloud",
  },
  {
    rank: 5,
    name: "Mistral Nemo",
    provider: "Mistral AI",
    context: "128K",
    gpqa: "85.7",
    swe: "65.9",
    strength: "Multilingual",
    type: "cloud",
  },
  {
    rank: 6,
    name: "Llama 3.1 405B",
    provider: "Meta",
    context: "128K",
    gpqa: "84.2",
    swe: "63.1",
    strength: "Open source",
    type: "cloud",
  },
  {
    rank: 7,
    name: "Phi-3.5 Mini Instruct",
    provider: "Microsoft",
    context: "128K",
    gpqa: "82.1",
    swe: "58.7",
    strength: "Small & efficient",
    type: "local",
    size: "2.3GB",
    quantization: "Q4_K_M",
    speed: "45ms",
  },
  {
    rank: 8,
    name: "Qwen 2.5-Coder-7B",
    provider: "Alibaba",
    context: "32K",
    gpqa: "79.8",
    swe: "55.3",
    strength: "Local coding",
    type: "local",
    size: "4.8GB",
    quantization: "Q5_K_M",
    speed: "120ms",
  },
];

export const Dashboard: React.FC<DashboardProps> = ({ mode }) => {
  if (mode === "lite") {
    return <LiteDashboard models={mockModels} />;
  }
  return <ProDashboard models={mockModels} />;
};
