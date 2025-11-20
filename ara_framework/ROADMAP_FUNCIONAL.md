# 🗺️ HOJA DE RUTA - ARA FRAMEWORK FUNCIONAL

**Fecha**: 8 de Noviembre 2025  
**Estado Actual**: Tests Pipeline 100% ✅ | Tests Completos 53% ⚠️  
**Objetivo**: Framework 100% funcional con CLI operativo

---

## 📊 ESTADO ACTUAL

### ✅ **COMPLETADO (53% - 23/43 tests)**

#### Tests Pipeline (16/16 - 100%)

- ✅ Inicialización del pipeline
- ✅ Validación de inputs (5 escenarios)
- ✅ Ejecución exitosa con mocks
- ✅ Manejo de timeouts
- ✅ Manejo de errores de Crew
- ✅ Guardado en Supabase y local
- ✅ Serialización de resultados

#### Tests Herramientas Básicos (7/7 - 100%)

- ✅ Instanciación de SearchTool
- ✅ Instanciación de ScrapingTool
- ✅ Instanciación de PDFTool
- ✅ Instanciación de DatabaseTool
- ✅ Extracción de secciones PDF

#### Tests Budget Manager Parciales (2/13)

- ✅ Creación de ModelCost
- ✅ Modelo gratuito

### ⚠️ **PENDIENTE (47% - 20/43 tests)**

#### 1. Tests Budget Manager (9 errores + 2 fallos)

**Problema**: `AttributeError: module 'core.budget_manager' has no attribute 'redis'`

- ❌ test_initialization
- ❌ test_get_model_config
- ❌ test_calculate_credits
- ❌ test_track_usage
- ❌ test_get_usage_since
- ❌ test_get_remaining_credits
- ❌ test_check_rate_limit
- ❌ test_alert_threshold_low
- ❌ test_alert_threshold_ok
- ❌ test_budget_status_creation (TypeError: unexpected argument 'total_credits')
- ❌ test_budget_status_alert_levels (TypeError: unexpected argument 'total_credits')

**Causa**: Mock incorrecto de Redis - `patch("core.budget_manager.redis.from_url")` debería ser `patch("core.budget_manager.Redis.from_url")`

#### 2. Tests Tools (8 fallos)

**Problema**: Atributos MCP no existen (`playwright_mcp`, `markitdown_mcp`, `supabase_mcp`)

- ❌ test_scrape_website_mock → `playwright_mcp` no existe
- ❌ test_convert_pdf_to_markdown_mock → `markitdown_mcp` no existe
- ❌ test_save_paper_mock → `supabase_mcp` no existe
- ❌ test_query_papers_mock → `supabase_mcp` no existe
- ❌ test_save_analysis_mock → `supabase_mcp` no existe
- ❌ test_log_model_usage_mock → `supabase_mcp` no existe

**Causa**: Tests asumen arquitectura MCP pero tools no usan adaptadores MCP internamente

#### 3. Fixtures Faltantes (3 errores)

- ❌ test_search_academic_papers_mock → fixture `sample_semantic_scholar_response` no definida
- ❌ test_search_papers_parallel_mock → fixture `sample_semantic_scholar_response` no definida
- ❌ test_search_and_save_paper → fixture `sample_semantic_scholar_response` no definida

**Causa**: Fixture definida como `mock_semantic_scholar_response` pero tests buscan `sample_semantic_scholar_response`

---

## 🎯 PLAN DE ACCIÓN

### **FASE 1: TESTS (Prioridad: ALTA)** 🔧

**Objetivo**: 43/43 tests pasando (100%)  
**Tiempo estimado**: 2-3 horas

#### Tarea 1.1: Corregir Tests Budget Manager

**Archivos**: `tests/test_budget_manager.py`, `tests/conftest.py`

```python
# ANTES (incorrecto):
patch("core.budget_manager.redis.from_url", return_value=mock_redis_client)

# DESPUÉS (correcto):
patch("core.budget_manager.Redis.from_url", return_value=mock_redis_client)
```

**Acciones**:

1. Buscar todas las ocurrencias de `"core.budget_manager.redis.from_url"`
2. Reemplazar por `"core.budget_manager.Redis.from_url"`
3. Actualizar fixture `budget_manager` en conftest.py
4. Corregir firma de `BudgetStatus` (eliminar parámetro `total_credits` de tests)
5. Ejecutar: `pytest tests/test_budget_manager.py -v`

**Resultado esperado**: 13/13 tests budget_manager pasando

---

#### Tarea 1.2: Corregir Tests Tools

**Archivos**: `tests/test_tools.py`, implementaciones en `tools/`

**Opción A - Adaptar Tests (RECOMENDADO)**:
Modificar tests para mockear métodos reales de las tools sin asumir arquitectura MCP

```python
# ANTES:
with patch.object(tool.playwright_mcp, "scrape", ...):

# DESPUÉS:
with patch("tools.scraping_tool.ScrapingTool.scrape_website", new_callable=AsyncMock):
```

**Opción B - Implementar Adaptadores MCP**:
Agregar `self.playwright_mcp`, `self.supabase_mcp`, etc. a las tools (más trabajo)

**Acciones**:

1. Inspeccionar `tools/scraping_tool.py`, `tools/pdf_tool.py`, `tools/database_tool.py`
2. Identificar métodos públicos reales
3. Actualizar tests para mockear métodos reales, no atributos MCP inexistentes
4. Ejecutar: `pytest tests/test_tools.py::TestScrapingTool -v`
5. Repetir para PDFTool y DatabaseTool

**Resultado esperado**: 6/6 tests tools corregidos

---

#### Tarea 1.3: Corregir Fixtures Faltantes

**Archivos**: `tests/conftest.py`

```python
# AGREGAR en conftest.py:
@pytest.fixture
def sample_semantic_scholar_response():
    """Fixture con respuesta mock de Semantic Scholar."""
    return {
        "data": [
            {
                "paperId": "test-paper-123",
                "title": "Sample Paper on Rust WASM",
                "abstract": "This is a sample abstract...",
                "year": 2024,
                "citationCount": 42,
                # ... resto de campos
            }
        ],
        "total": 1,
        "offset": 0,
        "next": None,
    }
```

**Acciones**:

1. Revisar fixture existente `mock_semantic_scholar_response`
2. Crear alias `sample_semantic_scholar_response` o renombrar
3. Ejecutar: `pytest tests/test_tools.py::TestSearchTool -v`

**Resultado esperado**: 3/3 tests search pasando

---

### **FASE 2: CLI FUNCIONAL (Prioridad: ALTA)** 🖥️

**Objetivo**: `python -m cli.main analyze` funcionando end-to-end  
**Tiempo estimado**: 1-2 horas

#### Tarea 2.1: Validar Conexiones API

**Archivo**: `test_api_connections.py`

```bash
# Ejecutar script de validación
python test_api_connections.py
```

**Verificar**:

- ✅ OpenAI API key válida
- ✅ Anthropic API key válida
- ✅ Google Gemini API key válida
- ✅ Supabase conexión exitosa
- ⚠️ Redis (opcional - puede funcionar sin caché)

**Acciones si falla**:

1. Revisar `.env` con variables correctas
2. Verificar saldos de API keys
3. Probar conexión a Supabase manualmente

---

#### Tarea 2.2: Test Manual del Pipeline

**Archivo**: `test_pipeline_manual.py`

```bash
# Test con niche simple
python test_pipeline_manual.py
```

**Escenarios**:

1. Niche corto: "Rust WASM"
2. Niche medio: "Rust WASM for audio processing"
3. Niche complejo: "Real-time audio processing with Rust WebAssembly in browser environments"

**Verificar**:

- Creación de agentes exitosa
- Ejecución de Crew sin errores
- Guardado de resultados en `outputs/`
- Logging estructurado visible

**Posibles errores**:

- `CHROMA_OPENAI_API_KEY` → Agregar a `.env` o deshabilitar memoria vectorial
- `ValidationError` → Revisar formato de respuesta de LLMs
- `TimeoutError` → Aumentar timeout en `pipeline.py`

---

#### Tarea 2.3: CLI End-to-End

**Archivo**: `cli/main.py`

```bash
# Test comando analyze
python -m cli.main analyze --niche "Rust WASM" --output results.json
```

**Comandos a validar**:

1. `analyze` → Ejecuta pipeline completo
2. `list-agents` → Lista agentes disponibles
3. `check-budget` → Muestra créditos restantes
4. `validate` → Valida configuración

**Resultado esperado**:

- CLI ejecuta sin errores
- Resultados guardados en archivo
- Progress bar visible
- Logs claros y estructurados

---

### **FASE 3: DOCUMENTACIÓN (Prioridad: MEDIA)** 📚

**Objetivo**: Guías completas para usuarios y desarrolladores  
**Tiempo estimado**: 2-3 horas

#### Tarea 3.1: Actualizar README.md

**Contenido**:

```markdown
# ARA Framework

## ⚡ Quick Start

\`\`\`bash
pip install -e .
python -m cli.main analyze --niche "your niche"
\`\`\`

## 📦 Installation

- Requisitos: Python 3.12+
- Dependencias: CrewAI 0.100.0, OpenAI, Anthropic

## 🎯 Features

- Multi-LLM orchestration
- Academic paper search
- Budget tracking
- Supabase persistence

## 🏗️ Architecture

[Diagrama de agentes y flujo]
```

---

#### Tarea 3.2: Crear TESTING.md

**Contenido**:

```markdown
# Testing Strategy

## Unit Tests

\`\`\`bash
pytest tests/test_budget_manager.py -v
\`\`\`

## Integration Tests

\`\`\`bash
pytest tests/test_pipeline.py -v
\`\`\`

## Coverage

\`\`\`bash
pytest --cov=core --cov=tools --cov=agents
\`\`\`

## Mocking Patterns

- Session-level: langchain_google_genai
- Test-level: Crew, agent creation functions
- AsyncMock for coroutines
```

---

#### Tarea 3.3: Crear DEPLOYMENT.md

**Contenido**:

```markdown
# Deployment Guide

## Production Setup

1. Configure environment variables
2. Setup Supabase database
3. Deploy to cloud (Railway, Render, etc.)

## Environment Variables

- OPENAI_API_KEY
- ANTHROPIC_API_KEY
- GOOGLE_API_KEY
- SUPABASE_URL
- SUPABASE_KEY

## Docker (Optional)

\`\`\`dockerfile
FROM python:3.12-slim
COPY . /app
RUN pip install -e .
CMD ["python", "-m", "cli.main"]
\`\`\`
```

---

### **FASE 4: OPTIMIZACIONES (Prioridad: BAJA)** 🚀

**Objetivo**: Mejoras de performance y UX  
**Tiempo estimado**: 3-5 horas

#### Tarea 4.1: Caché Inteligente

- Implementar caché de búsquedas académicas (Redis)
- Caché de respuestas de LLMs por hash de prompt
- TTL configurable por tipo de caché

#### Tarea 4.2: Paralelización

- Ejecutar agentes en paralelo cuando sea posible
- Búsquedas académicas paralelas mejoradas
- Web scraping concurrente

#### Tarea 4.3: Monitoring

- Dashboard simple con FastAPI
- Métricas de uso de créditos
- Historial de análisis
- Health checks de APIs

---

## 📋 CHECKLIST FINAL

### Para declarar framework FUNCIONAL:

- [ ] **Tests: 43/43 pasando (100%)**

  - [ ] test_budget_manager.py: 13/13 ✅
  - [ ] test_pipeline.py: 16/16 ✅ (COMPLETADO)
  - [ ] test_tools.py: 14/14 ✅

- [ ] **CLI operativo**

  - [ ] `python -m cli.main analyze` funciona
  - [ ] Guardado de resultados exitoso
  - [ ] Manejo de errores robusto

- [ ] **Conexiones API validadas**

  - [ ] OpenAI conectado
  - [ ] Anthropic conectado
  - [ ] Google Gemini conectado
  - [ ] Supabase conectado

- [ ] **Documentación básica**
  - [ ] README.md actualizado
  - [ ] INSTALLATION.md completo
  - [ ] Ejemplos de uso

---

## 🎯 SIGUIENTE PASO INMEDIATO

**EJECUTAR AHORA**:

```bash
# 1. Corregir tests budget_manager
#    Cambiar patch("core.budget_manager.redis.from_url")
#    por patch("core.budget_manager.Redis.from_url")

# 2. Ejecutar tests
pytest tests/test_budget_manager.py -v

# 3. Corregir tests tools (adaptadores MCP)
pytest tests/test_tools.py -v

# 4. Test manual pipeline
python test_pipeline_manual.py

# 5. CLI end-to-end
python -m cli.main analyze --niche "Rust WASM"
```

---

## 💡 NOTAS IMPORTANTES

### Dependencias Conocidas

- **openai 2.7.1 vs <2.0.0**: Ignorar warning, funciona
- **protobuf 6.33.0 vs <6.0.0**: Ignorar warning, funciona
- **langchain_google_genai**: Mockeado a nivel de sesión

### Limitaciones Actuales

- Memory vectorial deshabilitada (requiere CHROMA_OPENAI_API_KEY)
- Redis opcional (funciona sin caché)
- Rate limiting básico (puede mejorar con Redis)

### Mejoras Futuras

- Implementar MCP adapters reales
- Dashboard de monitoreo
- Tests de integración con APIs reales
- CI/CD pipeline
- Docker deployment

---

**Última actualización**: 2025-11-08  
**Mantenedor**: GitHub Copilot  
**Estado**: 🟡 En Progreso → 🟢 Funcional (pending Fase 1+2)
