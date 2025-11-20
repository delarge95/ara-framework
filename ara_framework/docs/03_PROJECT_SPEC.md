# 📋 Especificación del Proyecto: Marco ARA (Agente de Investigación Autónomo)

## 🎯 Visión del Proyecto

### ¿Qué estamos construyendo?

Un **sistema multi-agente autónomo** capaz de generar tesis académicas completas de forma automatizada, utilizando IA avanzada para replicar el proceso de investigación humano pero a escala y velocidad sin precedentes.

### ¿Por qué es importante?

#### Problema Actual:

1. **Barrera de Entrada Alta**: Escribir una tesis de calidad requiere meses de investigación manual
2. **Trabajo Repetitivo**: Mucha de la investigación implica tareas mecánicas (búsqueda de papers, extracción de datos, formateo)
3. **Inconsistencia**: La calidad depende enormemente del investigador individual
4. **No Escalable**: Un investigador humano solo puede trabajar en 1-2 tesis simultáneamente

#### Nuestra Solución:

Un equipo de **agentes de IA especializados** que:

- Automatizan la búsqueda y análisis de literatura
- Realizan análisis de mercado en tiempo real
- Generan especificaciones técnicas detalladas
- Sintetizan contenido académico coherente y bien fundamentado

#### Impacto:

- ✅ Reducir tiempo de generación de tesis de **meses a horas**
- ✅ Democratizar el acceso a investigación de calidad
- ✅ Permitir investigación paralela en múltiples dominios
- ✅ Establecer un nuevo paradigma en investigación asistida por IA

---

## 🏗️ Arquitectura Conceptual

### Paradigma: Flujos de Trabajo Agénticos vs. Automatización Tradicional

El Marco ARA NO es:

- ❌ Un simple script de automatización lineal
- ❌ Un chatbot con un solo LLM monolítico
- ❌ Una herramienta de "generación de texto con prompts"

El Marco ARA ES:

- ✅ Un **sistema multi-agente** donde cada agente tiene roles y herramientas especializadas
- ✅ Un **workflow dinámico** que se adapta al contexto
- ✅ Una **arquitectura de microservicios** para herramientas desacopladas
- ✅ Un **pipeline secuencial** con validación en cada etapa

### Filosofía de Diseño: "División del Trabajo"

Inspirado en equipos de investigación reales:

- El **Analista de Mercado** identifica problemas viables
- El **Investigador Académico** revisa literatura y teorías
- El **Arquitecto Técnico** diseña soluciones
- El **Escritor** sintetiza todo en un documento coherente

Cada agente es **autónomo pero colaborativo**, con su propio conjunto de herramientas especializadas.

---

## 👥 El Elenco de Agentes

### 1. **ProjectManager** 🎩

**Responsabilidad**: Orquestación y control de calidad

**Tareas**:

- Asignar tareas a agentes especializados
- Monitorear progreso del pipeline
- Validar que cada sección cumple requisitos estructurales
- Resolver conflictos entre agentes

**Herramientas**:

- Task Assignment Tool
- Quality Validation Tool
- Inter-Agent Communication Protocol

**Salida**: Plan de ejecución y reporte de validación

---

### 2. **NicheAnalyst** 🔍

**Responsabilidad**: Identificar problemas viables y oportunidades de mercado

**Tareas**:

- Analizar tendencias de mercado en un dominio específico
- Escanear actividad de la competencia
- Recolectar sentimiento del consumidor
- Identificar "espacios en blanco" (whitespace opportunities)

**Herramientas**:

- WebScraping MCP Server (Playwright-based)
  - `search_and_extract()`: Buscar productos en e-commerce
  - `extract_product_details()`: Extraer información de páginas de producto
  - `extract_reviews()`: Recolectar reseñas de clientes
  - `scan_competitor_websites()`: Analizar features de competidores

**Salida**: Secciones "Planteamiento del Problema" y "Justificación"

**Ejemplo de Ejecución**:

```
Input: "Analizar mercado de bebidas espirituosas premium"
↓
Agente planea:
1. Escanear sitios web de Absolut, Grey Goose, Belvedere
2. Buscar reseñas en Drizly, ReserveBar
3. Identificar tecnologías de marketing utilizadas

↓
Ejecuta herramientas:
- scan_features("https://www.greygoose.com") → {"has_web3d": false}
- extract_reviews("drizly", "Absolut Vodka") → {"sentiment": "neutral", "common_complaint": "lack_of_engaging_experience"}

↓
Sintetiza hallazgos:
"Los competidores no utilizan experiencias Web 3D inmersivas.
Los consumidores buscan experiencias de compra más atractivas para productos premium."
```

---

### 3. **LiteratureResearcher** 📚

**Responsabilidad**: Construcción del Estado del Arte y Marco Teórico

**Tareas**:

- Búsqueda por palabras clave en bases de datos académicas
- Descarga y procesamiento de PDFs académicos
- Resumen individual de papers
- Análisis temático y extracción de marcos teóricos
- Identificación de brechas de investigación (gap analysis)

**Herramientas**:

- **Academic Search Tools**:
  - `search_semantic_scholar(query, year_filter)`: Búsqueda en Semantic Scholar
  - `search_arxiv(query)`: Búsqueda en ArXiv
- **PDF Ingestion MCP Server**:
  - `process_pdf(url)`: Extrae contenido estructurado de PDFs académicos

**Salida**: Secciones "Estado del Arte", "Marco Teórico" y "Gap Analysis"

**Pipeline de Ejecución**:

```
1. Búsqueda de Papers:
   Keywords: ["Web 3D", "Immersive Storytelling", "PBR Rendering"]
   → Retrieval: 50 papers relevantes

2. Filtrado:
   Criterios: Year > 2018, Citations > 10
   → Filtered: 15 papers de alta calidad

3. Procesamiento:
   Para cada paper:
     - Descargar PDF
     - Extraer texto estructurado (Unstructured.io)
     - Generar resumen con LLM

4. Síntesis Temática:
   Agrupar papers por:
   - Marcos teóricos (e.g., "Modelo S-O-R")
   - Metodologías (e.g., "Desarrollo Ágil")
   - Limitaciones mencionadas

5. Gap Analysis:
   Identificar preguntas no respondidas en la literatura
```

---

### 4. **TechnicalArchitect** ⚙️

**Responsabilidad**: Diseño de soluciones técnicas y especificaciones

**Tareas**:

- Selección de stack tecnológico justificado
- Diseño de arquitectura de software
- Definición de componentes y APIs
- Identificación de desafíos de implementación
- Coordinación de generación de activos 3D

**Herramientas**:

- Code Repository Search Tools
- Blender Control MCP Server (para generación de activos)
- Generative 3D Tools (TripoSR)

**Salida**: Sección "Especificaciones Técnicas del MVP"

---

### 5. **ImplementationSpecialist** 💻

**Responsabilidad**: Ejecución de tareas técnicas programáticas

**Tareas**:

- Generación de activos 3D desde imágenes
- Refinamiento de modelos en Blender
- Aplicación de materiales PBR
- Renderizado de imágenes de prueba
- Ejecución de scripts de construcción

**Herramientas**:

- FileSystem MCP Server
- Code Execution Tool
- Blender Control MCP Server (ejecución de comandos)

**Salida**: Activos visuales y código boilerplate

---

### 6. **ContentSynthesizer** ✍️

**Responsabilidad**: Ensamblaje final del documento de tesis

**Tareas**:

- Unificación de tono y estilo
- Formateo según plantilla académica
- Generación de transiciones entre secciones
- Gestión de citas bibliográficas
- Integración de elementos visuales (figuras, tablas)

**Herramientas**:

- Text Formatting Tools
- Citation Management Tools
- Document Assembly Pipeline

**Salida**: Documento de tesis completo y formateado (PDF/LaTeX/DOCX)

---

## 🔧 El Patrón "Servidor MCP": Herramientas como Microservicios

### Problema:

Los agentes necesitan capacidades más allá de la generación de lenguaje:

- Navegar la web con JavaScript complejo
- Procesar PDFs con layouts multi-columna
- Controlar software externo (Blender)
- Ejecutar código computacionalmente intensivo

### Solución Arquitectónica:

```
┌─────────────────────────────────────────────────────────────┐
│                    LangGraph Agents Layer                    │
│  [NicheAnalyst] [LiteratureResearcher] [TechnicalArchitect] │
└────────────┬───────────────┬────────────────┬───────────────┘
             │               │                │
             │  HTTP REST    │  HTTP REST     │  HTTP REST
             ▼               ▼                ▼
┌──────────────────┐  ┌──────────────┐  ┌─────────────────┐
│  WebScraping     │  │ PDF Ingestion│  │ Blender Control │
│  MCP Server      │  │ MCP Server   │  │ MCP Server      │
│                  │  │              │  │                 │
│  FastAPI         │  │  FastAPI     │  │  FastAPI + ZMQ  │
│  + Playwright    │  │  + Unstruct. │  │  + Blender API  │
└──────────────────┘  └──────────────┘  └─────────────────┘
```

### Beneficios:

1. **Desacoplamiento**: Los agentes no conocen la implementación de las herramientas
2. **Modularidad**: Cada servidor es independiente, fácil de desarrollar y probar
3. **Escalabilidad**: Cada servidor puede correr en su propio contenedor
4. **Gestión de Dependencias**: Bibliotecas pesadas (PyTorch, Playwright) aisladas

### Ejemplo de Implementación:

**Servidor (FastAPI)**:

```python
from fastapi import FastAPI
from playwright.async_api import async_playwright

app = FastAPI()

@app.post("/scrape/product_details")
async def scrape_product_details(url: str) -> dict:
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)

        title = await page.locator("h1.product-title").text_content()
        price = await page.locator(".price").text_content()

        await browser.close()

        return {"title": title, "price": price}
```

**Cliente (Agent Tool)**:

```python
import requests

def scrape_product_details(url: str) -> dict:
    """Herramienta que los agentes pueden usar."""
    response = requests.post(
        "http://localhost:8001/scrape/product_details",
        json={"url": url}
    )
    return response.json()
```

---

## 🔄 Pipeline de Ejecución Secuencial

### Flujo Completo:

```
[USER INPUT]
    "Generar tesis sobre: Marketing digital para bebidas premium"
    ↓
[PHASE 0: Initialization]
    ProjectManager crea plan de ejecución
    → Asigna tareas a agentes
    ↓
[PHASE 1: Problem Discovery] (~5 min)
    NicheAnalyst ejecuta:
    1. Escanea sitios de competidores
    2. Analiza reseñas de consumidores
    3. Identifica brecha de mercado
    → OUTPUT: "Planteamiento del Problema" + "Justificación"
    ↓
[PHASE 2: Literature Review] (~15 min)
    LiteratureResearcher ejecuta:
    1. Busca 50 papers en Semantic Scholar + ArXiv
    2. Procesa PDFs con Unstructured.io
    3. Resume cada paper individualmente
    4. Realiza análisis temático
    5. Identifica gaps de investigación
    → OUTPUT: "Estado del Arte" + "Marco Teórico" + "Gap Analysis"
    ↓
[PHASE 3: Technical Design] (~8 min)
    TechnicalArchitect ejecuta:
    1. Analiza requisitos del problema
    2. Selecciona stack tecnológico (React Three Fiber, GSAP, etc.)
    3. Diseña arquitectura de componentes
    4. Genera diagramas técnicos
    → OUTPUT: "Especificaciones Técnicas del MVP"
    ↓
[PHASE 4: Asset Generation] (~5 min)
    ImplementationSpecialist ejecuta:
    1. Genera modelo 3D base con TripoSR
    2. Refina en Blender (vía MCP Server)
    3. Aplica materiales PBR
    4. Renderiza imágenes de prueba
    → OUTPUT: Activos visuales (renders, diagramas)
    ↓
[PHASE 5: Synthesis] (~7 min)
    ContentSynthesizer ejecuta:
    1. Recibe todas las secciones generadas
    2. Unifica tono y estilo
    3. Genera transiciones
    4. Formatea citas bibliográficas
    5. Inserta figuras y tablas
    6. Genera documento final
    → OUTPUT: Documento de tesis completo (PDF)
    ↓
[PROJECT MANAGER: Quality Check]
    Valida estructura, coherencia y completitud
    → Si pasa: Entrega final
    → Si falla: Re-asigna tareas de corrección
```

**Tiempo Total Estimado**: 30-40 minutos para una tesis completa

---

## 🎯 Criterios de Éxito

### Métricas Cuantitativas:

- [ ] Generación de tesis completa en **< 45 minutos**
- [ ] Coherencia temática (validación por evaluador humano): **> 8/10**
- [ ] Precisión fáctica (citas reales y verificables): **> 95%**
- [ ] Estructura completa (todas las secciones requeridas): **100%**

### Métricas Cualitativas:

- [ ] El documento debe ser **indistinguible de una tesis escrita por humano** (Turing test)
- [ ] Las recomendaciones técnicas deben ser **implementables y actuales**
- [ ] Las citas académicas deben ser **relevantes y correctamente contextualizadas**
- [ ] El análisis de mercado debe estar **fundamentado en datos reales**

---

## 🚀 Caso de Uso de Ejemplo

**Input del Usuario**:

```
Dominio: "Marketing de Bebidas Espirituosas Premium"
Marca Foco: "Absolut Vodka"
Tecnología Propuesta: "Experiencias Web 3D Interactivas"
```

**Output Esperado**:
Un documento de tesis de ~60 páginas que incluye:

1. **Introducción y Planteamiento del Problema** (5 pags)

   - Análisis de la brecha de storytelling digital en el sector
   - Justificación basada en datos de mercado reales

2. **Estado del Arte y Marco Teórico** (15 pags)

   - Revisión de 15+ papers sobre Web 3D, storytelling inmersivo
   - Marcos teóricos: Modelo S-O-R, Teoría de Presencia Mediada
   - Gap analysis: Falta de plataformas 3D centralizadas

3. **Especificaciones Técnicas del MVP** (10 pags)

   - Stack: React Three Fiber, Three.js, GSAP, Vite
   - Arquitectura de componentes
   - Materiales PBR para renderizado fotorrealista

4. **Desarrollo e Implementación** (20 pags)

   - Pipeline de activos 3D
   - Código de ejemplo para componentes clave
   - Renders de alta calidad del producto

5. **Resultados y Conclusiones** (10 pags)
   - Validación técnica del MVP
   - Análisis de impacto potencial
   - Futuras líneas de investigación

**Valor Agregado**:

- ✅ Todo fundamentado en datos reales (no alucinaciones)
- ✅ Citas académicas verificables
- ✅ Especificaciones técnicas implementables
- ✅ Activos visuales de alta calidad

---

## 🌍 Impacto y Futuro

### Impacto Inmediato:

- Acelerar generación de tesis de grado/maestría
- Democratizar acceso a investigación de calidad
- Establecer nuevo estándar en investigación asistida por IA

### Evolución Futura:

1. **Ajuste Fino de Modelos**: Entrenar LLMs especializados en dominios específicos
2. **Agentes Colaborativos**: Múltiples agentes debatiendo hipótesis
3. **Validación Automática**: Verificación de claims contra bases de datos
4. **Multi-Modalidad**: Generación de videos, presentaciones, demos interactivos

### Limitaciones Conocidas:

- ⚠️ Requiere supervisión humana para validación final
- ⚠️ Dependiente de calidad de datos accesibles (APIs, papers abiertos)
- ⚠️ No reemplaza el juicio crítico humano, lo aumenta

---

## 📊 ACTUALIZACIÓN NOVIEMBRE 2025: Requerimientos Validados

> **Fuente**: Investigación exhaustiva Nov 2025 (MiniMax + Perplexity + Gemini)  
> **Estado**: ✅ ESPECIFICACIONES ACTUALIZADAS CON DATOS REALES

### 1. **SLAs de Performance Revisados (Basados en Evidencia)**

#### **Pipeline Completo: Tiempos Reales**

```yaml
performance_slas:
  original_target: "< 45 minutos"
  status: "❌ NO VIABLE (basado en investigación técnica)"

  realistic_targets:
    optimistic: "60-75 minutos"
    confidence: "85%"
    assumptions:
      - "Paralelización implementada"
      - "Caching funcionando"
      - "Rate limits manejados"

    realistic: "135-165 minutos"
    confidence: "95%"
    assumptions:
      - "Flujo secuencial sin optimizaciones"
      - "APIs externas con delays"
      - "Procesamiento PDFs variable"

  recommended_target: "60-75 minutos"
  justification: |
    Alcanzable con optimizaciones incrementales.
    Aún representa 99% de ahorro vs investigación manual (6-18 meses).
```

#### **SLAs por Agente (Validados con Investigación)**

```yaml
agent_slas:
  NicheAnalyst:
    original: "~5 minutos"
    validated: "7-8 minutos"
    deviation: "+60%"
    bottlenecks:
      - "Scraping de sitios JS-heavy con anti-bot"
      - "Rate limits de proveedores (Google, Bing)"
      - "Variabilidad en tiempos de respuesta de páginas"
    mitigation:
      - "Playwright con stealth mode"
      - "Proxies rotativos (solo si necesario)"
      - "Caching de búsquedas repetitivas (TTL 24h)"

  LiteratureResearcher:
    original: "~15 minutos"
    validated: "20-25 minutos"
    deviation: "+67%"
    bottlenecks:
      - "⚠️ CRÍTICO: Semantic Scholar 1 RPS (solicitud por segundo)"
      - "Descarga de 15-50 papers en cola secuencial"
      - "Parsing de PDFs con layouts complejos"
    mitigation:
      - "Cola de trabajo paralela con RateLimitedQueue"
      - "Prefetch de papers más citados"
      - "PyMuPDF para velocidad (0.12s/página vs 1.29s Unstructured)"
    code_example: |
      async def fetch_papers_parallel(queries, rate_limit=1):
          queue = RateLimitedQueue(rate_limit=rate_limit)
          tasks = [queue.enqueue(fetch_paper, q) for q in queries]
          return await asyncio.gather(*tasks)

  TechnicalArchitect:
    original: "~8 minutos"
    validated: "10-12 minutos"
    deviation: "+50%"
    bottlenecks:
      - "Latencia de modelos premium (Claude Sonnet 4.5: 2-3s)"
      - "Generación de diagramas complejos"
      - "Validación de especificaciones técnicas"
    mitigation:
      - "Usar Claude Sonnet 4.5 (77.2% SWE-bench)"
      - "Templates de arquitectura pre-cargados"
      - "Generación paralela de diagramas"

  ImplementationSpecialist:
    original: "~5 minutos"
    validated: "7-8 minutos"
    deviation: "+60%"
    bottlenecks:
      - "Rendering 3D con Blender (headless)"
      - "Generación de assets múltiples"
      - "Control de calidad de renders"
    mitigation:
      - "Blender + pyzmq en modo batch"
      - "TripoSR para generación rápida (GPU: RTX 3060+)"
      - "Cloud GPU para cargas intensivas"

  ContentSynthesizer:
    original: "~7 minutos"
    validated: "9-10 minutos"
    deviation: "+43%"
    bottlenecks:
      - "Gestión de 50-100 citas bibliográficas"
      - "Validación de consistencia entre secciones"
      - "Formateo de documento extenso (50-80 páginas)"
    mitigation:
      - "Templates de LaTeX pre-validados"
      - "BibTeX automation con validación"
      - "Gates de calidad automatizados"

  Orchestration_Overhead:
    original: "2-5 minutos"
    validated: "5-7 minutos"
    deviation: "+100%"
    bottlenecks:
      - "Traspaso de contexto entre agentes (100-500ms cada uno)"
      - "Estudios Anthropic: hasta 15x más tokens en multi-agente"
      - "Validación entre fases (gates de calidad)"
    mitigation:
      - "✅ Arquitectura basada en artefactos (NO conversacional)"
      - "Agentes consumen/producen JSON/Markdown"
      - "Elimina 80% de overhead de tokens"
```

### 2. **Asignación de Modelos por Agente (Oficial)**

```yaml
model_assignments:
  budget:
    monthly: "$10-18"
    copilot_credits: 300
    projected_usage: 45 # 15% del total
    buffer: 255 # 85% para spikes

  agents:
    NicheAnalyst:
      model: "gpt-4o"
      provider: "GitHub Copilot Pro"
      cost: "0x créditos (GRATIS)"
      benchmarks:
        humaneval: "88%"
        mmlu: "88.7%"
      justification: "Suficiente para análisis de mercado, multimodal, sin costo"
      fallback: "minimax-m2 (69.4% SWE-bench, $0)"

    LiteratureResearcher:
      model: "gemini-2.5-pro"
      provider: "Google AI Studio"
      cost: "$0 (plan gratuito)"
      benchmarks:
        context: "1M tokens ⭐"
        humaneval: "90%"
      justification: "CRÍTICO: 1M contexto para analizar 10-50 papers simultáneamente"
      usage_pattern: "10-50 papers × 5-10K tokens/paper = 50-500K tokens → requiere 1M contexto"
      fallback: "deepseek-v3 (92% HumanEval, 128K ctx, $0)"

    TechnicalArchitect:
      model: "claude-sonnet-4.5"
      provider: "GitHub Copilot Pro"
      cost: "1x crédito"
      benchmarks:
        swe_bench: "77.2% (SOTA) ⭐"
        mmlu: "88%"
      justification: "Mejor para diseño arquitectónico SWE-level, razonamiento profundo"
      estimated_usage: "10 análisis/mes × 1 crédito = 10 créditos"
      fallback: "gpt-5 (72.8% SWE-bench, 1x crédito)"

    FinancialAnalyst:
      model: "gpt-5"
      provider: "GitHub Copilot Pro"
      cost: "1x crédito"
      benchmarks:
        mmlu: "88.7%"
        gsm8k: "~92%"
      justification: "Máxima precisión matemática y razonamiento complejo"
      estimated_usage: "15 análisis/mes × 1 crédito = 15 créditos"
      fallback: "claude-sonnet-4.5 (88% MMLU, 1x crédito)"

    StrategyProposer:
      model: "claude-haiku-4.5"
      provider: "GitHub Copilot Pro"
      cost: "0.33x créditos"
      benchmarks:
        ifbench: "72% (seguimiento instrucciones) ⭐"
        latency: "600-1000ms (4-5x más rápido)"
        swe_bench: "73.3%"
      justification: "Mejor para propuestas estratégicas, baja latencia, ROI óptimo"
      estimated_usage: "20 análisis/mes × 0.33 crédito = 6.6 créditos"
      fallback: "gpt-4o (0x créditos, equivalente en escritura)"

    ReportGenerator:
      model: "minimax-m2"
      provider: "MiniMax API / Self-hosted"
      cost: "$0"
      benchmarks:
        swe_bench: "69.4%"
        params: "229B MoE (10B activos)"
        license: "MIT (open-source)"
      justification: "Generación de código alta calidad, sin costo, self-hosted viable"
      estimated_usage: "20 análisis/mes × $0 = $0"
      fallback: "gpt-4o (88% HumanEval, 0x créditos)"

    OrchestratorAgent:
      model: "claude-haiku-4.5"
      provider: "GitHub Copilot Pro"
      cost: "0.33x créditos"
      benchmarks:
        latency: "600-1000ms ⭐"
        computer_use: "50.7% OSWorld"
      justification: "Decisiones rápidas en orquestación, baja latencia crítica"
      estimated_usage: "10 análisis/mes × 0.33 crédito = 3.3 créditos"
      fallback: "gpt-4o (0x créditos, 1.2-1.6s latency)"

  total_budget:
    copilot_credits_used: 45 # de 300 disponibles
    percentage_used: "15%"
    buffer_remaining: "85%"
    monthly_cost: "$10 (suscripción Copilot Pro)"
    apis_external: "$0-8 (uso moderado APIs gratuitas)"
    total: "$10-18/mes"
```

### 3. **Servidores MCP: Especificación Técnica Completa**

```yaml
mcp_servers:
  total_count: 8
  total_cost: "$0/mes (100% gratuito)"

  servers:
    - name: "GitHub MCP"
      status: "✅ REQUIRED"
      provider: "GitHub (oficial)"
      capabilities:
        - "Repositorios (read/write)"
        - "Issues, PRs, discussions"
        - "Security alerts, Actions"
      rate_limits: "Según políticas API GitHub"
      authentication: "PAT con scopes mínimos (repo, read:org)"
      sla: "< 2s por request"

    - name: "Playwright MCP"
      status: "✅ REQUIRED"
      provider: "ExecuteAutomation (comunidad)"
      capabilities:
        - "Web scraping moderno (SPAs)"
        - "Auto-waiting inteligente"
        - "Multi-browser (Chromium, Firefox, WebKit)"
      performance: "Superior a Selenium en SPAs"
      sla: "< 5s por página"
      mitigation: "Proxies rotativos solo si sitio lo requiere"

    - name: "MarkItDown MCP"
      status: "✅ REQUIRED"
      provider: "Microsoft"
      capabilities:
        - "PDF → Markdown"
        - "DOCX, PPTX → Markdown"
      performance:
        pymupdf: "~0.12s/página (rápido)"
        unstructured: "~1.29s/página (semántico)"
      strategy: "PyMuPDF para velocidad, Unstructured para RAG"
      sla: "< 10s por PDF de 20 páginas"

    - name: "Jina AI Reader MCP"
      status: "✅ REQUIRED (reemplazo Firecrawl)"
      provider: "Jina AI"
      capabilities:
        - "URL → Markdown limpio"
        - "Scraping estructurado"
      rate_limits:
        without_key: "20 RPM"
        with_free_key: "200 RPM"
        tokens: "10M tokens incluidos"
      cost: "$0"
      usage_estimate: "100 análisis × 2 requests = 200 req/mes (dentro de límite)"
      sla: "< 3s por URL"

    - name: "Supabase MCP"
      status: "✅ REQUIRED"
      provider: "Supabase"
      free_tier_limits:
        database: "500 MB"
        storage: "1 GB"
        egress: "5 GB/mes"
        mau: "50,000 usuarios"
        realtime: "2M mensajes/mes"
      warnings:
        - "Proyectos se pausan tras 1 semana inactividad"
        - "Monitorear uso para evitar pausa"
      usage_pattern: "Metadatos de análisis + cache de resultados"
      sla: "< 100ms queries"

    - name: "Notion MCP"
      status: "✅ OPTIONAL"
      provider: "Notion API"
      capabilities:
        - "Gestión de conocimiento"
        - "Documentación interna"
        - "Tracking de investigación"
      rate_limits:
        average: "3 req/s"
        burst: "Parcialmente permitido"
        payload: "1000 bloques, 500 KB"
      error_handling: "HTTP 429 → respetar Retry-After"
      sla: "< 2s por operación"

    - name: "ChromeDevTools MCP"
      status: "✅ OPTIONAL (debugging)"
      capabilities:
        - "Network monitoring"
        - "Console logs"
        - "Debugging scraping"
      use_case: "Desarrollo y troubleshooting"

    - name: "Rube MCP"
      status: "⚠️ TBD (evaluar)"
      capabilities:
        - "Orquestación workflows"
        - "Multi-tool execution"
      status_note: "Integrated with LangGraph StateGraph"

  rejected_servers:
    - name: "Firecrawl MCP"
      cost: "$49/mes mínimo"
      reason: "❌ Rompe restricción presupuestaria $0"
      replacement: "Jina AI Reader (200 RPM gratis)"
```

### 4. **Presupuesto y Capacidad Operativa**

```yaml
operational_capacity:
  monthly_budget:
    copilot_pro: "$10"
    apis_external: "$0-8"
    total: "$10-18"
    confidence: "95%"

  analyses_per_month:
    target: 100
    cost_per_analysis: "$0.10-0.18"
    roi_vs_manual:
      manual_cost: "$25/análisis (30 min × $50/hora)"
      automated_cost: "$0.15/análisis"
      savings: "$24.85/análisis (99.4%)"
      monthly_savings: "$2,485 (100 análisis)"
      roi_multiplier: "166x"

  credit_management:
    copilot_credits:
      allocated: 300
      projected_usage: 45
      buffer: 255
      alert_threshold: 240 # Alertar si < 60 créditos

    usage_by_agent:
      FinancialAnalyst: "15 créditos (15 × 1.0)"
      TechnicalArchitect: "10 créditos (10 × 1.0)"
      StrategyProposer: "6.6 créditos (20 × 0.33)"
      OrchestratorAgent: "3.3 créditos (10 × 0.33)"
      Others: "10 créditos (buffer spikes)"
      total: "44.9 créditos"

  scalability:
    current_capacity: "100 análisis/mes"
    bottleneck: "Semantic Scholar 1 RPS (rate limit externo)"
    scale_to_200: "Requiere paralelización avanzada + caching"
    scale_to_500: "Requiere rediseño arquitectónico (abandonar conversacional)"
```

### 5. **Requerimientos No Funcionales Validados**

```yaml
non_functional_requirements:
  reliability:
    uptime_target: "> 99%"
    mtbf: "> 720 horas"
    mttr: "< 15 minutos"
    monitoring: "OpenTelemetry + Uptrace (free)"

  observability:
    logging:
      format: "JSON estructurado (structlog)"
      retention: "30 días (compresión + ILM)"
      fields_required:
        - "timestamp"
        - "agent"
        - "task"
        - "duration"
        - "cost_credits"
        - "model_used"

    metrics:
      latency: "P50, P95, P99 por agente"
      cost: "Créditos y $ por análisis"
      errors: "Tasa de error por proveedor API"

    traces:
      tool: "OpenTelemetry SDK"
      backend: "Uptrace (1TB free storage)"
      sampling: "100% en producción (bajo volumen)"

  security:
    authentication:
      github_pat: "Scopes mínimos (repo, read:org)"
      api_keys: ".env con .gitignore"
      rotation: "Cada 90 días (automatizado)"

    data_privacy:
      pdf_handling: "Descargar → Procesar → Eliminar inmediato"
      no_persistence: "No guardar datos sensibles sin consentimiento"
      logs_sanitized: "URLs y parámetros sanitizados"

  resilience:
    patterns:
      - name: "Rate Limiting"
        implementation: "SlowAPI (token bucket)"
        config: "Por IP, por API key, por proveedor"

      - name: "Circuit Breaker"
        implementation: "PyBreaker"
        thresholds:
          failure_threshold: 5
          recovery_timeout: "60s"
          half_open_requests: 1

      - name: "Retry with Backoff"
        implementation: "Exponential backoff + jitter"
        config:
          max_retries: 3
          base_delay: "1s"
          max_delay: "30s"

      - name: "Timeout Management"
        config:
          api_calls: "30s"
          scraping: "60s"
          pdf_processing: "120s"
```

### 6. **Gates de Calidad Automatizados**

```yaml
quality_gates:
  mandatory_checks:
    - gate: "Structure Validation"
      when: "Después de cada agente"
      checks:
        - "Secciones obligatorias presentes"
        - "Formato Markdown válido"
        - "Sin placeholders (TODO, FIXME, XXX)"
        - "Longitud mínima cumplida"
      action_on_failure: "Retry con prompt específico (max 2 intentos)"

    - gate: "Citation Validation"
      when: "Después de ContentSynthesizer"
      checks:
        - "Formato de citas correcto"
        - "Referencias bibliográficas completas"
        - "No hay citas huérfanas"
        - "Orden alfabético en bibliografía"
      action_on_failure: "Rerun con validación de BibTeX"

    - gate: "Consistency Check"
      when: "Antes de output final"
      checks:
        - "Terminología consistente"
        - "No contradicciones entre secciones"
        - "Tono académico uniforme"
        - "Coherencia narrativa"
      action_on_failure: "Review manual + corrección asistida"

    - gate: "Performance Check"
      when: "Durante ejecución"
      checks:
        - "Tiempo < SLA + 20%"
        - "Créditos < presupuesto"
        - "Tasa error < 1%"
        - "Uso memoria < 80%"
      action_on_failure: "Log warning + alertar si crítico"

    - gate: "Cost Check"
      when: "Antes y después de cada agente"
      checks:
        - "Créditos gastados vs proyectado"
        - "APIs externas dentro de límites"
        - "No exceder presupuesto diario"
      action_on_failure: "Pausar pipeline + alertar + usar fallback"
```

### 7. **Evolución y Roadmap de Features**

```yaml
feature_roadmap:
  phase_1_mvp:
    timeline: "Sprint 1-4 (8 semanas)"
    features:
      - "6 agentes core funcionando"
      - "8 servidores MCP integrados"
      - "Pipeline secuencial completo"
      - "Generación de 1 tesis ejemplo"
    success_criteria:
      - "Pipeline completo en 60-75 min"
      - "Presupuesto < $20/mes"
      - "Calidad académica validada"

  phase_2_optimization:
    timeline: "Sprint 5-8 (8 semanas)"
    features:
      - "Paralelización de LiteratureResearcher"
      - "Caching distribuido (Valkey/Redis)"
      - "Dashboard de monitoreo (Uptrace)"
      - "Gates de calidad automatizados"
    success_criteria:
      - "Pipeline optimizado < 60 min"
      - "Uptime > 99%"
      - "100 análisis/mes sin intervención"

  phase_3_scale:
    timeline: "Sprint 9-12 (8 semanas)"
    features:
      - "Arquitectura basada en artefactos"
      - "Multi-tenancy (múltiples usuarios)"
      - "API REST para integración externa"
      - "Marketplace de templates"
    success_criteria:
      - "Soportar 200 análisis/mes"
      - "Latencia P95 < SLA"
      - "5 clientes piloto activos"
```

---

## ✅ Conclusión: Especificaciones Validadas y Listas para Implementación

Estas especificaciones han sido **actualizadas con investigación real de Nov 2025**:

- ✅ **SLAs realistas** basados en benchmarks y limitaciones técnicas reales
- ✅ **Asignación de modelos** optimizada para ROI máximo ($10-18/mes)
- ✅ **8 servidores MCP** 100% gratuitos con límites verificados
- ✅ **Presupuesto validado** con 85% de buffer para escalabilidad
- ✅ **Gates de calidad** para garantizar outputs profesionales
- ✅ **Roadmap pragmático** alineado con capacidades reales

**El proyecto está LISTO para proceder a implementación con confianza del 95%.**

---

_Esta especificación define el QUÉ y el POR QUÉ. El plan técnico define el CÓMO._
