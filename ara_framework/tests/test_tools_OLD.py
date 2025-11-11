"""
Tests for Tools Layer - search_tool, scraping_tool, pdf_tool, database_tool.

Tests básicos para verificar que los tools están correctamente configurados
y pueden manejar inputs válidos/inválidos.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock

from tools import (
    get_search_tool,
    get_scraping_tool,
    get_pdf_tool,
    get_database_tool,
)


class TestSearchTool:
    """Tests para search_tool (Semantic Scholar)."""
    
    def test_get_search_tool(self):
        """Test obtención del search_tool."""
        tool = get_search_tool()
        
        assert tool is not None
        assert hasattr(tool, "search_academic_papers")
        assert hasattr(tool, "search_papers_parallel")
        assert hasattr(tool, "get_paper_details")
    
    @pytest.mark.asyncio
    async def test_search_academic_papers_mock(
        self,
        mock_semantic_scholar_response,
    ):
        """Test búsqueda de papers (mock)."""
        tool = get_search_tool()
        
        # Mock the MCP adapter
        with patch.object(
            tool.adapter,
            "search_papers",
            new_callable=AsyncMock,
            return_value=mock_semantic_scholar_response,
        ):
            results = await tool.search_academic_papers(
                query="Rust WASM",
                limit=10,
            )
            
            assert results is not None
            assert "data" in results
            assert len(results["data"]) > 0
    
    @pytest.mark.asyncio
    async def test_search_papers_parallel_mock(
        self,
        mock_semantic_scholar_response,
    ):
        """Test búsqueda paralela (mock)."""
        tool = get_search_tool()
        
        with patch.object(
            tool.adapter,
            "search_papers_parallel",
            new_callable=AsyncMock,
            return_value=[mock_semantic_scholar_response],
        ):
            results = await tool.search_papers_parallel(
                queries=["Rust WASM", "Audio processing"],
                limit_per_query=10,
            )
            
            assert results is not None
            assert isinstance(results, list)


class TestScrapingTool:
    """Tests para scraping_tool (Playwright)."""
    
    def test_get_scraping_tool(self):
        """Test obtención del scraping_tool."""
        tool = get_scraping_tool()
        
        assert tool is not None
        assert hasattr(tool, "scrape_website")
        assert hasattr(tool, "scrape_multiple_urls")
        assert hasattr(tool, "extract_structured_data")
    
    @pytest.mark.asyncio
    async def test_scrape_website_mock(self):
        """Test scraping de website (mock)."""
        tool = get_scraping_tool()
        
        mock_content = {
            "url": "https://example.com",
            "title": "Example Page",
            "content": "This is example content",
        }
        
        with patch.object(
            tool.adapter,
            "scrape_page",
            new_callable=AsyncMock,
            return_value=mock_content,
        ):
            result = await tool.scrape_website("https://example.com")
            
            assert result is not None
            assert "url" in result
            assert "content" in result


class TestPdfTool:
    """Tests para pdf_tool (MarkItDown)."""
    
    def test_get_pdf_tool(self):
        """Test obtención del pdf_tool."""
        tool = get_pdf_tool()
        
        assert tool is not None
        assert hasattr(tool, "convert_pdf_to_markdown")
        assert hasattr(tool, "extract_pdf_sections")
        assert hasattr(tool, "convert_multiple_pdfs")
    
    @pytest.mark.asyncio
    async def test_convert_pdf_to_markdown_mock(self, sample_pdf_path):
        """Test conversión de PDF a Markdown (mock)."""
        tool = get_pdf_tool()
        
        mock_markdown = "# Sample Paper\n\nThis is the paper content."
        
        with patch.object(
            tool.adapter,
            "convert_file",
            new_callable=AsyncMock,
            return_value={"markdown": mock_markdown},
        ):
            result = await tool.convert_pdf_to_markdown(str(sample_pdf_path))
            
            assert result is not None
            assert "markdown" in result or isinstance(result, str)
    
    @pytest.mark.asyncio
    async def test_extract_pdf_sections_mock(self, sample_pdf_path):
        """Test extracción de secciones (mock)."""
        tool = get_pdf_tool()
        
        mock_sections = {
            "Abstract": "This is the abstract",
            "Introduction": "This is the introduction",
            "Methods": "These are the methods",
        }
        
        with patch.object(
            tool,
            "extract_pdf_sections",
            new_callable=AsyncMock,
            return_value=mock_sections,
        ):
            result = await tool.extract_pdf_sections(
                str(sample_pdf_path),
                sections=["Abstract", "Introduction", "Methods"],
            )
            
            assert result is not None
            assert "Abstract" in result


class TestDatabaseTool:
    """Tests para database_tool (Supabase)."""
    
    def test_get_database_tool(self):
        """Test obtención del database_tool."""
        tool = get_database_tool()
        
        assert tool is not None
        assert hasattr(tool, "save_paper")
        assert hasattr(tool, "query_papers")
        assert hasattr(tool, "save_analysis")
        assert hasattr(tool, "log_model_usage")
    
    @pytest.mark.asyncio
    async def test_save_paper_mock(self, sample_paper):
        """Test guardado de paper (mock)."""
        tool = get_database_tool()
        
        with patch.object(
            tool.adapter,
            "insert_record",
            new_callable=AsyncMock,
            return_value={"id": "test-id-123"},
        ):
            result = await tool.save_paper(
                paper_id=sample_paper["paperId"],
                title=sample_paper["title"],
                abstract=sample_paper["abstract"],
                year=sample_paper["year"],
                citations=sample_paper["citationCount"],
            )
            
            assert result is not None
    
    @pytest.mark.asyncio
    async def test_query_papers_mock(self):
        """Test query de papers (mock)."""
        tool = get_database_tool()
        
        mock_results = [
            {"id": "1", "title": "Paper 1"},
            {"id": "2", "title": "Paper 2"},
        ]
        
        with patch.object(
            tool.adapter,
            "query_records",
            new_callable=AsyncMock,
            return_value=mock_results,
        ):
            results = await tool.query_papers(
                filters={"year": 2024},
                limit=10,
            )
            
            assert results is not None
            assert isinstance(results, list)
    
    @pytest.mark.asyncio
    async def test_save_analysis_mock(self, sample_niche, sample_literature_review):
        """Test guardado de análisis (mock)."""
        tool = get_database_tool()
        
        with patch.object(
            tool.adapter,
            "insert_record",
            new_callable=AsyncMock,
            return_value={"id": "analysis-123"},
        ):
            result = await tool.save_analysis(
                niche_name=sample_niche,
                status="completed",
                report_markdown=sample_literature_review,
                metadata={"credits_used": 2.5},
            )
            
            assert result is not None
    
    @pytest.mark.asyncio
    async def test_log_model_usage_mock(self):
        """Test logging de uso de modelo (mock)."""
        tool = get_database_tool()
        
        with patch.object(
            tool.adapter,
            "insert_record",
            new_callable=AsyncMock,
            return_value={"id": "usage-123"},
        ):
            result = await tool.log_model_usage(
                model_name="gpt-5",
                credits_used=1.0,
                prompt_tokens=1000,
                completion_tokens=500,
            )
            
            assert result is not None


class TestToolsIntegration:
    """Tests de integración entre tools."""
    
    @pytest.mark.asyncio
    async def test_search_and_save_paper(
        self,
        sample_paper,
        mock_semantic_scholar_response,
    ):
        """Test: Buscar paper y guardarlo en Supabase."""
        search_tool = get_search_tool()
        database_tool = get_database_tool()
        
        # Mock search
        with patch.object(
            search_tool.adapter,
            "search_papers",
            new_callable=AsyncMock,
            return_value=mock_semantic_scholar_response,
        ):
            # Mock save
            with patch.object(
                database_tool.adapter,
                "insert_record",
                new_callable=AsyncMock,
                return_value={"id": "saved-paper-123"},
            ):
                # Search
                results = await search_tool.search_academic_papers(
                    query="Rust WASM",
                    limit=10,
                )
                
                # Save first paper
                paper = results["data"][0]
                saved = await database_tool.save_paper(
                    paper_id=paper["paperId"],
                    title=paper["title"],
                    abstract=paper["abstract"],
                    year=paper["year"],
                    citations=paper["citationCount"],
                )
                
                assert saved is not None
