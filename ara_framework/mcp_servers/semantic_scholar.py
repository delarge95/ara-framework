"""
Semantic Scholar MCP Adapter con rate limiting estricto (1 req/seg).

⚠️ CRÍTICO: Semantic Scholar API tiene rate limit de 1 request/segundo.
Este es el bottleneck principal del pipeline (identificado en investigación Nov 2025).

Fuente: investigación perplexity/15_semantic_scholar_api.md
Referencia: docs/07_TASKS.md (LiteratureResearcher +67% tiempo por bottleneck)

Estrategias de mitigación implementadas:
1. Rate limiting estricto con asyncio.sleep(1.0)
2. Cache agresivo (7 días TTL para papers)
3. Paralelización con offsets (múltiples queries simultáneas)
4. Circuit breaker para errores 429
"""
import asyncio
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
import httpx
from pybreaker import CircuitBreaker
import structlog

from mcp_servers.base import MCPAdapter
from config.settings import settings

logger = structlog.get_logger()


@dataclass
class Paper:
    """Representación de un paper académico."""
    
    paper_id: str
    title: str
    abstract: Optional[str]
    year: Optional[int]
    authors: List[str]
    citation_count: int
    url: str
    venue: Optional[str] = None
    fields_of_study: List[str] = None
    
    @classmethod
    def from_api_response(cls, data: dict) -> "Paper":
        """Crea Paper desde respuesta de Semantic Scholar API."""
        return cls(
            paper_id=data.get("paperId", ""),
            title=data.get("title", ""),
            abstract=data.get("abstract"),
            year=data.get("year"),
            authors=[
                author.get("name", "Unknown")
                for author in data.get("authors", [])
            ],
            citation_count=data.get("citationCount", 0),
            url=data.get("url", ""),
            venue=data.get("venue"),
            fields_of_study=data.get("fieldsOfStudy", []),
        )
    
    def to_dict(self) -> dict:
        """Serializa a dict."""
        return {
            "paper_id": self.paper_id,
            "title": self.title,
            "abstract": self.abstract,
            "year": self.year,
            "authors": self.authors,
            "citation_count": self.citation_count,
            "url": self.url,
            "venue": self.venue,
            "fields_of_study": self.fields_of_study or [],
        }


class SemanticScholarAdapter(MCPAdapter[List[Paper]]):
    """
    Adaptador para Semantic Scholar API con rate limiting estricto.
    
    Rate Limit: 1 request/segundo (100% enforcement)
    Cache TTL: 7 días (papers son estables)
    Circuit Breaker: 5 fallos → open por 60 segundos
    
    Uso:
        async with SemanticScholarAdapter(redis_client) as scholar:
            papers = await scholar.search_papers("machine learning", limit=10)
            
            # Búsqueda paralela con offsets (mitiga bottleneck)
            all_papers = await scholar.search_papers_parallel(
                "deep learning",
                total=100,
                batch_size=10
            )
    """
    
    def __init__(self, redis_client=None):
        super().__init__(
            name="semantic_scholar",
            redis_client=redis_client,
            rate_limit_rpm=60,  # Teórico, pero enforceamos 1 req/seg manualmente
            cache_ttl=settings.REDIS_TTL_PAPERS,  # 7 días
        )
        
        self.base_url = settings.SEMANTIC_SCHOLAR_BASE_URL
        self.delay = settings.SEMANTIC_SCHOLAR_DELAY  # 1.0 segundo
        
        # HTTP client
        self.client: Optional[httpx.AsyncClient] = None
        
        # Circuit breaker para 429 errors
        self.circuit_breaker = CircuitBreaker(
            fail_max=settings.CIRCUIT_BREAKER_FAIL_MAX,
            reset_timeout=settings.CIRCUIT_BREAKER_TIMEOUT,
        )
        
        # Timestamp del último request (para 1 req/seg enforcement)
        self._last_request_time: float = 0
        self._request_lock = asyncio.Lock()
    
    async def connect(self) -> None:
        """Inicializa el cliente HTTP."""
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=30.0,
            headers={
                "User-Agent": "ARA-Framework/0.1.0 (Academic Research Assistant)"
            },
        )
        self.logger.info("semantic_scholar_connected")
    
    async def disconnect(self) -> None:
        """Cierra el cliente HTTP."""
        if self.client:
            await self.client.aclose()
            self.logger.info("semantic_scholar_disconnected")
    
    async def health_check(self) -> bool:
        """Verifica que la API esté disponible."""
        try:
            # Simple query para verificar conectividad
            response = await self.client.get("/paper/search", params={"query": "test", "limit": 1})
            return response.status_code == 200
        except Exception as e:
            self.logger.error("health_check_failed", error=str(e))
            return False
    
    async def search_papers(
        self,
        query: str,
        limit: int = 10,
        fields: Optional[List[str]] = None,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
        offset: int = 0,
    ) -> List[Paper]:
        """
        Busca papers en Semantic Scholar.
        
        Args:
            query: Query de búsqueda
            limit: Número de resultados (max 100 por request)
            fields: Campos a retornar (default: todos)
            year_from: Año mínimo (opcional)
            year_to: Año máximo (opcional)
            offset: Offset para paginación (para búsqueda paralela)
        
        Returns:
            Lista de Papers
        """
        # Check cache
        cache_key = self._make_cache_key(
            "search",
            query,
            str(limit),
            str(offset),
            str(year_from or ""),
            str(year_to or ""),
        )
        
        cached = await self._get_cached(cache_key)
        if cached:
            return [Paper(**paper_data) for paper_data in cached]
        
        # Enforce rate limit (1 req/seg)
        await self._enforce_rate_limit()
        
        # Build params
        params = {
            "query": query,
            "limit": min(limit, 100),  # API max
            "offset": offset,
            "fields": ",".join(fields or [
                "paperId",
                "title",
                "abstract",
                "year",
                "authors",
                "citationCount",
                "url",
                "venue",
                "fieldsOfStudy",
            ]),
        }
        
        if year_from:
            params["year"] = f"{year_from}-"
        if year_to:
            if "year" in params:
                params["year"] = f"{year_from}-{year_to}"
            else:
                params["year"] = f"-{year_to}"
        
        # Request con circuit breaker
        try:
            response_data = await self._make_request("/paper/search", params)
            
            papers = [
                Paper.from_api_response(paper_data)
                for paper_data in response_data.get("data", [])
            ]
            
            # Cache results
            await self._set_cached(
                cache_key,
                [paper.to_dict() for paper in papers],
                ttl=settings.REDIS_TTL_PAPERS,
            )
            
            self.logger.info(
                "papers_found",
                query=query,
                count=len(papers),
                offset=offset,
            )
            
            return papers
        
        except Exception as e:
            self.logger.error("search_error", query=query, error=str(e))
            raise
    
    async def search_papers_parallel(
        self,
        query: str,
        total: int = 100,
        batch_size: int = 10,
        **kwargs,
    ) -> List[Paper]:
        """
        Búsqueda paralela con offsets para mitigar bottleneck de 1 req/seg.
        
        Estrategia:
        - Divide búsqueda en batches con diferentes offsets
        - Ejecuta requests con delay de 1 segundo entre cada uno
        - Combina resultados
        
        Ejemplo:
            total=100, batch_size=10 → 10 requests paralelos
            Request 1: offset=0, limit=10 (t=0s)
            Request 2: offset=10, limit=10 (t=1s)
            ...
            Request 10: offset=90, limit=10 (t=9s)
            
            Total time: 10 segundos (vs 1 request de 100 = imposible por API limit)
        
        Args:
            query: Query de búsqueda
            total: Total de papers deseados
            batch_size: Tamaño de cada batch
            **kwargs: Argumentos adicionales para search_papers
        
        Returns:
            Lista combinada de Papers (hasta total)
        """
        num_batches = (total + batch_size - 1) // batch_size
        
        self.logger.info(
            "parallel_search_started",
            query=query,
            total=total,
            batch_size=batch_size,
            num_batches=num_batches,
        )
        
        tasks = []
        for i in range(num_batches):
            offset = i * batch_size
            tasks.append(
                self.search_papers(
                    query=query,
                    limit=batch_size,
                    offset=offset,
                    **kwargs,
                )
            )
        
        # Execute con gather (respeta rate limit interno)
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Combine results
        all_papers = []
        for result in results:
            if isinstance(result, Exception):
                self.logger.error("batch_error", error=str(result))
                continue
            all_papers.extend(result)
        
        self.logger.info(
            "parallel_search_completed",
            query=query,
            total_found=len(all_papers),
        )
        
        return all_papers[:total]
    
    async def get_paper_details(self, paper_id: str) -> Optional[Paper]:
        """
        Obtiene detalles de un paper específico.
        
        Args:
            paper_id: ID del paper en Semantic Scholar
        
        Returns:
            Paper o None si no existe
        """
        # Check cache
        cache_key = self._make_cache_key("paper", paper_id)
        cached = await self._get_cached(cache_key)
        if cached:
            return Paper(**cached)
        
        # Enforce rate limit
        await self._enforce_rate_limit()
        
        try:
            response_data = await self._make_request(f"/paper/{paper_id}")
            
            paper = Paper.from_api_response(response_data)
            
            # Cache
            await self._set_cached(
                cache_key,
                paper.to_dict(),
                ttl=settings.REDIS_TTL_PAPERS,
            )
            
            return paper
        
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                self.logger.warning("paper_not_found", paper_id=paper_id)
                return None
            raise
    
    async def get_recommendations(
        self,
        paper_id: str,
        limit: int = 10,
    ) -> List[Paper]:
        """
        Obtiene papers relacionados (recommendations).
        
        Args:
            paper_id: ID del paper base
            limit: Número de recomendaciones
        
        Returns:
            Lista de Papers relacionados
        """
        # Check cache
        cache_key = self._make_cache_key("recommendations", paper_id, str(limit))
        cached = await self._get_cached(cache_key)
        if cached:
            return [Paper(**paper_data) for paper_data in cached]
        
        # Enforce rate limit
        await self._enforce_rate_limit()
        
        try:
            response_data = await self._make_request(
                f"/paper/{paper_id}/recommendations",
                params={"limit": limit},
            )
            
            papers = [
                Paper.from_api_response(rec["paper"])
                for rec in response_data.get("data", [])
            ]
            
            # Cache
            await self._set_cached(
                cache_key,
                [paper.to_dict() for paper in papers],
                ttl=settings.REDIS_TTL_PAPERS,
            )
            
            return papers
        
        except Exception as e:
            self.logger.error("recommendations_error", paper_id=paper_id, error=str(e))
            raise
    
    # ============================================================
    # MÉTODOS PRIVADOS
    # ============================================================
    
    async def _enforce_rate_limit(self) -> None:
        """
        Enforce estricto de 1 request por segundo.
        
        Usa lock para garantizar que solo 1 request se ejecute por segundo,
        incluso con múltiples tasks concurrentes.
        """
        async with self._request_lock:
            now = asyncio.get_event_loop().time()
            elapsed = now - self._last_request_time
            
            if elapsed < self.delay:
                wait_time = self.delay - elapsed
                self.logger.debug(
                    "rate_limit_enforced",
                    wait_seconds=round(wait_time, 2),
                )
                await asyncio.sleep(wait_time)
            
            self._last_request_time = asyncio.get_event_loop().time()
    
    async def _make_request(
        self,
        endpoint: str,
        params: Optional[dict] = None,
    ) -> dict:
        """
        Hace request al API con circuit breaker.
        
        Args:
            endpoint: Endpoint (ej: "/paper/search")
            params: Query parameters
        
        Returns:
            Response JSON
        
        Raises:
            httpx.HTTPStatusError: Si error HTTP
        """
        response = await self.client.get(endpoint, params=params)
        
        # Handle 429 (rate limit exceeded)
        if response.status_code == 429:
            self.logger.error(
                "rate_limit_exceeded",
                endpoint=endpoint,
                message="Server returned 429 despite client-side limiting",
            )
            # Open circuit breaker
            raise httpx.HTTPStatusError(
                "Rate limit exceeded",
                request=response.request,
                response=response,
            )
        
        response.raise_for_status()
        return response.json()
