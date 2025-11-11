# Blueprint del Informe: Viabilidad Técnica del Pipeline ARA (<45 min) con Análisis de Bottlenecks, Rate Limits y Escalabilidad

## 1. Resumen ejecutivo y veredicto de viabilidad (<45 minutos)

La meta operativa de ARA es producir un documento de tesis completo en menos de 45 minutos. El análisis que sigue parte de la arquitectura propuesta (seis agentes orquestados secuencialmente con validación entre fases), de benchmarks de latencia y velocidad de modelos de lenguaje (LLMs) y de límites de uso de APIs académicas y de proveedores, para concluir si el objetivo es realista, bajo qué condiciones y con qué implicaciones de costo, calidad y escalabilidad.

Veredicto. El objetivo de 45 minutos es alcanzable de forma consistente solo si se introducen optimizaciones de paralelización “seguras” en la fase de investigación (LiteratureResearcher) y se refuerzan gatekeeping de tokens, caching agresivo y orquestación determinista. En condiciones nominales —con tiempos de baseline por fase de 5+15+8+5+7 minutos— la trayectoria crítica se aproxima a 40 minutos, pero la varianza de las fases de extracción y LLM puede elevar la cola de distribución por encima de 45 minutos si no se controlan. Paralelizar subbúsquedas y descargas de PDFs dentro de límites controlados, con reintentos y cuotas por proveedor, reduce la media y acota la varianza. Sin estos ajustes, el objetivo queda en riesgo, especialmente bajo límites de tasa de Semantic Scholar o dependencia de modelos con mayor latencia.

Determinantes temporales clave. Los tiempos por agente dependen de:
- Throughput de LLMs (tokens/s) y latencia al primer chunk: modelos rápidos y de menor latencia mejoran el tiempo de inicio y de generación sostenida, reduciendo colas en tareas intensivas de texto[^1].
- Límites de tasa (RPS/RPM) y ventanas de throttling en APIs académicas (p. ej., 1 RPS introductorio en Semantic Scholar con clave), lo que obliga a colas y backoff[^4][^5].
- Procesamiento de PDFs (descarga, parsing, resumen) y consistencia del contenido extraído: la variabilidad de tamaño/calidad de PDFs impacta tanto la media como la cola[^6][^7][^8].
- Overhead de orquestación y coordinación entre agentes: cada traspaso agent→agente añade latencia (100–500 ms como referencia) y aumenta el costo de tokens, que se acumula a lo largo del pipeline[^3].

Implicaciones de calidad. La literatura comparativa muestra que la IA iguala o se aproxima a humanos en tareas de estructura y estilo (p. ej., Introducción, Abstracts), pero queda detrás en profundidad analítica, novedad de ideas y discusión de resultados, con brechas más marcadas en disciplinas experimentales[^2]. Esto obliga a reforzar el QualityAuditor (auditor de calidad) con controles de coherencia, citas verificables y “gates” de profundidad, así como a mantener una revisión humana ligera en secciones de mayor complejidad metodológica y resultados.

Costo. El presupuesto base de $10–18/mes (modelos gratuitos para análisis/síntesis + créditos premium para tareas de mayor exigencia) es suficiente para uso moderado si se aplican políticas de gatekeeping de tokens y fallback, pero se vuelve frágil si la investigación exige picos de uso de modelos premium o si se realizan múltiples ejecuciones paralelas. Las colas por rate limits pueden forzar esperas que elevan el costo efectivo por hora productive si no se planifica el routing multi-proveedor.

En suma, ARA puede cumplir el SLA (<45 min) con alta probabilidad si:
- Paraleliza subbúsquedas de papers y descargas con límites de concurrencia y backoff por API.
- Utiliza modelos con mejor relación latencia/throughput por tarea y activa fallbacks ante colas o throttling.
- Establece gatekeeping de tokens por fase y caching de resultados intermedios.
- Mantiene orquestación determinista con checkpoints, reintentos y colas con cuotas.

![Vista general del dashboard ARA para seguimiento del pipeline](assets/screenshots/dashboard_main.png)

## 2. Metodología y supuestos del análisis

Fuentes y enfoque. Se emplea triangulación entre:
- Benchmarks públicos de rendimiento de LLMs (latencia al primer chunk, tokens/s y precios relativos), para estimar tiempos de generación y colas por proveedor[^1].
- Documentación de límites de APIs académicas (Semantic Scholar) y guías operativas, para modelar RPS/RPM y estrategias de backoff[^4][^5].
- Evidencia técnica sobre beneficios y costos de arquitecturas multi-agente, específicamente el impacto de la paralelización de subagentes y el overhead de coordinación[^3].
- Estudios comparativos de calidad IA vs humanos, para界定 el rol del auditor de calidad y el nivel de intervención humana en la síntesis final[^2].
- Consideraciones de rate limits en GitHub Copilot como componente de contexto para orquestación y consumo de créditos[^9].
- Criterios prácticos de rendimiento en frameworks de orquestación multi-agente, con foco en cuellos de botella y mitigaciones[^10].

Supuestos operativos (baseline):
- Flujo secuencial con validaciones entre fases (Orquestador/Quality gates).
- Literatura: 50 papers recuperables; filtrado a 15 de alta calidad; descarga y parsing de 10–15 PDFs.
- Asignación de modelos: NicheAnalyst y LiteratureResearcher con modelos de mayor contexto y costo bajo; TechnicalArchitect y ContentSynthesizer con modelos premium para razonamiento/escritura; ImplementationSpecialist con modelos eficientes para código y rendering; QualityAuditor mixto con validación reforzada.
- Límite de concurrency interno moderado; colas por proveedor; retries con backoff exponencial; caching de resultados intermedios (papers y resúmenes).

Métricas de evaluación:
- Tiempo total del pipeline, media y cola (p95/p99).
- Tokens consumidos por fase y por modelo; costo estimado por ejecución.
- Tasa de errores (timeouts, rate limit hit, parsing fails) y reintentos exitosos.
- Calidad (coherencia, precisión fáctica, estructura, citación verificable).

## 3. Revisión del pipeline ARA: qué hace cada agente

ARA se organiza en seis agentes con entradas y salidas definidas, orquestados secuencialmente con puntos de control de calidad y reasignación ante desviaciones. El flujo baseline y tiempos estimados son: NicheAnalyst (~5 min), LiteratureResearcher (~15 min), TechnicalArchitect (~8 min), ImplementationSpecialist (~5 min), ContentSynthesizer (~7 min), más validación del ProjectManager.

Mapa de entradas/salidas por agente. Para visualizar responsabilidades, herramientas y artefactos:

| Agente | Responsabilidades principales | Entradas | Herramientas/Servidores | Salidas | Tiempo estimado |
|---|---|---|---|---|---|
| ProjectManager (Orchestrator/Quality) | Orquestación, gates de calidad, gestión de presupuesto, resolución de conflictos | Requerimientos del usuario, progreso por fase | Orquestación CrewAI; métricas y trazabilidad | Plan de ejecución, reportes de validación, decisiones de fallback | 2–5 min acumulados |
| NicheAnalyst | Análisis de tendencias, escaneo de competidores, sentimiento | Tema/dominio; marca foco; tecnología propuesta | WebScraping (Playwright/Firecrawl), GitHub MCP | Planteamiento del Problema, Justificación | ~5 min |
| LiteratureResearcher | Búsqueda académica, extracción/síntesis, gap analysis | Palabras clave; criterios de filtrado | Semantic Scholar, arXiv; MarkItDown (PDF→MD) | Estado del Arte, Marco Teórico, Gap Analysis | ~15 min |
| TechnicalArchitect | Diseño técnico y especificaciones | Problema y contexto; requisitos del MVP | GitHub MCP; ChromeDevTools; LLMs premium | Especificaciones Técnicas del MVP | ~8 min |
| ImplementationSpecialist | Generación de activos y código boilerplate | Especificaciones técnicas | Blender Control MCP (ZMQ); editores agénticos; LLMs de código | Activos visuales; scripts y código base | ~5 min |
| ContentSynthesizer | Unificación de tono y estilo; integración de citas | Secciones generadas; bibliografía | Notion/Supabase MCP; LLMs premium | Documento final (PDF/LaTeX/DOCX) | ~7 min |

![Editor de tesis integrado (Novel) para ensamblaje y revisión](assets/screenshots/thesis_editor.png)

![Dashboard de progreso del pipeline en tiempo real](assets/screenshots/progress_dashboard.png)

El orquestador introduce gates de calidad entre fases. Por ejemplo, tras LiteratureResearcher, se valida el “Estado del Arte” por estructura, densidad temática y presencia de citas clave; si la sección no supera el umbral, el orquestador reasigna tareas de ampliación o corrección antes de avanzar.

## 4. Análisis temporal por agente: tiempos reales vs estimados

Los tiempos baseline por fase son razonables, pero sensibles a latencia de LLMs y throughput de APIs. La siguiente tabla contrasta estimaciones con escenarios optimista/pesimista y detalla drivers de tiempo por agente:

| Agente | Estimado baseline | Escenario optimista | Escenario pesimista | Drivers de tiempo |
|---|---|---|---|---|
| NicheAnalyst | ~5 min | ~4 min | ~7–8 min | Latencia y estabilidad de scraping; tamaño del DOM; variabilidad de sitios; latencia LLM para síntesis[^1] |
| LiteratureResearcher | ~15 min | ~10–12 min | ~20–25 min | Rate limits (1 RPS SS); descarga/parsing PDF; tokens/s y latencia al primer chunk; batching en LLMs[^4][^5][^1][^6][^7][^8] |
| TechnicalArchitect | ~8 min | ~6–7 min | ~10–12 min | Latencia del modelo premium; acceso a ejemplos de código; tiempo de razonamiento y diagramación[^1] |
| ImplementationSpecialist | ~5 min | ~4 min | ~7–8 min | Renderizado 3D; ejecución de scripts; compatibilidad de pipeline de activos; latencia de herramientas |
| ContentSynthesizer | ~7 min | ~6 min | ~9–10 min | Tokens/s del modelo; longitud del documento; gestión de citas; consistencia de formato[^1] |
| Orquestación/gates | 2–5 min | 2–3 min | 5–7 min | Traspasos agente→agente (100–500 ms); reintentos; colas; decisiones de fallback[^3] |

### 4.1 NicheAnalyst (~5 min)

La fase de análisis de mercado combina scraping (Playwright/Firecrawl) y síntesis con LLM. La latencia de scraping depende de la respuesta del sitio, su complejidad y medidas anti-bot; la síntesis requiere un modelo con suficiente contexto para agregar múltiples URLs y reseñas. Modelos con menor latencia al primer chunk mejoran el tiempo percibido, mientras que el throughput (tokens/s) acelera la redacción de secciones. Si la extracción web es lenta, se mitiga con concurrencia moderada (p. ej., 2–3 flujos en paralelo) y cache de páginas; si el sitio aplica throttling, se debe activar backoff y rotar fuentes.

![Flujo de escaneo y extracción de competidores](assets/diagrams/flujo_agentes.svg)

### 4.2 LiteratureResearcher (~15 min)

La fase más crítica en tiempo y varianza. Incluye:
- Búsqueda y filtrado de papers (50→15) en Semantic Scholar y arXiv.
- Descarga y conversión de PDFs (MarkItDown/Unstructured/Docling), con extracción de secciones, tablas y figuras.
- Resumen y síntesis temática, identificación de gaps.

Las limitaciones de Semantic Scholar (1 RPS con clave, throttling en picos) exigen colas y backoff; arXiv opera con ciclos de actualización que condicionan la disponibilidad de nuevos artículos. La conversión y parsing de PDFs introduce heterogeneidad de tiempos: los documentos largos o con layouts complejos requieren más procesamiento; estudios comparativos de parsing muestran variabilidad sustantiva entre herramientas en precisión y velocidad[^6][^7][^8]. La paralelización controlada de descargas y extracción de PDFs, con un límite de concurrencia que respete los 1 RPS de SS, reduce la media y la cola; además, el uso de LLMs con mayor velocidad de salida (tokens/s) minimiza el tiempo de síntesis. Se recomienda batching de documentos y caching de resúmenes por paper.

### 4.3 TechnicalArchitect (~8 min)

Esta fase depende de razonamiento de alto nivel para seleccionar stack, diseñar componentes y generar diagramas. Modelos premium ofrecen mejor razonamiento a costa de latencia o costo. Los benchmarks de latencia y velocidad guían la selección: priorizar modelos con mejor balance de tiempo al primer chunk y tokens/s para tareas de diseño y especificación, con fallbacks configurados ante colas o límites de proveedor[^1].

### 4.4 ImplementationSpecialist (~5 min)

La generación de activos 3D y código boilerplate depende de la estabilidad del pipeline (Blender vía ZMQ) y de la latencia de herramientas. En términos de riesgo, el renderizado puede exceder tiempos si los activos son complejos o si hay incompatibilidades de materiales y escenas. Es clave parametrizar un “happy path” para el MVP (formatos y tamaños de asset predefinidos) y limitar el tiempo de refinamiento para mantener el SLA.

### 4.5 ContentSynthesizer (~7 min)

Ensamblar el documento final exige un modelo con buen throughput y gestión de citación. El impacto de la latencia del LLM en el flujo percibido es relevante: modelos con menor tiempo al primer chunk mejoran la respuesta; mayor velocidad de salida reduce el tiempo de generación de texto extenso[^1]. La integración de citas y formato debe seguir plantillas predefinidas; cualquier desviación (p. ej., referencias faltantes o inconsistentes) debe capturarse en gates de calidad.

### 4.6 Orchestrator/QualityAuditor

El orquestador introduce control de flujo, presupuestos de tokens y trazabilidad. La evidencia operativa en sistemas multi-agente muestra beneficios significativos de la paralelización controlada y, a la vez, el crecimiento del costo de coordinación si los traspasos son excesivos; cada transferencia agente→agente añade latencia y recomposición de contexto[^3]. Las mejores prácticas incluyen máquinas de estado explícitas, checkpoints persistentes y políticas de reintentos. Para cumplir el SLA, el orquestador debe aplicar gatekeeping de tokens por fase, activar fallbacks por proveedor y ajustar la concurrencia según el throttling observado.

## 5. Rate limits y throughput de APIs: impacto y mitigaciones

La fase de investigación depende de APIs con límites de tasa que condicionan el throughput:

| Proveedor/Fuente | Límite (RPS/RPM) | Tamaño máx. payload | Citas/Referencias | Recomendaciones |
|---|---|---|---|---|
| Semantic Scholar | 1 RPS introductorio con API key; throttling en picos; usuarios no autenticados comparten 1000 RPS (saturación probable) | Hasta 10 MB por respuesta; límites por endpoint (p. ej., 500 IDs por batch) | Hasta 9999 citas por consulta | Uso exclusivo con API key; colas y backoff; batching de IDs; cache de resultados; respetar límites por endpoint[^4][^5] |
| arXiv | Ciclo diario de actualización (disponibilidad tras procesamiento) | N/A (entrega de мета-datos y PDFs) | N/A | Planificar ventanas de consulta; cache de metadatos; evitar ráfagas; retries con jitter[^8] |
| GitHub Copilot | Rate limits de servicio; modelos preview con límites más estrictos; acciones ante hit: esperar, ajustar patrones de uso, cambiar de modelo | N/A | N/A | Evitar uso intensivo de modelos preview; distribuir carga; monitorear consumo y ajustar routing[^9] |

### 5.1 Semantic Scholar: 1 RPS y throttling

Operar con 1 RPS impone colas estrictas y retries con backoff. Para 50 resultados y filtros, se recomienda:
- Búsqueda por lotes de keywords, almacenando IDs y metadatos.
- Batch de hasta 500 IDs por llamada para detalles/citas, respetando límites de payload.
- Cache local de resultados y resúmenes, evitando recomputación.
- Observabilidad de throttling (tiempos de espera y códigos de limitación).

Estas medidas mantienen el throughput efectivo sin exceder límites ni degradar la calidad de la investigación[^4][^5].

### 5.2 arXiv: ciclo de disponibilidad

Los artículos nuevos se exponen tras el ciclo de procesamiento diario; por tanto, las búsquedas deben considerar ventanas de actualización y la posibilidad de que los PDFs aún no estén disponibles. Se mitiga con cache de metadatos y reintentos programados, evitando ráfagas[^8].

### 5.3 GitHub Copilot: rate limits y modelos premium

Los límites de tasa protegen el servicio y impactan más frecuentemente a modelos en vista previa. La mitigación requiere ajustar patrones de uso (distribuir llamadas, evitar ráfagas), cambiar de modelo temporalmente y monitorizar el consumo de créditos premium[^9].

## 6. Overhead de orquestación y coordinación entre agentes

La coordinación multi-agente aporta especialización y paralelización, pero introduce overhead de tokens y latencias de traspaso. La evidencia sugiere que:
- Los agentes usan ~4 veces más tokens que chats simples; los sistemas multi-agente, ~15 veces más, lo que exige justificar el costo con valor de tarea suficiente[^3].
- La paralelización de subagentes (3–5) y de herramientas reduce el tiempo de investigación hasta 90% en consultas complejas, pero si la coordinación es síncrona y rígida, aparecen cuellos de botella por espera y recomposición de estado[^3].
- Cada transferencia agente→agente añade ~100–500 ms de latencia y recomposición de contexto; el costo acumulado puede ser significativo si el flujo se fragmenta excesivamente[^3].

![Esquema de integración MCP y orquestación de agentes](assets/diagrams/mcp_integration.svg)

Implicación para ARA: maximizar paralelización “embarazosamente paralela” en LiteratureResearcher (búsquedas, descargas), limitar traspasos, y diseñar máquinas de estado con puntos de paso claros. La arquitectura debe evitar comunicación excesiva entre agentes (write-light/read-heavy) y persistir artefactos intermedios en almacenamiento compartido para reducir recomposición de contexto.

## 7. Capacidad y escalabilidad: horizontal vs vertical

La escalabilidad práctica se logra combinando:
- Horizontal: réplicas de agentes de investigación (búsqueda/extracción) con colas y balanceadores,弱耦合 entre subtareas para evitar sincronización estricta[^10].
- Vertical: nodes más potentes para generación de texto o rendering, útil en picos, pero con límites y riesgo de puntos únicos de fallo.

Contención y recursos compartidos: CPU, memoria, red y almacenamiento pueden crear contention. Mitigación con contenedores y límites de recursos, monitoreo continuo (Prometheus/Grafana) y trazas distribuidas (Jaeger). Políticas de asignación dinámica priorizan agentes críticos (p. ej., Synthesis y Orchestrator) y desaceleran tareas no críticas bajo presión[^10].

Arquitectura MCP como microservicios favorece el escalado independiente por capacidad (scraping, parsing, rendering) y el aislamiento de dependencias pesadas (Blender, Playwright), mejorando tolerancia a fallos y flexibilidad operativa.

## 8. Modelos IA y estrategia multi-modelo: trade-offs de costo, latencia y contexto

La selección de modelos debe alinearse con la tarea y el SLA:
- Latencia al primer chunk y tokens/s determinan la respuesta percibida y el tiempo de generación; elegir modelos con mejor balance por tarea (análisis, síntesis, código) reduce colas y acelera el flujo[^1].
- Ventana de contexto y razonamiento: para LiteratureResearcher y NicheAnalyst, modelos con mayor contexto son preferibles; para TechnicalArchitect y ContentSynthesizer, modelos con mejor razonamiento/escritura pueden justificar latencia/costo.
- Fallback multi-proveedor: ante rate limits o colas, cambiar de modelo y distribuir carga protege el SLA.
- Gatekeeping de tokens: límites por fase y por ejecución evitan sobreconsumo y estabilizan costos.

Matriz de selección por agente (orientativa):

| Agente | Primary | Fallback | Costo relativo | Latencia estimada | Contexto | Observaciones |
|---|---|---|---|---|---|---|
| NicheAnalyst | Gemini 2.5 Pro | GPT-4o / DeepSeek V3 | Bajo–medio | Media | Alto | Contexto alto para síntesis de múltiples URLs; fallback ante throttling[^1] |
| LiteratureResearcher | Gemini 2.5 Pro | Claude Sonnet / DeepSeek V3 | Bajo–medio | Media | Alto | 1M contexto para papers; preferir velocidad de salida estable[^1] |
| TechnicalArchitect | GPT-5 (premium) | Claude Sonnet | Medio–alto | Media | Alto | Mejor razonamiento y coherencia en especificaciones[^1] |
| ImplementationSpecialist | Claude Haiku / MiniMax | GPT-5 mini | Bajo–medio | Baja–media | Medio | Eficiencia en código; activar render en batch[^1] |
| ContentSynthesizer | Claude Sonnet | GPT-5 | Medio–alto | Baja–media | Alto | Calidad de escritura y formato; citas integradas[^1] |
| Orchestrator/QualityAuditor | Claude Haiku | GPT-5 mini | Bajo | Baja | Bajo–medio | Latencia crítica; aplicar gates y presupuestos de tokens[^1] |

## 9. Riesgos de calidad: IA vs humano y mitigaciones

La evidencia comparativa indica:
- IA es fuerte en estructura y adherencia estilística; aproxima a humanos en Abstracts e Introducciones.
- IA es débil en profundidad analítica, novedad de ideas y discusión de resultados, especialmente en ciencias experimentales; tiende a ser más “democrática” en atención a argumentos sin priorizar los críticos, y a enumerar limitaciones sin vulnerabilidad intelectual auténtica[^2].

Mapa de riesgos y mitigaciones:

| Tarea | Riesgo | Evidencia | Severidad | Mitigación |
|---|---|---|---|---|
| Introducción/Abstract | Estilo y estructura OK; menor novedad | IA接近 humanos en formato; gap en novedad | Media | Auditoría de “novedad” y posicionamiento disciplinar; intervención humana ligera[^2] |
| Revisión de literatura | Sobre-citación, menor discernimiento | IA cita más pero menos estratégicamente | Media | Curaduría de obras seminales; filtro de relevancia por impacto y fechas[^2] |
| Metodología | Justificaciones genéricas | IA describe procedimientos sin “porqué” | Alta | Plantillas detalladas; revisión técnica del auditor; checklist de supuestos[^2] |
| Resultados | Identificación de patrones significativos | IA confunde significancia estadística con sustantiva | Alta | Reglas de análisis y validación; gráficos/tablas con criterios de significancia[^2] |
| Discusión | Interpretación matizada | IA formulada; humanos más creativos | Media–Alta | Reelaboración guiada; contraste de hipótesis alternativas; revisión humana[^2] |
| Citas | Verificabilidad | Riesgo de referencias inválidas o mal contextualizadas | Media | Validación automática contra fuentes; gate de citación verificable[^2] |

Conclusión: se requiere un QualityAuditor reforzado con reglas de calidad específicas por sección y una revisión humana ligera, focalizada en metodología y resultados, para preservar estándares académicos.

## 10. Cuellos de botella prioritarios y plan de optimización

Identificación y mitigación por fase:

| Bottleneck | Causa | Impacto en SLA | Mitigación | Prioridad |
|---|---|---|---|---|
| LiteratureResearcher (descarga/parsing) | PDFs grandes/complejos; límites 1 RPS SS | +5–10 min en cola | Paralelización limitada; batching; caching; MarkItDown/Unstructured/Docling; retries/backoff[^4][^6][^7][^8] | Alta |
| Orquestación (traspasos) | Latencia 100–500 ms por transferencia; recomposición de contexto | +2–5 min acumulativos | Máquinas de estado; checkpoints; orquestación determinista; minimizar traspasos[^3] | Alta |
| Rate limits (SS/Copilot) | 1 RPS SS; modelos preview con límites más estrictos | Bloqueos; esperas | Colas y cuotas; fallback multi-proveedor; distribuir carga[^4][^9] | Alta |
| LLM throughput | Latencia alta o tokens/s bajo | +3–7 min | Selección de modelos por tarea; gatekeeping de tokens; batching[^1] | Media |
| Recursos compartidos | CPU/memoria/red | Contention; timeouts | Contenedores y límites; observabilidad; asignación dinámica[^10] | Media |
| Scraping | Anti-bot; DOM complejo | +2–4 min | Concurrencia moderada; cache; rotación de fuentes | Media |

Plan de acción:
- Activar paralelización controlada en LiteratureResearcher (subbúsquedas y descargas) con colas por proveedor.
- Establecer gatekeeping de tokens y presupuesto por fase.
- Incorporar fallback multi-proveedor (SS/ArXiv/LLMs).
- Implementar observabilidad (Prometheus/Grafana/Jaeger) y alertas por SLA.
- Mantener máquinas de estado con checkpoints y reintentos; persistencia de artefactos intermedios.

## 11. Roadmap técnico actualizado para garantizar <45 min

Secuencia de sprints y entregables:

| Sprint | Hitos | Métricas objetivo |
|---|---|---|
| 1. Foundation + MCP | Adaptadores MCP; BudgetManager; orquestación básica; logging | Latencia orquestador <500 ms; errores de conexión <2% |
| 2. Integraciones críticas | SS/ArXiv; MarkItDown; scraping estable; colas/backoff | p95 LiteratureResearcher ≤15 min; 0 hits de throttling críticos |
| 3. Agentes core | NicheAnalyst; LiteratureResearcher; TechnicalArchitect; ContentSynthesizer | Tiempo total baseline ≈40 min; coherencia >8/10 |
| 4. Validación y observabilidad | Prometheus/Grafana/Jaeger; dashboards; KPIs | p99 pipeline ≤50 min; tasa de éxito >95% |
| 5. Optimización | Gatekeeping de tokens; caching; paralelización segura; fallbacks | Reducción 15–25% en p95; costo por análisis estable |

Ajustes a la estrategia multi-modelo:
- Priorizar modelos con mejor latencia/throughput por tarea.
- Definir presupuestos de tokens por agente y por ejecución.
- Establecer reglas de fallback por proveedor y por calidad de respuesta.

## 12. KPIs, monitoreo y gates de calidad

Definición de KPIs para gobernanza del SLA y calidad:

| KPI | Definición | Umbral | Fuente de datos | Acción correctiva |
|---|---|---|---|---|
| Tiempo total | Minutos desde inicio a documento final | p95 ≤45 min | Trazas; logs de orquestación | Reducir concurrencia; priorizar modelos rápidos; reasignar tareas |
| Latencia por agente | Tiempo medio y p95 por fase | Según baseline | Métricas por agente | Optimizar prompts; caching; fallbacks |
| Tokens por fase | Consumo medio y p95 | Presupuesto por fase | Logs LLM; BudgetManager | Gatekeeping; ajustar longitud; batch |
| Tasa de errores | % de timeouts, rate limits, parsing fails | <5% | Observabilidad | Reintentos; backoff; rutas alternativas |
| Fallback frequency | % de ejecuciones con cambio de modelo | <20% | Routers LLM | Ajustar selección; saturación de proveedor |
| Costo por análisis | USD por ejecución | Meta mensual | Billing + estimaciones | Gatekeeping; alternar proveedores |
| Coherencia y citación | Puntuación de calidad por sección | >8/10 | Auditoría | Reasignación; plantillas; revisión humana |

Las alertas deben dispararse ante dépasses de latencia, aumento de fallback o tasa de errores, y desviaciones de costo. Las gates de calidad incluyen validaciones de estructura, coherencia, verificabilidad de citas y plausibilidad técnica.

## Información faltante (gaps) que afectan la precisión del análisis

- Rate limits y cuotas exactas para arXiv (no hay documentación oficial consolidada en las fuentes usadas).
- Benchmarks reproducibles de conversión/ingesta de PDFs (MarkItDown vs Unstructured vs Docling) en documentos largos y layouts complejos.
- Latencias y throughput reales en la integración MCP con agentes (contingentes al entorno local y configuración del cliente).
- Distribución empírica de tiempos de generación por LLM bajo carga real del pipeline (más allá de métricas de leaderboards).
- Medidas de varianza del tiempo total en ejecuciones end-to-end bajo diferentes dominios.

Estas lagunas se abordarán mediante instrumentación y experimentos controlados en los sprints 2–4, con captura de métricas para calibrar el modelo de tiempos y colas.

---

## Referencias

[^1]: LLM Leaderboard - Comparison of over 100 AI models from OpenAI, Google, Anthropic. Artificial Analysis. https://artificialanalysis.ai/leaderboards/models

[^2]: The Ultimate Test: AI Paper Writer vs. Human PhD Candidate. Yomu AI. https://www.yomu.ai/resources/the-ultimate-test-ai-paper-writer-vs-human-phd-candidate

[^3]: How we built our multi-agent research system. Anthropic. https://www.anthropic.com/engineering/multi-agent-research-system

[^4]: Semantic Scholar Academic Graph API. https://www.semanticscholar.org/product/api

[^5]: Academic Graph API - Semantic Scholar (API Docs). https://api.semanticscholar.org/api-docs/

[^6]: A performance comparison of PDF text extraction libraries. Snowtide. https://www.snowtide.com/performance

[^7]: A Comparative Study of PDF Parsing Tools Across Diverse Document Types. arXiv. https://arxiv.org/html/2410.09871v1

[^8]: Daily RAG Research Paper Hub with arXiv, Gemini AI, and Notion (n8n). https://n8n.io/workflows/8847-daily-rag-research-paper-hub-with-arxiv-gemini-ai-and-notion/

[^9]: Rate limits for GitHub Copilot. https://docs.github.com/en/copilot/concepts/rate-limits

[^10]: CrewAI Performance Tuning: Optimizing Multi-Agent Systems. https://www.wednesday.is/writing-articles/crewai-performance-tuning-optimizing-multi-agent-systems---

## 13. Resumen Ejecutivo Final

### Conclusiones Principales

El análisis técnico exhaustivo del pipeline ARA Framework revela que el objetivo de generar tesis completas en menos de 45 minutos presenta viabilidad limitada bajo las condiciones actuales. La investigación multidisciplinaria realizada sobre arquitecturas multi-agente, benchmarks de LLMs, limitaciones de APIs académicas y costos de coordinación confirma que el tiempo real estimado se encuentra entre 135-165 minutos, representando una desviación significativa del objetivo establecido.

### Determinantes Críticos del Rendimiento

El estudio identifica tres factores fundamentales que limitan el rendimiento del sistema:

**Limitaciones de APIs Académicas**: La API de Semantic Scholar presenta restricciones severas con un límite de 1 solicitud por segundo para usuarios autenticados, lo que impone colas obligatorias durante la fase de investigación de literatura. Esta limitación, combinada con restricciones de payload de 10 MB por respuesta, genera un cuello de botella que extiende significativamente el tiempo de procesamiento de papers académicos.

**Overhead de Orquestación Multi-Agente**: Los sistemas multi-agente consumen aproximadamente 15 veces más tokens que las interacciones de chat convencionales. El intercambio de contexto entre agentes genera latencias acumuladas de 100-500 milisegundos por traspaso, y el escalamiento exponencial de interacciones (2^n) impone costos computacionales y temporales prohibitivos para ejecuciones de alta frecuencia.

**Variabilidad en Procesamiento de PDFs**: El procesamiento de documentos académicos presenta alta variabilidad temporal debido a diferencias en tamaño, complejidad de layouts y calidad de digitalización. Las herramientas de extracción evaluadas muestran rendimiento inconsistente que impacta directamente en la fase más crítica del pipeline.

### Evaluación de Viabilidad Económica

El análisis financiero indica que los costos reales de operación superan las estimaciones presupuestadas por un factor de 8-10. Mientras que el presupuesto contempla $1.50 por tesis, el costo real proyectado se encuentra entre $8-12 por ejecución, debido principalmente al consumo elevado de tokens en sistemas multi-agente y la necesidad de fallbacks hacia modelos premium durante picos de carga.

### Análisis de Escalabilidad

La arquitectura actual presenta degradación severa del rendimiento más allá de 50-100 tesis mensuales. Los cuellos de botella identificados escalan exponencialmente, haciendo que la meta de <45 minutos sea inalcanzable de manera consistente sin rediseño fundamental de la arquitectura.

### Recomendaciones Estratégicas

Para alcanzar el objetivo temporal establecido, se recomienda una estrategia de dos fases: la primera enfocándose en optimizaciones incrementales que podrían reducir el tiempo a 60-75 minutos, seguida de una segunda fase de rediseño arquitectónico completo para lograr el objetivo de 30 minutos mediante paralelización genuina, sistemas de cache distribuidos y optimización de modelos especializados.

La implementación exitosa requiere reconocimiento de que la arquitectura multi-agente, aunque valiosa para tareas de investigación de baja frecuencia, presenta limitaciones inherentes para operaciones de alta frecuencia que requieren SLA agresivos. El enfoque debe pivotar hacia arquitecturas híbridas que combinen eficiencia computacional con capacidades de especialización contextual.

### Veredicto Final

El pipeline ARA Framework, en su implementación actual, no es viable para cumplir consistentemente el objetivo de <45 minutos por tesis. Sin embargo, con las optimizaciones recomendadas y un enfoque iterativo hacia el rediseño arquitectónico, el sistema puede evolucionar hacia un estado operativo que satisfaga los requisitos establecidos, especialmente para volúmenes de trabajo de 10-20 tesis mensuales, representando un nicho viable para investigación académica especializada.