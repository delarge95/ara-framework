"""
Tools package for CrewAI agents.

Este paquete contiene todos los tools que los agents pueden usar:

1. SearchTool (5 tools): Búsqueda académica en Semantic Scholar
   - search_academic_papers: Búsqueda básica con rate limit 1 req/seg
   - search_papers_parallel: Búsqueda paralela (mitiga bottleneck)
   - get_paper_details: Detalles de paper específico
   - get_related_papers: Papers relacionados/recommendations
   - search_recent_papers: Papers recientes ordenados por citaciones

2. ScrapingTool (5 tools): Web scraping con Playwright
   - scrape_website: Scraping básico con anti-detection stealth mode
   - extract_structured_data: Extracción con selectores CSS
   - scrape_multiple_urls: Scraping paralelo con concurrencia limitada
   - take_screenshot: Captura de pantalla para debugging
   - execute_javascript: Ejecución de JS en contexto de página

3. PDFTool (6 tools): Procesamiento de PDFs académicos
   - convert_pdf_to_markdown: Conversión PDF → Markdown (MarkItDown + PyMuPDF hybrid)
   - extract_pdf_sections: Extracción de secciones académicas (Abstract, Methods, etc.)
   - extract_pdf_text_only: Solo texto plano sin formatting
   - convert_multiple_pdfs: Conversión batch con rate limit
   - get_pdf_metadata: Solo metadatos (rápido)

4. DatabaseTool (11 tools): Persistencia con Supabase PostgreSQL + Storage
   - save_analysis/get_previous_analysis/list_recent_analyses: Análisis completos
   - save_paper/query_papers/get_paper_by_id: Papers académicos
   - upload_file/download_file: Storage de PDFs y screenshots
   - log_model_usage/get_usage_statistics: Tracking de uso para BudgetManager

Total: 27 tools funcionales para los 6 agents

Uso:
    from tools import get_search_tool, get_scraping_tool, get_pdf_tool, get_database_tool
    
    # Obtener instancias (singleton pattern)
    search_tool = get_search_tool()
    scraping_tool = get_scraping_tool()
    pdf_tool = get_pdf_tool()
    database_tool = get_database_tool()
    
    # Crear agent con tools
    agent = Agent(
        role="Literature Researcher",
        tools=[
            search_tool.search_academic_papers,
            search_tool.search_papers_parallel,
            pdf_tool.convert_pdf_to_markdown,
            database_tool.save_paper,
        ],
        ...
    )

Fuente: docs/04_ARCHITECTURE.md (Tools Layer)
Referencia: docs/03_AI_MODELS.md (CrewAI integration patterns)
"""
from tools.search_tool import SearchTool, get_search_tool
from tools.scraping_tool import ScrapingTool, get_scraping_tool
from tools.pdf_tool import PDFTool, get_pdf_tool
from tools.database_tool import DatabaseTool, get_database_tool

__all__ = [
    "SearchTool",
    "ScrapingTool",
    "PDFTool",
    "DatabaseTool",
    "get_search_tool",
    "get_scraping_tool",
    "get_pdf_tool",
    "get_database_tool",
]
