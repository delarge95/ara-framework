# 🤖 ARA Framework - Academic Research Automation

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![CrewAI 0.100.0](https://img.shields.io/badge/CrewAI-0.100.0-green.svg)](https://github.com/joaomdmoura/crewAI)
[![Groq LLaMA 3.3-70B](https://img.shields.io/badge/LLM-Groq%20LLaMA%203.3--70B-orange.svg)](https://groq.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Sistema multi-agente inteligente para automatización completa de investigación académica**: desde análisis de nicho hasta generación de documentos técnicos profesionales.

---

## 📋 Tabla de Contenidos

- [🎯 Características Principales](#-características-principales)
- [🏗️ Arquitectura](#️-arquitectura)
- [🚀 Inicio Rápido](#-inicio-rápido)
- [⚙️ Configuración](#️-configuración)
- [🤖 Agentes del Sistema](#-agentes-del-sistema)
- [🛠️ Herramientas Integradas](#️-herramientas-integradas)
- [📊 Modelos LLM Soportados](#-modelos-llm-soportados)
- [💡 Uso](#-uso)
- [🧪 Testing](#-testing)
- [📁 Estructura del Proyecto](#-estructura-del-proyecto)
- [🤝 Contribuir](#-contribuir)
- [📄 Licencia](#-licencia)

---

## 🎯 Características Principales

### ✨ Pipeline Completo de Investigación Automatizada
- **Análisis de Nicho**: Evaluación automática de viabilidad, tendencias y oportunidades
- **Revisión de Literatura**: Búsqueda y análisis de papers académicos (Semantic Scholar, arXiv)
- **Arquitectura Técnica**: Diseño de sistemas con mejores prácticas y patrones modernos
- **Plan de Implementación**: Roadmap detallado con sprints y estimaciones
- **Documentación Final**: Generación de reportes técnicos profesionales en Markdown

### 🧠 Sistema Multi-Agente con CrewAI
- **5 Agentes Especializados** trabajando en colaboración secuencial
- **Memoria de Largo Plazo** con ChromaDB para contexto entre agentes
- **Razonamiento Avanzado** con LLaMA 3.3-70B (70 billones de parámetros)
- **Monitoreo en Tiempo Real** con detección automática de bloqueos

### 💰 Integración LLM Flexible y Económica
- **Groq (100% GRATIS)**: LLaMA 3.3-70B ultra rápido (750+ tokens/seg)
- Soporte para **OpenAI GPT-4o/GPT-5**, **Claude Sonnet 4.5**, **Gemini 2.5 Pro**
- Configuración vía **LiteLLM** (cambio de modelo en 1 línea)
- **Budget Manager** para control de costos y límites

### 🔧 Herramientas Avanzadas
- **Web Scraping** (Playwright MCP) con JavaScript rendering
- **Búsqueda Académica** (Semantic Scholar API) con filtros avanzados
- **Procesamiento de PDFs** (MarkItDown MCP) con extracción de secciones
- **Base de Datos** (Redis + Supabase opcional) para persistencia

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                    ARA FRAMEWORK PIPELINE                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐     │
│  │   Agent 1    │───▶│   Agent 2    │───▶│   Agent 3    │     │
│  │Niche Analyst │    │ Literature   │    │ Technical    │     │
│  │              │    │ Researcher   │    │ Architect    │     │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘     │
│         │                    │                    │              │
│         ▼                    ▼                    ▼              │
│  ┌──────────────────────────────────────────────────────┐      │
│  │         ChromaDB Memory (Context Retention)          │      │
│  └──────────────────────────────────────────────────────┘      │
│         │                    │                    │              │
│         ▼                    ▼                    ▼              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐     │
│  │   Agent 4    │───▶│   Agent 5    │───▶│   OUTPUT     │     │
│  │Implementation│    │   Content    │    │  Final.md    │     │
│  │ Specialist   │    │ Synthesizer  │    │              │     │
│  └──────────────┘    └──────────────┘    └──────────────┘     │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│                     TOOLS & INTEGRATIONS                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  🌐 Web Scraping  │  🔍 Academic Search  │  📄 PDF Processing   │
│  💾 Database      │  🤖 Groq LLM API     │  📊 Budget Manager   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Tech Stack**:
- **Framework**: CrewAI 0.100.0 (orchestration multi-agente)
- **LLM**: Groq LLaMA 3.3-70B via LiteLLM
- **Memory**: ChromaDB (embeddings) + Redis (cache)
- **Tools**: Playwright MCP, Semantic Scholar, MarkItDown MCP
- **Languages**: Python 3.12+

---

## 🚀 Inicio Rápido

### Prerrequisitos
- Python 3.12 o superior
- Git
- API Key de Groq (gratis en [console.groq.com](https://console.groq.com))

### Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/delarge95/ara-framework.git
cd ara-framework/ara_framework

# 2. Crear entorno virtual
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env y agregar tu GROQ_API_KEY
```

### Primer Test

```bash
# Ejecutar test simple
python test_simple.py

# Ejecutar pipeline completo con monitoreo
python test_monitored_realtime.py
```

**Salida esperada** (53-63 minutos):
```
[18:45:00] === INICIO TEST E2E CON MONITOREO ===
[18:45:00] Niche: Rust WebAssembly for real-time audio processing
[18:45:02] Agent 1 (NicheAnalyst) starting...
[18:52:15] Agent 1 completed ✓
[18:52:16] Agent 2 (LiteratureResearcher) starting...
...
[19:38:45] ✅ TEST COMPLETADO EXITOSAMENTE
[19:38:45] Reporte guardado: outputs/Rust_WebAssembly_20251110_184500.md
```

---

## ⚙️ Configuración

### Variables de Entorno (`.env`)

```bash
# === LLM API Keys (elegir UNO) ===

# Opción 1: Groq (GRATIS - Recomendado)
GROQ_API_KEY=gsk_tu_api_key_aqui

# Opción 2: OpenAI (Pago)
OPENAI_API_KEY=sk-proj-tu_api_key_aqui

# Opción 3: Anthropic Claude (Pago)
ANTHROPIC_API_KEY=sk-ant-tu_api_key_aqui

# Opción 4: Google Gemini (Cuota gratis limitada)
GEMINI_API_KEY=AIzaSy_tu_api_key_aqui

# === Database (Opcional) ===
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Supabase (opcional para persistencia)
SUPABASE_URL=https://tu_proyecto.supabase.co
SUPABASE_KEY=eyJhbGc_tu_anon_key_aqui
```

### Cambiar de Modelo LLM

Editar `agents/niche_analyst.py` (y otros 4 agentes):

```python
# Groq (GRATIS)
llm_model = "groq/llama-3.3-70b-versatile"

# OpenAI
llm_model = "openai/gpt-4o-mini"  # Económico
llm_model = "openai/gpt-5"         # Más potente

# Anthropic
llm_model = "anthropic/claude-sonnet-4.5"

# Google
llm_model = "gemini/gemini-2.5-pro"
```

**Nota**: CrewAI usa **LiteLLM** internamente, por lo que cualquier modelo soportado por LiteLLM funcionará con el formato `provider/model-name`.

---

## 🤖 Agentes del Sistema

### 1️⃣ **Niche Analyst** (`niche_analyst.py`)
**Rol**: Analista de mercado y tendencias  
**Objetivo**: Evaluar viabilidad del nicho de investigación  
**Tools**: Scraping, Search  
**Salida**: Análisis SWOT, tendencias, oportunidades  
**Tiempo**: ~7-8 minutos

### 2️⃣ **Literature Researcher** (`literature_researcher.py`)
**Rol**: Investigador académico PhD  
**Objetivo**: Revisión exhaustiva de literatura científica  
**Tools**: Search, PDF, Database  
**Salida**: 10-15 papers relevantes con análisis crítico  
**Tiempo**: ~12-15 minutos

### 3️⃣ **Technical Architect** (`technical_architect.py`)
**Rol**: Arquitecto de software senior  
**Objetivo**: Diseñar arquitectura técnica completa  
**Tools**: Scraping, PDF, Database  
**Salida**: Diagramas, stack tecnológico, patrones  
**Tiempo**: ~10-12 minutos

### 4️⃣ **Implementation Specialist** (`implementation_specialist.py`)
**Rol**: Líder técnico / Scrum Master  
**Objetivo**: Crear roadmap de implementación  
**Tools**: Scraping, Database  
**Salida**: Sprints, estimaciones, riesgos, milestones  
**Tiempo**: ~8-10 minutos

### 5️⃣ **Content Synthesizer** (`content_synthesizer.py`)
**Rol**: Editor técnico / Documentador  
**Objetivo**: Generar documento final profesional  
**Tools**: Database  
**Salida**: Markdown completo con todas las secciones integradas  
**Tiempo**: ~15-18 minutos

---

## 🛠️ Herramientas Integradas

### 🌐 ScrapingTool (`tools/scraping_tool.py`)
```python
# Capacidades:
- Scraping con JavaScript rendering (Playwright MCP)
- Extracción de contenido limpio (sin ads/scripts)
- Manejo de Single Page Applications (SPAs)
- Rate limiting y retries automáticos
```

### 🔍 SearchTool (`tools/search_tool.py`)
```python
# Fuentes:
- Semantic Scholar API (papers académicos)
- Filtros: año, citaciones, campos, autores
- Búsqueda paralela (hasta 5 queries simultáneas)
- Caché de resultados en Redis
```

### 📄 PDFTool (`tools/pdf_tool.py`)
```python
# Funciones:
- Conversión PDF → Markdown (MarkItDown MCP)
- Extracción de secciones específicas
- OCR para PDFs escaneados
- Batch processing (múltiples PDFs)
```

### 💾 DatabaseTool (`tools/database_tool.py`)
```python
# Almacenamiento:
- Redis (caché rápido para resultados intermedios)
- Supabase (opcional, persistencia long-term)
- Save/Load papers, análisis, reportes
```

---

## 📊 Modelos LLM Soportados

| Proveedor | Modelo | Costo | Tokens/min | Calidad | Recomendado |
|-----------|--------|-------|------------|---------|-------------|
| **Groq** | llama-3.3-70b-versatile | **$0.00** | 12,000 | ⭐⭐⭐⭐ | ✅ **SÍ** |
| Groq | llama-3.1-8b-instant | $0.00 | 50,000+ | ⭐⭐⭐ | Para tests rápidos |
| OpenAI | gpt-4o-mini | ~$0.15 | Variable | ⭐⭐⭐⭐ | Budget-friendly |
| OpenAI | gpt-5 | ~$3.00 | Variable | ⭐⭐⭐⭐⭐ | Máxima calidad |
| Anthropic | claude-sonnet-4.5 | ~$3.00 | Variable | ⭐⭐⭐⭐⭐ | Razonamiento largo |
| Google | gemini-2.5-pro | Cuota gratis | 15/min | ⭐⭐⭐⭐ | Cuota limitada |

**Recomendación**: Comenzar con **Groq LLaMA 3.3-70B** (100% gratis, excelente calidad).

**Investigación completa** en [`investigación perplexity/`](./investigación%20perplexity/) y [`investigación_minimax/`](./investigación_minimax/)

---

## 💡 Uso

### CLI Básico

```bash
# Test simple (un solo agente)
python test_simple.py

# Pipeline completo con monitoreo
python test_monitored_realtime.py

# Pipeline manual (paso a paso)
python test_pipeline_manual.py
```

### API Programática

```python
from core.pipeline import ResearchPipeline

# Inicializar pipeline
pipeline = ResearchPipeline(budget_limit=5.0)

# Ejecutar investigación
result = pipeline.run_analysis_sync(
    niche="Rust WebAssembly for real-time audio processing"
)

# Acceder a resultados
print(result.status)  # PipelineStatus.COMPLETED
print(result.final_document)  # Markdown completo
print(result.total_credits_used)  # 0.0 con Groq
```

### Personalizar Agentes

```python
# agents/custom_agent.py
from crewai import Agent

custom_agent = Agent(
    role="Custom Researcher",
    goal="Tu objetivo específico aquí",
    backstory="Contexto del agente...",
    llm="groq/llama-3.3-70b-versatile",
    tools=[scraping_tool, search_tool],
    verbose=True
)
```

---

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest tests/

# Test específico
pytest tests/test_pipeline.py -v

# Test con coverage
pytest --cov=ara_framework tests/

# Test de integración E2E (53-63 min)
python test_monitored_realtime.py
```

**Tests incluidos**:
- ✅ `test_pipeline.py` - Pipeline completo
- ✅ `test_tools.py` - Todas las herramientas
- ✅ `test_budget_manager.py` - Control de costos
- ✅ `test_api_connections.py` - Conectividad APIs

---

## 📁 Estructura del Proyecto

```
ara-framework/
├── ara_framework/                 # Framework principal
│   ├── agents/                    # 5 agentes especializados
│   │   ├── niche_analyst.py
│   │   ├── literature_researcher.py
│   │   ├── technical_architect.py
│   │   ├── implementation_specialist.py
│   │   └── content_synthesizer.py
│   ├── core/                      # Pipeline y lógica central
│   │   ├── pipeline.py
│   │   └── budget_manager.py
│   ├── tools/                     # Herramientas integradas
│   │   ├── scraping_tool.py
│   │   ├── search_tool.py
│   │   ├── pdf_tool.py
│   │   └── database_tool.py
│   ├── mcp_servers/               # Model Context Protocol servers
│   │   ├── playwright_mcp.py
│   │   ├── markitdown_mcp.py
│   │   └── semantic_scholar.py
│   ├── tests/                     # Suite de testing
│   ├── outputs/                   # Reportes generados
│   ├── .env.example               # Template de configuración
│   └── requirements.txt           # Dependencias Python
├── investigación perplexity/      # Investigación LLM pricing (Nov 2025)
├── investigación_minimax/         # Análisis técnico profundo
├── .gitignore
└── README.md                      # Este archivo
```

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! 

### Áreas de Mejora
- 🔧 **Nuevas herramientas**: Integración con más APIs (arXiv, PubMed, etc.)
- 🤖 **Agentes adicionales**: Code Generator, Testing Agent, Deployment Agent
- 🌐 **Internacionalización**: Soporte multi-idioma
- 📊 **UI/Dashboard**: Interfaz web para monitoreo en tiempo real
- ⚡ **Optimizaciones**: Paralelización de agentes, caché inteligente

### Workflow
1. Fork el repositorio
2. Crear branch: `git checkout -b feature/nueva-funcionalidad`
3. Commit cambios: `git commit -m 'feat: Agregar nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Abrir Pull Request

---

## 📄 Licencia

Este proyecto está bajo la licencia **MIT**. Ver [LICENSE](LICENSE) para más detalles.

---

## 🙏 Agradecimientos

- **CrewAI** - Framework multi-agente excepcional
- **Groq** - LLM ultrarrápido y gratuito
- **Semantic Scholar** - API académica de alta calidad
- **Playwright** - Scraping moderno con JavaScript rendering
- **LiteLLM** - Abstracción unificada para LLMs

---

## 📞 Contacto

- **GitHub**: [@delarge95](https://github.com/delarge95)
- **Repo**: [ara-framework](https://github.com/delarge95/ara-framework)
- **Issues**: [Reportar bugs/sugerencias](https://github.com/delarge95/ara-framework/issues)

---

<div align="center">

**⭐ Si este proyecto te resulta útil, considera darle una estrella en GitHub ⭐**

Hecho con ❤️ por la comunidad de investigación académica

</div>
