# 🔑 Guía de API Keys - ARA Framework

Esta guía te ayudará a obtener todas las API keys necesarias para usar el ARA Framework con diferentes proveedores de IA.

---

## 📋 Índice

1. [Perplexity AI](#perplexity-ai) ⭐ **Real-time web search**
2. [GitHub Models](#github-models) ⭐ **GRATIS: GPT-4o, Claude 3.5**
3. [Groq](#groq) - **Ya configurado ✅**
4. [GitHub Copilot Pro](#github-copilot-pro) - **Alternativas**
5. [Resumen de Costos](#resumen-de-costos)

---

## 1. Perplexity AI

**¿Para qué sirve?**

- Búsqueda web en tiempo real + análisis LLM
- Ideal para Agent 1 (Niche Analyst) - tendencias actuales
- Reemplaza scraping tradicional con resultados más inteligentes

**¿Cómo obtener API Key?**

### Paso 1: Crear cuenta

1. Ir a: https://www.perplexity.ai/
2. Click en "Sign Up"
3. Registrarse con email o GitHub

### Paso 2: Obtener API Key

1. Ir a: https://www.perplexity.ai/settings/api
2. Click en "Generate API Key"
3. Copiar la key (formato: `pplx-xxxxx`)

### Paso 3: Configurar en ARA

```bash
# En tu archivo .env:
PERPLEXITY_API_KEY=pplx-tu-key-aqui
PERPLEXITY_MODEL=llama-3.1-sonar-large-128k-online
```

**Modelos disponibles:**

- `llama-3.1-sonar-small-128k-online`: Rápido, más barato (~$1/1M tokens)
- `llama-3.1-sonar-large-128k-online`: Mejor calidad (~$5/1M tokens) ⭐
- `llama-3.1-sonar-huge-128k-online`: Máxima calidad, más lento (~$10/1M tokens)

**Precios (Nov 2025):**

- Input: $1-5 / 1M tokens (según modelo)
- Output: $1-5 / 1M tokens
- **Créditos iniciales**: $5 gratis para probar

**Test:**

```bash
cd ara_framework
python test_perplexity.py
```

---

## 2. GitHub Models

**¿Para qué sirve?**

- Acceso **GRATIS** (durante beta) a modelos premium:
  - GPT-4o (OpenAI)
  - Claude 3.5 Sonnet (Anthropic) ⭐
  - Llama 3.1 405B (Meta)
  - Phi-3 (Microsoft)
  - Mistral Large
- **NO requiere** GitHub Copilot Pro
- **NO requiere** suscripción

**¿Cómo obtener acceso?**

### Paso 1: Personal Access Token

1. Ir a: https://github.com/settings/tokens
2. Click en "Generate new token" → "Generate new token (classic)"
3. **Scopes necesarios**:
   - ✅ `read:packages` (CRÍTICO)
   - ✅ `repo` (opcional, si quieres usar GitHub MCP)
4. Click en "Generate token"
5. **COPIAR EL TOKEN** (solo se muestra una vez)

### Paso 2: Probar acceso

1. Ir a: https://github.com/marketplace/models
2. Si ves los modelos, tienes acceso ✅
3. Click en cualquier modelo para ver ejemplos de uso

### Paso 3: Configurar en ARA

```bash
# En tu archivo .env:
GITHUB_TOKEN=ghp_tu_token_aqui
GITHUB_MODEL=gpt-4o  # o claude-3.5-sonnet
```

**Modelos recomendados:**

| Modelo              | Mejor para              | Velocidad | Calidad    |
| ------------------- | ----------------------- | --------- | ---------- |
| `gpt-4o`            | Arquitectura técnica    | ⚡⚡      | ⭐⭐⭐⭐⭐ |
| `claude-3.5-sonnet` | Análisis de literatura  | ⚡⚡      | ⭐⭐⭐⭐⭐ |
| `llama-3.1-405b`    | Alternativa open source | ⚡        | ⭐⭐⭐⭐   |
| `gpt-4o-mini`       | Tareas rápidas          | ⚡⚡⚡    | ⭐⭐⭐     |

**Integración en código:**

```python
from langchain_openai import ChatOpenAI
from config.settings import settings

# Usar GitHub Models
llm = ChatOpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=settings.GITHUB_TOKEN,
    model="gpt-4o",  # o "claude-3.5-sonnet"
    temperature=0.7,
)
```

**Límites (Beta):**

- **Rate limit**: Generoso (no publicado oficialmente)
- **Costo**: **GRATIS** durante beta
- **Duración beta**: Indefinida (por ahora)

---

## 3. Groq

**¿Para qué sirve?**

- LLMs ultra-rápidos (LLaMA 3.3-70B)
- **GRATIS**: 14,400 requests/día
- Ya lo estás usando ✅

**Status actual:**

```bash
✅ GROQ_API_KEY configurado
✅ Modelo: llama-3.1-8b-instant
✅ Funcionando en los 5 agentes
```

**Para optimizar:**

```bash
# Cambiar a modelo más potente (si no tienes rate limits):
GROQ_MODEL=llama-3.3-70b-versatile
```

---

## 4. GitHub Copilot Pro

### ❌ **Respuesta: NO tiene API pública**

GitHub Copilot Pro **no ofrece API** para uso programático directo. Sin embargo:

### ✅ **Alternativa 1: GitHub Models (Recomendado)**

- **Gratis** durante beta
- Acceso a **GPT-4o** y **Claude 3.5 Sonnet**
- No requiere Copilot Pro
- Ver [Sección 2](#github-models) arriba

### ✅ **Alternativa 2: Azure OpenAI**

Si tienes **Copilot Pro**, probablemente tengas acceso a Azure:

```bash
# 1. Ir a: https://portal.azure.com/
# 2. Buscar "Azure OpenAI"
# 3. Crear recurso si tienes acceso
# 4. Obtener endpoint y key

AZURE_OPENAI_ENDPOINT=https://tu-instancia.openai.azure.com/
AZURE_OPENAI_KEY=tu_key_aqui
AZURE_OPENAI_DEPLOYMENT=gpt-4o
```

**Integración:**

```python
from langchain_openai import AzureChatOpenAI

llm = AzureChatOpenAI(
    azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
    api_key=settings.AZURE_OPENAI_KEY,
    deployment_name="gpt-4o",
    api_version="2024-08-01-preview",
)
```

### ✅ **Alternativa 3: Comprar APIs directamente**

| Proveedor | Modelo            | Precio Input | Precio Output |
| --------- | ----------------- | ------------ | ------------- |
| OpenAI    | GPT-4o            | $2.50/1M     | $10/1M        |
| Anthropic | Claude 3.5 Sonnet | $3/1M        | $15/1M        |
| DeepSeek  | DeepSeek V3       | $0.27/1M     | $1.10/1M ⭐   |

---

## 5. Resumen de Costos

### 🆓 **Opciones GRATIS:**

| Servicio          | Límite         | Calidad    | Recomendado para          |
| ----------------- | -------------- | ---------- | ------------------------- |
| **Groq**          | 14,400 req/día | ⭐⭐⭐⭐   | Desarrollo, testing       |
| **GitHub Models** | Beta gratis    | ⭐⭐⭐⭐⭐ | Producción, GPT-4o/Claude |
| **Gemini**        | 1,500 req/día  | ⭐⭐⭐⭐   | Alternativa sólida        |

### 💰 **Opciones de PAGO:**

| Servicio       | Costo/Mes | Mejor para                |
| -------------- | --------- | ------------------------- |
| **Perplexity** | ~$5-20    | Web search en tiempo real |
| **DeepSeek**   | ~$10-50   | Mejor precio/calidad      |
| **Claude**     | ~$20-100  | Análisis profundo         |
| **GPT-4o**     | ~$50-200  | Arquitectura técnica      |

---

## 🚀 Setup Recomendado para ARA

### **Configuración Óptima (Gratis + Perplexity)**

```bash
# .env
# ===== GRATIS =====
GROQ_API_KEY=tu_groq_key  # Para Agents 1, 4, 5 (rápidos)
GITHUB_TOKEN=tu_github_token  # Para Agents 2, 3 (calidad)

# ===== PAGO (Opcional) =====
PERPLEXITY_API_KEY=tu_perplexity_key  # Para Agent 1 (web search)
```

**Asignación por Agente:**

| Agente            | Proveedor     | Modelo            | Justificación             |
| ----------------- | ------------- | ----------------- | ------------------------- |
| 1. Niche Analyst  | Perplexity    | sonar-large       | Web search en tiempo real |
| 2. Literature     | GitHub Models | claude-3.5-sonnet | Mejor análisis de papers  |
| 3. Architecture   | GitHub Models | gpt-4o            | Mejor diseño técnico      |
| 4. Implementation | Groq          | llama-3.1-8b      | Suficiente, rápido        |
| 5. Synthesis      | GitHub Models | gpt-4o            | Mejor escritura           |

**Costo estimado:** $5-10/mes (solo Perplexity)

---

## 📝 Próximos Pasos

1. **Obtener Perplexity API Key** (5 min)
   - https://www.perplexity.ai/settings/api
2. **Obtener GitHub Token** (2 min)

   - https://github.com/settings/tokens
   - Scope: `read:packages`

3. **Configurar `.env`** (1 min)

   ```bash
   cp .env.example .env
   # Editar con tus keys
   ```

4. **Probar Perplexity** (2 min)

   ```bash
   python test_perplexity.py
   ```

5. **Integrar en Agent 1** (10 min)
   - Agregar `perplexity_search` a herramientas del Niche Analyst

---

## 🆘 Troubleshooting

### Error: "API key not found"

```bash
# Verificar que .env existe y tiene la key
cat .env | grep PERPLEXITY_API_KEY
```

### Error: "Rate limit exceeded"

```bash
# Cambiar a modelo más pequeño
PERPLEXITY_MODEL=llama-3.1-sonar-small-128k-online
```

### GitHub Models: "Unauthorized"

```bash
# Verificar que el token tiene scope "read:packages"
# Regenerar token si es necesario
```

---

## 📚 Referencias

- Perplexity Docs: https://docs.perplexity.ai/
- GitHub Models: https://github.com/marketplace/models
- Groq Console: https://console.groq.com/
- LangChain Integration: https://python.langchain.com/docs/integrations/

---

**¿Preguntas?** Consulta `docs/APIS_POR_AGENTE.md` para más detalles sobre cada API.
