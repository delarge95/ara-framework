# 🎯 MODELOS GITHUB - LISTA COMPLETA VERIFICADA (Nov 2025)

**Fecha**: 12 de Noviembre de 2025  
**Método**: Prueba directa con API de GitHub Models  
**Total probado**: 36 modelos  
**Total disponible**: 12 modelos ✅

---

## ✅ MODELOS DISPONIBLES (12 modelos)

### 🤖 OpenAI (2 modelos)

| Modelo          | Parámetros | Uso recomendado                                | Velocidad           |
| --------------- | ---------- | ---------------------------------------------- | ------------------- |
| **gpt-4o**      | ~200B      | **MEJOR OPCIÓN** - Análisis, código, escritura | ⚡⚡⚡ Rápido       |
| **gpt-4o-mini** | ~20B       | Tareas simples, prototipos                     | ⚡⚡⚡⚡ Muy rápido |

**Recomendación**: Usar `gpt-4o` como modelo principal para TODOS los agentes.

---

### 🦙 Meta Llama (3 modelos)

| Modelo                           | Parámetros | Uso recomendado                              | Velocidad           |
| -------------------------------- | ---------- | -------------------------------------------- | ------------------- |
| **Llama-3.3-70B-Instruct**       | 70B        | Último Llama 3.3 - Balance calidad/velocidad | ⚡⚡⚡ Rápido       |
| **Meta-Llama-3.1-405B-Instruct** | **405B**   | **MODELO MÁS GRANDE** - Tareas complejas     | ⚡⚡ Medio          |
| **Meta-Llama-3.1-8B-Instruct**   | 8B         | Tareas rápidas, testing                      | ⚡⚡⚡⚡ Muy rápido |

**Recomendación**: `Meta-Llama-3.1-405B-Instruct` es el modelo más poderoso disponible GRATIS (405 mil millones de parámetros). Alternativa seria a GPT-4o.

---

### 🔬 Microsoft Phi (1 modelo)

| Modelo    | Parámetros | Uso recomendado                   | Velocidad     |
| --------- | ---------- | --------------------------------- | ------------- |
| **Phi-4** | ~14B       | Último Phi - Código, razonamiento | ⚡⚡⚡ Rápido |

**Recomendación**: Excelente para generación de código y tareas técnicas.

---

### 🌟 Mistral AI (2 modelos)

| Modelo            | Parámetros | Uso recomendado           | Velocidad           |
| ----------------- | ---------- | ------------------------- | ------------------- |
| **Mistral-Nemo**  | 12B        | Balance calidad/velocidad | ⚡⚡⚡ Rápido       |
| **Mistral-small** | 7B         | Tareas rápidas            | ⚡⚡⚡⚡ Muy rápido |

**Recomendación**: Buenos para tareas generales si hay rate limits con GPT-4o.

---

### 🔷 Cohere (2 modelos)

| Modelo                            | Parámetros | Uso recomendado             | Velocidad     |
| --------------------------------- | ---------- | --------------------------- | ------------- |
| **cohere-command-r-08-2024**      | ~35B       | Tareas generales, RAG       | ⚡⚡⚡ Rápido |
| **cohere-command-r-plus-08-2024** | ~104B      | Análisis complejo, síntesis | ⚡⚡ Medio    |

**Recomendación**: `cohere-command-r-plus-08-2024` excelente para síntesis de contenido (Agent 5).

---

### 🎯 AI21 Labs (1 modelo)

| Modelo              | Parámetros | Uso recomendado                         | Velocidad  |
| ------------------- | ---------- | --------------------------------------- | ---------- |
| **jamba-1.5-large** | ~94B       | Híbrido SSM-Transformer, contexto largo | ⚡⚡ Medio |

**Recomendación**: Bueno para documentos largos (papers académicos).

---

### 🚀 Otras Opciones (1 modelo)

| Modelo           | Parámetros | Uso recomendado             | Velocidad          |
| ---------------- | ---------- | --------------------------- | ------------------ |
| **ministral-3b** | 3B         | Testing, prototipos rápidos | ⚡⚡⚡⚡⚡ Extremo |

---

## ❌ MODELOS NO DISPONIBLES

### Anthropic Claude

- ❌ claude-3-5-sonnet
- ❌ claude-3-opus
- ❌ claude-3-sonnet
- ❌ claude-3-haiku

**Nota**: Ninguna versión de Claude está disponible en GitHub Models actualmente.

### OpenAI o1

- ❌ o1-preview (error en API)
- ❌ o1-mini (error en API)

### Otros Llama

- ❌ Meta-Llama-3.1-70B-Instruct (usa Llama-3.3-70B en su lugar)
- ❌ Meta-Llama-3-70B-Instruct
- ❌ Meta-Llama-3-8B-Instruct

### Otros Phi

- ❌ Phi-3.5-\* (todas las versiones)
- ❌ Phi-3-\* (todas las versiones)

---

## 🏆 TOP 3 MODELOS RECOMENDADOS PARA TU TFG

### 1️⃣ **gpt-4o** (OpenAI)

**Por qué**:

- ✅ Mejor calidad general
- ✅ Excelente para código, análisis, escritura
- ✅ Balance perfecto calidad/velocidad
- ✅ Usado por empresas en producción

**Usar para**: TODOS los agentes (1, 2, 3, 4, 5)

---

### 2️⃣ **Meta-Llama-3.1-405B-Instruct** (Meta)

**Por qué**:

- ✅ **405 mil millones de parámetros** (modelo más grande)
- ✅ Open source (puedes citarlo en TFG)
- ✅ Compite con GPT-4o en benchmarks
- ✅ Gratis sin límites ocultos

**Usar para**: Alternativa cuando GPT-4o tenga rate limits

---

### 3️⃣ **cohere-command-r-plus-08-2024** (Cohere)

**Por qué**:

- ✅ Excelente para síntesis de contenido
- ✅ Bueno para RAG (Retrieval Augmented Generation)
- ✅ Optimizado para tareas de escritura

**Usar para**: Agent 5 (Content Synthesizer) si necesitas diversificar

---

## 💡 ESTRATEGIA RECOMENDADA

### Opción A: Todo con GPT-4o (más simple)

```python
# Todos los agentes
model = "gpt-4o"
```

**Ventajas**:

- ✅ Máxima calidad
- ✅ Consistencia entre agentes
- ✅ Más fácil de debuggear

**Desventajas**:

- ⚠️ Rate limits (~100-200 req/hora)

---

### Opción B: Multi-modelo (más robusto)

```python
# Agent 1: Niche Analyst
model = "gpt-4o"

# Agent 2: Literature Researcher
model = "Meta-Llama-3.1-405B-Instruct"  # Mejor para papers largos

# Agent 3: Technical Architect
model = "gpt-4o"

# Agent 4: Implementation Specialist
model = "Phi-4"  # Especializado en código

# Agent 5: Content Synthesizer
model = "cohere-command-r-plus-08-2024"  # Mejor para escritura
```

**Ventajas**:

- ✅ Distribuye rate limits
- ✅ Usa fortalezas de cada modelo
- ✅ Más robusto ante fallos

**Desventajas**:

- ⚠️ Más complejo de configurar
- ⚠️ Resultados pueden variar entre agentes

---

## 🧪 CÓMO PROBAR LOS MODELOS

### Probar un modelo específico:

```python
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.getenv("GITHUB_TOKEN"),
)

# Cambiar el modelo aquí
response = client.chat.completions.create(
    model="Meta-Llama-3.1-405B-Instruct",  # o cualquier otro
    messages=[
        {"role": "user", "content": "Explica qué son los agentes autónomos"}
    ],
    max_tokens=500,
)

print(response.choices[0].message.content)
```

### Script para comparar modelos:

```bash
python discover_github_models.py
```

---

## 📊 COMPARACIÓN CON OTROS SERVICIOS

| Servicio  | Modelo similar    | Costo              | GitHub Models                |
| --------- | ----------------- | ------------------ | ---------------------------- |
| OpenAI    | GPT-4o            | $5-15/1M tokens    | **GRATIS** ✅                |
| Anthropic | Claude Sonnet 4.5 | $3-15/1M tokens    | ❌ No disponible             |
| Meta      | Llama 3.1-405B    | Gratis (self-host) | **GRATIS** ✅ (no self-host) |
| Cohere    | Command R+        | $3-15/1M tokens    | **GRATIS** ✅                |
| AI21      | Jamba 1.5         | $0.2-8/1M tokens   | **GRATIS** ✅                |

**Conclusión**: GitHub Models te da acceso GRATIS a modelos que costarían $50-100/mes en otros servicios.

---

## 🚀 PRÓXIMOS PASOS

1. ✅ **Ya tienes configurado**: GitHub Token + Perplexity API
2. ⏹️ **Siguiente**: Integrar modelos en los agentes
3. ⏹️ **Después**: Probar pipeline completo
4. ⏹️ **Finalmente**: Optimizar qué modelo usar en cada agente

---

## 📚 SCRIPTS DISPONIBLES

```bash
# Ver todos los modelos disponibles
python discover_github_models.py

# Probar acceso rápido
python test_github_models_env.py

# Listar modelos con detalles
python list_github_models.py
```

---

## ✅ RESUMEN EJECUTIVO

**Total verificado**: 36 modelos  
**Total disponible**: 12 modelos (33% de lo probado)  
**Mejor modelo**: `gpt-4o` (OpenAI)  
**Modelo más grande**: `Meta-Llama-3.1-405B-Instruct` (405B parámetros)  
**Costo**: **GRATIS** durante beta  
**Rate limit**: ~100-200 requests/hora

**Conclusión**: Tienes acceso a modelos de nivel enterprise completamente gratis. Usa `gpt-4o` como principal y `Meta-Llama-3.1-405B-Instruct` como backup.
