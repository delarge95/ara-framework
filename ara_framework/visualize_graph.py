"""
Visualización del Grafo de LangGraph - ARA Framework

Este script genera representaciones visuales del grafo de investigación:
- Diagrama Mermaid (formato Markdown)
- Diagrama ASCII
- Diagrama interactivo (PNG/SVG si graphviz está instalado)
- Información detallada de nodos y edges

Uso:
    python visualize_graph.py
    python visualize_graph.py --format mermaid
    python visualize_graph.py --format ascii
    python visualize_graph.py --format png --output graph.png
"""

import argparse

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.tree import Tree
    from rich.markdown import Markdown
    console = Console()
except ImportError:
    # Fallback simple sin rich
    console = None
    class Panel:
        def __init__(self, *args, **kwargs): pass
    class Table:
        def __init__(self, *args, **kwargs): pass
        def add_column(self, *args, **kwargs): pass
        def add_row(self, *args, **kwargs): pass
    class Tree:
        def __init__(self, *args, **kwargs): pass
        def add(self, *args, **kwargs): return self
    class Markdown:
        def __init__(self, *args, **kwargs): pass


def generate_mermaid_diagram() -> str:
    """
    Genera un diagrama Mermaid del grafo.
    
    Mermaid es un lenguaje de diagramas que GitHub, Notion, etc. pueden renderizar.
    """
    mermaid = """```mermaid
graph TD
    START([START]) --> NicheAnalyst[Niche Analyst]
    NicheAnalyst --> LiteratureResearcher[Literature Researcher]
    LiteratureResearcher --> TechnicalArchitect[Technical Architect]
    TechnicalArchitect --> ImplementationSpecialist[Implementation Specialist]
    ImplementationSpecialist --> ContentSynthesizer[Content Synthesizer]
    ContentSynthesizer --> END([END])
    
    style START fill:#90EE90
    style END fill:#FFB6C1
    style NicheAnalyst fill:#87CEEB
    style LiteratureResearcher fill:#DDA0DD
    style TechnicalArchitect fill:#F0E68C
    style ImplementationSpecialist fill:#FFD700
    style ContentSynthesizer fill:#FFA07A
    
    NicheAnalyst -.->|Tools| T1[scraping_tool<br/>search_tool]
    LiteratureResearcher -.->|Tools| T2[search_tool<br/>pdf_tool<br/>database_tool]
    TechnicalArchitect -.->|Tools| T3[scraping_tool<br/>pdf_tool<br/>database_tool]
    ImplementationSpecialist -.->|Tools| T4[scraping_tool<br/>database_tool]
    ContentSynthesizer -.->|Tools| T5[database_tool]
    
    style T1 fill:#E6E6FA
    style T2 fill:#E6E6FA
    style T3 fill:#E6E6FA
    style T4 fill:#E6E6FA
    style T5 fill:#E6E6FA
```"""
    return mermaid


def generate_ascii_diagram() -> str:
    """
    Genera un diagrama ASCII del flujo del grafo.
    """
    return r"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    ARA FRAMEWORK - LANGGRAPH PIPELINE                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

                                   [START]
                                      │
                                      ▼
                    ┌─────────────────────────────────────┐
                    │      1. NICHE ANALYST 🔍           │
                    │                                     │
                    │  • Analyze market viability         │
                    │  • Search academic papers           │
                    │  • Scrape GitHub/Reddit/Blogs       │
                    │  • Identify trends & gaps           │
                    │                                     │
                    │  Tools: scraping_tool, search_tool  │
                    │  Duration: ~7-8 min                 │
                    │  LLM: Groq LLaMA 3.3-70B           │
                    └─────────────────────────────────────┘
                                      │
                                      │ niche_analysis
                                      ▼
                    ┌─────────────────────────────────────┐
                    │   2. LITERATURE RESEARCHER 📚       │
                    │                                     │
                    │  • Search 100-200 papers            │
                    │  • Deep analysis of top 20          │
                    │  • Extract methodologies            │
                    │  • Identify research gaps           │
                    │                                     │
                    │  Tools: search, pdf, database       │
                    │  Duration: ~20-25 min               │
                    │  LLM: Groq LLaMA 3.3-70B           │
                    └─────────────────────────────────────┘
                                      │
                                      │ literature_review
                                      ▼
                    ┌─────────────────────────────────────┐
                    │   3. TECHNICAL ARCHITECT 🏗️         │
                    │                                     │
                    │  • Design system architecture       │
                    │  • Select tech stack                │
                    │  • Define design patterns           │
                    │  • Address scalability/security     │
                    │                                     │
                    │  Tools: scraping, pdf, database     │
                    │  Duration: ~10-12 min               │
                    │  LLM: Groq LLaMA 3.3-70B           │
                    └─────────────────────────────────────┘
                                      │
                                      │ technical_architecture
                                      ▼
                    ┌─────────────────────────────────────┐
                    │  4. IMPLEMENTATION SPECIALIST 📋    │
                    │                                     │
                    │  • Break down into tasks            │
                    │  • Create sprint plans              │
                    │  • Estimate timeline/effort         │
                    │  • Identify risks                   │
                    │                                     │
                    │  Tools: scraping, database          │
                    │  Duration: ~7-8 min                 │
                    │  LLM: Groq LLaMA 3.3-70B           │
                    └─────────────────────────────────────┘
                                      │
                                      │ implementation_plan
                                      ▼
                    ┌─────────────────────────────────────┐
                    │   5. CONTENT SYNTHESIZER ✍️         │
                    │                                     │
                    │  • Integrate all outputs            │
                    │  • Create executive summary         │
                    │  • Format final report              │
                    │  • Generate TOC & references        │
                    │                                     │
                    │  Tools: database                    │
                    │  Duration: ~15-18 min               │
                    │  LLM: Groq LLaMA 3.3-70B           │
                    └─────────────────────────────────────┘
                                      │
                                      │ final_report
                                      ▼
                                    [END]

╔══════════════════════════════════════════════════════════════════════════════╗
║  TOTAL DURATION: ~60-75 minutes                                              ║
║  TOTAL COST: $0.10-0.20 per analysis (mostly API rate limits, Groq is free) ║
║  CHECKPOINTING: Enabled (can pause/resume at any node)                       ║
║  ERROR HANDLING: Retry logic with max 3 attempts per node                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""


def generate_detailed_info() -> Table:
    """
    Genera una tabla detallada con información de cada nodo.
    """
    table = Table(title="📊 Nodos del Grafo - Detalles", show_header=True, header_style="bold magenta")
    
    table.add_column("Nodo", style="cyan", width=20)
    table.add_column("Responsabilidad", style="white", width=40)
    table.add_column("Herramientas", style="yellow", width=20)
    table.add_column("Duración", style="green", width=12)
    
    nodes_info = [
        (
            "1. Niche Analyst",
            "Analiza viabilidad del nicho, busca papers académicos, scrapea comunidades, identifica tendencias",
            "scraping_tool\nsearch_tool",
            "~7-8 min"
        ),
        (
            "2. Literature Researcher",
            "Revisa 100-200 papers, análisis profundo de top 20, extrae metodologías, identifica gaps",
            "search_tool\npdf_tool\ndatabase_tool",
            "~20-25 min"
        ),
        (
            "3. Technical Architect",
            "Diseña arquitectura del sistema, selecciona stack tecnológico, define patrones de diseño",
            "scraping_tool\npdf_tool\ndatabase_tool",
            "~10-12 min"
        ),
        (
            "4. Implementation Specialist",
            "Crea roadmap detallado, divide en tareas, estima esfuerzo, identifica riesgos",
            "scraping_tool\ndatabase_tool",
            "~7-8 min"
        ),
        (
            "5. Content Synthesizer",
            "Integra todos los outputs, crea reporte final, genera executive summary y referencias",
            "database_tool",
            "~15-18 min"
        ),
    ]
    
    for node_name, responsibility, tools, duration in nodes_info:
        table.add_row(node_name, responsibility, tools, duration)
    
    return table


def generate_state_flow() -> Tree:
    """
    Genera un árbol que muestra el flujo de datos en el estado.
    """
    tree = Tree("🔄 [bold cyan]Flujo de Estado (ResearchState)[/bold cyan]")
    
    # Input
    input_branch = tree.add("📥 [yellow]INPUT[/yellow]")
    input_branch.add("niche: str [dim](tema de investigación)[/dim]")
    
    # Agent Outputs
    outputs_branch = tree.add("📤 [yellow]OUTPUTS DE AGENTES[/yellow]")
    outputs_branch.add("1️⃣ niche_analysis → [cyan]Análisis de viabilidad[/cyan]")
    outputs_branch.add("2️⃣ literature_review → [cyan]Revisión de literatura[/cyan]")
    outputs_branch.add("3️⃣ technical_architecture → [cyan]Arquitectura técnica[/cyan]")
    outputs_branch.add("4️⃣ implementation_plan → [cyan]Plan de implementación[/cyan]")
    outputs_branch.add("5️⃣ final_report → [cyan]Reporte final[/cyan]")
    
    # Messages (accumulator)
    messages_branch = tree.add("💬 [yellow]MENSAJES (acumulador)[/yellow]")
    messages_branch.add("messages: List[BaseMessage]")
    messages_branch.add("└─ SystemMessage, HumanMessage, AIMessage, ToolMessage")
    
    # Metadata
    metadata_branch = tree.add("📊 [yellow]METADATA[/yellow]")
    metadata_branch.add("current_agent: str")
    metadata_branch.add("agent_history: List[str]")
    metadata_branch.add("start_time: str")
    metadata_branch.add("end_time: Optional[str]")
    
    # Error Handling
    errors_branch = tree.add("⚠️ [yellow]MANEJO DE ERRORES[/yellow]")
    errors_branch.add("errors: List[str]")
    errors_branch.add("warnings: List[str]")
    errors_branch.add("retry_count: Dict[str, int]")
    
    # Budget
    budget_branch = tree.add("💰 [yellow]PRESUPUESTO[/yellow]")
    budget_branch.add("total_credits_used: float")
    budget_branch.add("budget_limit: float")
    budget_branch.add("budget_exceeded: bool")
    
    return tree


def generate_features_panel() -> Panel:
    """
    Genera un panel con las características de LangGraph.
    """
    features = """
## 🚀 Características Clave de LangGraph

### 1. **Checkpointing** ⏸️
- Pausa y reanuda workflows en cualquier nodo
- Estado persistente en memoria o Redis
- Perfecto para análisis largos (60-75 min)

### 2. **Control Explícito** 🎛️
- Flujo de grafo definido explícitamente
- Fácil agregar condicionales y loops
- Mejor debugging que pipelines implícitos

### 3. **Error Handling** 🛡️
- Retry logic integrado (máx 3 intentos)
- Tracking de errores por nodo
- Recuperación automática de fallos

### 4. **Observabilidad** 👁️
- Integración con LangSmith
- Logs estructurados con structlog
- Tracking de herramientas usadas

### 5. **Escalabilidad** 📈
- Usado por Uber, LinkedIn, Replit, Elastic
- Soporte para ejecución paralela de nodos
- Ready para producción

### 6. **Compatibilidad** 🔗
- 100% compatible con herramientas LangChain
- Fácil migración desde CrewAI
- Soporta múltiples LLMs (Groq, OpenAI, Anthropic, etc.)
"""
    return Panel(Markdown(features), title="✨ Features", border_style="green")


def try_generate_graphviz() -> bool:
    """
    Intenta generar visualización con graphviz (requiere instalación).
    """
    print("\n⚠️  Para generar imágenes PNG, necesitas instalar:")
    print("    pip install pygraphviz pillow")
    print("    Y luego ejecutar el grafo directamente desde Python\n")
    return False


def main():
    parser = argparse.ArgumentParser(
        description="Visualiza el grafo de LangGraph del ARA Framework"
    )
    parser.add_argument(
        "--format",
        choices=["all", "ascii", "mermaid", "table", "tree", "png"],
        default="all",
        help="Formato de visualización"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Archivo de salida (solo para formato PNG)"
    )
    
    args = parser.parse_args()
    
    if console:
        console.print("\n[bold cyan]🔍 Visualizando grafo de investigación...[/bold cyan]\n")
    else:
        print("\n🔍 Visualizando grafo de investigación...\n")
    
    # Mostrar visualizaciones según el formato
    if args.format in ["all", "ascii"]:
        if console:
            console.print(Panel(generate_ascii_diagram(), title="📊 Diagrama ASCII", border_style="cyan"))
        else:
            print("\n" + "="*80)
            print("📊 Diagrama ASCII")
            print("="*80)
            print(generate_ascii_diagram())
    
    if args.format in ["all", "mermaid"]:
        if console:
            console.print(Panel(generate_mermaid_diagram(), title="🎨 Diagrama Mermaid", border_style="magenta"))
            console.print("\n[dim]💡 Copia el código Mermaid arriba y pégalo en GitHub, Notion o https://mermaid.live[/dim]\n")
        else:
            print("\n" + "="*80)
            print("🎨 Diagrama Mermaid")
            print("="*80)
            print(generate_mermaid_diagram())
            print("\n💡 Copia el código Mermaid arriba y pégalo en GitHub, Notion o https://mermaid.live\n")
    
    if args.format in ["all", "table"]:
        table = generate_detailed_info()
        if console:
            console.print("\n")
            console.print(table)
            console.print("\n")
        else:
            print("\n📊 Nodos del Grafo - Detalles\n")
            print("="*80)
            print("Ver tabla en modo rich (instala: pip install rich)")
    
    if args.format in ["all", "tree"]:
        tree = generate_state_flow()
        if console:
            console.print("\n")
            console.print(tree)
            console.print("\n")
        else:
            print("\n🔄 Flujo de Estado (ResearchState)\n")
            print("="*80)
            print("Ver árbol en modo rich (instala: pip install rich)")
    
    if args.format in ["all"]:
        features_panel = generate_features_panel()
        if console:
            console.print(features_panel)
        else:
            print("\n✨ Features\n")
            print("="*80)
            print("Ver panel en modo rich (instala: pip install rich)")
    
    if args.format == "png":
        success = try_generate_graphviz()
        if not success and args.format == "png":
            if console:
                console.print("\n[yellow]Mostrando formato ASCII como alternativa:[/yellow]\n")
                console.print(Panel(generate_ascii_diagram(), title="📊 Diagrama ASCII", border_style="cyan"))
            else:
                print("\nMostrando formato ASCII como alternativa:\n")
                print(generate_ascii_diagram())
    
    # Información adicional
    if console:
        console.print("\n[bold green]✨ Información del Grafo[/bold green]")
        console.print(f"   • Nodos: [cyan]5 agentes[/cyan]")
        console.print(f"   • Edges: [cyan]5 secuenciales[/cyan]")
        console.print(f"   • Duración total: [cyan]~60-75 minutos[/cyan]")
        console.print(f"   • Costo por análisis: [cyan]$0.10-0.20[/cyan]")
        console.print(f"   • LLM: [cyan]Groq LLaMA 3.3-70B (GRATIS)[/cyan]")
        console.print(f"   • Checkpointing: [cyan]Soportado[/cyan]")
        console.print(f"   • Retry logic: [cyan]Máx 3 intentos por nodo[/cyan]\n")
    else:
        print("\n✨ Información del Grafo")
        print("   • Nodos: 5 agentes")
        print("   • Edges: 5 secuenciales")
        print("   • Duración total: ~60-75 minutos")
        print("   • Costo por análisis: $0.10-0.20")
        print("   • LLM: Groq LLaMA 3.3-70B (GRATIS)")
        print("   • Checkpointing: Soportado")
        print("   • Retry logic: Máx 3 intentos por nodo\n")
    
    # Ejemplo de uso
    example_code = """
🚀 Ejemplo de Uso:

# Ejecutar el pipeline completo
from graphs.research_graph import run_research_pipeline

result = await run_research_pipeline(
    niche="Rust WebAssembly for real-time audio processing",
    budget_limit=10.0,
)

print(result["final_report"])

# O usar el grafo directamente
from graphs.research_graph import create_research_graph

graph = create_research_graph()
result = await graph.ainvoke({
    "niche": "Tu tema de investigación",
    "messages": [],
})

print(result["final_report"])
"""
    
    if console:
        console.print(Panel(example_code, title="📖 Cómo Usar", border_style="blue"))
        console.print("\n[bold green]✅ Visualización completada[/bold green]\n")
    else:
        print("\n" + "="*80)
        print("📖 Cómo Usar")
        print("="*80)
        print(example_code)
        print("\n✅ Visualización completada\n")


if __name__ == "__main__":
    main()
