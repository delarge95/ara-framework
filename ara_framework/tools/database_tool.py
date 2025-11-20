"""
DatabaseTool para persistencia y consultas en Supabase.

Fuente: docs/04_ARCHITECTURE.md (Tools Layer)
Referencia: docs/03_AI_MODELS.md (CrewAI tools integration)

Este tool es usado por:
- Todos los agents: Persistencia de resultados intermedios
- Orchestrator: Guardado de análisis completos
- BudgetManager: Logs de uso de modelos

Features:
- PostgreSQL queries (papers, analyses, logs)
- Storage para PDFs y screenshots
- Cache histórico (análisis previos)
- Rate limiting (100 queries/min)
"""
import asyncio
from typing import Optional, Dict, Any, List
from datetime import datetime
from langchain_core.tools import tool
import structlog

from mcp_servers.supabase_mcp import SupabaseAdapter, StoredAnalysis
from config.settings import settings

logger = structlog.get_logger()


class DatabaseTool:
    """
    Tool de database integrado con CrewAI.
    
    Uso en Agents:
        agent = Agent(
            tools=[
                database_tool.save_analysis,
                database_tool.query_papers,
                database_tool.upload_file,
            ],
            ...
        )
    """
    
    def __init__(self, redis_client=None):
        try:
            self.adapter = SupabaseAdapter(redis_client=redis_client)
            self._connected = False
        except Exception as e:
            logger.warning("database_tool_disabled", reason="Supabase not configured", error=str(e))
            self.adapter = None
            self._connected = False
    
    async def _ensure_connected(self):
        """Conecta adapter si no está conectado."""
        if not self.adapter:
            logger.warning("database_tool_skipped", reason="Supabase not configured")
            return False
        if not self._connected:
            await self.adapter.connect()
            self._connected = True
        return True
    
    # ============================================================
    # ANALYSES
    # ============================================================
    
    @tool("save_analysis")
    async def save_analysis(
        niche_name: str,
        status: str,
        report_markdown: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Guarda o actualiza un análisis en la base de datos.
        
        Args:
            niche_name (str): Nombre del niche analizado
            status (str): Estado del análisis ("pending", "processing", "completed", "failed")
            report_markdown (str, optional): Reporte completo en Markdown
            metadata (dict, optional): Metadata adicional (papers usados, tiempos, etc.)
        
        Returns:
            str: ID del análisis guardado
        
        Example:
            analysis_id = save_analysis(
                niche_name="AI in healthcare",
                status="completed",
                report_markdown="# Analysis Report\\n\\n...",
                metadata={
                    "papers_analyzed": 50,
                    "execution_time": 3600,
                    "credits_used": 15.5,
                }
            )
        """
        tool_instance = _get_database_tool_instance()
        await tool_instance._ensure_connected()
        
        try:
            analysis_id = await tool_instance.adapter.save_analysis({
                "niche_name": niche_name,
                "status": status,
                "report_markdown": report_markdown,
                "metadata": metadata or {},
                "created_at": datetime.now().isoformat(),
            })
            
            logger.info(
                "analysis_saved",
                analysis_id=analysis_id,
                niche_name=niche_name,
                status=status,
            )
            
            return analysis_id
        
        except Exception as e:
            logger.error(
                "save_analysis_failed",
                niche_name=niche_name,
                error=str(e),
            )
            return ""
    
    @tool("get_previous_analysis")
    async def get_previous_analysis(niche_name: str) -> Optional[Dict[str, Any]]:
        """
        Busca análisis previo por nombre de niche.
        
        Útil para evitar reanalizar el mismo niche.
        
        Args:
            niche_name (str): Nombre del niche
        
        Returns:
            Dict: Análisis previo o None si no existe
        
        Example:
            previous = get_previous_analysis("AI in healthcare")
            
            if previous and previous["status"] == "completed":
                print(f"Analysis already exists from {previous['created_at']}")
                return previous["report_markdown"]
        """
        tool_instance = _get_database_tool_instance()
        await tool_instance._ensure_connected()
        
        try:
            analysis = await tool_instance.adapter.get_analysis_by_niche(niche_name)
            
            if analysis:
                logger.info(
                    "previous_analysis_found",
                    niche_name=niche_name,
                    status=analysis.status,
                    created_at=analysis.created_at,
                )
                return analysis.to_dict()
            else:
                logger.info(
                    "no_previous_analysis",
                    niche_name=niche_name,
                )
                return None
        
        except Exception as e:
            logger.error(
                "get_previous_analysis_failed",
                niche_name=niche_name,
                error=str(e),
            )
            return None
    
    @tool("list_recent_analyses")
    async def list_recent_analyses(
        limit: int = 10,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """
        Lista análisis recientes.
        
        Args:
            limit (int): Número de resultados
            offset (int): Offset para paginación
        
        Returns:
            List[Dict]: Lista de análisis recientes
        
        Example:
            recent = list_recent_analyses(limit=20)
            
            for analysis in recent:
                print(f"{analysis['niche_name']}: {analysis['status']}")
        """
        tool_instance = _get_database_tool_instance()
        await tool_instance._ensure_connected()
        
        try:
            analyses = await tool_instance.adapter.list_analyses(
                limit=limit,
                offset=offset,
            )
            
            logger.info(
                "analyses_listed",
                count=len(analyses),
            )
            
            return [a.to_dict() for a in analyses]
        
        except Exception as e:
            logger.error(
                "list_analyses_failed",
                error=str(e),
            )
            return []
    
    # ============================================================
    # PAPERS
    # ============================================================
    
    @tool("save_paper")
    async def save_paper(
        paper_id: str,
        title: str,
        abstract: Optional[str] = None,
        authors: Optional[List[str]] = None,
        year: Optional[int] = None,
        citation_count: int = 0,
        url: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Guarda paper académico en la base de datos.
        
        Args:
            paper_id (str): ID del paper (Semantic Scholar)
            title (str): Título del paper
            abstract (str, optional): Abstract/resumen
            authors (list, optional): Lista de autores
            year (int, optional): Año de publicación
            citation_count (int): Número de citaciones
            url (str, optional): URL al paper
            metadata (dict, optional): Metadata adicional
        
        Returns:
            str: ID del paper guardado
        
        Example:
            paper_id = save_paper(
                paper_id="abc123",
                title="Attention Is All You Need",
                abstract="The dominant...",
                authors=["Vaswani", "Shazeer", "Parmar"],
                year=2017,
                citation_count=50000,
                url="https://arxiv.org/abs/1706.03762"
            )
        """
        tool_instance = _get_database_tool_instance()
        await tool_instance._ensure_connected()
        
        try:
            saved_id = await tool_instance.adapter.save_paper({
                "paper_id": paper_id,
                "title": title,
                "abstract": abstract,
                "authors": authors or [],
                "year": year,
                "citation_count": citation_count,
                "url": url,
                "metadata": metadata or {},
            })
            
            logger.info(
                "paper_saved",
                paper_id=paper_id,
                title=title[:50],
            )
            
            return saved_id
        
        except Exception as e:
            logger.error(
                "save_paper_failed",
                paper_id=paper_id,
                error=str(e),
            )
            return ""
    
    @tool("query_papers")
    async def query_papers(
        query: str,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Busca papers en la base de datos por texto.
        
        Usa full-text search en título y abstract.
        
        Args:
            query (str): Query de búsqueda
            limit (int): Número de resultados
        
        Returns:
            List[Dict]: Papers encontrados
        
        Example:
            papers = query_papers("transformers", limit=20)
            
            for paper in papers:
                print(f"{paper['title']} ({paper['year']})")
        """
        tool_instance = _get_database_tool_instance()
        await tool_instance._ensure_connected()
        
        try:
            papers = await tool_instance.adapter.search_papers(
                query=query,
                limit=limit,
            )
            
            logger.info(
                "papers_queried",
                query=query,
                results=len(papers),
            )
            
            return papers
        
        except Exception as e:
            logger.error(
                "query_papers_failed",
                query=query,
                error=str(e),
            )
            return []
    
    @tool("get_paper_by_id")
    async def get_paper_by_id(paper_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene paper por ID desde la base de datos.
        
        Args:
            paper_id (str): ID del paper
        
        Returns:
            Dict: Datos del paper o None si no existe
        
        Example:
            paper = get_paper_by_id("abc123")
            
            if paper:
                print(f"Title: {paper['title']}")
        """
        tool_instance = _get_database_tool_instance()
        await tool_instance._ensure_connected()
        
        try:
            paper = await tool_instance.adapter.get_paper(paper_id)
            
            if paper:
                logger.info(
                    "paper_retrieved",
                    paper_id=paper_id,
                )
            else:
                logger.info(
                    "paper_not_found",
                    paper_id=paper_id,
                )
            
            return paper
        
        except Exception as e:
            logger.error(
                "get_paper_failed",
                paper_id=paper_id,
                error=str(e),
            )
            return None
    
    # ============================================================
    # STORAGE (Files)
    # ============================================================
    
    @tool("upload_file")
    async def upload_file(
        bucket: str,
        file_path: str,
        destination_path: str,
    ) -> str:
        """
        Sube archivo a Supabase Storage.
        
        Args:
            bucket (str): Nombre del bucket ("pdfs", "screenshots", etc.)
            file_path (str): Path local del archivo
            destination_path (str): Path destino en Storage
        
        Returns:
            str: URL pública del archivo
        
        Example:
            url = upload_file(
                bucket="pdfs",
                file_path="papers/downloaded.pdf",
                destination_path="analysis_123/paper1.pdf"
            )
        """
        tool_instance = _get_database_tool_instance()
        await tool_instance._ensure_connected()
        
        try:
            public_url = await tool_instance.adapter.upload_file(
                bucket=bucket,
                file_path=file_path,
                destination_path=destination_path,
            )
            
            logger.info(
                "file_uploaded",
                bucket=bucket,
                destination=destination_path,
                url=public_url[:50],
            )
            
            return public_url
        
        except Exception as e:
            logger.error(
                "upload_file_failed",
                bucket=bucket,
                file_path=file_path,
                error=str(e),
            )
            return ""
    
    @tool("download_file")
    async def download_file(
        bucket: str,
        file_path: str,
    ) -> bytes:
        """
        Descarga archivo desde Supabase Storage.
        
        Args:
            bucket (str): Nombre del bucket
            file_path (str): Path del archivo en Storage
        
        Returns:
            bytes: Contenido del archivo
        
        Example:
            content = download_file(
                bucket="pdfs",
                file_path="analysis_123/paper1.pdf"
            )
            
            with open("local_copy.pdf", "wb") as f:
                f.write(content)
        """
        tool_instance = _get_database_tool_instance()
        await tool_instance._ensure_connected()
        
        try:
            content = await tool_instance.adapter.download_file(
                bucket=bucket,
                file_path=file_path,
            )
            
            logger.info(
                "file_downloaded",
                bucket=bucket,
                file_path=file_path,
                size=len(content),
            )
            
            return content
        
        except Exception as e:
            logger.error(
                "download_file_failed",
                bucket=bucket,
                file_path=file_path,
                error=str(e),
            )
            return b""
    
    # ============================================================
    # USAGE LOGS (for BudgetManager)
    # ============================================================
    
    @tool("log_model_usage")
    async def log_model_usage(
        model: str,
        credits: float,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Registra uso de modelo para tracking de créditos.
        
        Args:
            model (str): Nombre del modelo ("gpt-5", "claude-sonnet-4.5", etc.)
            credits (float): Créditos consumidos
            metadata (dict, optional): Metadata adicional (task, duration, etc.)
        
        Returns:
            str: ID del log
        
        Example:
            log_id = log_model_usage(
                model="gpt-5",
                credits=1.0,
                metadata={
                    "task": "literature_research",
                    "duration": 120,
                    "tokens": 5000,
                }
            )
        """
        tool_instance = _get_database_tool_instance()
        await tool_instance._ensure_connected()
        
        try:
            log_id = await tool_instance.adapter.log_usage({
                "model": model,
                "credits": credits,
                "timestamp": datetime.now().isoformat(),
                "metadata": metadata or {},
            })
            
            logger.info(
                "usage_logged",
                log_id=log_id,
                model=model,
                credits=credits,
            )
            
            return log_id
        
        except Exception as e:
            logger.error(
                "log_usage_failed",
                model=model,
                error=str(e),
            )
            return ""
    
    @tool("get_usage_statistics")
    async def get_usage_statistics(
        days_back: int = 30,
    ) -> Dict[str, Any]:
        """
        Obtiene estadísticas de uso de modelos.
        
        Args:
            days_back (int): Días hacia atrás para analizar
        
        Returns:
            Dict: Estadísticas con estructura:
                - total_credits: Total de créditos usados
                - total_requests: Total de requests
                - requests_by_model: Dict de {model: count}
                - credits_by_model: Dict de {model: credits}
        
        Example:
            stats = get_usage_statistics(days_back=7)
            
            print(f"Last week: {stats['total_credits']} credits used")
            print(f"Most used model: {max(stats['requests_by_model'], key=stats['requests_by_model'].get)}")
        """
        tool_instance = _get_database_tool_instance()
        await tool_instance._ensure_connected()
        
        try:
            from datetime import timedelta
            
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            stats = await tool_instance.adapter.get_usage_stats(
                start_date=start_date,
                end_date=end_date,
            )
            
            logger.info(
                "usage_stats_retrieved",
                days_back=days_back,
                total_credits=stats["total_credits"],
                total_requests=stats["total_requests"],
            )
            
            return stats
        
        except Exception as e:
            logger.error(
                "get_usage_stats_failed",
                error=str(e),
            )
            return {
                "total_credits": 0,
                "total_requests": 0,
                "requests_by_model": {},
                "credits_by_model": {},
            }
    
    async def close(self):
        """Cierra conexión del adapter."""
        if self._connected:
            await self.adapter.disconnect()
            self._connected = False


# Global instance for singleton pattern
_database_tool_instance = None


def _get_database_tool_instance(redis_client=None) -> DatabaseTool:
    """
    Obtiene instancia global de DatabaseTool (singleton).
    
    Args:
        redis_client: Cliente Redis (opcional)
    
    Returns:
        DatabaseTool instance
    """
    global _database_tool_instance
    
    if _database_tool_instance is None:
        _database_tool_instance = DatabaseTool(redis_client=redis_client)
    
    return _database_tool_instance


def get_database_tool(redis_client=None) -> DatabaseTool:
    """
    Alias público para obtener instancia.
    
    Args:
        redis_client: Cliente Redis (opcional)
    
    Returns:
        DatabaseTool instance
    """
    return _get_database_tool_instance(redis_client)


# ============================================================
# Module-level tool functions (LangChain @tool decorated)
# ============================================================

@tool("save_analysis")
async def save_analysis(
    niche_name: str,
    status: str,
    report_markdown: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Guarda o actualiza un análisis en la base de datos.
    
    Args:
        niche_name (str): Nombre del niche analizado
        status (str): Estado del análisis ("pending", "processing", "completed", "failed")
        report_markdown (str, optional): Reporte completo en Markdown
        metadata (dict, optional): Metadata adicional (papers usados, tiempos, etc.)
    
    Returns:
        str: ID del análisis guardado
    
    Example:
        analysis_id = save_analysis(
            niche_name="AI in healthcare",
            status="completed",
            report_markdown="# Analysis Report\\n\\n...",
            metadata={
                "papers_analyzed": 50,
                "execution_time": 3600,
                "credits_used": 15.5,
            }
        )
    """
    from datetime import datetime
    
    tool_instance = _get_database_tool_instance()
    await tool_instance._ensure_connected()
    
    try:
        analysis_id = await tool_instance.adapter.save_analysis({
            "niche_name": niche_name,
            "status": status,
            "report_markdown": report_markdown,
            "metadata": metadata or {},
            "created_at": datetime.now().isoformat(),
        })
        
        logger.info(
            "analysis_saved",
            analysis_id=analysis_id,
            niche_name=niche_name,
            status=status,
        )
        
        return analysis_id
    
    except Exception as e:
        logger.error(
            "save_analysis_failed",
            niche_name=niche_name,
            error=str(e),
        )
        return ""
