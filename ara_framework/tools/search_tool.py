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
    
    @tool("Search Academic Papers")
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
    
    @tool("Search Papers in Parallel")
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
    
    @tool("Get Paper Details")
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
    
    @tool("Get Related Papers")
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
    
    @tool("Search Recent Papers")
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
