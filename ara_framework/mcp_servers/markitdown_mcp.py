"""
MarkItDown MCP Adapter para conversión de PDFs académicos a Markdown.

Fuente: investigación perplexity/21_pdf_processing_tools.md
Referencia: docs/04_ARCHITECTURE.md (Data Ingestion Layer)

Estrategia híbrida:
1. Intenta MarkItDown primero (mejor calidad para PDFs modernos)
2. Fallback a PyMuPDF si MarkItDown falla
3. Extracción de metadatos (autor, título, año)
4. Limpieza de texto (elimina headers/footers repetitivos)
"""
import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from pathlib import Path
import tempfile
import structlog

# MarkItDown imports - lazy loading para evitar problemas de importación
MARKITDOWN_AVAILABLE = False
MarkItDown = None

def _lazy_load_markitdown():
    """Carga MarkItDown solo cuando se necesita."""
    global MARKITDOWN_AVAILABLE, MarkItDown
    if MarkItDown is None:
        try:
            from markitdown import MarkItDown as _MarkItDown
            MarkItDown = _MarkItDown
            MARKITDOWN_AVAILABLE = True
        except Exception as e:
            MARKITDOWN_AVAILABLE = False
            structlog.get_logger().warning("markitdown_not_available", error=str(e))
    return MARKITDOWN_AVAILABLE

# PyMuPDF fallback imports
try:
    import pymupdf as fitz
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False
    structlog.get_logger().warning("pymupdf_not_installed")

from mcp_servers.base import MCPAdapter
from config.settings import settings

logger = structlog.get_logger()


@dataclass
class ProcessedPDF:
    """Resultado del procesamiento de PDF."""
    
    file_path: str
    markdown: str
    metadata: Dict[str, Any]
    page_count: int
    method_used: str  # "markitdown" o "pymupdf"
    
    def to_dict(self) -> dict:
        """Serializa a dict."""
        return {
            "file_path": self.file_path,
            "markdown": self.markdown,
            "metadata": self.metadata,
            "page_count": self.page_count,
            "method_used": self.method_used,
        }


class MarkItDownAdapter(MCPAdapter[ProcessedPDF]):
    """
    Adaptador para conversión de PDFs académicos a Markdown.
    
    Estrategia híbrida:
    - MarkItDown (Microsoft): Mejor para PDFs modernos con estructura
    - PyMuPDF: Fallback para PDFs legacy o con problemas
    
    Features:
    - Extracción de metadatos (autor, título, año)
    - Limpieza automática de headers/footers
    - Detección de secciones (Abstract, Introduction, etc.)
    - Cache agresivo (PDFs no cambian)
    
    Rate Limiting: 5 conversiones/min (CPU-intensive)
    Cache TTL: 7 días (mismo que papers)
    
    Uso:
        async with MarkItDownAdapter(redis_client) as md:
            # Conversión simple
            result = await md.convert_pdf("paper.pdf")
            
            # Conversión con limpieza
            result = await md.convert_pdf(
                "paper.pdf",
                clean_headers=True,
                extract_sections=True,
            )
            
            # Batch conversion
            results = await md.convert_multiple([
                "paper1.pdf",
                "paper2.pdf",
            ])
    """
    
    def __init__(self, redis_client=None):
        super().__init__(
            name="markitdown",
            redis_client=redis_client,
            rate_limit_rpm=5,  # Conservative (CPU-intensive)
            cache_ttl=settings.REDIS_TTL_PAPERS,  # 7 días
        )
        
        # MarkItDown converter - lazy loading
        self.markitdown = None
        self._markitdown_loaded = False
    
    def _ensure_markitdown(self):
        """Inicializa MarkItDown si está disponible y no ha sido cargado."""
        if not self._markitdown_loaded:
            if _lazy_load_markitdown() and MarkItDown:
                self.markitdown = MarkItDown()
            self._markitdown_loaded = True
        return self.markitdown is not None
    
    async def connect(self) -> None:
        """Valida que al menos un conversor esté disponible."""
        # Check si algún converter está disponible (lazy load para MarkItDown)
        markitdown_ok = self._ensure_markitdown()
        
        if not markitdown_ok and not PYMUPDF_AVAILABLE:
            raise RuntimeError(
                "No PDF converter available. Install markitdown or pymupdf."
            )
        
        self.logger.info(
            "markitdown_connected",
            markitdown_available=markitdown_ok,
            pymupdf_available=PYMUPDF_AVAILABLE,
        )
    
    async def disconnect(self) -> None:
        """Nada que cerrar."""
        self.logger.info("markitdown_disconnected")
    
    async def health_check(self) -> bool:
        """Verifica disponibilidad de conversores."""
        return self._ensure_markitdown() or PYMUPDF_AVAILABLE
    
    async def convert_pdf(
        self,
        file_path: str,
        clean_headers: bool = True,
        extract_sections: bool = True,
    ) -> ProcessedPDF:
        """
        Convierte PDF a Markdown usando estrategia híbrida.
        
        Args:
            file_path: Path al archivo PDF
            clean_headers: Si limpiar headers/footers repetitivos
            extract_sections: Si detectar secciones (Abstract, etc.)
        
        Returns:
            ProcessedPDF con markdown y metadatos
        """
        # Check cache
        cache_key = self._make_cache_key(
            "convert",
            file_path,
            str(clean_headers),
            str(extract_sections),
        )
        cached = await self._get_cached(cache_key)
        if cached:
            return ProcessedPDF(**cached)
        
        # Enforce rate limit
        await self._wait_for_rate_limit()
        
        # Validate file exists
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"PDF not found: {file_path}")
        
        # Try MarkItDown first (lazy load)
        if self._ensure_markitdown():
            try:
                result = await self._convert_with_markitdown(
                    file_path,
                    clean_headers,
                    extract_sections,
                )
                
                # Cache
                await self._set_cached(
                    cache_key,
                    result.to_dict(),
                    ttl=settings.REDIS_TTL_PAPERS,
                )
                
                return result
            
            except Exception as e:
                self.logger.warning(
                    "markitdown_failed",
                    file_path=file_path,
                    error=str(e),
                    fallback="pymupdf",
                )
        
        # Fallback to PyMuPDF
        if PYMUPDF_AVAILABLE:
            result = await self._convert_with_pymupdf(
                file_path,
                clean_headers,
                extract_sections,
            )
            
            # Cache
            await self._set_cached(
                cache_key,
                result.to_dict(),
                ttl=settings.REDIS_TTL_PAPERS,
            )
            
            return result
        
        raise RuntimeError("No PDF converter succeeded")
    
    async def convert_multiple(
        self,
        file_paths: List[str],
        max_concurrent: int = 2,
        **kwargs,
    ) -> List[ProcessedPDF]:
        """
        Convierte múltiples PDFs con concurrencia limitada.
        
        Args:
            file_paths: Lista de paths a PDFs
            max_concurrent: Máximo conversiones simultáneas
            **kwargs: Argumentos para convert_pdf
        
        Returns:
            Lista de ProcessedPDF
        """
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def convert_with_semaphore(path: str) -> ProcessedPDF:
            async with semaphore:
                return await self.convert_pdf(path, **kwargs)
        
        tasks = [convert_with_semaphore(path) for path in file_paths]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter exceptions
        successful = []
        for result in results:
            if isinstance(result, Exception):
                self.logger.error("conversion_failed", error=str(result))
            else:
                successful.append(result)
        
        self.logger.info(
            "batch_conversion_completed",
            total=len(file_paths),
            successful=len(successful),
        )
        
        return successful
    
    async def extract_text_only(self, file_path: str) -> str:
        """
        Extrae solo texto sin markdown (útil para búsquedas).
        
        Args:
            file_path: Path al PDF
        
        Returns:
            Texto plano extraído
        """
        result = await self.convert_pdf(file_path, clean_headers=False, extract_sections=False)
        
        # Remove markdown formatting
        text = result.markdown
        text = text.replace("#", "")
        text = text.replace("**", "")
        text = text.replace("*", "")
        text = text.replace("_", "")
        
        return text.strip()
    
    # ============================================================
    # MÉTODOS PRIVADOS
    # ============================================================
    
    async def _convert_with_markitdown(
        self,
        file_path: str,
        clean_headers: bool,
        extract_sections: bool,
    ) -> ProcessedPDF:
        """Conversión usando MarkItDown."""
        # Asegurar que MarkItDown está cargado
        if not self._ensure_markitdown():
            raise RuntimeError("MarkItDown not available")
        
        # MarkItDown es síncrono, ejecutar en thread pool
        loop = asyncio.get_event_loop()
        
        def sync_convert():
            result = self.markitdown.convert(file_path)
            return result.text_content
        
        markdown = await loop.run_in_executor(None, sync_convert)
        
        # Extract metadata (si disponible)
        metadata = await self._extract_metadata_pymupdf(file_path)
        
        # Clean headers if requested
        if clean_headers:
            markdown = self._clean_repetitive_headers(markdown)
        
        # Extract sections if requested
        if extract_sections:
            sections = self._extract_sections(markdown)
            metadata["sections"] = sections
        
        # Page count (usar PyMuPDF si disponible)
        page_count = metadata.get("page_count", 0)
        
        self.logger.info(
            "pdf_converted",
            file_path=file_path,
            method="markitdown",
            pages=page_count,
            markdown_length=len(markdown),
        )
        
        return ProcessedPDF(
            file_path=file_path,
            markdown=markdown,
            metadata=metadata,
            page_count=page_count,
            method_used="markitdown",
        )
    
    async def _convert_with_pymupdf(
        self,
        file_path: str,
        clean_headers: bool,
        extract_sections: bool,
    ) -> ProcessedPDF:
        """Conversión usando PyMuPDF."""
        loop = asyncio.get_event_loop()
        
        def sync_convert():
            doc = fitz.open(file_path)
            
            # Extract text from all pages
            text_parts = []
            for page in doc:
                text_parts.append(page.get_text())
            
            markdown = "\n\n".join(text_parts)
            
            # Extract metadata
            metadata = {
                "title": doc.metadata.get("title", ""),
                "author": doc.metadata.get("author", ""),
                "subject": doc.metadata.get("subject", ""),
                "creator": doc.metadata.get("creator", ""),
                "page_count": len(doc),
            }
            
            doc.close()
            
            return markdown, metadata
        
        markdown, metadata = await loop.run_in_executor(None, sync_convert)
        
        # Clean headers
        if clean_headers:
            markdown = self._clean_repetitive_headers(markdown)
        
        # Extract sections
        if extract_sections:
            sections = self._extract_sections(markdown)
            metadata["sections"] = sections
        
        self.logger.info(
            "pdf_converted",
            file_path=file_path,
            method="pymupdf",
            pages=metadata["page_count"],
            markdown_length=len(markdown),
        )
        
        return ProcessedPDF(
            file_path=file_path,
            markdown=markdown,
            metadata=metadata,
            page_count=metadata["page_count"],
            method_used="pymupdf",
        )
    
    async def _extract_metadata_pymupdf(self, file_path: str) -> Dict[str, Any]:
        """Extrae metadatos usando PyMuPDF."""
        if not PYMUPDF_AVAILABLE:
            return {}
        
        loop = asyncio.get_event_loop()
        
        def sync_extract():
            doc = fitz.open(file_path)
            metadata = {
                "title": doc.metadata.get("title", ""),
                "author": doc.metadata.get("author", ""),
                "subject": doc.metadata.get("subject", ""),
                "creator": doc.metadata.get("creator", ""),
                "page_count": len(doc),
            }
            doc.close()
            return metadata
        
        return await loop.run_in_executor(None, sync_extract)
    
    def _clean_repetitive_headers(self, text: str) -> str:
        """
        Limpia headers/footers repetitivos (números de página, etc.).
        
        Estrategia simple:
        - Elimina líneas que aparecen >3 veces exactamente iguales
        - Elimina líneas que son solo números (páginas)
        """
        lines = text.split("\n")
        
        # Count line frequencies
        line_counts = {}
        for line in lines:
            stripped = line.strip()
            if stripped:
                line_counts[stripped] = line_counts.get(stripped, 0) + 1
        
        # Filter out repetitive lines (>3 occurrences)
        cleaned_lines = []
        for line in lines:
            stripped = line.strip()
            
            # Keep empty lines
            if not stripped:
                cleaned_lines.append(line)
                continue
            
            # Remove if repetitive
            if line_counts[stripped] > 3:
                continue
            
            # Remove if just numbers (page numbers)
            if stripped.isdigit():
                continue
            
            cleaned_lines.append(line)
        
        return "\n".join(cleaned_lines)
    
    def _extract_sections(self, markdown: str) -> Dict[str, str]:
        """
        Detecta secciones académicas comunes.
        
        Returns:
            Dict de {section_name: section_text}
        """
        sections = {}
        
        # Common academic section headers
        section_keywords = [
            "abstract",
            "introduction",
            "related work",
            "methodology",
            "methods",
            "results",
            "discussion",
            "conclusion",
            "references",
            "acknowledgments",
        ]
        
        lines = markdown.split("\n")
        current_section = "header"
        current_text = []
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Check if line is a section header
            is_section = False
            for keyword in section_keywords:
                if keyword in line_lower and len(line_lower) < 50:
                    # Save previous section
                    if current_text:
                        sections[current_section] = "\n".join(current_text).strip()
                    
                    # Start new section
                    current_section = keyword.replace(" ", "_")
                    current_text = []
                    is_section = True
                    break
            
            if not is_section:
                current_text.append(line)
        
        # Save last section
        if current_text:
            sections[current_section] = "\n".join(current_text).strip()
        
        return sections
