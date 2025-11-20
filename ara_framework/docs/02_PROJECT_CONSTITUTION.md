# 📜 Constitución del Proyecto ARA (Agente de Investigación Autónomo)

## Principios Fundamentales de Gobernanza

### 1. **Calidad de Código (Code Quality)**

#### Principios:

- **Modularidad Absoluta**: Cada agente, herramienta y servidor MCP debe ser un módulo independiente y reutilizable
- **Desacoplamiento**: Las herramientas se exponen mediante APIs REST (FastAPI), nunca acopladas directamente a los agentes
- **Type Safety**: Uso estricto de type hints en Python 3.12+ para toda la base de código
- **Documentación Obligatoria**: Cada función/clase debe tener docstrings con formato Google Style
- **Clean Code**: Seguir PEP 8 y principios SOLID

#### Standards:

```python
# ✅ CORRECTO: Función bien documentada y tipada
def process_pdf(pdf_url: str, output_format: str = "json") -> dict[str, Any]:
    """
    Procesa un PDF académico y extrae contenido estructurado.

    Args:
        pdf_url: URL del archivo PDF a procesar
        output_format: Formato de salida ('json' o 'text')

    Returns:
        Diccionario con contenido estructurado del PDF

    Raises:
        ValueError: Si la URL es inválida
        requests.RequestException: Si falla la descarga
    """
    pass
```

### 2. **Estándares de Testing**

#### Cobertura Mínima:

- **Unit Tests**: 80% de cobertura para toda lógica de negocio
- **Integration Tests**: Para cada MCP Server (endpoint testing)
- **E2E Tests**: Para el pipeline completo de generación de tesis

#### Framework:

- pytest para unit tests
- pytest-asyncio para código asíncrono
- httpx para testing de FastAPI
- pytest-cov para reportes de cobertura

#### Estructura de Tests:

```
tests/
├── unit/
│   ├── test_agents/
│   ├── test_tools/
│   └── test_mcp_servers/
├── integration/
│   ├── test_webscraping_api.py
│   ├── test_pdf_ingestion_api.py
│   └── test_blender_control_api.py
└── e2e/
    └── test_thesis_generation_pipeline.py
```

### 3. **Consistencia en la Experiencia de Usuario**

#### Principios UX:

- **Feedback Constante**: Los agentes deben reportar progreso en tiempo real
- **Manejo de Errores Graceful**: Nunca fallar silenciosamente, siempre proporcionar contexto
- **Trazabilidad**: Cada sección generada debe indicar qué agente la produjo
- **Reproducibilidad**: Seeds configurables para resultados determinísticos

#### Logging Estructurado:

```python
import structlog

logger = structlog.get_logger()

logger.info(
    "agent_execution_started",
    agent="NicheAnalyst",
    task="market_analysis",
    sector="premium_spirits"
)
```

### 4. **Requisitos de Performance**

#### Métricas Objetivo:

| Componente                   | Métrica          | Target                      |
| ---------------------------- | ---------------- | --------------------------- |
| WebScraping MCP              | Response time    | < 5s por página             |
| PDF Ingestion MCP            | Processing speed | < 10s por PDF de 20 páginas |
| LiteratureResearcher         | Paper retrieval  | < 30s para 10 papers        |
| Thesis Generation (completa) | Total pipeline   | < 30 minutos                |

#### Optimizaciones Requeridas:

- **Caching**: Redis para resultados de búsquedas académicas
- **Async Processing**: Uso de asyncio para operaciones I/O-bound
- **Batch Processing**: Procesamiento paralelo de PDFs múltiples
- **Resource Limits**: Timeouts configurables para evitar bloqueos

### 5. **Seguridad y Privacidad**

#### Principios:

- **API Keys Seguras**: Todas las credenciales en variables de entorno (.env)
- **Validación de Entrada**: Sanitización estricta de URLs y parámetros
- **Aislamiento**: Cada MCP Server corre en su propio proceso/contenedor
- **No Persistencia de Datos Sensibles**: Los PDFs descargados se eliminan tras procesamiento

### 6. **Mantenibilidad y Escalabilidad**

#### Arquitectura:

- **Microservices**: Cada MCP Server es un servicio independiente
- **Containerización**: Docker para cada servidor
- **Orquestación**: docker-compose para desarrollo, Kubernetes para producción
- **Versionado de APIs**: /v1/ prefix para todos los endpoints

#### Evolución del Sistema:

- **Extensibilidad**: Fácil agregar nuevos agentes sin modificar existentes
- **Configuración Externa**: YAML/JSON para configuración de agentes y crews
- **Feature Flags**: Para activar/desactivar funcionalidades experimentales

---

## Flujo de Trabajo de Desarrollo

### 1. Antes de Implementar una Feature:

```bash
# Crear rama feature
git checkout -b feature/literature-researcher-agent

# Instalar dependencias en entorno virtual
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt -r requirements-dev.txt
```

### 2. Durante el Desarrollo:

- Escribir tests PRIMERO (TDD)
- Commits atómicos con mensajes descriptivos
- Ejecutar linter antes de commit: `ruff check .`
- Ejecutar formatter: `black .`

### 3. Antes de Merge:

- Todos los tests pasan: `pytest tests/ -v --cov`
- Cobertura > 80%
- Code review de al menos 1 persona
- Documentación actualizada

---

## Stack Tecnológico Autorizado

### Core Framework:

- **Python**: 3.12+ (required for modern type hints)
- **LangGraph**: Framework de orquestación multi-agente con StateGraph
- **LangChain**: Para tools y prompts (opcional)

### MCP Servers:

- **FastAPI**: Framework para exponer herramientas como REST APIs
- **uvicorn**: ASGI server para FastAPI

### Herramientas Especializadas:

- **Playwright**: Web scraping dinámico
- **Unstructured**: Procesamiento de PDFs
- **Semantic Scholar API**: Búsqueda académica
- **ArXiv API**: Papers de pre-print
- **ZMQ**: Comunicación con Blender
- **TripoSR**: Generación 3D (opcional)

### Calidad y Testing:

- **pytest**: Framework de testing
- **ruff**: Linter ultrarrápido
- **black**: Code formatter
- **mypy**: Type checker
- **structlog**: Logging estructurado

### Infrastructure:

- **Docker**: Containerización
- **docker-compose**: Orquestación local
- **Redis**: Caching (opcional)
- **PostgreSQL**: Persistencia de metadatos (opcional)

---

## Estructura de Commits

Formato obligatorio:

```
<tipo>(<scope>): <descripción corta>

<descripción detallada opcional>

<referencias a issues>
```

Tipos válidos:

- `feat`: Nueva feature
- `fix`: Bug fix
- `docs`: Cambios en documentación
- `test`: Agregar/modificar tests
- `refactor`: Refactorización sin cambio funcional
- `perf`: Mejoras de performance
- `chore`: Tareas de mantenimiento

Ejemplo:

```
feat(mcp-servers): implementar WebScraping MCP Server con Playwright

- Agregar endpoints /search, /product_details, /reviews
- Implementar rate limiting y retry logic
- Agregar tests de integración

Closes #12
```

---

## Definición de "Done"

Una feature está completa cuando:

- [ ] Código implementado y funcional
- [ ] Tests unitarios escritos y pasando
- [ ] Tests de integración (si aplica)
- [ ] Cobertura de código > 80%
- [ ] Documentación actualizada (docstrings + README)
- [ ] Code review aprobado
- [ ] Sin warnings de linter/type checker
- [ ] Performance dentro de targets definidos

---

## 🆕 ACTUALIZACIÓN NOVIEMBRE 2025: Stack Tecnológico Definitivo

> **Decisión Crítica**: Basada en investigación exhaustiva de 3 fuentes independientes  
> **Estado**: ✅ APROBADO PARA PRODUCCIÓN  
> **Presupuesto**: $10-18/mes (95% funcionalidad, ROI >160x)

### 1. **Modelos de IA: Configuración Official**

#### **Suscripción Base Obligatoria**

```yaml
primary_subscription:
  service: "GitHub Copilot Pro"
  cost: "$10/mes"
  justification: |
    Acceso a modelos premium (GPT-5, Claude Sonnet 4.5, Haiku 4.5)
    con 300 créditos/mes. Uso proyectado: ~45 créditos (15%).
    Buffer del 85% para picos de demanda.
  alternatives_rejected:
    - name: "Cursor Pro"
      cost: "$20/mes"
      reason: "2x más caro con funcionalidad equivalente a Copilot Pro + Continue.dev"
    - name: "Claude Pro"
      cost: "$20/mes"
      reason: "Acceso directo vs créditos de Copilot (peor relación precio/valor)"
```

#### **Asignación Oficial de Modelos por Agente**

```yaml
agents:
  NicheAnalyst:
    primary:
      model: "gpt-4o"
      provider: "GitHub Copilot Pro"
      cost: "0x créditos (GRATIS)"
      justification: "88% HumanEval, multimodal, suficiente para análisis de mercado"
    fallback:
      model: "minimax-m2"
      provider: "MiniMax API (self-hosted o gratuita)"
      cost: "$0"
      justification: "69.4% SWE-bench, 229B MoE, elite en agentic benchmarks"

  LiteratureResearcher:
    primary:
      model: "gemini-2.5-pro"
      provider: "Google AI Studio"
      cost: "$0"
      justification: "1M tokens de contexto, crítico para analizar 10-50 papers simultáneamente"
    fallback:
      model: "deepseek-v3"
      provider: "DeepSeek API gratuita"
      cost: "$0"
      justification: "92% HumanEval, 128K contexto, API gratuita estable"

  TechnicalArchitect:
    primary:
      model: "claude-sonnet-4.5"
      provider: "GitHub Copilot Pro"
      cost: "1x crédito"
      justification: "77.2% SWE-bench (SOTA), mejor para diseño arquitectónico complejo"
    fallback:
      model: "gpt-5"
      provider: "GitHub Copilot Pro"
      cost: "1x crédito"
      justification: "72.8% SWE-bench, excelente razonamiento general"

  FinancialAnalyst:
    primary:
      model: "gpt-5"
      provider: "GitHub Copilot Pro"
      cost: "1x crédito"
      justification: "88.7% MMLU, máxima precisión matemática y razonamiento complejo"
    fallback:
      model: "claude-sonnet-4.5"
      provider: "GitHub Copilot Pro"
      cost: "1x crédito"
      justification: "88% MMLU, análisis financiero robusto"

  StrategyProposer:
    primary:
      model: "claude-haiku-4.5"
      provider: "GitHub Copilot Pro"
      cost: "0.33x créditos"
      justification: "72% IFBench (seguimiento de instrucciones), 600-1000ms latencia, ideal para propuestas estratégicas"
    fallback:
      model: "gpt-4o"
      provider: "GitHub Copilot Pro"
      cost: "0x créditos (GRATIS)"
      justification: "Equivalente en escritura, sin costo"

  ReportGenerator:
    primary:
      model: "minimax-m2"
      provider: "MiniMax API / Self-hosted"
      cost: "$0"
      justification: "69.4% SWE-bench, MIT license, 229B params, generación de código de alta calidad"
    fallback:
      model: "gpt-4o"
      provider: "GitHub Copilot Pro"
      cost: "0x créditos (GRATIS)"
      justification: "88% HumanEval, generación confiable"

  OrchestratorAgent:
    primary:
      model: "claude-haiku-4.5"
      provider: "GitHub Copilot Pro"
      cost: "0.33x créditos"
      justification: "600-1000ms latencia (4-5x más rápido que Sonnet), decisiones rápidas"
    fallback:
      model: "gpt-4o"
      provider: "GitHub Copilot Pro"
      cost: "0x créditos (GRATIS)"
      justification: "Sin costo, latencia aceptable (1.2-1.6s)"
```

#### **Gestión de Presupuesto de Créditos**

```python
# Budget Manager Configuration (Official)
COPILOT_CREDITS = {
    "monthly_allocation": 300,
    "cost_per_model": {
        "gpt-5": 1.0,
        "gpt-5-codex": 1.0,
        "claude-sonnet-4.5": 1.0,
        "claude-haiku-4.5": 0.33,
        "gpt-4o": 0.0,
        "gpt-4o-mini": 0.0,
    },
    "projected_usage": {
        "FinancialAnalyst": 15,    # 15 análisis × 1.0 = 15 créditos
        "TechnicalArchitect": 10,  # 10 análisis × 1.0 = 10 créditos
        "StrategyProposer": 20,    # 20 análisis × 0.33 = 6.6 créditos
        "OrchestratorAgent": 10,   # 10 análisis × 0.33 = 3.3 créditos
    },
    "total_projected": 45,  # ~15% de 300
    "buffer": 255,          # 85% para picos
    "alert_threshold": 240, # Alertar si < 60 créditos (80%)
}
```

### 2. **Editores Agénticos: Decisión Oficial**

```yaml
development_tools:
  approved:
    - name: "Continue.dev"
      status: "✅ ADOPTADO"
      cost: "$0"
      license: "Apache 2.0 (open-source)"
      features:
        - "Extensión VS Code gratuita"
        - "BYO APIs (configuración con Copilot Pro)"
        - "Arquitectura extensible"
        - "Control total de costos"
      justification: |
        Funcionalidad equivalente a Cursor Pro cuando se combina
        con GitHub Copilot Pro. Ahorro: $240/año.

    - name: "GitHub Copilot"
      status: "✅ INTEGRADO"
      cost: "$10/mes (suscripción Pro)"
      features:
        - "Inline completions"
        - "Chat en IDE"
        - "Acceso a GPT-5, Claude Sonnet/Haiku"
        - "300 créditos premium/mes"

  rejected:
    - name: "Cursor Pro"
      cost: "$20/mes"
      reason: |
        Cancelado. Funcionalidad duplicada con Copilot Pro + Continue.dev.
        Decisión respaldada por 3 fuentes de investigación independientes.
        Trial de 14 días permitido solo para evaluar multi-file editing.

    - name: "Cline"
      reason: "No adoptado (sin suscripción activa)"

    - name: "Windsurf"
      reason: "No adoptado (sin suscripción activa)"

    - name: "Roo Code"
      reason: "No adoptado (sin suscripción activa)"

    - name: "Kilo.ai"
      reason: "No adoptado (sin suscripción activa)"

    - name: "Zed"
      reason: "No adoptado (sin suscripción activa)"
```

### 3. **Servidores MCP: Ecosystem Oficial (100% Gratuito)**

```yaml
mcp_servers:
  official_stack:
    - name: "GitHub MCP"
      status: "✅ ADOPTADO"
      provider: "GitHub (oficial)"
      cost: "$0"
      license: "MIT"
      capabilities:
        - "Repositorios, issues, PRs"
        - "Discusiones, security alerts"
        - "GitHub Actions"
      rate_limits: "Según políticas API de GitHub"
      authentication: "PAT (Personal Access Token) con scopes mínimos"

    - name: "Playwright MCP"
      status: "✅ ADOPTADO"
      provider: "ExecuteAutomation (comunidad)"
      cost: "$0"
      license: "MIT"
      capabilities:
        - "Web scraping moderno (SPAs)"
        - "Automatización de navegador"
        - "Screenshots, ejecución de JS"
      justification: |
        Superior a Selenium en SPAs (auto-waiting, multi-browser).
        Benchmarks: más robusto en sitios JS-heavy.

    - name: "MarkItDown MCP"
      status: "✅ ADOPTADO"
      provider: "Microsoft"
      cost: "$0"
      license: "MIT"
      capabilities:
        - "PDF → Markdown"
        - "DOCX, PPTX → Markdown"
      justification: "Esencial para ingesta de papers académicos"

    - name: "Jina AI Reader MCP"
      status: "✅ ADOPTADO (reemplazo de Firecrawl)"
      provider: "Jina AI"
      cost: "$0"
      api: "https://r.jina.ai/{url}"
      rate_limits:
        without_key: "20 RPM"
        with_free_key: "200 RPM"
        tokens_included: "10M tokens gratuitos"
      capabilities:
        - "URL → Markdown limpio"
        - "Scraping estructurado"
      justification: |
        Reemplaza Firecrawl ($49/mes). 200 RPM suficiente
        para 100 análisis/mes (2 requests/análisis = 200 requests/mes).

    - name: "Supabase MCP"
      status: "✅ ADOPTADO"
      provider: "Supabase"
      cost: "$0 (free tier)"
      limits:
        database: "500 MB"
        storage: "1 GB"
        egress: "5 GB"
        mau: "50,000 usuarios activos/mes"
        realtime: "2M mensajes/mes"
        edge_functions: "500K invocaciones/mes"
      warnings:
        - "Proyectos se pausan tras 1 semana de inactividad"
        - "Monitorear uso para evitar pausa"
      capabilities:
        - "Base de datos PostgreSQL"
        - "Storage de artefactos"
        - "Edge Functions"

    - name: "Notion MCP"
      status: "✅ ADOPTADO"
      provider: "Notion (API oficial)"
      cost: "$0 (uso de API gratuito)"
      rate_limits:
        average: "3 req/s por integración"
        burst: "Ráfagas permitidas parcialmente"
        payload: "1000 bloques, 500 KB"
        error: "HTTP 429 → respetar Retry-After"
      capabilities:
        - "Gestión de conocimiento"
        - "Documentación interna"
        - "Tracking de investigación"

    - name: "ChromeDevTools MCP"
      status: "✅ ADOPTADO"
      provider: "Comunidad"
      cost: "$0"
      license: "Open-source"
      capabilities:
        - "Debugging de scraping"
        - "Network monitoring"
        - "Console logging"

    - name: "Rube MCP"
      status: "✅ ADOPTADO (TBD)"
      provider: "Comunidad"
      cost: "$0"
      capabilities:
        - "Orquestación de workflows"
        - "Multi-tool execution"

  rejected:
    - name: "Firecrawl MCP"
      cost: "$49/mes mínimo (créditos en nube)"
      reason: |
        ❌ RECHAZADO por costo. Reemplazado por Jina AI Reader (gratuito).
        Firecrawl es potente para crawling profundo, pero rompe restricción
        presupuestaria. Considerar solo si se habilita presupuesto futuro.
```

### 4. **Stack Técnico Validado**

```yaml
core_technologies:
  programming_language:
    name: "Python"
    version: "3.11+"
    justification: "Type hints modernos, performance, compatibilidad con FastAPI y LangGraph"

  orchestration:
    framework: "LangGraph"
    justification: |
      Orientado a roles y procesos. Mejor que AutoGen (conversacional)
      y LangGraph (estado complejo) para flujos estructurados.
      Evidencia: investigación_minimax/docs/core_tech_stack_validation.md

  api_framework:
    framework: "FastAPI"
    justification: |
      15-20k RPS vs Flask 2-3k RPS en benchmarks I/O-bound.
      Async/await nativo, validación Pydantic, auto-documentación.
      Crítico para microservicios MCP con alta concurrencia.

  web_scraping:
    tool: "Playwright"
    justification: |
      Superior a Selenium (flaky en SPAs) y Puppeteer (solo Chrome).
      Auto-waiting, multi-browser (Chromium, Firefox, WebKit).
      Async APIs, mejor estabilidad en sitios JS-heavy.

  pdf_processing:
    tools:
      - name: "Unstructured.io"
        use_case: "RAG (fragmentos semánticos)"
        cost: "$0 (open-source)"
      - name: "PyMuPDF (pymupdf4llm)"
        use_case: "Velocidad (~0.12s/página)"
        cost: "$0"
      - name: "pdfplumber"
        use_case: "Tablas complejas"
        cost: "$0"
    justification: |
      Unstructured: mejor para RAG (Title, NarrativeText).
      PyMuPDF: 10x más rápido que Unstructured.
      pdfplumber: mejor para tablas basadas en coordenadas.

  3d_pipeline:
    tools:
      - name: "Blender"
        control: "Python (bpy) + pyzmq"
        use_case: "Render headless, manipulación de escenas"
      - name: "TripoSR"
        use_case: "Reconstrucción 3D desde imagen"
        requirements: "GPU RTX 3060 6GB mínimo (A100 para velocidad)"
      - name: "Open3D + trimesh"
        use_case: "Operaciones geométricas, mallas"

  caching:
    backend: "Valkey (Redis-compatible)"
    justification: |
      OSS, compatible con Redis. Alternativa: Dragonfly (compresión 1.18).
      TTL por endpoint, caching distribuido.
    policy:
      search_papers: "24-72 horas"
      pdf_conversion: "30 días"
      project_metadata: "24 horas"

  observability:
    stack:
      - tool: "OpenTelemetry (OTel)"
        justification: "Estándar para traces, métricas, logs"
      - tool: "Uptrace"
        cost: "$0 (plan free: 1TB storage)"
        justification: "Backend open-source basado en ClickHouse"
      - tool: "structlog"
        justification: "Logging JSON estructurado, líneas canónicas"

  resilience:
    patterns:
      - name: "Rate Limiting"
        implementation: "SlowAPI (token bucket)"
        justification: "Cumplir límites de proveedores (Semantic Scholar 1 RPS)"
      - name: "Circuit Breaker"
        implementation: "PyBreaker"
        justification: "Aislar fallas de APIs externas"
      - name: "Retry with Backoff"
        implementation: "Exponential backoff con jitter"
        justification: "Recuperación automática de errores transitorios"
```

### 5. **Arquitectura Oficial: Basada en Artefactos**

```yaml
architecture:
  paradigm: "Basada en Artefactos (NO conversacional)"
  justification: |
    Estudios de Anthropic: sistemas conversacionales consumen 15x más tokens.
    Cada traspaso de contexto: 100-500 ms latencia.
    Arquitectura basada en artefactos: agentes consumen/producen JSON/Markdown.
    Beneficios: -80% tokens, trazabilidad, reproducibilidad.

  flow:
    - step: "Input"
      format: "JSON con parámetros de análisis"
      example:
        niche: "premium_spirits"
        brand: "absolut_vodka"
        target_market: "millennials_urban"

    - step: "NicheAnalyst → Artefacto"
      output: "niche_analysis.json"
      content:
        - "market_size"
        - "competitors"
        - "trends"

    - step: "LiteratureResearcher → Artefacto"
      output: "literature_review.md"
      content:
        - "papers_summary"
        - "key_findings"
        - "citations"

    - step: "TechnicalArchitect → Artefacto"
      output: "architecture_diagram.svg + specs.md"

    - step: "ContentSynthesizer → Artefacto"
      output: "thesis_draft.md"
      validation: "Gates de calidad (coherencia, citas, estructura)"

  parallelization:
    - component: "LiteratureResearcher"
      strategy: "Cola de trabajo paralela con rate limiting"
      justification: |
        Semantic Scholar: 1 RPS → cuello de botella crítico.
        Implementar RateLimitedQueue para paralelizar respetando límites.
      code:
        python: |
          async def fetch_papers_parallel(queries, rate_limit=1):
              queue = RateLimitedQueue(rate_limit)
              tasks = [queue.enqueue(fetch_paper, q) for q in queries]
              return await asyncio.gather(*tasks)
```

### 6. **SLAs y Performance Targets Revisados**

```yaml
performance_targets:
  realistic_pipeline:
    optimistic: "60-75 minutos"
    realistic: "135-165 minutos (sin optimizaciones)"
    justification: |
      Investigación Nov 2025 confirma: objetivo original de <45 min NO es viable.
      Bottlenecks: Semantic Scholar 1 RPS, overhead multi-agente, variabilidad PDFs.

  by_agent:
    NicheAnalyst:
      target: "7-8 minutos"
      original: "~5 minutos"
      deviation: "+60% (scraping JS-heavy con anti-bot)"

    LiteratureResearcher:
      target: "20-25 minutos"
      original: "~15 minutos"
      deviation: "+67% (1 RPS de Semantic Scholar)"

    TechnicalArchitect:
      target: "10-12 minutos"
      original: "~8 minutos"
      deviation: "+50% (latencia modelos premium)"

    ImplementationSpecialist:
      target: "7-8 minutos"
      original: "~5 minutos"
      deviation: "+60% (rendering 3D, assets)"

    ContentSynthesizer:
      target: "9-10 minutos"
      original: "~7 minutos"
      deviation: "+43% (gestión citas, formato)"

    Orchestration_Overhead:
      target: "5-7 minutos"
      original: "2-5 minutos"
      deviation: "+100% (traspaso contexto, validación gates)"

  budgets:
    monthly:
      copilot_pro: "$10"
      apis_external: "$0-8"
      total: "$10-18"
      analyses_per_month: "100"
      cost_per_analysis: "$0.10-0.18"

  monitoring:
    dashboard: "OpenTelemetry + Uptrace (free)"
    alerts:
      - condition: "Presupuesto > 80%"
        action: "Email/Slack alert"
      - condition: "Latencia P95 > objetivo + 20%"
        action: "Email/Slack alert"
      - condition: "Tasa error API > 5% en 10 min"
        action: "Email/Slack alert"
      - condition: "Créditos Copilot < 60"
        action: "Email/Slack alert"
```

### 7. **Gates de Calidad Obligatorios**

```yaml
quality_gates:
  between_agents:
    - gate: "Structure Validation"
      checks:
        - "Secciones obligatorias presentes"
        - "Formato Markdown correcto"
        - "Sin placeholders (TODO, XXX, FIXME)"
      action_on_failure: "Retry con prompt específico"

    - gate: "Citation Validation"
      checks:
        - "Todas las citas tienen formato correcto"
        - "Referencias bibliográficas completas"
        - "No hay citas huérfanas"
      action_on_failure: "Rerun ContentSynthesizer con validación"

    - gate: "Consistency Check"
      checks:
        - "Terminología consistente"
        - "No contradicciones entre secciones"
        - "Tono y estilo uniforme"
      action_on_failure: "Rewrite con guía de estilo"

    - gate: "Performance Check"
      checks:
        - "Tiempo de ejecución < SLA + 20%"
        - "Uso de créditos < presupuesto"
        - "Tasa de error < 1%"
      action_on_failure: "Log warning + continuar"
```

### 8. **Decisiones de Seguridad**

```yaml
security:
  api_keys:
    storage: "Variables de entorno (.env)"
    never_commit: "Agregar .env a .gitignore"
    rotation: "Cada 90 días (automated)"
    scopes: "Principio de mínimo privilegio"

  data_privacy:
    pdf_handling: "Descargar → Procesar → Eliminar inmediatamente"
    user_data: "No persistir datos sensibles sin consentimiento"
    logs: "Sanitizar URLs y parámetros sensibles"

  network:
    mcp_servers: "Aislamiento por contenedor Docker"
    proxies: "Rotativos para scraping (solo si necesario)"
    rate_limiting: "Token bucket por IP/API key"

  monitoring:
    audit_logs: "JSON estructurado con timestamp, user, action"
    retention: "30 días (compresión + ILM)"
    alertas: "Anomalías en consumo de créditos/APIs"
```

---

## 🎯 Conclusión: Constitución Actualizada y Validada

Esta constitución ha sido **actualizada y validada** con evidencia de:

- ✅ **Investigación exhaustiva de 3 fuentes** (MiniMax, Perplexity, Gemini)
- ✅ **Benchmarks reales de Nov 2025** (SWE-bench, HumanEval, MMLU)
- ✅ **Costos verificados** ($10-18/mes, ROI >160x)
- ✅ **Limitaciones técnicas reales** (Semantic Scholar 1 RPS, overhead multi-agente)
- ✅ **Stack completamente gratuito** (8 servidores MCP sin costo)

**Todos los principios arquitectónicos y de gobernanza se mantienen válidos.**  
**El stack tecnológico ha sido optimizado para máximo ROI con presupuesto mínimo.**

---

_Este documento es la ley del proyecto. Toda decisión arquitectónica debe ser consistente con estos principios._
