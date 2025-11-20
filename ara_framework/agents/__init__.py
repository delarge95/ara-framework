"""
Agents Layer - CrewAI specialized agents for analysis pipeline.

Este módulo exporta 6 agentes especializados que forman el pipeline de análisis:

1. **NicheAnalyst** (7-8 min, 0 créditos):
   - Analiza viabilidad del niche
   - Identifica tendencias y sub-niches
   - Scraping de GitHub, Reddit, papers recientes

2. **LiteratureResearcher** (20-25 min, ~0.15-1.5 créditos):
   - Búsqueda de 100-200 papers académicos
   - Análisis profundo de top 20 papers
   - Identificación de trends y gaps
   - BOTTLENECK: Semantic Scholar 1 req/sec

3. **TechnicalArchitect** (10-12 min, ~1 crédito):
   - Diseño de arquitectura técnica
   - Stack tecnológico completo
   - Patrones de diseño y seguridad
   - Diagramas de componentes

4. **ImplementationSpecialist** (7-8 min, ~0.33 créditos):
   - Plan de implementación detallado
   - User stories y cronograma
   - Identificación de librerías específicas
   - Setup instructions

5. **ContentSynthesizer** (9-10 min, ~0.5 créditos):
   - Síntesis de todos los outputs anteriores
   - Executive summary impactante
   - Reporte completo (~10k-15k palabras)
   - 12 secciones estructuradas

6. **Orchestrator** (5-7 min coordinación, ~1 crédito):
   - Coordina ejecución secuencial
   - Validación de outputs intermedios
   - Error handling y retries
   - Budget tracking y telemetry
   - Guardado en Supabase

**Total Pipeline**: ~57-70 minutos, ~3-5 créditos

Usage:
    ```python
    from agents import (
        create_niche_analyst,
        create_literature_researcher,
        create_technical_architect,
        create_implementation_specialist,
        create_content_synthesizer,
        create_orchestrator,
    )
    
    # Crear agentes para un niche
    niche = "Rust WASM for real-time audio processing"
    
    niche_agent, niche_task = create_niche_analyst(niche)
    lit_agent, lit_task = create_literature_researcher(niche, [niche_task])
    arch_agent, arch_task = create_technical_architect(niche, [niche_task, lit_task])
    impl_agent, impl_task = create_implementation_specialist(niche, arch_task)
    synth_agent, synth_task = create_content_synthesizer(niche, [niche_task, lit_task, arch_task, impl_task])
    
    # Crear crew
    # CrewAI removed - using LangGraph only
    
    crew = Crew(
        agents=[niche_agent, lit_agent, arch_agent, impl_agent, synth_agent],
        tasks=[niche_task, lit_task, arch_task, impl_task, synth_task],
        # StateGraph sequential execution
        verbose=True,
        memory=True,
    )
    
    # Ejecutar
    result = await graph.ainvoke({"niche": niche})
    ```

Fuente: docs/04_ARCHITECTURE.md (Agents Layer), docs/03_AI_MODELS.md
"""
from agents.niche_analyst import (
    create_niche_analyst_agent,
    create_niche_analysis_task,
    create_niche_analyst,
)

from agents.literature_researcher import (
    create_literature_researcher_agent,
    create_literature_research_task,
    create_literature_researcher,
)

from agents.technical_architect import (
    create_technical_architect_agent,
    create_technical_architecture_task,
    create_technical_architect,
)

from agents.implementation_specialist import (
    create_implementation_specialist_agent,
    create_implementation_plan_task,
    create_implementation_specialist,
)

from agents.content_synthesizer import (
    create_content_synthesizer_agent,
    create_synthesis_task,
    create_content_synthesizer,
)

from agents.orchestrator import (
    create_orchestrator_agent,
    create_orchestration_task,
    create_orchestrator,
)


__all__ = [
    # Main helpers (recomendados)
    "create_niche_analyst",
    "create_literature_researcher",
    "create_technical_architect",
    "create_implementation_specialist",
    "create_content_synthesizer",
    "create_orchestrator",
    
    # Agent creators (si necesitas solo el agent)
    "create_niche_analyst_agent",
    "create_literature_researcher_agent",
    "create_technical_architect_agent",
    "create_implementation_specialist_agent",
    "create_content_synthesizer_agent",
    "create_orchestrator_agent",
    
    # Task creators (si necesitas solo la task)
    "create_niche_analysis_task",
    "create_literature_research_task",
    "create_technical_architecture_task",
    "create_implementation_plan_task",
    "create_synthesis_task",
    "create_orchestration_task",
]
