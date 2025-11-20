import React, { useState } from "react";
import { GlassCard } from "../ui/GlassCard";
import {
  Search,
  BookOpen,
  Brain,
  Cpu,
  Database,
  Globe,
  Zap,
  Shield,
  Code,
  ChevronRight,
  Star,
} from "lucide-react";

interface GlossaryTerm {
  term: string;
  category: string;
  definition: string;
  example?: string;
  related?: string[];
}

const glossaryTerms: GlossaryTerm[] = [
  {
    term: "ARA (Agentic Reasoning Architecture)",
    category: "Architecture",
    definition:
      "Framework para orquestar múltiples agentes de IA con capacidades de reasoning automatizado y routing inteligente entre modelos.",
    example:
      "ARA permite que un agente arquitectónico tome decisiones y delegue tareas específicas a otros agentes especializados.",
    related: ["Agentic", "Orchestration", "Routing"],
  },
  {
    term: "Agentic",
    category: "Concepts",
    definition:
      "Capacidad de un agente de IA para tomar decisiones autónomas, planificar secuencias de acciones y adaptarse dinámicamente al contexto.",
    example:
      "Un agente agentic puede decidir automáticamente cuándo usar cada modelo basado en la complejidad de la tarea.",
    related: ["Autonomy", "Planning", "Decision Making"],
  },
  {
    term: "Multi-Agent Orchestration",
    category: "Architecture",
    definition:
      "Coordinación sistemática de múltiples agentes especializados para resolver tareas complejas de manera colaborativa.",
    example:
      "Un arquitecto de IA, un agente de código y un validador de seguridad trabajan juntos en un pipeline de desarrollo.",
    related: ["ARA", "Coordination", "Pipeline"],
  },
  {
    term: "Semantic Routing",
    category: "Performance",
    definition:
      "Enrutamiento inteligente de requests basado en el análisis semántico del contenido, optimizando latencia y calidad de respuesta.",
    example:
      "Una pregunta matemática simple se enruta automáticamente a Phi-3.5 mientras una consulta compleja va a GPT-5.1.",
    related: ["Intelligent Routing", "Context Analysis", "Optimization"],
  },
  {
    term: "Context-Aware Switching",
    category: "Performance",
    definition:
      "Cambio dinámico entre modelos manteniendo el contexto de la conversación para preservar la coherencia y reducir costos.",
    example:
      "Transición fluida de GPT-5.1 (análisis) a Claude 4.5 (código) sin pérdida de contexto.",
    related: ["Context Preservation", "Model Switching", "Cost Optimization"],
  },
  {
    term: "Guardrails",
    category: "Security",
    definition:
      "Mecanismos de seguridad y validación automática para prevenir alucinaciones, filtrar PII y cumplir políticas empresariales.",
    example:
      "ARAShield valida cada import de código contra npm registry antes de ejecutar.",
    related: ["Security", "Compliance", "Validation"],
  },
  {
    term: "Hot Pool Models",
    category: "Performance",
    definition:
      "Conjunto de modelos pre-cargados en memoria VRAM para minimizar latencia de cambio de contexto.",
    example:
      "Mantener GPT-5.1 y Claude 4.5 cargados en VRAM para respuestas instantáneas.",
    related: ["VRAM Management", "Latency Optimization", "Memory Pool"],
  },
  {
    term: "Quantization",
    category: "Optimization",
    definition:
      "Reducción del tamaño de modelos de IA mediante compresión numérica (Q4, Q5, Q8) manteniendo calidad aceptable.",
    example:
      "Q4_K_M comprime un modelo de 7B parámetros a ~3GB manteniendo 95% de la calidad original.",
    related: ["Model Compression", "VRAM Efficiency", "Quality Trade-offs"],
  },
  {
    term: "Local-First Architecture",
    category: "Architecture",
    definition:
      "Enfoque de desarrollo que prioriza capacidades locales (Ollama, Llama.cpp) con fallbacks cloud para máxima privacidad y control.",
    example:
      "ARA Lite ejecuta todo localmente con acceso controlado a GPT-5.1 solo para tareas críticas.",
    related: ["Privacy", "Local Processing", "Fallback Strategy"],
  },
  {
    term: "MCP (Model Context Protocol)",
    category: "Integration",
    definition:
      "Protocolo estándar para conectar modelos de IA con herramientas externas de manera segura y estructurada.",
    example:
      "MCP permite que un agente acceda a bases de datos, APIs y sistemas de archivos de forma controlada.",
    related: ["Protocol", "Tool Integration", "Security"],
  },
];

const categories = [
  { name: "All", icon: BookOpen },
  { name: "Architecture", icon: Cpu },
  { name: "Concepts", icon: Brain },
  { name: "Performance", icon: Zap },
  { name: "Security", icon: Shield },
  { name: "Optimization", icon: Database },
  { name: "Integration", icon: Globe },
];

export const Glossary: React.FC = () => {
  const [selectedCategory, setSelectedCategory] = useState("All");
  const [searchTerm, setSearchTerm] = useState("");
  const [expandedTerm, setExpandedTerm] = useState<string | null>(null);

  const filteredTerms = glossaryTerms.filter((term) => {
    const matchesCategory =
      selectedCategory === "All" || term.category === selectedCategory;
    const matchesSearch =
      term.term.toLowerCase().includes(searchTerm.toLowerCase()) ||
      term.definition.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  return (
    <div className="animate-fade-in max-w-6xl mx-auto pb-20">
      {/* Header */}
      <header className="mb-10 border-b border-white/10 pb-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-gradient-to-r from-purple-600 to-indigo-500 rounded-xl text-white shadow-lg">
              <BookOpen size={32} />
            </div>
            <div>
              <h1 className="text-4xl font-serif text-purple-400 mb-1">
                ARA Glossary
              </h1>
              <p className="text-slate-400">
                Comprehensive guide to Agentic Reasoning Architecture concepts
              </p>
            </div>
          </div>
          <div className="text-right">
            <div className="text-2xl font-mono text-purple-400">
              {glossaryTerms.length}
            </div>
            <div className="text-xs text-slate-500">Terms Defined</div>
          </div>
        </div>
      </header>

      {/* Search and Filter */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8 mb-10">
        {/* Sidebar Categories */}
        <div className="lg:col-span-1">
          <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
            <Brain size={20} className="text-purple-400" />
            Categories
          </h3>
          <div className="space-y-2">
            {categories.map((category) => {
              const Icon = category.icon;
              return (
                <button
                  key={category.name}
                  onClick={() => setSelectedCategory(category.name)}
                  className={`w-full flex items-center gap-3 p-3 rounded-lg transition-all text-left ${
                    selectedCategory === category.name
                      ? "bg-purple-500/20 border border-purple-500/30 text-white"
                      : "bg-white/5 border border-white/10 text-slate-400 hover:border-white/20 hover:text-slate-200"
                  }`}
                >
                  <Icon size={18} />
                  <span className="font-medium">{category.name}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Main Content */}
        <div className="lg:col-span-3 space-y-6">
          {/* Search */}
          <div className="relative">
            <Search
              size={20}
              className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400"
            />
            <input
              type="text"
              placeholder="Search terms, definitions, concepts..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:border-purple-500 focus:bg-purple-500/5 transition-all"
            />
          </div>

          {/* Results */}
          <div className="space-y-4">
            {filteredTerms.length === 0 ? (
              <GlassCard>
                <div className="text-center py-12">
                  <Search size={48} className="text-slate-600 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold text-slate-400 mb-2">
                    No terms found
                  </h3>
                  <p className="text-slate-500">
                    Try adjusting your search or category filter
                  </p>
                </div>
              </GlassCard>
            ) : (
              filteredTerms.map((term, index) => (
                <GlassCard
                  key={index}
                  className={`cursor-pointer transition-all hover:border-purple-500/30 ${
                    expandedTerm === term.term
                      ? "border-purple-500/50 bg-purple-500/5"
                      : ""
                  }`}
                >
                  <div
                    onClick={() =>
                      setExpandedTerm(
                        expandedTerm === term.term ? null : term.term
                      )
                    }
                  >
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center gap-3">
                        <div className="p-2 bg-purple-500/20 rounded-lg">
                          {categories.find((c) => c.name === term.category)
                            ?.icon &&
                            React.createElement(
                              categories.find((c) => c.name === term.category)!
                                .icon,
                              {
                                size: 16,
                                className: "text-purple-400",
                              }
                            )}
                        </div>
                        <div>
                          <h3 className="text-lg font-semibold text-white">
                            {term.term}
                          </h3>
                          <span className="text-xs px-2 py-1 bg-purple-900/30 text-purple-400 rounded">
                            {term.category}
                          </span>
                        </div>
                      </div>
                      <ChevronRight
                        size={20}
                        className={`text-slate-400 transition-transform ${
                          expandedTerm === term.term
                            ? "rotate-90 text-purple-400"
                            : ""
                        }`}
                      />
                    </div>

                    <p className="text-slate-300 leading-relaxed">
                      {term.definition}
                    </p>
                  </div>

                  {expandedTerm === term.term && (
                    <div className="mt-4 pt-4 border-t border-white/10 space-y-4">
                      {term.example && (
                        <div>
                          <h4 className="text-sm font-semibold text-white mb-2 flex items-center gap-2">
                            <Star size={16} className="text-amber-400" />
                            Example
                          </h4>
                          <div className="p-3 bg-black/40 border border-white/5 rounded-lg">
                            <p className="text-slate-300 italic">
                              "{term.example}"
                            </p>
                          </div>
                        </div>
                      )}

                      {term.related && term.related.length > 0 && (
                        <div>
                          <h4 className="text-sm font-semibold text-white mb-2">
                            Related Terms
                          </h4>
                          <div className="flex flex-wrap gap-2">
                            {term.related.map((related, i) => (
                              <button
                                key={i}
                                onClick={() => setSearchTerm(related)}
                                className="text-xs px-3 py-1 bg-purple-500/10 border border-purple-500/20 text-purple-300 rounded-full hover:bg-purple-500/20 transition-colors"
                              >
                                {related}
                              </button>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </GlassCard>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
