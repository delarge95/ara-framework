"""
LiteratureResearcher Agent - Deep academic literature analysis.

Este agente:
1. Recibe keywords del NicheAnalyst
2. Realiza búsqueda profunda en Semantic Scholar (100-200 papers)
3. Descarga y procesa PDFs de papers críticos (20-30 PDFs)
4. Analiza citaciones, trends, y metodologías
5. Identifica gaps en la investigación actual
6. Guarda papers en base de datos para referencia futura

Modelos:
- Primary: GPT-5 (1 crédito, mejor comprensión de papers académicos)
- Fallback: Claude Haiku 4.5 (0.33 créditos, rápido y barato)

SLA: 20-25 minutos (BOTTLENECK debido a rate limit de Semantic Scholar 1 req/seg)
Budget: ~0.15 créditos con cache hits, ~1.5 sin cache

OPTIMIZACIÓN CRÍTICA:
- Usa search_papers_parallel con offsets para mitigar bottleneck
- Cache agresivo (7 días) en Redis para papers
- Prioriza papers con >10 citaciones y año >2020

Tools: search_tool (todos: 5 tools), pdf_tool (4 tools), database_tool (3 tools)

Output: Base de conocimiento con 50-100 papers procesados, análisis de trends

Fuente: docs/03_AI_MODELS.md (Agent 2), docs/04_ARCHITECTURE.md (Agents Layer)
"""
import structlog
# from crewai import Agent, Task  # CrewAI removed - using LangGraph only
from typing import Dict, Any, Optional

from config.settings import settings
from tools import get_search_tool, get_pdf_tool, get_database_tool

logger = structlog.get_logger()


def create_literature_researcher_agent() -> Agent:
    """
    Crea el agente LiteratureResearcher.
    
    Este agente es el más intensivo en tiempo debido al rate limit
    de Semantic Scholar (1 req/seg). Usa búsqueda paralela para mitigar.
    
    Returns:
        Agent: Instancia configurada del LiteratureResearcher
    """
    # Obtener tools
    search_tool = get_search_tool()
    pdf_tool = get_pdf_tool()
    database_tool = get_database_tool()
    
    # Configurar LLM (Groq - LLaMA 3.3-70B GRATIS)
    llm_model = "groq/llama-3.3-70b-versatile"
    
    agent = Agent(
        role="Academic Literature Researcher",
        
        goal="""Realizar investigación profunda en literatura académica sobre '{niche}':
        1. Búsqueda exhaustiva en Semantic Scholar (100-200 papers)
        2. Análisis de citaciones y trends (papers más influyentes)
        3. Descarga y procesamiento de PDFs críticos (20-30 papers)
        4. Identificación de metodologías comunes y gaps
        5. Construcción de knowledge base persistente en Supabase
        6. Generación de insights accionables para arquitectura técnica
        """,
        
        backstory="""Eres un investigador académico PhD en Computer Science con 15 años de experiencia.
        
        Tu expertise incluye:
        - Búsqueda sistemática en bases académicas (Semantic Scholar, arXiv)
        - Análisis de citaciones y redes de papers (bibliometría)
        - Lectura rápida de papers: Abstract → Introduction → Conclusion → Methods
        - Identificación de metodologías reproducibles vs experimentales
        - Detección de trends emergentes antes de que sean mainstream
        - Evaluación crítica de calidad de investigación (venue, citaciones, reproducibilidad)
        
        Tu proceso de trabajo:
        1. **Búsqueda Estratégica**: Empiezas con keywords broad, luego refinas
        2. **Filtrado Inteligente**: Priorizas papers con >10 citaciones, venues top-tier
        3. **Análisis en Profundidad**: Lees 20-30 papers críticos (no solo abstracts)
        4. **Síntesis**: Identificas patterns, metodologías comunes, y gaps
        5. **Persistencia**: Guardas TODOS los papers en base de datos para futura referencia
        
        OPTIMIZACIONES CRÍTICAS (para cumplir SLA de 25 minutos):
        - Usa search_papers_parallel con 5 offsets simultáneos (mitiga bottleneck de 1 req/seg)
        - Cache hits = 7 días en Redis (si el niche ya fue analizado, retorna cache)
        - Descarga PDFs solo de top 20-30 papers (no los 200)
        - Extrae solo Abstract + Introduction + Methods de PDFs (skip Results/Discussion)
        
        MANEJO DE RATE LIMITS:
        - Semantic Scholar: 1 req/seg (CRÍTICO) → Usa parallel search con offsets
        - Si hit rate limit 429: espera 60 segundos automáticamente (circuit breaker)
        - PDFs: 5 conversions/min (MarkItDown) → Procesa en batches de 5
        
        IMPORTANTE:
        - NO uses search_academic_papers básico (toma 200 segundos para 200 papers)
        - USA search_papers_parallel (toma 40-50 segundos para 200 papers)
        - Guarda papers en DB ANTES de descargar PDFs (para reanudar si falla)
        """,
        
        tools=[
            # Academic search (BOTTLENECK - 1 req/seg)
            search_tool.search_academic_papers,  # Búsqueda básica
            search_tool.search_papers_parallel,  # USAR ESTO (parallel con offsets)
            search_tool.get_paper_details,       # Detalles de paper específico
            search_tool.get_related_papers,      # Recommendations/citations
            search_tool.search_recent_papers,    # Papers recientes sorted by citations
            
            # PDF processing (5 conversions/min)
            pdf_tool.convert_pdf_to_markdown,    # Conversión completa
            pdf_tool.extract_pdf_sections,       # Solo secciones específicas
            pdf_tool.extract_pdf_text_only,      # Solo texto (para búsquedas)
            pdf_tool.convert_multiple_pdfs,      # Batch conversion
            
            # Database persistence
            database_tool.save_paper,            # Guardar paper individual
            database_tool.query_papers,          # Buscar papers guardados
            database_tool.get_paper_by_id,       # Retrieve by Semantic Scholar ID
        ],
        
        llm=llm_model,
        
        verbose=True,
        memory=True,
        allow_delegation=False,
        max_iter=30,  # Más iteraciones (proceso largo)
        max_rpm=60,   # GPT-5 via Copilot no tiene rate limit estricto
    )
    
    logger.info(
        "literature_researcher_created",
        model="gpt-5",
        fallback="claude-haiku-4.5",
        tools_count=12,
        estimated_duration="20-25 minutes",
        bottleneck="semantic_scholar_rate_limit",
    )
    
    return agent


def create_literature_research_task(
    agent: Agent, 
    niche: str,
    niche_analysis_context: Optional[Task] = None
) -> Task:
    """
    Crea la tarea de investigación literaria.
    
    Args:
        agent: Instancia del LiteratureResearcher
        niche: Nombre del niche
        niche_analysis_context: Task del NicheAnalyst (para recibir keywords)
    
    Returns:
        Task: Tarea configurada con descripción y output esperado
    """
    task = Task(
        description="""
        Realiza investigación profunda en literatura académica sobre "__NICHE__".
        
        Recibes del NicheAnalyst:
        - Keywords principales (5-7)
        - Keywords secundarias (5-8)
        - Sub-niches sugeridos (2-3)
        - Queries optimizadas para Semantic Scholar
        
        **FASE 1: Búsqueda Exhaustiva (8-10 minutos)**
        
        PASO 1.1: Búsqueda Paralela Inicial (3-4 min)
        - USA search_papers_parallel() con keywords principales
        - Busca 200 papers en total (5 queries paralelas × 40 papers cada una)
        - Offsets: [0, 40, 80, 120, 160] → Total 200 papers en ~40 segundos
        - Filtra por: year >= 2020, citations >= 10
        
        PASO 1.2: Análisis de Papers Top (2-3 min)
        - Ordena los 200 papers por citaciones (descendente)
        - Identifica los Top 50 papers más citados
        - Para cada uno: analiza Abstract (ya incluido en response)
        - Categoriza por subtemas usando keywords
        
        PASO 1.3: Expansión con Related Papers (3 min)
        - Selecciona Top 5 papers más citados
        - Para cada uno: get_related_papers() → 10 recommendations
        - Agrega papers únicos (sin duplicados) → +30-40 papers
        - Total: ~200-240 papers identificados
        
        PASO 1.4: Persistencia en Base de Datos (2 min)
        - Guarda TODOS los papers en Supabase usando save_paper()
        - Batch insert (no uno por uno) para eficiencia
        - Esto permite:
          a) Consultas futuras sin re-scrapear Semantic Scholar
          b) Análisis de trends a lo largo del tiempo
          c) Compartir knowledge base entre análisis
        
        **FASE 2: Análisis en Profundidad (10-12 minutos)**
        
        PASO 2.1: Selección de Papers Críticos (1 min)
        - De los 200-240 papers, selecciona Top 25 para lectura profunda
        - Criterios:
          a) Citaciones > 20 (papers influyentes)
          b) Año 2022-2024 (investigación reciente)
          c) Venues top: ACL, NeurIPS, ICML, CVPR, ICLR, etc.
          d) Diversidad: cubrir todos los subtemas identificados
        
        PASO 2.2: Descarga y Procesamiento de PDFs (8-10 min)
        - Descarga PDFs de los 25 papers seleccionados
        - USA convert_multiple_pdfs() con max_concurrent=5 (respeta rate limit)
        - Si PDF no disponible: usa extract_pdf_text_only() como fallback
        - Extrae SOLO: Abstract, Introduction, Methods, Conclusion
        - Skip: Results, Discussion, References (ahorran tiempo)
        - Batch de 5 papers × 5 batches = 25 papers en ~10 min
        
        PASO 2.3: Análisis de Metodologías (1 min)
        - Identifica metodologías comunes en los 25 papers
        - Categoriza: experimental, theoretical, survey, implementation
        - ¿Qué datasets usan? ¿Qué benchmarks?
        - ¿Qué métricas de evaluación?
        
        **FASE 3: Síntesis y Gaps (2-3 minutos)**
        
        PASO 3.1: Análisis de Trends (1 min)
        - Compara papers 2020-2021 vs 2022-2024
        - ¿Qué ha cambiado? ¿Qué está emergiendo?
        - ¿Hay shifts en paradigmas? (ej: de RNNs a Transformers)
        
        PASO 3.2: Identificación de Gaps (1 min)
        - ¿Qué problemas están sin resolver?
        - ¿Qué áreas tienen pocos papers (<5)?
        - ¿Hay discrepancias entre papers? (findings contradictorios)
        - ¿Qué intersecciones no se han explorado?
        
        PASO 3.3: Generación de Insights (1 min)
        - 3-5 insights clave para TechnicalArchitect
        - Recomendaciones de arquitecturas técnicas basadas en papers
        - Tecnologías/frameworks mencionados frecuentemente
        - Datasets públicos disponibles para experimentación
        
        **MANEJO DE ERRORES Y OPTIMIZACIONES**:
        - Si Semantic Scholar retorna 429 (rate limit): espera 60 seg automáticamente
        - Si PDF download falla: continúa con los demás (no bloqueante)
        - Si cache hit en Redis: skip búsqueda (retorna papers guardados)
        - Si ya hay papers en DB para este niche: complementa (no duplica)
        
        **OUTPUTS INTERMEDIOS** (para logs):
        - Después de FASE 1: "Encontrados X papers, Top 10: [títulos]"
        - Después de FASE 2: "Procesados Y PDFs, Z fallaron"
        - Después de FASE 3: "Identificados N gaps, M trends"
    """.replace("__NICHE__", niche),

    expected_output="""
    # Investigación Literaria: __NICHE__
        
        ## 1. Resumen Ejecutivo (3-4 párrafos)
        - ¿Qué encontramos? (hallazgos principales en 2-3 oraciones)
        - ¿Cuál es el estado del arte actual? (descripción general)
        - ¿Qué gaps son más prometedores? (2-3 oportunidades clave)
        - Conclusión: ¿Hay suficiente investigación para continuar? (SÍ/NO + justificación)
        
        ## 2. Estadísticas de Búsqueda
        - **Papers encontrados**: X papers (total en Semantic Scholar)
        - **Papers analizados**: Y papers (después de filtros)
        - **Papers guardados en DB**: Z papers (persistidos en Supabase)
        - **PDFs procesados**: W papers (lectura profunda)
        - **Tiempo total**: XX minutos YY segundos
        - **Cache hits**: N queries (si aplica)
        
        ## 3. Papers Más Influyentes (Top 10)
        Para cada paper:
        ### Paper 1: [Título]
        - **Autores**: [nombres]
        - **Año**: YYYY
        - **Venue**: [conferencia/journal]
        - **Citaciones**: XXX
        - **Semantic Scholar ID**: [id para referencia]
        - **Insight clave** (1-2 líneas): [qué aporta este paper]
        - **Metodología**: [experimental/theoretical/survey/implementation]
        - **URL**: [link a paper]
        
        [Repetir para Top 10]
        
        ## 4. Análisis por Subtemas
        ### Subtema 1: [Nombre]
        - **Papers encontrados**: X papers
        - **Trend**: ⬆️ Creciendo | ➡️ Estable | ⬇️ Declinando
        - **Papers clave**: [3-5 papers más citados]
        - **Metodologías comunes**: [lista]
        - **Gaps identificados**: [2-3 problemas sin resolver]
        
        ### Subtema 2: [Nombre]
        [Misma estructura]
        
        ### Subtema 3: [Nombre]
        [Misma estructura]
        
        ## 5. Metodologías y Tecnologías
        ### Metodologías Comunes (3-5)
        1. **[Metodología 1]**: Usada en X papers
           - Descripción: [2-3 líneas]
           - Papers representativos: [links]
           - Limitaciones conocidas: [1-2 líneas]
        
        ### Tecnologías/Frameworks Frecuentes
        - **[Tech 1]**: Mencionada en X papers (ej: PyTorch, TensorFlow)
        - **[Tech 2]**: Mencionada en Y papers
        - **[Tech 3]**: Mencionada en Z papers
        
        ### Datasets Públicos Disponibles
        - **[Dataset 1]**: [Descripción 1 línea] | Usado en X papers | [Link]
        - **[Dataset 2]**: [Descripción 1 línea] | Usado en Y papers | [Link]
        
        ### Benchmarks Estándar
        - **[Benchmark 1]**: [Métrica] | Usado en X papers
        - **[Benchmark 2]**: [Métrica] | Usado en Y papers
        
        ## 6. Análisis Temporal de Trends
        ### Evolución 2020-2024
        - **2020-2021**: [Qué se investigaba] | X papers
        - **2022-2023**: [Shift en enfoque] | Y papers
        - **2024**: [Estado actual] | Z papers
        
        ### Trends Emergentes (3-5)
        1. **[Trend 1]**: [Descripción 2-3 líneas]
           - Evidencia: X papers en últimos 6 meses
           - Papers clave: [links]
           - Predicción: [hacia dónde va]
        
        2. **[Trend 2]**: [Descripción 2-3 líneas]
           [Misma estructura]
        
        ## 7. Gaps en la Investigación (CRÍTICO para arquitectura)
        ### Gap 1: [Nombre del Gap]
        - **Descripción**: [3-4 líneas: qué falta, por qué importa]
        - **Evidencia**: Solo X papers abordan esto (vs Y esperados)
        - **Oportunidad**: [Cómo se podría resolver]
        - **Complejidad**: Baja | Media | Alta
        - **Impacto potencial**: Bajo | Medio | Alto
        
        ### Gap 2: [Nombre del Gap]
        [Misma estructura]
        
        ### Gap 3: [Nombre del Gap]
        [Misma estructura]
        
        ## 8. Discrepancias y Controversias
        - ¿Hay findings contradictorios? (Paper A dice X, Paper B dice Y)
        - ¿Hay debates abiertos en la comunidad?
        - ¿Qué metodologías están siendo cuestionadas?
        
        ## 9. Recomendaciones para TechnicalArchitect
        ### Arquitecturas Técnicas Sugeridas (basadas en papers)
        1. **[Arquitectura 1]**: [Descripción]
           - Papers que la usan: [links]
           - Ventajas: [lista]
           - Desventajas: [lista]
           - Complejidad de implementación: 1-10
        
        2. **[Arquitectura 2]**: [Descripción]
           [Misma estructura]
        
        ### Stack Tecnológico Recomendado
        - **Lenguajes**: [ej: Python, Rust] (basado en X papers)
        - **Frameworks**: [ej: PyTorch, JAX] (basado en Y papers)
        - **Infraestructura**: [ej: Docker, Kubernetes] (basado en Z papers)
        - **CI/CD**: [ej: GitHub Actions] (best practices de papers)
        
        ### Datasets para Prototipado
        - **[Dataset 1]**: [Por qué este] | [Link]
        - **[Dataset 2]**: [Por qué este] | [Link]
        
        ### Métricas de Evaluación
        - **[Métrica 1]**: [Descripción] | Usada en X papers
        - **[Métrica 2]**: [Descripción] | Usada en Y papers
        
        ## 10. Knowledge Base Construida
        - **Papers guardados en Supabase**: X papers
    - **Query para consultar**: `SELECT * FROM papers WHERE niche = '__NICHE__'`
        - **PDFs procesados disponibles**: Y archivos
        - **Secciones extraídas**: Abstract, Introduction, Methods, Conclusion
        
        ## 11. Limitaciones y Consideraciones
        - ⚠️ **Rate Limits hit**: [Si hubo problemas con Semantic Scholar]
        - ⚠️ **PDFs no disponibles**: [Lista de papers sin PDF]
        - ⚠️ **Papers paywalled**: [Papers detrás de paywall]
        - 💡 **Queries alternativas**: [Sugerencias si búsqueda fue limitada]
        - 🚫 **Red flags**: [Cualquier problema de calidad en papers]
        
        ## 12. Próximos Pasos para TechnicalArchitect
        - **Enfocar diseño en**: [Subtemas/gaps específicos]
        - **Priorizar metodologías**: [Top 2-3 metodologías]
    - **Explorar intersecciones**: [niche + tech X, niche + method Y]
    - **Validar con datasets**: [Datasets recomendados para pruebas]
    """.replace("__NICHE__", niche),
        
        agent=agent,
        
        # Recibe contexto del NicheAnalyst
        context=[niche_analysis_context] if niche_analysis_context else [],
    )
    
    logger.info(
        "literature_research_task_created",
        niche=niche,
        expected_duration="20-25 minutes",
        tools_used=["search_tool (5)", "pdf_tool (4)", "database_tool (3)"],
        bottleneck="semantic_scholar_rate_limit_1_req_per_sec",
    )
    
    return task


# Función helper
def create_literature_researcher(
    niche: str,
    niche_analysis_task: Optional[Task] = None
) -> tuple[Agent, Task]:
    """
    Helper para crear el LiteratureResearcher con su tarea.
    
    Args:
        niche: Nombre del niche a analizar
        niche_analysis_task: Task del NicheAnalyst (para recibir keywords)
    
    Returns:
        tuple[Agent, Task]: Tupla (agente, tarea)
    
    Example:
        >>> # Después de ejecutar NicheAnalyst
        >>> niche_agent, niche_task = create_niche_analyst("Rust + WebAssembly")
        >>> lit_agent, lit_task = create_literature_researcher(
        ...     "Rust + WebAssembly", 
        ...     niche_analysis_task=niche_task
        ... )
        >>> crew = Crew(
        ...     agents=[niche_agent, lit_agent],
        ...     tasks=[niche_task, lit_task],
        ...     process=Process.sequential
        ... )
        >>> result = crew.kickoff()
    """
    agent = create_literature_researcher_agent()
    task = create_literature_research_task(agent, niche, niche_analysis_task)
    return agent, task
