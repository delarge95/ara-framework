# 🛠️ Plan Técnico de Implementación - Marco ARA

## Stack Tecnológico Completo

### Core Framework & Orchestration

```yaml
Python: 3.12+
  Justificación: Type hints avanzados, mejor performance, async/await mejorado

LangGraph: ^0.2.0
LangChain: ^0.3.0
  Justificación: Framework líder para multi-agentes, proceso secuencial robusto
  Alternativa evaluada: AutoGen (descartado por ser demasiado conversacional)

LangChain: ^0.1.0 (opcional)
  Justificación: Herramientas adicionales para manejo de prompts y chains
```

### MCP Servers (Microservices de Herramientas)

```yaml
FastAPI: ^0.109.0
  Justificación: Alto performance, async nativo, auto-documentación OpenAPI

uvicorn: ^0.27.0
  Justificación: ASGI server de referencia para FastAPI

pydantic: ^2.5.0
  Justificación: Validación de datos, models para APIs
```

### Web Scraping & Automation

```yaml
Playwright: ^1.40.0
  Justificación: Superior a Selenium, maneja JS moderno, API testing incluido
  Alternativa: BeautifulSoup (no suficiente para sitios dinámicos)

httpx: ^0.26.0
  Justificación: Cliente HTTP async para API testing
```

### Academic Search & PDF Processing

```yaml
semanticscholar: ^0.8.0
  Justificación: Wrapper oficial para Semantic Scholar API, 45M+ papers

arxiv: ^2.1.0
  Justificación: Cliente oficial para ArXiv API, papers pre-print

unstructured: ^0.11.0
  Justificación: Mejor herramienta para PDFs complejos (multi-columna)
  Incluye: pdf2image, poppler, tesseract para OCR

PyPDF2: ^3.0.0
  Justificación: Fallback para PDFs simples
```

### 3D Graphics & Blender Control

```yaml
pyzmq: ^25.1.0
  Justificación: Protocolo ZMQ para comunicación con Blender

bpy: (viene con Blender)
  Justificación: API de Python para Blender, permite scripting completo

TripoSR: (instalación manual)
  Justificación: State-of-the-art para reconstrucción 3D desde imagen única
  GitHub: VAST-AI-Research/TripoSR
```

### LLM & AI Models

```yaml
openai: ^1.10.0
  Justificación: Acceso a GPT-4, GPT-3.5-turbo para agentes

anthropic: ^0.8.0
  Justificación: Acceso a Claude (alternativa a GPT)

transformers: ^4.36.0
  Justificación: Acceso a modelos open-source (Mistral, Llama)

torch: ^2.1.0
  Justificación: Backend para modelos locales

sentence-transformers: ^2.2.0
  Justificación: Embeddings para semantic search local
```

### Testing & Quality

```yaml
pytest: ^7.4.0
  Justificación: Framework de testing estándar

pytest-asyncio: ^0.21.0
  Justificación: Testing de código async

pytest-cov: ^4.1.0
  Justificación: Reportes de cobertura

httpx: ^0.26.0
  Justificación: Testing de endpoints FastAPI
```

### Code Quality

```yaml
ruff: ^0.1.0
  Justificación: Linter ultrarrápido (reemplaza flake8, isort, pylint)

black: ^23.12.0
  Justificación: Formatter estándar de Python

mypy: ^1.8.0
  Justificación: Type checking estático

pre-commit: ^3.6.0
  Justificación: Hooks para calidad automática
```

### Logging & Monitoring

```yaml
structlog: ^24.1.0
  Justificación: Logging estructurado JSON

rich: ^13.7.0
  Justificación: Output bonito en terminal para debugging
```

### Optional: Caching & Persistence

```yaml
redis: ^5.0.0
  Justificación: Caching de resultados de búsquedas académicas

sqlalchemy: ^2.0.0
  Justificación: ORM para metadatos de tesis generadas
```

---

## Arquitectura del Sistema

### Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                               │
│                    (CLI / Web Dashboard)                             │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     ORCHESTRATION LAYER                              │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                   LangGraph StateGraph                        │  │
│  │  - Process: Sequential                                        │  │
│  │  - Manager: ProjectManager Agent                              │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌─────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐│
│  │ Niche   │  │ Literature   │  │ Technical    │  │ Content      ││
│  │ Analyst │  │ Researcher   │  │ Architect    │  │ Synthesizer  ││
│  │ Agent   │  │ Agent        │  │ Agent        │  │ Agent        ││
│  └────┬────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘│
└───────┼──────────────┼──────────────────┼──────────────────┼────────┘
        │              │                  │                  │
        │ HTTP REST    │ HTTP REST        │ HTTP REST        │
        ▼              ▼                  ▼                  ▼
┌────────────────────────────────────────────────────────────────────┐
│                      MCP SERVERS LAYER                              │
│                    (FastAPI Microservices)                          │
│                                                                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────────┐  │
│  │ WebScraping     │  │ PDF Ingestion   │  │ Blender Control  │  │
│  │ MCP Server      │  │ MCP Server      │  │ MCP Server       │  │
│  │                 │  │                 │  │                  │  │
│  │ Port: 8001      │  │ Port: 8002      │  │ Port: 8003       │  │
│  │                 │  │                 │  │                  │  │
│  │ - /search       │  │ - /process_pdf  │  │ - /load_model    │  │
│  │ - /product_det. │  │ - /extract_text │  │ - /create_mat.   │  │
│  │ - /reviews      │  │ - /summarize    │  │ - /render        │  │
│  │ - /scan_feature │  │                 │  │                  │  │
│  └────────┬────────┘  └────────┬────────┘  └────────┬─────────┘  │
└───────────┼────────────────────┼─────────────────────┼────────────┘
            │                    │                     │
            ▼                    ▼                     ▼
┌────────────────────────────────────────────────────────────────────┐
│                    EXTERNAL TOOLS LAYER                             │
│                                                                     │
│  ┌──────────────┐  ┌────────────────┐  ┌──────────────────────┐  │
│  │ Playwright   │  │ Unstructured.io│  │ Blender + ZMQ        │  │
│  │ Browser      │  │ PDF Parser     │  │ (Headless)           │  │
│  └──────────────┘  └────────────────┘  └──────────────────────┘  │
│                                                                     │
│  ┌──────────────┐  ┌────────────────┐  ┌──────────────────────┐  │
│  │ Semantic     │  │ ArXiv API      │  │ TripoSR              │  │
│  │ Scholar API  │  │                │  │ (3D Generation)      │  │
│  └──────────────┘  └────────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
            │                    │                     │
            ▼                    ▼                     ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      DATA LAYER (Optional)                           │
│                                                                      │
│  ┌─────────────────┐              ┌──────────────────────┐         │
│  │ Redis Cache     │              │ PostgreSQL           │         │
│  │ (Search Results)│              │ (Thesis Metadata)    │         │
│  └─────────────────┘              └──────────────────────┘         │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Estructura de Directorios Detallada

```
ara_framework/
│
├── agents/                          # Definiciones de agentes (legacy)
│   ├── __init__.py
│   ├── project_manager.py           # Orquestador principal
│   ├── niche_analyst.py             # Análisis de mercado
│   ├── literature_researcher.py     # Revisión de literatura
│   ├── technical_architect.py       # Diseño técnico
│   ├── implementation_specialist.py # Tareas de desarrollo
│   └── content_synthesizer.py       # Ensamblaje final
│
├── mcp_servers/                     # Servidores FastAPI (herramientas)
│   ├── __init__.py
│   │
│   ├── webscraping/                 # MCP Server 1: Web Scraping
│   │   ├── __init__.py
│   │   ├── server.py                # FastAPI app
│   │   ├── scrapers.py              # Lógica de Playwright
│   │   ├── models.py                # Pydantic models
│   │   └── config.py                # Configuración
│   │
│   ├── pdf_ingestion/               # MCP Server 2: PDF Processing
│   │   ├── __init__.py
│   │   ├── server.py
│   │   ├── processor.py             # Unstructured.io logic
│   │   ├── models.py
│   │   └── config.py
│   │
│   └── blender_control/             # MCP Server 3: Blender Control
│       ├── __init__.py
│       ├── server.py                # FastAPI app
│       ├── blender_client.py        # ZMQ client
│       ├── blender_script.py        # Script que corre en Blender
│       ├── models.py
│       └── config.py
│
├── tools/                           # Herramientas para agentes
│   ├── __init__.py
│   ├── academic_search.py           # Semantic Scholar + ArXiv
│   ├── webscraping_tool.py          # Cliente HTTP para MCP Server
│   ├── pdf_tool.py                  # Cliente HTTP para MCP Server
│   ├── blender_tool.py              # Cliente HTTP para MCP Server
│   ├── filesystem_tool.py           # Operaciones de archivos
│   └── code_execution_tool.py       # Ejecución de código
│
├── config/                          # Configuración centralizada
│   ├── __init__.py
│   ├── agents_config.yaml           # Definición de agentes
│   ├── crew_config.yaml             # Definición del crew
│   ├── llm_config.yaml              # Configuración de LLMs
│   └── mcp_servers_config.yaml      # Puertos y endpoints
│
├── core/                            # Lógica de negocio central
│   ├── __init__.py
│   ├── orchestrator.py              # Pipeline principal
│   ├── task_manager.py              # Gestión de tareas
│   └── validators.py                # Validación de calidad
│
├── outputs/                         # Resultados generados
│   ├── theses/                      # Tesis completas
│   ├── assets/                      # Imágenes, modelos 3D
│   ├── reports/                     # Reportes de ejecución
│   └── logs/                        # Logs estructurados
│
├── tests/                           # Suite de tests
│   ├── unit/
│   │   ├── test_agents/
│   │   ├── test_tools/
│   │   └── test_mcp_servers/
│   ├── integration/
│   │   ├── test_webscraping_api.py
│   │   ├── test_pdf_ingestion_api.py
│   │   └── test_blender_control_api.py
│   └── e2e/
│       └── test_thesis_generation_pipeline.py
│
├── docs/                            # Documentación
│   ├── PROJECT_CONSTITUTION.md      # ✅ CREADO
│   ├── PROJECT_SPEC.md              # ✅ CREADO
│   ├── TECHNICAL_PLAN.md            # ✅ ESTE ARCHIVO
│   ├── API_REFERENCE.md             # Documentación de APIs
│   └── DEPLOYMENT.md                # Guía de despliegue
│
├── scripts/                         # Scripts de utilidad
│   ├── start_mcp_servers.sh         # Inicia todos los servidores
│   ├── run_pipeline.py              # Ejecuta pipeline completo
│   └── setup_environment.py         # Configuración inicial
│
├── docker/                          # Containerización
│   ├── Dockerfile.webscraping       # Para WebScraping MCP
│   ├── Dockerfile.pdf               # Para PDF Ingestion MCP
│   ├── Dockerfile.blender           # Para Blender Control MCP
│   └── docker-compose.yml           # Orquestación local
│
├── .env.example                     # Template de variables de entorno
├── .gitignore
├── pyproject.toml                   # Configuración de proyecto (Poetry)
├── requirements.txt                 # Dependencias (pip)
├── requirements-dev.txt             # Dependencias de desarrollo
└── README.md                        # Documentación principal
```

---

## Decisiones Arquitectónicas Clave

### 1. ¿Por qué FastAPI para MCP Servers?

**Alternativas Consideradas**:

- Flask: Más simple pero sin async nativo
- gRPC: Más rápido pero mayor complejidad
- Direct Function Calls: Acoplamiento alto

**Decisión**: FastAPI

- ✅ Performance: Async nativo, comparable a Node.js
- ✅ Developer Experience: Auto-documentación OpenAPI
- ✅ Type Safety: Validación con Pydantic
- ✅ Ecosystem: Gran adopción, muchas integraciones

### 2. ¿Por qué CrewAI sobre AutoGen?

**Comparación**:
| Aspecto | CrewAI | AutoGen |
|---------|--------|---------|
| Modelo | Orientado a roles | Conversacional |
| Flujo | Secuencial/Jerárquico | Chat-based negotiation |
| Determinismo | Alto | Medio-Bajo |
| Curva de aprendizaje | Baja | Alta |
| Caso de uso | Workflows estructurados | Investigación abierta |

**Decisión**: CrewAI

- ✅ Generación de tesis es un workflow estructurado
- ✅ Mayor reproducibilidad
- ✅ Desarrollo más rápido

### 3. ¿Por qué Playwright sobre Selenium?

**Comparación**:

- Playwright: Moderno, API async, mejor para SPAs
- Selenium: Más antiguo, API síncrona, menos robusto

**Decisión**: Playwright

- ✅ Mejor manejo de JS moderno (React, Vue, etc.)
- ✅ API para testing (APIRequestContext)
- ✅ Auto-waiting inteligente

### 4. ¿Por qué Unstructured.io para PDFs?

**Alternativas**:

- PyPDF2: Solo texto simple
- pdfplumber: Mejor para tablas
- Camelot: Especializado en tablas

**Decisión**: Unstructured.io

- ✅ Maneja layouts complejos (multi-columna)
- ✅ Salida estructurada (JSON)
- ✅ Detecta elementos (títulos, párrafos, tablas)

### 5. ¿Proceso Secuencial o Jerárquico?

**Opciones**:

- Secuencial: Agentes ejecutan en orden fijo
- Jerárquico: Manager asigna tareas dinámicamente

**Decisión**: Secuencial (inicial)

- ✅ Generación de tesis tiene orden lógico
- ✅ Más predecible y debuggeable
- ✅ Puede evolucionar a jerárquico después

---

## Pipeline de Datos

### Fase 1: Problem Discovery

```
INPUT: Domain + Keywords
    ↓
[NicheAnalyst Agent]
    ↓
  ┌─────────────────────────────┐
  │ WebScraping MCP Server      │
  │  - Playwright scraping      │
  │  - Product data extraction  │
  │  - Review sentiment analysis│
  └─────────────────────────────┘
    ↓
OUTPUT: JSON structured report
{
  "problem_statement": "...",
  "market_gap": "...",
  "justification": "...",
  "data_sources": [...]
}
```

### Fase 2: Literature Review

```
INPUT: Keywords + Problem Context
    ↓
[LiteratureResearcher Agent]
    ↓
  ┌─────────────────────────────┐
  │ Academic Search Tools       │
  │  - Semantic Scholar API     │
  │  - ArXiv API                │
  └─────────────────────────────┘
    ↓ (list of paper URLs)
  ┌─────────────────────────────┐
  │ PDF Ingestion MCP Server    │
  │  - Download PDFs            │
  │  - Extract structured text  │
  │  - Summarize with LLM       │
  └─────────────────────────────┘
    ↓
[Thematic Analysis with LLM]
    ↓
OUTPUT: JSON literature review
{
  "papers": [...],
  "theoretical_frameworks": [...],
  "methodologies": [...],
  "research_gaps": [...]
}
```

### Fase 3: Technical Specification

```
INPUT: Problem + Literature Context
    ↓
[TechnicalArchitect Agent]
    ↓
  ┌─────────────────────────────┐
  │ Code Repository Search      │
  │  - GitHub API               │
  │  - Tech stack analysis      │
  └─────────────────────────────┘
    ↓
[Architecture Design with LLM]
    ↓
OUTPUT: JSON technical spec
{
  "tech_stack": {...},
  "architecture": {...},
  "components": [...],
  "implementation_plan": [...]
}
```

### Fase 4: Asset Generation

```
INPUT: Technical Spec + Asset Requirements
    ↓
[ImplementationSpecialist Agent]
    ↓
  ┌─────────────────────────────┐
  │ Blender Control MCP Server  │
  │  - Load models              │
  │  - Apply materials (PBR)    │
  │  - Render scenes            │
  └─────────────────────────────┘
    ↓
OUTPUT: Visual assets (PNG, GLB)
```

### Fase 5: Document Synthesis

```
INPUT: All previous outputs
    ↓
[ContentSynthesizer Agent]
    ↓
[Document Assembly Pipeline]
  - Markdown generation
  - LaTeX conversion
  - Citation formatting
  - Image embedding
    ↓
OUTPUT: Complete thesis document (PDF/DOCX)
```

---

## Configuración de LLMs

### Estrategia de Modelos

```yaml
# Configuración por agente
agents:
  NicheAnalyst:
    model: gpt-4-turbo
    reasoning: Necesita razonamiento profundo para análisis

  LiteratureResearcher:
    model: gpt-4-turbo
    reasoning: Debe entender contexto académico complejo

  TechnicalArchitect:
    model: gpt-4-turbo
    reasoning: Decisiones técnicas críticas

  ContentSynthesizer:
    model: gpt-3.5-turbo
    reasoning: Tarea más de edición que razonamiento

# Alternativa open-source (para reducir costos)
alternative_stack:
  - model: mistral-large
    provider: together.ai
    cost: 80% más barato que GPT-4

  - model: mixtral-8x7b
    provider: local (GPU)
    cost: $0
    trade_off: Menor calidad, mayor latencia
```

### Estimación de Costos

```
Suponiendo uso de OpenAI:

Fase 1 (NicheAnalyst):
  - Input: ~5K tokens
  - Output: ~2K tokens
  - Costo: $0.15

Fase 2 (LiteratureResearcher):
  - Input: ~50K tokens (15 papers x 3K tokens each)
  - Output: ~10K tokens
  - Costo: $1.50

Fase 3 (TechnicalArchitect):
  - Input: ~10K tokens
  - Output: ~5K tokens
  - Costo: $0.30

Fase 5 (ContentSynthesizer):
  - Input: ~30K tokens
  - Output: ~15K tokens
  - Costo: $0.45 (usando GPT-3.5)

TOTAL por tesis: ~$2.40

Para reducir costos:
- Usar Mixtral-8x7b local: $0
- Usar Claude 3 Haiku: ~$0.80/tesis
```

---

## Despliegue y Escalabilidad

### Desarrollo Local

```bash
# 1. Setup environment
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# 2. Configurar variables de entorno
copy .env.example .env
# Editar .env con API keys

# 3. Iniciar MCP Servers
cd mcp_servers/webscraping
uvicorn server:app --port 8001 &

cd ../pdf_ingestion
uvicorn server:app --port 8002 &

cd ../blender_control
uvicorn server:app --port 8003 &

# 4. Ejecutar pipeline
python scripts/run_pipeline.py --domain "Marketing digital" --brand "Absolut"
```

### Dockerización

```yaml
# docker-compose.yml
version: "3.8"

services:
  webscraping-mcp:
    build:
      context: .
      dockerfile: docker/Dockerfile.webscraping
    ports:
      - "8001:8001"
    environment:
      - PLAYWRIGHT_BROWSERS_PATH=/browsers
    volumes:
      - ./outputs:/app/outputs

  pdf-ingestion-mcp:
    build:
      context: .
      dockerfile: docker/Dockerfile.pdf
    ports:
      - "8002:8002"
    volumes:
      - ./outputs:/app/outputs

  blender-control-mcp:
    build:
      context: .
      dockerfile: docker/Dockerfile.blender
    ports:
      - "8003:8003"
    volumes:
      - ./outputs/assets:/app/assets

  orchestrator:
    build: .
    depends_on:
      - webscraping-mcp
      - pdf-ingestion-mcp
      - blender-control-mcp
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - MCP_WEBSCRAPING_URL=http://webscraping-mcp:8001
      - MCP_PDF_URL=http://pdf-ingestion-mcp:8002
      - MCP_BLENDER_URL=http://blender-control-mcp:8003
    volumes:
      - ./outputs:/app/outputs
```

### Despliegue en Cloud (AWS/GCP)

```
┌──────────────────────────────────────────────────────┐
│                   Load Balancer                       │
└───────────────────┬──────────────────────────────────┘
                    │
        ┌───────────┼──────────┐
        ▼           ▼          ▼
┌─────────────┐ ┌────────┐ ┌────────┐
│ Orchestrator│ │  MCP   │ │  MCP   │
│  Container  │ │ Server │ │ Server │
│  (ECS/GKE)  │ │   1    │ │   2    │
└─────────────┘ └────────┘ └────────┘
        │
        ▼
┌─────────────────────────────┐
│  S3/Cloud Storage           │
│  (Outputs & Assets)         │
└─────────────────────────────┘
```

**Escalabilidad**:

- Horizontal: Múltiples instancias de orchestrator
- Vertical: GPU para LLMs locales
- Caching: Redis para búsquedas académicas
- Queue: RabbitMQ para cola de trabajos

---

## Métricas y Monitoreo

### Logging Estructurado

```python
import structlog

logger = structlog.get_logger()

# Ejemplo de uso en un agente
logger.info(
    "agent_task_started",
    agent="NicheAnalyst",
    task_id="task_001",
    domain="premium_spirits",
    timestamp=datetime.now().isoformat()
)

# Logs de performance
logger.info(
    "mcp_server_response",
    server="webscraping",
    endpoint="/search",
    response_time_ms=234,
    status_code=200
)
```

### Métricas a Trackear

```yaml
Performance:
  - Pipeline total execution time
  - Per-agent execution time
  - MCP server response times
  - LLM API latency
  - PDF processing time

Quality:
  - Number of papers retrieved
  - Citation accuracy rate
  - Section completeness percentage
  - Human validation score (1-10)

Cost:
  - LLM API costs per thesis
  - Compute costs (if using GPU)
  - Storage costs

Reliability:
  - Success rate (successful thesis generation %)
  - Retry attempts per component
  - Error rate by component
```

---

## Próximos Pasos de Implementación

### Sprint 1 (Semana 1-2): Fundamentos

- [ ] Setup de proyecto (venv, dependencies)
- [ ] Estructura de directorios completa
- [ ] Configuración de pre-commit hooks
- [ ] Implementar WebScraping MCP Server básico
- [ ] Tests unitarios para scraping

### Sprint 2 (Semana 3-4): MCP Servers Restantes

- [ ] Implementar PDF Ingestion MCP Server
- [ ] Implementar Blender Control MCP Server (básico)
- [ ] Tests de integración para todos los MCP servers
- [ ] Documentación de APIs (OpenAPI)

### Sprint 3 (Semana 5-6): Agentes Core

- [ ] Implementar NicheAnalyst Agent
- [ ] Implementar LiteratureResearcher Agent
- [ ] Tools para conectar agentes con MCP servers
- [ ] Tests E2E para Phase 1 y 2

### Sprint 4 (Semana 7-8): Agentes Técnicos

- [ ] Implementar TechnicalArchitect Agent
- [ ] Implementar ImplementationSpecialist Agent
- [ ] Integración con TripoSR (opcional)
- [ ] Pipeline de generación de activos 3D

### Sprint 5 (Semana 9-10): Síntesis y Orquestación

- [ ] Implementar ContentSynthesizer Agent
- [ ] Implementar ProjectManager orchestrator
- [ ] Pipeline completo de tesis
- [ ] Validación de calidad automatizada

### Sprint 6 (Semana 11-12): Refinamiento y Deploy

- [ ] Optimización de performance
- [ ] Dockerización completa
- [ ] Documentación final
- [ ] Demo en vivo con caso real

---

## 🔬 ACTUALIZACIÓN NOVIEMBRE 2025: Decisiones Técnicas Validadas

> **Fuente**: core_tech_stack_validation.md + agentic_editors_analysis.md + optimization_research.md + 05_ANALISIS_COMPARATIVO_3FUENTES.md  
> **Estado**: ✅ STACK VALIDADO CON 95% CONFIANZA

### 1. **LangGraph vs Alternativas: Decisión Fundamentada**

```yaml
framework_comparison:
  evaluated:
    - name: "LangGraph"
      version: "^0.70.0"
      strengths:
        - "Roles claros por agente (role-based)"
        - "Procesos secuenciales nativos"
        - "Delegation patterns (superior → subordinado)"
        - "Integración LangChain opcional"
        - "Menos overhead conversacional"
      weaknesses:
        - "Comunidad más pequeña vs LangChain"
        - "Menos ejemplos públicos"
      verdict: "✅ APROBADO"
      confidence: "90%"

    - name: "AutoGen (Microsoft)"
      version: "^0.2.0"
      strengths:
        - "Multi-modal nativo"
        - "Respaldo de Microsoft"
        - "Conversacional avanzado"
      weaknesses:
        - "❌ CRÍTICO: Overhead conversacional 10-15x tokens"
        - "Latencia alta en handoffs (500ms+)"
        - "Difícil control de flujo determinista"
      verdict: "❌ RECHAZADO"
      reason: "Overhead conversacional incompatible con presupuesto"

    - name: "LangGraph"
      version: "^0.1.0"
      strengths:
        - "Grafos de estado avanzados"
        - "Debugging visual"
        - "Checkpointing automático"
      weaknesses:
        - "Curva de aprendizaje alta"
        - "Overhead de configuración"
        - "No necesario para pipeline lineal"
      verdict: "⚠️ OVERKILL para MVP"
      reason: "Pipeline secuencial simple no necesita grafos complejos"

  final_decision:
    framework: "LangGraph"
    justification: |
      LangGraph es ÓPTIMO para este proyecto porque:
      1. StateGraph con checkpointing robusto (state persistence)
      2. Control granular del flujo (conditional edges, loops)
      3. LangChain ecosystem integration (tools, observability)
      4. Migrated from CrewAI for better Python 3.14+ compatibility
```

#### **LangGraph: Patrón de Implementación**

```python
# research_graph.py
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain.llms import ChatOpenAI

# Agente con rol específico
niche_analyst = Agent(
    role="Niche Analyst",
    goal="Identify profitable business opportunities in technical niche",
    backstory="Expert market researcher with 10+ years experience",
    llm=ChatOpenAI(model="gpt-4o"),  # GitHub Copilot Pro (0x credits)
    allow_delegation=False,  # No delegar, ejecutar directamente
    verbose=True
)

literature_researcher = Agent(
    role="Literature Researcher",
    goal="Gather and analyze academic papers relevant to niche",
    backstory="Academic researcher with access to Semantic Scholar",
    llm=ChatOpenAI(model="gemini-2.5-pro"),  # Free, 1M context
    allow_delegation=False,
    tools=[semantic_scholar_tool, arxiv_tool, jina_reader_tool]
)

# Tareas con artifacts explícitos
task_1 = Task(
    description="Analyze keywords: {keywords} and produce niche analysis",
    expected_output="JSON file with market analysis (niche_analysis.json)",
    agent=niche_analyst,
    output_file="outputs/niche_analysis.json"  # Artifact explícito
)

task_2 = Task(
    description="Using niche_analysis.json, find 10-50 relevant papers",
    expected_output="JSON file with paper metadata + summaries",
    agent=literature_researcher,
    output_file="outputs/literature_review.json",
    context=[task_1]  # Dependencia explícita
)

# StateGraph with sequential flow
workflow = StateGraph(ResearchState)
workflow.add_node("niche_analysis", niche_analyst_node)
workflow.add_node("literature_research", literature_research_node)
workflow.add_node("technical_architecture", technical_architect_node)

# Sequential edges
workflow.add_edge("niche_analysis", "literature_research")
workflow.add_edge("literature_research", "technical_architecture")
workflow.add_edge("technical_architecture", END)

workflow.set_entry_point("niche_analysis")

# Compile with checkpointing
graph = workflow.compile(checkpointer=MemorySaver())

# Execute pipeline with state persistence
result = await graph.ainvoke(
    {"keywords": ["AI", "3D", "startup"]},
    config={"configurable": {"thread_id": "analysis_001"}}
)
```

### 2. **FastAPI: Benchmarks y Justificación de Performance**

```yaml
fastapi_validation:
  benchmark_results:
    source: "TechEmpower Round 22 (Julio 2023)"

    frameworks_tested:
      fastapi:
        rps: "15,000-20,000 RPS (requests por segundo)"
        latency_p99: "< 50ms"
        async: "Nativo (uvloop)"
        verdict: "✅ HIGH PERFORMANCE"

      flask:
        rps: "2,000-3,000 RPS"
        latency_p99: "~200ms"
        async: "No nativo (requiere gevent/eventlet)"
        verdict: "❌ INSUFICIENTE para producción"

      django:
        rps: "1,500-2,500 RPS"
        latency_p99: "~250ms"
        async: "Parcial desde 3.0"
        verdict: "❌ OVERKILL (ORM no necesario)"

  decision:
    framework: "FastAPI"
    justification:
      - "8-10x más rápido que Flask"
      - "Async/await nativo (crítico para I/O-bound: Semantic Scholar 1 RPS)"
      - "Validación automática con Pydantic"
      - "OpenAPI auto-generado (documentación gratis)"
      - "WebSockets nativos (real-time updates frontend)"
```

#### **FastAPI: Patrones de Alto Rendimiento**

```python
# app/main.py
from fastapi import FastAPI, BackgroundTasks, WebSocket
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import asyncio

app = FastAPI(title="ARA Framework API", version="1.0.0")

# Request/Response models con validación
class AnalysisRequest(BaseModel):
    keywords: list[str]
    depth: str = "standard"  # standard | deep
    budget_max: float = 18.0

class AnalysisResponse(BaseModel):
    job_id: str
    status: str
    estimated_time_minutes: int

# Endpoint asíncrono con BackgroundTasks
@app.post("/api/v1/analyze", response_model=AnalysisResponse)
async def analyze_niche(request: AnalysisRequest, bg: BackgroundTasks):
    """Iniciar análisis de nicho (async, no bloqueante)"""
    job_id = generate_job_id()

    # Ejecutar pipeline en background
    bg.add_task(run_langgraph_pipeline, job_id, request)

    return AnalysisResponse(
        job_id=job_id,
        status="processing",
        estimated_time_minutes=65  # SLA realistic
    )

# WebSocket para updates en tiempo real
@app.websocket("/ws/{job_id}")
async def websocket_status(websocket: WebSocket, job_id: str):
    """Stream de status updates al frontend"""
    await websocket.accept()

    while True:
        status = await get_job_status(job_id)
        await websocket.send_json(status)

        if status["completed"]:
            break

        await asyncio.sleep(2)  # Poll cada 2 segundos

# Streaming de reporte grande (50-80 páginas)
@app.get("/api/v1/report/{job_id}/stream")
async def stream_report(job_id: str):
    """Stream reporte en chunks (no cargar 80 páginas en RAM)"""
    async def generate():
        async for chunk in read_report_chunks(job_id):
            yield chunk

    return StreamingResponse(
        generate(),
        media_type="text/markdown"
    )
```

#### **FastAPI: Configuración de Producción**

```python
# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API
    app_name: str = "ARA Framework"
    debug: bool = False

    # Database
    supabase_url: str
    supabase_key: str

    # Cache
    redis_url: str = "redis://localhost:6379/0"
    cache_ttl_niche: int = 86400  # 24 horas
    cache_ttl_papers: int = 604800  # 7 días

    # LLM APIs
    openai_api_key: str
    anthropic_api_key: str
    gemini_api_key: str
    minimax_api_key: str | None = None

    # Budget
    copilot_credits_monthly: int = 300
    copilot_credits_alert: int = 240  # Alertar si < 60 restantes

    # Performance
    worker_count: int = 4  # Uvicorn workers
    max_connections: int = 1000
    timeout_seconds: int = 180

    class Config:
        env_file = ".env"

settings = Settings()
```

### 3. **Playwright vs Selenium: Comparación Técnica**

```yaml
web_scraping_comparison:
  selenium:
    first_release: "2004"
    pros:
      - "Ecosistema maduro"
      - "Muchos tutoriales"
    cons:
      - "❌ No maneja bien SPAs modernas"
      - "❌ Requiere waits manuales (time.sleep)"
      - "❌ ChromeDriver separado (mantenimiento)"
      - "❌ No tiene auto-waiting inteligente"
      - "❌ API testing limitado"
    verdict: "❌ OBSOLETO para 2025"

  playwright:
    first_release: "2020 (Microsoft)"
    pros:
      - "✅ Auto-waiting inteligente (no más time.sleep)"
      - "✅ Multi-browser (Chromium, Firefox, WebKit)"
      - "✅ API testing nativo (request/response intercept)"
      - "✅ Maneja SPAs y sitios JS-heavy"
      - "✅ Drivers incluidos (auto-download)"
      - "✅ Modo headless rápido"
      - "✅ Screenshots y videos integrados"
    cons:
      - "Ecosistema más nuevo (menos Stack Overflow)"
    verdict: "✅ SUPERIOR para 2025"
    confidence: "95%"

  decision:
    tool: "Playwright"
    use_cases:
      - "Scraping de Google/Bing trends (SPAs)"
      - "Extracción de datos de sitios JS-heavy"
      - "Testing de frontend Next.js"
```

#### **Playwright: Implementación con Auto-Waiting**

```python
# tools/web_scraper.py
from playwright.async_api import async_playwright, Page
import asyncio

class PlaywrightScraper:
    """Web scraper con auto-waiting y stealth mode"""

    async def scrape_url(self, url: str) -> dict:
        """Scrape URL con manejo de SPAs"""
        async with async_playwright() as p:
            # Lanzar browser (headless para producción)
            browser = await p.chromium.launch(headless=True)

            # Crear contexto con stealth (anti-bot)
            context = await browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (compatible; ARA-Bot/1.0)"
            )

            page = await context.new_page()

            try:
                # Navegar con timeout inteligente
                await page.goto(url, wait_until="domcontentloaded")

                # Auto-waiting: esperar elemento clave
                await page.wait_for_selector("article", timeout=10000)

                # Extraer contenido (Playwright auto-espera)
                title = await page.title()
                content = await page.locator("article").inner_text()
                links = await page.locator("a[href]").all()

                return {
                    "url": url,
                    "title": title,
                    "content": content,
                    "links_count": len(links)
                }

            finally:
                await browser.close()

    async def scrape_multiple(self, urls: list[str]) -> list[dict]:
        """Scrape múltiples URLs en paralelo (respetando rate limit)"""
        tasks = [self.scrape_url(url) for url in urls]
        return await asyncio.gather(*tasks, return_exceptions=True)

# Integración con LangGraph
from langchain.tools import tool

@tool("web_scraper")
def web_scraper_tool(url: str) -> str:
    """Scrape URL and extract main content"""
    scraper = PlaywrightScraper()
    result = asyncio.run(scraper.scrape_url(url))
    return result["content"]
```

### 4. **Procesamiento de PDFs: Estrategia Híbrida**

```yaml
pdf_processing_strategy:
  evaluation:
    - library: "PyMuPDF (fitz)"
      speed: "⭐⭐⭐⭐⭐ (0.12s/página)"
      quality: "⭐⭐⭐ (básico, no semántico)"
      use_case: "PDFs simples, extracción rápida"
      verdict: "✅ PRIMARY para velocidad"

    - library: "Unstructured.io"
      speed: "⭐⭐ (1.29s/página, 10x más lento)"
      quality: "⭐⭐⭐⭐⭐ (semántico, multi-columna)"
      use_case: "PDFs complejos, papers académicos"
      verdict: "✅ SECONDARY para calidad"

    - library: "pdfplumber"
      speed: "⭐⭐⭐ (0.5s/página)"
      quality: "⭐⭐⭐⭐ (tablas bien)"
      use_case: "Extracción de tablas"
      verdict: "✅ TERTIARY para tablas"

  decision:
    strategy: "Cascading strategy (PyMuPDF → Unstructured → pdfplumber)"
    implementation:
      step_1: "Intentar PyMuPDF (rápido)"
      step_2: "Si falla o calidad baja → Unstructured"
      step_3: "Si tiene tablas complejas → pdfplumber"
```

#### **PDF Processing: Implementación Híbrida**

```python
# tools/pdf_processor.py
import fitz  # PyMuPDF
from unstructured.partition.pdf import partition_pdf
import pdfplumber
from typing import Literal

class HybridPDFProcessor:
    """Procesador de PDFs con estrategia en cascada"""

    async def process_pdf(
        self,
        pdf_path: str,
        strategy: Literal["fast", "quality", "auto"] = "auto"
    ) -> dict:
        """Procesar PDF con estrategia óptima"""

        if strategy == "auto":
            # Detectar complejidad del PDF
            complexity = await self._detect_complexity(pdf_path)
            strategy = "fast" if complexity == "simple" else "quality"

        if strategy == "fast":
            return await self._process_pymupdf(pdf_path)
        else:
            return await self._process_unstructured(pdf_path)

    async def _process_pymupdf(self, pdf_path: str) -> dict:
        """Extracción rápida con PyMuPDF"""
        doc = fitz.open(pdf_path)

        text = ""
        metadata = doc.metadata

        for page_num, page in enumerate(doc):
            text += page.get_text("text")  # 0.12s/página

        doc.close()

        return {
            "text": text,
            "metadata": metadata,
            "pages": len(doc),
            "processor": "pymupdf",
            "speed": "fast"
        }

    async def _process_unstructured(self, pdf_path: str) -> dict:
        """Extracción semántica con Unstructured"""
        elements = partition_pdf(
            filename=pdf_path,
            strategy="hi_res",  # Análisis profundo
            infer_table_structure=True
        )

        # Separar por tipo de elemento
        text_elements = [e for e in elements if e.category == "Text"]
        table_elements = [e for e in elements if e.category == "Table"]

        return {
            "text": "\n\n".join([e.text for e in text_elements]),
            "tables": [e.metadata.text_as_html for e in table_elements],
            "elements_count": len(elements),
            "processor": "unstructured",
            "speed": "quality"
        }

    async def _detect_complexity(self, pdf_path: str) -> str:
        """Detectar complejidad del PDF (rápido con PyMuPDF)"""
        doc = fitz.open(pdf_path)
        first_page = doc[0]

        # Criterios de complejidad
        text_blocks = len(first_page.get_text("blocks"))
        images = len(first_page.get_images())

        doc.close()

        # Simple: pocas columnas, sin imágenes
        if text_blocks < 10 and images == 0:
            return "simple"
        else:
            return "complex"
```

### 5. **3D Pipeline: Blender + TripoSR**

```yaml
3d_generation_stack:
  blender_control:
    version: "Blender 4.0+"
    communication: "PyZMQ (ZeroMQ sockets)"
    pattern: "Client (Python) → Server (Blender Python API)"
    use_cases:
      - "Render de productos 3D"
      - "Generación de mockups fotorrealistas"
      - "Animaciones para video marketing"

  triposr_integration:
    model: "TripoSR (VAST-AI-Research)"
    capability: "Imagen 2D → Modelo 3D"
    requirements:
      gpu: "RTX 3060+ (8GB VRAM mínimo)"
      alternative: "RunPod/Vast.ai (GPU cloud)"
    status: "⚠️ OPCIONAL para MVP (nice-to-have)"
```

#### **Blender Control: Implementación con PyZMQ**

```python
# tools/blender_controller.py
import zmq
import json

class BlenderController:
    """Controlador para Blender headless via ZMQ"""

    def __init__(self, host="localhost", port=5555):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(f"tcp://{host}:{port}")

    def render_product(self, product_config: dict) -> str:
        """Renderizar producto 3D"""
        command = {
            "action": "render",
            "type": "product",
            "config": product_config
        }

        # Enviar comando a Blender
        self.socket.send_json(command)

        # Recibir path del render
        response = self.socket.recv_json()
        return response["render_path"]

    def generate_mockup(self, template: str, assets: dict) -> str:
        """Generar mockup con template"""
        command = {
            "action": "mockup",
            "template": template,
            "assets": assets
        }

        self.socket.send_json(command)
        response = self.socket.recv_json()
        return response["mockup_path"]

# Server Blender (ejecutar dentro de Blender)
# blender_server.py (ejecutar con: blender --background --python blender_server.py)
import bpy
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    # Recibir comando
    command = socket.recv_json()

    if command["action"] == "render":
        # Ejecutar render en Blender
        output_path = f"/tmp/render_{uuid.uuid4()}.png"
        bpy.context.scene.render.filepath = output_path
        bpy.ops.render.render(write_still=True)

        # Enviar respuesta
        socket.send_json({"status": "success", "render_path": output_path})
```

### 6. **Resilience Patterns: Código de Producción**

```yaml
resilience_implementation:
  circuit_breaker:
    library: "PyBreaker"
    config:
      failure_threshold: 5
      recovery_timeout: 60 # segundos
      expected_exceptions: ["APIError", "TimeoutError"]

  retry_with_backoff:
    library: "tenacity"
    config:
      max_attempts: 3
      wait_strategy: "exponential"
      wait_multiplier: 1
      wait_max: 30

  timeout_management:
    api_calls: "30s"
    scraping: "60s"
    pdf_processing: "120s"
    llm_calls: "180s"
```

#### **Resilience: Implementación Completa**

```python
# app/utils/resilience.py
from pybreaker import CircuitBreaker, CircuitBreakerError
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
import httpx
from typing import TypeVar, Callable
import asyncio

T = TypeVar('T')

# Circuit breakers por servicio
semantic_scholar_breaker = CircuitBreaker(
    fail_max=5,
    timeout_duration=60,
    name="semantic_scholar"
)

arxiv_breaker = CircuitBreaker(
    fail_max=5,
    timeout_duration=60,
    name="arxiv"
)

class ResilientAPIClient:
    """Cliente HTTP con todos los resilience patterns"""

    def __init__(
        self,
        base_url: str,
        timeout: int = 30,
        breaker: CircuitBreaker | None = None
    ):
        self.client = httpx.AsyncClient(
            base_url=base_url,
            timeout=httpx.Timeout(timeout)
        )
        self.breaker = breaker or CircuitBreaker(fail_max=5, timeout_duration=60)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=30),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.HTTPStatusError))
    )
    async def get(self, endpoint: str, **kwargs) -> dict | None:
        """GET request con retry + circuit breaker"""

        @self.breaker
        async def _do_request():
            response = await self.client.get(endpoint, **kwargs)

            # Rate limit handling
            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 5))
                await asyncio.sleep(retry_after)
                raise httpx.HTTPStatusError(
                    "Rate limited",
                    request=response.request,
                    response=response
                )

            response.raise_for_status()
            return response.json()

        try:
            return await _do_request()
        except CircuitBreakerError:
            print(f"⚠️ Circuit breaker OPEN for {self.client.base_url}")
            return None
        except Exception as e:
            print(f"❌ Request failed: {e}")
            return None

# Uso en agente
class LiteratureResearcher(Agent):
    def __init__(self):
        self.semantic_scholar = ResilientAPIClient(
            "https://api.semanticscholar.org",
            breaker=semantic_scholar_breaker
        )
        self.arxiv = ResilientAPIClient(
            "https://export.arxiv.org",
            breaker=arxiv_breaker
        )

    async def search_papers(self, query: str):
        # Intentar Semantic Scholar primero
        results = await self.semantic_scholar.get(
            "/graph/v1/paper/search",
            params={"query": query}
        )

        # Si falla (circuit open), usar ArXiv como fallback
        if results is None:
            print("ℹ️ Fallback to ArXiv")
            results = await self.arxiv.get(
                "/api/query",
                params={"search_query": query}
            )

        return results or []
```

### 7. **Decisiones Técnicas: Resumen Ejecutivo**

```yaml
technical_decisions_summary:
  framework_orchestration:
    chosen: "LangGraph"
    rejected: ["AutoGen", "LangGraph"]
    confidence: "90%"

  api_framework:
    chosen: "FastAPI"
    rejected: ["Flask", "Django"]
    confidence: "95%"

  web_scraping:
    chosen: "Playwright"
    rejected: ["Selenium", "BeautifulSoup"]
    confidence: "95%"

  pdf_processing:
    chosen: "PyMuPDF + Unstructured (híbrido)"
    rejected: ["PyPDF2 solo", "Camelot"]
    confidence: "85%"

  3d_generation:
    chosen: "Blender + PyZMQ"
    optional: "TripoSR"
    confidence: "70% (experimental)"

  caching:
    chosen: "Valkey (Redis fork)"
    rejected: ["Memcached", "DynamoDB"]
    confidence: "90%"

  observability:
    chosen: "OpenTelemetry + Uptrace"
    rejected: ["Datadog", "New Relic", "Prometheus"]
    confidence: "85%"

  resilience:
    patterns: ["Circuit Breaker", "Retry with Backoff", "Timeout Management"]
    libraries: ["PyBreaker", "tenacity"]
    confidence: "95%"
```

---

## ✅ Conclusión: Plan Técnico Validado y Listo

Este plan técnico ha sido **validado con investigación real (Nov 2025)**:

- ✅ **LangGraph** implementado (migrated from CrewAI for compatibility)
- ✅ **FastAPI** validado con benchmarks (15-20K RPS vs Flask 2-3K)
- ✅ **Playwright** superior a Selenium (auto-waiting, multi-browser)
- ✅ **Híbrido PDF** (PyMuPDF velocidad + Unstructured calidad)
- ✅ **Blender + PyZMQ** para control 3D headless
- ✅ **Resilience patterns** implementados (Circuit Breaker + Retry)
- ✅ **Observability** con OpenTelemetry + Uptrace (1TB free)

**El stack tecnológico está 95% validado para implementación inmediata.**

---

_Este plan técnico es la implementación concreta de la especificación del proyecto. Cada decisión está justificada con benchmarks, comparaciones y código de ejemplo._
