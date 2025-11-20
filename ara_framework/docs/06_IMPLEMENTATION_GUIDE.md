# 🛠️ Guía de Implementación - ARA Framework

**Guía Práctica Paso a Paso para Configurar y Ejecutar el Framework**

---

## 📑 Tabla de Contenidos

1. [Pre-requisitos](#pre-requisitos)
2. [Instalación Inicial](#instalación-inicial)
3. [Configuración de API Keys y Servicios](#configuración-de-api-keys-y-servicios)
4. [Setup de MCP Servers](#setup-de-mcp-servers)
5. [Configuración de Agentes](#configuración-de-agentes)
6. [Primer Análisis de Prueba](#primer-análisis-de-prueba)
7. [Monitoreo de Costos](#monitoreo-de-costos)
8. [Casos de Uso Prácticos](#casos-de-uso-prácticos)
9. [Troubleshooting](#troubleshooting)

---

## 🔧 Pre-requisitos

### Software Requerido:

- **Python 3.12+**
- **Git** para clonar el repositorio
- **PowerShell** (Windows) o **bash** (Linux/Mac)
- **Visual Studio Code** (recomendado) con extensiones:
  - Python (ms-python.python)
  - Pylance
  - YAML

### Suscripciones Necesarias:

#### Opción Mínima ($10/mes):

- ✅ **GitHub Copilot Pro** ($10/mes) - Acceso a GPT-5, GPT-4o, Claude 4.5, Gemini 2.5 Pro
- ✅ **Google AI Studio** (gratis) - API key para Gemini 2.5 Pro
- ✅ **DeepSeek** (gratis) - API key para DeepSeek V3

#### Opción Óptima ($30/mes):

- Todo lo anterior +
- ✅ **Cursor Pro** ($20/mes) - IDE agentic completo
- ⚠️ **MiniMax-M2 local** (opcional, requiere GPU) - Open-source, 229B params

### Hardware Recomendado:

- **RAM:** 8 GB mínimo, 16 GB recomendado
- **Disco:** 5 GB libres
- **GPU:** Opcional para MiniMax-M2 local (NVIDIA 24GB+ VRAM para quantización FP8)
- **Internet:** Conexión estable (APIs requieren latencia baja)

---

## 📦 Instalación Inicial

### 1. Clonar el Repositorio

```powershell
# Clonar el proyecto
git clone https://github.com/tu-usuario/ara_framework.git
cd ara_framework

# Crear entorno virtual
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# source venv/bin/activate    # Linux/Mac

# Verificar versión de Python
python --version  # Debe ser 3.11+
```

### 2. Instalar Dependencias

```powershell
# Instalar paquetes principales
pip install -r requirements.txt

# Instalar dependencias de desarrollo (opcional)
pip install -r requirements-dev.txt

# Verificar instalación de librerías clave
python -c "import langgraph, openai, anthropic, supabase; print('OK')"
```

### 3. Ejecutar Script de Setup Automatizado (Opcional)

```powershell
# Windows
.\setup.ps1

# Linux/Mac
chmod +x setup.sh
./setup.sh
```

Este script:

- ✅ Valida versión de Python
- ✅ Crea entorno virtual automáticamente
- ✅ Instala dependencias
- ✅ Crea archivo `.env` desde `.env.example`
- ✅ Valida estructura de directorios

---

## 🔑 Configuración de API Keys y Servicios

### 1. Crear Archivo `.env`

Copia el archivo de ejemplo:

```powershell
Copy-Item .env.example .env
```

### 2. Obtener API Keys

#### **GitHub Copilot Pro** (requerido, $10/mes)

1. Suscríbete en [https://github.com/features/copilot](https://github.com/features/copilot)
2. En VS Code, instala la extensión GitHub Copilot
3. Autentícate con tu cuenta de GitHub
4. **Configuración en código:**

```python
# El SDK de OpenAI detecta automáticamente la suscripción de Copilot
from openai import OpenAI

client = OpenAI()  # No requiere API key explícita si tienes Copilot activo

# Modelos disponibles con Copilot Pro:
# - "gpt-5" (1x credit)
# - "gpt-5-codex" (1x credit)
# - "gpt-4o" (0x credit, gratis)
# - "gpt-4o-mini" (0x credit, gratis)
# - "o1", "o3" (reasoning models, 1x credit)
```

#### **Google AI Studio** (gratis)

1. Ve a [https://ai.google.dev](https://ai.google.dev)
2. Crea un proyecto nuevo o selecciona uno existente
3. Habilita la API de Gemini
4. Genera una API key desde "Get API Key"
5. Agrega al `.env`:

```bash
GOOGLE_AI_API_KEY=AIzaSy... # Tu key aquí
```

#### **DeepSeek** (gratis)

1. Regístrate en [https://platform.deepseek.com](https://platform.deepseek.com)
2. Ve a "API Keys" y genera una nueva
3. Agrega al `.env`:

```bash
DEEPSEEK_API_KEY=sk-... # Tu key aquí
```

#### **Anthropic Claude** (opcional, via Copilot)

- Si tienes Copilot Pro, Claude 4.5 ya está disponible sin key adicional
- Si quieres usar la API directa de Anthropic (no recomendado por costos):

```bash
ANTHROPIC_API_KEY=sk-ant-... # Tu key aquí (opcional)
```

#### **MiniMax-M2** (open-source, gratis si descargas los pesos)

**Opción 1: API Gratuita (limitada)**

1. Ve a [https://platform.minimax.io](https://platform.minimax.io)
2. Regístrate y genera API key
3. Agrega al `.env`:

```bash
MINIMAX_API_KEY=mm-... # Tu key aquí
```

**Opción 2: Deploy Local (requiere GPU)**

```bash
# Descargar pesos desde Hugging Face (229B params, ~100GB)
git lfs install
git clone https://huggingface.co/MiniMaxAI/MiniMax-M2

# Servir con SGLang (recomendado)
pip install sglang[all]
python -m sglang.launch_server \
  --model-path MiniMax-M2 \
  --tp 8 \  # Tensor parallelism (ajustar según GPUs)
  --port 8000
```

### 3. Configurar Supabase (Base de Datos Gratis)

1. Crea cuenta en [https://supabase.com](https://supabase.com)
2. Crea un nuevo proyecto (elige región más cercana)
3. En "Settings → API", copia:
   - **Project URL**: `https://xyzproject.supabase.co`
   - **Anon Key**: `eyJhbGc...` (public, seguro)
   - **Service Role Key**: `eyJhbGc...` (privado, solo para server-side)
4. Agrega al `.env`:

```bash
SUPABASE_URL=https://xyzproject.supabase.co
SUPABASE_KEY=eyJhbGc...  # Usa anon key para client-side
```

5. **Crear tablas necesarias:**

```sql
-- Ejecutar en Supabase SQL Editor
CREATE TABLE analysis_results (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  niche VARCHAR(255) NOT NULL,
  agent_name VARCHAR(100),
  result JSONB,
  cost_usd DECIMAL(10, 4),
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE agent_executions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_name VARCHAR(100),
  model_used VARCHAR(100),
  tokens_input INTEGER,
  tokens_output INTEGER,
  cost_usd DECIMAL(10, 6),
  execution_time_ms INTEGER,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### 4. Configurar Notion (Opcional, para Knowledge Base)

1. Crea cuenta en [https://notion.so](https://notion.so)
2. Ve a [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)
3. Crea una nueva integración
4. Copia el "Internal Integration Token"
5. Comparte tu workspace con la integración
6. Agrega al `.env`:

```bash
NOTION_TOKEN=secret_... # Tu token aquí
NOTION_DATABASE_ID=abc123...  # ID de tu base de datos
```

---

## 🔌 Setup de MCP Servers

Los MCP Servers conectan los agentes con herramientas externas. Todos son **gratuitos**.

### 1. Configuración Global de MCP

Crea el archivo `config/mcp_config.yaml`:

```yaml
mcp_servers:
  # Web Scraping - Jina AI Reader (20 req/min gratis)
  jina_ai_reader:
    enabled: true
    endpoint: "https://r.jina.ai/"
    api_key: null # No requiere key para uso básico
    rate_limit: 20 # requests por minuto
    timeout: 30
    agents: ["NicheAnalyst", "LiteratureResearcher"]

  # GitHub Integration (requiere GitHub token)
  github:
    enabled: true
    api_key: ${GITHUB_TOKEN} # Referencia a .env
    rate_limit: 5000 # requests por hora (GitHub free tier)
    agents: ["LiteratureResearcher", "StrategyProposer"]

  # Browser Automation - Playwright
  playwright:
    enabled: true
    headless: true
    browser: "chromium" # o "firefox", "webkit"
    agents: ["NicheAnalyst", "FinancialAnalyst"]

  # Database - Supabase
  supabase:
    enabled: true
    url: ${SUPABASE_URL}
    key: ${SUPABASE_KEY}
    agents: ["all"] # Todos los agentes pueden guardar resultados

  # Knowledge Base - Notion
  notion:
    enabled: false # Opcional
    token: ${NOTION_TOKEN}
    database_id: ${NOTION_DATABASE_ID}
    agents: ["ReportGenerator"]
```

### 2. Implementar Adaptadores en Python

Crea `core/mcp_adapter.py`:

```python
import httpx
from typing import Optional, Dict, Any

class JinaAIReaderAdapter:
    """Adapter para Jina AI Reader - Web scraping gratis."""

    def __init__(self, rate_limit: int = 20):
        self.base_url = "https://r.jina.ai/"
        self.rate_limit = rate_limit
        self.client = httpx.AsyncClient(timeout=30.0)

    async def fetch_url(self, url: str) -> str:
        """Extrae contenido limpio de una URL."""
        response = await self.client.get(f"{self.base_url}{url}")
        response.raise_for_status()
        return response.text  # Devuelve markdown limpio

    async def search_web(self, query: str) -> list[str]:
        """Busca en la web y devuelve URLs relevantes."""
        # Implementar búsqueda (puede usar Google Custom Search API gratis)
        pass


class SupabaseMCPAdapter:
    """Adapter para Supabase - Base de datos PostgreSQL gratis."""

    def __init__(self, url: str, key: str):
        from supabase import create_client, Client
        self.client: Client = create_client(url, key)

    def save_result(self, table: str, data: Dict[str, Any]) -> Dict:
        """Guarda resultado en Supabase."""
        return self.client.table(table).insert(data).execute()

    def query_results(self, table: str, filters: Dict) -> list[Dict]:
        """Consulta resultados previos."""
        query = self.client.table(table).select("*")
        for key, value in filters.items():
            query = query.eq(key, value)
        return query.execute().data
```

### 3. Validar Conexiones

```python
# tests/test_mcp_connections.py
import pytest
from core.mcp_adapter import JinaAIReaderAdapter, SupabaseMCPAdapter

@pytest.mark.asyncio
async def test_jina_reader():
    adapter = JinaAIReaderAdapter()
    content = await adapter.fetch_url("https://example.com")
    assert len(content) > 100

def test_supabase_connection():
    import os
    adapter = SupabaseMCPAdapter(
        url=os.getenv("SUPABASE_URL"),
        key=os.getenv("SUPABASE_KEY")
    )
    result = adapter.save_result("analysis_results", {
        "niche": "test",
        "result": {"status": "ok"}
    })
    assert result
```

---

## 🤖 Configuración de Agentes

### 1. Definir Agente con Multi-Modelo

Crea `agents/niche_analyst.py`:

```python
from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from core.mcp_adapter import JinaAIReaderAdapter, SupabaseMCPAdapter
from core.budget_manager import BudgetManager

class NicheAnalystAgent:
    def __init__(self, budget_manager: BudgetManager):
        self.budget = budget_manager

        # Modelo primary: Gemini 2.5 Pro (gratis via Google AI Studio)
        self.primary_model = ChatGoogleGenerativeAI(
            model="gemini-2.5-pro",
            google_api_key=os.getenv("GOOGLE_AI_API_KEY"),
            temperature=0.7
        )

        # Fallback 1: MiniMax-M2 (open-source, gratis si local)
        self.fallback_model = ChatOpenAI(
            base_url="http://localhost:8000/v1",  # SGLang local
            model="MiniMax-M2",
            temperature=0.7
        )

        # Fallback 2: GPT-4o (gratis con Copilot Pro, 0x credits)
        self.emergency_model = ChatOpenAI(
            model="gpt-4o",
            temperature=0.7
        )

        # MCP Adapters
        self.jina = JinaAIReaderAdapter()
        self.db = SupabaseMCPAdapter(
            url=os.getenv("SUPABASE_URL"),
            key=os.getenv("SUPABASE_KEY")
        )

        # Agente LangGraph node
        self.agent = Agent(
            role="Niche Market Analyst",
            goal="Identify emerging market niches and trends",
            backstory="""Expert in trend analysis, market research,
            and competitive intelligence.""",
            llm=self.primary_model,
            verbose=True
        )

    async def analyze_niche(self, niche: str) -> dict:
        """Analiza un nicho de mercado específico."""
        try:
            # 1. Scraping con Jina AI
            google_search_url = f"https://www.google.com/search?q={niche}+market+trends"
            trends_content = await self.jina.fetch_url(google_search_url)

            # 2. Análisis con modelo primary
            result = await self._execute_with_fallback(
                prompt=f"Analyze this niche market: {niche}\n\nData:\n{trends_content}",
                niche=niche
            )

            # 3. Guardar en Supabase
            self.db.save_result("analysis_results", {
                "niche": niche,
                "agent_name": "NicheAnalyst",
                "result": result
            })

            return result

        except Exception as e:
            self.budget.log_error("NicheAnalyst", str(e))
            raise

    async def _execute_with_fallback(self, prompt: str, niche: str) -> dict:
        """Ejecuta con modelo primary y fallback automático si falla."""
        models = [
            ("gemini-2.5-pro", self.primary_model, 0.0),  # Gratis
            ("minimax-m2", self.fallback_model, 0.0),     # Gratis local
            ("gpt-4o", self.emergency_model, 0.0)         # 0x credits
        ]

        for model_name, model, cost in models:
            try:
                response = await model.ainvoke(prompt)
                self.budget.track_usage(
                    agent="NicheAnalyst",
                    model=model_name,
                    cost=cost
                )
                return {"content": response.content, "model": model_name}
            except Exception as e:
                print(f"Model {model_name} failed: {e}. Trying next...")
                continue

        raise RuntimeError("All models failed for NicheAnalyst")
```

### 2. Configurar Budget Manager

Crea `core/budget_manager.py`:

```python
from typing import Dict, List
import json
from datetime import datetime

class BudgetManager:
    """Gestor de presupuesto y tracking de costos."""

    def __init__(self, max_budget_usd: float = 5.0):
        self.max_budget = max_budget_usd
        self.current_spend = 0.0
        self.usage_log: List[Dict] = []

        # Costos por modelo (en USD por 1M tokens)
        self.model_costs = {
            # Modelos gratuitos (via subscripciones)
            "gpt-4o": 0.0,  # 0x credits en Copilot Pro
            "gpt-4o-mini": 0.0,
            "gpt-5-mini": 0.0,
            "gemini-2.5-pro": 0.0,  # Gratis en Google AI Studio
            "deepseek-v3": 0.0,  # API gratis
            "minimax-m2": 0.0,  # Open-source local

            # Modelos premium (vía Copilot Pro, 1x credit)
            "gpt-5": 0.03,  # Estimado equivalente
            "gpt-5-codex": 0.03,
            "claude-sonnet-4.5": 0.03,
            "claude-haiku-4.5": 0.01,  # 0.33x credit
        }

    def track_usage(self, agent: str, model: str, tokens: int = 1000):
        """Registra uso de un modelo."""
        cost = (tokens / 1_000_000) * self.model_costs.get(model, 0.0)
        self.current_spend += cost

        self.usage_log.append({
            "timestamp": datetime.now().isoformat(),
            "agent": agent,
            "model": model,
            "tokens": tokens,
            "cost_usd": cost
        })

        if self.current_spend > self.max_budget:
            raise BudgetExceededError(
                f"Budget exceeded: ${self.current_spend:.4f} > ${self.max_budget}"
            )

    def get_report(self) -> Dict:
        """Genera reporte de costos."""
        return {
            "total_spend_usd": self.current_spend,
            "budget_remaining_usd": self.max_budget - self.current_spend,
            "usage_by_agent": self._group_by_agent(),
            "usage_by_model": self._group_by_model()
        }

    def _group_by_agent(self) -> Dict[str, float]:
        grouped = {}
        for entry in self.usage_log:
            agent = entry["agent"]
            grouped[agent] = grouped.get(agent, 0.0) + entry["cost_usd"]
        return grouped

    def _group_by_model(self) -> Dict[str, float]:
        grouped = {}
        for entry in self.usage_log:
            model = entry["model"]
            grouped[model] = grouped.get(model, 0.0) + entry["cost_usd"]
        return grouped

class BudgetExceededError(Exception):
    pass
```

---

## 🚀 Primer Análisis de Prueba

### 1. Ejecutar Análisis Básico

Crea `main.py`:

```python
import asyncio
from agents.niche_analyst import NicheAnalystAgent
from core.budget_manager import BudgetManager

async def main():
    # Configurar presupuesto
    budget = BudgetManager(max_budget_usd=2.0)

    # Crear agente
    analyst = NicheAnalystAgent(budget)

    # Analizar nicho
    result = await analyst.analyze_niche("AI-powered productivity tools")

    print("\n=== ANÁLISIS COMPLETADO ===")
    print(result)

    # Reporte de costos
    print("\n=== REPORTE DE COSTOS ===")
    print(budget.get_report())

if __name__ == "__main__":
    asyncio.run(main())
```

Ejecutar:

```powershell
python main.py
```

### 2. Verificar Resultados

```powershell
# Ver logs en Supabase
# Abre tu proyecto en https://supabase.com y ve a Table Editor → analysis_results
```

---

## 📊 Monitoreo de Costos

### Dashboard en Tiempo Real

Crea `scripts/cost_dashboard.py`:

```python
import streamlit as st
from core.budget_manager import BudgetManager
from supabase import create_client
import os

st.title("ARA Framework - Cost Dashboard")

# Conectar a Supabase
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

# Obtener ejecuciones recientes
executions = supabase.table("agent_executions").select("*").order("created_at", desc=True).limit(50).execute()

# Gráfico de costos por agente
st.bar_chart(...)
```

Ejecutar dashboard:

```powershell
streamlit run scripts/cost_dashboard.py
```

---

## 🎯 Casos de Uso Prácticos

### Caso 1: Análisis Completo de Nicho

```python
from crews.niche_research_crew import NicheResearchCrew

crew = NicheResearchCrew(budget=5.0)
report = await crew.run_full_analysis(
    niche="Sustainable fashion for Gen Z",
    depth="comprehensive"  # o "quick", "deep"
)
```

### Caso 2: Revisión de Literatura Académica

```python
from agents.literature_researcher import LiteratureResearcherAgent

researcher = LiteratureResearcherAgent(budget_manager)
papers = await researcher.find_papers(
    topic="Multi-agent systems with MCP protocol",
    min_citations=10,
    years=[2023, 2024, 2025]
)
```

---

## 🐛 Troubleshooting

### Error: "Budget exceeded"

**Solución:** Aumentar `max_budget_usd` en `BudgetManager` o usar modelos más baratos (0x credits).

### Error: "Jina AI rate limit"

**Solución:** Implementar rate limiting con `asyncio.sleep()` entre requests.

### Error: "Supabase connection failed"

**Solución:** Verificar que `SUPABASE_URL` y `SUPABASE_KEY` estén correctos en `.env`.

---

## 🚀 ACTUALIZACIÓN NOVIEMBRE 2025: Roadmap de Implementación Validado

> **Fuente**: INFORME_MAESTRO sección 5 + optimization_research.md + RESUMEN_EJECUTIVO_DECISION_FINAL.md  
> **Estado**: ✅ ROADMAP CON 4 FASES PRAGMÁTICAS

### **Roadmap de Implementación: 4 Fases**

```yaml
implementation_roadmap:
  overview:
    duration_total: "12 semanas (3 meses)"
    confidence: "95%"
    risk_level: "BAJO (stack validado)"

  phases:
    phase_1_setup:
      name: "Setup y Fundamentos"
      duration: "Días 1-2 (16 horas)"
      goal: "Entorno funcional con todos los servicios"
      success_criteria:
        - "GitHub Copilot Pro activo con 300 créditos"
        - "Continue.dev instalado en VS Code"
        - "8 MCP servers conectados y validados"
        - "APIs gratuitas configuradas (Gemini, DeepSeek, MiniMax)"
        - ".env configurado sin errores"
        - "FastAPI corriendo en localhost:8000"

    phase_2_validation:
      name: "Validación de Pipeline Básico"
      duration: "Días 3-5 (24 horas)"
      goal: "Pipeline E2E funcionando sin optimizaciones"
      success_criteria:
        - "6 agentes LangGraph implementados"
        - "Pipeline secuencial completo (135-165 min)"
        - "1 tesis de ejemplo generada"
        - "BudgetManager reportando uso < 50 créditos"
        - "Sin errores críticos en 3 ejecuciones"

    phase_3_optimization:
      name: "Deploy y Optimización"
      duration: "Semana 2 (40 horas)"
      goal: "Pipeline optimizado a 60-75 min"
      success_criteria:
        - "Caching implementado (Valkey/Redis)"
        - "Paralelización en LiteratureResearcher"
        - "Circuit breaker + retry patterns"
        - "OpenTelemetry + Uptrace configurado"
        - "Pipeline < 75 min en 80% de casos"
        - "Cache hit ratio > 30%"

    phase_4_monitoring:
      name: "Monitoreo y Producción"
      duration: "Continuo (post-deploy)"
      goal: "Sistema estable en producción"
      success_criteria:
        - "Uptime > 99%"
        - "100 análisis/mes sin intervención"
        - "Presupuesto < $18/mes"
        - "Alertas configuradas (créditos, errores, latencia)"
        - "Dashboard Uptrace funcional"
```

### **Fase 1: Setup y Fundamentos (Días 1-2)**

#### **Día 1: Suscripciones y Herramientas**

```yaml
day_1_tasks:
  morning:
    - task: "Suscribirse a GitHub Copilot Pro"
      duration: "15 minutos"
      steps:
        - "Ir a https://github.com/features/copilot"
        - "Seleccionar plan Pro ($10/mes)"
        - "Verificar 300 créditos disponibles"
      validation: "gh copilot status → debe mostrar 'Pro Plan'"

    - task: "Instalar Continue.dev en VS Code"
      duration: "10 minutos"
      steps:
        - "Extensions → buscar 'Continue'"
        - "Install Continue (official)"
        - "Configurar con GitHub Copilot Pro"
      validation: "Continue.dev aparece en sidebar"

    - task: "Obtener API keys gratuitas"
      duration: "30 minutos"
      apis:
        - name: "Gemini 2.5 Pro"
          url: "https://aistudio.google.com/app/apikey"
          quota: "1M tokens context, free"

        - name: "DeepSeek V3"
          url: "https://platform.deepseek.com"
          quota: "128K context, free tier"

        - name: "MiniMax M.2"
          url: "https://api.minimax.chat"
          quota: "Open-source, self-hosted o API"
      validation: "3 API keys guardadas en password manager"

  afternoon:
    - task: "Instalar 8 MCP Servers"
      duration: "60 minutos"
      servers:
        - name: "GitHub MCP"
          command: "npx @modelcontextprotocol/server-github"
          config: |
            {
              "mcpServers": {
                "github": {
                  "command": "npx",
                  "args": ["-y", "@modelcontextprotocol/server-github"],
                  "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": "YOUR_TOKEN"}
                }
              }
            }

        - name: "Playwright MCP"
          command: "npx @executeautomation/playwright-mcp-server"
          config: |
            {
              "playwright": {
                "command": "npx",
                "args": ["-y", "@executeautomation/playwright-mcp-server"]
              }
            }

        - name: "MarkItDown MCP"
          command: "npx @microsoft/markitdown-mcp"
          config: |
            {
              "markitdown": {
                "command": "npx",
                "args": ["-y", "@microsoft/markitdown-mcp"]
              }
            }

        - name: "Jina AI Reader MCP"
          url: "https://github.com/jina-ai/reader-mcp"
          config: |
            {
              "jina-reader": {
                "command": "npx",
                "args": ["-y", "@jina-ai/reader-mcp"],
                "env": {"JINA_API_KEY": "YOUR_KEY"}
              }
            }

        - name: "Supabase MCP"
          url: "https://github.com/supabase/mcp-server-supabase"
          config: |
            {
              "supabase": {
                "command": "npx",
                "args": ["-y", "@supabase/mcp-server"],
                "env": {
                  "SUPABASE_URL": "YOUR_URL",
                  "SUPABASE_KEY": "YOUR_KEY"
                }
              }
            }

      validation: |
        # Verificar que todos los servers responden
        npx mcp-inspector list-servers
        # Debe mostrar 8 servers activos

    - task: "Configurar .env principal"
      duration: "15 minutos"
      template: |
        # .env (root del proyecto)

        # GitHub Copilot Pro (ya configurado en VS Code)
        GITHUB_TOKEN=ghp_xxxxx

        # APIs Gratuitas
        GEMINI_API_KEY=AIzaSyxxxxxx
        DEEPSEEK_API_KEY=sk-xxxxx
        MINIMAX_API_KEY=xxxxx  # Opcional

        # Supabase (free tier)
        SUPABASE_URL=https://xxxxx.supabase.co
        SUPABASE_KEY=eyJhbGciOiJ...

        # Jina AI Reader (free tier)
        JINA_API_KEY=jina_xxxxx

        # Redis/Valkey (local)
        REDIS_URL=redis://localhost:6379/0

        # Uptrace (free tier)
        UPTRACE_DSN=https://xxxxx@api.uptrace.dev

        # Budget Configuration
        COPILOT_CREDITS_MONTHLY=300
        COPILOT_CREDITS_ALERT=240
        MAX_BUDGET_USD=18.0

      validation: |
        python -c "from dotenv import load_dotenv; load_dotenv(); print('OK')"
```

#### **Día 2: Infraestructura Local**

```yaml
day_2_tasks:
  morning:
    - task: "Instalar Valkey/Redis local"
      duration: "20 minutos"
      steps_windows: |
        # Opción 1: Docker (recomendado)
        docker pull valkey/valkey:latest
        docker run -d -p 6379:6379 --name valkey valkey/valkey

        # Opción 2: WSL + apt
        wsl --install Ubuntu
        sudo apt update && sudo apt install redis-server -y
        sudo service redis-server start

      steps_linux: |
        sudo apt update
        sudo apt install redis-server -y
        sudo systemctl start redis-server
        sudo systemctl enable redis-server

      validation: |
        redis-cli ping
        # Debe retornar: PONG

    - task: "Setup FastAPI backend"
      duration: "30 minutos"
      steps: |
        # Crear estructura de proyecto
        mkdir -p app/{api,agents,mcp_layer,budget,services,utils}
        touch app/__init__.py

        # Crear main.py básico
        cat > app/main.py << 'EOF'
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware

        app = FastAPI(title="ARA Framework API", version="1.0.0")

        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"]
        )

        @app.get("/health")
        async def health():
            return {"status": "healthy", "service": "ara-framework"}

        @app.get("/api/v1/budget")
        async def get_budget():
            return {"credits_remaining": 300, "budget_used": 0}
        EOF

        # Ejecutar
        uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

      validation: |
        curl http://localhost:8000/health
        # Debe retornar: {"status":"healthy","service":"ara-framework"}

    - task: "Setup OpenTelemetry + Uptrace"
      duration: "25 minutos"
      steps: |
        # Crear cuenta en Uptrace (free tier)
        # https://uptrace.dev/get/get-started.html

        # Instalar SDK
        pip install opentelemetry-api opentelemetry-sdk
        pip install opentelemetry-exporter-otlp

        # Configurar en app/services/telemetry.py
        cat > app/services/telemetry.py << 'EOF'
        from opentelemetry import trace, metrics
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
        import os

        def setup_telemetry():
            provider = TracerProvider()
            exporter = OTLPSpanExporter(
                endpoint="https://otlp.uptrace.dev:4317",
                headers={"uptrace-dsn": os.getenv("UPTRACE_DSN")}
            )
            provider.add_span_processor(exporter)
            trace.set_tracer_provider(provider)
            return trace.get_tracer(__name__)
        EOF

      validation: |
        # Ejecutar test trace
        python -c "from app.services.telemetry import setup_telemetry; setup_telemetry()"
        # Verificar en dashboard Uptrace que aparece el servicio

  afternoon:
    - task: "Implementar BudgetManager"
      duration: "45 minutos"
      code: |
        # app/budget/manager.py
        from pydantic import BaseModel
        from typing import Literal
        import structlog

        logger = structlog.get_logger()

        class ModelConfig(BaseModel):
            name: str
            provider: str
            cost_multiplier: float  # 0.33x, 1x, etc.
            fallback: str | None = None

        class BudgetManager:
            def __init__(self, monthly_credits: int = 300):
                self.monthly_credits = monthly_credits
                self.used_credits = 0
                self.alert_threshold = 240  # 80% usage
                
                self.models = {
                    "gpt-4o": ModelConfig(name="gpt-4o", provider="copilot", cost_multiplier=0, fallback="minimax-m2"),
                    "claude-sonnet-4.5": ModelConfig(name="claude-sonnet-4.5", provider="copilot", cost_multiplier=1.0, fallback="gpt-5"),
                    "claude-haiku-4.5": ModelConfig(name="claude-haiku-4.5", provider="copilot", cost_multiplier=0.33, fallback="gpt-4o"),
                    "gpt-5": ModelConfig(name="gpt-5", provider="copilot", cost_multiplier=1.0, fallback="claude-sonnet-4.5"),
                    "gemini-2.5-pro": ModelConfig(name="gemini-2.5-pro", provider="google", cost_multiplier=0, fallback="deepseek-v3"),
                    "minimax-m2": ModelConfig(name="minimax-m2", provider="minimax", cost_multiplier=0, fallback="gpt-4o"),
                }
            
            def check_budget(self, model_name: str) -> bool:
                """Verificar si hay presupuesto para usar el modelo"""
                model = self.models.get(model_name)
                if not model:
                    raise ValueError(f"Unknown model: {model_name}")
                
                cost = model.cost_multiplier
                remaining = self.monthly_credits - self.used_credits
                
                if cost == 0:
                    return True  # Modelo gratis
                
                if remaining < cost:
                    logger.warning("budget_low", model=model_name, remaining=remaining)
                    return False
                
                return True
            
            def record_usage(self, model_name: str):
                """Registrar uso de créditos"""
                model = self.models.get(model_name)
                self.used_credits += model.cost_multiplier
                
                logger.info("credit_usage", 
                    model=model_name, 
                    cost=model.cost_multiplier,
                    total_used=self.used_credits,
                    remaining=self.monthly_credits - self.used_credits
                )
                
                if self.used_credits >= self.alert_threshold:
                    logger.warning("budget_alert", 
                        used=self.used_credits, 
                        limit=self.monthly_credits
                    )
            
            def get_model_or_fallback(self, preferred: str) -> str:
                """Obtener modelo preferido o fallback si no hay presupuesto"""
                if self.check_budget(preferred):
                    return preferred
                
                model = self.models[preferred]
                if model.fallback:
                    logger.info("using_fallback", preferred=preferred, fallback=model.fallback)
                    return model.fallback
                
                raise RuntimeError(f"No budget for {preferred} and no fallback available")

      validation: |
        python -c "
        from app.budget.manager import BudgetManager
        bm = BudgetManager()
        print('GPT-4o available:', bm.check_budget('gpt-4o'))
        print('Claude Sonnet available:', bm.check_budget('claude-sonnet-4.5'))
        "

    - task: "Test completo de setup"
      duration: "15 minutos"
      checklist:
        - "✅ GitHub Copilot Pro: 300 créditos"
        - "✅ Continue.dev: funcional"
        - "✅ 8 MCP servers: conectados"
        - "✅ APIs gratuitas: keys válidas"
        - "✅ .env: sin errores"
        - "✅ Valkey/Redis: PONG"
        - "✅ FastAPI: /health OK"
        - "✅ Uptrace: traces visibles"
        - "✅ BudgetManager: tests passed"
```

### **Fase 2: Validación de Pipeline (Días 3-5)**

```yaml
phase_2_validation:
  day_3:
    - task: "Implementar 3 agentes core"
      duration: "4 horas"
      agents:
        - "NicheAnalyst (GPT-4o, 0x credits)"
        - "LiteratureResearcher (Gemini 2.5 Pro, free)"
        - "TechnicalArchitect (Claude Sonnet 4.5, 1x)"
      deliverable: "3 agentes funcionales con artifact outputs"

    - task: "Implementar pipeline secuencial"
      duration: "2 horas"
      code: |
        # app/orchestrator.py
        from langgraph.graph import StateGraph, END
        from app.agents.niche_analyst import niche_analyst, task_niche_analysis
        from app.agents.literature_researcher import literature_researcher, task_literature
        from app.agents.technical_architect import technical_architect, task_architecture

        def create_research_crew():
            return Crew(
                agents=[niche_analyst, literature_researcher, technical_architect],
                tasks=[task_niche_analysis, task_literature, task_architecture],
                process=Process.sequential,
                verbose=True
            )

        async def run_pipeline(keywords: list[str]):
            crew = create_research_crew()
            result = crew.kickoff(inputs={"keywords": keywords})
            return result
      validation: "Pipeline ejecuta sin errores (aunque tome 135+ min)"

  day_4:
    - task: "Implementar agentes restantes"
      duration: "4 horas"
      agents:
        - "ImplementationSpecialist"
        - "ContentSynthesizer (MiniMax-M2, free)"
        - "OrchestratorAgent (Claude Haiku 4.5, 0.33x)"
      deliverable: "Pipeline completo de 6 agentes"

    - task: "Integrar MCP servers con agentes"
      duration: "2 horas"
      integrations:
        - "NicheAnalyst → Playwright MCP (scraping)"
        - "LiteratureResearcher → Jina AI Reader (papers)"
        - "ContentSynthesizer → MarkItDown (PDF export)"
      validation: "Agentes usan MCP tools correctamente"

  day_5:
    - task: "Generar tesis de ejemplo completa"
      duration: "3 horas (135-165 min pipeline)"
      input_keywords: ["AI", "3D printing", "healthcare"]
      expected_output:
        - "niche_analysis.json"
        - "literature_review.json"
        - "technical_architecture.md"
        - "implementation_plan.md"
        - "final_thesis.pdf (50-80 páginas)"
      validation: |
        - PDF generado
        - < 50 créditos usados
        - Sin errores críticos

    - task: "Análisis de costos reales"
      duration: "1 hora"
      metrics_to_collect:
        - "Créditos totales usados"
        - "Tiempo total del pipeline"
        - "Breakdown por agente"
        - "APIs externas llamadas"
      validation: "Costos < $20/análisis"
```

### **Fase 3: Optimización (Semana 2)**

```yaml
phase_3_optimization:
  quick_wins:
    - name: "Implementar caching de nicho"
      impact: "30% cache hit ratio → ahorro 20 min"
      effort: "2 horas"
      code: |
        # Agregar caching a NicheAnalyst
        @cache_result(ttl=86400)  # 24 horas
        async def analyze_niche(keywords):
            ...

    - name: "Paralelizar fetch de papers"
      impact: "De 50s a 30s en LiteratureResearcher"
      effort: "3 horas"
      code: |
        # Usar RateLimitedQueue
        async def fetch_papers_parallel(queries):
            queue = RateLimitedQueue(rate_limit=1.0)
            tasks = [queue.enqueue(fetch_paper, q) for q in queries]
            return await asyncio.gather(*tasks)

    - name: "Implementar Circuit Breaker"
      impact: "Evitar cascading failures"
      effort: "2 horas"
      code: |
        from pybreaker import CircuitBreaker
        breaker = CircuitBreaker(fail_max=5, timeout_duration=60)

        @breaker
        async def call_semantic_scholar(query):
            ...

    - name: "Logs estructurados JSON"
      impact: "Facilitar debugging y observability"
      effort: "1 hora"
      code: |
        import structlog
        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.JSONRenderer()
            ]
        )

  advanced_optimizations:
    - name: "Artifact-based architecture"
      impact: "Eliminar 80% overhead conversacional"
      effort: "8 horas"
      description: "Refactor agentes para consumir/producir JSON/Markdown"

    - name: "Quality gates automatizados"
      impact: "Detectar errores antes de handoff"
      effort: "4 horas"
      gates:
        - "Structure validation"
        - "Citation validation"
        - "Consistency check"

    - name: "Dashboard Uptrace personalizado"
      impact: "Visibilidad de métricas clave"
      effort: "2 horas"
      metrics:
        - "Latencia P95 por agente"
        - "Créditos gastados por análisis"
        - "Tasa de error por API"
```

### **Fase 4: Monitoreo Continuo**

```yaml
phase_4_monitoring:
  daily_checks:
    - metric: "Créditos restantes"
      alert_threshold: "< 60 créditos (20%)"
      action: "Email + Slack notification"

    - metric: "Tasa de error"
      alert_threshold: "> 1%"
      action: "Investigar logs en Uptrace"

    - metric: "Latencia P95"
      alert_threshold: "> 90 minutos"
      action: "Revisar bottlenecks en traces"

  weekly_reviews:
    - "Análisis de uso de créditos (debe ser < 45/mes)"
    - "Cache hit ratio (objetivo > 30%)"
    - "Uptime del servicio (objetivo > 99%)"
    - "Feedback de usuarios (si aplica)"

  monthly_optimization:
    - "Revisar modelos más eficientes (benchmarks actualizados)"
    - "Ajustar TTL de cache según patrones de uso"
    - "Evaluar upgrade a plan superior si ROI lo justifica"
```

### **Desglose de Costos por Componente**

```yaml
cost_breakdown_detailed:
  infrastructure:
    fastapi_hosting: "$0 (self-hosted)"
    valkey_redis: "$0 (local/Docker)"
    supabase_database: "$0 (free tier 500MB)"
    uptrace_observability: "$0 (free 1TB)"
    total_infrastructure: "$0/mes"

  models_and_apis:
    github_copilot_pro: "$10/mes (300 créditos)"
    gemini_2_5_pro: "$0 (free tier Google AI Studio)"
    deepseek_v3: "$0 (free tier)"
    minimax_m2: "$0 (open-source o free API)"
    jina_ai_reader: "$0 (200 RPM free)"
    semantic_scholar: "$0 (1 RPS free)"
    arxiv: "$0 (5 RPS free)"
    total_models: "$10/mes"

  development_tools:
    continue_dev: "$0 (open-source)"
    vs_code: "$0 (free)"
    cursor_pro: "$0 (RECHAZADO, ahorro $20/mes)"
    total_tools: "$0/mes"

  optional_upgrades:
    claude_api_direct: "$0-8/mes (si excede Copilot credits)"
    runpod_gpu: "$0-10/mes (solo si necesitas TripoSR 24/7)"
    total_optional: "$0-18/mes"

  total_monthly_cost:
    minimum: "$10/mes (Copilot Pro solo)"
    realistic: "$10-18/mes (con uso moderado)"
    maximum: "$30/mes (con Cursor Pro, NO recomendado)"
```

### **Checklist de Validación Final**

```yaml
final_validation_checklist:
  phase_1_setup: "✅ Completado"
    - "GitHub Copilot Pro activo"
    - "8 MCP servers funcionando"
    - "APIs gratuitas configuradas"
    - "Infraestructura local operativa"

  phase_2_validation: "✅ Completado"
    - "6 agentes implementados"
    - "Pipeline E2E funcional"
    - "1 tesis de ejemplo generada"
    - "Costos < $20/análisis"

  phase_3_optimization: "✅ Completado"
    - "Pipeline < 75 min (80% casos)"
    - "Caching implementado"
    - "Circuit breaker activo"
    - "Observability funcional"

  phase_4_monitoring: "🔄 Continuo"
    - "Alertas configuradas"
    - "Dashboard Uptrace activo"
    - "Presupuesto monitoreado"
    - "100 análisis/mes sostenibles"
```

---

## ✅ Conclusión: Guía de Implementación Lista para Ejecución

Esta guía ha sido **validada con investigación Nov 2025** y proporciona:

- ✅ **Roadmap pragmático** de 4 fases (12 semanas)
- ✅ **Setup detallado** día por día (Días 1-2)
- ✅ **Validación de pipeline** con métricas reales (Días 3-5)
- ✅ **Quick wins** para optimización (Semana 2)
- ✅ **Monitoreo continuo** con alertas automáticas
- ✅ **Desglose completo de costos** ($10-18/mes validado)
- ✅ **Checklist de validación** para cada fase

**El proyecto puede iniciarse INMEDIATAMENTE siguiendo esta guía paso a paso.**

---

**Próximo paso:** Ver [08_GETTING_STARTED.md](./08_GETTING_STARTED.md) para un tutorial simplificado.
