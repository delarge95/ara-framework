# 📊 COMPARATIVA CONSOLIDADA DE BENCHMARKS - NOVIEMBRE 2025

**Fuentes**: Perplexity + Gemini + SWE-bench + EvalPlus + Investigación propia

---

## Tabla 1: Benchmarks Completos (15 Modelos)

| Modelo                | Proveedor | Contexto  | HumanEval | MMLU        | GSM8K | SWE-bench    | Terminal | Latencia          | Costo       | Disponibilidad                     |
| --------------------- | --------- | --------- | --------- | ----------- | ----- | ------------ | -------- | ----------------- | ----------- | ---------------------------------- |
| **GPT-5**             | OpenAI    | 400K      | ~92%      | **88.7%**   | ~95%  | 72.8%        | 43.8%    | 1.5-2s            | 1x          | Copilot Pro+/Chat                  |
| **GPT-5-Codex**       | OpenAI    | 400K      | ~94%      | ~90%        | ~95%  | ~75%         | ~45%     | 1.8-2.2s          | 1x          | Copilot Pro+/VSCode                |
| **GPT-5 mini**        | OpenAI    | 128K      | ~85%      | ~87%        | ~85%  | ~70%         | ~40%     | 800-1200ms        | 0x          | Copilot Pro/Chat                   |
| **o3/o3-mini**        | OpenAI    | 128K      | ~95%      | ~92%        | ~98%  | 74.9%        | ~48%     | 3-5s              | 1-2x        | Deprecated (integrated into GPT-5) |
| **Claude Sonnet 4.5** | Anthropic | 200K      | ~85%      | ~88%        | ~94%  | **77.2%** ⭐ | 50.0%    | 1.2-1.6s          | 1x          | Copilot Pro+/API                   |
| **Claude Haiku 4.5**  | Anthropic | 200K      | ~80%      | ~82%        | ~88%  | 73.3%        | ~42%     | **600-1000ms** ⭐ | 0.33x       | Copilot Pro/API                    |
| **Claude Opus 4.1**   | Anthropic | 200K      | ~84%      | ~87%        | ~92%  | 76.5%        | ~48%     | 1.5-2s            | 1x          | API only                           |
| **Gemini 2.5 Pro**    | Google    | **1M** ⭐ | ~90%      | 86%         | ~90%  | 63.8%        | 25.3%    | 2-3s              | **FREE** ⭐ | Google AI Studio                   |
| **Gemini 2.5 Flash**  | Google    | 500K      | ~88%      | 85%         | ~88%  | ~60%         | ~20%     | 1.5-2s            | **FREE**    | Google AI Studio                   |
| **Gemini 2.0 Flash**  | Google    | 1M        | ~87%      | 84%         | ~86%  | ~55%         | ~15%     | 1-1.5s            | **FREE**    | Google AI Studio                   |
| **DeepSeek V3**       | DeepSeek  | 128K      | ~92%      | ~88%        | ~89%  | 67.8%        | 37.7%    | 1-1.5s            | **FREE**    | OpenRouter/platform                |
| **MiniMax-M2**        | MiniMax   | 200K+     | ~83%      | **~95%** ⭐ | ~92%  | 69.4%        | 46.3%    | 800-1200ms        | **FREE**    | API + Open-source                  |
| **Qwen 2.5 Coder**    | Alibaba   | 128K      | ~87%      | ~86%        | ~85%  | ~72%         | ~38%     | 1-1.5s            | **FREE**    | API + Open-source                  |
| **Grok Code Fast 1**  | xAI       | 128K      | ~82%      | ~85%        | ~82%  | ~65%         | ~35%     | 400-800ms         | 0.25x       | Copilot Pro                        |
| **GPT-4o**            | OpenAI    | 128K      | ~88%      | **88.7%**   | ~88%  | ~68%         | ~40%     | 1.2-1.6s          | **0x** ⭐   | Copilot Chat/API                   |

---

## Tabla 2: Ranking por Categoría

### 🏆 SWE-bench Verified (Software Engineering)

Top performers para tareas de ingeniería de software compleja:

1. **Claude Sonnet 4.5**: 77.2% ⭐
2. **GPT-5-Codex**: ~75%
3. **o3-mini**: 74.9%
4. **Claude Haiku 4.5**: 73.3%
5. **GPT-5**: 72.8%
6. **Qwen 2.5 Coder**: ~72%
7. **MiniMax-M2**: 69.4%
8. **DeepSeek V3**: 67.8%
9. **Gemini 2.5 Pro**: 63.8%

### 🧮 MMLU (General Knowledge)

Comprensión de conocimiento general a nivel universitario:

1. **MiniMax-M2**: ~95% ⭐
2. **GPT-5**: 88.7% ⭐
3. **GPT-4o**: 88.7% ⭐
4. **Claude Sonnet 4.5**: ~88%
5. **DeepSeek V3**: ~88%
6. **Gemini 2.5 Pro**: 86%
7. **Qwen 2.5 Coder**: ~86%
8. **Claude Haiku 4.5**: ~82%

### 📐 GSM8K (Math)

Razonamiento matemático grado 8:

1. **GPT-5**: ~95% ⭐ (SOTA)
2. **GPT-5-Codex**: ~95%
3. **MiniMax-M2**: ~92%
4. **o3-mini**: ~98% (pero 3-5s latencia)
5. **DeepSeek V3**: ~89%
6. **Claude Sonnet 4.5**: ~94%
7. **Gemini 2.5 Pro**: ~90%

### ⚡ Latencia (Velocidad)

Menor latencia = mejor para aplicaciones interactivas:

| Modelo                | TTFB (ms)         | Razón                                  |
| --------------------- | ----------------- | -------------------------------------- |
| **Grok Code Fast 1**  | **400-800ms** ⭐  | Optimizado para velocidad              |
| **Claude Haiku 4.5**  | **600-1000ms** ⭐ | Diseñado para baja latencia            |
| **GPT-5 mini**        | 800-1200ms        | Modelo mini rápido                     |
| **MiniMax-M2**        | 800-1200ms        | Eficiente                              |
| **DeepSeek V3**       | 1-1.5s            | Razonable                              |
| **Claude Sonnet 4.5** | 1.2-1.6s          | Estándar                               |
| **GPT-4o**            | 1.2-1.6s          | Estándar                               |
| Gemini 2.5 Flash      | 1.5-2s            | Rápido pero más lento que alternativas |
| **GPT-5**             | 1.5-2s            | Alto (reasoning integrado)             |
| **o3-mini**           | **3-5s** ⚠️       | Demasiado lento para orchestration     |
| **Gemini 2.5 Pro**    | 2-3s              | Más lento por contexto grande          |

### 🔓 Disponibilidad de Free Tier

Modelos disponibles SIN COSTO:

| Modelo               | Free Tier           | Límites                   |
| -------------------- | ------------------- | ------------------------- |
| **Gemini 2.5 Pro**   | ✅ Google AI Studio | 5 RPM, 32K TPM            |
| **Gemini 2.5 Flash** | ✅ Google AI Studio | 10 RPM, 32K TPM           |
| **GPT-4o**           | ✅ Copilot Chat     | 50 mensajes/3h            |
| **GPT-5 mini**       | ✅ Copilot Pro (0x) | Ilimitado en Copilot      |
| **DeepSeek V3**      | ✅ OpenRouter       | 100 req/day o pago        |
| **MiniMax-M2**       | ✅ API Gratis       | Ilimitado (límites TBD)   |
| **Qwen 2.5 Coder**   | ✅ API + Ollama     | Ilimitado (self-hosted)   |
| **Claude Haiku 4.5** | ❌ Solo Copilot/API | 0.33x Copilot o $1/$5 API |
| **Grok Code Fast 1** | ⚠️ 0.25x Copilot    | Casi gratis               |

---

## Tabla 3: Análisis Comparativo por Caso de Uso

### Caso 1: Research Largo (1M contexto necesario)

| Modelo               | Contexto  | Costo       | Velocidad       | Recomendación |
| -------------------- | --------- | ----------- | --------------- | ------------- |
| **Gemini 2.5 Pro**   | **1M** ⭐ | **FREE** ⭐ | Media (2-3s)    | ✅ USAR       |
| **Gemini 2.0 Flash** | 1M        | FREE        | Rápido (1-1.5s) | ✅ USAR       |
| Claude Sonnet 4.5    | 200K      | 1x          | Rápido (1.2s)   | Fallback      |
| GPT-5                | 400K      | 1x          | Lento (1.5-2s)  | Fallback      |

**Veredicto**: Gemini 2.5 Pro es insustituible

---

### Caso 2: Coding SWE-level (Best in class)

| Modelo                | SWE-bench    | Costo | Disponibilidad | Recomendación               |
| --------------------- | ------------ | ----- | -------------- | --------------------------- |
| **Claude Sonnet 4.5** | **77.2%** ⭐ | 1x    | Copilot Pro+   | ✅ PRIMARY                  |
| **GPT-5-Codex**       | ~75%         | 1x    | Copilot Pro+   | ✅ CUANDO SOBRAN CRÉDITOS   |
| **MiniMax-M2**        | 69.4%        | FREE  | API gratis     | ✅ FALLBACK (90% tan bueno) |
| o3-mini               | 74.9%        | 1-2x  | Copilot Pro+   | ⚠️ Lento (3-5s)             |

**Veredicto**: Sonnet si presupuesto, MiniMax si cost-optimized

---

### Caso 3: Razonamiento Matemático (Finance)

| Modelo            | GSM8K       | Math   | Costo | Recomendación      |
| ----------------- | ----------- | ------ | ----- | ------------------ |
| **o3-mini**       | **~98%** ⭐ | Best   | 1-2x  | ❌ Demasiado lento |
| **GPT-5**         | **~95%** ⭐ | SOTA   | 1x    | ✅ PRIMARY         |
| **MiniMax-M2**    | **~92%** ⭐ | Fuerte | FREE  | ✅ FALLBACK        |
| Claude Sonnet 4.5 | ~94%        | SOTA   | 1x    | ✅ FALLBACK        |

**Veredicto**: GPT-5 necesario para math complejo

---

### Caso 4: Escritura Estratégica (MT-Bench)

| Modelo                | Escritura           | Costo | Latencia       | Recomendación |
| --------------------- | ------------------- | ----- | -------------- | ------------- |
| **GPT-5**             | SOTA                | 1x    | Lento (1.5-2s) | ✅ Mejor      |
| **Claude Sonnet 4.5** | SOTA                | 1x    | Rápido (1.2s)  | ✅ Mejor      |
| **Claude Haiku 4.5**  | Buena (IFBench 72%) | 0.33x | **Rápido** ⭐  | ✅ BALANCEADO |
| **GPT-4o**            | Muy buena           | 0x    | Estándar       | ✅ Gratis     |

**Veredicto**: Haiku 0.33x es sweet spot para presupuesto limitado

---

### Caso 5: Computer Use / Terminal (OSWorld, Terminal-Bench)

| Modelo               | OSWorld      | Terminal | Costo | Recomendación      |
| -------------------- | ------------ | -------- | ----- | ------------------ |
| **Claude Haiku 4.5** | **50.7%** ⭐ | 42%      | 0.33x | ✅ MEJOR           |
| Claude Sonnet 4.5    | 42.2%        | 50%      | 1x    | ⚠️ Mixed           |
| Claude Opus 4.1      | 39.8%        | ~48%     | 1x    | ⚠️ Inferior        |
| GPT-4o               | 45%          | 40%      | 0x    | ✅ Gratis fallback |

**Veredicto**: Haiku supera aquí a Sonnet en 8.5% (computer use)

---

## Tabla 4: Matriz Costo-Beneficio

Para cada modelo, score de ROI en escala 1-10 (10 = mejor):

| Modelo               | Performance | Costo  | Disponibilidad | Latencia | ROI Total           |
| -------------------- | ----------- | ------ | -------------- | -------- | ------------------- |
| **Gemini 2.5 Pro**   | 8           | **10** | **9**          | 6        | **33/40** ⭐⭐⭐    |
| **MiniMax-M2**       | 8           | **10** | **9**          | 8        | **35/40** ⭐⭐⭐    |
| **Claude Haiku 4.5** | 7           | 8      | 8              | **10**   | **33/40** ⭐⭐⭐    |
| **GPT-4o**           | 8           | **10** | **9**          | 7        | **34/40** ⭐⭐⭐    |
| **GPT-5 mini**       | 7           | **10** | 8              | 8        | **33/40** ⭐⭐⭐    |
| **DeepSeek V3**      | 8           | **10** | 8              | 8        | **34/40** ⭐⭐⭐    |
| Claude Sonnet 4.5    | 9           | 4      | 8              | 7        | 28/40               |
| GPT-5                | 9           | 4      | 7              | 6        | 26/40               |
| Gemini 2.5 Flash     | 8           | **10** | 8              | 8        | 34/40 ⭐⭐⭐        |
| o3-mini              | **10**      | 3      | 7              | 2        | 22/40 (impractical) |

---

## Tabla 5: Distribución Óptima para 100 Análisis/mes

```
Distribución Propuesta (Escenario Balanceado):

┌─────────────────────────────────────────────┐
│ PRESUPUESTO TOTAL: $10-15/mes               │
└─────────────────────────────────────────────┘

Agente                  | Análisis | Modelo Primary      | Créditos
───────────────────────────────────────────────────────────────
NicheAnalyst           | 15       | Gemini 2.5 Pro (FREE) | 0
LiteratureResearcher   | 20       | Gemini 2.5 Pro (FREE) | 0
FinancialAnalyst       | 15       | GPT-5 (1x)           | 15 ✓
StrategyProposer       | 20       | Haiku 4.5 (0.33x)   | 6.6 ✓
ReportGenerator        | 20       | MiniMax-M2 (FREE)    | 0
OrchestratorAgent      | 10       | Haiku 4.5 (0.33x)   | 3.3 ✓
───────────────────────────────────────────────────────────────
TOTAL                  | 100      | MIXED STACK          | 25 ✓

Créditos Disponibles: 300
Créditos Utilizados: 25
Buffer Disponible: 275 (92%)
```

---

## 📌 CONCLUSIONES DE BENCHMARKS

### 1. Modelos Insustituibles

| Rol                   | Modelo            | Razón                             |
| --------------------- | ----------------- | --------------------------------- |
| Research Long-Context | Gemini 2.5 Pro    | 1M contexto único (gratis)        |
| Math/Finance          | GPT-5             | 95% GSM8K (SOTA)                  |
| SWE-Coding            | Claude Sonnet 4.5 | 77.2% SWE-bench (líder)           |
| Orchestration         | Claude Haiku 4.5  | 600-1000ms latencia (4-5x rápido) |

### 2. Reemplazos Económicos

| Situación                      | En lugar de       | Usar              | Beneficio                    |
| ------------------------------ | ----------------- | ----------------- | ---------------------------- |
| Coding si presupuesto limitado | GPT-5-Codex (1x)  | MiniMax-M2 (0x)   | 90% performance, 100% ahorro |
| Escritura si budget limitado   | Sonnet 4.5 (1x)   | Haiku 4.5 (0.33x) | 80% quality, 67% ahorro      |
| General purpose fallback       | Cualquier premium | GPT-4o (0x)       | Gratis, muy competitivo      |

### 3. Evitar

| Modelo                  | Razón                                                 |
| ----------------------- | ----------------------------------------------------- |
| o3/o3-mini reasoning    | Latencia 3-5s = inutilizable para orchestration       |
| Cursor Pro ($20)        | 2x costo Copilot Pro por menos requests               |
| DeepSeek V3 si critical | Riesgos de seguridad (94% jailbreak success per NIST) |

---

**Generado**: 4 de noviembre de 2025  
**Fuentes**: Perplexity + Gemini + SWE-bench + EvalPlus
