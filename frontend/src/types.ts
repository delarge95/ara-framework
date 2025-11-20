import React from "react";

export type AppMode = "pro" | "lite";

export interface BudgetData {
  service: string;
  used: number;
  limit: number;
  unit: string;
  cost: string;
  healthy?: boolean;
}

export interface ModelStatus {
  name: string;
  role: string;
  status: "ready" | "loading" | "offline";
  latency?: string;
  progress?: number;
}

export interface ModelData {
  rank: number;
  name: string;
  provider: string;
  context: string;
  gpqa: string;
  swe: string;
  strength: string;
  // Campos adicionales para LiteDashboard
  type?: "local" | "cloud";
  size?: string;
  quantization?: string;
  speed?: string;
}

export interface NavItem {
  label: string;
  path: string;
  icon: React.ElementType;
}
