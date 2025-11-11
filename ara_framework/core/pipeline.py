"""
Pipeline Orchestration - CrewAI-based analysis pipeline.

Este módulo implementa el pipeline completo de análisis que coordina
6 agentes especializados en secuencia:

1. NicheAnalyst → 2. LiteratureResearcher → 3. TechnicalArchitect 
→ 4. ImplementationSpecialist → 5. ContentSynthesizer

El pipeline incluye:
- Context passing automático entre agentes (task dependencies)
- Budget tracking con BudgetManager
- Error handling con circuit breaker y retries
- OpenTelemetry instrumentation para observabilidad
- Structured logging con structlog
- Guardado automático en Supabase

SLA Total: ~57-70 minutos
Budget: ~3-5 créditos/análisis

Usage:
    ```python
    from core.pipeline import AnalysisPipeline
    
    pipeline = AnalysisPipeline()
    result = await pipeline.run_analysis("Rust WASM for audio processing")
    
    print(result.status)  # "completed" / "failed" / "partial"
    print(result.final_report)  # Markdown report
    print(result.metadata)  # Credits, duration, etc.
    ```

Fuente: docs/04_ARCHITECTURE.md (Pipeline Orchestration)
"""
import asyncio
import inspect
import structlog
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum

from crewai import Crew, Process, Agent, Task

try:  # CrewAI <1.x ships CrewOutput under crewai.crews
    from crewai.crews.crew_output import CrewOutput as CrewOutputType  # type: ignore
except ImportError:  # CrewAI 0.11.x and similar do not expose CrewOutput
    CrewOutputType = None  # type: ignore

# Conditional imports para OpenTelemetry (opcional)
try:
    from opentelemetry import trace
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.sdk.resources import Resource
    
    OTEL_AVAILABLE = True
except ImportError:
    OTEL_AVAILABLE = False
    trace = None

# Conditional import para circuit breaker (opcional)
try:
    from pybreaker import CircuitBreaker
    BREAKER_AVAILABLE = True
except ImportError:
    BREAKER_AVAILABLE = False
    CircuitBreaker = None

from config.settings import settings
from core.budget_manager import BudgetManager
from tools import get_database_tool
from agents import (
    create_niche_analyst,
    create_literature_researcher,
    create_technical_architect,
    create_implementation_specialist,
    create_content_synthesizer,
)

logger = structlog.get_logger(__name__)


class PipelineStatus(str, Enum):
    """Status del pipeline."""
    NOT_STARTED = "not_started"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"  # Algunos agentes completados, otros fallaron
    TIMEOUT = "timeout"


@dataclass
class AgentResult:
    """Resultado de un agente individual."""
    agent_name: str
    status: str  # "success" / "failed"
    output: Optional[str] = None
    duration_seconds: float = 0.0
    credits_used: float = 0.0
    retries: int = 0
    error: Optional[str] = None


@dataclass
class PipelineResult:
    """Resultado completo del pipeline."""
    niche: str
    status: PipelineStatus
    final_report: Optional[str] = None
    
    # Metadata
    start_time: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    end_time: Optional[datetime] = None
    duration_seconds: float = 0.0
    total_credits_used: float = 0.0
    
    # Agent results
    agent_results: List[AgentResult] = field(default_factory=list)
    
    # Storage
    supabase_saved: bool = False
    supabase_record_id: Optional[str] = None
    local_backup_path: Optional[str] = None
    
    # Errors
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a dict para JSON serialization."""
        return {
            "niche": self.niche,
            "status": self.status.value,
            "final_report": self.final_report,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_seconds": self.duration_seconds,
            "total_credits_used": self.total_credits_used,
            "agent_results": [
                {
                    "agent_name": r.agent_name,
                    "status": r.status,
                    "output_size": len(r.output) if r.output else 0,
                    "duration_seconds": r.duration_seconds,
                    "credits_used": r.credits_used,
                    "retries": r.retries,
                    "error": r.error,
                }
                for r in self.agent_results
            ],
            "supabase_saved": self.supabase_saved,
            "supabase_record_id": self.supabase_record_id,
            "local_backup_path": self.local_backup_path,
            "errors": self.errors,
            "warnings": self.warnings,
        }


class AnalysisPipeline:
    """
    Pipeline de análisis que coordina 5 agentes CrewAI.
    
    Features:
    - Sequential execution con context passing automático
    - Budget tracking
    - Error handling con retries
    - OpenTelemetry tracing (opcional)
    - Circuit breaker (opcional)
    - Structured logging
    - Auto-save a Supabase
    """
    
    def __init__(
        self,
        max_retries: int = 3,
        enable_telemetry: bool = True,
        enable_circuit_breaker: bool = True,
        timeout_minutes: int = 90,
    ):
        """
        Inicializa el pipeline.
        
        Args:
            max_retries: Máximo número de retries por agente
            enable_telemetry: Habilitar OpenTelemetry tracing
            enable_circuit_breaker: Habilitar circuit breaker
            timeout_minutes: Timeout global del pipeline
        """
        self.max_retries = max_retries
        self.timeout_minutes = timeout_minutes
        
        # Budget manager
        self.budget_manager = BudgetManager()
        
        # Database tool
        self.database_tool = get_database_tool()
        
        # OpenTelemetry setup (opcional)
        self.tracer = None
        if enable_telemetry and OTEL_AVAILABLE and settings.UPTRACE_DSN:
            self._setup_telemetry()
        elif enable_telemetry and not OTEL_AVAILABLE:
            logger.warning(
                "telemetry_requested_but_unavailable",
                reason="opentelemetry not installed",
                install_cmd="pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp",
            )
        
        # Circuit breaker (opcional)
        self.circuit_breaker = None
        if enable_circuit_breaker and BREAKER_AVAILABLE:
            self.circuit_breaker = CircuitBreaker(
                fail_max=3,
                reset_timeout=60,
                name="analysis_pipeline_breaker",
            )
            logger.info("circuit_breaker_enabled", fail_max=3, reset_timeout=60)
        elif enable_circuit_breaker and not BREAKER_AVAILABLE:
            logger.warning(
                "circuit_breaker_requested_but_unavailable",
                reason="pybreaker not installed",
                install_cmd="pip install pybreaker",
            )
        
        logger.info(
            "pipeline_initialized",
            max_retries=max_retries,
            timeout_minutes=timeout_minutes,
            telemetry_enabled=self.tracer is not None,
            circuit_breaker_enabled=self.circuit_breaker is not None,
        )
    
    def _setup_telemetry(self):
        """Configura OpenTelemetry con Uptrace."""
        try:
            # Create resource
            resource = Resource.create(
                {
                    "service.name": "ara-framework",
                    "service.version": "1.0.0",
                    "deployment.environment": "production",
                }
            )
            
            # Create tracer provider
            provider = TracerProvider(resource=resource)
            
            # Create OTLP exporter (Uptrace)
            otlp_exporter = OTLPSpanExporter(
                endpoint=settings.UPTRACE_DSN,
                headers={"uptrace-dsn": settings.UPTRACE_DSN},
            )
            
            # Add span processor
            provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
            
            # Set as global
            trace.set_tracer_provider(provider)
            
            # Get tracer
            self.tracer = trace.get_tracer(__name__)
            
            logger.info("telemetry_configured", backend="uptrace")
        except Exception as e:
            logger.error("telemetry_setup_failed", error=str(e))
            self.tracer = None
    
    def _validate_niche(self, niche: str) -> tuple[bool, Optional[str]]:
        """
        Valida que el niche sea válido.
        
        Returns:
            (is_valid, error_message)
        """
        if not niche:
            return False, "Niche is empty"
        
        if len(niche) < 5:
            return False, f"Niche too short (min 5 chars): '{niche}'"
        
        if len(niche) > 200:
            return False, f"Niche too long (max 200 chars): {len(niche)} chars"
        
        # Check for suspicious characters
        suspicious_chars = ["<", ">", "{", "}", "[", "]", "|", "\\", "^", "~"]
        for char in suspicious_chars:
            if char in niche:
                return False, f"Niche contains suspicious character: '{char}'"
        
        return True, None
    
    async def run_analysis(self, niche: str) -> PipelineResult:
        """
        Ejecuta el pipeline completo de análisis.
        
        Args:
            niche: Nombre del niche a analizar
        
        Returns:
            PipelineResult con todos los outputs y metadata
        """
        result = PipelineResult(niche=niche, status=PipelineStatus.RUNNING)
        
        # Start tracing span (si está habilitado)
        span = None
        if self.tracer:
            span = self.tracer.start_span("analysis_pipeline")
            span.set_attribute("niche", niche)
        
        try:
            logger.info(
                "pipeline_started",
                niche=niche,
                timeout_minutes=self.timeout_minutes,
                max_retries=self.max_retries,
            )
            
            # STEP 1: Validate input
            is_valid, error_msg = self._validate_niche(niche)
            if not is_valid:
                result.status = PipelineStatus.FAILED
                result.errors.append(f"Input validation failed: {error_msg}")
                logger.error("input_validation_failed", niche=niche, error=error_msg)
                return result
            
            # STEP 2: Check budget
            available_credits = await self.budget_manager.get_remaining_credits()
            estimated_cost = 5.0  # Conservador: ~3-5 créditos
            
            if available_credits < estimated_cost:
                warning = f"Low credits: {available_credits:.2f} available, ~{estimated_cost} needed. Using free fallback models."
                result.warnings.append(warning)
                logger.warning(
                    "low_credits_warning",
                    available=available_credits,
                    needed=estimated_cost,
                )
            
            # STEP 3: Create agents and tasks
            logger.info("creating_agents", niche=niche)
            
            # Agent 1: NicheAnalyst (no dependencies)
            niche_agent, niche_task = create_niche_analyst(niche)
            
            # Agent 2: LiteratureResearcher (depends on niche_task)
            lit_agent, lit_task = create_literature_researcher(
                niche, niche_analysis_task=niche_task
            )
            
            # Agent 3: TechnicalArchitect (depends on niche + literature)
            arch_agent, arch_task = create_technical_architect(
                niche, literature_research_task=lit_task
            )
            
            # Agent 4: ImplementationSpecialist (depends on architecture)
            impl_agent, impl_task = create_implementation_specialist(
                niche, architecture_task=arch_task
            )
            
            # Agent 5: ContentSynthesizer (depends on all previous)
            synth_agent, synth_task = create_content_synthesizer(
                niche, context_tasks=[niche_task, lit_task, arch_task, impl_task]
            )
            
            logger.info("agents_created", count=5)
            
            # STEP 4: Create CrewAI Crew
            # Configure embeddings for memory (using free local embeddings)
            embedder_config = {
                "provider": "google",  # Use Gemini embeddings (free)
                "config": {
                    "model": "models/embedding-001",
                    "task_type": "retrieval_document",
                }
            }
            
            crew = Crew(
                agents=[niche_agent, lit_agent, arch_agent, impl_agent, synth_agent],
                tasks=[niche_task, lit_task, arch_task, impl_task, synth_task],
                process=Process.sequential,  # Sequential execution
                verbose=True,
                memory=True,  # Enable memory for context
                embedder=embedder_config,  # Use Gemini embeddings (free with API key)
                cache=True,  # Enable caching
                max_rpm=100,  # Rate limiting
            )
            
            logger.info(
                "crew_created",
                agents_count=5,
                tasks_count=5,
                process="sequential",
            )
            
            # STEP 5: Execute crew with timeout
            crew_output = None
            try:
                # Use asyncio.wait_for for timeout
                crew_output = await asyncio.wait_for(
                    self._run_crew_with_circuit_breaker(crew, niche),
                    timeout=self.timeout_minutes * 60,
                )
                
                logger.info("crew_execution_completed")
                
            except asyncio.TimeoutError:
                result.status = PipelineStatus.TIMEOUT
                error_msg = f"Pipeline timeout after {self.timeout_minutes} minutes"
                result.errors.append(error_msg)
                logger.error("pipeline_timeout", timeout_minutes=self.timeout_minutes)
                
                # Save partial results
                await self._save_partial_results(result, niche)
                return result
            
            except Exception as e:
                result.status = PipelineStatus.FAILED
                error_msg = f"Crew execution failed: {str(e)}"
                result.errors.append(error_msg)
                logger.error("crew_execution_failed", error=str(e), exc_info=True)
                
                # Save partial results
                await self._save_partial_results(result, niche)
                return result
            
            # STEP 6: Extract final report
            final_report = self._normalize_crew_output(crew_output)
            if final_report:
                result.final_report = final_report
                result.status = PipelineStatus.COMPLETED

                logger.info(
                    "final_report_extracted",
                    report_size=len(result.final_report),
                )
            else:
                result.status = PipelineStatus.FAILED
                result.errors.append("No output from crew")
                logger.error("no_crew_output")
                return result
            
            # STEP 7: Calculate metrics
            result.end_time = datetime.now(timezone.utc)
            result.duration_seconds = (
                result.end_time - result.start_time
            ).total_seconds()
            
            # Get credits used from budget manager
            result.total_credits_used = self.budget_manager.get_usage_since(
                result.start_time
            )
            
            logger.info(
                "pipeline_metrics",
                duration_seconds=result.duration_seconds,
                duration_minutes=result.duration_seconds / 60,
                credits_used=result.total_credits_used,
            )
            
            # STEP 8: Save to Supabase
            try:
                await self._save_to_supabase(result)
            except Exception as e:
                warning = f"Supabase save failed: {str(e)}"
                result.warnings.append(warning)
                logger.warning("supabase_save_failed", error=str(e))
                
                # Fallback: Save locally
                await self._save_locally(result)
            
            logger.info(
                "pipeline_completed_successfully",
                niche=niche,
                status=result.status.value,
                duration_minutes=result.duration_seconds / 60,
                credits_used=result.total_credits_used,
                supabase_saved=result.supabase_saved,
            )
            
            return result
        
        except Exception as e:
            result.status = PipelineStatus.FAILED
            result.errors.append(f"Unexpected error: {str(e)}")
            logger.error(
                "pipeline_unexpected_error",
                niche=niche,
                error=str(e),
                exc_info=True,
            )
            return result
        
        finally:
            # End tracing span
            if span:
                span.set_attribute("status", result.status.value)
                span.set_attribute("duration_seconds", result.duration_seconds)
                span.set_attribute("credits_used", result.total_credits_used)
                span.end()
    
    async def _run_crew_with_circuit_breaker(
        self, crew: Crew, niche: str
    ) -> Any:
        """
        Ejecuta crew con circuit breaker (si está habilitado).
        
        Args:
            crew: Crew configurado
            niche: Nombre del niche
        
        Returns:
            CrewOutput
        """
        async def _execute_kickoff() -> Any:
            kickoff_async = getattr(crew, "kickoff_async", None)
            if kickoff_async and callable(kickoff_async):
                try:
                    signature = inspect.signature(kickoff_async)
                    if "inputs" in signature.parameters:
                        return await kickoff_async(inputs={"niche": niche})
                except (TypeError, ValueError):
                    pass
                return await kickoff_async()

            kickoff = getattr(crew, "kickoff", None)
            if not callable(kickoff):
                raise AttributeError("Crew instance has no kickoff method")

            loop = asyncio.get_running_loop()

            def _sync_kickoff() -> Any:
                try:
                    signature = inspect.signature(kickoff)
                    if "inputs" in signature.parameters:
                        return kickoff(inputs={"niche": niche})
                except (TypeError, ValueError):
                    pass
                return kickoff()

            return await loop.run_in_executor(None, _sync_kickoff)

        if self.circuit_breaker:
            # Wrap en circuit breaker
            @self.circuit_breaker
            async def execute():
                return await _execute_kickoff()

            return await execute()

        # Sin circuit breaker
        return await _execute_kickoff()

    def _normalize_crew_output(self, crew_output: Any) -> Optional[str]:
        """Compatibiliza diferentes versiones de CrewAI devolviendo un string."""
        if crew_output is None:
            return None

        if CrewOutputType and isinstance(crew_output, CrewOutputType):
            raw_value = getattr(crew_output, "raw", None)
            if raw_value:
                return str(raw_value)
            final_output = getattr(crew_output, "final_output", None)
            if final_output:
                return str(final_output)

        if isinstance(crew_output, str):
            return crew_output

        if isinstance(crew_output, bytes):
            try:
                return crew_output.decode("utf-8")
            except UnicodeDecodeError:
                return crew_output.decode("latin-1", errors="ignore")

        if isinstance(crew_output, dict):
            for key in ("raw", "final_output", "output"):
                value = crew_output.get(key)
                if value:
                    return str(value)

        if hasattr(crew_output, "raw") and getattr(crew_output, "raw"):
            return str(getattr(crew_output, "raw"))

        return str(crew_output)
    
    async def _save_to_supabase(self, result: PipelineResult):
        """
        Guarda análisis completo en Supabase.
        
        Args:
            result: PipelineResult a guardar
        """
        try:
            record_data = {
                "niche_name": result.niche,
                "status": result.status.value,
                "report_markdown": result.final_report,
                "metadata": {
                    "start_time": result.start_time.isoformat(),
                    "end_time": result.end_time.isoformat() if result.end_time else None,
                    "duration_seconds": result.duration_seconds,
                    "duration_minutes": result.duration_seconds / 60,
                    "total_credits_used": result.total_credits_used,
                    "agent_results": [
                        {
                            "agent_name": r.agent_name,
                            "status": r.status,
                            "duration_seconds": r.duration_seconds,
                            "credits_used": r.credits_used,
                            "retries": r.retries,
                        }
                        for r in result.agent_results
                    ],
                    "errors": result.errors,
                    "warnings": result.warnings,
                },
            }
            
            # Save using database_tool
            saved = await self.database_tool.save_analysis(**record_data)
            
            if saved:
                result.supabase_saved = True
                # Extract record ID if available
                if isinstance(saved, dict) and "id" in saved:
                    result.supabase_record_id = saved["id"]
                
                logger.info(
                    "supabase_save_success",
                    niche=result.niche,
                    record_id=result.supabase_record_id,
                )
        
        except Exception as e:
            logger.error("supabase_save_error", error=str(e), exc_info=True)
            raise
    
    async def _save_locally(self, result: PipelineResult):
        """
        Guarda análisis localmente como backup.
        
        Args:
            result: PipelineResult a guardar
        """
        import json
        from pathlib import Path
        
        # Create outputs directory
        outputs_dir = Path("./outputs")
        outputs_dir.mkdir(exist_ok=True)
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{result.niche.replace(' ', '_')}_{timestamp}.json"
        filepath = outputs_dir / filename
        
        # Save as JSON
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)
        
        result.local_backup_path = str(filepath)
        
        logger.info(
            "local_backup_saved",
            niche=result.niche,
            path=str(filepath),
        )
    
    async def _save_partial_results(self, result: PipelineResult, niche: str):
        """
        Guarda resultados parciales cuando el pipeline falla.
        
        Args:
            result: PipelineResult parcial
            niche: Nombre del niche
        """
        logger.info("saving_partial_results", niche=niche)
        
        result.status = PipelineStatus.PARTIAL
        result.end_time = datetime.now(timezone.utc)
        result.duration_seconds = (
            result.end_time - result.start_time
        ).total_seconds()
        
        # Save locally (Supabase might be down)
        await self._save_locally(result)
        
        logger.warning(
            "partial_results_saved",
            niche=niche,
            path=result.local_backup_path,
        )


async def run_quick_analysis(niche: str) -> PipelineResult:
    """
    Helper function para ejecutar análisis rápido.
    
    Args:
        niche: Nombre del niche
    
    Returns:
        PipelineResult
    
    Example:
        ```python
        result = await run_quick_analysis("Rust WASM for audio")
        print(result.final_report)
        ```
    """
    pipeline = AnalysisPipeline()
    return await pipeline.run_analysis(niche)


def run_analysis_sync(niche: str) -> PipelineResult:
    """
    Versión síncrona para convenience.
    
    Args:
        niche: Nombre del niche
    
    Returns:
        PipelineResult
    
    Example:
        ```python
        result = run_analysis_sync("Rust WASM for audio")
        ```
    """
    return asyncio.run(run_quick_analysis(niche))


if __name__ == "__main__":
    # Test básico del pipeline
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python pipeline.py '<niche>'")
        print("Example: python pipeline.py 'Rust WASM for real-time audio processing'")
        sys.exit(1)
    
    niche = sys.argv[1]
    
    print(f"🚀 Starting analysis for: {niche}")
    print(f"⏱️  Estimated time: 57-70 minutes")
    print(f"💰 Estimated cost: ~3-5 credits")
    print()
    
    result = run_analysis_sync(niche)
    
    print()
    print(f"✅ Pipeline completed: {result.status.value}")
    print(f"⏱️  Duration: {result.duration_seconds / 60:.1f} minutes")
    print(f"💰 Credits used: {result.total_credits_used:.2f}")
    print(f"📊 Report size: {len(result.final_report) if result.final_report else 0} characters")
    
    if result.supabase_saved:
        print(f"💾 Saved to Supabase: {result.supabase_record_id}")
    elif result.local_backup_path:
        print(f"💾 Saved locally: {result.local_backup_path}")
    
    if result.errors:
        print(f"❌ Errors: {len(result.errors)}")
        for error in result.errors:
            print(f"   - {error}")
    
    if result.warnings:
        print(f"⚠️  Warnings: {len(result.warnings)}")
        for warning in result.warnings:
            print(f"   - {warning}")
