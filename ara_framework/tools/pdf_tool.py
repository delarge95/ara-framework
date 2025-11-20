"""
PDFTool para procesamiento de papers académicos.

Fuente: docs/04_ARCHITECTURE.md (Tools Layer)
Referencia: docs/03_AI_MODELS.md (CrewAI tools integration)

Este tool es usado por:
- LiteratureResearcher: Procesamiento de PDFs descargados
- TechnicalArchitect: Análisis de documentación técnica en PDF
- ContentSynthesizer: Extracción de contenido para síntesis

Features:
- Conversión PDF → Markdown (MarkItDown + PyMuPDF hybrid)
- Extracción de metadatos (autor, título, año)
- Detección de secciones académicas (Abstract, Introduction, etc.)
- Rate limiting (5 conversiones/min - CPU intensive)
- Cache agresivo (7 días)
"""
import asyncio
from typing import Optional, Dict, Any, List
from langchain_core.tools import tool
import structlog

from mcp_servers.markitdown_mcp import MarkItDownAdapter, ProcessedPDF
from config.settings import settings

logger = structlog.get_logger()


class PDFTool:
    """
    Tool de procesamiento de PDFs integrado con CrewAI.
    
    Uso en Agents:
        agent = Agent(
            tools=[
                pdf_tool.convert_pdf_to_markdown,
                pdf_tool.extract_pdf_sections,
            ],
            ...
        )
    """
    
    def __init__(self, redis_client=None):
        self.adapter = MarkItDownAdapter(redis_client=redis_client)
        self._connected = False
    
    async def _ensure_connected(self):
        """Conecta adapter si no está conectado."""
        if not self._connected:
            await self.adapter.connect()
            self._connected = True
    
    @tool("convert_pdf_to_markdown")
    async def convert_pdf_to_markdown(
        file_path: str,
        clean_headers: bool = True,
        extract_sections: bool = True,
    ) -> Dict[str, Any]:
        """
        Convierte PDF académico a Markdown.
        
        Este tool usa estrategia híbrida:
        1. Intenta MarkItDown (Microsoft) para mejor calidad
        2. Fallback a PyMuPDF si falla
        
        Args:
            file_path (str): Path al archivo PDF
            clean_headers (bool): Si limpiar headers/footers repetitivos
            extract_sections (bool): Si detectar secciones académicas
        
        Returns:
            Dict: Resultado del procesamiento con estructura:
                - file_path: Path original
                - markdown: Contenido en Markdown
                - metadata: Dict con autor, título, año, etc.
                - page_count: Número de páginas
                - method_used: "markitdown" o "pymupdf"
        
        Example:
            result = convert_pdf_to_markdown(
                "papers/transformer_paper.pdf",
                clean_headers=True,
                extract_sections=True
            )
            
            markdown_content = result["markdown"]
            abstract = result["metadata"]["sections"]["abstract"]
        """
        tool_instance = _get_pdf_tool_instance()
        await tool_instance._ensure_connected()
        
        try:
            result = await tool_instance.adapter.convert_pdf(
                file_path=file_path,
                clean_headers=clean_headers,
                extract_sections=extract_sections,
            )
            
            logger.info(
                "pdf_converted",
                file_path=file_path,
                pages=result.page_count,
                method=result.method_used,
                markdown_length=len(result.markdown),
            )
            
            return result.to_dict()
        
        except FileNotFoundError:
            logger.error(
                "pdf_not_found",
                file_path=file_path,
            )
            return {
                "file_path": file_path,
                "markdown": "",
                "metadata": {"error": "File not found"},
                "page_count": 0,
                "method_used": "none",
            }
        except Exception as e:
            logger.error(
                "pdf_conversion_failed",
                file_path=file_path,
                error=str(e),
            )
            return {
                "file_path": file_path,
                "markdown": "",
                "metadata": {"error": str(e)},
                "page_count": 0,
                "method_used": "none",
            }
    
    @tool("extract_pdf_sections")
    async def extract_pdf_sections(file_path: str) -> Dict[str, str]:
        """
        Extrae secciones académicas de un PDF.
        
        Detecta secciones comunes: Abstract, Introduction, Methods, Results,
        Discussion, Conclusion, References, etc.
        
        Args:
            file_path (str): Path al archivo PDF
        
        Returns:
            Dict: Mapeo de {section_name: section_text}
        
        Example:
            sections = extract_pdf_sections("paper.pdf")
            
            abstract = sections.get("abstract", "")
            introduction = sections.get("introduction", "")
            methods = sections.get("methods", "")
        """
        tool_instance = _get_pdf_tool_instance()
        await tool_instance._ensure_connected()
        
        try:
            result = await tool_instance.adapter.convert_pdf(
                file_path=file_path,
                clean_headers=True,
                extract_sections=True,
            )
            
            sections = result.metadata.get("sections", {})
            
            logger.info(
                "pdf_sections_extracted",
                file_path=file_path,
                sections_found=len(sections),
            )
            
            return sections
        
        except Exception as e:
            logger.error(
                "pdf_section_extraction_failed",
                file_path=file_path,
                error=str(e),
            )
            return {}
    
    @tool("extract_pdf_text_only")
    async def extract_pdf_text_only(file_path: str) -> str:
        """
        Extrae solo texto plano de un PDF (sin markdown formatting).
        
        Útil para búsquedas o análisis de texto donde el formato no importa.
        
        Args:
            file_path (str): Path al archivo PDF
        
        Returns:
            str: Texto plano extraído
        
        Example:
            text = extract_pdf_text_only("paper.pdf")
            
            # Buscar keyword
            if "deep learning" in text.lower():
                print("Paper mentions deep learning")
        """
        tool_instance = _get_pdf_tool_instance()
        await tool_instance._ensure_connected()
        
        try:
            text = await tool_instance.adapter.extract_text_only(file_path)
            
            logger.info(
                "pdf_text_extracted",
                file_path=file_path,
                text_length=len(text),
            )
            
            return text
        
        except Exception as e:
            logger.error(
                "pdf_text_extraction_failed",
                file_path=file_path,
                error=str(e),
            )
            return ""
    
    @tool("convert_multiple_pdfs")
    async def convert_multiple_pdfs(
        file_paths: List[str],
        max_concurrent: int = 2,
        clean_headers: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        Convierte múltiples PDFs en paralelo.
        
        Usa concurrencia limitada para no sobrecargar CPU.
        
        Args:
            file_paths (list): Lista de paths a PDFs
            max_concurrent (int): Máximo conversiones simultáneas (default 2)
            clean_headers (bool): Si limpiar headers/footers
        
        Returns:
            List[Dict]: Lista de resultados de conversión
        
        Example:
            results = convert_multiple_pdfs([
                "papers/paper1.pdf",
                "papers/paper2.pdf",
                "papers/paper3.pdf",
            ])
            
            for result in results:
                print(f"{result['file_path']}: {result['page_count']} pages")
        """
        tool_instance = _get_pdf_tool_instance()
        await tool_instance._ensure_connected()
        
        try:
            results = await tool_instance.adapter.convert_multiple(
                file_paths=file_paths,
                max_concurrent=max_concurrent,
                clean_headers=clean_headers,
                extract_sections=False,  # Skip for batch processing
            )
            
            logger.info(
                "batch_conversion_completed",
                total=len(file_paths),
                successful=len(results),
            )
            
            return [r.to_dict() for r in results]
        
        except Exception as e:
            logger.error(
                "batch_conversion_failed",
                total=len(file_paths),
                error=str(e),
            )
            return []
    
    @tool("get_pdf_metadata")
    async def get_pdf_metadata(file_path: str) -> Dict[str, Any]:
        """
        Extrae solo metadatos de un PDF (sin convertir contenido).
        
        Más rápido que conversión completa cuando solo necesitas metadata.
        
        Args:
            file_path (str): Path al archivo PDF
        
        Returns:
            Dict: Metadatos (título, autor, páginas, etc.)
        
        Example:
            metadata = get_pdf_metadata("paper.pdf")
            
            print(f"Title: {metadata['title']}")
            print(f"Author: {metadata['author']}")
            print(f"Pages: {metadata['page_count']}")
        """
        tool_instance = _get_pdf_tool_instance()
        await tool_instance._ensure_connected()
        
        try:
            # Convert with sections to get full metadata
            result = await tool_instance.adapter.convert_pdf(
                file_path=file_path,
                clean_headers=False,
                extract_sections=True,
            )
            
            logger.info(
                "pdf_metadata_extracted",
                file_path=file_path,
                title=result.metadata.get("title", "")[:50],
            )
            
            return result.metadata
        
        except Exception as e:
            logger.error(
                "pdf_metadata_extraction_failed",
                file_path=file_path,
                error=str(e),
            )
            return {
                "error": str(e),
                "file_path": file_path,
            }
    
    async def close(self):
        """Cierra conexión del adapter."""
        if self._connected:
            await self.adapter.disconnect()
            self._connected = False


# Global instance for singleton pattern
_pdf_tool_instance = None


def _get_pdf_tool_instance(redis_client=None) -> PDFTool:
    """
    Obtiene instancia global de PDFTool (singleton).
    
    Args:
        redis_client: Cliente Redis (opcional)
    
    Returns:
        PDFTool instance
    """
    global _pdf_tool_instance
    
    if _pdf_tool_instance is None:
        _pdf_tool_instance = PDFTool(redis_client=redis_client)
    
    return _pdf_tool_instance


def get_pdf_tool(redis_client=None) -> PDFTool:
    """
    Alias público para obtener instancia.
    
    Args:
        redis_client: Cliente Redis (opcional)
    
    Returns:
        PDFTool instance
    """
    return _get_pdf_tool_instance(redis_client)


# ============================================================
# Module-level tool functions (LangChain @tool decorated)
# ============================================================

@tool("extract_pdf_text_only")
async def extract_pdf_text_only(file_path: str) -> str:
    """
    Extrae solo texto plano de un PDF (sin markdown formatting).
    
    Útil para búsquedas o análisis de texto donde el formato no importa.
    
    Args:
        file_path (str): Path al archivo PDF
    
    Returns:
        str: Texto plano extraído
    
    Example:
        text = extract_pdf_text_only("paper.pdf")
        
        # Buscar keyword
        if "deep learning" in text.lower():
            print("Paper mentions deep learning")
    """
    tool_instance = _get_pdf_tool_instance()
    await tool_instance._ensure_connected()
    
    try:
        text = await tool_instance.adapter.extract_text_only(file_path)
        
        logger.info(
            "pdf_text_extracted",
            file_path=file_path,
            text_length=len(text),
        )
        
        return text
    
    except Exception as e:
        logger.error(
            "pdf_text_extraction_failed",
            file_path=file_path,
            error=str(e),
        )
        return ""
