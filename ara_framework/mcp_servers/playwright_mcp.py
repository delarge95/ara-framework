"""
Playwright MCP Adapter para automatización de browser y scraping.

Fuente: investigación perplexity/20_web_scraping_tools.md
Referencia: docs/04_ARCHITECTURE.md (MCP Servers Layer)

Capacidades:
1. Navegación headless (Chromium, Firefox, WebKit)
2. Scraping con anti-detection (stealth mode)
3. Screenshots para debugging
4. Extracción estructurada con selectores
5. JavaScript execution en contexto de página
"""
import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from pathlib import Path
import structlog
from playwright.async_api import (
    async_playwright,
    Browser,
    BrowserContext,
    Page,
    Playwright,
)

from mcp_servers.base import MCPAdapter
from config.settings import settings

logger = structlog.get_logger()


@dataclass
class ScrapedContent:
    """Contenido scrapeado de una página."""
    
    url: str
    title: str
    text: str
    html: Optional[str] = None
    screenshot_path: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def to_dict(self) -> dict:
        """Serializa a dict."""
        return {
            "url": self.url,
            "title": self.title,
            "text": self.text,
            "html": self.html,
            "screenshot_path": self.screenshot_path,
            "metadata": self.metadata or {},
        }


class PlaywrightAdapter(MCPAdapter[ScrapedContent]):
    """
    Adaptador de Playwright para scraping y automatización.
    
    Features:
    - Headless browser (Chromium por defecto)
    - Stealth mode (evasión de detección de bots)
    - Screenshots para debugging
    - Extracción estructurada con CSS/XPath
    - JavaScript evaluation
    
    Rate Limiting: 10 requests/min por defecto (configurable)
    Cache TTL: 3 días (contenido web cambia frecuentemente)
    
    Uso:
        async with PlaywrightAdapter(redis_client) as pw:
            # Scraping simple
            content = await pw.scrape_page("https://example.com")
            
            # Scraping con selector específico
            data = await pw.extract_structured_data(
                "https://example.com",
                selectors={
                    "title": "h1",
                    "content": ".article-body",
                }
            )
            
            # Screenshot
            screenshot = await pw.take_screenshot(
                "https://example.com",
                path="debug.png"
            )
    """
    
    def __init__(self, redis_client=None, browser_type: str = "chromium"):
        super().__init__(
            name="playwright",
            redis_client=redis_client,
            rate_limit_rpm=10,  # Conservative por defecto
            cache_ttl=settings.REDIS_TTL_CONTENT,  # 3 días
        )
        
        self.browser_type = browser_type
        
        # Playwright objects
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
    
    async def connect(self) -> None:
        """Inicializa Playwright y browser."""
        self.playwright = await async_playwright().start()
        
        # Launch browser
        browser_launcher = getattr(self.playwright, self.browser_type)
        self.browser = await browser_launcher.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",  # Anti-detection
            ],
        )
        
        # Create context con stealth settings
        self.context = await self.browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            locale="en-US",
            timezone_id="America/New_York",
        )
        
        # Inject stealth scripts
        await self.context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
        
        self.logger.info(
            "playwright_connected",
            browser_type=self.browser_type,
        )
    
    async def disconnect(self) -> None:
        """Cierra browser y Playwright."""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        
        self.logger.info("playwright_disconnected")
    
    async def health_check(self) -> bool:
        """Verifica que browser esté operativo."""
        try:
            page = await self.context.new_page()
            await page.goto("about:blank")
            await page.close()
            return True
        except Exception as e:
            self.logger.error("health_check_failed", error=str(e))
            return False
    
    async def scrape_page(
        self,
        url: str,
        wait_for_selector: Optional[str] = None,
        wait_timeout: int = 15000,  # Reducido de 30s a 15s
        include_html: bool = False,
    ) -> ScrapedContent:
        """
        Scrape completo de una página.
        
        Args:
            url: URL a scrapear
            wait_for_selector: Selector CSS para esperar antes de scrapear
            wait_timeout: Timeout en ms (default 15s, reducido de 30s)
            include_html: Si incluir HTML completo en resultado
        
        Returns:
            ScrapedContent con texto extraído
        """
        # Check cache
        cache_key = self._make_cache_key("scrape", url)
        cached = await self._get_cached(cache_key)
        if cached:
            return ScrapedContent(**cached)
        
        # Enforce rate limit
        await self._wait_for_rate_limit()
        
        page = await self.context.new_page()
        
        try:
            # Navigate
            await page.goto(url, wait_until="domcontentloaded", timeout=wait_timeout)
            
            # Wait for specific selector if provided (con fallback)
            if wait_for_selector:
                try:
                    await page.wait_for_selector(wait_for_selector, timeout=wait_timeout)
                except Exception as e:
                    # Si falla selector específico, continuar con scraping genérico
                    self.logger.warning(
                        "selector_wait_failed_using_fallback",
                        url=url,
                        selector=wait_for_selector,
                        error=str(e),
                    )
                    # Continuar sin error - scraping genérico
            
            # Extract content
            title = await page.title()
            text = await page.inner_text("body")
            html = await page.content() if include_html else None
            
            # Metadata
            metadata = {
                "status": page.url,
                "final_url": page.url,  # Puede ser diferente por redirects
            }
            
            content = ScrapedContent(
                url=url,
                title=title,
                text=text,
                html=html,
                metadata=metadata,
            )
            
            # Cache
            await self._set_cached(
                cache_key,
                content.to_dict(),
                ttl=settings.REDIS_TTL_CONTENT,
            )
            
            self.logger.info(
                "page_scraped",
                url=url,
                text_length=len(text),
            )
            
            return content
        
        finally:
            await page.close()
    
    async def extract_structured_data(
        self,
        url: str,
        selectors: Dict[str, str],
        wait_timeout: int = 30000,
    ) -> Dict[str, Any]:
        """
        Extrae datos estructurados usando selectores CSS.
        
        Args:
            url: URL a scrapear
            selectors: Dict de {campo: selector_css}
            wait_timeout: Timeout en ms
        
        Returns:
            Dict con datos extraídos
        
        Example:
            selectors = {
                "title": "h1.article-title",
                "author": ".author-name",
                "date": "time.published",
                "content": ".article-body",
            }
            data = await adapter.extract_structured_data(url, selectors)
        """
        # Check cache
        cache_key = self._make_cache_key("extract", url, str(sorted(selectors.items())))
        cached = await self._get_cached(cache_key)
        if cached:
            return cached
        
        # Enforce rate limit
        await self._wait_for_rate_limit()
        
        page = await self.context.new_page()
        
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=wait_timeout)
            
            # Extract each field
            data = {}
            for field, selector in selectors.items():
                try:
                    element = await page.query_selector(selector)
                    if element:
                        data[field] = await element.inner_text()
                    else:
                        data[field] = None
                except Exception as e:
                    self.logger.warning(
                        "selector_failed",
                        field=field,
                        selector=selector,
                        error=str(e),
                    )
                    data[field] = None
            
            # Cache
            await self._set_cached(
                cache_key,
                data,
                ttl=settings.REDIS_TTL_CONTENT,
            )
            
            self.logger.info(
                "structured_data_extracted",
                url=url,
                fields=len(data),
            )
            
            return data
        
        finally:
            await page.close()
    
    async def take_screenshot(
        self,
        url: str,
        path: Optional[str] = None,
        full_page: bool = True,
    ) -> str:
        """
        Toma screenshot de una página.
        
        Args:
            url: URL a capturar
            path: Path donde guardar (si None, usa temp)
            full_page: Si capturar página completa
        
        Returns:
            Path del screenshot guardado
        """
        # Enforce rate limit
        await self._wait_for_rate_limit()
        
        page = await self.context.new_page()
        
        try:
            await page.goto(url, wait_until="domcontentloaded")
            
            # Generate path if not provided
            if path is None:
                screenshots_dir = Path("screenshots")
                screenshots_dir.mkdir(exist_ok=True)
                path = str(screenshots_dir / f"{hash(url)}.png")
            
            await page.screenshot(path=path, full_page=full_page)
            
            self.logger.info(
                "screenshot_taken",
                url=url,
                path=path,
            )
            
            return path
        
        finally:
            await page.close()
    
    async def evaluate_js(
        self,
        url: str,
        script: str,
        wait_timeout: int = 30000,
    ) -> Any:
        """
        Ejecuta JavaScript en el contexto de la página.
        
        Args:
            url: URL donde ejecutar
            script: Script JavaScript a ejecutar
            wait_timeout: Timeout en ms
        
        Returns:
            Resultado del script (debe ser JSON-serializable)
        
        Example:
            result = await adapter.evaluate_js(
                "https://example.com",
                "document.querySelectorAll('a').length"
            )
        """
        # Enforce rate limit
        await self._wait_for_rate_limit()
        
        page = await self.context.new_page()
        
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=wait_timeout)
            
            result = await page.evaluate(script)
            
            self.logger.info(
                "js_evaluated",
                url=url,
                script_length=len(script),
            )
            
            return result
        
        finally:
            await page.close()
    
    async def scrape_multiple(
        self,
        urls: List[str],
        max_concurrent: int = 3,
        **kwargs,
    ) -> List[ScrapedContent]:
        """
        Scrape múltiples URLs con concurrencia limitada.
        
        Args:
            urls: Lista de URLs
            max_concurrent: Máximo número de scrapes simultáneos
            **kwargs: Argumentos para scrape_page
        
        Returns:
            Lista de ScrapedContent
        """
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def scrape_with_semaphore(url: str) -> ScrapedContent:
            async with semaphore:
                return await self.scrape_page(url, **kwargs)
        
        tasks = [scrape_with_semaphore(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions
        successful = []
        for result in results:
            if isinstance(result, Exception):
                self.logger.error("scrape_failed", error=str(result))
            else:
                successful.append(result)
        
        self.logger.info(
            "multiple_scrape_completed",
            total=len(urls),
            successful=len(successful),
        )
        
        return successful
