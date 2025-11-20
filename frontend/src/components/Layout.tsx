import React, { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import {
  LayoutDashboard,
  Database,
  BookOpen,
  Cpu,
  Activity,
  ShieldAlert,
  Zap,
  Settings,
  Layers,
  GraduationCap,
  ChevronLeft,
  ChevronRight,
  Menu,
} from "lucide-react";
import { AppMode } from "../types";

interface LayoutProps {
  children: React.ReactNode;
  mode: AppMode;
  setMode: (mode: AppMode) => void;
}

export const Layout: React.FC<LayoutProps> = ({ children, mode, setMode }) => {
  const location = useLocation();
  const [isCollapsed, setIsCollapsed] = useState(false);

  const isActive = (path: string) => location.pathname === path;

  return (
    <div className="flex h-screen w-full overflow-hidden bg-ara-bg text-slate-200 font-sans selection:bg-ara-primary selection:text-white">
      {/* Background Mesh Gradient */}
      <div className="fixed top-[-20%] right-[-10%] w-[800px] h-[800px] rounded-full bg-[radial-gradient(circle,rgba(210,105,30,0.15)_0%,transparent_70%)] pointer-events-none z-0 blur-3xl" />
      <div className="fixed bottom-[-20%] left-[-10%] w-[600px] h-[600px] rounded-full bg-[radial-gradient(circle,rgba(16,185,129,0.05)_0%,transparent_70%)] pointer-events-none z-0 blur-3xl" />

      {/* Sidebar */}
      <aside
        className={`relative bg-ara-surface/50 backdrop-blur-xl border-r border-white/5 flex flex-col z-10 transition-all duration-300 ease-in-out ${
          isCollapsed ? "w-20" : "w-72"
        }`}
      >
        {/* Collapse Button */}
        <button
          onClick={() => setIsCollapsed(!isCollapsed)}
          className="absolute -right-3 top-8 bg-ara-surface border border-white/10 text-slate-400 p-1 rounded-full hover:text-white hover:bg-ara-primary hover:border-ara-primary transition-colors z-50 shadow-lg"
        >
          {isCollapsed ? <ChevronRight size={14} /> : <ChevronLeft size={14} />}
        </button>

        <div
          className={`p-6 flex items-center gap-3 ${
            isCollapsed ? "justify-center" : ""
          }`}
        >
          <div className="w-8 h-8 min-w-[32px] bg-gradient-to-tr from-ara-primary to-amber-600 rounded flex items-center justify-center shadow-[0_0_15px_rgba(210,105,30,0.4)]">
            <span className="font-serif font-bold text-white text-lg">A</span>
          </div>
          {!isCollapsed && (
            <div className="overflow-hidden whitespace-nowrap">
              <h1 className="font-serif text-xl font-bold tracking-wide text-white">
                ARA 2.2
              </h1>
              <span className="text-[10px] uppercase tracking-widest text-ara-primary opacity-80">
                Platform
              </span>
            </div>
          )}
        </div>

        {/* Mode Switcher */}
        <div
          className={`px-4 mb-6 ${isCollapsed ? "flex justify-center" : ""}`}
        >
          {isCollapsed ? (
            <button
              onClick={() => setMode(mode === "pro" ? "lite" : "pro")}
              className={`w-10 h-10 rounded-lg flex items-center justify-center transition-all duration-300 ${
                mode === "pro"
                  ? "bg-ara-primary/20 text-ara-primary border border-ara-primary/30"
                  : "bg-green-500/20 text-green-400 border border-green-500/30"
              }`}
              title={`Switch to ${mode === "pro" ? "Lite" : "Pro"}`}
            >
              {mode === "pro" ? <Zap size={18} /> : <ShieldAlert size={18} />}
            </button>
          ) : (
            <div className="bg-black/40 p-1 rounded-lg flex border border-white/10">
              <button
                onClick={() => setMode("pro")}
                className={`flex-1 py-2 text-xs font-medium rounded-md transition-all duration-300 ${
                  mode === "pro"
                    ? "bg-ara-primary/20 text-ara-primary shadow-[0_0_10px_rgba(210,105,30,0.2)] border border-ara-primary/30"
                    : "text-slate-500 hover:text-slate-300"
                }`}
              >
                PRO SaaS
              </button>
              <button
                onClick={() => setMode("lite")}
                className={`flex-1 py-2 text-xs font-medium rounded-md transition-all duration-300 ${
                  mode === "lite"
                    ? "bg-green-500/20 text-green-400 shadow-[0_0_10px_rgba(16,185,129,0.2)] border border-green-500/30"
                    : "text-slate-500 hover:text-slate-300"
                }`}
              >
                LITE Student
              </button>
            </div>
          )}
        </div>

        <nav className="flex-1 px-3 space-y-1 overflow-y-auto custom-scrollbar">
          <NavSection title="SYSTEM" isCollapsed={isCollapsed}>
            <NavLink
              to="/"
              icon={LayoutDashboard}
              label="Dashboard"
              active={isActive("/")}
              collapsed={isCollapsed}
            />
          </NavSection>

          <NavSection title="INTELLIGENCE" isCollapsed={isCollapsed}>
            <NavLink
              to="/docs/models"
              icon={Database}
              label="Model Leaderboard"
              active={isActive("/docs/models")}
              collapsed={isCollapsed}
            />
            <NavLink
              to="/docs/architecture"
              icon={Layers}
              label="System Architecture"
              active={isActive("/docs/architecture")}
              collapsed={isCollapsed}
            />
          </NavSection>

          <NavSection title="EDUCATION" isCollapsed={isCollapsed}>
            <NavLink
              to="/learning/concepts"
              icon={BookOpen}
              label="Deep Concepts"
              active={isActive("/learning/concepts")}
              collapsed={isCollapsed}
            />
            <NavLink
              to="/learning/glossary"
              icon={GraduationCap}
              label="Glossary & Tools"
              active={isActive("/learning/glossary")}
              collapsed={isCollapsed}
            />
          </NavSection>

          <NavSection title="INFRASTRUCTURE" isCollapsed={isCollapsed}>
            <NavLink
              to="#"
              icon={Cpu}
              label="Compute Nodes"
              active={false}
              collapsed={isCollapsed}
              disabled
            />
            <NavLink
              to="#"
              icon={Activity}
              label="Telemetry"
              active={false}
              collapsed={isCollapsed}
              disabled
            />
          </NavSection>
        </nav>

        <div className="p-4 border-t border-white/5">
          <Link
            to="/config"
            className={`flex items-center gap-3 px-3 py-2 text-slate-400 hover:text-white cursor-pointer rounded-lg hover:bg-white/5 transition-colors 
              ${isActive("/config") ? "bg-white/5 text-white" : ""}
              ${isCollapsed ? "justify-center" : ""}`}
          >
            <Settings
              size={20}
              className={isActive("/config") ? "text-ara-primary" : ""}
            />
            {!isCollapsed && (
              <span className="text-sm font-medium">Configuration</span>
            )}
          </Link>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 overflow-y-auto relative z-10 bg-ara-bg/50">
        {/* Top Bar */}
        <header className="h-16 border-b border-white/5 bg-ara-bg/80 backdrop-blur-md sticky top-0 z-20 flex items-center justify-between px-8">
          <div className="flex items-center gap-2">
            {mode === "pro" ? (
              <span className="flex items-center gap-2 text-xs font-mono text-ara-primary bg-ara-primary/10 px-2 py-1 rounded border border-ara-primary/20">
                <Zap size={12} /> SYSTEM ACTIVE
              </span>
            ) : (
              <span className="flex items-center gap-2 text-xs font-mono text-green-400 bg-green-900/20 px-2 py-1 rounded border border-green-500/20">
                <ShieldAlert size={12} /> LOCAL MODE
              </span>
            )}
          </div>
          <div className="flex items-center gap-4">
            <div className="text-right hidden md:block">
              <div className="text-xs text-slate-400">v2.2.0-build.492</div>
              <div className="text-[10px] text-slate-600 font-mono">
                LATENCY: 12ms
              </div>
            </div>
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-slate-700 to-slate-800 border border-white/10 flex items-center justify-center text-xs text-slate-300 font-mono">
              usr
            </div>
          </div>
        </header>

        <div className="p-8 pb-20 min-h-full">{children}</div>
      </main>
    </div>
  );
};

const NavSection: React.FC<{
  title: string;
  children: React.ReactNode;
  isCollapsed: boolean;
}> = ({ title, children, isCollapsed }) => (
  <div className="mb-6">
    {!isCollapsed && (
      <div className="text-[10px] font-mono font-bold text-slate-600 px-4 mb-2 tracking-wider">
        {title}
      </div>
    )}
    <div className="space-y-0.5">{children}</div>
  </div>
);

const NavLink: React.FC<{
  to: string;
  icon: React.ElementType;
  label: string;
  active: boolean;
  collapsed: boolean;
  disabled?: boolean;
}> = ({ to, icon: Icon, label, active, collapsed, disabled }) => (
  <Link to={to} className={disabled ? "pointer-events-none" : ""}>
    <div
      className={`flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-200 group relative
            ${
              active
                ? "bg-white/5 text-white border border-white/10 shadow-sm"
                : "text-slate-400 hover:text-slate-200 hover:bg-white/5"
            }
            ${disabled ? "opacity-50" : ""}
            ${collapsed ? "justify-center" : ""}
        `}
    >
      <Icon
        size={20}
        className={
          active
            ? "text-ara-primary"
            : "text-slate-500 group-hover:text-slate-300"
        }
      />
      {!collapsed && <span className="text-sm font-medium">{label}</span>}

      {/* Tooltip for collapsed state */}
      {collapsed && (
        <div className="absolute left-full ml-2 px-2 py-1 bg-slate-800 text-white text-xs rounded opacity-0 group-hover:opacity-100 pointer-events-none whitespace-nowrap border border-white/10 z-50">
          {label}
        </div>
      )}
    </div>
  </Link>
);
