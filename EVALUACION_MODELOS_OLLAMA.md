# Evaluación de Modelos Ollama para Reemplazo de GitHub Models

**Fecha:** 2025
**Objetivo:** Identificar modelo local en Ollama que soporte tool calling para reemplazar GitHub Models (gpt-4o)

---

## 🎯 RESUMEN EJECUTIVO

### ✅ MODELO RECOMENDADO: **Mistral 7B v0.3**

**Razón:** Único modelo verificado con soporte explícito de function calling (tool calling) en Ollama.

---

## 📋 CRITERIOS DE EVALUACIÓN

### Requisitos Críticos (No Negociables)

1. **Tool Calling Support**: ✅ OBLIGATORIO

   - Sistema usa LangChain con decoradores `@tool`
   - Agents 1-2 requieren `search_recent_papers` y `scrape_website`
   - Sin tool calling: outputs caen a 79-95 caracteres (probado en v2.0)

2. **Contexto Mínimo**: 32K tokens

   - 15 papers = ~19K tokens en resultados
   - Necesario para system prompts + razonamiento

3. **Compatibilidad LangChain**:

   - Debe funcionar con `ChatOllama` o `Ollama`
   - API compatible con OpenAI

4. **Tamaño del Modelo**: ≤ 8B parámetros
   - PC no soporta modelos grandes
   - Máximo ~5GB en disco

---

## 🔍 ANÁLISIS DE MODELOS DISPONIBLES

### ✅ TIER 1: CONFIRMADO FUNCIONAL

#### **Mistral 7B v0.3** ⭐ RECOMENDADO

```
✅ Tool Calling: SÍ (Explícitamente documentado)
✅ Context: 32K tokens
✅ Tamaño: 4.4GB
✅ LangChain: Soportado con ChatOllama + bind_tools()
✅ Documentación: Ejemplos de function calling en raw mode
```

**Evidencia:**

- Documentación oficial: "Mistral 0.3 supports function calling"
- Formato: `[AVAILABLE_TOOLS]` con estructura OpenAI-compatible
- Ejemplo documentado:
  ```json
  [AVAILABLE_TOOLS] [{"type": "function", "function": {...}}][/AVAILABLE_TOOLS]
  [INST] What is the weather like today in San Francisco [/INST]
  [TOOL_CALLS] [{"name": "get_current_weather", "arguments": {...}}]
  ```

**Comando de instalación:**

```bash
ollama pull mistral:7b
```

**Integración con LangChain:**

```python
from langchain_ollama import ChatOllama
from langchain.tools import tool

@tool
def search_recent_papers(query: str, max_results: int = 15):
    """Search Semantic Scholar for recent papers"""
    pass

llm = ChatOllama(
    model="mistral:7b",
    temperature=0
).bind_tools([search_recent_papers])
```

---

### ❓ TIER 2: POSIBLEMENTE FUNCIONAL (Requiere Pruebas)

#### **Qwen2.5 8B**

```
❓ Tool Calling: NO CONFIRMADO (etiqueta "tools" pero sin documentación explícita)
✅ Context: 32K tokens (128K en versiones más grandes)
✅ Tamaño: 4.7GB
✅ JSON: Generación estructurada mejorada (mencionado en docs)
⚠️  Necesita verificación: GitHub repo o comunidad LangChain
```

**Estado:**

- Tag "tools" visible en Ollama Library
- Fuerte capacidad de JSON generation
- Sin ejemplos explícitos de function calling
- Qwen3 menciona "tool use" en documentación general
- **Acción requerida**: Probar con LangChain `bind_tools()`

**Comando de instalación:**

```bash
ollama pull qwen2.5:8b
```

#### **Phi3 3.8B**

```
❌ Tool Calling: NO MENCIONADO en documentación
✅✅ Context: 128K tokens (excelente!)
✅ Tamaño: 2.2GB (muy eficiente)
✅ Capacidades: Razonamiento, matemáticas, código
⚠️  Foco: Instruction following, no tool use
```

**Estado:**

- Documentación NO menciona function calling
- Enfoque en razonamiento y contexto largo
- Probable que NO soporte tool calling nativamente
- **Recomendación**: Solo si Mistral y Qwen fallan

---

### ⛔ TIER 3: NO RECOMENDADOS

#### **Gemma2 4B**

```
❌ Tool Calling: NO MENCIONADO
⚠️  Context: Solo 8K tokens (insuficiente para 15 papers)
✅ Tamaño: 1.6GB (versión 2b)
❌ Documentación: Solo casos de uso generales
```

**Razón de descarte:** Contexto insuficiente + sin tool calling

#### **Zephyr 7B**

```
❓ Tool Calling: NO MENCIONADO
✅ Context: 32K tokens
✅ Tamaño: 4.1GB
ℹ️  Nota: Basado en Mistral (fine-tuned)
```

**Razón de descarte:** Sin evidencia de tool calling (aunque base es Mistral)

#### **DeepSeek-Coder 6.7B**

```
❌ Tool Calling: NO MENCIONADO
✅ Context: 16K tokens (límite)
✅ Tamaño: 3.8GB
⚠️  Enfoque: Code generation (no tool use)
```

**Razón de descarte:** Especializado en código, no tool calling

#### **CodeGemma 7B**

```
❌ Tool Calling: NO INVESTIGADO (probablemente no)
❓ Context: Desconocido
⚠️  Enfoque: Code generation
```

**Razón de descarte:** Similar a DeepSeek-Coder

#### **Nomic-Embed-Text**

```
❌ No aplicable: Modelo de embeddings
```

#### **Llava 7B**

```
❌ No aplicable: Modelo de visión (multimodal)
```

---

## 🔧 INTEGRACIÓN CON LANGCHAIN

### Documentación Oficial Verificada

**Fuente:** https://python.langchain.com/docs/integrations/chat/ollama

**Soporte de Tool Calling:**

```python
# ChatOllama soporta bind_tools() con modelos compatibles
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="mistral:7b",  # Modelo con tool support
    temperature=0
).bind_tools([validate_user])  # Método estándar de LangChain

result = llm.invoke("Could you validate user 123?")
# Output: result.tool_calls contiene llamadas estructuradas
```

**Requisitos:**

- `langchain-ollama` package instalado
- Ollama server corriendo (`ollama serve`)
- Modelo debe estar en lista de [modelos con tool support](https://ollama.com/search?&c=tools)

---

## 📊 COMPARACIÓN CON GITHUB MODELS

| Característica     | GitHub Models (gpt-4o) | Mistral 7B v0.3 (Ollama) |
| ------------------ | ---------------------- | ------------------------ |
| **Tool Calling**   | ✅ Completo            | ✅ Soportado (raw mode)  |
| **Context**        | 128K tokens            | 32K tokens               |
| **Límite Request** | 8K tokens body         | Sin límite local         |
| **Rate Limit**     | 50 req/day             | ∞ (local)                |
| **Costo**          | $0.00 (beta)           | $0.00 (local)            |
| **Velocidad**      | API (variable)         | Local (depende GPU)      |
| **Disponibilidad** | Requiere internet      | Offline                  |

**Ventajas de Mistral Local:**

- ✅ Sin rate limits (desarrollo ilimitado)
- ✅ Sin dependencia de internet
- ✅ Sin costos futuros (post-beta)

**Desventajas:**

- ⚠️ Contexto menor (32K vs 128K)
- ⚠️ Requiere hardware adecuado
- ⚠️ Posible reducción en calidad de outputs vs gpt-4o

---

## 🧪 PLAN DE PRUEBAS RECOMENDADO

### Fase 1: Verificación Básica de Tool Calling (30 min)

```python
# test_mistral_tools.py
from langchain_ollama import ChatOllama
from langchain_core.tools import tool

@tool("search_test")
def search_test(query: str, max_results: int = 5) -> str:
    """Test function for tool calling verification"""
    return f"Searched for: {query}, max: {max_results}"

# Configurar Mistral
llm = ChatOllama(
    model="mistral:7b",
    temperature=0
).bind_tools([search_test])

# Test 1: Verificar que reconoce la herramienta
result = llm.invoke("Search for 'deep learning' papers, max 10 results")

# Verificaciones
assert hasattr(result, 'tool_calls'), "No tool_calls attribute"
assert len(result.tool_calls) > 0, "No tool calls generated"
assert result.tool_calls[0]['name'] == 'search_test', "Wrong tool called"
print("✅ Tool calling funciona correctamente")
print(f"Tool calls: {result.tool_calls}")
```

### Fase 2: Prueba con Tools Reales (1 hora)

```python
# test_agent1_mistral.py
from graphs.research_graph import create_research_graph
from langchain_ollama import ChatOllama

# Modificar config temporalmente
test_llm = ChatOllama(
    model="mistral:7b",
    temperature=0,
    num_ctx=32768  # Contexto completo
)

# Probar con Agent 1 (Niche Analyst)
# - Usar query simple: "deep learning"
# - Max 5 papers (para prueba rápida)
# - Verificar que:
#   1. Llama search_recent_papers correctamente
#   2. Procesa resultados
#   3. Genera análisis coherente (>500 caracteres)
```

### Fase 3: Comparación de Calidad (2 horas)

**Escenarios de prueba:**

1. **Query simple:** "machine learning"

   - Comparar outputs gpt-4o vs mistral:7b
   - Métricas: longitud, coherencia, uso de herramientas

2. **Query compleja:** "transformer architectures for NLP"

   - Verificar manejo de contexto
   - Validar scraping web funciona

3. **Contexto largo:** 15 papers
   - Verificar que no excede 32K tokens
   - Medir degradación vs 5 papers

### Fase 4: Prueba End-to-End (3 horas)

```python
# Ejecutar workflow completo con Mistral
# Agents 1-5, query: "reinforcement learning"
# Documentar:
# - Tiempo total de ejecución
# - Calidad de outputs por agente
# - Errores/warnings
# - Tokens consumidos por agente
```

---

## 📝 RECOMENDACIONES FINALES

### Opción A: Usar Mistral 7B (RECOMENDADA) ✅

**Cuándo:**

- Desarrollo intensivo (muchas pruebas)
- GitHub Models rate limit alcanzado
- Necesitas trabajo offline

**Pasos:**

1. `ollama pull mistral:7b`
2. Ejecutar Fase 1 de pruebas (verificación básica)
3. Si funciona: Modificar `config/settings.py` para agregar opción Ollama
4. Si falla: Pasar a Opción B

### Opción B: Probar Qwen2.5 (ALTERNATIVA) ❓

**Cuándo:**

- Mistral no cumple calidad esperada
- Necesitas mejor contexto/JSON handling

**Pasos:**

1. `ollama pull qwen2.5:8b`
2. Ejecutar misma Fase 1
3. Si no hay tool_calls: Investigar implementación custom

### Opción C: Mantener GitHub Models (FALLBACK) ⚠️

**Cuándo:**

- Ningún modelo local funciona con tool calling
- Calidad es crítica (gpt-4o superior)
- Rate limit manejable (50 req/day suficiente)

**Mejoras:**

- Implementar cache de respuestas
- Agregar delay entre requests
- Usar solo para pruebas finales

### Opción D: Modelo Más Grande (ÚLTIMA OPCIÓN) 🔧

**Si PC lo permite:**

- `qwen2.5:14b` (9.0GB) - Mejor capacidad, verificar tool support
- `mistral:7b-instruct-v0.3` - Versión instruct específica

---

## 🚀 PRÓXIMOS PASOS INMEDIATOS

1. **[5 min]** Instalar Mistral:

   ```bash
   ollama pull mistral:7b
   ollama run mistral:7b  # Verificar descarga
   ```

2. **[10 min]** Crear script de prueba básico (Fase 1)

3. **[15 min]** Ejecutar y documentar resultados

4. **[Decisión]**
   - ✅ Si funciona → Proceder Fase 2 (integración real)
   - ❌ Si falla → Probar Qwen2.5 o reportar hallazgos

---

## 📚 REFERENCIAS

### Documentación Verificada

1. **Mistral Tool Calling:** https://ollama.com/library/mistral
   - Sección "Function calling with Mistral 0.3"
2. **LangChain + Ollama:** https://python.langchain.com/docs/integrations/chat/ollama
   - Sección "Tool calling"
3. **Qwen3 Tool Use:** https://github.com/QwenLM/Qwen3

   - Sección "Build with Qwen3 > Tool Use"

4. **Ollama Tool Support:** https://ollama.com/search?&c=tools
   - Lista de modelos con tag "tools"

### Modelos con Tool Support Confirmado (Ollama)

- ✅ mistral (v0.3+)
- ✅ gpt-oss:20b (mencionado en docs LangChain)
- ❓ qwen2.5 (tag presente, sin confirmar)
- ❓ llama3.1 (mencionado en algunos contextos)

---

## ⚠️ ADVERTENCIAS

1. **Tool Calling != Code Generation**

   - Modelos de código (DeepSeek, CodeGemma) NO son para tool calling
   - Son para completion/generation, no function orchestration

2. **Contexto es Crítico**

   - 15 papers + system prompts ≈ 20-25K tokens
   - Modelos con <32K no son viables
   - Mistral 32K es justo el mínimo

3. **Quality vs Speed Tradeoff**

   - gpt-4o (GitHub Models) probablemente tiene mejor calidad
   - Mistral 7B será más rápido pero posiblemente menos preciso
   - Evaluar si tradeoff es aceptable para tu caso de uso

4. **Hardware Requirements**
   - Mistral 7B (4.4GB) requiere ~8GB RAM
   - GPU recomendada para velocidad decente
   - Sin GPU: expect respuestas lentas (30-60s por request)

---

**Última actualización:** 2025-01-XX
**Estado:** Investigación completada, pendiente pruebas prácticas
**Decisión recomendada:** Probar Mistral 7B v0.3 inmediatamente
