# 🤖 ARA Framework - Academic Research Automation

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![LangGraph 1.0+](https://img.shields.io/badge/LangGraph-1.0+-green.svg)](https://github.com/langchain-ai/langgraph)
[![Groq LLaMA 3.3-70B](https://img.shields.io/badge/LLM-Groq%20LLaMA%203.3--70B-orange.svg)](https://groq.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Last Updated](https://img.shields.io/badge/Updated-Dec_2025-blue.svg)](#)

> **Sistema multi-agente inteligente para automatización completa de investigación académica**: desde análisis de nicho hasta generación de documentos técnicos profesionales.

> ⚠️ **MIGRATED TO LANGGRAPH (Nov 2025)**: This framework has been upgraded from CrewAI to LangGraph, the industry-leading production-ready framework used by Uber, LinkedIn, Replit, and Elastic.

---

## 🚀 Inicio Rápido

```bash
# 1. Clonar repositorio
git clone https://github.com/delarge95/ara-framework.git
cd ara-framework

# 2. Configurar entorno (Python 3.12+ requerido)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o .\venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 3. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus API keys (mínimo GROQ_API_KEY)

# 4. Ejecutar setup y validación
python scripts/validate_setup.py

# 5. Ejecutar pipeline de investigación
python -m ara_framework.cli.main --domain "AI in Healthcare" --focus "market_analysis"
```

**Resultado**: Reporte de investigación completo en `output/final_report.md`

---

## 🎯 Características Principales

### ✨ Pipeline Completo de Investigación Automatizada
- **Análisis de Nicho**: Evaluación automática de viabilidad, tendencias y oportunidades
- **Revisión de Literatura**: Búsqueda y análisis de papers académicos (Semantic Scholar, arXiv)
- **Arquitectura Técnica**: Diseño de sistemas con mejores prácticas y patrones modernos
- **Plan de Implementación**: Roadmap detallado con sprints y estimaciones
- **Documentación Final**: Generación de reportes técnicos profesionales en Markdown

### 🧠 Sistema Multi-Agente con LangGraph
- **5 Agentes Especializados** trabajando en colaboración secuencial
- **Graph-based Architecture** con control de flujo explícito
- **Built-in Checkpointing** para pausar y reanudar ejecución
- **Razonamiento Avanzado** con LLaMA 3.3-70B (70 billones de parámetros)
- **Production-Ready** con escalabilidad empresarial probada

### 💰 Integración LLM Flexible y Económica
- **Groq (100% GRATIS)**: LLaMA 3.3-70B ultra rápido (750+ tokens/seg)
- Soporte para **OpenAI GPT-4o**, **Claude Sonnet 3.5**, **Gemini Pro**
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
│  │         Memory & Context Management                   │      │
│  └──────────────────────────────────────────────────────┘      │
│         │                    │                    │              │
│         ▼                    ▼                    ▼              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐     │
│  │   Agent 4    │    │   Agent 5    │    │    Final     │     │
│  │Implementation│    │   Content    │    │   Report     │     │
│  │ Specialist   │    │ Synthesizer  │    │  Generator   │     │
│  └──────────────┘    └──────────────┘    └──────────────┘     │
└─────────────────────────────────────────────────────────────────┘
│  │  ProjectManager (Orquestador)                    │  │
│  │  • Delega tareas a agentes                       │  │
│  │  • Gestiona budget de modelos                    │  │
│  │  • Valida calidad en cada fase                   │  │
│  └─────────────────────────────────────────────────┘  │
│                                                         │
│  ┌───────┐   ┌────────┐   ┌────────┐   ┌─────────┐   │
│  │ Niche │ → │ Liter. │ → │ Tech.  │ → │ Content │   │
│  │Analyst│   │Researcher   │Architect   │Synthesis│   │
│  └───────┘   └────────┘   └────────┘   └─────────┘   │
│      ↓            ↓            ↓             ↓        │
│  MiniMax-M2  Gemini 2.5    GPT-5       Claude 4.5     │
│  (MIT OSS)   Pro (gratis)  (Copilot)   Sonnet (Cop.)  │
└────────────────────┬────────────────────────────────────┘
                     │ MCP Protocol
                     ▼
┌─────────────────────────────────────────────────────────┐
│  CAPA 3: TOOLS & INTEGRATIONS                          │
│                                                         │
│  MCP SERVERS (100% Gratuitos):                         │
│  ┌──────────┐ ┌───────────┐ ┌──────────┐             │
│  │ GitHub   │ │ Playwright│ │MarkItDown│             │
│  │ Repos    │ │ Browser   │ │ PDF→MD   │             │
│  └──────────┘ └───────────┘ └──────────┘             │
│  ┌──────────┐ ┌───────────┐ ┌──────────┐             │
│  │ Supabase │ │  Notion   │ │Jina AI   │             │
│  │ 500MB DB │ │ Knowledge │ │ Reader   │             │
│  └──────────┘ └───────────┘ └──────────┘             │
│                                                         │
│  AGENTIC EDITORS (Activos):                            │
│  • Cursor Pro ($20/mes) → Multi-file editing + GPT-5   │
│  • GitHub Copilot Pro ($10/mes) → Todos los modelos    │
└─────────────────────────────────────────────────────────┘
```

---

## 🧠 Los 6 Agentes Especializados

### 1. 📊 **NicheAnalyst**

- **Rol**: Analista de mercado y tendencias
- **Herramientas**: Playwright MCP, Jina AI Reader (20 req/min gratis)
- **Modelos**: GPT-4o (0x) → MiniMax-M2 (229B OSS, elite agentic) → Grok Code Fast
- **Output**: Análisis competitivo, gaps de mercado, oportunidades de nicho

### 2. 📚 **LiteratureResearcher**

- **Rol**: Investigador de literatura académica
- **Herramientas**: MarkItDown MCP, Jina AI Reader, Semantic Scholar
- **Modelos**: Gemini 2.5 Pro (1M ctx, gratis AI Studio) → MiniMax-M2 → DeepSeek V3
- **Output**: 20-30 papers relevantes, síntesis de literatura científica

### 3. 💰 **FinancialAnalyst**

- **Rol**: Analista financiero y de mercado
- **Herramientas**: Playwright MCP, GitHub MCP
- **Modelos**: GPT-5 (1x) → DeepSeek V3 (gratis backup)
- **Output**: Análisis de viabilidad, proyecciones financieras

### 4. 🎯 **StrategyProposer**

- **Rol**: Estratega de negocio
- **Herramientas**: Notion MCP, Supabase MCP
- **Modelos**: Claude Sonnet 4.5 (1x, mejor escritura estratégica)
- **Output**: Propuestas de entrada al mercado, estrategias diferenciadas

### 5. 📝 **ReportGenerator**

- **Rol**: Generador de informes finales
- **Herramientas**: Notion MCP, MarkItDown MCP
- **Modelos**: GPT-5-Codex (1x) → MiniMax-M2 (elite coding) → Qwen 2.5 Coder
- **Output**: Documento final estructurado, con código y diagramas

### 6. 🎛️ **OrchestratorAgent**

- **Rol**: Coordinador del flujo multi-agente
- **Herramientas**: Todos los MCP servers
- **Modelos**: GPT-5 (1x) → GPT-4o (0x backup)
- **Output**: Coordinación de tareas, validación de calidad, gestión de budget

---

## 📦 Tech Stack Completo

### Backend (Python)

```yaml
orchestration:
  crewai: ^0.70.0 # Multi-agent framework
  fastapi: ^0.109.0 # API framework
  pydantic: ^2.5.0 # Data validation

llm_clients:
  openai: ^1.10.0 # GPT-5, GPT-5-Codex, GPT-4o (via Copilot Pro)
  anthropic: ^0.8.0 # Claude Sonnet 4.5, Haiku 4.5 (via Copilot Pro)
  google_generativeai: ^0.3.0 # Gemini 2.5 Pro (gratis via AI Studio)
  # Custom clients para modelos gratuitos/open-source:
  minimax_m2: custom # 229B total, 10B activado, MIT OSS, elite agentic
  deepseek_v3: custom # Free API, 128K context

mcp_integration:
  mcp_client: ^1.0.0 # Cliente para MCP servers
  # Adaptadores para: GitHub, Playwright, MarkItDown, etc.

tools:
  playwright: ^1.40.0 # Solo para custom needs
  arxiv: ^2.1.0 # Academic search
  semantic_scholar: ^0.8.0
  pyzmq: ^25.1.0 # Blender control

storage:
  supabase: ^2.0.0 # Database + file storage
```

### Frontend (Next.js)

```yaml
framework:
  next: 14.0.0 # App Router
  react: ^18.2.0
  typescript: ^5.0.0

ui:
  shadcn_ui: latest # Component library
  tailwindcss: ^3.3.0
  lucide_icons: latest # Icon set

features:
  zustand: ^4.4.0 # State management
  socket_io: ^4.6.0 # WebSocket (realtime)
  novel: ^0.1.0 # Notion-style editor
  react_pdf: ^7.0.0 # PDF export
  recharts: ^2.10.0 # Charts
```

---

## 🔌 MCP Servers Integrados

**ARA usa 8 MCP servers** ya instalados en VS Code:

| Server                 | Proveedor | Uso en ARA                           |
| ---------------------- | --------- | ------------------------------------ |
| **GitHub MCP**         | Official  | Búsqueda de código, ejemplos, issues |
| **Playwright MCP**     | Microsoft | Web scraping dinámico                |
| **MarkItDown MCP**     | Microsoft | Conversión PDF → Markdown            |
| **Supabase MCP**       | Official  | Base de datos + storage              |
| **Notion MCP**         | Official  | Documentación estructurada           |
| **Firecrawl MCP**      | Firecrawl | Extracción web estructurada          |
| **ChromeDevTools MCP** | Official  | Debugging de web apps                |
| **Rube MCP**           | Rube      | [Pendiente definir uso]              |

> 💡 **No necesitas instalarlos**: Si ya tienes estos servers en VS Code, ARA se conecta automáticamente via el protocolo MCP.

---

## 🏠 Ollama - Desarrollo Local Sin Límites

**NUEVO**: ARA ahora soporta **Ollama** para desarrollo local ilimitado.

### ¿Por Qué Ollama?

Durante el desarrollo, GitHub Models tiene un límite de **50 requests/día**. Con Ollama:

- ✅ **Requests ilimitados** (inferencia local)
- ✅ **$0 costo** (sin API keys)
- ✅ **Tool calling funcional** (verificado con 4/4 tests)
- ⚠️ **Calidad ligeramente inferior** a gpt-4o (aceptable para desarrollo)

### Modelo Usado: Mistral 7B v0.3

```yaml
modelo: mistral:7b
parametros: 7B
context_window: 32K tokens
tool_calling: ✅ Confirmado (documentación oficial Ollama)
tamaño: 4.4GB
velocidad: ~2x más lento que gpt-4o (6-8 min vs 3-5 min)
```

### Uso Rápido

```bash
# 1. Asegurarse que Ollama está corriendo
ollama serve

# 2. Usar Ollama en vez de GitHub Models
$env:USE_OLLAMA="true"
python main.py

# 3. Volver a GitHub Models
$env:USE_OLLAMA="false"
python main.py
```

### Estrategia Recomendada: Híbrida

```bash
# Desarrollo e iteración (sin límites)
USE_OLLAMA=true python main.py  # Ejecutar N veces

# Validación final (máxima calidad)
USE_OLLAMA=false python main.py  # Antes de entregar
```

### Tests Disponibles

```bash
# Test rápido (~3-5 min)
python test_ollama_quick.py

# Comparación completa GitHub vs Ollama (~15 min)
python test_ollama_vs_github.py
```

**Documentación completa**: Ver `OLLAMA_QUICKSTART.md` y `GUIA_OLLAMA.md`

---

## 💰 Gestión Inteligente de Créditos

ARA incluye un **Budget Manager** que optimiza costos:

### Estrategia Multi-Modelo

```python
# Prioridad 0: Modelos gratuitos (usar siempre que sea posible)
• MiniMax M.2 (free, 8K context)
• DeepSeek V3 (free, 64K context)

# Prioridad 1: Créditos de editores agénticos
• Cline (Claude 3.5) → ~500K tokens disponibles
• Cursor (GPT-4) → ~300K tokens disponibles
• Windsurf (Cascade) → ~400K tokens disponibles

# Prioridad 2: Créditos limitados
• GitHub Copilot Pro (GPT-4) → ~200K tokens (reservar)

# Prioridad 3: Pago por uso (último recurso)
• OpenAI API Direct → $0.01 per 1K tokens
```

### Costo Estimado por Tesis

```
Total: ~$1.50 USD por tesis de 80 páginas

Breakdown:
• NicheAnalyst:         $0.00 (MiniMax M.2)
• LiteratureResearcher: $0.00 (DeepSeek V3)
• TechnicalArchitect:   $0.25 (GPT-4 via Cursor)
• CodeImplementation:   $0.12 (Claude via Cline)
• ContentSynthesizer:   $0.30 (Claude via Cline)
• DocumentationAgent:   $0.00 (MiniMax M.2)
```

**Comparativa**:

- Tesis manual: $5,000 USD (tiempo + herramientas + asesorías)
- Tesis con ARA: $1.50 USD (**99.97% de ahorro**)

---

## 📚 Documentación Completa

El proyecto tiene **2 niveles de documentación**:

### 1. Documentación del Sistema (para desarrolladores)

```
ara_framework/docs/
├── PROJECT_CONSTITUTION.md          # Principios y estándares
├── PROJECT_SPEC.md                  # Especificación funcional
├── TECHNICAL_PLAN.md                # Plan de implementación original
├── ARCHITECTURE_v2_MCP_MULTIMODEL.md # ✨ Arquitectura actualizada
├── PROBLEM_CORE_REDEFINITION.md     # ✨ Núcleo problemático redefinido
├── TASKS.md                         # Roadmap de tareas
└── GETTING_STARTED.md               # Guía de instalación
```

### 2. Meta-Documentación (tu tesis de grado)

```
tesis_principal/
├── capitulos/
│   ├── 01_introduccion.md           # Contexto y estado del arte
│   ├── 02_nucleo_problematico.md    # Definición del problema
│   ├── 03_marco_teorico.md          # CrewAI, MCP, editores agénticos
│   ├── 04_metodologia.md            # Diseño del sistema
│   ├── 05_implementacion.md         # Código y arquitectura
│   ├── 06_casos_de_uso.md           # 3 tesis generadas como ejemplos
│   ├── 07_validacion.md             # Métricas y benchmarks
│   ├── 08_resultados.md             # Análisis de calidad
│   ├── 09_conclusiones.md           # Logros y limitaciones
│   └── 10_anexos.md                 # Código fuente, configs
├── assets/
├── bibliografia/
└── tesis_final.pdf
```

---

## 🎯 Casos de Uso Reales

### Ejemplo 1: Tesis de Marketing Digital

**Input**:

```bash
python -m ara_framework.main \
  --domain "Marketing Digital" \
  --company "Absolut Vodka" \
  --focus "Experiencia Web 3D Interactiva" \
  --length 80
```

**Output** (45 minutos después):

```
outputs/absolut_vodka_thesis_20250104/
├── thesis_complete.md              # 85 páginas
├── thesis_complete.pdf             # Exportado a PDF
├── chapters/
│   ├── 01_introduction.md
│   ├── 02_literature_review.md
│   ├── 03_methodology.md
│   ├── 04_implementation.md
│   └── 05_conclusions.md
├── assets/
│   ├── architecture_diagram.svg
│   ├── competitor_analysis.png
│   └── 3d_bottle_render.png
├── code/
│   └── threejs_implementation.js
├── execution_log.json              # Para tu tesis principal
└── metrics.json                    # Tiempo, costos, agentes
```

**Métricas**:

- ⏱️ Tiempo total: 43 minutos
- 💰 Costo: $1.52 USD
- 📚 Papers citados: 28
- 🎨 Assets generados: 7 (5 imágenes, 2 modelos 3D)
- ⭐ Calidad (evaluación humana): 8.2/10

---

## 🛠️ Instalación Detallada

### Prerequisitos

- Python 3.11+
- Node.js 18+ (para frontend)
- Git
- VS Code (opcional, para MCP servers)

### 1. Backend (Python)

```bash
# Clonar repo
git clone https://github.com/tu-usuario/ara_framework.git
cd ara_framework

# Crear entorno virtual
python -m venv venv

# Activar (Windows PowerShell)
.\venv\Scripts\activate

# Activar (Linux/Mac)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Para desarrollo

# Instalar Playwright browsers
playwright install chromium

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus API keys:
# - OPENAI_API_KEY
# - ANTHROPIC_API_KEY
# - SEMANTIC_SCHOLAR_API_KEY
# - SUPABASE_URL & SUPABASE_KEY
# - NOTION_TOKEN
# - etc.

# Validar setup
python scripts/validate_setup.py
```

### 2. Frontend (Next.js)

```bash
cd frontend

# Instalar dependencias
npm install

# Configurar variables de entorno
cp .env.example .env.local
# Editar .env.local con la URL del backend:
# NEXT_PUBLIC_API_URL=http://localhost:8000

# Ejecutar en desarrollo
npm run dev
```

### 3. MCP Servers (Opcional)

Si quieres usar los MCP servers, configura VS Code:

1. Instalar extensión: **Roo Cline** o **Cline**
2. Configurar `cline_mcp_settings.json` (ver `docs/ARCHITECTURE_v2_MCP_MULTIMODEL.md`)
3. Reiniciar VS Code

---

## 🚀 Uso

### Opción 1: CLI (Línea de Comandos)

```bash
# Generar tesis básica
python -m ara_framework.main \
  --domain "Tu dominio" \
  --company "Nombre de empresa (opcional)" \
  --focus "Enfoque específico" \
  --length 80

# Con configuración avanzada
python -m ara_framework.main \
  --domain "E-commerce" \
  --company "Zara" \
  --focus "Realidad Aumentada para Prueba Virtual" \
  --length 100 \
  --use-free-models  # Prioriza modelos gratuitos
  --output-dir "outputs/zara_thesis"
```

### Opción 2: Web Dashboard

```bash
# Terminal 1: Backend
python -m ara_framework.api.main

# Terminal 2: Frontend
cd frontend && npm run dev

# Abrir navegador en http://localhost:3000
```

**Flujo en Web**:

1. Click en "New Thesis Project"
2. Rellenar wizard (4 pasos):
   - Paso 1: Seleccionar dominio
   - Paso 2: Definir keywords
   - Paso 3: Configurar agentes (enable/disable)
   - Paso 4: Click "Generate"
3. Ver progreso en tiempo real (WebSocket)
4. Editar documento inline (Notion-style)
5. Exportar a PDF/DOCX

---

## 📊 Roadmap

### ✅ Fase 0: Foundation (Semana 1-2)

- [x] Estructura de proyecto dual
- [x] Documentación completa (5 docs principales)
- [ ] Adaptadores MCP en Python
- [ ] Budget Manager
- [ ] Frontend setup (Next.js 14)

### 🚧 Fase 1: Core Agents (Semana 3-4)

- [ ] NicheAnalyst con Playwright MCP
- [ ] LiteratureResearcher con MarkItDown MCP
- [ ] TechnicalArchitect con GitHub MCP
- [ ] CodeImplementation con Cline
- [ ] ContentSynthesizer con Claude
- [ ] DocumentationAgent (meta-level)

### 📝 Fase 2: Pipeline (Semana 5-6)

- [ ] ProjectManager (orquestador)
- [ ] Pipeline secuencial completo
- [ ] WebSocket para updates en tiempo real
- [ ] Quality gates (validación)

### 🎨 Fase 3: Frontend (Semana 6-7)

- [ ] Thesis Builder (wizard)
- [ ] Progress Dashboard
- [ ] Document Editor (Novel.js)
- [ ] Export (PDF, DOCX, LaTeX)

### 🧪 Fase 4: Casos de Uso (Semana 7-8)

- [ ] Tesis 1: Absolut Vodka (Web 3D)
- [ ] Tesis 2: E-commerce con AR
- [ ] Tesis 3: Telemedicina con IA
- [ ] Análisis comparativo

### 📚 Fase 5: Tu Tesis Principal (Semana 9-10)

- [ ] Capítulos 1-5
- [ ] Capítulos 6-10
- [ ] Revisión y pulido

### 🚀 Fase 6: Producción (Semana 11-12)

- [ ] Refactoring y optimización
- [ ] Tests (coverage >80%)
- [ ] Deployment (Vercel + Railway)
- [ ] Repo público + documentación

---

## 🤝 Contribuir

Este es un proyecto académico, pero las contribuciones son bienvenidas:

1. Fork el repositorio
2. Crea un branch (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'Add: nueva funcionalidad'`)
4. Push al branch (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

---

## 📄 Licencia

MIT License - Ver [LICENSE](LICENSE) para detalles.

---

## 👨‍💻 Autor

**[Tu Nombre]**

- Tesis de Grado: [Universidad]
- LinkedIn: [Tu perfil]
- GitHub: [@tu-usuario](https://github.com/tu-usuario)

---

## 🤖 Agentes del Sistema

### 🔍 **Agent 1: Niche Analyst**
- **Rol**: Análisis de mercado y viabilidad
- **Tareas**: Evaluación de competencia, identificación de brechas, análisis SWOT
- **Herramientas**: Web scraping, búsquedas especializadas

### 📚 **Agent 2: Literature Researcher**  
- **Rol**: Investigación académica y científica
- **Tareas**: Búsqueda de papers, análisis de estado del arte, síntesis bibliográfica
- **Herramientas**: Semantic Scholar API, ArXiv, filtros avanzados

### 🏗️ **Agent 3: Technical Architect**
- **Rol**: Diseño de soluciones técnicas
- **Tareas**: Arquitectura de sistemas, selección de tecnologías, diagramas
- **Herramientas**: Análisis de frameworks, patrones de diseño

### 💻 **Agent 4: Implementation Specialist**
- **Rol**: Especialista en implementación
- **Tareas**: Roadmaps de desarrollo, estimaciones, sprints
- **Herramientas**: Planificación ágil, análisis de dependencias

### ✍️ **Agent 5: Content Synthesizer**
- **Rol**: Generador de informes finales
- **Tareas**: Síntesis de información, redacción técnica, estructura de documentos
- **Herramientas**: Plantillas profesionales, formateo automático

---

## 🙏 Agradecimientos

- **LangChain/LangGraph** por el framework de graphs de IA
- **Groq** por el acceso gratuito a LLaMA 3.3-70B
- **Anthropic** (Claude 3.5) y **OpenAI** (GPT-4o) por los LLMs
- **Microsoft** por Playwright MCP y MarkItDown MCP
- **Spec Kit** por la metodología de documentación
- **Comunidad MCP** por el ecosistema de servers

---

## 📮 Contacto

¿Tienes preguntas o quieres colaborar?

- 📧 Email: tu.email@ejemplo.com
- 💬 Discord: [Link al servidor]
- 🐦 Twitter: [@tu_usuario](https://twitter.com/tu_usuario)

---

<div align="center">
  <strong>⭐ Si este proyecto te resultó útil, dale una estrella en GitHub ⭐</strong>
</div>
