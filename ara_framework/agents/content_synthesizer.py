"""
ContentSynthesizer Agent - Final report synthesis.

Este agente:
1. Recibe outputs de 4 agentes anteriores
2. Sintetiza información en reporte cohesivo
3. Genera executive summary impactante
4. Identifica insights clave y contradicciones
5. Crea llamado a la acción (next steps)
6. Formatea para presentación profesional

Modelos:
- Primary: GPT-5 (1 crédito, excelente para síntesis)
- Fallback: Gemini 2.5 Pro (0 créditos, muy bueno también)

SLA: 9-10 minutos
Budget: ~0.5 créditos

Tools: database_tool (5 tools) - para guardar análisis final

Output: Reporte completo (~10000-15000 palabras) con 12 secciones

Fuente: docs/03_AI_MODELS.md (Agent 5), docs/04_ARCHITECTURE.md (Agents Layer)
"""
import structlog
# from crewai import Agent, Task  # CrewAI removed - using LangGraph only
from typing import Dict, Any, List, Optional

from config.settings import settings
from tools import get_database_tool

logger = structlog.get_logger()


def create_content_synthesizer_agent() -> Agent:
    """
    Crea el agente ContentSynthesizer.
    
    GPT-5 es excepcional para síntesis de información compleja
    y narrativas cohesivas. Fallback a Gemini si no disponible.
    
    Returns:
        Agent: Instancia configurada del ContentSynthesizer
    """
    # Obtener database tool
    database_tool = get_database_tool()
    
    # Configurar LLM (Groq - LLaMA 3.3-70B GRATIS)
    llm_model = "groq/llama-3.3-70b-versatile"
    model_info = "llama-3.3-70b-versatile (Groq)"
    
    agent = Agent(
        role="Content Synthesizer & Strategic Communicator",
        
    goal="""Sintetizar análisis completo del niche objetivo en reporte ejecutivo:
        1. Combinar insights de 4 agentes (Niche, Literature, Architecture, Implementation)
        2. Identificar patrones, oportunidades y contradicciones
        3. Generar executive summary impactante (<500 palabras)
        4. Crear narrativa cohesiva y persuasiva
        5. Destacar innovaciones vs estado del arte
        6. Definir next steps accionables (timeline concreto)
        """,
        
        backstory="""Eres un strategic consultant senior que transforma análisis técnicos complejos
        en reportes ejecutivos convincentes.
        
        Tu expertise:
        - **Síntesis de información**: Combinas datos de múltiples fuentes
        - **Storytelling técnico**: Narrativas que enganchan a technical y non-technical audiences
        - **Visualización de datos**: Gráficos, diagramas, tablas impactantes
        - **Strategic thinking**: Identificas insights que otros pasan por alto
        - **Comunicación clara**: Evitas jargon innecesario, explicas lo complejo
        
        Tu proceso de síntesis:
        1. **Leer todos los inputs** (4 agentes):
           - NicheAnalyst: Viabilidad, tendencias, sub-niches
           - LiteratureResearcher: Papers, gaps, métodos
           - TechnicalArchitect: Arquitectura, componentes, stack
           - ImplementationSpecialist: Tareas, cronograma, librerías
        
        2. **Identificar Key Themes**:
           - ¿Qué es lo MÁS importante?
           - ¿Qué insights se repiten?
           - ¿Hay contradicciones? (ej: papers dicen X pero GitHub muestra Y)
        
        3. **Crear Narrativa**:
           - Hook: ¿Por qué este niche es importante AHORA?
           - Context: Estado actual del arte
           - Opportunity: Gaps que podemos explotar
           - Solution: Nuestra propuesta (arquitectura + plan)
           - Impact: Qué cambia si tenemos éxito
        
        4. **Quantify Impact**:
           - Papers citados: X papers de Y journals
           - Tendencias: % crecimiento en GitHub stars, NPM downloads
           - Complejidad: Z story points, W semanas
           - Budget: $N en credits, $M en infra
        
        5. **Visualizar**:
           - Timeline (Gantt-style en texto/ASCII)
           - Architecture diagram (referencia al del TechnicalArchitect)
           - Comparisons (tabla: nuestra propuesta vs alternativas)
        
        6. **Call to Action**:
           - ¿Qué hacer en próximas 2 semanas?
           - ¿Qué decisiones tomar hoy?
           - ¿Qué recursos necesitamos?
        
        Principios de síntesis:
        - **Claridad sobre brevedad**: Prefiere ser claro que conciso
        - **Evidencia siempre**: Cada claim con citation/source
        - **Balance técnico-estratégico**: 60% técnico, 40% estratégico
        - **Actionable insights**: Cada sección con 1-2 takeaways concretos
        - **Honest assessment**: Reconoce limitaciones, riesgos, trade-offs
        
        Formato del reporte:
        - Markdown profesional (headings, lists, tables, code blocks)
        - Citations: [Paper Title, Year] o [Source URL]
        - Tablas para comparisons y specs
        - Code snippets solo cuando añaden valor
        - Diagramas en ASCII art o Mermaid syntax (texto)
        
        IMPORTANTE:
        - NO repitas información textualmente de los inputs
        - SÍ sintetiza, conecta, interpreta
        - Identifica lo que los agentes NO vieron (meta-analysis)
        - Sé crítico: ¿Hay gaps en el análisis? ¿Qué falta?
        """,
        
        tools=[
            # Database para guardar análisis final
            database_tool.save_analysis,
            database_tool.get_previous_analysis,
            database_tool.query_papers,
            database_tool.log_model_usage,
            database_tool.get_usage_statistics,
        ],
        
        llm=llm_model,
        
        verbose=True,
        memory=True,
        allow_delegation=False,
        max_iter=12,
        max_rpm=20,  # GPT-5 rate limit
    )
    
    logger.info(
        "content_synthesizer_created",
        model=model_info,
        tools_count=5,
        estimated_duration="9-10 minutes",
        expected_credits=0.5,
    )
    
    return agent


def create_synthesis_task(
    agent: Agent,
    niche: str,
    context_tasks: Optional[List[Task]] = None
) -> Task:
    """
    Crea la tarea de síntesis final.
    
    Args:
        agent: Instancia del ContentSynthesizer
        niche: Nombre del niche
        context_tasks: Tasks de los 4 agentes anteriores
    
    Returns:
        Task: Tarea configurada con descripción y output esperado
    """
    task = Task(
        description="""
        Sintetiza análisis completo de "__NICHE__" en reporte ejecutivo profesional.
        
        **INPUTS DISPONIBLES** (de 4 agentes previos):
        
        1. **NicheAnalyst Output**:
           - Viabilidad del niche (score 1-10)
           - Tendencias en GitHub, Reddit, papers
           - Sub-niches identificados (5-7)
           - Keywords y términos técnicos
           - Análisis de demanda/competencia
        
        2. **LiteratureResearcher Output**:
           - 100-200 papers analizados
           - Top 20 papers más relevantes
           - Trends (3-5 tendencias principales)
           - Gaps (2-3 gaps de investigación)
           - Métodos y arquitecturas usadas
           - Datasets y benchmarks
        
        3. **TechnicalArchitect Output**:
           - Arquitectura propuesta (5 componentes)
           - Stack tecnológico completo
           - Diagramas de arquitectura
           - Patrones de diseño (3-5)
           - Consideraciones de seguridad (5-7)
           - Complejidad técnica (1-10)
        
        4. **ImplementationSpecialist Output**:
           - User stories (20-40 tasks)
           - Cronograma (4-8 sprints)
           - Librerías específicas con versiones
           - Code examples y templates
           - Riesgos técnicos identificados
           - Setup instructions
        
        **TU PROCESO DE SÍNTESIS** (9-10 minutos total):
        
        **FASE 1: Análisis de Inputs (3-4 minutos)**
        
        PASO 1.1: Leer todos los outputs (2 min)
        - Lee cronológicamente: Niche → Literature → Architecture → Implementation
        - Toma notas mentales:
          * Key numbers (citations, story points, duración)
          * Technical terms que se repiten
          * Claims importantes de cada agente
        
        PASO 1.2: Identificar Themes (1 min)
        - ¿Qué es lo MÁS importante?
          Ejemplo: "WASM es clave en 80% de papers + aparece en arquitectura"
        - ¿Hay contradicciones?
          Ejemplo: "Papers dicen que X es difícil, pero GitHub muestra librerías maduras"
        - ¿Qué insights son únicos?
          Ejemplo: "Gap específico no mencionado en papers pero crítico en práctica"
        
        **FASE 2: Construcción del Reporte (4-5 minutos)**
        
        PASO 2.1: Executive Summary (1 min)
        - 300-500 palabras
        - Hook: ¿Por qué importa este niche AHORA?
        - Key Finding 1: [Del NicheAnalyst]
        - Key Finding 2: [Del LiteratureResearcher]
        - Key Finding 3: [Del TechnicalArchitect]
        - Recommendation: [Acción concreta]
        - Expected Impact: [Métricas cuantificables]
        
        PASO 2.2: Secciones Principales (3 min)
        - Introducción (context del niche)
        - Análisis del Estado del Arte (synthesis de papers)
        - Oportunidades Identificadas (gaps + demanda)
        - Solución Propuesta (arquitectura high-level)
        - Plan de Implementación (timeline, budget)
        - Riesgos y Mitigaciones
        
        PASO 2.3: Visualizaciones (1 min)
        - Tabla comparativa (nuestra propuesta vs alternativas)
        - Timeline (Gantt en ASCII/Markdown)
        - Metrics dashboard (texto: papers analizados, story points, etc.)
        
        **FASE 3: Refinamiento (2 minutos)**
        
        PASO 3.1: Meta-Analysis (1 min)
        - ¿Hay algo que los agentes NO vieron?
        - ¿Gaps en el análisis?
        - ¿Sesgos evidentes?
        - Agrega sección "Limitations and Future Work"
        
        PASO 3.2: Actionable Insights (1 min)
        - Para cada sección mayor, agrega:
          "**Key Takeaway**: [Insight concreto en 1-2 líneas]"
        - Sección final "Next Steps" con timeline:
          * Semana 1-2: [Tareas críticas]
          * Mes 1: [Milestone]
          * Mes 2-3: [MVP]
        
        **OUTPUT ESPERADO**: Ver expected_output abajo
        
        **CALIDAD CHECKS**:
        - [ ] Executive summary puede leerse standalone
        - [ ] Cada claim tiene citation/source
        - [ ] Tablas y listas bien formateadas
        - [ ] Code blocks tienen syntax highlighting
        - [ ] Next steps son SMART (Specific, Measurable, Achievable, Relevant, Time-bound)
        - [ ] Reconoce limitaciones honestamente
        - [ ] Balance técnico vs estratégico (~60/40)
    """.replace("__NICHE__", niche),
        
    expected_output="""
    # Análisis Completo: __NICHE__
        ## Reporte Ejecutivo y Plan de Implementación
        
        ---
        
        ## Executive Summary
        
        [300-500 palabras impactantes]
        
        ### Context
        [2-3 oraciones sobre el estado actual del niche]
        
        ### Key Findings
        1. **Viabilidad**: [Score X/10] - [Razón en 1 línea del NicheAnalyst]
        2. **Estado del Arte**: [Resumen de literatura en 2 líneas]
        3. **Oportunidad Técnica**: [Gap específico identificado]
        4. **Factibilidad**: [Complejidad Y/10, Z semanas, W story points]
        
        ### Recommendation
        [1-2 párrafos con recomendación clara: GO/NO-GO/PIVOT]
        
        Si GO:
        - **Timeline**: X semanas (Y sprints)
        - **Budget estimado**: ~$N (credits + infra)
        - **Team**: Z developers
        - **MVP**: [Fecha estimada]
        
        ### Expected Impact
        - **Innovation**: [Qué es nuevo vs papers]
        - **Market opportunity**: [Tamaño, crecimiento]
        - **Technical contribution**: [A quién ayuda]
        
        ---
        
        ## 1. Introducción
        
        ### 1.1 Motivación
        [2-3 párrafos: ¿Por qué este niche? ¿Qué problema resuelve?]
        
        Basado en análisis de:
        - **X papers académicos** (últimos 2 años, >Y citaciones promedio)
        - **Z repositorios GitHub** (>W stars totales)
        - **N discusiones comunitarias** (Reddit, HN, Discord)
        
    ### 1.2 Definición del Niche
    **__NICHE__** se define como: [Definición técnica precisa]
        
        **Sub-niches identificados** (del NicheAnalyst):
        1. [Sub-niche 1] - Viabilidad: X/10
        2. [Sub-niche 2] - Viabilidad: Y/10
        3-5. [Otros sub-niches]
        
        **Términos clave**: [Lista de keywords técnicos]
        
        ### 1.3 Metodología del Análisis
        Este reporte sintetiza outputs de 4 agentes especializados:
        - **NicheAnalyst**: Viabilidad y tendencias
        - **LiteratureResearcher**: 100-200 papers académicos
        - **TechnicalArchitect**: Diseño de sistema
        - **ImplementationSpecialist**: Plan de desarrollo
        
        ---
        
        ## 2. Estado del Arte
        
        ### 2.1 Revisión de Literatura
        **Papers analizados**: [N papers, con desglose por año]
        
        **Top 5 Papers Clave**:
        1. **[Title]** (Autor, Año) - [Citations: X]
           - **Contribución**: [Qué aporta en 2 líneas]
           - **Relevancia**: [Por qué es importante para nuestro niche]
        
        2-5. [Misma estructura]
        
        **Key Takeaway**: [Insight principal de la literatura en 2 líneas]
        
        ### 2.2 Tendencias Identificadas
        Del LiteratureResearcher:
        
        #### Trend 1: [Nombre de trend]
        - **Evidencia**: [Papers que lo mencionan: X%, Y de Z papers]
        - **Implicación**: [Qué significa para nosotros]
        
        #### Trend 2-5: [Misma estructura]
        
        **Key Takeaway**: [Cuál es la dirección del campo]
        
        ### 2.3 Métodos y Arquitecturas Existentes
        Arquitecturas usadas en papers:
        - **[Arquitectura 1]**: [% de papers que la usan] - [Pros/Cons]
        - **[Arquitectura 2-3]**: [Misma estructura]
        
        Tecnologías dominantes:
        | Categoría | Tecnología | Adopción | Madurez |
        |-----------|------------|----------|---------|
        | Lenguaje  | [X]        | [%]      | [Alta/Media/Baja] |
        | Framework | [Y]        | [%]      | [...] |
        | Database  | [Z]        | [%]      | [...] |
        
        **Key Takeaway**: [Qué stack usar y por qué]
        
        ### 2.4 Gaps de Investigación
        Del LiteratureResearcher:
        
        #### Gap 1: [Descripción]
        - **Problema**: [Qué falta en papers]
        - **Impacto**: [Por qué es importante]
        - **Opportunity**: [Cómo podemos llenarlo]
        
        #### Gap 2-3: [Misma estructura]
        
        **Key Takeaway**: [Cuál gap atacar primero]
        
        ---
        
        ## 3. Análisis de Viabilidad
        
        ### 3.1 Viabilidad Técnica
        **Score**: [X/10] (del NicheAnalyst)
        
        **Factores**:
        - **Complejidad técnica**: [Y/10] - [Razón]
        - **Madurez de herramientas**: [Z/10] - [Librerías disponibles]
        - **Riesgos técnicos**: [N riesgos identificados]
        
        ### 3.2 Viabilidad de Mercado
        **Score**: [X/10]
        
        **Indicadores**:
        - **Demanda**: [Evidencia: GitHub stars, NPM downloads, etc.]
        - **Competencia**: [Proyectos similares: X proyectos, Y estrellas promedio]
        - **Crecimiento**: [% crecimiento en último año]
        
        ### 3.3 Viabilidad de Implementación
        **Score**: [X/10]
        
        **Recursos requeridos**:
        - **Developers**: [N personas]
        - **Timeline**: [X semanas]
        - **Budget**: [~$Y en credits + $Z en infra]
        - **Expertise necesario**: [Skills: Rust, WASM, etc.]
        
        **Key Takeaway**: [GO/NO-GO y por qué]
        
        ---
        
        ## 4. Solución Propuesta
        
        ### 4.1 Arquitectura High-Level
        [Descripción de 2-3 párrafos basada en TechnicalArchitect output]
        
        **Componentes principales** (5 componentes):
        1. **[Componente 1]**: [Responsabilidad]
        2-5. [Misma estructura]
        
        **Diagrama de Arquitectura**:
        ```
        [Referencia al diagrama ASCII del TechnicalArchitect, o versión simplificada]
        ```
        
        **Key Takeaway**: [Por qué esta arquitectura vs alternativas]
        
        ### 4.2 Stack Tecnológico
        Del TechnicalArchitect + ImplementationSpecialist:
        
        | Capa | Tecnología | Versión | Justificación |
        |------|------------|---------|---------------|
        | Frontend | [X] | vY.Z | [Por qué] |
        | Backend | [A] | vB.C | [Por qué] |
        | Database | [D] | vE.F | [Por qué] |
        | Deployment | [G] | vH.I | [Por qué] |
        
        **Librerías clave** (del ImplementationSpecialist):
        - **[Lib 1]**: vX.Y - [Link GitHub] - [Stars: Z] - [Por qué es crítica]
        - **[Lib 2-5]**: [Misma estructura]
        
        **Key Takeaway**: [Por qué este stack vs alternativas populares]
        
        ### 4.3 Patrones de Diseño
        Del TechnicalArchitect:
        
        1. **[Pattern 1]**: [Qué problema resuelve]
        2-3. [Misma estructura]
        
        ### 4.4 Innovaciones vs Estado del Arte
        [Tabla comparativa]
        
        | Aspecto | Papers (estado del arte) | Nuestra propuesta | Ventaja |
        |---------|--------------------------|-------------------|---------|
        | [Aspecto 1] | [Approach actual] | [Nuestro approach] | [Mejora X%] |
        | [Aspecto 2-4] | [...] | [...] | [...] |
        
        **Key Takeaway**: [Qué es realmente nuevo]
        
        ---
        
        ## 5. Plan de Implementación
        
        ### 5.1 Cronograma
        Del ImplementationSpecialist:
        
        **Duración total**: [X semanas] ([Y sprints de 2 semanas])
        
        **Timeline (Gantt-style)**:
        ```
        Sprint 1-2 (4 weeks): Setup + MVP
        ├── Week 1: [Tareas]
        ├── Week 2: [Tareas]
        └── Week 3-4: [Tareas]
        
        Sprint 3-4 (4 weeks): Core Features
        ├── Week 5-6: [Tareas]
        └── Week 7-8: [Tareas]
        
        Sprint 5-6 (4 weeks): Testing + Docs
        └── Week 9-12: [Tareas]
        ```
        
        ### 5.2 Hitos Clave (Milestones)
        - **Week 2**: Repo setup + CI/CD ✓
        - **Week 4**: MVP funcional (componente core)
        - **Week 8**: Sistema completo integrado
        - **Week 12**: Tests completos + documentación → **Release v1.0**
        
        ### 5.3 Complejidad y Effort
        **Story points totales**: [X points]
        **Velocity estimada**: [Y points/sprint]
        **Sprints necesarios**: [Z sprints]
        
        **Desglose por componente**:
        - [Componente 1]: [X story points] ([Y% del total])
        - [Componente 2-5]: [Misma estructura]
        
        **Key Takeaway**: [Qué componente es el bottleneck]
        
        ### 5.4 Recursos Necesarios
        **Team composition**:
        - [N] Full-stack developers (skills: [X, Y, Z])
        - [M] DevOps engineer (opcional para setup)
        
        **Budget estimado**:
        - **Development**: [X developer-weeks × $Y] = $Z
        - **AI credits**: ~[W créditos/analysis × $N] = $M
        - **Infrastructure**: [Cloud costs: $P/month × Q meses] = $R
        - **Total**: ~$[Z + M + R]
        
        **Key Takeaway**: [Es cost-effective vs alternatives]
        
        ---
        
        ## 6. Riesgos y Mitigaciones
        
        Del ImplementationSpecialist + meta-analysis:
        
        ### Riesgo 1: [Nombre]
        - **Descripción**: [Qué puede salir mal]
        - **Probabilidad**: [Alta/Media/Baja]
        - **Impacto**: [Alto/Medio/Bajo]
        - **Mitigación**: [Qué hacer para prevenir]
        - **Plan B**: [Alternativa si ocurre]
        
        ### Riesgo 2-5: [Misma estructura]
        
        **Riesgos NO considerados por agentes** (meta-analysis):
        - [Riesgo adicional que identificaste al sintetizar]
        
        **Key Takeaway**: [Cuál es el mayor riesgo y cómo manejarlo]
        
        ---
        
        ## 7. Comparación con Alternativas
        
        ### Alternativa 1: [Proyecto/Approach similar]
        - **Approach**: [Qué hacen]
        - **Pros**: [Ventajas]
        - **Cons**: [Desventajas]
        - **Diferenciación**: [Por qué somos mejores]
        
        ### Alternativa 2-3: [Misma estructura]
        
        **Tabla de comparación**:
        | Criterio | Nuestra propuesta | Alt 1 | Alt 2 | Alt 3 |
        |----------|-------------------|-------|-------|-------|
        | Complejidad | [X/10] | [Y/10] | [Z/10] | [W/10] |
        | Timeline | [N weeks] | [M weeks] | [...] | [...] |
        | Innovation | [Alta/Media/Baja] | [...] | [...] | [...] |
        | Cost | [$X] | [$Y] | [...] | [...] |
        
        **Key Takeaway**: [Por qué elegir nuestra propuesta]
        
        ---
        
        ## 8. Métricas de Éxito
        
        ### KPIs Técnicos
        - **Performance**: [Métrica: latencia <X ms, throughput >Y req/s]
        - **Reliability**: [Uptime >99.x%]
        - **Test coverage**: [>X%]
        
        ### KPIs de Adopción
        - **GitHub stars**: [Target: X en Y meses]
        - **NPM/crates.io downloads**: [Target: Z/week]
        - **Contributors**: [Target: N developers]
        
        ### KPIs de Impacto
        - **Papers citando el proyecto**: [Target: X papers en Y años]
        - **Production usage**: [Target: Z companies usando]
        
        **Key Takeaway**: [Cómo medir si tuvimos éxito]
        
        ---
        
        ## 9. Limitaciones del Análisis
        
        ### Limitaciones Técnicas
        - [Qué NO pudimos analizar en detalle]
        - [Gaps en el análisis de papers]
        - [Tecnologías no evaluadas]
        
        ### Limitaciones de Scope
        - [Qué quedó fuera del scope]
        - [Trade-offs que no exploramos]
        
        ### Sesgos Identificados
        - [Sesgos en selección de papers (ej: solo inglés)]
        - [Sesgos en evaluación de librerías (ej: preferencia por populares)]
        
        **Key Takeaway**: [Qué análisis adicional se necesita]
        
        ---
        
        ## 10. Next Steps (Accionables)
        
        ### Immediate Actions (Próximas 2 semanas)
        1. **[Acción 1]**: [Qué hacer] - [Owner: quién] - [Deadline: cuando]
        2. **[Acción 2-5]**: [Misma estructura]
        
        ### Short-term (Mes 1)
        - **Milestone**: [Qué lograr]
        - **Tasks**:
          - [ ] [Tarea 1]
          - [ ] [Tarea 2-5]
        
        ### Medium-term (Meses 2-3)
        - **Milestone**: MVP completo
        - **Decision points**: [Qué decisiones tomar en este punto]
        
        ### Long-term (Meses 4-6)
        - **Milestone**: v1.0 release
        - **Success criteria**: [Qué define éxito]
        
        **Key Takeaway**: [Cuál es el primer paso más crítico]
        
        ---
        
        ## 11. Conclusiones
        
        ### Resumen de Findings
        [2-3 párrafos sintetizando todo]
        
        ### Recomendación Final
        **[GO / NO-GO / PIVOT]**
        
        **Si GO**:
        - **Confidence level**: [Alta/Media/Baja] - [Por qué]
        - **Biggest opportunity**: [Qué gap llenamos]
        - **Biggest risk**: [Qué nos preocupa más]
        - **Next step**: [Acción inmediata]
        
        **Si NO-GO**:
        - **Razones**: [Por qué no proceder]
        - **Alternativas**: [Qué hacer en su lugar]
        
        **Si PIVOT**:
        - **Propuesta alternativa**: [Qué ajustar]
        - **Razón del pivot**: [Por qué cambiar]
        
        ### Impacto Esperado
        [2 párrafos sobre el impacto técnico, científico y práctico]
        
        ---
        
        ## 12. Apéndices
        
        ### A. Referencias
        **Papers citados**: [Lista completa con links]
        1. [Paper 1 con citation completa]
        2-N. [Otros papers]
        
        **Recursos técnicos**: [Links a docs, repos, tutorials]
        
    ### B. Metadata del Análisis
    - **Niche analizado**: __NICHE__
        - **Fecha**: [Timestamp]
        - **Papers analizados**: [N papers]
        - **Duración del análisis**: [X minutos]
        - **Créditos utilizados**: [Y credits]
        - **Agentes involucrados**: 5 (NicheAnalyst, LiteratureResearcher, TechnicalArchitect, ImplementationSpecialist, ContentSynthesizer)
        
        ### C. Feedback Loop
        **Para mejorar futuros análisis**:
        - ¿Qué faltó en este análisis?
        - ¿Qué secciones fueron más/menos útiles?
        - ¿Qué preguntas quedaron sin responder?
        
        ---
        
        **Fin del Reporte**
        
        *Generado por ARA Framework (Automated Research & Analysis)*
        *Para más información: [GitHub repo link]*
    """.replace("__NICHE__", niche),
        
        agent=agent,
        
        context=context_tasks if context_tasks else [],
    )
    
    logger.info(
        "synthesis_task_created",
        niche=niche,
        expected_duration="9-10 minutes",
        dependencies=len(context_tasks) if context_tasks else 0,
        expected_output_words="10000-15000",
    )
    
    return task


def create_content_synthesizer(
    niche: str,
    context_tasks: Optional[List[Task]] = None
) -> tuple[Agent, Task]:
    """
    Helper para crear el ContentSynthesizer.
    
    Args:
        niche: Nombre del niche a analizar
        context_tasks: Lista de tasks de agentes previos (niche, literature, architecture, implementation)
    
    Returns:
        tuple: (agent, task) listos para crew
    """
    agent = create_content_synthesizer_agent()
    task = create_synthesis_task(agent, niche, context_tasks)
    
    logger.info(
        "content_synthesizer_ready",
        niche=niche,
        sla="9-10 minutes",
        budget="~0.5 credits",
        output_sections=12,
    )
    
    return agent, task
