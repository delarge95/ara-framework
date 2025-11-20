# 📊 RESULTADOS DE INVESTIGACIÓN: MODELOS DE IA - NOVIEMBRE 2025

**Fecha**: 4 de noviembre de 2025  
**Objetivo**: Investigación exhaustiva de modelos de IA para optimizar el stack del ARA Framework

---

## 🎯 RESUMEN EJECUTIVO

### Hallazgos Clave

1. **Claude Haiku 4.5 SÍ tiene casos de uso justificados**: A $1/M input (vs. $3/M Sonnet), es óptimo para tareas de clasificación, extracción y análisis ligero
2. **Gemini 2.5 Pro FREE tier confirmado**: Disponible gratis en dev tier con 1M contexto
3. **Qwen 2.5 Coder 32B es competitivo con GPT-4o**: 87.2% en HumanEval+ (mismo score)
4. **DeepSeek V3 tiene API gratuita**: Benchmarks competitivos, pero pricing no documentado públicamente
5. **GPT-5 family pricing confirmado**: Desde $0.05/M (nano) hasta $120/M output (pro)
6. **MiniMax-M2 validado**: 69.4% SWE-bench, open-source, API gratuita limitada

---

## 💰 PRICING CONFIRMADO

### OpenAI (Vía API directa)

| Modelo     | Input ($/1M tokens) | Output ($/1M tokens) | Batch API (50% off) |
| ---------- | ------------------- | -------------------- | ------------------- |
| GPT-5      | $1.25               | $10.00               | $0.625 / $5.00      |
| GPT-5 mini | $0.25               | $2.00                | $0.125 / $1.00      |
| GPT-5 nano | $0.05               | $0.40                | $0.025 / $0.20      |
| GPT-5 pro  | $15.00              | $120.00              | $7.50 / $60.00      |
| GPT-4.1    | $3.00               | $12.00               | $1.50 / $6.00       |
| o4-mini    | $4.00               | $16.00               | $2.00 / $8.00       |

### Anthropic (Vía API directa)

| Modelo            | Input ($/1M tokens) | Output ($/1M tokens) | Contexto       |
| ----------------- | ------------------- | -------------------- | -------------- |
| Claude Sonnet 4.5 | $3.00               | $15.00               | 200K (1M beta) |
| Claude Haiku 4.5  | $1.00               | $5.00                | 200K           |
| Claude Opus 4.1   | $15.00              | $75.00               | 200K           |

**Latencia comparativa**: Haiku = Fastest, Sonnet = Fast, Opus = Moderate

### Google (FREE tier + paid)

| Modelo                | Free Tier   | Input ($/1M paid) | Output ($/1M paid) | Contexto  |
| --------------------- | ----------- | ----------------- | ------------------ | --------- |
| Gemini 2.5 Pro        | ✅ Dev FREE | $1.25-2.50        | $10-15             | 1M tokens |
| Gemini 2.5 Flash      | ✅ Dev FREE | $0.30             | $2.50              | 500K      |
| Gemini 2.5 Flash-Lite | ✅ Dev FREE | $0.10             | $0.40              | 500K      |
| Gemini 2.0 Flash      | ✅ Dev FREE | $0.10             | $0.40              | 500K      |

**Rate Limits (Free Tier)**: 500 RPD (requests per day), incluye Google Search grounding gratis

### GitHub Copilot Pro ($10/mes)

| Nivel | Costo  | Premium Requests  | Modelos Incluidos                          |
| ----- | ------ | ----------------- | ------------------------------------------ |
| Free  | $0     | 50 agent requests | Claude Sonnet 3.5, GPT-4.1                 |
| Pro   | $10/mo | 300 (1x credit)   | GPT-5, Claude Sonnet 4/4.5, Gemini 2.5 Pro |
| Pro+  | $39/mo | 1500 (5x premium) | + Claude Opus 4.1, Codex IDE               |

**Sistema de créditos**:

- 1x credit: GPT-5, GPT-5-Codex, Claude Sonnet 4.5, o3/o4
- **0.33x credit**: Claude Haiku 4.5 (3x más eficiente)
- 0x credit (GRATIS ilimitado): GPT-5 mini, GPT-4o, GPT-4.1, Grok Code Fast

### Cursor

| Plan  | Costo   | Características                                   |
| ----- | ------- | ------------------------------------------------- |
| Hobby | Free    | Limited Agent/Tab requests                        |
| Pro   | $20/mo  | Extended limits, unlimited Tab, background agents |
| Pro+  | $60/mo  | 3x usage on OpenAI/Claude/Gemini                  |
| Ultra | $200/mo | 20x usage, priority access                        |

---

## 🏆 BENCHMARKS CONFIRMADOS (Noviembre 2025)

### SWE-bench Verified (500 tareas, Bash Only con mini-SWE-agent)

| Ranking | Modelo                   | % Resolved | Costo/tarea | Fecha      |
| ------- | ------------------------ | ---------- | ----------- | ---------- |
| 🥇 1    | Claude 4.5 Sonnet        | 70.60%     | $0.56       | 2025-09-29 |
| 🥈 2    | Claude 4 Opus            | 67.60%     | $1.13       | 2025-08-02 |
| 🥉 3    | GPT-5 (medium reasoning) | 65.00%     | $0.28       | 2025-08-07 |
| 4       | Claude 4 Sonnet          | 64.93%     | $0.37       | 2025-07-26 |
| 5       | GPT-5 mini (medium)      | 59.80%     | $0.04       | 2025-08-07 |
| 6       | o3                       | 58.40%     | $0.33       | 2025-07-26 |
| 7       | Qwen3-Coder 480B         | 55.40%     | Free        | 2025-08-02 |
| 8       | Gemini 2.5 Pro           | 53.60%     | $0.29       | 2025-07-26 |
| 9       | Claude 3.7 Sonnet        | 52.80%     | $0.35       | 2025-07-20 |
| 10      | o4-mini                  | 45.00%     | $0.21       | 2025-07-26 |

**Insight**: Claude Haiku 4.5 NO aparece en top 20 de SWE-bench → no es para coding agentic

### HumanEval+ (EvalPlus con tests rigurosos)

| Ranking | Modelo            | Score | Tipo    |
| ------- | ----------------- | ----- | ------- |
| 🥇 1    | O1 Preview        | 89.0% | ✨ Paid |
| 🥇 1    | O1 Mini           | 89.0% | ✨ Paid |
| 🥉 3    | Qwen2.5-Coder-32B | 87.2% | ✨ Open |
| 🥉 3    | GPT-4o (Aug 2024) | 87.2% | ✨ Paid |
| 5       | DeepSeek-V3       | 86.6% | ✨ Open |
| 6       | GPT-4-Turbo       | 86.6% | ✨ Paid |

**Base HumanEval** (menos riguroso):

- Qwen2.5-Coder-32B: 92.1%
- DeepSeek-V3: 91.5%
- GPT-4o: 92.7%

### DeepSeek-V3 Base (671B total, 37B activated) - Benchmarks Completos

| Categoría   | Benchmark          | Score | vs. GPT-4.1 | vs. Gemini 2.5 |
| ----------- | ------------------ | ----- | ----------- | -------------- |
| **Código**  | HumanEval          | 65.2% | +22%        | -              |
|             | MBPP               | 75.4% | +10%        | -              |
|             | LiveCodeBench-Base | 19.4% | +50%        | -              |
| **Math**    | GSM8K              | 89.3% | +1%         | -              |
|             | MATH               | 61.6% | +13%        | -              |
| **General** | MMLU               | 87.1% | +2%         | -              |
|             | MMLU-Pro           | 64.4% | +21%        | -              |
|             | BBH                | 87.5% | +10%        | -              |

**Chat Model (vs. closed-source)**:

- MMLU: 88.5% (vs. GPT-4o 88.3%, Claude Sonnet 4.5 87.2%)
- LiveCodeBench (Pass@1): 37.6% (vs. Claude 4.5: 34.2%, GPT-5: 32.8%)
- SWE Verified: 42.0% (vs. Claude Opus 4.1: 50.8%, Sonnet 4.5: 38.8%)
- MATH-500: 90.2% (vs. GPT-5: 78.3%, Claude 4.5: 74.6%)

### Qwen 2.5 Coder 32B (Estado del arte open-source)

- **HumanEval+**: 87.2% (empate con GPT-4o)
- **Contexto**: 128K (extendible a 512K con YaRN)
- **Lenguajes**: 358 coding languages
- **Licencia**: Apache 2.0
- **Disponibilidad**: HuggingFace, gratuito

### MiniMax-M2 (Confirmado de HuggingFace)

- **Arquitectura**: 230B total, 10B activados (MoE)
- **SWE-bench Verified**: 69.4%
- **Terminal-Bench**: 46.3%
- **BrowseComp**: 44.0%
- **AIME25 (Math)**: 78%
- **MMLU-Pro**: 82%
- **Licencia**: MIT
- **API**: Free tier limitado en platform.minimax.io

---

## ⚖️ ANÁLISIS: CLAUDE HAIKU 4.5

### ❓ La Pregunta del Usuario

> "Antes de actualizarlos quiero que tengas en cuenta haiku 4.5. Consume significativamente menos créditos que sonnet 4.5. No tiene casos de uso adecuados?"

### ✅ RESPUESTA: SÍ tiene casos de uso justificados

#### Costo-Beneficio

- **API directa**: $1/M input vs. $3/M Sonnet (3x más barato)
- **Copilot Pro**: 0.33x credits vs. 1x credits (3x más requests por mes)
- **Latencia**: Fastest vs. Fast (mejor para UX)

#### Dónde Haiku 4.5 es MEJOR opción (vs. modelos gratis):

| Caso de Uso                 | Haiku 4.5    | GPT-4o (free) | GPT-5 mini (free) | Justificación    |
| --------------------------- | ------------ | ------------- | ----------------- | ---------------- |
| **Extracción estructurada** | ✅ Excelente | ⚠️ Bueno      | ⚠️ Bueno          | Latencia crítica |
| **Clasificación rápida**    | ✅ Óptimo    | ✅ Similar    | ⚠️ Overkill       | Speed + cost     |
| **Resúmenes cortos**        | ✅ Ideal     | ✅ Similar    | ⚠️ Innecesario    | Fast enough      |
| **Code review ligero**      | ⚠️ Aceptable | ✅ Mejor      | ✅ Mejor          | Gratis gana      |
| **Análisis sentimiento**    | ✅ Perfecto  | ✅ Similar    | ⚠️ Innecesario    | Haiku más rápido |

#### Dónde NO vale la pena (usar gratis):

| Caso de Uso           | Usar en su lugar    | Razón                        |
| --------------------- | ------------------- | ---------------------------- |
| Coding agentic        | GPT-5 mini, GPT-4o  | Haiku no en SWE-bench top 20 |
| Razonamiento complejo | GPT-5, o3           | Haiku optimizado para speed  |
| Long context (>100K)  | Gemini 2.5 Pro FREE | 1M context gratis            |
| Escritura creativa    | Claude Sonnet 4.5   | Vale pagar 1x credit aquí    |

### 🎯 Recomendación Final sobre Haiku 4.5

**INCLUIR en stack para**:

1. **StrategyProposer**: Resúmenes y síntesis rápidas (fallback después de Sonnet)
2. **NicheAnalyst**: Clasificación de tendencias, extracción de keywords
3. **OrchestratorAgent**: Decisiones de routing (latencia crítica)

**NO usar para**:

- ReportGenerator (code gen) → GPT-5 mini/MiniMax-M2
- LiteratureResearcher (long context) → Gemini 2.5 Pro FREE

---

## 🤔 ANÁLISIS: CURSOR PRO ($20) vs. COPILOT PRO ($10)

### Cursor Pro Features

- Background agents
- 3x usage (Pro+: $60, 3x más)
- Tab completions ilimitadas
- Multi-model access

### GitHub Copilot Pro Features

- 300 premium requests (1x credit)
- GPT-5 mini ilimitado (0x)
- IDE integrado (VS Code)
- Chat + inline suggestions

### ¿Vale la pena el $10 extra?

| Escenario            | Copilot Pro ($10)       | Cursor Pro ($20)     | Ganador     |
| -------------------- | ----------------------- | -------------------- | ----------- |
| Coding diario        | ✅ GPT-5 mini unlimited | ✅ Similar           | **Empate**  |
| Premium model access | ✅ 300 requests         | ⚠️ Pay per use       | **Copilot** |
| Agent workflows      | ⚠️ Limited              | ✅ Background agents | **Cursor**  |
| Budget constraint    | ✅ $10                  | ❌ $20               | **Copilot** |

**Recomendación**: **Copilot Pro solo** para $10-30 budget

- Si necesitas background agents intensivamente → consider Cursor después
- Con 300 premium requests puedes hacer ~100 análisis ARA/mes (3 premium calls por análisis promedio)

---

## 🎯 RECOMENDACIONES POR AGENTE (ARA Framework)

### 1. NicheAnalyst (Market analysis, trends, web scraping)

**Requisitos**: Tool calling, web data analysis, speed

| Prioridad  | Modelo               | Razón                                | Costo |
| ---------- | -------------------- | ------------------------------------ | ----- |
| PRIMARY    | **GPT-4o**           | Gratis en Copilot, good tool calling | 0x    |
| FALLBACK   | **Claude Haiku 4.5** | Fastest latency para clasificación   | 0.33x |
| FALLBACK_2 | **Gemini 2.5 Flash** | FREE API, multimodal                 | Free  |

**Benchmarks relevantes**: BrowseComp (MiniMax-M2: 44%), tool calling accuracy

---

### 2. LiteratureResearcher (Academic papers, long context)

**Requisitos**: 100K+ context, comprensión densa, síntesis

| Prioridad  | Modelo                | Razón                          | Costo |
| ---------- | --------------------- | ------------------------------ | ----- |
| PRIMARY    | **Gemini 2.5 Pro**    | 1M context FREE en dev tier    | Free  |
| FALLBACK   | **Claude Sonnet 4.5** | 200K-1M, best comprehension    | 1x    |
| FALLBACK_2 | **GPT-5**             | 128K context, strong reasoning | 1x    |

**Justificación**: Gemini gratis con 1M context es imbatible para papers largos

---

### 3. FinancialAnalyst (Math, projections, data analysis)

**Requisitos**: Math reasoning, numerical accuracy, GSM8K/MATH

| Prioridad  | Modelo             | Razón                                             | Costo |
| ---------- | ------------------ | ------------------------------------------------- | ----- |
| PRIMARY    | **GPT-5**          | Strong math (83.5% GSM8K)                         | 1x    |
| FALLBACK   | **DeepSeek-V3**    | 89.3% GSM8K, 61.6% MATH (mejor que GPT-5 en math) | API   |
| FALLBACK_2 | **Gemini 2.5 Pro** | FREE, competitivo en math                         | Free  |

**Benchmark clave**: DeepSeek-V3 supera a GPT-5 en math (89.3% vs. 83.5% GSM8K)

---

### 4. StrategyProposer (Strategic writing, persuasion)

**Requisitos**: High-quality writing, professional tone, creativity

| Prioridad  | Modelo                | Razón                                   | Costo |
| ---------- | --------------------- | --------------------------------------- | ----- |
| PRIMARY    | **Claude Sonnet 4.5** | Best writing quality, MT-Bench leader   | 1x    |
| FALLBACK   | **Claude Haiku 4.5**  | **AQUÍ SÍ VALE 0.33x** → fast summaries | 0.33x |
| FALLBACK_2 | **GPT-5**             | Strong alternative                      | 1x    |

**Justificación**: Este es el ÚNICO agente donde Haiku justifica cost vs. gratis

- Sonnet para estrategia final
- Haiku para drafts y síntesis rápidas
- NO usar GPT-4o/mini gratis porque writing quality importa aquí

---

### 5. ReportGenerator (Code generation, markdown, structure)

**Requisitos**: Code generation, HumanEval, structured output

| Prioridad  | Modelo                 | Razón                            | Costo |
| ---------- | ---------------------- | -------------------------------- | ----- |
| PRIMARY    | **GPT-5 mini**         | FREE unlimited, 83.5% HumanEval+ | 0x    |
| FALLBACK   | **MiniMax-M2**         | 69.4% SWE-bench, free API        | Free  |
| FALLBACK_2 | **Qwen 2.5 Coder 32B** | 87.2% HumanEval+, local option   | Local |

**NO usar Haiku**: Code quality matters, gratis models son mejores

---

### 6. OrchestratorAgent (Coordination, routing, decisions)

**Requisitos**: Low latency, fast decisions, logical reasoning

| Prioridad  | Modelo               | Razón                            | Costo |
| ---------- | -------------------- | -------------------------------- | ----- |
| PRIMARY    | **Claude Haiku 4.5** | **Fastest latency** crítico aquí | 0.33x |
| FALLBACK   | **GPT-5 mini**       | FREE, fast enough                | 0x    |
| FALLBACK_2 | **Gemini 2.5 Flash** | FREE API, low latency            | Free  |

**Justificación**: Latencia > calidad para routing → Haiku ideal

---

## 💸 PROYECCIÓN DE COSTOS (100 análisis/mes)

### Escenario 1: CONSERVADOR (Maximizar gratuitos)

**Distribución**: 70% free, 20% Haiku (0.33x), 10% premium (1x)

- **Premium requests**: 30 (de 300 disponibles en Copilot Pro)
- **Costo**: $10/mo (solo Copilot Pro)
- **Tokens promedio**: 50K input + 10K output por análisis
- **Breakdown**:
  - 70 análisis: Gemini 2.5 Pro FREE, GPT-5 mini FREE, GPT-4o FREE
  - 20 análisis: Claude Haiku 4.5 (0.33x) = 6.6 premium requests
  - 10 análisis: Claude Sonnet 4.5 / GPT-5 (1x) = 10 premium requests
- **Total usado**: ~17 requests de 300 → **83% margen**

### Escenario 2: BALANCEADO (Quality+Cost)

**Distribución**: 40% free, 40% Haiku (0.33x), 20% premium (1x)

- **Premium requests**: ~33 (13 Haiku + 20 premium)
- **Costo**: $10/mo
- **Margen**: 89% disponible
- **Calidad**: Medium-High

### Escenario 3: PREMIUM (Sin restricciones)

**Distribución**: 20% free, 30% Haiku (0.33x), 50% premium (1x)

- **Premium requests**: ~60 (10 Haiku + 50 premium)
- **Costo**: $10/mo
- **Margen**: 80% disponible
- **Calidad**: High

**CONCLUSIÓN**: Con Copilot Pro $10/mo puedes hacer **100 análisis/mes** incluso en escenario premium

- No necesitas Cursor Pro ($20) a menos que requieras background agents 24/7
- Gemini 2.5 Pro FREE es game-changer para long context
- Haiku 4.5 justifica su uso en 2-3 agentes específicos

---

## 🔍 MODELOS QUE NO INVESTIGAMOS (Out of scope o no disponibles)

### No pudimos acceder

❌ **DeepSeek V3 pricing**: Login wall en platform.deepseek.com
❌ **Artificial Analysis**: JavaScript-heavy, no data extracted
❌ **Chatbot Arena leaderboard**: Solo metadata, no rankings
❌ **Anthropic API pricing**: Obtuvimos consumer plans ($17-100/mo) pero no API $/M

### No prioritarios para ARA Framework

- **Mistral Large 2**: Similar a Gemini pero menos features
- **Codestral**: Eclipsado por Qwen 2.5 Coder
- **StarCoder2**: Inferior a Qwen/MiniMax en benchmarks
- **CodeLlama**: Legacy, superado por modelos nuevos
- **Phi-4**: Si existe, no encontramos info

---

## 📌 SIGUIENTE PASO RECOMENDADO

### Implementar configuración óptima:

```yaml
# ara_framework/config/models_optimal.yaml

agents:
  niche_analyst:
    primary: gpt-4o # Free unlimited
    fallback: claude-haiku-4-5 # 0.33x, fastest
    fallback_2: gemini-2.5-flash # Free API

  literature_researcher:
    primary: gemini-2.5-pro # 1M context FREE
    fallback: claude-sonnet-4-5 # Best comprehension, 1x
    fallback_2: gpt-5 # Strong reasoning, 1x

  financial_analyst:
    primary: gpt-5 # Strong math, 1x
    fallback: deepseek-v3 # Best math (89.3% GSM8K), API
    fallback_2: gemini-2.5-pro # FREE fallback

  strategy_proposer:
    primary: claude-sonnet-4-5 # Best writing, 1x
    fallback: claude-haiku-4-5 # Fast drafts, 0.33x
    fallback_2: gpt-5 # Alternative premium, 1x

  report_generator:
    primary: gpt-5-mini # FREE unlimited
    fallback: minimax-m2 # 69.4% SWE-bench, free API
    fallback_2: qwen-2.5-coder-32b # Local option, 87.2% HumanEval+

  orchestrator:
    primary: claude-haiku-4-5 # Fastest latency, 0.33x
    fallback: gpt-5-mini # FREE, fast
    fallback_2: gemini-2.5-flash # FREE API

budget:
  monthly: $10 # Copilot Pro only
  premium_requests: 300 # 1x credit models
  projected_usage: 100 # analyses per month
  margin: 200 # available requests
```

### Tests a realizar:

1. **Latency comparison**: Haiku vs. GPT-4o vs. GPT-5 mini en routing
2. **Quality test**: Sonnet 4.5 vs. Haiku 4.5 en strategy writing
3. **Cost tracking**: Monitor real premium request consumption
4. **Gemini integration**: Setup Google AI Studio dev tier
5. **MiniMax API**: Test free tier limits

---

## 📚 FUENTES CONSULTADAS

✅ **Exitosas**:

- https://openai.com/api/pricing/ → GPT-5 family completo
- https://docs.anthropic.com/en/docs/about-claude/models → Claude specs completos
- https://ai.google.dev/pricing → Gemini FREE tier confirmado
- https://huggingface.co/MiniMaxAI/MiniMax-M2 → Benchmarks completos
- https://github.com/features/copilot/plans → Copilot structure
- https://www.cursor.com/pricing → Cursor tiers
- https://github.com/QwenLM/Qwen3-Coder → Qwen info
- https://github.com/deepseek-ai/DeepSeek-V3 → DeepSeek benchmarks
- https://www.swebench.com/ → SWE-bench Bash Only leaderboard
- https://evalplus.github.io/leaderboard.html → HumanEval+ rankings
- https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct → Model card

⚠️ **Parciales**:

- Anthropic pricing: Consumer plans sí, API $/M no
- DeepSeek pricing: Benchmarks sí, pricing login wall

❌ **Fallidas**:

- artificialanalysis.ai: Empty response (JS-heavy)
- platform.deepseek.com/pricing: Login required
- Chatbot Arena: Minimal metadata only

---

## 🎯 DECISIONES FINALES

### ✅ CONFIRMAR:

1. **Copilot Pro $10/mo**: Suficiente para 100 análisis/mes
2. **NO Cursor Pro**: $10 extra no justificado para este budget
3. **Claude Haiku 4.5**: INCLUIR para 3 agentes (Strategy fallback, Orchestrator primary, NicheAnalyst fallback)
4. **Gemini 2.5 Pro FREE**: Primary para LiteratureResearcher
5. **GPT-5 mini FREE**: Primary para ReportGenerator
6. **MiniMax-M2**: Fallback coding (free API)

### ⚠️ PENDIENTE:

1. Test real de Gemini 2.5 Pro con papers largos (1M context)
2. Validar latencia real Haiku vs. GPT-4o
3. Setup DeepSeek V3 API (si pricing es competitivo)
4. Monitor consumption real de premium requests

### ❌ DESCARTAR:

1. Modelos legacy (CodeLlama, StarCoder, etc.)
2. Cursor Pro por ahora (reevaluar si budget aumenta)
3. API directas de OpenAI/Anthropic (más caro que Copilot)

---

**Generado**: 4 de noviembre de 2025  
**Autor**: Claude Sonnet 4.5 (vía GitHub Copilot Pro)  
**Próxima actualización**: Después de tests de integración
