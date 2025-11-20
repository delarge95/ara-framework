"""
SearchTool para búsqueda académica con Semantic Scholar.

Fuente: docs/04_ARCHITECTURE.md (Tools Layer)
Referencia: docs/03_AI_MODELS.md (CrewAI tools integration)

Este tool es usado por:
- NicheAnalyst: Búsqueda inicial de tendencias
- LiteratureResearcher: Búsqueda profunda de papers (bottleneck 1 req/seg)
- TechnicalArchitect: Búsqueda de implementaciones técnicas

Features:
- Rate limiting automático (1 req/seg vía adapter)
- Cache agresivo (7 días)
- Búsqueda paralela con offsets
- Filtrado por año y campo de estudio
"""
import asyncio
from typing import List, Optional, Dict, Any
from langchain_core.tools import tool
import structlog

from mcp_servers.semantic_scholar import SemanticScholarAdapter, Paper
from config.settings import settings

logger = structlog.get_logger()


class SearchTool:
    """
    Tool de búsqueda académica integrado con CrewAI.
    
    Uso en Agents:
        agent = Agent(
            tools=[search_tool.search_academic_papers],
            ...
        )
    """
    
    def __init__(self, redis_client=None):
        self.adapter = SemanticScholarAdapter(redis_client=redis_client)
        self._connected = False
    
    async def _ensure_connected(self):
        """Conecta adapter si no está conectado."""
        if not self._connected:
            await self.adapter.connect()
            self._connected = True
    
    @tool("search_academic_papers")
    async def search_academic_papers(
        query: str,
        limit: int = 10,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Busca papers académicos en Semantic Scholar.
        
        Este tool busca papers relevantes usando la API de Semantic Scholar.
        Respeta rate limit de 1 request/segundo automáticamente.
        
        Args:
            query (str): Query de búsqueda (ej: "deep learning for healthcare")
            limit (int): Número máximo de resultados (default 10, max 100)
            year_from (int, optional): Año mínimo de publicación
            year_to (int, optional): Año máximo de publicación
        
        Returns:
            List[Dict]: Lista de papers con estructura:
                - paper_id: ID único en Semantic Scholar
                - title: Título del paper
                - abstract: Resumen (puede ser None)
                - year: Año de publicación
                - authors: Lista de nombres de autores
                - citation_count: Número de citaciones
                - url: URL al paper
                - venue: Venue de publicación (conferencia/journal)
                - fields_of_study: Lista de campos (ej: ["Computer Science", "Medicine"])
        
        Example:
            papers = search_academic_papers(
                "transformers for natural language processing",
                limit=20,
                year_from=2020
            )
        """
        # Ensure adapter connected
        if not self._connected:
            await self.adapter.connect()
            self._connected = True
        
        try:
            papers = await self.adapter.search_papers(
                query=query,
                limit=limit,
                year_from=year_from,
                year_to=year_to,
            )
            
            logger.info(
                "search_tool_executed",
                query=query,
                results_count=len(papers),
                year_from=year_from,
                year_to=year_to,
            )
            
            # Convert to dicts for CrewAI
            return [paper.to_dict() for paper in papers]
        
        except Exception as e:
            logger.error(
                "search_tool_failed",
                query=query,
                error=str(e),
            )
            return []
    
    @tool("search_papers_in_parallel")
    async def search_papers_parallel(
        query: str,
        total: int = 100,
        batch_size: int = 10,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Búsqueda paralela de muchos papers (mitiga bottleneck de 1 req/seg).
        
        Este tool divide la búsqueda en múltiples requests con diferentes offsets,
        permitiendo obtener más resultados en menos tiempo.
        
        Args:
            query (str): Query de búsqueda
            total (int): Total de papers deseados (default 100)
            batch_size (int): Tamaño de cada batch (default 10)
            year_from (int, optional): Año mínimo
            year_to (int, optional): Año máximo
        
        Returns:
            List[Dict]: Lista de papers (hasta total)
        
        Example:
            # Obtener 100 papers en ~10 segundos (vs 100 segundos secuenciales)
            papers = search_papers_parallel(
                "machine learning",
                total=100,
                batch_size=10
            )
        """
        if not self._connected:
            await self.adapter.connect()
            self._connected = True
        
        try:
            papers = await self.adapter.search_papers_parallel(
                query=query,
                total=total,
                batch_size=batch_size,
                year_from=year_from,
                year_to=year_to,
            )
            
            logger.info(
                "parallel_search_completed",
                query=query,
                total_found=len(papers),
            )
            
            return [paper.to_dict() for paper in papers]
        
        except Exception as e:
            logger.error(
                "parallel_search_failed",
                query=query,
                error=str(e),
            )
            return []
    
    @tool("get_paper_details")
    async def get_paper_details(paper_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene detalles completos de un paper específico.
        
        Args:
            paper_id (str): ID del paper en Semantic Scholar
        
        Returns:
            Dict: Datos completos del paper, o None si no existe
        
        Example:
            paper = get_paper_details("abc123def456")
        """
        if not self._connected:
            await self.adapter.connect()
            self._connected = True
        
        try:
            paper = await self.adapter.get_paper_details(paper_id)
            
            if paper:
                logger.info(
                    "paper_details_retrieved",
                    paper_id=paper_id,
                    title=paper.title[:50],
                )
                return paper.to_dict()
            else:
                logger.warning("paper_not_found", paper_id=paper_id)
                return None
        
        except Exception as e:
            logger.error(
                "get_paper_details_failed",
                paper_id=paper_id,
                error=str(e),
            )
            return None
    
    @tool("get_related_papers")
    async def get_related_papers(
        paper_id: str,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Obtiene papers relacionados (recommendations).
        
        Útil para explorar literatura relacionada a partir de un paper semilla.
        
        Args:
            paper_id (str): ID del paper base
            limit (int): Número de recomendaciones (default 10)
        
        Returns:
            List[Dict]: Lista de papers relacionados
        
        Example:
            # Encontrar papers similares
            related = get_related_papers("abc123", limit=20)
        """
        if not self._connected:
            await self.adapter.connect()
            self._connected = True
        
        try:
            papers = await self.adapter.get_recommendations(
                paper_id=paper_id,
                limit=limit,
            )
            
            logger.info(
                "related_papers_found",
                paper_id=paper_id,
                count=len(papers),
            )
            
            return [paper.to_dict() for paper in papers]
        
        except Exception as e:
            logger.error(
                "get_related_papers_failed",
                paper_id=paper_id,
                error=str(e),
            )
            return []
    
    @tool("search_recent_papers")
    async def search_recent_papers(
        query: str,
        years_back: int = 2,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        """
        Busca papers recientes (últimos N años).
        
        Útil para identificar tendencias y estado del arte actual.
        
        Args:
            query (str): Query de búsqueda
            years_back (int): Cuántos años hacia atrás (default 2)
            limit (int): Número de resultados (default 20)
        
        Returns:
            List[Dict]: Papers recientes ordenados por citaciones
        
        Example:
            # Papers de los últimos 2 años
            recent = search_recent_papers(
                "generative AI",
                years_back=2,
                limit=50
            )
        """
        from datetime import datetime
        
        current_year = datetime.now().year
        year_from = current_year - years_back
        
        if not self._connected:
            await self.adapter.connect()
            self._connected = True
        
        try:
            papers = await self.adapter.search_papers(
                query=query,
                limit=limit,
                year_from=year_from,
            )
            
            # Sort by citation count (más citados primero)
            papers_sorted = sorted(
                papers,
                key=lambda p: p.citation_count,
                reverse=True,
            )
            
            logger.info(
                "recent_papers_found",
                query=query,
                year_from=year_from,
                count=len(papers_sorted),
            )
            
            return [paper.to_dict() for paper in papers_sorted]
        
        except Exception as e:
            logger.error(
                "search_recent_failed",
                query=query,
                error=str(e),
            )
            return []
    
    async def close(self):
        """Cierra conexión del adapter."""
        if self._connected:
            await self.adapter.disconnect()
            self._connected = False


# Global instance for easy import
_search_tool_instance = None


def get_search_tool(redis_client=None) -> SearchTool:
    """
    Obtiene instancia global de SearchTool (singleton).
    
    Args:
        redis_client: Cliente Redis (opcional)
    
    Returns:
        SearchTool instance
    """
    global _search_tool_instance
    
    if _search_tool_instance is None:
        _search_tool_instance = SearchTool(redis_client=redis_client)
    
    return _search_tool_instance


# ============================================================
# Module-level tool functions (LangChain @tool decorated)
# ============================================================

@tool("search_recent_papers")
async def search_recent_papers(
    query: str,
    years_back: int = 2,
    limit: int = 20,
) -> List[Dict[str, Any]]:
    """
    Busca papers recientes (últimos N años) con paginación inteligente.
    
    OPTIMIZACIÓN: Si limit > 50, divide en múltiples requests pequeños
    para evitar token limits en modelos como GPT-4o (8K max).
    
    Args:
        query (str): Query de búsqueda
        years_back (int): Cuántos años hacia atrás (default 2)
        limit (int): Número de resultados (default 20, max 100)
    
    Returns:
        List[Dict]: Papers recientes ordenados por citaciones (max 100 total)
    
    Example:
        # Papers de los últimos 2 años (paginado automáticamente)
        recent = search_recent_papers(
            "generative AI",
            years_back=2,
            limit=100  # Se divide en 5 requests de 20
        )
    """
    from datetime import datetime
    
    tool_instance = get_search_tool()
    current_year = datetime.now().year
    year_from = current_year - years_back
    
    if not tool_instance._connected:
        await tool_instance.adapter.connect()
        tool_instance._connected = True
    
    try:
        # PAGINACIÓN: Si limit > 50, dividir en chunks de 20
        # Para evitar token limits (GPT-4o max 8K tokens en request body)
        if limit > 50:
            page_size = 20
            num_pages = min(5, (limit + page_size - 1) // page_size)  # Max 5 páginas (100 total)
            all_papers = []
            
            logger.info(
                "paginated_search_started",
                query=query,
                total_limit=limit,
                page_size=page_size,
                num_pages=num_pages,
            )
            
            for page in range(num_pages):
                papers = await tool_instance.adapter.search_papers(
                    query=query,
                    limit=page_size,
                    offset=page * page_size,
                    year_from=year_from,
                )
                all_papers.extend(papers)
                
                logger.info(
                    "page_fetched",
                    page=page + 1,
                    fetched=len(papers),
                    total_so_far=len(all_papers),
                )
                
                # Si una página devuelve menos resultados, no hay más
                if len(papers) < page_size:
                    break
            
            papers = all_papers[:limit]  # Limitar al número solicitado
        else:
            # Request normal (limit <= 50)
            papers = await tool_instance.adapter.search_papers(
                query=query,
                limit=limit,
                year_from=year_from,
            )
        
        # Sort by citation count (más citados primero)
        papers_sorted = sorted(
            papers,
            key=lambda p: p.citation_count,
            reverse=True,
        )
        
        logger.info(
            "recent_papers_found",
            query=query,
            count=len(papers_sorted),
            years_back=years_back,
            paginated=limit > 50,
        )
        
        return [p.to_dict() for p in papers_sorted]
    
    except Exception as e:
        # Si falla por rate limit, intentar con backoff exponencial
        if "429" in str(e) or "rate limit" in str(e).lower():
            logger.warning(
                "rate_limit_detected_retrying",
                query=query,
                error=str(e),
            )
            return await _search_with_backoff(tool_instance, query, year_from, limit)
        
        logger.error(
            "search_recent_papers_failed",
            query=query,
            error=str(e),
        )
        return []


async def _search_with_backoff(
    tool_instance,
    query: str,
    year_from: int,
    limit: int,
    max_retries: int = 3,
) -> List[Dict[str, Any]]:
    """
    Implementa backoff exponencial para manejar rate limits de Semantic Scholar.
    
    Estrategia:
    - Retry 1: Esperar 2 segundos
    - Retry 2: Esperar 4 segundos
    - Retry 3: Esperar 8 segundos
    
    Args:
        tool_instance: Instancia de SearchTool
        query: Query de búsqueda
        year_from: Año desde el cual buscar
        limit: Número de resultados
        max_retries: Número máximo de reintentos (default 3)
    
    Returns:
        List[Dict]: Papers encontrados o lista vacía si fallan todos los reintentos
    """
    import random
    
    for attempt in range(max_retries):
        try:
            # Calcular tiempo de espera exponencial con jitter
            wait_time = (2 ** attempt) + random.uniform(0, 1)
            
            logger.info(
                "backoff_retry_attempt",
                attempt=attempt + 1,
                max_retries=max_retries,
                wait_seconds=wait_time,
                query=query,
            )
            
            await asyncio.sleep(wait_time)
            
            # Intentar búsqueda nuevamente
            papers = await tool_instance.adapter.search_papers(
                query=query,
                limit=limit,
                year_from=year_from,
            )
            
            # Éxito - ordenar y retornar
            papers_sorted = sorted(
                papers,
                key=lambda p: p.citation_count,
                reverse=True,
            )
            
            logger.info(
                "backoff_retry_success",
                attempt=attempt + 1,
                papers_found=len(papers_sorted),
                query=query,
            )
            
            return [p.to_dict() for p in papers_sorted]
        
        except Exception as e:
            logger.warning(
                "backoff_retry_failed",
                attempt=attempt + 1,
                error=str(e),
                query=query,
            )
            
            # Si es el último intento, log error y retornar vacío
            if attempt == max_retries - 1:
                logger.error(
                    "backoff_max_retries_exceeded",
                    query=query,
                    error=str(e),
                )
                return []
            
            # Si no, continuar al siguiente intento
            continue
    
    return []
