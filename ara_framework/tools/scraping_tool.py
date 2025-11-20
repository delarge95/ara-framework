"""
ScrapingTool para extracción de contenido web con Playwright.

Fuente: docs/04_ARCHITECTURE.md (Tools Layer)
Referencia: docs/03_AI_MODELS.md (CrewAI tools integration)

Este tool es usado por:
- NicheAnalyst: Scraping de blogs, GitHub trends, foros
- LiteratureResearcher: Extracción de papers desde URLs
- TechnicalArchitect: Análisis de documentación técnica

Features:
- Browser automation con anti-detection
- Rate limiting automático (10 req/min vía adapter)
- Cache de contenido (3 días)
- Extracción estructurada con selectores CSS
- Screenshots para debugging
"""
import asyncio
from typing import Optional, Dict, Any, List
from langchain_core.tools import tool
import structlog

from mcp_servers.playwright_mcp import PlaywrightAdapter, ScrapedContent
from config.settings import settings

logger = structlog.get_logger()


class ScrapingTool:
    """
    Tool de web scraping integrado con CrewAI.
    
    Uso en Agents:
        agent = Agent(
            tools=[
                scraping_tool.scrape_website,
                scraping_tool.extract_structured_data,
            ],
            ...
        )
    """
    
    def __init__(self, redis_client=None):
        self.adapter = PlaywrightAdapter(redis_client=redis_client)
        self._connected = False
    
    async def _ensure_connected(self):
        """Conecta adapter si no está conectado."""
        if not self._connected:
            await self.adapter.connect()
            self._connected = True
    
    @tool("scrape_website")
    async def scrape_website(
        url: str,
        wait_for_selector: Optional[str] = None,
        include_html: bool = False,
    ) -> Dict[str, Any]:
        """
        Extrae contenido completo de una página web.
        
        Este tool usa Playwright para navegar y extraer contenido de páginas web,
        con soporte para JavaScript rendering y anti-detection.
        
        Args:
            url (str): URL de la página a scrapear
            wait_for_selector (str, optional): Selector CSS para esperar antes de extraer
            include_html (bool): Si incluir HTML completo en resultado
        
        Returns:
            Dict: Contenido scrapeado con estructura:
                - url: URL original
                - title: Título de la página
                - text: Texto extraído (limpio)
                - html: HTML completo (si include_html=True)
                - metadata: Metadata adicional (final_url, status, etc.)
        
        Example:
            # Scraping simple
            content = scrape_website("https://example.com")
            
            # Esperar elemento específico
            content = scrape_website(
                "https://spa-app.com",
                wait_for_selector=".main-content"
            )
        """
        # Instance method workaround for @tool decorator
        tool_instance = _get_scraping_tool_instance()
        await tool_instance._ensure_connected()
        
        try:
            result = await tool_instance.adapter.scrape_page(
                url=url,
                wait_for_selector=wait_for_selector,
                include_html=include_html,
            )
            
            logger.info(
                "scraping_tool_executed",
                url=url,
                text_length=len(result.text),
            )
            
            return result.to_dict()
        
        except Exception as e:
            logger.error(
                "scraping_tool_failed",
                url=url,
                error=str(e),
            )
            return {
                "url": url,
                "title": "",
                "text": "",
                "html": None,
                "metadata": {"error": str(e)},
            }
    
    @tool("extract_structured_data")
    async def extract_structured_data(
        url: str,
        selectors: Dict[str, str],
    ) -> Dict[str, Any]:
        """
        Extrae datos estructurados usando selectores CSS.
        
        Útil para extraer información específica de páginas con estructura conocida.
        
        Args:
            url (str): URL de la página
            selectors (dict): Mapeo de {campo: selector_css}
                Ejemplo: {
                    "title": "h1.article-title",
                    "author": ".author-name",
                    "date": "time.published",
                    "content": ".article-body",
                }
        
        Returns:
            Dict: Datos extraídos según selectores
        
        Example:
            data = extract_structured_data(
                "https://blog.com/post",
                {
                    "title": "h1",
                    "author": ".author",
                    "content": "article",
                }
            )
        """
        tool_instance = _get_scraping_tool_instance()
        await tool_instance._ensure_connected()
        
        try:
            data = await tool_instance.adapter.extract_structured_data(
                url=url,
                selectors=selectors,
            )
            
            logger.info(
                "structured_extraction_completed",
                url=url,
                fields_extracted=len([v for v in data.values() if v is not None]),
            )
            
            return data
        
        except Exception as e:
            logger.error(
                "structured_extraction_failed",
                url=url,
                error=str(e),
            )
            return {field: None for field in selectors.keys()}
    
    @tool("scrape_multiple_urls")
    async def scrape_multiple_urls(
        urls: List[str],
        max_concurrent: int = 3,
    ) -> List[Dict[str, Any]]:
        """
        Extrae contenido de múltiples URLs en paralelo.
        
        Args:
            urls (list): Lista de URLs a scrapear
            max_concurrent (int): Máximo número de scrapes simultáneos (default 3)
        
        Returns:
            List[Dict]: Lista de contenidos scrapeados
        
        Example:
            results = scrape_multiple_urls([
                "https://blog.com/post1",
                "https://blog.com/post2",
                "https://blog.com/post3",
            ])
        """
        tool_instance = _get_scraping_tool_instance()
        await tool_instance._ensure_connected()
        
        try:
            results = await tool_instance.adapter.scrape_multiple(
                urls=urls,
                max_concurrent=max_concurrent,
            )
            
            logger.info(
                "multiple_scrape_completed",
                total_urls=len(urls),
                successful=len(results),
            )
            
            return [r.to_dict() for r in results]
        
        except Exception as e:
            logger.error(
                "multiple_scrape_failed",
                total_urls=len(urls),
                error=str(e),
            )
            return []
    
    @tool("take_screenshot")
    async def take_screenshot(
        url: str,
        path: Optional[str] = None,
        full_page: bool = True,
    ) -> str:
        """
        Captura screenshot de una página web.
        
        Útil para debugging o documentación visual.
        
        Args:
            url (str): URL de la página
            path (str, optional): Path donde guardar (si None, usa temp)
            full_page (bool): Si capturar página completa
        
        Returns:
            str: Path del screenshot guardado
        
        Example:
            screenshot_path = take_screenshot(
                "https://example.com",
                path="screenshots/example.png"
            )
        """
        tool_instance = _get_scraping_tool_instance()
        await tool_instance._ensure_connected()
        
        try:
            screenshot_path = await tool_instance.adapter.take_screenshot(
                url=url,
                path=path,
                full_page=full_page,
            )
            
            logger.info(
                "screenshot_captured",
                url=url,
                path=screenshot_path,
            )
            
            return screenshot_path
        
        except Exception as e:
            logger.error(
                "screenshot_failed",
                url=url,
                error=str(e),
            )
            return ""
    
    @tool("execute_javascript")
    async def execute_javascript(
        url: str,
        script: str,
    ) -> Any:
        """
        Ejecuta JavaScript en el contexto de una página web.
        
        Útil para interacciones complejas o extracción de datos dinámicos.
        
        Args:
            url (str): URL de la página
            script (str): Código JavaScript a ejecutar
        
        Returns:
            Any: Resultado del script (debe ser JSON-serializable)
        
        Example:
            # Contar links
            link_count = execute_javascript(
                "https://example.com",
                "document.querySelectorAll('a').length"
            )
            
            # Extraer datos del DOM
            data = execute_javascript(
                "https://example.com",
                "Array.from(document.querySelectorAll('h2')).map(h => h.textContent)"
            )
        """
        tool_instance = _get_scraping_tool_instance()
        await tool_instance._ensure_connected()
        
        try:
            result = await tool_instance.adapter.evaluate_js(
                url=url,
                script=script,
            )
            
            logger.info(
                "javascript_executed",
                url=url,
                script_length=len(script),
            )
            
            return result
        
        except Exception as e:
            logger.error(
                "javascript_execution_failed",
                url=url,
                error=str(e),
            )
            return None
    
    async def close(self):
        """Cierra conexión del adapter."""
        if self._connected:
            await self.adapter.disconnect()
            self._connected = False


# Global instance for singleton pattern
_scraping_tool_instance = None


def _get_scraping_tool_instance(redis_client=None) -> ScrapingTool:
    """
    Obtiene instancia global de ScrapingTool (singleton).
    
    Args:
        redis_client: Cliente Redis (opcional)
    
    Returns:
        ScrapingTool instance
    """
    global _scraping_tool_instance
    
    if _scraping_tool_instance is None:
        _scraping_tool_instance = ScrapingTool(redis_client=redis_client)
    
    return _scraping_tool_instance


def get_scraping_tool(redis_client=None) -> ScrapingTool:
    """
    Alias público para obtener instancia.
    
    Args:
        redis_client: Cliente Redis (opcional)
    
    Returns:
        ScrapingTool instance
    """
    return _get_scraping_tool_instance(redis_client)


# ============================================================
# Module-level tool functions (LangChain @tool decorated)
# ============================================================
# These functions are defined at module level to avoid issues
# with @tool decorator and class methods. They use the singleton
# instance internally via _get_scraping_tool_instance().
# ============================================================

@tool("scrape_website")
async def scrape_website(
    url: str,
    wait_for_selector: Optional[str] = None,
    include_html: bool = False,
) -> Dict[str, Any]:
    """
    Extrae contenido completo de una página web.
    
    Este tool usa Playwright para navegar y extraer contenido de páginas web,
    con soporte para JavaScript rendering y anti-detection.
    
    Args:
        url (str): URL de la página a scrapear
        wait_for_selector (str, optional): Selector CSS para esperar antes de extraer
        include_html (bool): Si incluir HTML completo en resultado
    
    Returns:
        Dict: Contenido scrapeado con estructura:
            - url: URL original
            - title: Título de la página
            - text: Texto extraído (limpio)
            - html: HTML completo (si include_html=True)
            - metadata: Metadata adicional (final_url, status, etc.)
    
    Example:
        # Scraping simple
        content = scrape_website("https://example.com")
        
        # Esperar elemento específico
        content = scrape_website(
            "https://spa-app.com",
            wait_for_selector=".main-content"
        )
    """
    tool_instance = _get_scraping_tool_instance()
    await tool_instance._ensure_connected()
    
    try:
        result = await tool_instance.adapter.scrape_page(
            url=url,
            wait_for_selector=wait_for_selector,
            include_html=include_html,
        )
        
        logger.info(
            "scraping_tool_executed",
            url=url,
            text_length=len(result.text),
        )
        
        return result.to_dict()
    
    except Exception as e:
        logger.error(
            "scraping_tool_failed",
            url=url,
            error=str(e),
        )
        return {
            "url": url,
            "title": "",
            "text": "",
            "html": None,
            "metadata": {"error": str(e)},
        }


@tool("scrape_multiple_urls")
async def scrape_multiple_urls(
    urls: List[str],
    max_concurrent: int = 3,
) -> List[Dict[str, Any]]:
    """
    Extrae contenido de múltiples URLs en paralelo.
    
    Args:
        urls: Lista de URLs a scrapear
        max_concurrent: Máximo número de scrapes simultáneos
    
    Returns:
        List[Dict]: Lista de resultados (mismo formato que scrape_website)
    """
    tool_instance = _get_scraping_tool_instance()
    await tool_instance._ensure_connected()
    
    async def scrape_one(url: str):
        try:
            return await tool_instance.adapter.scrape_page(url=url)
        except Exception as e:
            logger.error("parallel_scrape_failed", url=url, error=str(e))
            return None
    
    # Process in batches
    results = []
    for i in range(0, len(urls), max_concurrent):
        batch = urls[i:i + max_concurrent]
        batch_results = await asyncio.gather(*[scrape_one(url) for url in batch])
        results.extend([r.to_dict() if r else None for r in batch_results])
    
    return [r for r in results if r is not None]
