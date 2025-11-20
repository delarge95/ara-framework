"""Orchestrator agent setup for coordinating the CrewAI pipeline."""

from datetime import datetime, timezone
from textwrap import dedent
from typing import Any, Dict, Optional

import structlog
# from crewai import Agent, Task  # LEGACY: CrewAI removed, using LangGraph only

from config.settings import settings
from core.budget_manager import BudgetManager
from tools import get_database_tool


logger = structlog.get_logger()


def _build_budget_snapshot(budget_manager: BudgetManager) -> Dict[str, Any]:
    """Return lightweight budget context for telemetry logs."""
    return {
        "manager_class": budget_manager.__class__.__name__,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def create_orchestrator_agent() -> Agent:
    """Create and configure the orchestration agent."""
    database_tool = get_database_tool()

    try:
        from langchain_openai import ChatOpenAI
    except ImportError as exc:  # pragma: no cover - optional dependency
        logger.error("chat_openai_import_failed", error=str(exc))
        raise

    try:
        llm = ChatOpenAI(
            model="gpt-5",
            temperature=0.3,
            openai_api_key=settings.OPENAI_API_KEY,
            max_tokens=4096,
        )
        model_info = "gpt-5 (primary)"
    except Exception as exc:  # pragma: no cover - fallback path
        logger.warning(
            "gpt5_unavailable_falling_back_to_gpt4o",
            error=str(exc),
            fallback="gpt-4o",
        )
        llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.3,
            openai_api_key=settings.OPENAI_API_KEY,
        )
        model_info = "gpt-4o (fallback, free)"

    agent = Agent(
        role="Pipeline Orchestrator & Execution Manager",
        goal=dedent(
            """
            Coordinar el pipeline end-to-end garantizando validaciones, logging detallado y handoffs impecables entre agentes.
            """
        ).strip(),
        backstory=dedent(
            """
            Eres un project manager técnico obsesionado con la confiabilidad. Planificas, validas y registras la ejecución completa, asegurando que cada agente entregue resultados accionables.
            """
        ).strip(),
        tools=[
            database_tool.save_analysis,
            database_tool.get_previous_analysis,
            database_tool.save_paper,
            database_tool.log_model_usage,
            database_tool.get_usage_statistics,
        ],
        llm=llm,
        verbose=True,
        memory=True,
        allow_delegation=False,
        max_iter=10,
        max_rpm=20,
    )

    logger.info(
        "orchestrator_created",
        model=model_info,
        tools_count=5,
        estimated_duration="5-7 minutes coordination time",
        expected_credits=1.0,
    )

    return agent


def create_orchestration_task(
    agent: Agent,
    niche: str,
    budget_manager: Optional[BudgetManager] = None,
) -> Task:
    """Create the orchestration task instructions."""
    budget_snapshot: Optional[Dict[str, Any]] = None
    if budget_manager is not None:
        budget_snapshot = _build_budget_snapshot(budget_manager)

    description = dedent(
        """
        Coordina ejecución completa del pipeline de análisis para "__NICHE__".

        **INPUT**: Niche name = "__NICHE__"

        **TU PROCESO** (5-7 minutos de coordinación):

        **PASO 1: Validación de Inputs (30 segundos)**

        Verifica:
        - Niche no es vacío: ✓ / ✗
        - Longitud razonable (5-100 chars): ✓ / ✗
        - Sin caracteres inválidos: ✓ / ✗

        Si falla alguna validación:
        - Log error
        - Return: {"status": "invalid_input", "error": "..."}
        - ABORT pipeline

        **PASO 2: Budget Check (30 segundos)**

        Query BudgetManager:
        ```python
        budget_manager = BudgetManager()
        available_credits = budget_manager.get_remaining_credits()
        estimated_cost = 5-8  # créditos para análisis completo

        if available_credits < estimated_cost:
            logger.warning("low_credits", available=available_credits, needed=estimated_cost)
            # Continuar de todos modos (fallbacks son free)
        ```

        **PASO 3: Supabase Connection Check (30 segundos)**

        Intenta query simple:
        ```python
        try:
            test = database_tool.get_usage_statistics()
            logger.info("supabase_connected")
        except Exception as e:
            logger.error("supabase_unavailable", error=str(e))
            # Continuar - guardaremos localmente si es necesario
        ```

        **PASO 4: Coordinar Agentes (esto lo hace CrewAI automáticamente)**

        IMPORTANTE: NO ejecutes los agentes tú mismo.
        Tu tarea en CrewAI es definir el PLAN de coordinación.
        CrewAI ejecutará los agentes basándose en este plan.

        Tu output debe ser un PLAN en Markdown:

        ```markdown
        # Pipeline Execution Plan for: __NICHE__

        ## Pre-Execution Checklist
        - [x] Input validation: PASSED
        - [x] Budget check: [X credits available]
        - [x] Supabase connection: [CONNECTED / OFFLINE]

        ## Execution Sequence

        ### Agent 1: NicheAnalyst
        - **SLA**: 7-8 minutes
        - **Inputs**: niche = "__NICHE__"
        - **Expected output**: niche_analysis.md (~5000-7000 palabras)
        - **Validation criteria**:
          * Contains "## 1." (Markdown sections)
          * Contains "Viabilidad:" (score)
          * Length > 3000 characters
        - **Retry policy**: Max 3 retries, exponential backoff
        - **Status**: PENDING

        ### Agent 2: LiteratureResearcher
        - **SLA**: 20-25 minutes
        - **Inputs**: niche + niche_analysis.md (from Agent 1)
        - **Dependencies**: Agent 1 SUCCESS
        - **Expected output**: literature_review.md (~8000-12000 palabras)
        - **Validation criteria**:
          * Contains "## 1."
          * Contains "paper" or "papers"
          * Length > 5000 characters
        - **Retry policy**: Max 3 retries
        - **Status**: PENDING

        ### Agent 3: TechnicalArchitect
        - **SLA**: 10-12 minutes
        - **Inputs**: niche + niche_analysis.md + literature_review.md
        - **Dependencies**: Agent 1, 2 SUCCESS
        - **Expected output**: architecture_doc.md (~6000-10000 palabras)
        - **Validation criteria**:
          * Contains "Arquitectura" or "Architecture"
          * Contains "Componentes" or "Components"
          * Length > 4000 characters
        - **Retry policy**: Max 3 retries
        - **Status**: PENDING

        ### Agent 4: ImplementationSpecialist
        - **SLA**: 7-8 minutes
        - **Inputs**: niche + architecture_doc.md
        - **Dependencies**: Agent 3 SUCCESS
        - **Expected output**: implementation_plan.md (~5000-7000 palabras)
        - **Validation criteria**:
          * Contains "US-" or "User Story"
          * Contains "Sprint"
          * Length > 3000 characters
        - **Retry policy**: Max 3 retries
        - **Status**: PENDING

        ### Agent 5: ContentSynthesizer
        - **SLA**: 9-10 minutes
        - **Inputs**: niche + ALL previous outputs
        - **Dependencies**: Agent 1, 2, 3, 4 SUCCESS
        - **Expected output**: final_report.md (~10000-15000 palabras)
        - **Validation criteria**:
          * Contains "Executive Summary"
          * Contains "## 1." (12 sections)
          * Length > 8000 characters
        - **Retry policy**: Max 3 retries
        - **Status**: PENDING

        ## Post-Execution Tasks

        ### Save to Supabase
        - **Table**: analyses
        - **Data**:
          ```json
          {
            "niche_name": "__NICHE__",
            "status": "completed",
            "report_markdown": "[final_report.md content]",
            "metadata": {
              "credits_used": X,
              "duration_minutes": Y,
              "agents_executed": ["NicheAnalyst", "LiteratureResearcher", ...],
              "timestamp": "2024-01-01T00:00:00Z",
              "errors": []
            }
          }
          ```
        - **Retry policy**: Max 3 retries

        ### Local Backup (if Supabase fails)
        - **Path**: ./outputs/__NICHE__{timestamp}.json
        - **Include**: All agent outputs + metadata

        ### Final Logging
        ```python
        logger.info(
            "pipeline_completed",
            niche="__NICHE__",
            status="completed",
            total_credits=X,
            total_duration_minutes=Y,
            final_report_size=Z,
        )
        ```

        ## Error Handling

        ### If any agent fails after 3 retries:
        1. Log error with stacktrace
        2. Save partial results (outputs from successful agents)
        3. Set status = "partial"
        4. Return partial analysis

        ### If budget insufficient:
        1. Log warning
        2. Continue (fallback models are free)
        3. Track which models were used (primary vs fallback)

        ### If Supabase unavailable:
        1. Save to local file: ./outputs/__NICHE__{timestamp}.json
        2. Log path to local file
        3. Return success with note about local save

        ### If global timeout (>90 minutes):
        1. Abort pipeline
        2. Save partial results
        3. Log "pipeline_timeout"
        4. Return status = "timeout"

        ## Expected Timeline

        - **Pre-execution**: 1-2 minutes
        - **Agent 1 (NicheAnalyst)**: 7-8 minutos
        - **Agent 2 (LiteratureResearcher)**: 20-25 minutos ← BOTTLENECK
        - **Agent 3 (TechnicalArchitect)**: 10-12 minutos
        - **Agent 4 (ImplementationSpecialist)**: 7-8 minutos
        - **Agent 5 (ContentSynthesizer)**: 9-10 minutos
        - **Post-execution**: 2-3 minutos

        **Total**: ~57-70 minutos

        ## Success Criteria

        Pipeline is successful if:
        - [x] All 5 agents executed successfully
        - [x] All outputs passed validation
        - [x] Final report saved to Supabase (or locally)
        - [x] Credits tracked correctly
        - [x] No errors in logs (or all errors handled)

        ---

        **Orchestrator Note**:
        This is a PLAN. CrewAI will execute it.
        My role: Coordinate, validate, log, save.
        I don't do the technical analysis - I manage the pipeline.
        ```

        **OUTPUT FINAL** (después de que CrewAI ejecute todo):

        Debes generar un execution summary:
        """
    ).strip().replace("__NICHE__", niche)

    expected_output = dedent(
        """
        # Pipeline Execution Summary: __NICHE__

        ## Status
        **Overall**: [COMPLETED / PARTIAL / FAILED]

        ## Execution Timeline
        - **Start**: [Timestamp ISO8601]
        - **End**: [Timestamp ISO8601]
        - **Duration**: [X minutes Y seconds]

        ## Agents Executed

        ### 1. NicheAnalyst
        - **Status**: [SUCCESS / FAILED]
        - **Duration**: [X min]
        - **Output size**: [Y caracteres]
        - **Retries**: [N]
        - **Errors**: [None / Error message]

        ### 2. LiteratureResearcher
        [Misma estructura]

        ### 3. TechnicalArchitect
        [Misma estructura]

        ### 4. ImplementationSpecialist
        [Misma estructura]

        ### 5. ContentSynthesizer
        [Misma estructura]

        ## Resource Usage
        - **Total credits used**: [X credits]
        - **Credits breakdown**:
          * NicheAnalyst: [0 credits (Gemini free)]
          * LiteratureResearcher: [~0.15-1.5 credits (GPT-5)]
          * TechnicalArchitect: [~1 credit (Claude Sonnet)]
          * ImplementationSpecialist: [~0.33 credits (DeepSeek/Haiku)]
          * ContentSynthesizer: [~0.5 credits (GPT-5)]
          * Orchestrator: [~1 credit (GPT-5)]

        - **Credits remaining**: [Y credits]

        ## Output Storage
        - **Supabase**: [SAVED / FAILED]
        - **Table**: analyses
        - **Record ID**: [UUID if saved]
        - **Local backup**: [Path if Supabase failed]

        ## Final Report
        - **Size**: [X palabras / Y caracteres]
        - **Sections**: 12
        - **Format**: Markdown
        - **Location**: [Supabase path or local path]

        ## Errors and Warnings
        [Si no hubo errores: "None"]
        [Si hubo errores: Lista con timestamps y detalles]

        ## Validation Results
        - **NicheAnalyst output**: [VALID / INVALID] - [Validation details]
        - **LiteratureResearcher output**: [VALID / INVALID]
        - **TechnicalArchitect output**: [VALID / INVALID]
        - **ImplementationSpecialist output**: [VALID / INVALID]
        - **ContentSynthesizer output**: [VALID / INVALID]

        ## Performance Metrics
        - **SLA adherence**:
          * NicheAnalyst: [Within SLA: YES/NO] (Target: 7-8 min, Actual: X min)
          * LiteratureResearcher: [Within SLA: YES/NO] (Target: 20-25 min, Actual: Y min)
          * [Others...]

        - **Success rate**: [X/5 agents succeeded = Y%]
        - **Retry rate**: [N total retries across all agents]

        ## Recommendations for Next Run
        [Si hubo issues, sugiere mejoras]
        [Ej: "LiteratureResearcher exceeded SLA by 10 min - consider increasing timeout"]
        [Ej: "Consider pre-caching papers to reduce LiteratureResearcher duration"]

        ## Next Steps for User
        1. [Acción 1 basada en el reporte generado]
        2. [Acción 2]
        3. [Acción 3]

        ---

        **Pipeline Completed Successfully**

        To view the full report:
        - Supabase: [Link o query]
        - Local: [Path to file]

        To re-run analysis:
        ```bash
        ara run "__NICHE__"
        ```
        """
    ).strip().replace("__NICHE__", niche)

    task = Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
    )

    logger.info(
        "orchestration_task_created",
        niche=niche,
        estimated_coordination_time="5-7 minutes",
        total_pipeline_time="57-70 minutes",
        agents_to_coordinate=5,
        budget_snapshot=budget_snapshot,
    )

    return task


def create_orchestrator(niche: str) -> tuple[Agent, Task]:
    """Create orchestrator agent and task pair for a niche."""
    agent = create_orchestrator_agent()
    budget_manager = BudgetManager()
    task = create_orchestration_task(agent, niche, budget_manager=budget_manager)

    logger.info(
        "orchestrator_ready",
        niche=niche,
        role="coordination_only",
        sla="5-7 minutes coordination",
        budget="~1 credit",
        budget_manager_class=budget_manager.__class__.__name__,
    )

    return agent, task

