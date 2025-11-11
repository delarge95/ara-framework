# Validación y Optimización del Core Tech Stack de ARA Framework (Python 3.11+, FastAPI, Playwright, Unstructured.io) con enfoque en costo/beneficio

## Resumen ejecutivo

ARA Framework ha evolucionado hacia una arquitectura de tres capas que combina orquestación multi‑agente (CrewAI), microservicios de herramientas expuestos por FastAPI y un ecosistema de servidores MCP ya instalados en el entorno de desarrollo. El stack propuesto, centrado en Python 3.11+, FastAPI, Playwright y Unstructured.io, es técnicamente sólido y opera con licenciamiento abierto, permitiendo optimización de costos mediante ejecución autosuficiente y uso estratégico de modelos de lenguaje (LLMs) con planes gratuitos o de bajo costo. Este informe valida la compatibilidad del stack, compara alternativas relevantes y plantea una estrategia de costos que prioriza autoservicio, concurrencia eficiente y proxies de scraping gestionados solo cuando sea imprescindible.

Las conclusiones principales son:

- CrewAI se mantiene como elección principal para orquestación por su orientación a roles y flujos estructurados. AutoGen es idóneo para prototipado conversacional y LangGraph sobresale en escenarios con estado y control de grafos; OpenAI Swarm, por su naturaleza experimental, no es recomendable para producción[^5][^6][^7][^8][^9].
- FastAPI es superior a Flask para microservicios MCP por su soporte asíncrono nativo, validación con Pydantic y auto‑documentación, lo que mejora la concurrencia en cargas I/O intensivas y reduce tiempos de ciclo. En escenarios con concurrencia moderada y equipos less‑experienced, Flask puede servir como fallback pragmático[^1][^2][^10].
- Playwright debe ser el estándar para scraping y automatización moderna frente a Selenium y Puppeteer. Su ergonomía async, auto‑waiting y soporte multi‑navegador lo hacen más robusto en SPAs. Los costos de operación se controlan combinando autoservicio con proxies/stealth gestionados en sitios difíciles[^3][^4].
- En procesamiento de PDFs, Unstructured.io ofrece valor diferencial para RAG por sus fragmentos semánticos; sin embargo, PyMuPDF (pymupdf4llm) y pdfplumber son superiores en velocidad y tablas respectivamente. marker‑pdf puede ser útil en conversiones de alta fidelidad. Docling y Unstract son alternativas open‑source viables para reducir costos de servicios gestionados[^11][^12][^13][^14][^15][^16][^17].
- Para la capa 3D, la combinación Blender + pyzmq es adecuada para control headless, y TripoSR permite reconstrucción 3D desde una imagen con requisitos GPU modestos; en cargas intensivas o por lotes, conviene evaluar infraestructura GPU en la nube. Open3D y trimesh complementan como librerías de geometría[^18][^19][^20][^21][^22].
- La compatibilidad con Python 3.11+ es adecuada en FastAPI y el ecosistema propuesto. El impacto en costo/beneficio proviene principalmente de reducir tiempos de espera con async/await, contratos de datos explícitos y scrapers robustos que disminuyen retrabajos[^1][^2].
- El modelo de licencias y precios muestra que CrewAI (OSS sin costo de licencia) y las bibliotecas OSS propuestas evitan costos de software. Las palancas de ahorro están en autoservicio (PDF/3D), uso de Playwright autoservicio, optimizaciones headless y selección de LLMs con planes gratuitos, reservando modelos premium solo para tareas críticas[^23].
- Los riesgos operativos incluyen bloqueo de proveedores, anti‑bot en scraping, colas de trabajo pesadas y variabilidad de latencias LLM. Se mitigan mediante proxies rotativos y stealth, caching/redis, desacoplamiento por colas, colas de trabajo y observabilidad con conteo de tokens y límites de presupuesto por agente.

Recomendación: mantener el stack propuesto (CrewAI + FastAPI + Playwright + Unstructured.io), con una estrategia de autoservicio y uso selectivo de servicios gestionados. Adoptar Unstructured.io para pipelines RAG y usar pymupdf4llm para velocidad y pdfplumber para tablas; mantener Playwright en scraping y habilitar proxies/stealth solo para sitios difíciles. Integrar Blender + pyzmq y TripoSR bajo demanda con dimensionamiento GPU adecuado.

## Contexto, alcance y metodología

El alcance de esta validación cubre los componentes core de ARA: orquestación multi‑agente (CrewAI), framework de APIs (FastAPI), automatización/scraping (Playwright) y procesamiento de documentos (Unstructured.io), además de la capa 3D (Blender + pyzmq y TripoSR). Se evalúan compatibilidad con Python 3.11+, escalabilidad en concurrencia, costo/beneficio y riesgos operativos. Se usan benchmarks reconocidos (por ejemplo, TechEmpower para frameworks web) y comparativas actualizadas 2025 en scraping y parsing de documentos. Las recomendaciones se apoyan en documentación oficial de los proyectos y fuentes públicas de la comunidad técnica[^2].

Para clarificar los criterios de evaluación, la siguiente matriz resume dimensiones y métricas aplicables.

Tabla 1. Matriz de criterios de evaluación
| Criterio             | Definición                                                                 | Métricas principales                                      | Fuentes de evidencia                                     |
|----------------------|-----------------------------------------------------------------------------|-----------------------------------------------------------|----------------------------------------------------------|
| Compatibilidad       | Soporte y estabilidad en Python 3.11+                                       | Versionado, issues, changelogs                            | Documentación oficial FastAPI, CrewAI[^1][^9][^10]       |
| Rendimiento          | Throughput/latencia en cargas I/O y paralelización                         | RPS, TTFB, p95 latency                                    | TechEmpower, comparativas FastAPI vs Flask[^1][^2]       |
| Escalabilidad        | Concurrencia y patrones asíncronos                                          | Conexiones concurrentes, backpressure                     | FastAPI docs, guías async[^1][^10]                       |
| Costo/beneficio      | Infraestructura, licencias, tiempo de desarrollo                            | Coste infra/mensual, horas dev, licencias                 | Páginas de pricing y artículos técnicos[^1][^3][^23]     |
| Mantenibilidad       | Madurez del ecosistema, tooling, comunidad                                  | Stars, releases, extensibilidad                           | Comparativas frameworks y repositorios[^5][^8][^9]       |
| Riesgos operativos   | Bloqueo proveedor, anti‑bot, colas, latencias LLM                           | Incidencias, mitigaciones, planes de contingencia         | Guías scraping, benchmarks LLM, prácticas ARA[^3][^4][^24] |

## Orquestación multi‑agente: CrewAI vs AutoGen vs LangGraph vs OpenAI Swarm

La capa de orquestación define cómo se estructuran los equipos de agentes, su estado y los flujos de trabajo. CrewAI se alinea con el enfoque de “roles + procesos” que favorece flujos secuenciales y reproducibilidad, adecuado para la generación de documentos complejos como tesis. AutoGen sobresale en prototipado rápido mediante conversaciones multi‑agente y es útil cuando la interacción flexible es central. LangGraph aporta control granular de estado y grafos, apropiado para workflows con memoria persistente y requerimientos de control a bajo nivel. OpenAI Swarm prioriza la simplicidad y la transparencia, pero su estado experimental y naturaleza sin estado lo vuelven poco recomendable para producción[^5][^6][^7][^8][^9].

Desde la perspectiva de ARA, donde cada agente tiene un rol especializado (por ejemplo, NicheAnalyst o LiteratureResearcher), CrewAI facilita definir procesos con calidad y gates de validación, mapeando claramente herramientas MCP por agente. AutoGen y LangGraph son alternativas complementarias: el primero para iteraciones conversacionales, el segundo para casos con estado y DAGs complejos. Swarm, al ser experimental, no debería emplearse en escenarios que requieren garantías de producción[^5][^6][^7][^8].

Tabla 2. Comparativa de frameworks multi‑agente
| Dimensión              | CrewAI                              | AutoGen                                | LangGraph                              | OpenAI Swarm                    |
|------------------------|-------------------------------------|----------------------------------------|----------------------------------------|---------------------------------|
| Modelo                 | Roles y equipos                     | Conversacional                         | Grafos con estado                      | Funciones y handoffs            |
| Estado                 | Gestión por procesos                | Conversaciones                         | Persistencia y control granular        | Sin estado entre llamadas       |
| Determinismo           | Alto (flujos secuenciales)          | Medio (depende de conversación)        | Alto (control de grafos)               | Bajo (experimental)             |
| Personalización        | Alta (herramientas por rol)         | Alta (APIs versátiles)                 | Muy alta (bajo nivel)                  | Limitada                        |
| Escalabilidad          | Diseñado para escalar               | Escala con diseño en capas             | Escala con estado y DAGs               | Limitada/incierta               |
| Preparación producción | Alta (OSS estable)                  | Alta (OSS, soporte MS)                 | Alta (OSS y opciones comerciales)      | Baja (experimental)             |

Conclusión: mantener CrewAI como orquestador principal, con AutoGen y LangGraph como alternativas contextuales para prototipado y flujos con estado. Evitar Swarm en producción[^5][^6][^7][^8].

### Análisis de costos de orquestación

CrewAI en su modalidad OSS no tiene costo de licencia; los costos se concentran en el uso de LLMs y la infraestructura de ejecución. La plataforma AMP ofrece planes con ejecución en la nube y beneficios operativos, pero el autoservicio con OSS reduce significativamente el costo directo. La comunidad confirma que CrewAI es open source bajo licencia permisiva, con costos separados de modelos y servicios asociados[^23][^25].

Tabla 3. CrewAI: OSS vs AMP (Basic/Professional/Enterprise)
| Modalidad       | Costo            | Capacidades clave                                                                 | Consideraciones de uso                                   |
|-----------------|------------------|-----------------------------------------------------------------------------------|----------------------------------------------------------|
| OSS (autoservicio) | $0 de licencia | Framework OSS, construcción de crews y procesos, integración con herramientas     | Pago solo por LLM/infra; control total on‑prem/cloud     |
| AMP Basic       | Gratis           | Editor visual, triggers, tracking, export MCP, métricas                           | Cuotas de ejecución incluidas (limitadas)                |
| AMP Professional| $25/mes          | Despliegues y ejecución con cuotas y precio por ejecución adicional               | Adecuado para equipos que requieren plataforma gestionada |
| Enterprise      | Personalizado    | SSO, RBAC, VPC dedicada, soporte y formación in situ                              | Para organizaciones que necesitan cumplimiento y soporte  |

Estrategia recomendada: quedarse en OSS mientras se controllinga el gasto por LLM y se mantenga control sobre datos y despliegue. Considerar AMP solo si los beneficios operativos compensan el costo incremental[^23][^25].

## Framework de API y microservicios: FastAPI (comparado con Flask/Quart)

FastAPI, construido sobre ASGI con soporte asíncrono nativo, ofrece contratos de datos explícitos vía Pydantic, validación automática y documentación OpenAPI generada. En cargas con alta concurrencia o llamadas a terceros, su arquitectura no bloqueante se traduce en mayor throughput y menor latencia. Comparativas públicas muestran rangos de rendimiento muy superiores a Flask en escenarios I/O‑intensivos, aunque en cargas mixtas la base de datos suele ser el cuello de botella[^1][^2][^10].

Para microservicios MCP, donde cada endpoint orquesta scraping, ingestión de PDFs o control de Blender, la asincronía y la validación de tipos son ventajas tangibles: reducen errores, acortan tiempos de respuesta y simplifican pruebas. Flask y Quart tienen cabida en escenarios más simples o equipos con menor experiencia en async, pero en el contexto de ARA —donde la paralelización es clave— FastAPI es la elección correcta[^1][^10].

Tabla 4. FastAPI vs Flask vs Quart
| Aspecto                  | FastAPI                             | Flask                              | Quart                               |
|--------------------------|-------------------------------------|------------------------------------|-------------------------------------|
| Concurrencia             | ASGI nativo, async/await            | WSGI síncrono                      | ASGI (compatible con async)         |
| Rendimiento (I/O)        | 15k–20k RPS (indicativo)            | 2k–3k RPS (indicativo)             | Competitivo con FastAPI             |
| Validación de datos      | Pydantic integrado                   | Manual con librerías externas      | Manual o addons                     |
| Documentación            | Swagger/ReDoc automáticos            | Requiere extensiones               | Requiere extensiones                |
| Curva de aprendizaje     | Moderada (tipado/async)             | Baja (síncrono, simple)            | Moderada (ASGI)                     |
| Ecosistema               | En crecimiento, tooling moderno     | Muy maduro, amplio                 | Menor que Flask                     |

Recomendación: mantener FastAPI para microservicios MCP; usar Flask/Quart solo como fallback táctico en endpoints muy simples o con restricciones de equipo[^1][^2][^10].

## Web scraping y automatización: Playwright vs Selenium vs Puppeteer

Playwright ofrece APIs asíncronas, auto‑waiting inteligente, soporte multi‑navegador y un modelo de contexto que mejora la estabilidad en sitios con JavaScript moderno. En scraping de SPAs, esto se traduce en menos flaky tests y mayor eficiencia. Selenium mantiene compatibilidad con ecosistemas amplios, pero su ergonomía y desempeño en SPAs son inferiores; Puppeteer, centrado en Chrome, es sólido pero menos versátil en navegadores y soporte de lenguajes[^3][^4].

Los costos de scraping provienen de infraestructura de navegadores headless, proxies, rotación de IPs y mitigación anti‑bot. La estrategia recomendada es operar en autoservicio siempre que sea posible, aplicar técnicas de stealth y activar proxies gestionados solo cuando el sitio objetivo lo exija. La diferencia de productividad con Playwright reduce horas de mantenimiento y retrabajo, aportando un mejor costo total de operación[^3][^4].

Tabla 5. Playwright vs Selenium vs Puppeteer
| Criterio             | Playwright                                  | Selenium                                     | Puppeteer                         |
|----------------------|----------------------------------------------|----------------------------------------------|-----------------------------------|
| Rendimiento          | Alto en SPAs, contextos eficientes           | Sólido, más propenso a flakiness en SPAs     | Alto en Chrome                    |
| Soporte de navegadores| Chromium, Firefox, WebKit                   | Amplio (multi‑navegador)                     | Principalmente Chrome             |
| APIs                 | Async/await, auto‑waiting, test API         | Síncrono, amplio ecosistema                   | Nativa Chrome, buen API           |
| Escalabilidad        | Elevada en contenedores y CI/CD              | Amplia, pero más trabajo de tuning            | Buena, limitada a Chrome          |
| Costos operativos    | Optimizables con autoservicio y stealth      | Similar; más horas de mantenimiento           | Similar; menor flexibilidad       |

Recomendación: estandarizar Playwright y reservar Selenium/Puppeteer para casos específicos o compatibilidad legacy[^3][^4].

## Procesamiento de documentos (PDF) y extracción de texto

La elección del extractor de PDFs afecta calidad de fragmentación, velocidad y dependencia de herramientas externas. Unstructured.io aporta fragmentos semánticos (Title, NarrativeText) ideales para pipelines RAG. PyMuPDF (pymupdf4llm) destaca por velocidad y produce Markdown limpio con jerarquía adecuada. pdfplumber sobresale en tablas y extracción basada en coordenadas. marker‑pdf ofrece máxima fidelidad de diseño, aunque con mayor latencia por modelos de visión. Como alternativas open‑source, Docling y Unstract reducen dependencia de servicios gestionados y permiten ejecución autosuficiente[^11][^12][^13][^14][^15][^16][^17].

Estrategia recomendada: usar Unstructured para RAG y análisis semántico; pymupdf4llm para volúmenes altos donde la velocidad es crítica; pdfplumber para casos con tablas complejas; marker‑pdf en conversiones de alta fidelidad. Considerar Docling/Unstract como opciones autoservicio para reducir costos operativos[^11][^12][^13][^14][^15][^16][^17].

Tabla 6. Benchmarks comparativos (PDFs de una página)
| Extractor        | Velocidad        | Calidad de texto            | Tablas                   | Dependencias              | Caso ideal                                |
|------------------|------------------|-----------------------------|--------------------------|--------------------------|-------------------------------------------|
| pypdfium2        | ~0.003s          | Texto limpio, sin estructura | No preserva estructura   | Binarios PDFium          | Volumen, indexación rápida                |
| pypdf            | ~0.024s          | Sólida, spacing ocasional   | Foco en texto            | Pura Python              | Funciones serverless/containers           |
| pdfplumber       | ~0.10s           | Requiere ajuste             | Buena, por coordenadas   | Dependencias de layout   | Tablas complejas                           |
| pymupdf4llm      | ~0.12s           | Markdown limpio              | Formato adecuado         | PyMuPDF                  | Velocidad + estructura de encabezados     |
| unstructured     | ~1.29s           | Fragmentos semánticos        | No foco en tablas        | OCR/otros opcional       | RAG, análisis semántico                    |
| marker‑pdf       | ~11.3s (primera) | Markdown con diseño          | Preservación perfecta    | Modelo visión (grande)   | Alta fidelidad de diseño                   |

Fuentes: pruebas publicadas y documentación técnica[^11][^12][^13][^14][^15][^16][^17].

## Herramientas 3D y pipelines de generación/render

Blender, controlado vía Python (bpy) y con comunicación por pyzmq, permite orquestar渲染 y manipulación de escenas en modo headless. TripoSR, un modelo de reconstrucción 3D desde una imagen, ofrece síntesis rápida y adecuada calidad, con requisitos GPU que van desde una RTX 3060 para flujos ligeros hasta A100 para máxima velocidad. Open3D y trimesh complementan el pipeline para mallas, point clouds y operaciones geométricas. En cargas intensivas o por lotes, conviene evaluar GPU en la nube y dimensionar VRAM según el volumen y la resolución[^18][^19][^20][^21][^22].

Recomendación: mantener Blender + pyzmq como capa de control y TripoSR para generación bajo demanda; planificar capacidad GPU y almacenamiento para modelos 3D, usando cloud GPU cuando el SLA y el tiempo de ciclo lo exijan[^18][^19][^20][^21][^22].

Tabla 7. Requisitos de hardware y casos de uso (3D)
| Herramienta | Caso de uso principal                       | Requisitos mínimos (referencia)     | Observaciones de costo                    |
|-------------|----------------------------------------------|-------------------------------------|-------------------------------------------|
| Blender     | Render y manipulación de escenas             | CPU adecuado, RAM 16–32GB           | Coste operativo CPU/RAM                   |
| TripoSR     | Reconstrucción 3D desde imagen               | GPU RTX 3060 6GB (básico); A100 para velocidad | Cloud GPU recomendable en picos           |
| Open3D      | Mallas/point clouds, reconstrucción          | CPU/GPU según tarea                 | OSS, costo dev y mantenimiento            |
| trimesh     | Carga y operaciones en mallas triangulares   | CPU                                 | OSS, complementario a Open3D              |

## Compatibilidad con Python 3.11+ e integración end‑to‑end

Python 3.11+ proporciona mejoras en tipado y rendimiento que potencian FastAPI y el ecosistema asíncrono. La validación con Pydantic, sumada a contratos explícitos entre orquestador y microservicios, reduce errores en producción y acelera pruebas. La integración con MCP se facilita por la compatibilidad de FastAPI y la estabilidad del stack, mientras que la capa Frontend (Next.js) opera como consumidor REST/WebSocket sin acoplarse a la lógica interna del backend. La compatibilidad verificada de FastAPI con Python 3.11+ refuerza la elección[^1][^2][^9][^10].

## Optimización de costos (infra, licencias y operación)

La estrategia de costos debe balancear autoservicio, licenciamiento abierto y uso selectivo de servicios gestionados. En LLMs, se recomienda priorizar modelos gratuitos o de bajo costo, reservando modelos premium para tareas que lo justifiquen. En scraping, aplicar Playwright autoservicio y stealth, habilitando proxies gestionados solo cuando el sitio lo requiera. En PDFs, ejecutar en autoservicio con Unstructured, PyMuPDF y pdfplumber; Docling/Unstract reducen dependencia de servicios de pago. En 3D, dimensionar GPU y almacenamiento y usar cloud GPU en cargas por lotes. Los planes de CrewAI se evalúan frente al autoservicio OSS según necesidades operativas[^1][^11][^23][^3].

Tabla 8. Mapa de costos por componente
| Componente | Modalidad autoservicio | Servicio gestionado     | Drivers de costo principales                  | Observaciones                          |
|------------|-------------------------|-------------------------|-----------------------------------------------|----------------------------------------|
| Orquestación (CrewAI) | OSS ($0 licencia)       | AMP (planes de pago)    | LLM tokens, infra de ejecución                 | OSS recomendado inicialmente[^23][^25] |
| API (FastAPI) | Nativo ($0 licencia)    | N/A                     | Infra compute, tiempo dev                      | Async reduce tiempos de espera[^1]     |
| Scraping (Playwright) | Contenedores + proxies opcionales | Proveedores scraping | Proxies, IPs, anti‑bot                         | Autoservicio es base[^3][^4]           |
| PDF (Unstructured/otros) | OSS local               | APIs gestionadas        | OCR, compute, almacenamiento                   | Docling/Unstract como alternativas[^11][^16][^17] |
| 3D (Blender + TripoSR) | Local/GPU on‑prem       | Cloud GPU               | VRAM, almacenamiento, cómputo                  | Dimensionar por lotes[^18][^21][^22]   |

## Escalabilidad, riesgos y mitigaciones

Escalar el pipeline implica instrumentar concurrencia en FastAPI, buffering en colas y caching selectivo. Los principales riesgos y mitigaciones se resumen a continuación.

Tabla 9. Matriz de riesgo y mitigación
| Riesgo                                   | Componente         | Impacto           | Probabilidad | Mitigación                                                   |
|------------------------------------------|--------------------|-------------------|--------------|--------------------------------------------------------------|
| Bloqueo de proveedor                     | Scraping/LLMs      | Alto              | Media        | Diseños pluggables, proxies rotativos, fallback modelos      |
| Anti‑bot/Cloudflare                      | Scraping           | Alto              | Alta         | Stealth, rotación IPs, autoservicio + proveedores managed[^3]|
| Cuellos por colas de trabajo             | PDFs/3D            | Medio             | Media        | Colas desacopladas, workers escalables, backpressure         |
| Latencias LLM y variabilidad             | Orquestación       | Medio             | Media        | Caching, distribución de modelos por tarea, límites de tokens |
| Dependencias externas (OCR/tesseract)    | PDF                | Medio             | Media        | Pre‑check de dependencias, fallbacks                         |
| Dimensionamiento GPU                     | 3D                 | Alto              | Media        | Benchmark local, cloud GPU para picos[^21]                   |

Estas medidas deben implementarse con observabilidad activa: tracking de uso, conteo de tokens, métricas por endpoint MCP y alertas de error. Las guías comparativas de scraping y benchmarks de frameworks respaldan estas prácticas[^3][^4][^2].

## Recomendaciones finales y plan de adopción

- Mantener CrewAI como orquestador principal; reservar AutoGen para prototipado conversacional y LangGraph para flujos complejos con estado. Evitar Swarm en producción[^5][^6][^7][^8].
- Establecer FastAPI como capa de microservicios MCP por su async nativo, validación con Pydantic y documentación automática; usar Flask/Quart solo en endpoints simples o con menos demanda de concurrencia[^1][^2][^10].
- Playwright como estándar en scraping/automation; aplicar stealth y proxies opcionales, con autoservicio como base para controlar costos[^3][^4].
- Pipeline de PDFs: Unstructured.io para RAG y análisis semántico; pymupdf4llm cuando la velocidad sea prioritaria; pdfplumber para tablas; marker‑pdf para alta fidelidad; Docling/Unstract como alternativas open‑source para autoservicio[^11][^12][^13][^14][^15][^16][^17].
- Capa 3D: Blender + pyzmq para control headless; TripoSR para reconstrucción 3D; dimensionar GPU y evaluar cloud para cargas por lotes[^18][^19][^20][^21][^22].
- Ejecución autoservicio por defecto y AMP de CrewAI solo si el valor operativo lo justifica; monitoreo continuo de costos por agente y tokens consumidos[^23][^25].

Tabla 10. Hoja de ruta de adopción
| Hito                               | Objetivo                                               | Tareas clave                                                         | Métricas de éxito                             |
|------------------------------------|--------------------------------------------------------|---------------------------------------------------------------------|-----------------------------------------------|
| Consolidación orquestación         | Alinear roles y procesos con CrewAI                    | Definir crews por agente, gates de calidad                           | Tasa de éxito por agente, retrabajos          |
| Refuerzo de microservicios MCP     | Maximizar concurrencia y contratos explícitos          | Endpoints FastAPI con Pydantic, tests de carga                      | p95 latency por endpoint, throughput          |
| Optimización scraping              | Robustez y control de costos                           | Playwright headless, stealth, rotación proxies opcionales           | Tasa de bloqueo, costo por 1k páginas         |
| Pipeline de PDFs                   | Balance calidad/velocidad/costo                        | Unstructured + pymupdf4llm + pdfplumber + marker‑pdf (fallback)     | Calidad de chunking, tablas correctas         |
| Capacidad 3D                       | Garantizar SLA de render y reconstrucción              | Validación GPU local, plan cloud GPU para picos                     | Tiempo de ciclo por lote, VRAM utilizada      |
| Observabilidad y costos            | Control presupuestario y trazabilidad                  | Tracking tokens por agente, límites de presupuesto                  | Coste por tesis, desviación presupuestaria    |

## Gaps de información

Se identifican las siguientes brechas de información que deben cerrarse con pruebas controladas o validación adicional:

- Benchmarks comparativos reproducibles de throughput/latencia entre CrewAI, AutoGen y LangGraph en escenarios con estado y DAGs.
- Medición de memoria/CPU de Playwright en contenedores frente a Selenium/Puppeteer bajo cargas sostenidas de scraping.
- Costos operativos detallados de Unstructured.io en producción con dependencias nativas (poppler/tesseract) y su impacto en CI/CD.
- Evidencia de estabilidad y escalabilidad de TripoSR en pipelines por lotes con GPU local vs cloud.
- Costos de infraestructura de microservicios FastAPI bajo alta concurrencia en nube (cuotas de egress, almacenamiento, balanceadores).
- Límites actuales y políticas de uso de MiniMax y DeepSeek en producción (límite de RPM/TPM y TOS).

## Referencias

[^1]: FastAPI vs Flask 2025: Performance, Speed & When to Choose. Strapi Blog. https://strapi.io/blog/fastapi-vs-flask-python-framework-comparison  
[^2]: TechEmpower Framework Benchmarks — Round 23. https://www.techempower.com/benchmarks/#section=data-r23  
[^3]: Playwright vs Selenium vs Puppeteer (2025). PromptFuel Blog. https://promptfuel.io/blog/playwright-vs-selenium-vs-puppeteer-2025  
[^4]: Playwright vs Selenium 2025: Browser Automation Comparison. Browserless Blog. https://www.browserless.io/blog/playwright-vs-selenium-2025-browser-automation-comparison  
[^5]: Which AI Agent Framework to use? CrewAI vs LangGraph vs AutoGen vs Swarm. Medium (Accredian). https://medium.com/accredian/which-ai-agent-framework-to-use-crewai-vs-langgraph-vs-autogen-vs-swarm-7c97f5778fc2  
[^6]: LangGraph Documentation. https://langchain-ai.github.io/langgraph/  
[^7]: Microsoft AutoGen — Getting Started. https://microsoft.github.io/autogen/0.2/docs/Getting-Started/  
[^8]: OpenAI Swarm — GitHub. https://github.com/openai/swarm  
[^9]: CrewAI Docs — Introduction. https://docs.crewai.com/introduction  
[^10]: FastAPI Documentation. https://fastapi.tiangolo.com/  
[^11]: I Tested 7 Python PDF Extractors (2025 Edition). Medium (Aman Kumar). https://onlyoneaman.medium.com/i-tested-7-python-pdf-extractors-so-you-dont-have-to-2025-edition-c88013922257  
[^12]: PyMuPDF4LLM — Documentation. https://pymupdf.readthedocs.io/en/latest/pymupdf4llm/  
[^13]: PDF Data Extraction Benchmark 2025: Docling vs Unstructured vs LlamaParse. Procycons. https://procycons.com/en/blogs/pdf-data-extraction-benchmark/  
[^14]: How to Process PDFs in Python. Unstructured Blog. https://unstructured.io/blog/how-to-process-pdf-in-python  
[^15]: marker‑pdf — PyPI. https://pypi.org/project/marker-pdf/  
[^16]: Docling: Powerful Alternative to Unstructured.io. LinkedIn (Ramanan Iyer). https://www.linkedin.com/pulse/using-docling-powerful-alternative-unstructuredio-ramanan-iyer-rzldf  
[^17]: Open-Source Document Data Extraction with Unstract & DeepSeek. Unstract Blog. https://unstract.com/blog/open-source-document-data-extraction-with-unstract-deepseek/  
[^18]: TripoSR: Fast 3D Object Reconstruction — GitHub. https://github.com/VAST-AI-Research/TripoSR  
[^19]: Complete TripoSR Blender Add-on Tutorial. TripoAI. https://www.triposrai.com/posts/triposr-blender-addon-workflow-tutorial/  
[^20]: Create a 3D Object from Images with TripoSR in Python. PyImageSearch. https://pyimagesearch.com/2024/11/25/create-a-3d-object-from-your-images-with-triposr-in-python/  
[^21]: Generating 3D Models with TripoSR on RunPod. RunPod Articles. https://www.runpod.io/articles/guides/generating-3d-models-with-tripo-gpu-platform  
[^22]: Open Source 3D Reconstruction Showdown. TripoAI. https://triposrai.com/posts/open-source-3d-reconstruction-showdown/  
[^23]: CrewAI Pricing. https://www.crewai.com/pricing  
[^24]: Benchmarks Consolidados Nov 2025 — ARA Framework (contexto interno).  
[^25]: CrewAI OSS Status and Costs (Community). https://community.crewai.com/t/crewais-open-source-status-and-associated-costs/4549