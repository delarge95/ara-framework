# 🔍 Análisis: Acceso a APIs Premium desde tus Suscripciones

**Fecha**: 12 Nov 2025  
**Objetivo**: Usar modelos incluidos en GitHub Copilot Pro, Perplexity Pro y Cursor

---

## 📊 Resumen Ejecutivo

| Plataforma             | Acceso API Programático       | Modelos Incluidos                                | Viabilidad           |
| ---------------------- | ----------------------------- | ------------------------------------------------ | -------------------- |
| **GitHub Copilot Pro** | ✅ **SÍ** (vía GitHub Models) | Claude Sonnet 4.5, GPT-4o, GPT-5, Gemini 2.5 Pro | ⭐⭐⭐⭐⭐ **IDEAL** |
| **Perplexity Pro**     | ✅ **SÍ** (API separada)      | Sonar Pro, Claude, GPT-4                         | ⭐⭐⭐⭐ Buena       |
| **Cursor**             | ❌ **NO** (solo IDE)          | Claude, GPT-4, Gemini                            | ⭐ No viable         |

**Recomendación**: Usar **GitHub Copilot Pro + Perplexity API** juntos.

---

## 1️⃣ GitHub Copilot Pro (TU MEJOR OPCIÓN)

### ✅ Acceso Programático: GitHub Models API

**Descripción**: GitHub Copilot Pro incluye acceso a **GitHub Models**, que son los mismos modelos premium pero con API REST pública.

### 📋 Modelos Disponibles (según tu screenshot):

```
✅ GPT-4.1          - Último modelo de OpenAI
✅ GPT-4o           - Modelo multimodal de OpenAI
✅ GPT-5 mini       - Versión ligera de GPT-5
✅ Claude Sonnet 4.5 - El mejor modelo de Anthropic
✅ Claude Sonnet 4  - Versión anterior
✅ Claude Haiku 4.5 - Modelo rápido de Anthropic
✅ Gemini 2.5 Pro   - Modelo de Google (1M tokens contexto)
✅ GPT-5            - Modelo más avanzado de OpenAI
✅ GPT-5-Codex (Preview) - Especializado en código
✅ Grok Code Fast 1 - Modelo de xAI
```

### 🔑 Cómo Obtener el Token

#### Opción A: Token Personal de GitHub (RECOMENDADO)

```bash
# 1. Ir a: https://github.com/settings/tokens
# 2. Click en "Generate new token (classic)"
# 3. Seleccionar scopes:
#    ✅ read:packages (REQUERIDO para GitHub Models)
#    ✅ read:user (opcional)
# 4. Copiar el token (empieza con ghp_)
# 5. Agregar a .env:
GITHUB_TOKEN=ghp_tu_token_aqui_xxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Límites**:

- **50 requests por día** por modelo (ya lo sabes por el error 429)
- Se resetea cada 24 horas
- **GRATIS** incluido en tu suscripción de Copilot Pro ($10/mes)

#### Opción B: Token OAuth de Copilot (MÁS LÍMITES)

Copilot usa OAuth internamente, pero tiene límites más estrictos:

- ~300 requests premium/mes
- Requiere autenticación OAuth compleja
- No recomendado para uso programático

### 💻 Implementación en ARA Framework

**Ya está implementado** en tu código actual:

```python
# core/model_factory.py (línea 40)
from langchain_openai import AzureChatOpenAI

llm = AzureChatOpenAI(
    api_key=settings.GITHUB_TOKEN,  # ← Tu token de GitHub
    azure_endpoint="https://models.inference.ai.azure.com",
    api_version="2024-05-01-preview",
    model="gpt-4o",  # o cualquier modelo de la lista
    temperature=0.7,
)
```

### 🎯 Estrategia Recomendada con GitHub Models

```yaml
# Distribución inteligente para maximizar los 50 req/día por modelo

Agent 1 (Niche Analyst):
  modelo: Claude Sonnet 4.5 # Mejor análisis cualitativo
  requests: ~1 por pipeline

Agent 2 (Literature Researcher):
  modelo: Gemini 2.5 Pro # 1M tokens contexto = cabe 40 papers
  requests: ~1 por pipeline
  fallback: GPT-4o (si Gemini falla)

Agent 3 (Technical Architect):
  modelo: GPT-5-Codex # Especializado en arquitectura
  requests: ~1 por pipeline

Agent 4 (Implementation Specialist):
  modelo: GPT-5-Codex # Especializado en código
  requests: ~1 por pipeline

Agent 5 (Content Synthesizer):
  modelo: GPT-5 # Mejor síntesis y escritura
  requests: ~1 por pipeline

Total: 5 requests/pipeline × 5 modelos = 25 requests/día
Capacidad: 5 pipelines completos/día sin repetir modelos
```

**Ventajas**:

- ✅ Cada agente usa el modelo más apropiado
- ✅ Distribución entre modelos evita rate limits
- ✅ 128K-1M contexto (suficiente para todos los agentes)
- ✅ Tool calling robusto en todos los modelos
- ✅ Calidad superior a Ollama Mistral 7B

---

## 2️⃣ Perplexity Pro API

### ✅ Acceso Programático: Perplexity API

**Descripción**: Perplexity Pro ($20/mes) **NO incluye créditos API**. Debes pagar por la API por separado.

### 📋 Modelos Disponibles

```
Perplexity Sonar Pro (128K contexto)
  - Búsqueda web en tiempo real
  - Citas automáticas
  - Ideal para: Agent 1 (Niche Analyst)

Claude 3.5 Sonnet (200K contexto)
  - Vía Perplexity API
  - Más caro que directo

GPT-4 Turbo (128K contexto)
  - Vía Perplexity API
```

### 💰 Precios API (ADICIONAL a tu suscripción Pro)

```
Sonar Pro:
  - $3.00 / 1M input tokens
  - $15.00 / 1M output tokens

Claude 3.5 Sonnet (vía Perplexity):
  - $3.00 / 1M input tokens
  - $15.00 / 1M output tokens
```

### 🔑 Cómo Obtener API Key

```bash
# 1. Ir a: https://www.perplexity.ai/settings/api
# 2. Click "Create API Key"
# 3. Copiar el key (empieza con pplx-)
# 4. Agregar a .env:
PERPLEXITY_API_KEY=pplx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 💻 Implementación

```python
# Agregar a core/model_factory.py
from openai import OpenAI

def create_perplexity_model(model: str = "sonar-pro", temperature: float = 0.7):
    """Create Perplexity API client (OpenAI-compatible)."""
    return OpenAI(
        api_key=settings.PERPLEXITY_API_KEY,
        base_url="https://api.perplexity.ai",
    ).chat.completions.create(
        model=model,
        temperature=temperature,
    )
```

### 🎯 Caso de Uso Ideal

**Agent 1 (Niche Analyst)** con Sonar Pro:

- Búsqueda web en tiempo real
- Análisis de tendencias actuales
- Citas automáticas de fuentes
- ~$0.50 por análisis completo

**Costo estimado**: ~$15/mes para 30 análisis (1 por día)

### ⚠️ Limitación

**Tu suscripción Perplexity Pro ($20/mes)** te da:

- ✅ Búsquedas ilimitadas en la web UI
- ✅ Acceso a Claude, GPT-4 en UI
- ❌ **NO incluye créditos API**

**Debes pagar API por separado** → No es la mejor opción económica.

---

## 3️⃣ Cursor (NO VIABLE)

### ❌ Sin Acceso API Programático

**Descripción**: Cursor es un IDE (fork de VS Code) con IA integrada. **No expone API pública**.

### 📋 Lo que incluye tu suscripción

```
Cursor Pro ($20/mes):
  - Chat con Claude/GPT-4/Gemini en el IDE
  - Autocompletado de código
  - Agents para tareas de desarrollo

  ❌ NO tiene API REST
  ❌ NO se puede usar fuera del IDE
  ❌ NO compatible con LangChain/LangGraph
```

### 🔧 ¿Alternativa?

**Cursor Rules** (experimental):

- Puedes crear reglas personalizadas en `.cursorrules`
- Pero sigue siendo solo dentro del IDE
- No sirve para pipelines automatizados

### 🎯 Mejor Uso de Cursor

1. **Desarrollo del framework** (editar código de ARA)
2. **Debugging interactivo** (usar Cursor Agent)
3. **Documentación** (generar docs con IA)

**No usar para**: Ejecución de pipelines de investigación.

---

## 📊 Comparación de Costos

### Escenario: 100 análisis/mes (pipeline completo)

| Opción              | Modelos               | Costo/Mes                        | Límites           | Viabilidad           |
| ------------------- | --------------------- | -------------------------------- | ----------------- | -------------------- |
| **GitHub Models**   | Claude, GPT-5, Gemini | **$0** (incluido en Copilot Pro) | 50 req/día/modelo | ⭐⭐⭐⭐⭐ **IDEAL** |
| **Perplexity API**  | Sonar Pro, Claude     | ~$50 (API adicional)             | Sin límite        | ⭐⭐⭐ Caro          |
| **Ollama (actual)** | Mistral 7B            | $0 (local)                       | Sin límite        | ⭐⭐⭐ Calidad baja  |
| **Cursor**          | N/A                   | N/A                              | No disponible     | ❌ No viable         |

### Híbrido Óptimo (RECOMENDACIÓN FINAL)

```yaml
Costo Total: $10/mes (solo Copilot Pro que ya tienes)

Distribución:
  80% de requests: GitHub Models (Claude, GPT-5, Gemini)
    - Agent 1-5: 5 modelos diferentes por pipeline
    - Capacidad: ~10 pipelines/día = 300/mes

  20% de requests: Ollama Mistral 7B (fallback local)
    - Cuando se agoten los 50 req/día de algún modelo
    - Para testing y desarrollo iterativo

  0% de requests: Perplexity API
    - No vale la pena el costo adicional
    - GitHub Models es gratis y mejor

Resultado:
  ✅ 300 pipelines completos/mes
  ✅ Calidad superior (Claude Sonnet, GPT-5)
  ✅ Sin costo adicional
  ✅ Fallback ilimitado con Ollama
```

---

## 🚀 Plan de Implementación

### Fase 1: Configurar GitHub Models (15 min)

```bash
# 1. Obtener token
# Ir a: https://github.com/settings/tokens
# Generate new token (classic)
# Scope: read:packages ✅
# Copiar token (ghp_xxx...)

# 2. Agregar a .env
echo "GITHUB_TOKEN=ghp_tu_token_aqui" >> ara_framework/.env

# 3. Verificar
cd ara_framework
python test_github_models_env.py
```

### Fase 2: Modificar model_factory.py (30 min)

```python
# core/model_factory.py

def create_model_smart(
    agent_name: str,
    temperature: float = 0.7,
) -> BaseChatModel:
    """
    Selección inteligente de modelo por agente.
    Maximiza uso de GitHub Models gratis.
    """

    # Mapa agente → modelo óptimo
    MODEL_MAP = {
        "niche_analyst": {
            "provider": "github",
            "model": "Claude-3.5-Sonnet",  # Mejor análisis cualitativo
        },
        "literature_researcher": {
            "provider": "github",
            "model": "Gemini-2.5-Pro",  # 1M contexto para 40 papers
        },
        "technical_architect": {
            "provider": "github",
            "model": "gpt-5-codex-preview",  # Especialista código
        },
        "implementation_specialist": {
            "provider": "github",
            "model": "gpt-5-codex-preview",  # Especialista código
        },
        "content_synthesizer": {
            "provider": "github",
            "model": "gpt-5",  # Mejor escritura
        },
    }

    config = MODEL_MAP.get(agent_name)

    if not config:
        # Fallback a Ollama
        logger.warning(f"Agent {agent_name} no configurado, usando Ollama")
        return create_ollama_model(temperature=temperature)

    try:
        # Intentar GitHub Models primero
        return create_github_model(
            model=config["model"],
            temperature=temperature,
        )
    except Exception as e:
        # Si falla (rate limit), usar Ollama
        logger.warning(
            f"GitHub Models falló para {agent_name}: {e}. Usando Ollama."
        )
        return create_ollama_model(temperature=temperature)
```

### Fase 3: Actualizar research_graph.py (15 min)

```python
# graphs/research_graph.py (modificar cada agente)

def niche_analyst_node(state):
    llm = create_model_smart(
        agent_name="niche_analyst",  # ← Selección automática
        temperature=0.7,
    )
    # resto del código igual...

def literature_researcher_node(state):
    llm = create_model_smart(
        agent_name="literature_researcher",
        temperature=0.7,
    )
    # resto del código igual...

# Repetir para Agent 3, 4, 5...
```

### Fase 4: Testing (20 min)

```bash
# Test 1: Verificar GitHub Models
python test_github_models_env.py

# Test 2: Pipeline completo con GitHub Models
$env:USE_GITHUB_MODELS="true"
python test_pipeline.py

# Test 3: Comparación GitHub vs Ollama
python test_github_vs_ollama.py  # Crear este script
```

### Fase 5: Monitoreo de Rate Limits (10 min)

```python
# Crear ara_framework/monitor_github_limits.py

import os
import requests
from datetime import datetime

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def check_rate_limits():
    """Verifica límites restantes de GitHub Models."""

    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

    # GitHub Models usa el mismo rate limit que GitHub API
    response = requests.get(
        "https://api.github.com/rate_limit",
        headers=headers,
    )

    data = response.json()

    print("\n" + "="*60)
    print("📊 GITHUB MODELS - LÍMITES RESTANTES")
    print("="*60)

    core = data["resources"]["core"]
    print(f"\n✅ Requests disponibles: {core['remaining']}/{core['limit']}")
    print(f"⏰ Reset en: {datetime.fromtimestamp(core['reset'])}")

    # Calcular requests por modelo (estimado)
    models_count = 9  # Número de modelos en tu screenshot
    per_model = 50  # Límite por modelo/día

    print(f"\n📊 Estimado por modelo:")
    print(f"   • Límite por modelo: {per_model} req/día")
    print(f"   • Modelos disponibles: {models_count}")
    print(f"   • Capacity total: {per_model * models_count} req/día")

    print("\n" + "="*60)

if __name__ == "__main__":
    check_rate_limits()
```

---

## 🎯 Próximos Pasos (ACCIÓN INMEDIATA)

### 1. Configurar GitHub Token (HOY - 5 min)

```bash
# Windows PowerShell
cd D:\Downloads\TRABAJO_DE_GRADO\ara_framework

# Ir a: https://github.com/settings/tokens
# Generate new token (classic)
# Scope: read:packages ✅
# Copiar token

# Agregar a .env
echo "GITHUB_TOKEN=ghp_tu_token_aqui" >> .env

# Verificar
python test_github_models_env.py
```

### 2. Esperar a mañana para test completo (13 Nov)

**Razón**: Tu límite actual se resetea en ~19 horas.

**Entonces ejecutar**:

```bash
# Mañana 13 Nov, ~11:00 AM
$env:USE_GITHUB_MODELS="true"
python test_pipeline.py
```

### 3. Implementar selección inteligente (Mañana - 1 hora)

Modificar `model_factory.py` y `research_graph.py` según Fase 2-3 arriba.

---

## 📝 Conclusión

### ✅ Respuesta a tu pregunta:

**"¿Puedo usar las IAs incluidas en Copilot Pro, Perplexity Pro y Cursor?"**

- ✅ **GitHub Copilot Pro**: SÍ, vía GitHub Models API (ya configurado en tu código)
- ⚠️ **Perplexity Pro**: SÍ, pero requiere pago adicional de API (~$50/mes extra)
- ❌ **Cursor**: NO, es solo IDE sin API programática

### 🏆 Recomendación Final:

**Usar exclusivamente GitHub Copilot Pro** con la estrategia de distribución de modelos:

```
Pipeline → 5 agentes → 5 modelos diferentes → 1 request c/u
= 5 requests/pipeline
= 10 pipelines/día posibles (50 req/día por modelo)
= 300 pipelines/mes
= $0 adicional (incluido en tu $10/mes de Copilot Pro)
```

**Resultado**: Calidad superior a Ollama, sin costo adicional, y capacidad suficiente para tu trabajo de grado.

---

**Generado**: 12 Nov 2025  
**Siguiente paso**: Configurar `GITHUB_TOKEN` y esperar a mañana para ejecutar pipeline completo.
