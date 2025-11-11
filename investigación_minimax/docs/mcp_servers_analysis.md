# Disponibilidad, estabilidad y costos reales de servidores MCP para ARA Framework (Presupuesto $0)

## Resumen ejecutivo

El proyecto ARA (Autonomous Research Assistant) propone una arquitectura de agentes orquestados que consumen herramientas a través del Model Context Protocol (MCP). La decisión crítica para su viabilidad inmediata es confirmar qué servidores MCP están disponibles hoy, son estables, tienen un nivel gratuito suficiente y cubren las capacidades requeridas (ingesta de documentos, scraping, operaciones de base de datos y gestión de conocimiento).

Conclusión clave: existe una combinación de servidores MCP y servicios subyacentes que permite operar ARA con un costo directo adicional de $0. El conjunto incluye GitHub MCP, Playwright MCP, MarkItDown MCP, Jina AI Reader MCP (vía servidor remoto MCP y/o API), Supabase MCP (API y plan gratuito) y Notion MCP (con rate limits de API). Firecrawl MCP, por su modelo de créditos de la API en la nube, no cumple el requisito de $0 para producción; se recomienda como opcional si se habilita un presupuesto adicional o autoalojamiento.

Para ilustrar la decisión de adopción, la siguiente matriz resume el estado por servidor.

Tabla 1. Matriz de adopción por servidor MCP

| Servidor MCP                 | Oficialidad y mantenimiento | Estado de costo            | Nivel gratuito real                               | Riesgos clave                                                | Recomendación |
|-----------------------------|-----------------------------|----------------------------|---------------------------------------------------|--------------------------------------------------------------|---------------|
| GitHub MCP                  | Oficial (GitHub) [^1][^2][^3] | Gratuito (MIT)             | Ilimitado (limitado por políticas de API GitHub)  | Permisos vía PAT; exposición accidental de secretos          | Adoptar       |
| Playwright MCP              | Comunidad (ExecuteAutomation) [^4][^5] | Gratuito (MIT)             | Ilimitado                                         | Gestión de navegadores; performance en sitios JS-heavy       | Adoptar       |
| MarkItDown MCP              | Ecosistema Microsoft (MarkItDown) [^6][^7] | Gratuito (MIT)             | Ilimitado                                         | Dependencias de formato; resultados varían por documento     | Adoptar       |
| Jina AI Reader MCP          | Jina AI (MCP remoto y API) [^8][^9] | Gratuito con límites       | 20 RPM sin API key; 200 RPM con API key; 10M tokens incluidos | Exceso de RPM; consumo de tokens; caching 5 min              | Adoptar       |
| Supabase MCP                | Ecosistema Supabase [^10][^11][^19] | Freemium                   | 500 MB DB; 1 GB storage; 5 GB egress; 50k MAUs; proyectos se pausan por inactividad | Pausa por inactividad; escalado fuera del free               | Adoptar       |
| Notion MCP                  | Comunidad/oficial (tools) [^12][^13][^20] | Uso de API sin coste directo | 3 req/s promedio; límites de payload; 429 con retry-after | Límites estrictos; variabilidad por plan de Notion           | Adoptar       |
| Firecrawl MCP               | Oficial (repositorio) [^14][^15] | Créditos (nube) / Auto-host | Free créditos puntuales; sin cifras exactas       | Costos variables; disponibilidad en la nube condicionada a créditos | No adoptar en $0; opcional presupuesto |

Narrativa de decisión: en un escenario de $0, la combinación GitHub + Playwright + MarkItDown + Jina (Reader) + Supabase (free) + Notion cubre el 100% de las capacidades críticas. Firecrawl es potente para crawling profundo y extracción estructurada, pero su modelo de créditos en la nube rompe la restricción presupuestaria; se considera opcional si se habilita un presupuesto.

Hoja de ruta de implementación: comenzar con la habilitación de clientes MCP en VS Code y adaptadores Python, configurar GitHub PAT y llaves de API, establecer límites operativos (rate limits y tamaños), activar caching en Jina y monitorización de Supabase (pausas por inactividad). Paralelamente, definir herramientas soportadas por cada servidor MCP en Notion y validar accesos, especialmente sobre rate limits y manejo de errores.

---

## Alcance, supuestos y metodología

Este análisis se centra en los servidores MCP propuestos para ARA: GitHub, Playwright, MarkItDown, Supabase, Notion, Jina AI Reader y Firecrawl. Se evalúan cuatro dimensiones: disponibilidad y oficialidad, estabilidad y madurez, costos y límites del nivel gratuito, y adecuación funcional a los flujos de ARA (scraping, conversión a Markdown, acceso a repos y temas de ingeniería, operaciones básicas de base de datos y conocimiento). La metodología combina revisión de documentación oficial, repositorios y páginas de precios, priorizando fuentes primarias y confirmando características en la práctica de configuración de servidores MCP en clientes como VS Code y Claude Desktop [^16]. Se contextualiza en el protocolo MCP y su evolución [^17].

Supuestos de presupuesto: el equipo ya dispone de GitHub Copilot Pro; no se contempla gasto adicional en herramientas MCP ni servicios en la nube. Se admite el uso de niveles gratuitos y open-source, con autoalojamiento cuando aplique (p. ej., Playwright en contenedores, MarkItDown como utilidad local). La evaluación se realiza desde la perspectiva de un arquitecto de software y un investigador técnico, con foco en factibilidad inmediata.

---

## Panorama MCP y criterios de evaluación

El Model Context Protocol (MCP) define una forma estándar de exponer recursos y herramientas a clientes (agentes LLM, editores agentic). Los servidores MCP pueden ser locales, remotos o híbridos, con descubribilidad y selección de toolsets que condicionan la seguridad y la experiencia de uso. La evolución del protocolo y el lanzamiento de registros oficiales permiten un mayor control y descubrimiento de servidores, lo cual es relevante para la gobernanza de herramientas en ARA [^17][^18].

Para priorizar la adopción, ARA debe evaluar:
- Disponibilidad y oficialidad (repositorio activo, mantenedor reconocido).
- Estabilidad y madurez (licencia, frecuencia de releases, documentación, adopción).
- Seguridad y permisos (scopes de tokens, principios de mínimo privilegio).
- Cobertura funcional (herramientas y recursos necesarios para los flujos).
- Costos y límites del nivel gratuito (rate limits, cuotas, costos ocultos).
- Facilidad de despliegue en VS Code / Claude Desktop / Cursor (configuración remote/local, Docker).

Tabla 2. Criterios y ponderación propuesta

| Criterio                        | Definición breve                                             | Ponderación |
|---------------------------------|--------------------------------------------------------------|------------|
| Disponibilidad y oficialidad    | Repositorio activo y mantenedor reconocido                   | 25%        |
| Estabilidad y madurez           | Licencia, releases, adopción, soporte                        | 20%        |
| Seguridad y permisos            | Scopes, manejo de secretos, permisos mínimos                 | 15%        |
| Cobertura funcional             | Herramientas y recursos necesarios para ARA                  | 20%        |
| Costos y límites del free tier  | RPM, cuotas, almacenamiento, costos ocultos                  | 15%        |
| Despliegue y operación          | Facilidad en VS Code/Claude/Cursor, Docker, remote/local     | 5%         |

---

## Evaluación por servidor MCP

### GitHub MCP

Disponibilidad y oficialidad. GitHub mantiene un servidor MCP oficial, con disponibilidad pública y documentación de uso en productos Copilot. El repositorio y la documentación describen herramientas para interactuar con repositorios, issues, pull requests (PRs), discusiones y seguridad, además de un sistema de toolsets para modular la exposición de capacidades [^1][^2][^3].

Funcionalidades clave. Entre los toolsets más relevantes para ARA se incluyen: repositorios, issues, PRs, usuarios, discusiones, Dependabot, seguridad de código y acciones. El servidor soporta modos de solo lectura y descubrimiento dinámico de herramientas para simplificar la experiencia de uso por parte de agentes [^1][^2].

Costos y rate limits. El servidor MCP es open-source (MIT). El uso se clasifica como gratuito, sujeto a políticas y límites de la API de GitHub (no detallados en las fuentes evaluadas). La autenticación se realiza mediante token de acceso personal (PAT), y se recomienda aplicar scopes mínimos (p. ej., repo, read:org) y prácticas de rotación y almacenamiento seguro [^1][^2].

Estabilidad y madurez. La adopción es amplia y cuenta con documentación oficial, soporte en hosts MCP populares (VS Code, Claude Desktop, Cursor) y releases activos [^1][^2][^3].

Implicaciones para ARA. GitHub MCP habilita lectura de repos y código, gestión de issues/PRs, acceso a Actions y datos de seguridad, fundamental para agentes de investigación técnica y orquestación de tareas de ingeniería.

### Playwright MCP

Disponibilidad y oficialidad. El servidor MCP de Playwright, mantenido por ExecuteAutomation, es open-source (MIT) con documentación y soporte para instalación vía npm/npx y ejecución en contenedores [^4][^5].

Funcionalidades clave. Automatización de navegador y APIs; scraping con interacción real (JS), capturas de pantalla, ejecución de scripts, y generación de código de pruebas. Soporta Docker y múltiples clientes MCP (Claude Desktop, Cursor, VS Code) [^4][^5].

Costos y rate limits. Software gratuito bajo licencia MIT. Los únicos costos operativos posibles derivan de infraestructura propia (proxies, cómputo), no del servidor en sí.

Estabilidad y madurez. Repositorio activo con adopción significativa y guía de herramientas soportadas para web (navegación, scrape, screenshot, run JS) [^5].

Implicaciones para ARA. Útil para scraping avanzado en sitios dinámicos, validaciones end-to-end y extracción con comportamiento real de navegador. Requiere gestión de navegadores y tuning de performance en sitios JS-heavy.

### MarkItDown MCP

Disponibilidad y oficialidad. MarkItDown, de Microsoft, ofrece un servidor MCP para convertir múltiples formatos (PDF, DOCX, PPTX, etc.) a Markdown. El proyecto es open-source (MIT) [^6][^7].

Funcionalidades clave. Conversión a Markdown de documentos de oficina y PDFs, integrable con aplicaciones LLM. El servidor MCP forma parte del ecosistema MarkItDown, con empaquetado como utilidad Python y servidor MCP [^6][^7].

Costos y rate limits. Gratuito bajo licencia MIT. La latencia y throughput dependen de tamaño y complejidad de los documentos y de la infraestructura donde se ejecute.

Estabilidad y madurez. Proyecto de Microsoft con documentación y guías; la disponibilidad del servidor MCP está referenciada en su repositorio principal [^6][^7].

Implicaciones para ARA. Esencial para ingestión de PDFs y documentos en Markdown para agentes de revisión de literatura y síntesis de contenido.

### Supabase MCP

Disponibilidad y oficialidad. Supabase documenta la integración MCP y ofrece guía de precios y capacidades del plan gratuito. El “model context protocol” está soportado en su ecosistema, incluyendo operaciones básicas de base de datos y almacenamiento [^10][^11][^19].

Costos y límites del plan gratuito. Los límites clave incluyen: base de datos de 500 MB por proyecto, almacenamiento de archivos de 1 GB, 5 GB de egress (y 5 GB cached egress), 50,000 usuarios activos mensuales (MAUs), 2 millones de mensajes mensuales en Realtime y 500,000 invocaciones de Edge Functions. Los proyectos gratuitos se pausan tras una semana de inactividad [^11].

Tabla 3. Límites del plan gratuito de Supabase

| Recurso                             | Límite en Free                              |
|-------------------------------------|---------------------------------------------|
| Tamaño de base de datos             | 500 MB por proyecto                         |
| Almacenamiento de archivos          | 1 GB                                        |
| Egress (salida)                     | 5 GB (+ 5 GB cached egress)                 |
| Usuarios activos mensuales (MAUs)   | 50,000                                      |
| Realtime mensajes/mes               | 2 millones                                  |
| Edge Functions invocaciones         | 500,000                                     |
| Pausa por inactividad               | Proyecto se pausa tras 1 semana             |

Implicaciones para ARA. Apto para persistencia ligera y almacenamiento de artefactos. Monitorear la pausa por inactividad y planificar reactivaciones. Para cargas mayores, evaluar migración a plan de pago.

### Notion MCP

Disponibilidad y oficialidad. Las herramientas soportadas por el servidor MCP de Notion están documentadas por sus desarrolladores, junto con los límites de la API. El uso de la API es gratuito; el costo proviene del plan del espacio de trabajo de Notion según necesidades de colaboración y funcionalidades requeridas [^12][^13][^20].

Rate limits. El límite de solicitud es un promedio de tres solicitudes por segundo por integración. Algunas ráfagas por encima del promedio están permitidas. Al exceder, la API devuelve HTTP 429 (“rate_limited”) e indica “Retry-After”. El tamaño máximo de payload es de 1000 bloques y 500 KB [^13].

Tabla 4. Resumen de límites de la API de Notion

| Tipo de límite                  | Valor / Comportamiento                               |
|---------------------------------|------------------------------------------------------|
| Rate limit promedio             | 3 solicitudes por segundo por integración            |
| Ráfagas                         | Permitidas parcialmente                              |
| Exceso de límite                | HTTP 429; respetar “Retry-After”                     |
| Tamaño de payload               | 1000 bloques; 500 KB                                 |

Implicaciones para ARA. Viable para gestión de conocimiento y documentación si se implementa backoff y batching. Ajustar la operación según rate limits y tamaños.

### Jina AI Reader MCP

Disponibilidad y oficialidad. Jina AI ofrece un servidor MCP remoto y una API Reader para convertir URLs a Markdown/JSON amigables para LLM. El servicio es gratuito con rate limits, y escalable a mayores cuotas mediante clave API [^8][^9].

Límites y costos. Sin API key, la API permite 20 solicitudes por minuto (r.jina.ai). Con API key estándar, se reportan 500 RPM; con clave premium, 5000 RPM. La función de búsqueda (s.jina.ai) permite 100 RPM estándar y 1000 RPM premium. Cada nueva clave incluye diez millones de tokens gratuitos; el conteo de tokens difiere entre r.jina.ai (salida) y s.jina.ai (costo fijo por solicitud). El contenido se cachea por cinco minutos [^8][^9].

Tabla 5. Límites y tokens de Jina AI Reader

| Modo                         | RPM sin API key | RPM con API key estándar | RPM con API key premium | Tokens / Cuotas                         |
|-----------------------------|------------------|--------------------------|-------------------------|-----------------------------------------|
| Reader (r.jina.ai)          | 20               | 500                      | 5000                    | 10M tokens gratuitos (salida contada)   |
| Search (s.jina.ai)          | Bloqueado        | 100                      | 1000                    | Costo fijo por solicitud (desde 10k)    |
| Caché                       | 5 minutos        | 5 minutos                | 5 minutos               | —                                       |

Implicaciones para ARA. Alternativa gratuita a Firecrawl para scraping de contenido en la mayoría de los sitios; para crawling profundo y extracción estructurada a gran escala, considerar Firecrawl si existe presupuesto.

### Firecrawl MCP

Disponibilidad y oficialidad. Firecrawl mantiene un servidor MCP oficial; el software es MIT, pero el uso del servicio en la nube requiere una API key y créditos, con monitoreo de umbrales de crédito [^14][^15]. La documentación y el repositorio detallan herramientas para scraping, crawling, mapeo de sitios y extracción estructurada.

Costos y créditos. El servicio ofrece comenzar gratis y escalar, pero las cifras exactas de límites del nivel gratuito no están publicadas en las fuentes evaluadas. El autoalojamiento es una opción para evitar costos de nube, a costa de operar infraestructura [^14][^15].

Tabla 6. Mapa de herramientas Firecrawl MCP (scrape, batch, search, crawl, extract)

| Herramienta                 | Propósito                                     | Consideraciones operativas                     |
|----------------------------|-----------------------------------------------|------------------------------------------------|
| firecrawl_scrape           | Extraer contenido de una URL                  | Ráfagas y rate limits; reintentos              |
| firecrawl_batch_scrape     | Múltiples URLs con limitación y paralelo      | Monitoreo de estado y errores                  |
| firecrawl_map              | Descubrir URLs indexadas de un sitio          | Profundidad y restricciones de dominio         |
| firecrawl_search           | Búsqueda web + extracción opcional            | Costos por uso en la nube                      |
| firecrawl_crawl            | Rastreo profundo y extracción                 | Asíncrono; control de límites y tiempos        |
| firecrawl_extract          | Extracción de datos estructurados con LLM     | Configuración de prompts y validación          |

Implicaciones para ARA. Es una solución robusta para crawling y extracción; sin embargo, el modelo de créditos en la nube no cumple el requisito de $0 directo. Se marca como opcional si se habilita presupuesto o autoalojamiento.

---

## Comparativa transversal y decisión de adopción

Para consolidar la decisión, se presenta una comparativa de disponibilidad, estabilidad, cobertura funcional, free tier y riesgos. El objetivo es verificar si la combinación $0 cubre los casos de uso esenciales.

Tabla 7. Comparativa final de adopción

| Servidor           | Disponible | Estable | Free tier suficiente | Cobertura funcional clave                 | Riesgos operativos                         | Decisión     |
|--------------------|------------|---------|----------------------|-------------------------------------------|--------------------------------------------|--------------|
| GitHub MCP         | Sí         | Sí      | Sí                   | Repos, issues, PRs, acciones, seguridad   | Permisos PAT; secretos                     | Adoptar      |
| Playwright MCP     | Sí         | Sí      | Sí                   | Scraping navegador, screenshots, JS       | Browser mgmt; performance JS-heavy         | Adoptar      |
| MarkItDown MCP     | Sí         | Sí      | Sí                   | Conversión PDF/DOCX a MD                  | Variabilidad por formato                   | Adoptar      |
| Jina Reader MCP    | Sí         | Sí      | Sí                   | URL→Markdown/JSON; SERP; PDFs             | RPM y tokens; caché 5 min                   | Adoptar      |
| Supabase MCP       | Sí         | Sí      | Sí                   | DB, storage, realtime, edge functions     | Pausa por inactividad; escalado            | Adoptar      |
| Notion MCP         | Sí         | Sí      | Sí                   | Gestión de conocimiento y documentación   | 3 req/s; payload 500KB; 429/retry-after    | Adoptar      |
| Firecrawl MCP      | Sí         | Sí      | No (nube con créditos) | Crawling profundo; extracción estructurada | Costos variables; créditos en nube         | No adoptar en $0; opcional |

Tabla 8. Matriz de rate limits y cuotas

| Servicio       | Rate limit / Cuota principal                               | Observaciones clave                           |
|----------------|-------------------------------------------------------------|-----------------------------------------------|
| Jina Reader    | 20 RPM sin API; 500/5000 RPM con API; 10M tokens           | Caché 5 min; s.jina.ai con límites separados  |
| Notion API     | 3 req/s promedio; HTTP 429 + Retry-After; payload 500KB    | Batching y backoff necesarios                 |
| Supabase Free  | 500 MB DB; 1 GB storage; 5 GB egress; 50k MAUs             | Proyectos se pausan por inactividad           |
| GitHub MCP     | Sujeto a API GitHub (no cifras en fuentes)                 | Scopes mínimos; manejo seguro de PAT          |

Resultado: ARA puede operar al 100% de sus capacidades críticas sin costo adicional combinando GitHub + Playwright + MarkItDown + Jina Reader + Supabase Free + Notion API. Firecrawl se reserva para escenarios que requieran crawling profundo y extracción estructurada a escala, sujeto a presupuesto.

---

## Diseño de integración en ARA (sin costo adicional)

La integración debe respetar las restricciones de cada servicio y minimizar costos operativos mediante caché, control de rate limits y herramientas de solo lectura cuando aplique.

- GitHub MCP. Configurar PAT con scopes mínimos (repo, read:org) y activar modo solo lectura cuando sea viable. Emplear toolsets por defecto y habilitar descubrimiento dinámico de herramientas para simplificar la interacción con agentes [^2].
- Playwright MCP. Desplegar en Docker para aislamiento y repetibilidad, descargando navegadores en el primer uso. Ajustar tiempos de espera y estrategias de auto-wait para mejorar la fiabilidad en sitios con mucho JavaScript [^4][^5].
- MarkItDown MCP. Ejecutar como utilidad local/servidor MCP para conversiones a Markdown; gestionar archivos grandes con control de errores y validaciones de formato [^6][^7].
- Jina Reader MCP. Usar el servidor remoto MCP y/o la API; aplicar caché de 5 minutos, controlar consumo de tokens, y limitar RPM (20 sin key, 500/5000 con key). Para búsquedas, emplear s.jina.ai con límites diferenciados [^8][^9].
- Supabase MCP. Configurar proyecto free, monitorizar límites (DB 500 MB, storage 1 GB, egress 5 GB), y planificar reactivaciones para evitar pausas por inactividad [^11].
- Notion MCP. Implementar batching y backoff ante HTTP 429 respetando Retry-After; limitar payloads a 500 KB y 1000 bloques por solicitud [^13].

Tabla 9. Checklist de configuración y seguridad

| Ítem                                   | Estado deseado                |
|----------------------------------------|-------------------------------|
| GitHub PAT con scopes mínimos          | Configurado                   |
| Modo solo lectura en GitHub MCP        | Activado cuando proceda       |
| Playwright MCP en Docker               | Desplegado                    |
| Descarga de navegadores en primer uso  | Validado                      |
| MarkItDown MCP local                   | Operativo                     |
| Jina API key (estándar/premium)        | Configurada si se requiere    |
| Límites RPM y tokens en Jina           | Monitorizados                 |
| Supabase proyecto free                 | Activo y observado            |
| Notion rate limits y Retry-After       | Implementados                 |
| Logs y alertas de costos               | Activados                     |

---

## Riesgos, limitaciones y mitigaciones

- Notion. Rigor en el manejo de rate limits (3 req/s promedio), payloads y errores 429 con Retry-After. Mitigar mediante colas, batching y control de tamaño de bloques [^13].
- Jina Reader. RPM y tokens son el principal riesgo; la caché de 5 minutos puede afectar frescura. Mitigar con planificación de llamadas, consolidación de requests y uso de API key cuando sea necesario [^8][^9].
- Supabase Free. Pausas por inactividad y límites de egress/storage. Mitigar con monitoreo activo, archivado de datos, y planes de migración a pago si se requiere continuidad garantizada [^11].
- GitHub MCP. Exposición de secretos por permisos excesivos en PAT. Mitigar con scopes mínimos, rotación de tokens, y evitar commits con credenciales [^1][^2].
- Playwright MCP. Performance en sitios JS-heavy y gestión de navegadores. Mitigar con Docker, auto-wait, y tuning de timeouts [^4][^5].
- Firecrawl MCP. Costos variables y dependencia de créditos en la nube. Mitigar con autoalojamiento o mantener como opcional bajo presupuesto [^14][^15].

Tabla 10. Mapa de riesgos por servidor

| Servidor       | Riesgo principal                        | Probabilidad | Impacto | Mitigación                                           | Dueño           |
|----------------|-----------------------------------------|--------------|---------|------------------------------------------------------|-----------------|
| Notion         | 429 / Retry-After y payload             | Media        | Media   | Batching, backoff, colas, control de tamaño          | Dev/Infra       |
| Jina Reader    | Exceso de RPM/tokens                    | Media        | Media   | Planificación, API key, caché, consolidación         | Dev/Infra       |
| Supabase Free  | Pausa por inactividad; egress/storage   | Media        | Alta    | Monitoreo, archivado, planes de migración            | Dev/Producto    |
| GitHub MCP     | Exposición de PAT                       | Baja         | Alta    | Scopes mínimos, rotación, secret management          | Seguridad       |
| Playwright MCP | Performance navegador                   | Media        | Media   | Docker, tuning de timeouts, auto-wait                | QA/Infra        |
| Firecrawl MCP  | Costos por créditos                     | Media        | Media   | Autoalojamiento; opcional con presupuesto            | Producto/Finanzas |

---

## Plan de validación y pruebas

Pruebas de humo por servidor:
- GitHub MCP. Lectura de repos, issues y PRs en modo solo lectura; verificación de toolsets y permisos [^2].
- Playwright MCP. Scraping básico con navegación, selección de elementos y captura de pantalla [^5].
- MarkItDown MCP. Conversión de PDF/DOCX/PPTX a Markdown, verificación de estructura y metadatos [^6][^7].
- Jina Reader MCP. URL→Markdown; comparación de contenido y medición de latencia; validación de caché y RPM [^8].
- Supabase MCP. Operaciones CRUD básicas y subida de archivos; verificación de límites de storage y egress [^10][^11].
- Notion MCP. Creación y actualización de páginas/blocks; manejo de errores 429 y Retry-After [^12][^13].

Métricas clave:
- Éxito de llamadas por servidor, latencia, tamaño de respuesta.
- Consumo de RPM y tokens (Jina), número de bloques y tamaño (Notion), almacenamiento y egress (Supabase).

Tabla 11. Plan de pruebas y métricas

| Caso                                   | Servidor       | Métrica principal                 | Umbral de aceptación            |
|----------------------------------------|----------------|-----------------------------------|---------------------------------|
| Leer repo y listar issues              | GitHub MCP     | Éxito de llamada; latencia        | >99% éxito; latencia <1s        |
| Navegar y capturar screenshot          | Playwright MCP | Éxito; latencia; tamaño           | >95% éxito; latencia <3s        |
| Convertir PDF a Markdown               | MarkItDown MCP | Éxito; integridad de contenido    | >95% éxito; estructura válida   |
| URL→Markdown (con caché)               | Jina Reader    | RPM; latencia; tokens             | Dentro de RPM; latencia <5s     |
| Insertar y descargar archivo           | Supabase MCP   | Éxito; egress; storage usado      | Dentro de cuotas; sin errores   |
| Crear página y añadir bloques          | Notion MCP     | Éxito; manejo de 429; tamaño      | Sin 429; payload <500KB         |

Estrategia de retries y backoff: configurar reintentos exponenciales para errores transitorios; respetar encabezados Retry-After en Notion; limitar concurrencia en Jina y Supabase para evitar cuotas.

---

## Alternativas gratuitas y cuándo considerarlas

Para web scraping, Jina Reader y Playwright cubren la mayoría de los casos sin costo. Firecrawl agrega crawling profundo y extracción estructurada a gran escala, con costo por créditos en la nube; si se habilita presupuesto o se autoaloja, es recomendable para coberturas exhaustivas [^8][^9][^14][^15]. Para base de datos y conocimiento, Supabase free es suficiente para persistencia ligera; si se necesita soberanía total o menor dependencia del servicio, explorar alternativas open-source como PocketBase o Appwrite, considerando el costo operativo del autoalojamiento [^11].

---

## Conclusiones y recomendación final

- Adopción inmediata bajo $0: GitHub MCP, Playwright MCP, MarkItDown MCP, Jina AI Reader MCP, Supabase (free) y Notion MCP. Esta combinación cubre scraping, conversión a Markdown, acceso a repos y temas de ingeniería, operaciones básicas de base de datos y gestión de conocimiento.
- Firecrawl MCP es una capacidad valiosa para crawling y extracción avanzada, pero su modelo de créditos en la nube no cumple el requisito de $0. Se recomienda como opcional si se asigna presupuesto o se considera autoalojamiento.
- Próximos pasos: completar la validación en entorno de destino, definir adaptación de herramientas por agente (NicheAnalyst, LiteratureResearcher, TechnicalArchitect, ContentSynthesizer), documentar accesos (PATs, API keys) y activar observabilidad con alertas sobre cuotas y errores.

---

## Apéndices

### Apéndice A — Límites y cuotas detalladas (consolidado)

Tabla A1. Consolidado de límites y cuotas

| Servicio       | Límite / Cuota                                         | Fuente |
|----------------|---------------------------------------------------------|--------|
| Jina Reader    | 20 RPM sin API; 500/5000 RPM con API; 10M tokens; caché 5 min | [^8][^9] |
| Notion API     | 3 req/s promedio; 429 + Retry-After; payload 500KB      | [^13]  |
| Supabase Free  | 500 MB DB; 1 GB storage; 5 GB egress; 50k MAUs; pausa por inactividad | [^11]  |
| GitHub MCP     | Uso sujeto a API GitHub (sin cifras en fuentes); PAT con scopes mínimos | [^1][^2] |

### Apéndice B — Toolsets de GitHub MCP (selección)

Tabla A2. Toolsets principales

| Toolset               | Descripción breve                                  |
|----------------------|-----------------------------------------------------|
| repositorios         | Lectura y exploración de código                     |
| incidencias (issues) | Gestión de issues                                   |
| solicitudes_de_extraccion (PRs) | Gestión de PRs                          |
| acciones             | Monitoreo de Actions                                |
| seguridad_de_código  | Alertas y hallazgos                                 |
| dependabot           | Dependencias y advisories                           |
| discusiones          | Discusiones del repositorio                         |

Fuente: documentación y repositorio oficial [^1][^2].

### Apéndice C — Herramientas Firecrawl MCP (scraping/crawling/extract)

Tabla A3. Firecrawl MCP herramientas

| Herramienta               | Uso recomendado                                    |
|---------------------------|----------------------------------------------------|
| firecrawl_scrape          | Página única con URL conocida                      |
| firecrawl_batch_scrape    | Múltiples páginas; control de velocidad            |
| firecrawl_map             | Descubrimiento de URLs                             |
| firecrawl_search          | Búsqueda + extracción opcional                     |
| firecrawl_crawl           | Rastreo profundo y extracción                      |
| firecrawl_extract         | Datos estructurados (precios, nombres, detalles)   |

Fuente: repositorio y documentación oficial [^14][^15].

---

## Referencias

[^1]: GitHub's official MCP Server — https://github.com/github/github-mcp-server  
[^2]: Using the GitHub MCP Server — https://docs.github.com/en/copilot/how-tos/provide-context/use-mcp/use-the-github-mcp-server  
[^3]: GitHub MCP Server public preview — https://github.blog/changelog/2025-04-04-github-mcp-server-public-preview/  
[^4]: GitHub - executeautomation/mcp-playwright — https://github.com/executeautomation/mcp-playwright  
[^5]: Playwright MCP Server Documentation — https://executeautomation.github.io/mcp-playwright/docs/intro  
[^6]: microsoft/markitdown — https://github.com/microsoft/markitdown  
[^7]: 10 Microsoft MCP Servers to Accelerate Your Development Workflow — https://developer.microsoft.com/blog/10-microsoft-mcp-servers-to-accelerate-your-development-workflow  
[^8]: Reader API - Jina AI — https://jina.ai/reader/  
[^9]: Jina AI Reader - Simon Willison's Weblog — https://simonwillison.net/2024/Jun/16/jina-ai-reader/  
[^10]: Model Context Protocol (MCP) | Supabase Docs — https://supabase.com/docs/guides/getting-started/mcp  
[^11]: Pricing & Fees - Supabase — https://supabase.com/pricing  
[^12]: Notion MCP – Supported tools — https://developers.notion.com/docs/mcp-supported-tools  
[^13]: Request limits - Notion API — https://developers.notion.com/reference/request-limits  
[^14]: Official Firecrawl MCP Server — https://github.com/firecrawl/firecrawl-mcp-server  
[^15]: Firecrawl MCP Server Documentation — https://docs.firecrawl.dev/mcp-server  
[^16]: Use MCP servers in VS Code — https://code.visualstudio.com/docs/copilot/customization/mcp-servers  
[^17]: MCP Protocol Docs - Introduction — https://modelcontextprotocol.io/introduction  
[^18]: MCP Registry (preview) — https://modelcontextprotocol.info/tools/registry/  
[^19]: Supabase Community MCP (PostgREST) — https://github.com/supabase-community/supabase-mcp  
[^20]: Notion Pricing Plans — https://www.notion.com/pricing

---

## Información faltante y supuestos

- Límites exactos de la API de GitHub para el servidor MCP: no se detallan cifras específicas en las fuentes consultadas; se asume uso sujeto a políticas de API GitHub [^1][^2].
- Disponibilidad de un “Supabase MCP” oficial: Supabase documenta MCP y el ecosistema asociado; se asume uso del servidor MCP PostgREST de la comunidad para integraciones AI [^10][^19].
- Estado de un servidor MCP oficial de Notion: las fuentes muestran herramientas soportadas y límites de API, sin confirmar un servidor MCP 100% oficial mantenido por Notion HQ; se adopta el uso de la API con MCP community [^12][^13][^20].
- Números oficiales y completos de límites y pricing de Firecrawl: existen referencias a “start free” y modelo de créditos, sin cifras exactas del tier gratuito; se recomienda autoalojamiento u opcionalidad bajo presupuesto [^14][^15].