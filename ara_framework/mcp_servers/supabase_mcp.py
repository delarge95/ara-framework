"""
Supabase MCP Adapter para persistencia de análisis y cache histórico.

Fuente: investigación perplexity/18_supabase_for_storage.md
Referencia: docs/04_ARCHITECTURE.md (Data Layer)

Schema:
- papers: Papers académicos con metadatos
- analyses: Análisis completos (niche → report)
- cache_entries: Cache histórico con TTLs
- usage_logs: Logs de uso de modelos (para BudgetManager)

Features:
- PostgreSQL queries con PostgREST
- Storage para PDFs y screenshots
- Real-time subscriptions (opcional)
- Row-level security (RLS)
"""
import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime
import structlog
from supabase import create_client, Client

from mcp_servers.base import MCPAdapter
from config.settings import settings

logger = structlog.get_logger()


@dataclass
class StoredAnalysis:
    """Análisis almacenado en Supabase."""
    
    id: str
    niche_name: str
    created_at: datetime
    status: str  # "pending", "processing", "completed", "failed"
    report_markdown: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def to_dict(self) -> dict:
        """Serializa a dict."""
        return {
            "id": self.id,
            "niche_name": self.niche_name,
            "created_at": self.created_at.isoformat(),
            "status": self.status,
            "report_markdown": self.report_markdown,
            "metadata": self.metadata or {},
        }


class SupabaseAdapter(MCPAdapter[Dict[str, Any]]):
    """
    Adaptador de Supabase para persistencia.
    
    Features:
    - PostgreSQL queries (papers, analyses, logs)
    - Storage para PDFs (papers descargados)
    - Storage para screenshots (debugging)
    - Cache histórico (análisis previos)
    
    Rate Limiting: 100 queries/min (tier free)
    Cache TTL: N/A (Supabase ES la capa de persistencia)
    
    Uso:
        async with SupabaseAdapter() as db:
            # Guardar análisis
            await db.save_analysis({
                "niche_name": "AI in healthcare",
                "status": "completed",
                "report_markdown": "# Report...",
            })
            
            # Buscar análisis previo
            analysis = await db.get_analysis_by_niche("AI in healthcare")
            
            # Guardar paper
            await db.save_paper({
                "paper_id": "abc123",
                "title": "Paper Title",
                "abstract": "...",
            })
            
            # Log de uso (para BudgetManager)
            await db.log_usage({
                "model": "gpt-5",
                "credits": 1.0,
                "timestamp": datetime.now(),
            })
    """
    
    def __init__(self, redis_client=None):
        super().__init__(
            name="supabase",
            redis_client=redis_client,
            rate_limit_rpm=100,  # Free tier limit
            cache_ttl=0,  # No cache (Supabase ES persistencia)
        )
        
        self.client: Optional[Client] = None
        self.supabase_url = settings.SUPABASE_URL
        self.supabase_key = settings.SUPABASE_SERVICE_ROLE_KEY
        
        # Validar que las credenciales estén configuradas
        if not self.supabase_url or not self.supabase_key:
            raise ValueError(
                "Supabase not configured. Set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY in .env"
            )
    
    async def connect(self) -> None:
        """Inicializa cliente de Supabase."""
        if not self.supabase_url or not self.supabase_key:
            self.logger.warning("supabase_skipped", reason="no credentials configured")
            return
        
        # Supabase client es síncrono, pero compatible con async
        self.client = create_client(self.supabase_url, self.supabase_key)
        
        self.logger.info(
            "supabase_connected",
            url=self.supabase_url[:30] + "...",
        )
    
    async def disconnect(self) -> None:
        """Cierra cliente (no necesario, pero por consistencia)."""
        self.client = None
        self.logger.info("supabase_disconnected")
    
    async def health_check(self) -> bool:
        """Verifica conectividad con Supabase."""
        try:
            # Simple query para verificar
            result = await self._execute_query(
                lambda: self.client.table("papers").select("id").limit(1).execute()
            )
            return True
        except Exception as e:
            self.logger.error("health_check_failed", error=str(e))
            return False
    
    # ============================================================
    # ANALYSES
    # ============================================================
    
    async def save_analysis(self, data: Dict[str, Any]) -> str:
        """
        Guarda o actualiza análisis.
        
        Args:
            data: Dict con campos de análisis
        
        Returns:
            ID del análisis
        """
        await self._wait_for_rate_limit()
        
        result = await self._execute_query(
            lambda: self.client.table("analyses").upsert(data).execute()
        )
        
        analysis_id = result.data[0]["id"]
        
        self.logger.info(
            "analysis_saved",
            analysis_id=analysis_id,
            niche=data.get("niche_name"),
        )
        
        return analysis_id
    
    async def get_analysis_by_niche(self, niche_name: str) -> Optional[StoredAnalysis]:
        """
        Busca análisis previo por nombre de niche.
        
        Args:
            niche_name: Nombre del niche
        
        Returns:
            StoredAnalysis si existe, None si no
        """
        await self._wait_for_rate_limit()
        
        result = await self._execute_query(
            lambda: self.client.table("analyses")
            .select("*")
            .eq("niche_name", niche_name)
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )
        
        if not result.data:
            return None
        
        data = result.data[0]
        return StoredAnalysis(
            id=data["id"],
            niche_name=data["niche_name"],
            created_at=datetime.fromisoformat(data["created_at"]),
            status=data["status"],
            report_markdown=data.get("report_markdown"),
            metadata=data.get("metadata", {}),
        )
    
    async def get_analysis_by_id(self, analysis_id: str) -> Optional[StoredAnalysis]:
        """
        Obtiene análisis por ID.
        
        Args:
            analysis_id: UUID del análisis
        
        Returns:
            StoredAnalysis si existe, None si no
        """
        await self._wait_for_rate_limit()
        
        result = await self._execute_query(
            lambda: self.client.table("analyses")
            .select("*")
            .eq("id", analysis_id)
            .single()
            .execute()
        )
        
        if not result.data:
            return None
        
        data = result.data
        return StoredAnalysis(
            id=data["id"],
            niche_name=data["niche_name"],
            created_at=datetime.fromisoformat(data["created_at"]),
            status=data["status"],
            report_markdown=data.get("report_markdown"),
            metadata=data.get("metadata", {}),
        )
    
    async def list_analyses(
        self,
        limit: int = 50,
        offset: int = 0,
    ) -> List[StoredAnalysis]:
        """
        Lista análisis recientes.
        
        Args:
            limit: Número de resultados
            offset: Offset para paginación
        
        Returns:
            Lista de StoredAnalysis
        """
        await self._wait_for_rate_limit()
        
        result = await self._execute_query(
            lambda: self.client.table("analyses")
            .select("*")
            .order("created_at", desc=True)
            .range(offset, offset + limit - 1)
            .execute()
        )
        
        analyses = []
        for data in result.data:
            analyses.append(
                StoredAnalysis(
                    id=data["id"],
                    niche_name=data["niche_name"],
                    created_at=datetime.fromisoformat(data["created_at"]),
                    status=data["status"],
                    report_markdown=data.get("report_markdown"),
                    metadata=data.get("metadata", {}),
                )
            )
        
        return analyses
    
    # ============================================================
    # PAPERS
    # ============================================================
    
    async def save_paper(self, data: Dict[str, Any]) -> str:
        """
        Guarda paper académico.
        
        Args:
            data: Dict con campos del paper
        
        Returns:
            ID del paper (paper_id de Semantic Scholar)
        """
        await self._wait_for_rate_limit()
        
        result = await self._execute_query(
            lambda: self.client.table("papers").upsert(data).execute()
        )
        
        paper_id = result.data[0]["paper_id"]
        
        self.logger.info(
            "paper_saved",
            paper_id=paper_id,
            title=data.get("title", "")[:50],
        )
        
        return paper_id
    
    async def get_paper(self, paper_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene paper por ID.
        
        Args:
            paper_id: ID del paper (Semantic Scholar)
        
        Returns:
            Dict con datos del paper, None si no existe
        """
        await self._wait_for_rate_limit()
        
        result = await self._execute_query(
            lambda: self.client.table("papers")
            .select("*")
            .eq("paper_id", paper_id)
            .single()
            .execute()
        )
        
        return result.data if result.data else None
    
    async def search_papers(
        self,
        query: str,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Busca papers por texto (full-text search).
        
        Args:
            query: Query de búsqueda
            limit: Número de resultados
        
        Returns:
            Lista de papers
        """
        await self._wait_for_rate_limit()
        
        # Full-text search en título y abstract
        result = await self._execute_query(
            lambda: self.client.table("papers")
            .select("*")
            .or_(f"title.ilike.%{query}%,abstract.ilike.%{query}%")
            .limit(limit)
            .execute()
        )
        
        return result.data
    
    # ============================================================
    # USAGE LOGS (para BudgetManager)
    # ============================================================
    
    async def log_usage(self, data: Dict[str, Any]) -> str:
        """
        Registra uso de modelo (para tracking de créditos).
        
        Args:
            data: Dict con campos de uso (model, credits, timestamp, metadata)
        
        Returns:
            ID del log
        """
        await self._wait_for_rate_limit()
        
        result = await self._execute_query(
            lambda: self.client.table("usage_logs").insert(data).execute()
        )
        
        log_id = result.data[0]["id"]
        
        self.logger.debug(
            "usage_logged",
            log_id=log_id,
            model=data.get("model"),
            credits=data.get("credits"),
        )
        
        return log_id
    
    async def get_usage_stats(
        self,
        start_date: datetime,
        end_date: datetime,
    ) -> Dict[str, Any]:
        """
        Obtiene estadísticas de uso en un rango de fechas.
        
        Args:
            start_date: Fecha inicio
            end_date: Fecha fin
        
        Returns:
            Dict con estadísticas (total_credits, requests_by_model, etc.)
        """
        await self._wait_for_rate_limit()
        
        result = await self._execute_query(
            lambda: self.client.table("usage_logs")
            .select("*")
            .gte("timestamp", start_date.isoformat())
            .lte("timestamp", end_date.isoformat())
            .execute()
        )
        
        logs = result.data
        
        # Aggregate stats
        stats = {
            "total_credits": sum(log.get("credits", 0) for log in logs),
            "total_requests": len(logs),
            "requests_by_model": {},
            "credits_by_model": {},
        }
        
        for log in logs:
            model = log.get("model", "unknown")
            credits = log.get("credits", 0)
            
            stats["requests_by_model"][model] = (
                stats["requests_by_model"].get(model, 0) + 1
            )
            stats["credits_by_model"][model] = (
                stats["credits_by_model"].get(model, 0) + credits
            )
        
        return stats
    
    # ============================================================
    # STORAGE (PDFs, Screenshots)
    # ============================================================
    
    async def upload_file(
        self,
        bucket: str,
        file_path: str,
        destination_path: str,
    ) -> str:
        """
        Sube archivo a Supabase Storage.
        
        Args:
            bucket: Nombre del bucket (ej: "pdfs", "screenshots")
            file_path: Path local del archivo
            destination_path: Path destino en Storage
        
        Returns:
            URL pública del archivo
        """
        await self._wait_for_rate_limit()
        
        with open(file_path, "rb") as f:
            file_data = f.read()
        
        result = await self._execute_query(
            lambda: self.client.storage.from_(bucket).upload(
                destination_path,
                file_data,
            )
        )
        
        # Get public URL
        public_url = self.client.storage.from_(bucket).get_public_url(destination_path)
        
        self.logger.info(
            "file_uploaded",
            bucket=bucket,
            destination=destination_path,
            url=public_url[:50],
        )
        
        return public_url
    
    async def download_file(
        self,
        bucket: str,
        file_path: str,
    ) -> bytes:
        """
        Descarga archivo desde Supabase Storage.
        
        Args:
            bucket: Nombre del bucket
            file_path: Path del archivo en Storage
        
        Returns:
            Bytes del archivo
        """
        await self._wait_for_rate_limit()
        
        result = await self._execute_query(
            lambda: self.client.storage.from_(bucket).download(file_path)
        )
        
        return result
    
    # ============================================================
    # MÉTODOS PRIVADOS
    # ============================================================
    
    async def _execute_query(self, query_func):
        """
        Ejecuta query síncrono de Supabase en thread pool.
        
        Args:
            query_func: Lambda que ejecuta query
        
        Returns:
            Resultado de la query
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, query_func)
