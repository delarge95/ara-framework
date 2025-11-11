"""
Test configuration and fixtures for ARA Framework tests.

Este módulo provee fixtures compartidos para todos los tests:
- Mock settings
- Mock database connections
- Mock API clients (Semantic Scholar, OpenAI, etc.)
- Sample data (papers, niches, etc.)

Para ejecutar tests:
    pytest tests/
    pytest tests/ -v
    pytest tests/ -v -s  # Con logs
    pytest tests/ --cov=ara_framework  # Con coverage
"""
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, MagicMock, patch
from datetime import datetime, timezone
from typing import Dict, Any, List


# Mock langchain_google_genai BEFORE any imports
@pytest.fixture(scope="session", autouse=True)
def mock_langchain_google_genai():
    """Mock langchain_google_genai to avoid MediaResolution import error."""
    import sys
    from unittest.mock import MagicMock
    
    # Create fake module
    fake_module = MagicMock()
    fake_module.ChatGoogleGenerativeAI = MagicMock()
    
    sys.modules['langchain_google_genai'] = fake_module
    sys.modules['langchain_google_genai._enums'] = MagicMock()
    
    yield fake_module
    
    # Cleanup
    if 'langchain_google_genai' in sys.modules:
        del sys.modules['langchain_google_genai']
    if 'langchain_google_genai._enums' in sys.modules:
        del sys.modules['langchain_google_genai._enums']


# Fixtures para event loop async
@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# Fixtures para settings mock
@pytest.fixture
def mock_settings():
    """Mock settings for tests."""
    from config.settings import Settings
    
    settings = Settings(
        # API Keys (fake para tests)
        OPENAI_API_KEY="sk-test-openai-key",
        ANTHROPIC_API_KEY="sk-test-anthropic-key",
        GEMINI_API_KEY="test-gemini-key",
        DEEPSEEK_API_KEY="test-deepseek-key",
        
        # Supabase (fake)
        SUPABASE_URL="https://test.supabase.co",
        SUPABASE_SERVICE_KEY="test-service-key",
        
        # Redis (local)
        REDIS_URL="redis://localhost:6379/1",  # DB 1 para tests
        
        # Budget
        MONTHLY_CREDIT_LIMIT=100.0,
        
        # OpenTelemetry (disabled para tests)
        UPTRACE_DSN="",
    )
    
    return settings


# Fixtures para mock database
@pytest.fixture
def mock_supabase_client():
    """Mock Supabase client."""
    client = MagicMock()
    
    # Mock table operations
    table_mock = MagicMock()
    table_mock.insert.return_value.execute.return_value = {
        "data": [{"id": "test-id-123"}],
        "error": None,
    }
    table_mock.select.return_value.eq.return_value.execute.return_value = {
        "data": [],
        "error": None,
    }
    table_mock.update.return_value.eq.return_value.execute.return_value = {
        "data": [{"id": "test-id-123"}],
        "error": None,
    }
    
    client.table.return_value = table_mock
    
    return client


# Fixtures para mock Redis
@pytest.fixture
def mock_redis_client():
    """Mock Redis client."""
    client = AsyncMock()
    
    # Mock basic operations
    client.get.return_value = None
    client.set.return_value = True
    client.delete.return_value = 1
    client.exists.return_value = False
    client.ttl.return_value = -1
    client.ping.return_value = True
    
    return client


# Fixtures para sample data
@pytest.fixture
def sample_paper():
    """Sample paper data."""
    return {
        "paperId": "test-paper-123",
        "title": "Sample Paper on Rust WASM",
        "abstract": "This is a sample abstract about Rust WebAssembly for real-time audio processing.",
        "year": 2024,
        "citationCount": 42,
        "authors": [
            {"name": "John Doe"},
            {"name": "Jane Smith"},
        ],
        "url": "https://arxiv.org/abs/2401.12345",
        "venue": "ICML",
        "publicationTypes": ["JournalArticle"],
        "fieldsOfStudy": ["Computer Science", "Audio Processing"],
    }


@pytest.fixture
def sample_papers_list(sample_paper):
    """List of sample papers."""
    papers = []
    for i in range(10):
        paper = sample_paper.copy()
        paper["paperId"] = f"test-paper-{i}"
        paper["title"] = f"Sample Paper {i}"
        paper["citationCount"] = 10 + i * 5
        papers.append(paper)
    return papers


@pytest.fixture
def sample_niche():
    """Sample niche string."""
    return "Rust WASM for real-time audio processing"


@pytest.fixture
def sample_niche_analysis():
    """Sample niche analysis output."""
    return """
    # Análisis de Niche: Rust WASM for real-time audio processing
    
    ## 1. Resumen Ejecutivo
    El niche de Rust WASM para audio en tiempo real presenta una viabilidad alta (8/10).
    
    ## 2. Análisis de Tendencias
    - Trend 1: Crecimiento de WASM en navegadores
    - Trend 2: Rust como lenguaje para systems programming
    
    ## 3. Sub-niches Identificados
    1. Audio synthesis en navegador
    2. DAW (Digital Audio Workstation) web-based
    
    ## 4. Viabilidad del Niche
    Score: 8/10
    Justificación: Alta demanda, tecnologías maduras.
    """


@pytest.fixture
def sample_literature_review():
    """Sample literature review output."""
    return """
    # Base de Conocimiento: Rust WASM for audio
    
    ## 1. Resumen Ejecutivo
    Se analizaron 100 papers sobre WASM y audio processing.
    
    ## 2. Papers Clave
    1. Paper A (2024, 50 citations)
    2. Paper B (2023, 30 citations)
    
    ## 3. Análisis de Tendencias
    - Trend 1: AudioWorklet API adoption
    - Trend 2: WASM SIMD for performance
    """


# Fixtures para mock agents
@pytest.fixture
def mock_niche_analyst_agent():
    """Mock NicheAnalyst agent."""
    agent = MagicMock()
    agent.role = "Niche Analyst"
    return agent


@pytest.fixture
def mock_crew_output(sample_literature_review):
    """Mock CrewAI output."""
    try:
        from crewai.crews.crew_output import CrewOutput  # type: ignore
    except ImportError:  # Older CrewAI versions without CrewOutput
        CrewOutput = None  # type: ignore

    output = MagicMock(spec=CrewOutput) if CrewOutput else MagicMock()
    output.raw = sample_literature_review
    output.tasks_output = []
    
    return output


# Fixtures para mock LLMs
@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client."""
    client = AsyncMock()
    
    # Mock chat completion
    completion_mock = MagicMock()
    completion_mock.choices = [
        MagicMock(
            message=MagicMock(content="This is a test response from GPT-5")
        )
    ]
    completion_mock.usage = MagicMock(
        prompt_tokens=100,
        completion_tokens=50,
        total_tokens=150,
    )
    
    client.chat.completions.create.return_value = completion_mock
    
    return client


@pytest.fixture
def mock_semantic_scholar_response(sample_paper):
    """Mock Semantic Scholar API response."""
    return {
        "total": 100,
        "offset": 0,
        "next": 10,
        "data": [sample_paper] * 10,
    }


# Fixtures para BudgetManager
@pytest.fixture
def mock_budget_manager():
    """Mock BudgetManager."""
    manager = MagicMock()
    manager.get_remaining_credits.return_value = 50.0
    manager.get_usage_since.return_value = 2.5
    manager.track_usage.return_value = None
    return manager


# Fixtures para file operations
@pytest.fixture
def temp_output_dir(tmp_path):
    """Temporary directory for output files."""
    output_dir = tmp_path / "outputs"
    output_dir.mkdir()
    return output_dir


@pytest.fixture
def sample_pdf_path(tmp_path):
    """Sample PDF file path (mock)."""
    pdf_path = tmp_path / "sample_paper.pdf"
    pdf_path.write_text("Sample PDF content")
    return pdf_path
