"""
Tests for Pipeline - CrewAI 0.100.0 orchestration and execution.

Estrategia de Testing Simplificada:
- Mocking directo de Crew.kickoff() sin stubs de internos de CrewAI
- Tests unitarios enfocados en lógica de AnalysisPipeline
- Tests de integración opcionales (requieren API keys)

Tests:
- Pipeline initialization
- Input validation
- Crew execution
- Error handling
- Timeout handling
- Result saving (Supabase + local)
"""
import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from datetime import datetime, timezone
import asyncio

from core.pipeline import (
    AnalysisPipeline,
    PipelineResult,
    PipelineStatus,
    AgentResult,
)


class TestPipelineInitialization:
    """Tests para inicialización del pipeline."""
    
    def test_pipeline_initialization_default(self):
        """Test inicialización con valores default."""
        pipeline = AnalysisPipeline()
        
        assert pipeline.max_retries == 3
        assert pipeline.timeout_minutes == 90
        assert pipeline.budget_manager is not None
        assert pipeline.database_tool is not None
    
    def test_pipeline_initialization_custom(self):
        """Test inicialización con valores custom."""
        pipeline = AnalysisPipeline(
            max_retries=5,
            timeout_minutes=120,
            enable_telemetry=False,
            enable_circuit_breaker=False,
        )
        
        assert pipeline.max_retries == 5
        assert pipeline.timeout_minutes == 120


class TestInputValidation:
    """Tests para validación de inputs."""
    
    def test_validate_niche_valid(self):
        """Test validación de niche válido."""
        pipeline = AnalysisPipeline()
        
        is_valid, error = pipeline._validate_niche("Rust WASM for audio")
        
        assert is_valid is True
        assert error is None
    
    def test_validate_niche_empty(self):
        """Test validación de niche vacío."""
        pipeline = AnalysisPipeline()
        
        is_valid, error = pipeline._validate_niche("")
        
        assert is_valid is False
        assert "empty" in error.lower()
    
    def test_validate_niche_too_short(self):
        """Test validación de niche muy corto."""
        pipeline = AnalysisPipeline()
        
        is_valid, error = pipeline._validate_niche("Rust")
        
        assert is_valid is False
        assert "short" in error.lower()
    
    def test_validate_niche_too_long(self):
        """Test validación de niche muy largo."""
        pipeline = AnalysisPipeline()
        
        long_niche = "A" * 300
        is_valid, error = pipeline._validate_niche(long_niche)
        
        assert is_valid is False
        assert "long" in error.lower()
    
    def test_validate_niche_suspicious_chars(self):
        """Test validación de caracteres sospechosos."""
        pipeline = AnalysisPipeline()
        
        is_valid, error = pipeline._validate_niche("Rust <script>alert</script>")
        
        assert is_valid is False
        assert "suspicious" in error.lower()


class TestPipelineExecution:
    """Tests para ejecución del pipeline."""
    
    @pytest.mark.asyncio
    async def test_run_analysis_success(
        self,
        sample_niche,
        sample_literature_review,
        mock_budget_manager,
    ):
        """Test ejecución exitosa del pipeline."""
        pipeline = AnalysisPipeline()
        
        # Mock budget manager
        pipeline.budget_manager = mock_budget_manager
        
        # Configurar mock para retornar coroutine
        mock_budget_manager.get_remaining_credits = AsyncMock(return_value=10.0)
        
        # Mock crew execution
        mock_crew_output = MagicMock()
        mock_crew_output.raw = sample_literature_review
        
        # Mock agent creation functions to avoid real Gemini initialization
        mock_agent = MagicMock()
        mock_task = MagicMock()
        
        # Mock Crew constructor to prevent real CrewAI initialization
        mock_crew = MagicMock()
        
        with patch('agents.niche_analyst.create_niche_analyst', return_value=(mock_agent, mock_task)):
            with patch('agents.literature_researcher.create_literature_researcher', return_value=(mock_agent, mock_task)):
                with patch('agents.technical_architect.create_technical_architect', return_value=(mock_agent, mock_task)):
                    with patch('agents.implementation_specialist.create_implementation_specialist', return_value=(mock_agent, mock_task)):
                        with patch('agents.content_synthesizer.create_content_synthesizer', return_value=(mock_agent, mock_task)):
                            with patch('core.pipeline.Crew', return_value=mock_crew):
                                with patch.object(
                                    pipeline,
                                    "_run_crew_with_circuit_breaker",
                                    return_value=mock_crew_output,
                                ):
                                    with patch.object(
                                        pipeline,
                                        "_save_to_supabase",
                                        new_callable=AsyncMock,
                                    ):
                                        result = await pipeline.run_analysis(sample_niche)
        
        assert result.status == PipelineStatus.COMPLETED
        assert result.final_report is not None
        assert len(result.final_report) > 0
        assert result.niche == sample_niche
    
    @pytest.mark.asyncio
    async def test_run_analysis_invalid_input(self):
        """Test con input inválido."""
        pipeline = AnalysisPipeline()
        
        result = await pipeline.run_analysis("")
        
        assert result.status == PipelineStatus.FAILED
        assert len(result.errors) > 0
        assert "validation" in result.errors[0].lower()
    
    @pytest.mark.asyncio
    async def test_run_analysis_timeout(
        self,
        sample_niche,
        mock_budget_manager,
    ):
        """Test timeout del pipeline."""
        pipeline = AnalysisPipeline(timeout_minutes=0.01)  # 0.01 min = 0.6 sec
        pipeline.budget_manager = mock_budget_manager
        
        # Configurar mock para retornar coroutine
        mock_budget_manager.get_remaining_credits = AsyncMock(return_value=10.0)
        
        # Mock crew execution que tarda mucho
        async def slow_execution(*args, **kwargs):
            await asyncio.sleep(10)  # 10 segundos > 0.6 segundos
            return MagicMock()
        
        # Mock agent creation functions
        mock_agent = MagicMock()
        mock_task = MagicMock()
        
        # Mock Crew constructor to prevent real CrewAI initialization
        mock_crew = MagicMock()
        
        with patch('agents.niche_analyst.create_niche_analyst', return_value=(mock_agent, mock_task)):
            with patch('agents.literature_researcher.create_literature_researcher', return_value=(mock_agent, mock_task)):
                with patch('agents.technical_architect.create_technical_architect', return_value=(mock_agent, mock_task)):
                    with patch('agents.implementation_specialist.create_implementation_specialist', return_value=(mock_agent, mock_task)):
                        with patch('agents.content_synthesizer.create_content_synthesizer', return_value=(mock_agent, mock_task)):
                            with patch('core.pipeline.Crew', return_value=mock_crew):
                                with patch.object(
                                    pipeline,
                                    "_run_crew_with_circuit_breaker",
                                    side_effect=slow_execution,
                                ):
                                    with patch.object(
                                        pipeline,
                                        "_save_partial_results",
                                        new_callable=AsyncMock,
                                    ):
                                        result = await pipeline.run_analysis(sample_niche)
        
        assert result.status == PipelineStatus.TIMEOUT
        assert any("timeout" in error.lower() for error in result.errors)
    
    @pytest.mark.asyncio
    async def test_run_analysis_crew_failure(
        self,
        sample_niche,
        mock_budget_manager,
    ):
        """Test cuando crew falla."""
        pipeline = AnalysisPipeline()
        pipeline.budget_manager = mock_budget_manager
        
        # Mock crew execution que falla
        with patch.object(
            pipeline,
            "_run_crew_with_circuit_breaker",
            side_effect=Exception("Crew execution failed"),
        ):
            with patch.object(
                pipeline,
                "_save_partial_results",
                new_callable=AsyncMock,
            ):
                result = await pipeline.run_analysis(sample_niche)
        
        assert result.status == PipelineStatus.FAILED
        assert len(result.errors) > 0


class TestResultSaving:
    """Tests para guardado de resultados."""
    
    @pytest.mark.asyncio
    async def test_save_to_supabase_success(
        self,
        sample_niche,
        sample_literature_review,
        mock_supabase_client,
    ):
        """Test guardado exitoso en Supabase."""
        pipeline = AnalysisPipeline()
        
        # Mock database tool
        pipeline.database_tool.save_analysis = AsyncMock(
            return_value={"id": "test-id-123"}
        )
        
        result = PipelineResult(
            niche=sample_niche,
            status=PipelineStatus.COMPLETED,
            final_report=sample_literature_review,
        )
        result.end_time = datetime.now(timezone.utc)
        
        await pipeline._save_to_supabase(result)
        
        assert result.supabase_saved is True
        assert result.supabase_record_id == "test-id-123"
    
    @pytest.mark.asyncio
    async def test_save_to_supabase_failure(
        self,
        sample_niche,
        sample_literature_review,
    ):
        """Test cuando Supabase falla."""
        pipeline = AnalysisPipeline()
        
        # Mock database tool to fail
        pipeline.database_tool.save_analysis = AsyncMock(
            side_effect=Exception("Supabase error")
        )
        
        result = PipelineResult(
            niche=sample_niche,
            status=PipelineStatus.COMPLETED,
            final_report=sample_literature_review,
        )
        
        with pytest.raises(Exception):
            await pipeline._save_to_supabase(result)
    
    @pytest.mark.asyncio
    async def test_save_locally(
        self,
        sample_niche,
        sample_literature_review,
        temp_output_dir,
    ):
        """Test guardado local como backup."""
        pipeline = AnalysisPipeline()
        
        result = PipelineResult(
            niche=sample_niche,
            status=PipelineStatus.COMPLETED,
            final_report=sample_literature_review,
        )
        result.end_time = datetime.now(timezone.utc)
        
        with patch("pathlib.Path", return_value=temp_output_dir):
            await pipeline._save_locally(result)
        
        assert result.local_backup_path is not None


class TestPipelineResult:
    """Tests para PipelineResult dataclass."""
    
    def test_pipeline_result_creation(self, sample_niche):
        """Test creación de PipelineResult."""
        result = PipelineResult(
            niche=sample_niche,
            status=PipelineStatus.RUNNING,
        )
        
        assert result.niche == sample_niche
        assert result.status == PipelineStatus.RUNNING
        assert result.final_report is None
        assert len(result.agent_results) == 0
        assert len(result.errors) == 0
    
    def test_pipeline_result_to_dict(self, sample_niche):
        """Test serialización a dict."""
        result = PipelineResult(
            niche=sample_niche,
            status=PipelineStatus.COMPLETED,
            final_report="Test report",
        )
        result.end_time = datetime.now(timezone.utc)
        
        data = result.to_dict()
        
        assert data["niche"] == sample_niche
        assert data["status"] == "completed"
        assert data["final_report"] == "Test report"
        assert "start_time" in data
        assert "end_time" in data
