# 🚀 Guía Rápida: Usar Ollama con ARA Framework

## ✅ Configuración Completada

El sistema ya está completamente configurado con **Ollama (Mistral 7B)** como proveedor alternativo a GitHub Models.

### Verificación (ya hecho):

- ✅ Ollama server corriendo en `http://localhost:11434`
- ✅ Modelo Mistral 7B descargado (4.4GB)
- ✅ Paquetes instalados: `langchain-ollama v1.0.0`
- ✅ Tool calling verificado: **4/4 tests pasados (100%)**
- ✅ Integración completa en `research_graph.py`

---

## 🎯 Uso: Cambiar de Proveedor

### Opción 1: Variable de Entorno (Recomendado)

```powershell
# Usar Ollama (sin límites, desarrollo)
$env:USE_OLLAMA="true"
python main.py

# Volver a GitHub Models (calidad producción)
$env:USE_OLLAMA="false"
python main.py
```

### Opción 2: Modificar Código Directamente

```python
# En graphs/research_graph.py (línea ~68)
USE_OLLAMA = True   # Forzar Ollama
# o
USE_OLLAMA = False  # Forzar GitHub Models
```

---

## 🧪 Scripts de Prueba Disponibles

### 1. Comparación Completa (Agent 1)

```bash
python test_ollama_vs_github.py
```

**Ejecuta**: Agent 1 con ambos proveedores y compara:

- ⏱️ Tiempo de ejecución
- 📝 Longitud de output
- 🎯 Calidad de análisis (viability score, trends, keywords)
- 🔧 Uso de herramientas

**Duración**: ~10-15 minutos (5-8 min por proveedor)

### 2. Test Individual con Ollama

```bash
$env:USE_OLLAMA="true"
python test_single_agent.py
```

### 3. Pipeline Completo con Ollama

```bash
$env:USE_OLLAMA="true"
python main.py
```

⚠️ **Nota**: Agent 2 puede fallar con 40 papers (63K tokens > 32K límite de Mistral). Usar configuración actual de 15 papers (v2.2c).

---

## 📊 Comparación Rápida

| Aspecto        | GitHub Models | Ollama                 |
| -------------- | ------------- | ---------------------- |
| **Modelo**     | gpt-4o        | mistral:7b             |
| **Context**    | 128K tokens   | 32K tokens             |
| **Rate Limit** | 50 req/día ⚠️ | ∞ Ilimitado ✅         |
| **Velocidad**  | Más rápido    | ~2x más lento          |
| **Calidad**    | ⭐⭐⭐⭐⭐    | ⭐⭐⭐⭐ (por validar) |
| **Costo**      | $0 (beta)     | $0 (local)             |
| **Uso**        | Producción    | Desarrollo             |

---

## 🎯 Estrategias Recomendadas

### Estrategia 1: Desarrollo + Validación Final

```bash
# Desarrollo e iteración rápida (sin límites)
$env:USE_OLLAMA="true"
python main.py  # Ejecutar N veces sin preocupación

# Validación final antes de entregar
$env:USE_OLLAMA="false"
python main.py  # Máxima calidad
```

### Estrategia 2: Híbrida por Agente

```python
# En research_graph.py, modificar cada agente:
def niche_analyst_node(state):
    # Agent 1: Ollama (ligero, 15 papers)
    llm = create_model("ollama", "mistral:7b")

def literature_researcher_node(state):
    # Agent 2: GitHub (requiere 128K context para 40 papers)
    llm = create_model("github", "gpt-4o")

def technical_architect_node(state):
    # Agent 3: Ollama (no requiere contexto grande)
    llm = create_model("ollama", "mistral:7b")
```

---

## ⚠️ Limitaciones de Ollama

1. **Context Window**: 32K (vs 128K de gpt-4o)

   - ✅ Agent 1 con 15 papers: ~19K tokens → OK
   - ❌ Agent 2 con 40 papers: ~63K tokens → Excede límite
   - **Solución**: Mantener 15 papers o usar GitHub para Agent 2

2. **Velocidad**: ~2x más lento que gpt-4o

   - Agent 1: 6-8 min vs 3-5 min
   - Aceptable para desarrollo

3. **Calidad**: Por validar en prueba completa
   - Tests unitarios: ✅ 100% exitosos
   - Test E2E: ⏳ Pendiente (`test_ollama_vs_github.py`)

---

## 🔧 Troubleshooting

### Error: "Connection refused to localhost:11434"

```bash
# Verificar que Ollama esté corriendo
# En la terminal donde funciona `ollama list`:
ollama serve

# O verificar vía HTTP:
curl http://localhost:11434/api/tags
```

### Error: "Model mistral:7b not found"

```bash
# Descargar Mistral (4.4GB)
ollama pull mistral:7b

# Verificar descarga
ollama list
```

### Error: Context length exceeded

```bash
# Reducir número de papers en Agent 1/2
# En graphs/research_graph.py buscar:
max_results=15  # Reducir si necesario
```

---

## 📁 Archivos Relevantes

### Configuración:

- `config/settings.py` - Variables `OLLAMA_*`
- `graphs/research_graph.py` - Integración en 5 agentes

### Testing:

- `test_ollama_mistral.py` - Test unitario tool calling (✅ 4/4)
- `test_ollama_vs_github.py` - Comparación completa
- `check_ollama_setup.py` - Diagnóstico (✅ 5/6 checks)

### Documentación:

- `GUIA_OLLAMA.md` - Guía completa (450 líneas)
- `OPTIMIZACIONES_MODELOS.md` - Sección v2.3
- `EVALUACION_MODELOS_OLLAMA.md` - Análisis 9 modelos

---

## 🎉 ¿Qué Sigue?

### Próximo paso recomendado:

```bash
# Ejecutar comparación completa
python test_ollama_vs_github.py
```

Esto te dará:

- ✅ Confirmación de que Ollama funciona en escenario real
- 📊 Métricas de calidad vs GitHub Models
- 💡 Recomendación de cuál estrategia usar

**Duración**: ~15 minutos  
**Resultado**: Decisión informada sobre cuándo usar cada proveedor

---

## 📞 Soporte

Ver documentación completa en:

- `GUIA_OLLAMA.md` - Setup detallado y troubleshooting
- `OPTIMIZACIONES_MODELOS.md` - Estrategias y arquitectura
- `core/model_factory.py` - Código fuente del factory pattern

**Estado actual**: ✅ **SISTEMA LISTO PARA USAR**
