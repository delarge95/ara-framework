# APIs Disponibles por Agente/Nodo

## 📋 Resumen Ejecutivo

El ARA Framework actual soporta múltiples APIs para cada agente. Este documento detalla todas las opciones disponibles, incluyendo APIs remotas, locales y de terceros como GitHub Copilot, Cursor, Perplexity, etc.

---

## 🤖 Agente 1: Niche Analyst (Analista de Nicho)

### **APIs Actuales (Implementadas)**
1. **GROQ** (LLM Principal)
   - Modelo: `mixtral-8x7b-32768` o `llama-3.1-8b-instant`
   - Uso: Análisis de mercado y tendencias
   - Costo: Gratis (límite: 14,400 req/día)
   - Latencia: ~1-2 segundos

2. **Semantic Scholar** (Búsqueda de Papers)
   - Endpoint: `https://api.semanticscholar.org/graph/v1`
   - Uso: Buscar papers académicos, tendencias de investigación
   - Autenticación: API Key (gratuita)
   - Rate limit: 1 req/seg

3. **Playwright** (Web Scraping)
   - Navegadores soportados: Chromium, Firefox, WebKit
   - Uso: Extraer información de GitHub, Reddit, HackerNews
   - Característica: Headless, stealth mode, anti-detection

### **APIs Alternativas Sugeridas**
| API | Tipo | Ventajas | Desventajas | Costo |
|-----|------|----------|-------------|--------|
| **OpenAI GPT-4** | LLM | Mejor calidad, más grande | Rate limit bajo | $0.03/1K tokens |
| **Anthropic Claude** | LLM | Excelente para análisis | API restrictiva | $0.003/1K tokens |
| **Azure OpenAI** | LLM (Empresa) | Mejor control, compliance | Setup complejo | Variable |
| **Llama 2 (Meta)** | LLM Local | Privacidad, sin límites | Requiere GPU local | Gratis |
| **Google Scholar API** | Search | Mejor cobertura académica | API cerrada (webscraping) | Gratis/Limitado |
| **arXiv API** | Search | Papers open-source | Menos papers industriales | Gratis |
| **Brave Search API** | Search | Mejor que Google | Costo moderado | $1-2/mes |

### **Código de Ejemplo - Alternativa GPT-4**
```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4-turbo",
    temperature=0.1,
    api_key=os.getenv("OPENAI_API_KEY")
)
```

---

## 📚 Agente 2: Literature Researcher (Investigador de Literatura)

### **APIs Actuales (Implementadas)**
1. **GROQ** (LLM Principal)
   - Uso: Sintetizar información de múltiples papers
   - Rol: Seleccionar y resumir literatura relevante

2. **Semantic Scholar** (Búsqueda Avanzada)
   - Uso: Buscar papers por fecha, citaciones, autores
   - Característica: Acceso a metadatos completos

3. **Playwright** (PDF Extraction)
   - Uso: Descargar y procesar PDFs de papers
   - Limitación: Algunos PDFs están protegidos

### **APIs Alternativas Sugeridas**
| API | Tipo | Ventajas | Desventajas | Costo |
|-----|------|----------|-------------|--------|
| **CrossRef API** | Metadata | Información completa de papers | Requiere parsing | Gratis |
| **OpenAlex** | Academic Data | Mejor que Semantic Scholar | Menos papers recientes | Gratis |
| **Unpaywall** | PDF Access | Acceso a papers open-access | No todos los papers | Gratis |
| **PDF.js (local)** | PDF Processing | Rápido, sin dependencias | Solo JavaScript | Gratis |
| **PyMuPDF (local)** | PDF Processing | Buena calidad, rápido | Dependencia nativa | Gratis |
| **PubMed API** | Medical Papers | Especializado en medicina | Scope limitado | Gratis |
| **IEEE Xplore API** | Technical Papers | Especializado en ingeniería | Acceso limitado | Pago |

### **Código de Ejemplo - PDF Extraction Local**
```python
import fitz  # PyMuPDF

doc = fitz.open("paper.pdf")
text = ""
for page in doc:
    text += page.get_text()
```

---

## 🏗️ Agente 3: Technical Architect (Arquitecto Técnico)

### **APIs Actuales (Implementadas)**
1. **GROQ** (LLM Principal)
   - Uso: Diseñar arquitectura técnica
   - Rol: Crear diagramas y especificaciones

2. **Playwright** (Scraping de Documentación)
   - Uso: Extraer documentación técnica
   - Fuentes: GitHub, Rust docs, WebAssembly specs

### **APIs Alternativas Sugeridas**
| API | Tipo | Ventajas | Desventajas | Costo |
|-----|------|----------|-------------|--------|
| **GitHub API** | Code Search | Análisis de repos, trending | Rate limit bajo (60 req/h) | Gratis |
| **GitLab API** | Code Search | Similar a GitHub | Alternativa | Gratis |
| **Stack Exchange API** | Q&A | Stack Overflow data | Limitado | Gratis |
| **DevDocs API** | Documentation | 500+ técnicas documentadas | Read-only | Gratis |
| **AsyncIO (local)** | Parallelism | Ejecutar tareas en paralelo | Solo Python | Gratis |
| **Graphviz (local)** | Diagrams | Generar diagramas | Requiere instalación | Gratis |

### **Código de Ejemplo - GitHub API**
```python
from github import Github

g = Github(os.getenv("GITHUB_TOKEN"))
repos = g.search_repositories(query="rust webassembly audio", sort="stars")

for repo in repos[:5]:
    print(f"{repo.name}: {repo.stargazers_count} stars")
```

---

## 💻 Agente 4: Implementation Specialist (Especialista de Implementación)

### **APIs Actuales (Implementadas)**
1. **GROQ** (LLM Principal)
   - Uso: Crear roadmap y user stories
   - Rol: Descomponer tareas complejas

2. **Playwright** (Scraping)
   - Uso: Buscar ejemplos de implementación

### **APIs Alternativas Sugeridas**
| API | Tipo | Ventajas | Desventajas | Costo |
|-----|------|----------|-------------|--------|
| **Jira API** | Project Management | Crear issues automáticamente | Requiere Jira Cloud | Pago |
| **GitHub Projects API** | Project Management | Integración nativa | Más simple que Jira | Gratis |
| **Linear API** | Project Management | Moderno, rápido | Relativamente nuevo | Pago |
| **Notion API** | Documentation | Crear documentos | Lento | Gratis |
| **Markdown (local)** | Docs | Rápido, versionable | No interactivo | Gratis |

### **Código de Ejemplo - GitHub Projects API**
```python
import requests

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# Crear issue
issue_data = {
    "title": "Phase 1: Setup",
    "body": "Setup development environment",
    "labels": ["phase-1", "setup"]
}

r = requests.post(
    f"https://api.github.com/repos/{owner}/{repo}/issues",
    json=issue_data,
    headers=headers
)
```

---

## 📝 Agente 5: Content Synthesizer (Sintetizador de Contenido)

### **APIs Actuales (Implementadas)**
1. **GROQ** (LLM Principal)
   - Uso: Generar reporte final
   - Rol: Integrar todo en un documento coherente

2. **Supabase** (Database)
   - Uso: Guardar análisis completado
   - Característica: PostgreSQL con autenticación

### **APIs Alternativas Sugeridas**
| API | Tipo | Ventajas | Desventajas | Costo |
|-----|------|----------|-------------|--------|
| **Markdown (local)** | Output | Rápido, versionable | No interactivo | Gratis |
| **HTML Generator (local)** | Output | Mejor visualización | Requiere CSS | Gratis |
| **Pandoc (local)** | Conversion | Convertir a PDF, DOCX | Dependencia externa | Gratis |
| **WeasyPrint (local)** | PDF | Generar PDF desde HTML | Requiere instalación | Gratis |
| **Google Docs API** | Cloud Storage | Colaboración en tiempo real | Setup complejo | Gratis |
| **Notion API** | Cloud Storage | Crear página con contenido | Lento | Gratis |
| **Typeform API** | Forms | Obtener retroalimentación | Scope limitado | Pago |

### **Código de Ejemplo - PDF Generation Local**
```python
from weasyprint import HTML, CSS

html_content = """
<html>
    <body>
        <h1>Research Report: Rust WebAssembly</h1>
        <p>Content here...</p>
    </body>
</html>
"""

HTML(string=html_content).write_pdf("report.pdf")
```

---

## 🔌 APIs de Terceros (GitHub Copilot, Cursor, Perplexity, etc.)

### 1. **GitHub Copilot** ⭐
**Tipo:** LLM (Codex-based)
**Integración:** IDE plugin (VS Code, JetBrains, etc.)
**Usos en ARA:**
- Generar boilerplate code para funciones
- Revisar código de agentes
- Sugerir mejoras de arquitectura

**Limitación:** No es una API HTTP, solo IDE plugin
**Alternativa:** Usar `copilot-cli` o GitHub Copilot API (beta)

```bash
# Instalar copilot CLI
npm install -g @github/copilot-cli

# Usar en terminal
copilot "<prompt>"
```

### 2. **Cursor Editor** 🎯
**Tipo:** IDE + LLM integrado
**Modelos soportados:** GPT-4, Claude
**Usos en ARA:**
- Escribir tests automáticamente
- Refactorizar código
- Generar documentación

**Limitación:** Es un editor, no una API
**Para ARA:** Podría usarse para desarrollo, no para ejecución

### 3. **Perplexity API** 🔍
**Tipo:** LLM + Search Engine
**Endpoint:** `https://api.perplexity.ai/chat/completions`
**Usos en ARA:**
- Buscar información actualizada
- Combinar LLM + Web Search

```python
import requests

headers = {
    "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": "pplx-7b-online",  # Online model con web search
    "messages": [
        {
            "role": "user",
            "content": "What are the latest trends in Rust WebAssembly?"
        }
    ]
}

response = requests.post(
    "https://api.perplexity.ai/chat/completions",
    json=payload,
    headers=headers
)
```

**Costo:** $0.005/1K tokens (entrada), $0.02/1K tokens (salida)

### 4. **Ollama (Local LLM)** 🏠
**Tipo:** Local LLM Server
**Modelos:** Llama 2, Mistral, Neural Chat, etc.
**Usos en ARA:**
- Privacidad total (datos locales)
- Sin rate limits
- Sin costos de API

```python
import requests

# Ollama escucha en localhost:11434
response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "mistral",
        "prompt": "Analyze this niche: Rust WebAssembly",
        "stream": False
    }
)

print(response.json()['response'])
```

**Ventajas:** 
- Completamente privado
- Sin límites de rate
- Funcionamiento offline

**Desventajas:**
- Requiere GPU local
- Modelos menos potentes que GPT-4

### 5. **LM Studio (Local, GUI)** 🖥️
**Tipo:** Local LLM con interfaz
**Similar a:** Ollama pero con GUI
**Modelos:** Llama 2, Mistral, etc.

### 6. **Claude API (Anthropic)** 🧠
**Tipo:** LLM de alta calidad
**Endpoint:** `https://api.anthropic.com/v1/messages`
**Usos en ARA:**
- Análisis profundo de literatura
- Síntesis de contenido complejo

```python
from anthropic import Anthropic

client = Anthropic()

message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Analyze this niche..."
        }
    ]
)
```

**Ventajas:**
- Superior en análisis de contexto
- Mejor para literatura académica
- Token limit muy alto (200K)

**Costo:** $0.015/1K tokens (entrada), $0.075/1K tokens (salida)

### 7. **LangSmith (Observabilidad)** 📊
**Tipo:** Monitoring y debugging para LangChain
**Usos en ARA:**
- Rastrear ejecución de agentes
- Debugging de tool calls
- Análisis de costos

```python
import os
from langsmith import Client

# Set API key
os.environ["LANGCHAIN_API_KEY"] = "..."
os.environ["LANGCHAIN_PROJECT"] = "ara-framework"

# LangChain automaticamente registrará todas las llamadas
```

---

## 📊 Matriz de Comparación: APIs para LLM

| API | Costo | Velocidad | Calidad | Tool Call | Rate Limit | Mejor Para |
|-----|-------|-----------|---------|-----------|-----------|-----------|
| **GROQ (Mixtral)** | 🟢 Gratis | ⚡ Rápido | 🟡 Bueno | ✅ Excelente | 14.4K/día | Prototipo rápido |
| **OpenAI GPT-4** | 🔴 $$$$ | 🟡 Medio | 🟢 Excelente | ✅ Perfecto | 40K/min | Producción |
| **Claude 3** | 🟡 $$ | 🟡 Medio | 🟢 Excelente | ✅ Bueno | 50K/min | Literatura, análisis |
| **Perplexity** | 🟡 $ | ⚡ Rápido | 🟡 Bueno | ⚠️ Limitado | 100/min | Web search integrado |
| **Llama Local** | 🟢 Gratis | 🟡 Variable | 🟡 Bueno | ⚠️ Limitado | ♾️ Ilimitado | Privacidad total |
| **Ollama** | 🟢 Gratis | 🟡 Variable | 🟡 Bueno | ⚠️ Limitado | ♾️ Ilimitado | Testing local |

---

## 🔧 Implementación Recomendada por Escenario

### **Escenario 1: Desarrollo Local (Tu PC)**
```python
# .env
LLM_PROVIDER=ollama
OLLAMA_MODEL=mistral
SEMANTIC_SCHOLAR_API_KEY=...
# Sin costos, datos privados
```

### **Escenario 2: Producción (Máxima Calidad)**
```python
# .env
LLM_PROVIDER=openai
OPENAI_MODEL=gpt-4-turbo
SEARCH_PROVIDER=perplexity  # Para datos recientes
# Costo: $20-100/mes
```

### **Escenario 3: Análisis Académico Especializado**
```python
# .env
LLM_PROVIDER=anthropic
ANTHROPIC_MODEL=claude-3-opus
SEARCH_PROVIDER=semantic_scholar
PDF_PROCESSOR=pymupdf  # Local
# Costo: $10-30/mes
```

### **Escenario 4: Máxima Velocidad (Startup)**
```python
# .env
LLM_PROVIDER=groq
GROQ_MODEL=mixtral-8x7b-32768
SEARCH_PROVIDER=semantic_scholar
# Costo: Gratis (con límites)
```

---

## 🚀 Próximos Pasos Recomendados

1. **Integrar múltiples LLMs** - Permitir switching entre GROQ, OpenAI, Claude
2. **Agregar Perplexity** - Para búsqueda web en tiempo real
3. **Soportar Ollama local** - Opción privada para desarrollo
4. **LangSmith integration** - Monitoreo de la pipeline
5. **Fallback strategy** - Si GROQ falla, usar OpenAI

---

## 📝 Notas

- **API Keys:** Nunca pushear a GitHub, usar `.env`
- **Rate Limits:** Implementar retry logic con exponential backoff
- **Caching:** Redis para resultados recientes (ya implementado)
- **Monitoring:** LangSmith para debugging
- **Cost Control:** Establecer budget limits en APIs de pago

