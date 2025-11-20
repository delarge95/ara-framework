# ⚠️ LIMITACIÓN CRÍTICA: TOOL CALLING EN GITHUB MODELS

**Fecha**: 12 de Noviembre de 2025  
**Descubrimiento**: Pruebas exhaustivas de tool calling support  
**Impacto**: Cambia completamente la estrategia multi-modelo

---

## 🔍 Descubrimiento

Durante la implementación de la estrategia multi-modelo, descubrimos que **NO todos los modelos de GitHub Models soportan tool calling (function calling)**.

### ✅ Modelos con Tool Calling Support:

| Modelo                            | Params | Tool Calling | Uso Recomendado                  |
| --------------------------------- | ------ | ------------ | -------------------------------- |
| **gpt-4o**                        | ~200B  | ✅ Excelente | Mejor calidad, agentes complejos |
| **gpt-4o-mini**                   | ~20B   | ✅ Excelente | Más rápido, agentes simples      |
| **cohere-command-r-plus-08-2024** | 104B   | ✅ Bueno     | Código y escritura técnica       |

### ❌ Modelos SIN Tool Calling Support:

| Modelo                           | Params | Tool Calling | Problema                                   |
| -------------------------------- | ------ | ------------ | ------------------------------------------ |
| **Meta-Llama-3.1-405B-Instruct** | 405B   | ❌ NO        | No llama herramientas, solo responde texto |
| **Phi-4**                        | 14B    | ❌ Error 400 | Parámetros incompatibles                   |
| **Mistral-small**                | 7B     | ❌ Error 422 | Input inválido                             |

---

## 🧪 Prueba Realizada

```python
# test_tool_calling_support.py
@tool
def get_weather(location: str) -> str:
    """Get weather for a location."""
    return f"Weather in {location}: Sunny, 25°C"

llm_with_tools = llm.bind_tools([get_weather])
response = llm_with_tools.invoke("What's the weather in Paris?")

# Resultados:
# ✅ gpt-4o: tool_calls = [{'name': 'get_weather', ...}]
# ✅ gpt-4o-mini: tool_calls = [{'name': 'get_weather', ...}]
# ✅ cohere-command-r-plus: tool_calls = [{'name': 'get_weather', ...}]
# ❌ Llama-405B: tool_calls = []  # No llamó la herramienta!
```

---

## 💡 Implicaciones para ARA Framework

### Agentes que NECESITAN Tools:

| Agente                       | Tools Requeridos                         | Modelos Viables                |
| ---------------------------- | ---------------------------------------- | ------------------------------ |
| **Agent 1** (Niche Analyst)  | `search_recent_papers`, `scrape_website` | ✅ gpt-4o, gpt-4o-mini, Cohere |
| **Agent 2** (Literature)     | `search_recent_papers`, `extract_pdf`    | ✅ gpt-4o, gpt-4o-mini, Cohere |
| **Agent 3** (Architect)      | Ninguno (solo pensamiento)               | ✅ Cualquier modelo            |
| **Agent 4** (Implementation) | `save_analysis`                          | ✅ gpt-4o, gpt-4o-mini, Cohere |
| **Agent 5** (Synthesizer)    | `save_analysis`                          | ✅ gpt-4o, gpt-4o-mini, Cohere |

### Agentes sin Tools (pueden usar Llama-405B):

Solo **Agent 3 (Technical Architect)** no usa herramientas, por lo que PODRÍA usar Llama-405B para mejor razonamiento arquitectónico.

---

## 🎯 Estrategia Actualizada (v2.1)

### Configuración Final:

| Agente  | Modelo                    | Params   | Razón                                 |
| ------- | ------------------------- | -------- | ------------------------------------- |
| Agent 1 | **gpt-4o-mini**           | 20B      | Tools + rápido, análisis básico       |
| Agent 2 | **gpt-4o-mini**           | 20B      | Tools + paginación para 100 papers    |
| Agent 3 | **Meta-Llama-3.1-405B**   | **405B** | 🔥 Sin tools, mejor razonamiento puro |
| Agent 4 | **cohere-command-r-plus** | 104B     | Tools + especializado en código       |
| Agent 5 | **gpt-4o**                | 200B     | Tools + mejor síntesis final          |

### Comparación con v2.0 (fallida):

| Agente  | v2.0 (Fallido) | v2.1 (Actualizado) | Cambio                        |
| ------- | -------------- | ------------------ | ----------------------------- |
| Agent 1 | Llama-405B ❌  | gpt-4o-mini ✅     | Necesita tools                |
| Agent 2 | Llama-405B ❌  | gpt-4o-mini ✅     | Necesita tools                |
| Agent 3 | gpt-4o         | Llama-405B ✅      | Sin tools, mejor razonamiento |
| Agent 4 | Cohere ✅      | Cohere ✅          | Sin cambio                    |
| Agent 5 | gpt-4o ✅      | gpt-4o ✅          | Sin cambio                    |

---

## 📊 Métricas Esperadas (v2.1)

### Token Limit Management:

| Agente  | Input Esperado                      | Modelo                  | Token Limit      | Solución                          |
| ------- | ----------------------------------- | ----------------------- | ---------------- | --------------------------------- |
| Agent 1 | Papers (16K) + Scraping (12K) = 28K | gpt-4o-mini (8K)        | ⚠️ Puede exceder | Limitar scraping, focus en papers |
| Agent 2 | 100 papers (~171K tokens)           | gpt-4o-mini (8K)        | ⚠️ Excede        | ✅ Paginación 5x20                |
| Agent 3 | Architecture context (3K)           | Llama-405B (sin límite) | ✅ OK            | Sin problema                      |
| Agent 4 | Architecture (3K)                   | Cohere (context limit?) | ✅ OK            | Sin problema                      |
| Agent 5 | All outputs (~15K)                  | gpt-4o (8K)             | ⚠️ Puede exceder | Truncar contextos                 |

### Performance:

- **Agent 1**: gpt-4o-mini → ~20-30s (más rápido que gpt-4o)
- **Agent 2**: gpt-4o-mini + paginación → ~60-90s (5 requests)
- **Agent 3**: Llama-405B → ~40-60s (más lento pero mejor calidad)
- **Agent 4**: Cohere → ~30-40s
- **Agent 5**: gpt-4o → ~20-30s

**Tiempo total estimado**: ~3-4 minutos (vs 5 minutos antes)

---

## ⚠️ Problemas Pendientes

### 1. Token Limit en Agent 1:

- **Problema**: Papers (16K) + Scraping (12K) > 8K limit de gpt-4o-mini
- **Solución Temporal**: Agent 1 debe:
  - ✅ Limitar papers a 10 (limit=10, no 100)
  - ✅ IGNORAR scraping fallido (ya configurado)
  - ✅ Enfocarse solo en academic papers

### 2. Token Limit en Agent 5:

- **Problema**: Recibe outputs de 4 agentes (~15K tokens) > 8K limit
- **Solución**: Truncar contextos en system prompt:
  ```python
  niche_analysis = state.get("niche_analysis", "")[:2000]
  literature = state.get("literature_review", "")[:3000]
  architecture = state.get("technical_architecture", "")[:3000]
  implementation = state.get("implementation_plan", "")[:3000]
  # Total: ~11K chars ≈ 3K tokens (OK)
  ```

### 3. Paginación en Agent 2:

- **Estado**: ✅ Ya implementada
- **Comportamiento**:
  - limit ≤ 50 → 1 request
  - limit > 50 → múltiples requests de 20
  - Max 100 papers (5 páginas)

---

## 🚀 Próximos Pasos

### Implementación:

1. ✅ Agent 1: Cambiar a gpt-4o-mini
2. ✅ Agent 2: Cambiar a gpt-4o-mini (con paginación)
3. ⏳ Agent 3: Cambiar a Llama-405B (sin tools OK)
4. ✅ Agent 4: Mantener Cohere
5. ✅ Agent 5: Mantener gpt-4o

### Testing:

1. ⏳ Probar pipeline completo
2. ⏳ Verificar que Agent 3 (Llama-405B) funciona sin tools
3. ⏳ Monitorear token limits en Agents 1 y 5
4. ⏳ Validar calidad de outputs

### Documentación:

1. ✅ Crear TOOL_CALLING_LIMITACION.md
2. ⏳ Actualizar OPTIMIZACIONES_MODELOS.md
3. ⏳ Actualizar GITHUB_MODELS_COMPLETO.md con tool calling status
4. ⏳ Crear guía de selección de modelos

---

## 📝 Lecciones Aprendidas

### 1. Tool Calling ≠ Disponibilidad del Modelo

- Que un modelo esté en GitHub Models NO significa que soporte tool calling
- Siempre probar tool calling antes de asignar a agentes

### 2. Llama-405B es Excelente... Para Texto

- 405B parámetros = razonamiento excepcional
- Pero sin tool calling, solo sirve para Agent 3 (Architect)

### 3. gpt-4o-mini es Subestimado

- Solo 20B params pero soporta tools
- Mucho más rápido que gpt-4o
- Ideal para agentes simples (Agents 1, 2)

### 4. Cohere es Especialista

- Tool calling funcional
- Excelente para código (Agent 4)
- 104B params, buen balance

---

## ✅ Checklist Actualizado

- [x] Descubrir limitación de tool calling
- [x] Probar 6 modelos diferentes
- [x] Documentar resultados (este archivo)
- [x] Actualizar Agent 1 a gpt-4o-mini
- [x] Actualizar Agent 2 a gpt-4o-mini
- [x] Quitar scrape_website de Agent 4 (Cohere tenía problemas)
- [ ] **Actualizar Agent 3 a Llama-405B** ⏳ SIGUIENTE
- [ ] Probar pipeline completo
- [ ] Validar calidad vs tiempo
- [ ] Actualizar documentación principal

---

**Estado**: DESCUBRIMIENTO CRÍTICO completado, implementación parcial, testing pendiente.

**Próxima acción**: Cambiar Agent 3 a Llama-405B y probar pipeline completo.
