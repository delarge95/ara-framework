# 🚀 Guía Rápida: Configuración y Prueba de Ollama Mistral

## 📋 Resumen de lo que hicimos

### ✅ Configuraciones Completadas

1. **`config/settings.py`**: Agregado soporte para Ollama

   ```python
   OLLAMA_BASE_URL: str = "http://localhost:11434"
   OLLAMA_MODEL: str = "mistral:7b"
   OLLAMA_MODELS_PATH: str = r"E:\modelos_ollama"
   OLLAMA_TEMPERATURE: float = 0.7
   OLLAMA_NUM_CTX: int = 32768  # 32K context window
   ```

2. **`requirements.txt`**: Agregado `langchain-ollama>=0.2.0`

   - ✅ Instalado correctamente

3. **`core/model_factory.py`**: Creado factory para modelos

   - `create_github_model()` - GitHub Models
   - `create_ollama_model()` - Ollama local
   - `create_model()` - Universal factory

4. **`test_ollama_mistral.py`**: Suite de pruebas completa
   - Test 0: Conexión básica
   - Test 1: Tool calling simple
   - Test 2: Múltiples herramientas
   - Test 3: Escenario realista

---

## 🔧 Cómo Ejecutar las Pruebas

### Opción 1: Desde la terminal donde ejecutaste `ollama pull`

**Esa terminal YA tiene Ollama configurado correctamente.**

```bash
# 1. Asegúrate que Ollama server está corriendo
ollama serve

# 2. En OTRA terminal (desde ara_framework), ejecuta:
cd D:\Downloads\TRABAJO_DE_GRADO\ara_framework
python test_ollama_mistral.py
```

### Opción 2: Configurar PATH en PowerShell actual

```powershell
# Agregar Ollama al PATH (temporal, solo esta sesión)
$env:Path += ";C:\Users\alexw\AppData\Local\Programs\Ollama"  # Ajusta si es otra ubicación

# Verificar
ollama list

# Debe mostrar: mistral:7b

# Luego ejecutar pruebas
python test_ollama_mistral.py
```

### Opción 3: Usar ruta completa de Ollama

Si sabes dónde está instalado Ollama:

```powershell
# Ejemplo: C:\Program Files\Ollama\ollama.exe serve
# O: C:\Users\alexw\AppData\Local\Programs\Ollama\ollama.exe serve

# Buscar dónde está:
Get-Command ollama -ErrorAction SilentlyContinue
# O buscar en Program Files:
Get-ChildItem -Path "C:\Program Files" -Filter "ollama.exe" -Recurse -ErrorAction SilentlyContinue
```

---

## 🎯 Qué Esperar de las Pruebas

### ✅ Si TODO funciona (mejor caso):

```
==================================================
 RESUMEN DE RESULTADOS
==================================================
✅ PASADO - Test 0: Conexión básica
✅ PASADO - Test 1: Reconocimiento de herramientas
✅ PASADO - Test 2: Múltiples herramientas
✅ PASADO - Test 3: Escenario realista

Total: 4/4 tests pasados (100.0%)
```

**Acción:** Mistral listo para desarrollo. Puedes usar Ollama sin límites.

### ⚠️ Si funciona PARCIALMENTE (caso probable):

```
==================================================
 RESUMEN DE RESULTADOS
==================================================
✅ PASADO - Test 0: Conexión básica
❌ FALLADO - Test 1: Reconocimiento de herramientas
❌ FALLADO - Test 2: Múltiples herramientas
✅ PASADO - Test 3: Escenario realista

Total: 2/4 tests pasados (50.0%)
```

**Razón:** Mistral puede responder en texto natural sin usar tool calling explícitamente.

**Acción:** Aún útil para desarrollo básico, pero herramientas pueden no funcionar igual que con GitHub Models.

### ❌ Si FALLA Test 0 (problema de conexión):

```
❌ ERROR en Test 0: Connection refused
```

**Razón:** Ollama server no está corriendo.

**Solución:**

1. Abrir terminal donde funcionó `ollama pull`
2. Ejecutar: `ollama serve`
3. Dejar corriendo en background
4. Volver a ejecutar: `python test_ollama_mistral.py`

---

## 📊 Resultados Esperados de la Investigación

Basándome en la documentación oficial:

### ✅ Mistral 7B v0.3 - Tool Calling Confirmado

**Documentación oficial Ollama dice:**

> "Mistral 0.3 supports function calling with Ollama's raw mode"

**Formato esperado:**

```
[AVAILABLE_TOOLS] [{"type": "function", "function": {...}}][/AVAILABLE_TOOLS]
[INST] user prompt [/INST]
[TOOL_CALLS] [{"name": "tool_name", "arguments": {...}}]
```

**Compatibilidad LangChain:**

```python
from langchain_ollama import ChatOllama

llm = ChatOllama(model="mistral:7b").bind_tools([my_tool])
# LangChain traduce automáticamente al formato de Mistral
```

### ⚠️ Posibles Limitaciones

1. **Formato diferente a OpenAI**: Mistral usa formato especial con tags
2. **Precisión menor**: Puede no siempre usar tools cuando debería
3. **Context window**: 32K (vs 128K en gpt-4o)
4. **Calidad**: Probablemente menor que gpt-4o para análisis complejos

---

## 🔄 Alternativas si Mistral No Funciona

### Plan B: Qwen2.5 8B

```bash
# En la terminal con Ollama configurado:
ollama pull qwen2.5:8b

# Luego ejecutar:
python test_ollama_mistral.py  # Modificar para usar qwen2.5:8b
```

**Ventajas:**

- Similar tamaño (4.7GB vs 4.4GB)
- Mejor JSON generation (documentado)
- Tag "tools" presente en Ollama

**Desventajas:**

- Tool calling NO confirmado explícitamente
- Necesita pruebas

### Plan C: Usar GitHub Models Solo Para Desarrollo Crítico

**Estrategia híbrida:**

1. **Pruebas locales rápidas**: Sin LLM, mock responses
2. **Pruebas de integración**: GitHub Models (limitado a 50/día)
3. **Producción**: GitHub Models o alternativa cloud

---

## 💡 Próximos Pasos DESPUÉS de Ejecutar Pruebas

### Si Mistral funciona (Test 1-4 pasan):

#### 1. Modificar `test_single_agent.py` para usar Ollama

```python
# Agregar al inicio del archivo:
USE_OLLAMA = True  # Toggle para cambiar entre providers

# En la función que crea el LLM:
if USE_OLLAMA:
    from core.model_factory import create_ollama_model
    llm = create_ollama_model(model="mistral:7b")
else:
    llm = ChatOpenAI(...)  # GitHub Models
```

#### 2. Comparar calidad de outputs

```bash
# GitHub Models
python test_single_agent.py  # Con USE_OLLAMA = False

# Ollama Mistral
python test_single_agent.py  # Con USE_OLLAMA = True

# Comparar:
# - Longitud de análisis
# - Uso de herramientas (tool calls)
# - Coherencia y calidad
# - Tiempo de ejecución
```

#### 3. Documentar en OPTIMIZACIONES_MODELOS.md

```markdown
## v2.3: Integración Ollama para Desarrollo Local

**Fecha:** 2025-01-XX
**Objetivo:** Eliminar rate limits de GitHub Models durante desarrollo

**Configuración:**

- Modelo: Mistral 7B v0.3
- Context: 32K tokens
- Tool calling: ✅ Soportado
- Costo: $0.00 (local)
- Rate limit: ∞

**Resultados:**

- Test 1: [✅/❌]
- Test 2: [✅/❌]
- Test 3: [✅/❌]
- Test 4: [✅/❌]

**Decisión:**
[Usar Mistral para desarrollo / Mantener GitHub Models / Otro]
```

### Si Mistral falla parcialmente (solo Test 0-1 pasan):

#### Opción A: Aceptar limitaciones

- Usar Ollama para pruebas de flujo (sin herramientas)
- GitHub Models para pruebas de integración completa
- Documentar limitación conocida

#### Opción B: Probar Qwen2.5

```bash
ollama pull qwen2.5:8b
# Modificar test para usar qwen2.5
# Re-ejecutar pruebas
```

#### Opción C: Investigar configuración avanzada

- Revisar logs de Ollama: `ollama logs`
- Verificar formato de tool calling específico de Mistral
- Consultar documentación: https://ollama.com/library/mistral

### Si Mistral falla completamente (Test 0 falla):

#### 1. Verificar instalación de Ollama

```powershell
# Buscar proceso
Get-Process | Where-Object {$_.Name -like "*ollama*"}

# Buscar instalación
Get-ChildItem -Path "C:\" -Filter "ollama.exe" -Recurse -ErrorAction SilentlyContinue
```

#### 2. Reinstalar si es necesario

- Descargar: https://ollama.com/download
- Instalar en ruta estándar
- Configurar variable de entorno OLLAMA_MODELS=E:\modelos_ollama
- Reiniciar terminal

#### 3. Plan Alternativo

```markdown
**Decisión:** Mantener solo GitHub Models

**Mitigación de rate limit:**

- Cache responses (Redis)
- Ejecutar tests menos frecuentemente
- Esperar reset diario (50 req/día es suficiente para 1-2 tests E2E)
- Considerar alternativas cloud:
  - Groq (14,400 req/día, gratis)
  - Gemini 2.5 Pro (1,500 req/día, gratis)
```

---

## 📝 Checklist de Verificación

Antes de reportar resultados:

- [ ] Ollama server está corriendo (`ollama serve` en terminal separada)
- [ ] Mistral descargado y visible (`ollama list` muestra mistral:7b)
- [ ] `langchain-ollama` instalado (`pip list | grep langchain-ollama`)
- [ ] Script ejecutado desde directorio correcto (`ara_framework/`)
- [ ] Puerto 11434 disponible (no bloqueado por firewall)

---

## 🆘 Troubleshooting Común

### Error: "Connection refused"

**Causa:** Ollama server no está corriendo
**Solución:** `ollama serve` en terminal separada

### Error: "Model not found"

**Causa:** Mistral no descargado o PATH incorrecta
**Solución:** Verificar con `ollama list`, re-descargar si necesario

### Error: "Import error: langchain_ollama"

**Causa:** Paquete no instalado
**Solución:** `pip install langchain-ollama`

### Warning: "No tool_calls detected"

**Causa:** Normal en algunos modelos, responden en texto
**Solución:** No es error fatal, documentar comportamiento

---

## 📞 Necesitas Ayuda?

Si encuentras problemas:

1. **Captura pantalla de error completo**
2. **Ejecuta diagnóstico:**
   ```bash
   ollama list
   ollama --version
   pip list | findstr langchain
   python --version
   ```
3. **Comparte resultados de test_ollama_mistral.py**
4. **Indica en qué paso fallaste**

---

**Última actualización:** 2025-01-XX  
**Estado:** Configuración completada, pendiente ejecución de pruebas  
**Próxima acción:** Ejecutar `python test_ollama_mistral.py` desde terminal con Ollama configurado
