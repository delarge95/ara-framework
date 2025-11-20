"""
ImplementationSpecialist Agent - Detailed implementation planning.

Este agente:
1. Recibe arquitectura del TechnicalArchitect
2. Genera plan de implementación paso a paso
3. Identifica librerías, herramientas y recursos específicos
4. Crea cronograma realista de desarrollo
5. Evalúa complejidad técnica de cada tarea
6. Provee code snippets y ejemplos de referencia

Modelos:
- Primary: DeepSeek V3 (0 créditos free, excelente para código)
- Fallback: Claude Haiku 4.5 (0.33 créditos, rápido)

SLA: 7-8 minutos
Budget: ~0.33 créditos (si fallback a Haiku)

Tools: scraping_tool (2 tools), database_tool (2 tools)

Output: Plan de implementación con tasks, librerías, cronograma, ejemplos

Fuente: docs/03_AI_MODELS.md (Agent 4), docs/04_ARCHITECTURE.md (Agents Layer)
"""
import structlog
# from crewai import Agent, Task  # CrewAI removed - using LangGraph only
from typing import Dict, Any, Optional

from config.settings import settings
from tools import get_scraping_tool, get_database_tool

logger = structlog.get_logger()


def create_implementation_specialist_agent() -> Agent:
    """
    Crea el agente ImplementationSpecialist.
    
    DeepSeek V3 es sorprendentemente bueno para planificación de código
    y es completamente gratuito.
    
    Returns:
        Agent: Instancia configurada del ImplementationSpecialist
    """
    # Obtener tools
    scraping_tool = get_scraping_tool()
    database_tool = get_database_tool()
    
    # Configurar LLM (Groq - LLaMA 3.3-70B GRATIS)
    llm_model = "groq/llama-3.3-70b-versatile"
    
    agent = Agent(
        role="Implementation Specialist & Developer Planner",
        
        goal="""Crear plan de implementación detallado para el niche objetivo:
        1. Desglosar arquitectura en tareas implementables (Jira-style)
        2. Identificar librerías, paquetes y herramientas específicas
        3. Generar cronograma realista (semanas, sprints)
        4. Evaluar complejidad de cada tarea (story points)
        5. Proveer code snippets de referencia (proof-of-concept)
        6. Documentar setup instructions (repo setup, env, CI/CD)
        """,
        
        backstory="""Eres un tech lead senior con 15+ años implementando sistemas complejos.
        
        Tu expertise:
        - Planificación ágil: sprints, user stories, story points
        - Evaluación de complejidad: T-shirt sizing, Fibonacci estimation
        - Selección de librerías: análisis de GitHub stars, NPM downloads, mantenimiento
        - Resolución de problemas: debugging, profiling, optimización
        - Best practices: clean code, SOLID, testing, documentation
        - Tooling: conoces TODAS las herramientas (CLI, IDEs, debuggers)
        
        Tu proceso:
        1. **Leer Arquitectura**: Entiendes componentes y sus relaciones
        2. **Descomponer**: Conviertes componentes en user stories
        3. **Investigar**: Buscas librerías/tools en GitHub, NPM, PyPI
        4. **Estimar**: Asignas story points (Fibonacci: 1,2,3,5,8,13)
        5. **Planificar**: Organizas en sprints de 2 semanas
        6. **Documentar**: Setup instructions, ejemplos, troubleshooting
        
        Principios:
        - **Pragmatismo**: MVP primero, optimización después
        - **Dependencies primero**: Setup básico antes de features
        - **Test desde día 1**: TDD cuando sea posible
        - **Documentación continua**: README, ADRs, inline comments
        - **Incremental delivery**: Funcionalidad completa cada sprint
        
        IMPORTANTE:
        - Estima de forma REALISTA (no optimista)
        - Considera deuda técnica y refactorings
        - Buffer de 20% para imprevistos
        - Identifica riesgos técnicos temprano
        """,
        
        tools=[
            # Web scraping para buscar librerías y ejemplos
            scraping_tool.scrape_website,
            scraping_tool.scrape_multiple_urls,
            
            # Database para consultar papers técnicos
            database_tool.query_papers,
            database_tool.get_paper_by_id,
        ],
        
        llm=llm_model,
        
        verbose=True,
        memory=True,
        allow_delegation=False,
        max_iter=15,
        max_rpm=100,  # DeepSeek free tier es generoso
    )
    
    logger.info(
        "implementation_specialist_created",
        model="deepseek-v3",
        fallback="claude-haiku-4.5",
        tools_count=4,
        estimated_duration="7-8 minutes",
    )
    
    return agent


def create_implementation_plan_task(
    agent: Agent,
    niche: str,
    architecture_context: Optional[Task] = None
) -> Task:
    """
    Crea la tarea de planificación de implementación.
    
    Args:
        agent: Instancia del ImplementationSpecialist
        niche: Nombre del niche
        architecture_context: Task del TechnicalArchitect
    
    Returns:
        Task: Tarea configurada con descripción y output esperado
    """
    task = Task(
        description=(
            """
            Crea plan de implementación detallado para "__NICHE__".
            
            Recibes del TechnicalArchitect:
            - Componentes y sus responsabilidades
            - Stack tecnológico (lenguajes, frameworks, DBs)
            - APIs y contratos
            - Diagramas de arquitectura
            
            **FASE 1: Investigación de Herramientas (2-3 minutos)**
            
            PASO 1.1: Identificar Librerías (2 min)
            - Para cada tecnología del stack, busca librerías top:
              Ejemplo para Rust + WASM:
              - GitHub: "https://github.com/search?q=rust+wasm+library&type=repositories"
              - Crates.io: scrape popular crates
            
            - Criterios de selección:
              a) Stars/downloads (popularidad)
              b) Última actualización (mantenimiento activo)
              c) Issues abiertos vs cerrados (salud del proyecto)
              d) Licencia (MIT, Apache 2.0 preferible)
              e) Documentación (README quality)
            
            PASO 1.2: Buscar Ejemplos (1 min)
            - Busca repos similares al proyecto:
              "https://github.com/search?q=__NICHE__+example&type=repositories"
            - Identifica: ¿Qué structure usan? ¿Qué patterns?
            - Extrae: Code snippets útiles, setup scripts
            
            **FASE 2: Descomposición en Tareas (3-4 minutos)**
            
            PASO 2.1: Crear User Stories (2 min)
            - Para cada componente de la arquitectura, genera 2-5 user stories
            - Formato:
              ```
              US-001: Setup proyecto base
              Como: Developer
              Quiero: Inicializar repo con estructura básica
              Para: Empezar desarrollo
              
              Acceptance Criteria:
              - [ ] Repo creado en GitHub
              - [ ] README con setup instructions
              - [ ] CI/CD configurado (tests, lint)
              - [ ] Docker Compose para local dev
              
              Story Points: 3
              Dependencies: None
              ```
            
            PASO 2.2: Estimar Complejidad (1 min)
            - Asigna story points (Fibonacci: 1,2,3,5,8,13)
            - 1 = Trivial (1-2 horas)
            - 2 = Simple (medio día)
            - 3 = Moderado (1 día)
            - 5 = Complejo (2-3 días)
            - 8 = Muy complejo (1 semana)
            - 13 = Épica (descomponer)
            
            PASO 2.3: Identificar Dependencies (1 min)
            - Qué tareas bloquean a otras
            - Crear dependency graph:
              ```
              US-001 (Setup) → US-002 (Core Logic)
              US-002 → US-003 (API)
              US-003 → US-004 (Testing)
              ```
            
            **FASE 3: Cronograma y Recursos (2 minutos)**
            
            PASO 3.1: Organizar en Sprints (1 min)
            - Sprint 1-2 (4 weeks): MVP
            - Sprint 3-4 (4 weeks): Features core
            - Sprint 5-6 (4 weeks): Optimización + docs
            
            - Velocity: ~20-30 story points/sprint (1 dev)
            
            PASO 3.2: Identificar Recursos (1 min)
            - Tutoriales útiles (links)
            - Docs oficiales (links)
            - Stack Overflow threads (para problemas comunes)
            - Discord/Slack communities (soporte)
            """
        ).replace("__NICHE__", niche),

        expected_output=(
            """
            # Plan de Implementación: __NICHE__
            
            ## 1. Resumen Ejecutivo
            - **Duración estimada**: X semanas (Y sprints)
            - **Complejidad total**: Z story points
            - **Team size recomendado**: N developers
            - **Riesgos principales**: [Top 3 riesgos técnicos]
            
            ## 2. Stack Tecnológico Detallado
            ### Lenguajes y Versiones
            - **[Lenguaje 1]**: vX.Y.Z (porque...)
            - **[Lenguaje 2]**: vX.Y.Z
            
            ### Librerías y Frameworks (con justificación)
            #### Core Dependencies
            - **[Librería 1]**: vX.Y
              - GitHub: [link] | Stars: XXX | Last update: YYYY-MM-DD
              - Por qué: [Razón técnica]
              - Alternativas: [Lib alternativa] (rechazada porque...)
            
            - **[Librería 2]**: vX.Y
              [Misma estructura]
            
            #### Development Dependencies
            - **Testing**: [Framework] (ej: pytest, jest)
            - **Linting**: [Tool] (ej: ruff, eslint)
            - **Formatting**: [Tool] (ej: black, prettier)
            - **Type checking**: [Tool] (ej: mypy, TypeScript)
            
            ### Tooling
            - **Package manager**: [npm, pip, cargo]
            - **Build tool**: [webpack, vite, cargo]
            - **Task runner**: [make, just, npm scripts]
            - **Container**: Docker + Docker Compose
            
            ## 3. Setup del Proyecto
            ### Estructura de Directorios
            ```
            project-name/
            ├── src/
            │   ├── component1/
            │   ├── component2/
            │   └── main.{{ext}}
            ├── tests/
            │   ├── unit/
            │   └── integration/
            ├── docs/
            ├── scripts/
            ├── docker/
            ├── .github/
            │   └── workflows/
            ├── Dockerfile
            ├── docker-compose.yml
            ├── README.md
            ├── Makefile
            └── [package.json / Cargo.toml / pyproject.toml]
            ```
            
            ### Setup Instructions (copy-paste ready)
            ```bash
            # 1. Clone repo
            git clone https://github.com/user/project-name.git
            cd project-name
            
            # 2. Install dependencies
            [comando específico: npm install, pip install -r requirements.txt, etc.]
            
            # 3. Setup environment
            cp .env.example .env
            # Edit .env con tus credenciales
            
            # 4. Run development server
            docker-compose up -d
            [comando para iniciar: npm run dev, cargo run, etc.]
            
            # 5. Run tests
            [comando de tests: npm test, pytest, cargo test]
            ```
            
            ## 4. User Stories y Tareas
            ### Epic 1: Project Setup & Infrastructure
            #### US-001: Inicializar Repositorio
            - **Como**: Developer
            - **Quiero**: Setup inicial del proyecto
            - **Para**: Empezar desarrollo
            - **Story Points**: 3
            - **Dependencies**: None
            - **Acceptance Criteria**:
              - [ ] Repo en GitHub con README
              - [ ] .gitignore configurado
              - [ ] LICENSE (MIT/Apache 2.0)
              - [ ] Estructura de directorios
              - [ ] package.json / Cargo.toml / pyproject.toml
            
            #### US-002: Configurar CI/CD
            - **Story Points**: 5
            - **Dependencies**: US-001
            - **Acceptance Criteria**:
              - [ ] GitHub Actions workflow
              - [ ] Tests automáticos en PRs
              - [ ] Lint + format check
              - [ ] Build Docker image
              - [ ] Deploy a staging (opcional)
            
            #### US-003: Setup Docker Development Environment
            - **Story Points**: 3
            - **Dependencies**: US-001
            - **Acceptance Criteria**:
              - [ ] Dockerfile multi-stage
              - [ ] docker-compose.yml con servicios
              - [ ] Hot reload configurado
              - [ ] DB seed data (si aplica)
            
            ### Epic 2: Core Components
            #### US-004: Implementar [Componente 1]
            - **Story Points**: 8
            - **Dependencies**: US-001, US-003
            - **Acceptance Criteria**:
              - [ ] Código funcional con tests
              - [ ] API definida (si aplica)
              - [ ] Documentación inline
              - [ ] Error handling
            - **Code Example**:
              ```[lenguaje]
              // Ejemplo de referencia (estructura básica)
              [código de ejemplo]
              ```
            
            #### US-005: Implementar [Componente 2]
            [Misma estructura]
            
            [Continuar para TODOS los componentes]
            
            ### Epic 3: Integration & Testing
            #### US-0XX: Integration Tests
            - **Story Points**: 5
            - **Dependencies**: [US de componentes]
            - **Acceptance Criteria**:
              - [ ] Test de flujo completo
              - [ ] Fixtures/mocks configurados
              - [ ] Coverage >80%
            
            #### US-0XX: Performance Testing
            - **Story Points**: 3
            - **Tools**: k6, Locust
            
            ### Epic 4: Documentation & Deployment
            #### US-0XX: Documentation
            - **Story Points**: 5
            - **Deliverables**:
              - [ ] README completo
              - [ ] API docs (Swagger/OpenAPI)
              - [ ] Architecture Decision Records (ADRs)
              - [ ] Deployment guide
            
            ## 5. Cronograma (Sprints)
            ### Sprint 1 (Semanas 1-2) - Foundation
            - US-001: Setup repo (3 pts)
            - US-002: CI/CD (5 pts)
            - US-003: Docker (3 pts)
            - US-004: Componente core 1 (8 pts)
            - **Total**: 19 story points
            - **Goal**: Proyecto inicializado, CI/CD funcionando, 1 componente MVP
            
            ### Sprint 2 (Semanas 3-4) - Core Features
            - US-005: Componente 2 (8 pts)
            - US-006: Componente 3 (5 pts)
            - US-007: API básica (5 pts)
            - **Total**: 18 story points
            - **Goal**: Componentes core completos, APIs funcionando
            
            ### Sprint 3 (Semanas 5-6) - Integration
            - US-008: Component integration (5 pts)
            - US-009: DB setup (3 pts)
            - US-010: Auth (5 pts)
            - US-011: Error handling (3 pts)
            - **Total**: 16 story points
            - **Goal**: Sistema integrado end-to-end
            
            ### Sprint 4 (Semanas 7-8) - Testing & Optimization
            - US-012: Unit tests completos (5 pts)
            - US-013: Integration tests (5 pts)
            - US-014: Performance optimization (5 pts)
            - US-015: Docs (5 pts)
            - **Total**: 20 story points
            - **Goal**: Sistema testeado, optimizado, documentado
            
            ## 6. Code Examples y Referencias
            ### Setup Script (Makefile)
            ```makefile
            .PHONY: install dev test lint build docker-up docker-down
            
            install:
                [comando para instalar deps]
            
            dev:
                [comando para iniciar dev server]
            
      test:
        [comando para correr tests]
            
      lint:
        [comando para lint]
            
      build:
        [comando para build production]
            
      docker-up:
        docker-compose up -d
            
      docker-down:
        docker-compose down
      ```
            
      ### Component Template
      ```[lenguaje]
      // Ejemplo de estructura básica para componentes
      [código template con comentarios explicativos]
      ```

      ### Test Template
      ```[lenguaje]
      // Ejemplo de test unitario
      [código test template]
      ```

      ## 7. Recursos y Referencias
      ### Tutoriales Recomendados
      - **[Tutorial 1]**: [Link] - [Qué cubre]
      - **[Tutorial 2]**: [Link] - [Qué cubre]

      ### Documentación Oficial
      - **[Framework 1]**: [Docs link]
      - **[Librería 1]**: [Docs link]

      ### Repos de Referencia
      - **[Repo 1]**: [Link] - [Por qué es útil]
      - **[Repo 2]**: [Link] - [Por qué es útil]

      ### Communities y Soporte
      - **Discord**: [Link a servidor]
      - **Stack Overflow**: [Tags relevantes]
            - **Reddit**: [Subreddit]

            ## 8. Riesgos Técnicos e Mitigaciones
            ### Riesgo 1: [Descripción]
            - **Probabilidad**: Alta | Media | Baja
            - **Impacto**: Alto | Medio | Bajo
            - **Mitigación**: [Qué hacer]
            - **Plan B**: [Alternativa si falla]

            ### Riesgo 2: [Descripción]
            [Misma estructura]

            ## 9. Definition of Done (DoD)
            Para considerar una user story "DONE":
            - [ ] Código implementado y funcional
            - [ ] Tests escritos (unit + integration)
            - [ ] Code review aprobado
            - [ ] Documentación actualizada
            - [ ] CI/CD pasa (green build)
            - [ ] Sin deuda técnica conocida
            - [ ] Deployed a staging (si aplica)

            ## 10. KPIs del Proyecto
            - **Velocity promedio**: X story points/sprint
            - **Bug rate**: < Y bugs/sprint
            - **Test coverage**: > 80%
            - **Build time**: < Z minutos
            - **Deploy frequency**: Diario (a staging)

            ## 11. Recomendaciones para ContentSynthesizer
            - **Highlights técnicos**: [Decisiones clave para mencionar en report]
            - **Achievements**: [Qué es innovador vs papers]
            - **Trade-offs tomados**: [Decisiones importantes con justificación]
            - **Next steps**: [Qué falta para v1.0, v2.0]
            """
        ).replace("__NICHE__", niche),

        agent=agent,

        context=[architecture_context] if architecture_context else [],
    )


    logger.info(
        "implementation_plan_task_created",
        niche=niche,
        expected_duration="7-8 minutes",
        tools_used=["scraping_tool (2)", "database_tool (2)"],
    )
    
    return task


def create_implementation_specialist(
    niche: str,
    architecture_task: Optional[Task] = None
) -> tuple[Agent, Task]:
    """Helper para crear el ImplementationSpecialist."""
    agent = create_implementation_specialist_agent()
    task = create_implementation_plan_task(agent, niche, architecture_task)
    return agent, task
