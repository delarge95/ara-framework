"""
NicheAnalyst Agent - First agent in the ARA pipeline.

Este agente:
1. Recibe un niche/tema de investigación
2. Identifica tendencias emergentes en el niche
3. Analiza comunidades (Reddit, GitHub, foros, blogs)
4. Evalúa viabilidad y demanda del mercado
5. Genera keywords y sub-niches para exploración profunda

Modelos:
- Primary: Gemini 2.5 Pro (free, 1500 req/día, 15 RPM)
- Fallback: MiniMax-M2 (free beta)

SLA: 7-8 minutos
Budget: 0 créditos (ambos modelos son gratuitos)

Tools: scraping_tool (scrape_website, scrape_multiple_urls), 
       search_tool (search_recent_papers)

Output: Reporte Markdown con:
- Viabilidad del niche (score 1-10)
- Tendencias identificadas (3-5)
- Comunidades activas (links + estadísticas)
- Keywords principales (10-15)
- Sub-niches sugeridos (2-3)
- Demanda estimada (score 1-10)

Fuente: docs/03_AI_MODELS.md (Agent 1), docs/04_ARCHITECTURE.md (Agents Layer)
"""
import structlog
# from crewai import Agent, Task  # CrewAI removed - using LangGraph only
from typing import Dict, Any

from config.settings import settings
from tools import get_scraping_tool, get_search_tool

logger = structlog.get_logger()


def create_niche_analyst_agent() -> Agent:
    """
    Crea el agente NicheAnalyst.
    
    Este agente es el primero en ejecutarse y su output alimenta
    a los demás agentes del pipeline.
    
    Returns:
        Agent: Instancia configurada del NicheAnalyst
    """
    # Obtener tools
    scraping_tool = get_scraping_tool()
    search_tool = get_search_tool()
    
    # Configurar LLM (Groq - LLaMA 3.3-70B GRATIS)
    llm_model = "groq/llama-3.3-70b-versatile"
    
    agent = Agent(
        role="Niche Market Analyst",
        
        goal="""Analizar la viabilidad y oportunidades del niche '{niche}' mediante:
        1. Búsqueda de papers recientes en Semantic Scholar (últimos 2 años)
        2. Scraping de comunidades activas (GitHub repos, Reddit threads, blogs)
        3. Identificación de tendencias emergentes y gaps
        4. Evaluación de demanda y competencia
        5. Generación de keywords y sub-niches para profundización
        """,
        
        backstory="""Eres un analista de mercado especializado en nichos tecnológicos emergentes.
        Tienes 10+ años de experiencia identificando oportunidades en intersecciones de tecnologías.
        
        Tu expertise incluye:
        - Análisis de trends en GitHub (stars, forks, recent activity)
        - Evaluación de comunidades en Reddit, HackerNews, dev.to
        - Identificación de papers académicos relevantes (Semantic Scholar)
        - Detección de gaps entre teoría académica y práctica industrial
        - Generación de keywords optimizadas para búsqueda profunda
        
        Tu misión es validar si el niche es viable (suficiente interés, comunidad activa,
        investigación académica, pero no oversaturado) y generar una hoja de ruta para
        los siguientes agentes.
        
        IMPORTANTE: 
        - Usa scraping_tool para buscar en GitHub, Reddit, blogs
        - Usa search_tool para encontrar papers recientes (últimos 2 años)
        - Enfócate en TENDENCIAS EMERGENTES, no en tecnologías maduras
        - Sé crítico: si el niche no es viable, indícalo claramente
        """,
        
        tools=[
            # Web scraping (10 req/min rate limit)
            scraping_tool.scrape_website,
            scraping_tool.scrape_multiple_urls,
            
            # Academic search (1 req/seg CRITICAL rate limit)
            search_tool.search_recent_papers,
        ],
        
        llm=llm_model,  # String del modelo en formato litellm
        
        verbose=True,  # Logs detallados
        memory=True,   # Recuerda contexto entre tareas
        allow_delegation=False,  # No delega a otros agentes (es el primero)
        max_iter=15,   # Máximo 15 iteraciones de tool usage
        max_rpm=15,    # Gemini free tier: 15 RPM
    )
    
    logger.info(
        "niche_analyst_created",
        model="gemini-2.5-pro",
        tools_count=3,
        max_rpm=15,
    )
    
    return agent


def create_niche_analysis_task(agent: Agent, niche: str) -> Task:
    """
    Crea la tarea de análisis de niche.
    
    Args:
        agent: Instancia del NicheAnalyst
        niche: Nombre del niche a analizar (ej: "Rust + WebAssembly")
    
    Returns:
        Task: Tarea configurada con descripción y output esperado
    """
    task = Task(
        description="""
        Analiza el niche "__NICHE__" siguiendo estos pasos:
        
        **PASO 1: Búsqueda Académica Inicial (2-3 minutos)**
    - Usa search_recent_papers("__NICHE__", limit=20, years_back=2)
        - Identifica: ¿Hay investigación activa? ¿Cuántos papers en últimos 2 años?
        - ¿Qué subtemas están en auge? (analiza títulos y abstracts)
        
        **PASO 2: Análisis de Comunidades (3-4 minutos)**
    - GitHub: Scrape "https://github.com/search?q=__NICHE__&type=repositories"
          → Identifica repos con >500 stars creados en últimos 2 años
          → Analiza activity (commits recientes, issues activos)
        
    - Reddit: Scrape "https://www.reddit.com/search/?q=__NICHE__"
          → Busca subreddits activos relacionados
          → Analiza cantidad de posts recientes
        
        - Dev.to/Medium: Scrape artículos recientes sobre el niche
          → ¿Hay hype? ¿O es un tema muerto?
        
        **PASO 3: Identificación de Trends (1-2 minutos)**
        - Compara papers académicos vs repos GitHub
        - ¿Hay gaps entre teoría y práctica?
        - ¿Qué problemas están sin resolver?
        - ¿Qué tecnologías complementarias están emergiendo?
        
        **PASO 4: Evaluación de Viabilidad (1 minuto)**
        - ¿Hay suficiente interés? (score 1-10)
        - ¿Hay demanda real? (evidencia: jobs, startups, funding)
        - ¿Está oversaturado? (demasiada competencia)
        - ¿Es tendencia pasajera o duradera?
        
        **PASO 5: Generación de Keywords y Sub-niches**
        - Keywords principales (10-15) para búsqueda profunda
        - Sub-niches específicos (2-3) para exploración
        - Queries optimizadas para Semantic Scholar
        
        IMPORTANTE:
        - Respeta rate limits: Semantic Scholar = 1 req/seg, Scraping = 10 req/min
        - Si el scraping falla (anti-bot), usa información de papers
        - Sé honesto: si el niche no es viable, di por qué
        - Prioriza CALIDAD sobre cantidad (mejor 5 insights buenos que 20 vagos)
    """.replace("__NICHE__", niche),

    expected_output="""
    # Análisis de Niche: __NICHE__
        
        ## 1. Resumen Ejecutivo (2-3 párrafos)
        - ¿Qué es este niche? (definición clara en 1-2 oraciones)
        - ¿Por qué es relevante ahora? (trends, timing)
        - Veredicto: ¿Es viable para investigación profunda? (SÍ/NO + justificación)
        
        ## 2. Viabilidad General
        - **Score de Viabilidad**: X/10 (justificar)
        - **Score de Demanda**: X/10 (evidencia: jobs, startups, repos activos)
        - **Score de Competencia**: X/10 (1=poco competido, 10=oversaturado)
        - **Tendencia**: ⬆️ Creciendo | ➡️ Estable | ⬇️ Declinando
        
        ## 3. Investigación Académica
        - **Papers encontrados**: X papers en últimos 2 años
        - **Top 3-5 papers más citados**: (título, año, citaciones, insight clave)
        - **Subtemas emergentes**: (3-5 subtemas con >3 papers cada uno)
        - **Gaps identificados**: (2-3 problemas sin resolver o poco explorados)
        
        ## 4. Comunidades y Ecosistema
        ### GitHub
        - **Repos relevantes**: (Top 3-5 con >500 stars, actividad reciente)
        - **Actividad**: (commits/mes, issues abiertos, contributors activos)
        - **Tech Stack común**: (lenguajes, frameworks más usados)
        
        ### Reddit/Foros
        - **Subreddits activos**: (nombre, subscribers, posts/mes)
        - **Discusiones recientes**: (temas hot, preguntas frecuentes)
        
        ### Blogs/Artículos
        - **Artículos técnicos**: (links a Medium, dev.to, blogs corporativos)
        - **Tutoriales**: ¿Hay contenido educativo de calidad?
        
        ## 5. Tendencias Identificadas
        1. **Trend 1**: (nombre + descripción 2-3 líneas + evidencia)
        2. **Trend 2**: (nombre + descripción 2-3 líneas + evidencia)
        3. **Trend 3**: (nombre + descripción 2-3 líneas + evidencia)
        
        ## 6. Keywords Principales (para LiteratureResearcher)
        ### Keywords Primarias (5-7):
    - "__NICHE__"
        - [keyword 2]
        - [keyword 3]
        - ...
        
        ### Keywords Secundarias (5-8):
        - [keyword combinada 1]
        - [keyword combinada 2]
        - ...
        
        ## 7. Sub-niches Sugeridos
        ### Sub-niche 1: [Nombre]
        - Descripción: [2-3 líneas]
        - Viabilidad: X/10
        - Razón: [por qué es interesante]
        
        ### Sub-niche 2: [Nombre]
        - Descripción: [2-3 líneas]
        - Viabilidad: X/10
        - Razón: [por qué es interesante]
        
        ## 8. Recomendaciones para Siguiente Agente (LiteratureResearcher)
        - **Enfocar búsqueda en**: [subtemas específicos]
        - **Priorizar papers con**: [características: citaciones, año, venues]
        - **Explorar intersecciones**: [niche + X, niche + Y]
        - **Queries Semantic Scholar sugeridas**: (3-5 queries optimizadas)
        
        ## 9. Alertas y Consideraciones
        - ⚠️ [Cualquier limitación encontrada: anti-bot, rate limits, etc.]
        - 💡 [Insights adicionales no cubiertos arriba]
        - 🚫 [Red flags si los hay: hype sin sustancia, comunidad tóxica, etc.]
    """.replace("__NICHE__", niche),
        
        agent=agent,
        
        # Este es el primer task, no tiene contexto previo
        context=[],
    )
    
    logger.info(
        "niche_analysis_task_created",
        niche=niche,
        expected_duration="7-8 minutes",
        tools_used=["scraping_tool", "search_tool"],
    )
    
    return task


# Función helper para crear agent + task juntos
def create_niche_analyst(niche: str) -> tuple[Agent, Task]:
    """
    Helper para crear el NicheAnalyst con su tarea.
    
    Args:
        niche: Nombre del niche a analizar
    
    Returns:
        tuple[Agent, Task]: Tupla (agente, tarea)
    
    Example:
        >>> agent, task = create_niche_analyst("Rust + WebAssembly")
        >>> crew = Crew(agents=[agent], tasks=[task])
        >>> result = graph.invoke()
    """
    agent = create_niche_analyst_agent()
    task = create_niche_analysis_task(agent, niche)
    return agent, task
