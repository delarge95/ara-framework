# 🔬 ARA Framework - Automated Research & Analysis

> **Sistema Multi-Agente con MCP para Análisis Automatizado de Nichos de Investigación**  
> _Genera análisis completos usando Gemini 2.5 Pro, Claude 4.5, GPT-4o, DeepSeek V3 con Model Context Protocol_

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![CrewAI](https://img.shields.io/badge/CrewAI-0.80+-green.svg)](https://github.com/joaomdmoura/crewAI)
[![MCP](https://img.shields.io/badge/MCP-Integrated-purple.svg)](https://modelcontextprotocol.io/)
[![Tests](https://img.shields.io/badge/Tests-37%2F37_passing-success.svg)](#testing)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📋 Tabla de Contenidos

- [¿Qué es ARA?](#-qué-es-ara)
- [Quick Start](#-quick-start)
- [Características](#-características-principales)
- [Arquitectura](#-arquitectura)
- [Uso del CLI](#-uso-del-cli)
- [Configuración](#-configuración)
- [Testing](#-testing)
- [Documentación](#-documentación)
- [Roadmap](#-roadmap)

---

## 🎯 ¿Qué es ARA?

**ARA Framework** (Automated Research & Analysis) es un sistema multi-agente que automatiza el proceso completo de investigación y análisis de nichos de mercado/tecnología. Utiliza **5 agentes especializados** trabajando en pipeline para generar reportes completos en **53-63 minutos**.

### ¿Qué Hace?

1. **🔍 Analiza Viabilidad** - Evalúa tendencias, competencia y oportunidades del nicho
2. **📚 Investiga Literatura** - Busca papers académicos relevantes (Semantic Scholar)
3. **🏗️ Diseña Arquitectura** - Propone soluciones técnicas y stack tecnológico
4. **💻 Especifica Implementación** - Detalla pasos, desafíos y mejores prácticas
5. **📄 Sintetiza Reporte** - Genera documento markdown profesional de 15-25 páginas

### Output Ejemplo

```
📁 outputs/rust_wasm_audio_20251108/
├── 📄 final_report.md          # Reporte completo (15-25 páginas)
├── 📊 niche_analysis.json      # Datos estructurados del análisis
├── 📚 papers.json              # Papers académicos encontrados
├── 🏗️ architecture.json        # Propuesta de arquitectura técnica
└── 📋 implementation.json      # Especificaciones de implementación
```

---

## 🚀 Quick Start

### Prerequisitos

- **Python 3.12+** (verificar con `python --version`)
- **Git** para clonar el repositorio
- **API Keys**: Al menos Gemini (gratis 1500 req/día)

### Instalación (5 minutos)

```bash
# 1. Clonar repositorio
git clone https://github.com/tu-usuario/ara_framework.git
cd ara_framework

# 2. Crear entorno virtual
python -m venv .venv_py312
.\.venv_py312\Scripts\activate  # Windows
source .venv_py312/bin/activate # Linux/Mac

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar .env
cp .env.example .env
# Editar .env con al menos GEMINI_API_KEY

# 5. Setup Supabase (opcional, 2 min)
# Ver sección Configuración > Supabase

# 6. Validar instalación
python test_api_connections.py
```

### Primer Análisis (1 hora)

```bash
# Análisis completo
python -m cli.main run "Rust WASM for audio processing"

# Con archivo de salida personalizado
python -m cli.main run "React Server Components" --output rsc_analysis.md

# Ver progreso y resultado
python -m cli.main status <analysis_id>
```

**Resultado**: Reporte completo en `outputs/rust_wasm_audio_YYYYMMDD/final_report.md` + guardado en Supabase.

---

## ✨ Características Principales

### 🤖 5 Agentes Especializados

| Agente                       | Función                                     | Tiempo    | Costo         |
| ---------------------------- | ------------------------------------------- | --------- | ------------- |
| **NicheAnalyst**             | Analiza viabilidad, tendencias, competencia | 7-8 min   | 0 cr (Gemini) |
| **LiteratureResearcher**     | Busca y analiza papers académicos           | 20-25 min | 0-0.33 cr     |
| **TechnicalArchitect**       | Diseña arquitectura técnica                 | 10-12 min | 0.33-1 cr     |
| **ImplementationSpecialist** | Detalla implementación paso a paso          | 7-8 min   | 0.33 cr       |
| **ContentSynthesizer**       | Genera reporte final profesional            | 9-10 min  | 0.33 cr       |

**Total**: 53-63 minutos | 1-2.33 créditos (~$0.05-$0.12 USD)

### 🔧 Stack Tecnológico

- **Orquestación**: CrewAI 0.80+ (agentes colaborativos)
- **LLMs**: Multi-modelo con fallbacks automáticos
  - Gemini 2.5 Pro (gratis, 15 RPM)
  - GPT-4o (gratis con OpenAI Tier 1)
  - Claude 4.5 Sonnet/Haiku (paid, mejor calidad)
  - DeepSeek V3 (gratis, 60 RPM)
- **MCP Servers**: 8 servidores integrados
  - Supabase (PostgreSQL + Storage)
  - GitHub (repos, issues, PRs)
  - Browser (Playwright automation)
  - Notion, Jina Reader, Composio, Git
- **Herramientas**:
  - Semantic Scholar (6.7M papers, gratis)
  - Jina Reader (scraping avanzado)
  - Redis (cache opcional)
- **Persistencia**: Supabase (PostgreSQL) + Local files

### 💰 Sistema de Budget

- **Límite mensual configurable** (default: 300 créditos)
- **Tracking en tiempo real** por modelo y agente
- **Fallbacks automáticos** a modelos gratuitos
- **Alertas proactivas** al alcanzar 80% del límite

### 📊 CLI Moderno

```bash
ara --help           # Ayuda general
ara run <niche>      # Ejecutar análisis
ara budget           # Ver créditos disponibles
ara list             # Listar análisis previos
ara status <id>      # Status de análisis específico
ara test             # Ejecutar test suite
ara version          # Versión del framework
```

Interface con **Rich** (progress bars, tablas, colores).

---

## 🏗️ Arquitectura

```
┌──────────────────────────────────────────────────────────────┐
│                       CLI Interface                          │
│                   (Typer + Rich UI)                          │
└────────────────────────┬─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│                    Pipeline Orchestrator                     │
│         (AnalysisPipeline - CrewAI Manager)                  │
└─────┬──────┬──────┬──────┬──────┬─────────────────────────┘
      │      │      │      │      │
      ▼      ▼      ▼      ▼      ▼
   ┌────┐┌────┐┌────┐┌────┐┌────┐
   │ NA ││ LR ││ TA ││ IS ││ CS │  ← 5 Agentes Especializados
   └──┬─┘└──┬─┘└──┬─┘└──┬─┘└──┬─┘
      │     │     │     │     │
      └─────┴──┬──┴─────┴─────┘
               │
┌──────────────▼──────────────────────────────────────────────┐
│                    Budget Manager                            │
│          (Tracking, Limits, Fallbacks)                       │
└─────────────┬──────────────────────────────────────────────┘
              │
┌─────────────┴──────────────────────────────────────────────┐
│                     Tools & MCP Servers                      │
├──────────────────────────────────────────────────────────────┤
│ SearchTool       → Semantic Scholar (6.7M papers)            │
│ ScrapingTool     → Jina Reader + Browser MCP                 │
│ DatabaseTool     → Supabase MCP (PostgreSQL)                 │
│ PdfTool          → LangChain PDF processing                  │
└──────────────────────────────────────────────────────────────┘
              │
┌─────────────┴──────────────────────────────────────────────┐
│                   External Services                          │
├──────────────────────────────────────────────────────────────┤
│ • Gemini 2.5 Pro         • Semantic Scholar                  │
│ • GPT-4o                 • Supabase                           │
│ • Claude 4.5             • Redis (opcional)                   │
│ • DeepSeek V3            • GitHub                             │
└──────────────────────────────────────────────────────────────┘
```

### Flujo de Ejecución

1. **User** → CLI command (`ara run "Rust WASM"`)
2. **Pipeline** → Inicializa BudgetManager y crea 5 agentes
3. **NicheAnalyst** → Analiza viabilidad (output: JSON viabilidad)
4. **LiteratureResearcher** → Busca papers (input: JSON anterior, output: lista papers)
5. **TechnicalArchitect** → Diseña arquitectura (input: papers, output: arquitectura)
6. **ImplementationSpecialist** → Detalla pasos (input: arquitectura, output: plan impl)
7. **ContentSynthesizer** → Genera reporte (input: todos los anteriores, output: markdown)
8. **Pipeline** → Guarda en Supabase + local files
9. **CLI** → Muestra resultado al usuario

---

## 🎮 Uso del CLI

### Comandos Principales

#### 1. Ejecutar Análisis

```bash
# Básico
python -m cli.main run "Rust WASM for audio processing"

# Con opciones
python -m cli.main run "React Server Components" \
  --output rsc_analysis.md \
  --timeout 120 \
  --verbose
```

**Opciones**:

- `--output, -o`: Archivo de salida personalizado
- `--timeout, -t`: Timeout en minutos (default: 90)
- `--verbose, -v`: Logging detallado

#### 2. Ver Budget

```bash
python -m cli.main budget
```

**Output**:

```
💰 Budget & Credits

📊 Límite mensual: 300.00 créditos
✅ Disponible: 298.33
📉 Usado: 1.67 (0.6%)

🤖 Modelos Configurados
┌───────────────────┬─────────┬───────────┬─────────┐
│ Modelo            │   Costo │ RPM Limit │ Status  │
├───────────────────┼─────────┼───────────┼─────────┤
│ gemini-2.5-pro    │ 0.00 cr │    15/min │ 🟢 FREE │
│ gpt-4o            │ 0.00 cr │   100/min │ 🟢 FREE │
│ claude-sonnet-4.5 │ 1.00 cr │    50/min │ 💰 PAID │
...
```

#### 3. Ver Status

```bash
python -m cli.main status <analysis_id>
```

#### 4. Listar Análisis

```bash
python -m cli.main list
```

#### 5. Información del Framework

```bash
python -m cli.main version
```

---

## ⚙️ Configuración

### Variables de Entorno (.env)

```bash
# ============================================================
# ENVIRONMENT
# ============================================================
ENV=development
DEBUG=True
LOG_LEVEL=INFO

# ============================================================
# AI MODELS (al menos 1 requerido)
# ============================================================
GEMINI_API_KEY=tu_key_aqui              # ✅ GRATIS 1500 req/día
OPENAI_API_KEY=sk-...                    # ⚠️  Requiere pago
ANTHROPIC_API_KEY=sk-ant-...             # ⚠️  Requiere pago
DEEPSEEK_API_KEY=sk-...                  # ✅ GRATIS 60 RPM

# ============================================================
# SUPABASE (Recomendado)
# ============================================================
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_ROLE_KEY=eyJ...

# ============================================================
# REDIS (Opcional - Cache)
# ============================================================
REDIS_URL=redis://localhost:6379/0

# ============================================================
# BUDGET (Opcional - Límites)
# ============================================================
MONTHLY_CREDIT_LIMIT=300.0
```

### Setup Supabase (2 minutos)

**¿Por qué Supabase?**

- Persistencia de análisis históricos
- Cache de papers académicos (evita búsquedas duplicadas)
- Tracking de uso de modelos

**Setup**:

1. Crear cuenta en [supabase.com](https://supabase.com) (gratis)
2. Crear nuevo proyecto
3. Copiar URL + Keys al `.env`
4. Ejecutar SQL en **SQL Editor**:

```sql
-- Copiar SQL desde setup_supabase_postgres.py output
-- O ejecutar manual desde Dashboard
```

5. Verificar:

```bash
python test_api_connections.py
# Debe mostrar: ✅ Supabase Database
```

### API Keys Recomendadas

| Servicio         | Costo       | Límite       | Cómo Obtener                                               |
| ---------------- | ----------- | ------------ | ---------------------------------------------------------- |
| **Gemini**       | 🟢 Gratis   | 1500 req/día | [Google AI Studio](https://aistudio.google.com/app/apikey) |
| OpenAI GPT-4o    | 🟢 Gratis\* | 100 RPM      | [OpenAI Platform](https://platform.openai.com/api-keys)    |
| Anthropic Claude | 🔴 Pago     | $4/M tokens  | [Anthropic Console](https://console.anthropic.com/)        |
| DeepSeek         | 🟢 Gratis   | 60 RPM       | [DeepSeek Platform](https://platform.deepseek.com/)        |
| Semantic Scholar | 🟢 Gratis   | 1 req/sec    | No requiere key                                            |

\*GPT-4o gratis con Tier 1 (después de primer pago de $5)

---

## 🧪 Testing

### Test Suite

```bash
# Ejecutar todos los tests (37/37 passing)
pytest tests/

# Tests específicos
pytest tests/test_budget_manager.py  # 13/13 tests
pytest tests/test_tools.py           # 8/8 tests
pytest tests/test_pipeline.py        # 16/16 tests

# Con coverage
pytest --cov=. --cov-report=html tests/
```

### Validación Manual

```bash
# Test de conexiones API
python test_api_connections.py

# Test manual del pipeline
python test_pipeline_manual.py
```

### Estado Actual

- ✅ **37/37 tests passing (100%)**
- ✅ Budget Manager: 13/13
- ✅ Tools: 8/8
- ✅ Pipeline: 16/16
- ✅ Cobertura: ~75%
- ⏱️ Tiempo ejecución: ~15 segundos

---

## 📚 Documentación

### Documentos Principales

- **[00_PROJECT_SUMMARY.md](docs/00_PROJECT_SUMMARY.md)** - Visión general del proyecto
- **[01_PHASE_0_DEFINITION.md](docs/01_PHASE_0_DEFINITION.md)** - Definiciones y alcance
- **[02_PROJECT_CONSTITUTION.md](docs/02_PROJECT_CONSTITUTION.md)** - Stack y decisiones arquitectónicas
- **[03_TECHNICAL_SPECIFICATIONS.md](docs/03_TECHNICAL_SPECIFICATIONS.md)** - Especificaciones técnicas detalladas
- **[04_PROJECT_PLAN.md](docs/04_PROJECT_PLAN.md)** - Plan de implementación (4 fases)
- **[05_TASK_BREAKDOWN.md](docs/05_TASK_BREAKDOWN.md)** - Tareas granulares (17 tasks)

### Reportes de Validación

- **[API_STATUS.md](docs/API_STATUS.md)** - Estado de APIs externas (3/6 operativas)
- **[CLI_VALIDATION_REPORT.md](docs/CLI_VALIDATION_REPORT.md)** - Validación del CLI (6/7 comandos)
- **[TEST_SUITE_STATUS.md](docs/TEST_SUITE_STATUS.md)** - Estado de tests (37/37 passing)
- **[TESTING_STRATEGY.md](docs/TESTING_STRATEGY.md)** - Estrategia de testing

### Guías de Desarrollo

- **[MCP_INTEGRATION.md](docs/mcp_integration/MCP_INTEGRATION.md)** - Integración Model Context Protocol
- **[DEPLOYMENT.md](docs/DEPLOYMENT.md)** - Guía de deployment (local/Docker/cloud)

---

## 🗺️ Roadmap

### ✅ Fase 0: Foundation (Completado)

- [x] SpecKit project governance
- [x] Stack tecnológico definido
- [x] Arquitectura multi-agente
- [x] Budget manager con fallbacks

### ✅ Fase 1: Core Development (Completado)

- [x] 5 agentes especializados
- [x] Pipeline orchestrator
- [x] Tools integration (Semantic Scholar, Jina, Supabase)
- [x] CLI con Typer + Rich
- [x] Test suite (37/37 passing)

### 🔄 Fase 2: MCP Integration (En Progreso)

- [x] 8 MCP servers integrados
- [x] Supabase MCP (PostgreSQL + Storage)
- [ ] Browser MCP (Playwright automation)
- [ ] GitHub MCP (repos, issues, PRs)
- [ ] Notion MCP (knowledge base)

### 📋 Fase 3: Production Ready

- [ ] Docker containerization
- [ ] CI/CD con GitHub Actions
- [ ] Monitoring y alertas
- [ ] Rate limiting por API
- [ ] Documentación completa
- [ ] Ejemplos de uso

### 🚀 Fase 4: Advanced Features

- [ ] Web UI (dashboard con resultados)
- [ ] Análisis comparativo de múltiples nichos
- [ ] Exportación a PDF profesional
- [ ] Integración con Langfuse (observability)
- [ ] Template system para reportes

---

## 🤝 Contribuir

¿Encontraste un bug o tienes una idea?

1. Fork el repositorio
2. Crea una rama (`git checkout -b feature/amazing-feature`)
3. Commit tus cambios (`git commit -m 'Add amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

---

## 🙏 Agradecimientos

- **CrewAI** - Framework multi-agente
- **Anthropic** - Model Context Protocol
- **Semantic Scholar** - API académica gratuita
- **Supabase** - PostgreSQL + Storage managed
- **Typer + Rich** - CLI moderno

---

## 📞 Soporte

- **Issues**: [GitHub Issues](https://github.com/tu-usuario/ara_framework/issues)
- **Docs**: [Documentación completa](docs/)
- **Email**: tu-email@example.com

---

**⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub**

---

_Última actualización: 2025-11-08_  
_Versión: 1.0.0_  
_Python: 3.12+_
