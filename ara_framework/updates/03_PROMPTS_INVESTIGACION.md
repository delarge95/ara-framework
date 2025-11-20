# 🔬 PROMPT PARA INVESTIGACIÓN PROFUNDA DE MODELOS DE IA - NOVIEMBRE 2025

**Objetivo**: Obtener datos actualizados y completos de TODOS los modelos de IA disponibles para tomar decisiones informadas sobre el stack tecnológico del proyecto ARA Framework.

---

## 📋 PROMPT PARA DEEP RESEARCH

```
# INVESTIGACIÓN EXHAUSTIVA DE MODELOS DE IA - NOVIEMBRE 2025

## CONTEXTO DEL PROYECTO
Estoy construyendo un sistema multi-agente para investigación de mercado con 6 agentes especializados:
1. NicheAnalyst - Análisis de tendencias y mercado
2. LiteratureResearcher - Revisión de literatura académica
3. FinancialAnalyst - Análisis financiero
4. StrategyProposer - Propuestas estratégicas
5. ReportGenerator - Generación de informes
6. OrchestratorAgent - Coordinación

**Presupuesto**: $10-30 USD/mes (GitHub Copilot Pro + Cursor Pro opcional)
**Requisito**: Maximizar uso de modelos gratuitos/económicos sin sacrificar calidad

---

## PARTE 1: MODELOS DISPONIBLES VÍA GITHUB COPILOT PRO ($10/mes)

Investiga y confirma para CADA modelo disponible en GitHub Copilot Pro (noviembre 2025):

### 1.1 MODELOS PREMIUM (1x crédito por request)
Para cada uno, necesito:
- **GPT-5**:
  - Ventana de contexto real
  - Casos de uso óptimos (¿razonamiento? ¿código? ¿escritura?)
  - Comparación con GPT-4 Turbo (% mejora en benchmarks)
  - ¿Vale la pena gastar 1x crédito vs. usar GPT-4o gratis?
- **GPT-5-Codex**:
  - ¿Qué lo diferencia de GPT-5 estándar?
  - Benchmarks en HumanEval, MBPP, SWE-bench
  - ¿Mejor que MiniMax-M2 para coding? (comparar)
- **o1, o3** (reasoning models):
  - Contexto máximo
  - Tiempo de respuesta promedio
  - Casos de uso donde vale 1x crédito
  - ¿Mejor que GPT-5 para arquitectura/strategy?
- **Claude Sonnet 4.5**:
  - Benchmarks de escritura (vs. Haiku, vs. Sonnet 3.5)
  - Contexto (¿200K confirmado?)
  - ¿Realmente mejor que GPT-5 para contenido académico?
- **Gemini 2.5 Pro** (via Copilot):
  - ¿Cuesta 1x crédito en Copilot? (confirmar)
  - Si sí, ¿por qué usarlo aquí si Google AI Studio es gratis?

### 1.2 MODELOS ECONÓMICOS (0.33x crédito)
- **Claude Haiku 4.5**:
  - ⚠️ **CRÍTICO**: Benchmarks completos (MMLU, HumanEval, GSM8K, etc.)
  - Velocidad (tokens/segundo) vs. Sonnet 4.5
  - Casos de uso óptimos donde 0.33x crédito vale la pena:
    - ¿Resúmenes rápidos?
    - ¿Análisis de sentimiento?
    - ¿Clasificación de texto?
    - ¿Extracción de datos estructurados?
    - ¿Code review ligero?
  - **Comparación directa**: Haiku 4.5 vs. GPT-4o (gratis):
    - ¿En qué escenarios Haiku supera a GPT-4o?
    - ¿Justifica pagar 0.33x si GPT-4o es gratis?
  - Latencia promedio (ms)
  - ¿Mejor que modelos gratuitos (GPT-4o, DeepSeek V3) para tareas específicas?

### 1.3 MODELOS GRATUITOS (0x crédito)
Para cada uno:
- **GPT-4o**:
  - Benchmarks actuales (noviembre 2025)
  - Contexto confirmado
  - ¿Multimodal? (¿acepta imágenes?)
  - Casos de uso donde es mejor opción que premium
- **GPT-4o mini**:
  - ¿Cuándo elegirlo sobre GPT-4o estándar?
  - Velocidad vs. calidad trade-off
- **GPT-5 mini**:
  - ⚠️ **CONFIRMAR**: ¿Existe como modelo separado o es alias?
  - Si existe, benchmarks vs. GPT-4o
- **GPT-4.1**:
  - ¿Qué versión es? (¿GPT-4 Turbo actualizado?)
  - Benchmarks actuales
- **Grok Code Fast 1**:
  - Benchmarks de código (HumanEval, MBPP)
  - Contexto
  - ¿Realmente competitivo para coding?

---

## PARTE 2: MODELOS EXTERNOS GRATUITOS

### 2.1 GOOGLE AI STUDIO (Gratis en tier dev)
- **Gemini 2.5 Pro**:
  - Confirmación de gratuidad (noviembre 2025)
  - Rate limits reales (RPM, RPD, TPM)
  - Benchmarks completos (MMLU, GSM8K, HumanEval, etc.)
  - Contexto: ¿1M tokens confirmado? ¿Cómo se compara con Claude Sonnet?
  - Casos de uso óptimos (papers largos, análisis extenso)
  - ¿Multimodal? (imágenes, video)
- **Gemini 2.5 Flash**:
  - Benchmarks vs. Gemini 2.5 Pro
  - Velocidad (tokens/segundo)
  - ¿Cuándo elegir Flash sobre Pro?
- **Gemini 2.0 Flash Thinking** (si existe en nov 2025):
  - Benchmarks de razonamiento
  - Comparación con o1/o3 de OpenAI

### 2.2 ANTHROPIC (API directa - si es viable económicamente)
- **Claude Sonnet 4.5** (API directa):
  - Pricing actual ($/1M tokens input/output)
  - ¿Vale la pena vs. usar créditos Copilot?
- **Claude Haiku 4.5** (API directa):
  - Pricing actual
  - ¿Más barato que 0.33x crédito en Copilot?
  - Si sí, calcular breakeven point

### 2.3 DEEPSEEK (API Gratis)
- **DeepSeek V3**:
  - Confirmación de gratuidad (noviembre 2025)
  - Rate limits
  - Benchmarks actualizados (código, razonamiento, matemáticas)
  - Contexto: 128K confirmado
  - Comparación con GPT-4o (gratis) y MiniMax-M2:
    - ¿En qué es mejor DeepSeek?
    - ¿En qué es peor?
- **DeepSeek Coder V2** (si existe):
  - Benchmarks de código
  - ¿Mejor que Qwen 2.5 Coder?

### 2.4 MINIMAX (Open-Source + API Gratis Limitada)
- **MiniMax-M2** (ya investigado, pero confirmar):
  - Benchmarks actualizados de noviembre 2025
  - API gratuita: rate limits exactos
  - Deployment local:
    - Requisitos mínimos GPU (VRAM)
    - Quantizaciones disponibles (FP8, INT4, etc.)
    - Velocidad inference local (tokens/segundo en diferentes GPUs)
  - Comparación directa con GPT-5-Codex:
    - SWE-bench: MiniMax 69.4% vs. GPT-5-Codex ?%
    - Terminal-Bench: MiniMax 46.3% vs. GPT-5-Codex ?%
  - ¿Vale la pena gastar 1x crédito en GPT-5-Codex si tengo MiniMax-M2 gratis?

### 2.5 ALIBABA QWEN
- **Qwen 2.5 Coder**:
  - Versión más reciente (noviembre 2025)
  - Tamaños disponibles (7B, 14B, 32B, 72B)
  - Benchmarks (HumanEval, MBPP, LiveCodeBench)
  - API gratuita disponible? Rate limits
  - Comparación con MiniMax-M2 y GPT-5-Codex
- **Qwen 2.5** (modelo base):
  - Benchmarks generales
  - Casos de uso vs. modelos especializados

### 2.6 MISTRAL
- **Codestral**:
  - API gratuita? Pricing
  - Benchmarks de código
  - ¿Mejor que Qwen 2.5 Coder en algún aspecto?
- **Mistral Large 2** (si es gratis):
  - Benchmarks generales
  - Comparación con GPT-4o, Claude Haiku 4.5

### 2.7 OTROS MODELOS OPEN-SOURCE RELEVANTES
Investiga si existen versiones actualizadas (nov 2025) de:
- **StarCoder2**: Benchmarks actuales, tamaños, casos de uso
- **CodeLlama**: ¿Sigue siendo relevante vs. Qwen/MiniMax?
- **LLaMA 3.x** (si Meta lanzó versión nueva): Benchmarks, gratuidad
- **Phi-4** (Microsoft, si existe): Benchmarks, tamaño, casos de uso

---

## PARTE 3: ANÁLISIS COMPARATIVO POR CASO DE USO

Para cada agente, necesito recomendación de modelo PRIMARY → FALLBACK → FALLBACK_2:

### 3.1 NicheAnalyst (Análisis de mercado, web scraping, trends)
Requisitos:
- Tool calling confiable (MCP: Jina AI, Playwright)
- Capacidad de análisis de datos web
- Síntesis de tendencias
- NO requiere escritura sofisticada

**Pregunta**: ¿Qué modelos son óptimos?
- Opciones a comparar: GPT-4o, Haiku 4.5, MiniMax-M2, DeepSeek V3, Gemini 2.5 Pro
- Benchmark relevante: BrowseComp, tool calling accuracy

### 3.2 LiteratureResearcher (Papers académicos largos, síntesis)
Requisitos:
- Contexto largo (idealmente 100K+ tokens)
- Comprensión de texto académico denso
- Síntesis precisa
- Extracción de información estructurada

**Pregunta**: ¿Qué modelos son óptimos?
- Opciones: Gemini 2.5 Pro (1M ctx), Claude Sonnet 4.5, GPT-5, MiniMax-M2, DeepSeek V3
- ¿Vale la pena pagar por Sonnet 4.5 vs. usar Gemini gratis?

### 3.3 FinancialAnalyst (Cálculos, análisis numérico, proyecciones)
Requisitos:
- Razonamiento matemático
- Análisis de tablas/datos
- Generación de insights cuantitativos

**Pregunta**: ¿Qué modelos son óptimos?
- Opciones: GPT-5, o1/o3, Gemini 2.5 Pro, DeepSeek V3, GPT-4o
- Benchmark relevante: GSM8K, MATH

### 3.4 StrategyProposer (Escritura estratégica, persuasión, creatividad)
Requisitos:
- Escritura de alta calidad
- Tono profesional/académico
- Creatividad en propuestas
- Coherencia narrativa

**Pregunta**: ¿Qué modelos son óptimos?
- Opciones: Claude Sonnet 4.5, Claude Haiku 4.5, GPT-5, Gemini 2.5 Pro
- ⚠️ **CRÍTICO**: ¿Haiku 4.5 es suficientemente bueno para estrategia? (0.33x crédito)
- Benchmark relevante: MT-Bench (escritura), IFEval

### 3.5 ReportGenerator (Generación de código markdown, estructuración, formato)
Requisitos:
- Generación de código (markdown, LaTeX)
- Estructuración de documentos
- Manejo de templates
- NO requiere escritura super sofisticada (más técnico)

**Pregunta**: ¿Qué modelos son óptimos?
- Opciones: GPT-5-Codex, MiniMax-M2, Qwen 2.5 Coder, Haiku 4.5, GPT-4o
- ¿Haiku 4.5 es bueno para código estructurado simple?

### 3.6 OrchestratorAgent (Coordinación, decisiones, routing)
Requisitos:
- Razonamiento lógico
- Toma de decisiones
- Low latency (respuestas rápidas)
- Gestión de estado

**Pregunta**: ¿Qué modelos son óptimos?
- Opciones: GPT-5, GPT-4o, Haiku 4.5 (rápido), DeepSeek V3
- ¿Haiku 4.5 es suficientemente inteligente para coordinar?

---

## PARTE 4: BENCHMARKS ESPECÍFICOS CRÍTICOS

Busca resultados actualizados (noviembre 2025) para TODOS los modelos en:

### 4.1 Benchmarks de Código
- **HumanEval** (Python coding)
- **MBPP** (Mostly Basic Python Problems)
- **SWE-bench Verified** (real repo edits)
- **SWE-bench Multilingual** (multi-language)
- **Terminal-Bench** (command-line tasks)
- **LiveCodeBench** (recent problems)
- **MultiPL-E** (multilanguage coding)

### 4.2 Benchmarks de Razonamiento
- **MMLU** (general knowledge)
- **MMLU-Pro** (harder variant)
- **GPQA** (science Q&A)
- **GSM8K** (math word problems)
- **MATH** (competition math)
- **ARC-Challenge** (reasoning)
- **HellaSwag** (commonsense)

### 4.3 Benchmarks Agentic
- **BrowseComp** (web browsing)
- **GAIA** (assistant tasks)
- **AgentBench** (agent capabilities)
- **WebArena** (web automation)
- **τ²-Bench** (tool use)

### 4.4 Benchmarks de Escritura
- **MT-Bench** (multi-turn conversation)
- **AlpacaEval** (instruction following)
- **IFEval** (instruction following)
- **Arena-Hard** (challenging prompts)

---

## PARTE 5: ANÁLISIS DE COSTOS DETALLADO

### 5.1 GitHub Copilot Pro Credits
- ¿Cuántos créditos incluye la suscripción mensual ($10)?
- ¿Qué pasa cuando se agotan? (throttling, pago extra, etc.)
- Casos reportados de agotamiento en uso intensivo

### 5.2 Comparación Económica
Calcula costo por 1M tokens (input + output promedio 50/50):

**Modelos de Pago:**
- GPT-5 (1x crédito): $? equivalente
- GPT-5-Codex (1x crédito): $?
- Claude Sonnet 4.5 (1x crédito): $?
- Claude Haiku 4.5 (0.33x crédito): $?
- Claude Haiku 4.5 (API directa Anthropic): $?

**Punto de Equilibrio:**
- ¿Cuántos requests de Haiku 4.5 necesito para que sea más barato usar API directa vs. Copilot?

### 5.3 Proyección de Costos para ARA Framework
Asumiendo:
- 1 análisis completo = 50 requests (distribución: 20% premium, 30% económicos, 50% gratis)
- Objetivo: 100 análisis/mes

Calcula costo mensual en 3 escenarios:
1. **Estrategia conservadora**: Solo modelos gratis + mínimo premium
2. **Estrategia balanceada**: Mix de gratis, Haiku, y premium selectivo
3. **Estrategia premium**: Usar mejores modelos sin restricción de créditos

---

## PARTE 6: LATENCIA Y PERFORMANCE

Para cada modelo, si disponible:
- **Latencia promedio** (time to first token)
- **Throughput** (tokens/segundo)
- **Tiempo total** respuesta típica (500 tokens output)

Esto es crítico para:
- Orchestrator (necesita baja latencia)
- ReportGenerator (puede tolerar latencia si calidad es mejor)

---

## PARTE 7: HERRAMIENTAS Y MCP SERVERS

### 7.1 MCP Servers Gratuitos (confirmar vigencia nov 2025)
Para cada uno, confirma:
- **Jina AI Reader**: Rate limits actuales, cambios en API
- **GitHub MCP**: Limitaciones, rate limits
- **Playwright MCP**: Funcionalidad completa, requiere setup especial?
- **Supabase MCP**: Free tier actual (500MB sigue vigente?)
- **Notion MCP**: Free tier, limitaciones
- **MarkItDown MCP**: Funcionalidad, limitaciones
- **ChromeDevTools MCP**: Status del proyecto
- **Rube MCP**: Qué hace exactamente? Vale la pena?

### 7.2 Alternativas a Considerar
Investiga si existen MCP servers nuevos (nov 2025) para:
- **Academic paper search** (mejor que Semantic Scholar?)
- **Financial data** (Yahoo Finance, Alpha Vantage)
- **Market research** (Statista, etc.)
- **Web scraping** (alternativas a Jina AI si rate limit es problema)

---

## PARTE 8: EDITORES AGENTIC

### 8.1 Cursor Pro vs. GitHub Copilot Pro
- ¿Cursor Pro ($20) realmente vale la pena SI ya tengo Copilot Pro ($10)?
- Features exclusivos de Cursor que justifiquen $20 extra
- Casos de uso donde Cursor supera Copilot
- ¿Puedo hacer todo con Copilot Pro + VS Code + extensiones?

### 8.2 Alternativas Gratuitas
- **Continue.dev**: ¿Qué modelos soporta? Integración con modelos locales
- **Tabby**: Self-hosted coding assistant
- **Cody** (Sourcegraph): Free tier, limitaciones
- ¿Alguna puede reemplazar Cursor Pro?

---

## FORMATO DE RESPUESTA ESPERADO

Por favor, estructura la investigación en:

### 1. TABLA COMPARATIVA MAESTRA
| Modelo | Provider | Costo | Contexto | HumanEval | MMLU | GSM8K | SWE-bench | Latency | Use Cases Óptimos |
|--------|----------|-------|----------|-----------|------|-------|-----------|---------|-------------------|
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

### 2. RECOMENDACIONES POR AGENTE
Para cada uno de los 6 agentes:
- **Primary Model**: [Modelo] - Razón
- **Fallback 1**: [Modelo] - Razón
- **Fallback 2**: [Modelo] - Razón
- **Justificación de costos**: Por qué esta combinación maximiza calidad/precio

### 3. ANÁLISIS DE CLAUDE HAIKU 4.5
- **Casos de uso donde Haiku 4.5 es MEJOR opción que modelos gratis**
- **Casos donde NO vale la pena (usar gratis en su lugar)**
- **Recomendación final**: ¿Incluirlo en el stack o no?

### 4. DECISIÓN SOBRE CURSOR PRO
- **Ventajas objetivas** de pagar $20 extra
- **Alternativas gratuitas** que logran 80% de la funcionalidad
- **Recomendación**: ¿Mantener trial y cancelar, o suscribir?

### 5. CONFIGURACIÓN ÓPTIMA FINAL
YAML completo con asignación de modelos basada en esta investigación

---

## FUENTES RECOMENDADAS PARA INVESTIGAR

- Artificial Analysis (https://artificialanalysis.ai/) - Benchmarks actualizados
- Chatbot Arena (LMSYS) - Rankings comunitarios
- Papers with Code - Leaderboards oficiales
- GitHub oficial de cada modelo - Documentación técnica
- Blogs oficiales: OpenAI, Anthropic, Google AI, DeepSeek, MiniMax
- Reddit: r/LocalLLaMA, r/MachineLearning - Experiencias reales
- Hugging Face Open LLM Leaderboard
- LLM Benchmarking por Anyscale/Modal
- Documentación oficial de GitHub Copilot (créditos)
- Anthropic pricing page (Claude API)
- Google AI Studio docs (Gemini rate limits)

---

## CRITERIOS DE DECISIÓN

Al final, quiero poder responder:

1. ¿Vale la pena pagar 1x crédito por GPT-5-Codex si MiniMax-M2 es gratis y comparablemente bueno?
2. ¿Claude Haiku 4.5 (0.33x) tiene casos de uso donde justifica el costo vs. GPT-4o (gratis)?
3. ¿Claude Sonnet 4.5 es significativamente mejor que GPT-5 para escritura?
4. ¿Gemini 2.5 Pro gratis puede reemplazar la mayoría de uso de modelos premium?
5. ¿Cursor Pro $20 se justifica o puedo hacer todo con Copilot Pro $10?
6. ¿Qué combinación de modelos me da la mejor relación calidad/precio para 100 análisis/mes?

---

## ENTREGABLES

1. **Documento Markdown** (~5000 palabras) con investigación completa
2. **Tabla Excel/CSV** con todos los benchmarks comparativos
3. **Archivo YAML** con configuración recomendada final de modelos
4. **Análisis de costos** con 3 escenarios (conservador, balanceado, premium)
5. **Recomendación ejecutiva** (1 página) con decisiones finales
```

---

## 🎯 CÓMO USAR ESTE PROMPT

### Opción 1: **Perplexity Pro** (Recomendado)

- Copia todo el prompt en Perplexity
- Usa modo "Pro Search" o "Deep Research"
- Espera 5-10 minutos para investigación profunda
- Obtendrás fuentes citadas y datos verificados

### Opción 2: **ChatGPT-4 + Web Browsing**

- Requiere ChatGPT Plus con browsing habilitado
- Copia el prompt
- Puede requerir múltiples iteraciones

### Opción 3: **Claude 3.5 Sonnet (API) + Artifacts**

- Usa en claude.ai con proyectos
- Puede generar tablas y YAML directamente
- Bueno para análisis cualitativo

### Opción 4: **Yo mismo (GitHub Copilot Agent)**

- Puedo ejecutar `fetch_webpage` múltiple para:
  - Artificial Analysis
  - Chatbot Arena
  - Documentación oficial de modelos
  - Pricing pages
- Limitación: Solo puedo acceder a páginas públicas

---

## 🚀 SIGUIENTE PASO RECOMENDADO

**TE RECOMIENDO**: Usa **Perplexity Pro** con este prompt porque:

1. ✅ Acceso a fuentes actualizadas (nov 2025)
2. ✅ Citación de fuentes verificables
3. ✅ Análisis profundo automatizado
4. ✅ Puede comparar benchmarks de múltiples fuentes
5. ✅ Genera tablas comparativas automáticamente

**ALTERNATIVAMENTE**: Si no tienes Perplexity Pro, puedo:

- Ejecutar investigación con `fetch_webpage` a 10-15 fuentes clave
- Tomará más tiempo pero puedo hacerlo ahora mismo
- ¿Quieres que lo haga yo con las herramientas disponibles?

---

**¿Qué prefieres?**

1. Usar este prompt en Perplexity Pro (tú ejecutas)
2. Que yo investigue con fetch_webpage (ejecuto yo ahora)
3. Ambos (tú en Perplexity, yo complemento con mis herramientas)
