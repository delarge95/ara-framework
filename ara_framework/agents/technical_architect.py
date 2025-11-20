"""
TechnicalArchitect Agent - System architecture design based on research.

Este agente:
1. Recibe papers y gaps del LiteratureResearcher
2. Diseña arquitectura técnica del sistema
3. Identifica tecnologías, frameworks y herramientas
4. Evalúa viabilidad de implementación
5. Define componentes, módulos y sus interacciones
6. Genera diagramas arquitectónicos (en texto/mermaid)

Modelos:
- Primary: Claude Sonnet 4.5 (1 crédito, excelente para arquitectura y sistemas)
- Fallback: DeepSeek V3 (0 créditos free, sorprendentemente bueno para código)

SLA: 10-12 minutos
Budget: ~1 crédito (Sonnet)

Tools: scraping_tool (2 tools), pdf_tool (2 tools), database_tool (2 tools)

Output: Documento de arquitectura técnica con componentes, diagramas, stack

Fuente: docs/03_AI_MODELS.md (Agent 3), docs/04_ARCHITECTURE.md (Agents Layer)
"""
import structlog
# from crewai import Agent, Task  # CrewAI removed - using LangGraph only
from typing import Dict, Any, Optional

from config.settings import settings
from tools import get_scraping_tool, get_pdf_tool, get_database_tool

logger = structlog.get_logger()


def create_technical_architect_agent() -> Agent:
    """
    Crea el agente TechnicalArchitect.
    
    Claude Sonnet es el mejor modelo para diseño de arquitecturas
    gracias a su razonamiento profundo y conocimiento actualizado.
    
    Returns:
        Agent: Instancia configurada del TechnicalArchitect
    """
    # Obtener tools
    scraping_tool = get_scraping_tool()
    pdf_tool = get_pdf_tool()
    database_tool = get_database_tool()
    
    # Configurar LLM (Groq - LLaMA 3.3-70B GRATIS)
    llm_model = "groq/llama-3.3-70b-versatile"
    
    agent = Agent(
        role="Technical Architect & System Designer",
        
        goal="""Diseñar arquitectura técnica completa para '{niche}' basada en:
        1. Investigación académica del LiteratureResearcher
        2. Gaps identificados (oportunidades de innovación)
        3. Best practices de papers implementados
        4. Análisis de repos GitHub similares (aprender de casos reales)
        5. Documentación técnica de frameworks relevantes
        
        Output: Documento arquitectónico profesional con diagramas, componentes, stack
        """,
        
        backstory="""Eres un arquitecto de software senior con 20+ años de experiencia.
        
        Tu expertise incluye:
        - Diseño de sistemas distribuidos escalables
        - Arquitecturas de microservicios, event-driven, serverless
        - Cloud-native patterns (AWS, GCP, Azure)
        - Machine Learning systems (MLOps, feature stores, model serving)
        - Data pipelines (ETL, streaming, batch processing)
        - Trade-offs: performance vs complexity, cost vs scalability
        
        Tu proceso de diseño:
        1. **Entender Requisitos**: Lees papers y gaps del LiteratureResearcher
        2. **Analizar Casos Reales**: Scrapeas repos GitHub exitosos en el niche
        3. **Diseñar Componentes**: Defines módulos, APIs, data flows
        4. **Elegir Stack**: Seleccionas tecnologías basadas en evidencia (papers + repos)
        5. **Evaluar Trade-offs**: Complejidad, costo, time-to-market, mantenibilidad
        6. **Documentar**: Diagramas Mermaid, descripciones detalladas, justificaciones
        
        Principios de diseño:
        - **Simplicidad primero**: KISS (Keep It Simple, Stupid)
        - **Modularidad**: Componentes independientes, low coupling, high cohesion
        - **Escalabilidad**: Diseño para crecer (horizontal scaling)
        - **Observabilidad**: Logs, metrics, traces desde el inicio
        - **Testabilidad**: Arquitectura que facilita unit + integration tests
        - **Documentación**: Código sin docs = código muerto
        
        IMPORTANTE:
        - No diseñes "ivory towers" (arquitecturas teóricas imposibles)
        - Balancea IDEAL vs PRAGMÁTICO (MVP primero, optimiza después)
        - Justifica CADA decisión técnica con evidencia (papers, repos, docs)
        - Si hay 2 opciones, compara pros/cons/costs
        - Anticipa puntos de falla y cuellos de botella
        """,
        
        tools=[
            # Web scraping para analizar repos GitHub y documentación
            scraping_tool.scrape_website,
            scraping_tool.extract_structured_data,
            
            # PDF processing para leer papers técnicos en detalle
            pdf_tool.extract_pdf_sections,
            pdf_tool.extract_pdf_text_only,
            
            # Database queries para consultar papers guardados
            database_tool.query_papers,
            database_tool.get_paper_by_id,
        ],
        
        llm=llm_model,
        
        verbose=True,
        memory=True,
        allow_delegation=False,
        max_iter=20,
        max_rpm=50,  # Anthropic rate limits
    )
    
    logger.info(
        "technical_architect_created",
        model="claude-sonnet-4.5",
        fallback="deepseek-v3",
        tools_count=6,
        estimated_duration="10-12 minutes",
    )
    
    return agent


def create_technical_architecture_task(
    agent: Agent,
    niche: str,
    literature_research_context: Optional[Task] = None
) -> Task:
    """
    Crea la tarea de diseño arquitectónico.
    
    Args:
        agent: Instancia del TechnicalArchitect
        niche: Nombre del niche
        literature_research_context: Task del LiteratureResearcher
    
    Returns:
        Task: Tarea configurada con descripción y output esperado
    """
    task = Task(
  description="""
  Diseña arquitectura técnica completa para un sistema de "__NICHE__".
        
        Recibes del LiteratureResearcher:
        - Top 10 papers más influyentes
        - Gaps identificados (oportunidades)
        - Metodologías comunes
        - Stack tecnológico recomendado
        - Datasets y benchmarks
        
        **FASE 1: Análisis de Contexto (3-4 minutos)**
        
        PASO 1.1: Revisar Papers Clave (2 min)
        - Lee Abstract + Methods de los Top 5 papers más citados
        - Usa get_paper_by_id() para obtener PDFs guardados
        - Usa extract_pdf_sections() para extraer Methods
        - Identifica: ¿Qué arquitecturas usan? ¿Qué componentes?
        
        PASO 1.2: Analizar Repos GitHub (2 min)
  - Busca repos en GitHub: "https://github.com/search?q=__NICHE__+stars:>500"
        - Usa scrape_website() para obtener README, arquitectura
        - Identifica: Tech stack real (no teórico), file structure
        - Observa: ¿Qué frameworks usan? ¿Qué patterns?
        
        **FASE 2: Diseño de Alto Nivel (4-5 minutos)**
        
        PASO 2.1: Definir Componentes Principales (2 min)
        - Basándote en papers + repos, define 4-8 componentes core
        - Ejemplo para "Rust + WebAssembly":
          1. Compiler (Rust → WASM)
          2. Runtime (WASM execution engine)
          3. Bindings (JS ↔ WASM communication)
          4. Tooling (debugger, profiler)
          5. Package manager (dependencies)
        
        - Para cada componente define:
          a) Responsabilidad (qué hace)
          b) Inputs/Outputs (qué recibe, qué retorna)
          c) Tecnologías candidatas (2-3 opciones)
        
        PASO 2.2: Diseñar Data Flow (1 min)
        - ¿Cómo fluyen los datos entre componentes?
        - ¿Hay APIs? ¿Message queues? ¿Shared storage?
        - Dibuja en Mermaid:
          ```mermaid
          graph LR
            A[Component1] -->|data| B[Component2]
            B -->|result| C[Component3]
          ```
        
        PASO 2.3: Identificar Puntos Críticos (1 min)
        - ¿Cuáles son los cuellos de botella? (CPU, I/O, network)
        - ¿Dónde puede fallar? (single points of failure)
        - ¿Qué es más costoso? (compute, storage, bandwidth)
        
        **FASE 3: Diseño Detallado (3-4 minutos)**
        
        PASO 3.1: Elegir Stack Tecnológico (2 min)
        - Basándote en papers + repos + docs, elige:
          a) Lenguajes: [ej: Rust, Python, TypeScript]
          b) Frameworks: [ej: Tokio, FastAPI, React]
          c) Bases de datos: [ej: PostgreSQL, Redis, S3]
          d) Infraestructura: [ej: Docker, Kubernetes, Terraform]
          e) Observabilidad: [ej: Prometheus, Grafana, OpenTelemetry]
        
        - Para CADA tecnología, justifica:
          - ¿Por qué esta y no alternativa X?
          - ¿Qué papers/repos la usan?
          - ¿Cuál es el trade-off? (performance vs complexity)
        
        PASO 3.2: Definir APIs y Contratos (1 min)
        - ¿Qué APIs expone cada componente?
        - Ejemplo:
          ```
          POST /compile
          {{
            "source_code": "...",
            "target": "wasm32-unknown-unknown"
          }}
          → Returns: {{ "wasm_binary": "...", "errors": [] }}
          ```
        
        PASO 3.3: Evaluar Complejidad (1 min)
        - Escala 1-10 para cada componente:
          a) Complejidad de implementación
          b) Time-to-market (semanas)
          c) Costo de mantenimiento
        
        - Identifica: ¿Qué es MVP vs nice-to-have?
        
        **SALIDAS INTERMEDIAS** (para logs):
    - Después de FASE 1: "Analizados X papers, Y repos GitHub"
    - Después de FASE 2: "Definidos Z componentes, W data flows"
    - Después de FASE 3: "Stack seleccionado: [lista]"
  """.replace("__NICHE__", niche),

  expected_output="""
    # Arquitectura Técnica: __NICHE__
        
        ## 1. Resumen Ejecutivo (3-4 párrafos)
        - ¿Qué estamos construyendo? (elevator pitch en 2 oraciones)
        - ¿Cuál es el enfoque arquitectónico? (monolith, microservices, serverless)
        - ¿Qué hace único este diseño? (innovación vs papers)
        - Complejidad estimada: Baja | Media | Alta (justificar)
        
        ## 2. Contexto y Decisiones de Diseño
        ### Papers Analizados
        - **[Paper 1]**: [Qué arquitectura usa] → [Qué aprendimos]
        - **[Paper 2]**: [Qué arquitectura usa] → [Qué aprendimos]
        - **[Paper 3]**: [Qué arquitectura usa] → [Qué aprendimos]
        
        ### Repos GitHub Analizados
        - **[Repo 1]**: [Tech stack] → [Qué adoptamos]
        - **[Repo 2]**: [Tech stack] → [Qué evitamos]
        
        ### Principios de Diseño Aplicados
        1. **[Principio 1]**: [Por qué] (ej: Simplicidad sobre complejidad)
        2. **[Principio 2]**: [Por qué] (ej: Modularidad para testability)
        3. **[Principio 3]**: [Por qué] (ej: Observabilidad desde día 1)
        
        ## 3. Arquitectura de Alto Nivel
        ### Diagrama de Componentes (Mermaid)
        ```mermaid
        graph TB
            subgraph "Frontend Layer"
                A[Web UI]
                B[CLI]
            end
            
            subgraph "API Layer"
                C[REST API]
                D[WebSocket Gateway]
            end
            
            subgraph "Core Logic"
                E[Component 1]
                F[Component 2]
                G[Component 3]
            end
            
            subgraph "Data Layer"
                H[PostgreSQL]
                I[Redis Cache]
                J[S3 Storage]
            end
            
            A --> C
            B --> C
            C --> E
            C --> F
            E --> F --> G
            E --> H
            F --> I
            G --> J
        ```
        
        ### Descripción de Capas
        1. **Frontend Layer**: [Descripción 2-3 líneas]
        2. **API Layer**: [Descripción 2-3 líneas]
        3. **Core Logic**: [Descripción 2-3 líneas]
        4. **Data Layer**: [Descripción 2-3 líneas]
        
        ## 4. Componentes Detallados
        ### Componente 1: [Nombre]
        - **Responsabilidad**: [Qué hace este componente]
        - **Inputs**: [Qué recibe]
        - **Outputs**: [Qué retorna]
        - **Tecnologías**: [Lenguaje, frameworks, librerías]
        - **Dependencias**: [Componentes de los que depende]
        - **Complejidad**: X/10
        - **Estimación**: Y semanas
        - **Justificación técnica**: [Por qué estas decisiones]
        - **Trade-offs**: [Pros y contras]
        
        ### Componente 2: [Nombre]
        [Misma estructura]
        
        ### Componente 3: [Nombre]
        [Misma estructura]
        
        [Continuar para todos los componentes]
        
        ## 5. Data Flow y Comunicación
        ### Flujo Principal (Happy Path)
        1. User request → [Componente A]
        2. [Componente A] procesa → [Componente B]
        3. [Componente B] consulta DB → [Componente C]
        4. [Componente C] retorna resultado → User
        
        ### Flujo de Errores (Error Handling)
        - Si falla [Componente A]: [Qué hacer]
        - Si timeout en [Componente B]: [Retry logic]
        - Si DB no disponible: [Fallback a cache]
        
        ### Diagrama de Secuencia (Mermaid)
        ```mermaid
        sequenceDiagram
            participant User
            participant API
            participant Component1
            participant Component2
            participant DB
            
            User->>API: Request
            API->>Component1: Process
            Component1->>Component2: Transform
            Component2->>DB: Query
            DB-->>Component2: Data
            Component2-->>Component1: Result
            Component1-->>API: Response
            API-->>User: Success
        ```
        
        ## 6. Stack Tecnológico (con Justificaciones)
        ### Lenguajes de Programación
        - **[Lenguaje 1]**: [Por qué] | Usado en X papers, Y repos
          - Alternativas consideradas: [Lenguaje alternativo] (rechazado porque...)
          - Trade-offs: [Performance vs Developer Experience]
        
        - **[Lenguaje 2]**: [Por qué]
          [Misma estructura]
        
        ### Frameworks y Librerías
        - **[Framework 1]**: [Por qué] | Evidencia: [Papers/repos]
        - **[Framework 2]**: [Por qué]
        - **[Librería 1]**: [Por qué]
        
        ### Bases de Datos y Storage
        - **[DB 1]**: [Por qué este tipo] (SQL vs NoSQL)
          - Schema: [Brevemente: tablas principales]
          - Escalabilidad: [Cómo escala]
          - Costo: [Estimado mensual]
        
        - **[Cache 1]**: [Por qué] (Redis, Memcached)
        - **[Storage 1]**: [Por qué] (S3, local filesystem)
        
        ### Infraestructura y DevOps
        - **Containerización**: Docker (porque...)
        - **Orchestration**: Kubernetes / Docker Compose (porque...)
        - **CI/CD**: GitHub Actions / GitLab CI (porque...)
        - **IaC**: Terraform / Pulumi (porque...)
        - **Cloud Provider**: AWS / GCP / Azure / Local (porque...)
        
        ### Observabilidad
        - **Logs**: [Herramienta] (ej: ELK stack, Loki)
        - **Metrics**: [Herramienta] (ej: Prometheus + Grafana)
        - **Traces**: [Herramienta] (ej: Jaeger, Zipkin, Uptrace)
        - **Alerting**: [Herramienta] (ej: PagerDuty, Slack)
        
        ## 7. APIs y Contratos
        ### API REST Endpoints
        ```
        POST /api/v1/[resource]
  GET /api/v1/[resource]/{{id}}
  PUT /api/v1/[resource]/{{id}}
  DELETE /api/v1/[resource]/{{id}}
        ```
        
        ### Ejemplo de Request/Response
        ```json
        // POST /api/v1/compile
        {
          "source_code": "fn main() { ... }",
          "target": "wasm32"
        }
        
        // Response 200 OK
        {
          "status": "success",
          "wasm_binary": "base64...",
          "compilation_time_ms": 1234,
          "warnings": []
        }
        ```
        
        ### WebSocket Events (si aplica)
        - `connection.open`: Cuando cliente conecta
        - `data.update`: Cuando hay nuevos datos
        - `error.occurred`: Cuando falla algo
        
        ## 8. Seguridad y Autenticación
        - **Autenticación**: JWT / OAuth2 / API Keys (porque...)
        - **Autorización**: RBAC / ABAC (porque...)
        - **Encriptación**: TLS 1.3 (en tránsito), AES-256 (en reposo)
        - **Secrets Management**: Vault / AWS Secrets Manager
        - **Rate Limiting**: [X requests/min por IP]
        - **Input Validation**: [Schema validation con Pydantic/Zod]
        
        ## 9. Escalabilidad y Performance
        ### Bottlenecks Identificados
        1. **[Bottleneck 1]**: [Descripción]
           - Impacto: Alto | Medio | Bajo
           - Solución: [Cómo mitigar] (caching, sharding, etc.)
        
        2. **[Bottleneck 2]**: [Descripción]
           [Misma estructura]
        
        ### Estrategias de Escalado
        - **Horizontal Scaling**: [Qué componentes] (stateless)
        - **Vertical Scaling**: [Qué componentes] (stateful, DB)
        - **Caching Strategy**: [Qué cachear] (Redis layers: L1, L2)
        - **Database Sharding**: [Si aplica] (cómo particionar)
        - **Load Balancing**: [Algoritmo] (round-robin, least-connections)
        
        ### Performance Targets (SLAs)
        - **Latencia p50**: < X ms
        - **Latencia p99**: < Y ms
        - **Throughput**: Z requests/sec
        - **Availability**: 99.9% uptime (8.7h downtime/año)
        
        ## 10. Testing Strategy
        ### Unit Tests
        - **Coverage target**: >80%
        - **Frameworks**: [pytest, Jest, etc.]
        - **Mocking**: [Qué mockear] (external APIs, DB)
        
        ### Integration Tests
        - **Qué testear**: [Component interactions]
        - **Fixtures**: [Datos de prueba]
        
        ### End-to-End Tests
        - **Scenarios**: [User flows críticos]
        - **Tools**: [Playwright, Cypress]
        
        ### Load Testing
        - **Tools**: [k6, Locust, JMeter]
        - **Scenarios**: [X concurrent users, Y requests/sec]
        
        ## 11. Deployment Strategy
        ### Entornos
        - **Development**: Local Docker Compose
        - **Staging**: [Cloud staging env]
        - **Production**: [Cloud production env]
        
        ### CI/CD Pipeline
        ```
        1. Code Push → GitHub
        2. Run Tests (unit + integration)
        3. Build Docker Images
        4. Push to Registry (Docker Hub, ECR)
        5. Deploy to Staging (automatic)
        6. Run E2E Tests
        7. Deploy to Production (manual approval)
        8. Health Check
        9. Rollback if failed
        ```
        
        ### Rollback Strategy
        - **Blue/Green Deployment**: [Descripción]
        - **Canary Releases**: [Descripción]
        - **Rollback Time**: < 5 minutos
        
        ## 12. Monitoreo y Alertas
        ### Métricas Clave (KPIs)
        - **Error Rate**: % de requests fallidos
        - **Response Time**: p50, p95, p99 latency
        - **Throughput**: requests/sec
        - **Resource Usage**: CPU, RAM, disk, network
        - **Database**: Query time, connection pool
        
        ### Alertas Configuradas
        - 🚨 **Critical**: Error rate > 5% → Página a on-call
        - ⚠️ **Warning**: Latency p99 > 1s → Slack notification
        - 💡 **Info**: Deployment completado → Slack notification
        
        ## 13. Costos Estimados
        ### Infraestructura (mensual)
        - **Compute**: $X (Y instances × $Z/hour × 730h)
        - **Database**: $W (storage + compute)
        - **Storage**: $V (S3, backups)
        - **Network**: $U (bandwidth)
        - **Monitoring**: $T (Datadog, NewRelic)
        - **Total**: $XXX/mes (para Z users)
        
        ### Escalado de Costos
        - 1K users: $X/mes
        - 10K users: $Y/mes
        - 100K users: $Z/mes
        
        ## 14. Roadmap de Implementación
        ### MVP (4-6 semanas)
        - ✅ Week 1-2: [Componentes core]
        - ✅ Week 3-4: [APIs + DB]
        - ✅ Week 5-6: [Testing + Deploy]
        
        ### v1.0 (12 semanas)
        - Week 7-8: [Feature X]
        - Week 9-10: [Feature Y]
        - Week 11-12: [Optimizaciones]
        
        ### v2.0 (24 semanas)
        - [Features avanzadas]
        
        ## 15. Riesgos y Mitigaciones
        ### Riesgo 1: [Descripción]
        - **Probabilidad**: Alta | Media | Baja
        - **Impacto**: Alto | Medio | Bajo
        - **Mitigación**: [Qué hacer para evitarlo]
        
        ### Riesgo 2: [Descripción]
        [Misma estructura]
        
        ## 16. Alternativas Consideradas (y por qué NO elegidas)
        ### Alternativa 1: [Nombre]
        - **Descripción**: [Qué sería diferente]
        - **Pros**: [Ventajas]
        - **Contras**: [Desventajas]
        - **Por qué NO**: [Razón de rechazo]
        
        ### Alternativa 2: [Nombre]
        [Misma estructura]
        
    ## 17. Recomendaciones para ImplementationSpecialist
    - **Empezar por**: [Componente X] (es el más crítico)
    - **Prototipo rápido**: [Qué validar primero]
    - **Librerías útiles**: [Lista con links]
    - **Patrones de código**: [Design patterns recomendados]
    - **Recursos**: [Tutoriales, docs, repos de referencia]
  """.replace("__NICHE__", niche),

    agent=agent,

    # Recibe contexto del LiteratureResearcher
    context=[literature_research_context] if literature_research_context else [],
  )
    
    logger.info(
        "technical_architecture_task_created",
        niche=niche,
        expected_duration="10-12 minutes",
        tools_used=["scraping_tool (2)", "pdf_tool (2)", "database_tool (2)"],
    )
    
    return task


# Función helper
def create_technical_architect(
    niche: str,
    literature_research_task: Optional[Task] = None
) -> tuple[Agent, Task]:
    """
    Helper para crear el TechnicalArchitect con su tarea.
    
    Args:
        niche: Nombre del niche
        literature_research_task: Task del LiteratureResearcher
    
    Returns:
        tuple[Agent, Task]: Tupla (agente, tarea)
    
    Example:
        >>> niche_agent, niche_task = create_niche_analyst("Rust + WASM")
        >>> lit_agent, lit_task = create_literature_researcher("Rust + WASM", niche_task)
        >>> arch_agent, arch_task = create_technical_architect("Rust + WASM", lit_task)
        >>> crew = Crew(
        ...     agents=[niche_agent, lit_agent, arch_agent],
        ...     tasks=[niche_task, lit_task, arch_task],
        ...     process=Process.sequential
        ... )
    """
    agent = create_technical_architect_agent()
    task = create_technical_architecture_task(agent, niche, literature_research_task)
    return agent, task
