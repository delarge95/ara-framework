# 🔧 ARA Framework - Technical Specifications

**Version**: 2.2.0  
**Created**: 2025-11-08  
**Last Updated**: 2025-12-19  
**Status**: ARA 2.2 Incremental Upgrade Specifications  
**Strategy**: Maintain existing interfaces while upgrading implementations
**Related**: `.speckit/constitution.md`, `.speckit/plan.md`

---

## 📦 Module Specifications - ARA 2.2

### 1. Core Pipeline (`core/pipeline.py`) - CURRENT + UPGRADES

#### Purpose

Orchestrate multi-agent LangGraph workflow for complete MVP construction from concept to deployment.

#### Current Implementation (PRESERVED)

##### `AnalysisPipeline` Class
```python
class AnalysisPipeline:
    """Main orchestration pipeline - UPGRADED to MVP construction.

    Current Responsibilities (MAINTAINED):
    - Input validation and sanitization
    - Budget checking with kill switches
    - Agent creation and coordination (6 agents)
    - LangGraph execution with checkpointing
    
    NEW ARA 2.2 Features:
    - Cache-first routing with AdaptiveRouter
    - Real-time telemetry and observability
    - Human gates with optimistic locking
    - Supply chain security with ARAShield 2.2
    - Chaos engineering integration
    - Result persistence (Supabase + local)
    - Error handling and partial result saving
    """

    def __init__(
        self,
        settings: Optional[Settings] = None,
        budget_manager: Optional[BudgetManager] = None,
    ) -> None:
        """Initialize pipeline with configuration."""

    async def run_analysis(self, niche: str) -> PipelineResult:
        """Execute full analysis pipeline.

        Args:
            niche: Technology niche to analyze (3-200 chars)

        Returns:
            PipelineResult with status, final_report, errors

        Raises:
            ValueError: Invalid niche input
            BudgetExceededError: Insufficient credits
            TimeoutError: Execution timeout (30min default)
        """
```

##### Input Validation

```python
def _validate_niche(self, niche: str) -> bool:
    """Validate niche input.

    Rules:
    - Length: 3-200 characters
    - No empty/whitespace only
    - No suspicious patterns (excessive symbols)

    Returns:
        bool: True if valid
    """
```

##### Agent Creation Pattern

```python
# Sequential agent creation with context passing
niche_agent, niche_task = create_niche_analyst(niche)
lit_agent, lit_task = create_literature_researcher(niche, context_task=niche_task)
arch_agent, arch_task = create_technical_architect(niche, context_task=lit_task)
impl_agent, impl_task = create_implementation_specialist(niche, architecture_task=arch_task)
synth_agent, synth_task = create_content_synthesizer(niche, context_tasks=[...])
```

##### Crew Configuration

```python
crew = Crew(
    agents=[niche_agent, lit_agent, arch_agent, impl_agent, synth_agent],
    tasks=[niche_task, lit_task, arch_task, impl_task, synth_task],
    # StateGraph with sequential execution
    verbose=True,
    memory=True,  # Enable context memory
    cache=True,   # Enable response caching
    max_rpm=100,  # Rate limit
)
```

#### Testing Strategy

**Unit Tests** (`tests/test_pipeline.py`):

- Mock all agent creation functions
- Mock `Crew()` constructor to prevent real LLM calls
- Mock `_run_crew_with_circuit_breaker` for execution control
- Mock Supabase save operations

**Key Mocks**:

```python
# Session-level mock to avoid import errors
@pytest.fixture(scope="session", autouse=True)
def mock_langchain_google_genai():
    fake_module = MagicMock()
    fake_module.ChatGoogleGenerativeAI = MagicMock()
    sys.modules['langchain_google_genai'] = fake_module
    sys.modules['langchain_google_genai._enums'] = fake_module
    yield
    # Cleanup after all tests

# Test-level mocks for agent creation
with patch('agents.niche_analyst.create_niche_analyst', return_value=(mock_agent, mock_task)):
    with patch('core.pipeline.Crew', return_value=mock_crew):
        # Execute test
```

---

### 2. Budget Manager (`core/budget_manager.py`)

#### Purpose

Track LLM credit usage and enforce budget limits.

#### Key Components

##### `BudgetManager` Class

```python
class BudgetManager:
    """Manage budget and track LLM usage.

    Features:
    - Per-model cost calculation
    - Usage history tracking
    - Alert thresholds (80% warning)
    - Rate limiting (requests per minute)
    - Redis caching (optional)
    """

    def __init__(
        self,
        total_credits: float = 100.0,
        alert_threshold: float = 0.8,
        redis_url: Optional[str] = None,
    ) -> None:
        """Initialize budget manager."""

    async def track_usage(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int,
    ) -> None:
        """Track token usage for a model."""

    async def get_remaining_credits(self) -> float:
        """Get remaining credits."""

    async def check_rate_limit(self, model: str) -> bool:
        """Check if rate limit allows request."""
```

##### Model Costs Configuration

```python
MODEL_COSTS = {
    "gpt-5": ModelCost(
        name="gpt-5",
        input_cost_per_1k=0.03,
        output_cost_per_1k=0.06,
        max_rpm=500,
    ),
    "claude-sonnet-4.5": ModelCost(
        name="claude-sonnet-4.5",
        input_cost_per_1k=0.015,
        output_cost_per_1k=0.075,
        max_rpm=1000,
    ),
    "gemini-2.5-pro": ModelCost(
        name="gemini-2.5-pro",
        input_cost_per_1k=0.00125,
        output_cost_per_1k=0.005,
        max_rpm=60,
    ),
    # ...
}
```

#### Testing Strategy

**Current Issues** (11 failing tests):

```python
# ❌ WRONG: lowercase 'redis'
patch("core.budget_manager.redis.from_url", return_value=mock_redis_client)

# ✅ CORRECT: uppercase 'Redis' (class name)
patch("core.budget_manager.Redis.from_url", return_value=mock_redis_client)
```

**BudgetStatus Constructor**:

```python
# Test expects this signature:
BudgetStatus(
    total_credits=100.0,  # ❌ This parameter doesn't exist
    used_credits=20.0,
    remaining_credits=80.0,
    alert_triggered=False,
)

# Actual signature (need to check core/budget_manager.py):
@dataclass
class BudgetStatus:
    used_credits: float
    remaining_credits: float
    alert_triggered: bool
    # total_credits not in constructor
```

---

### 3. Tools Layer (`tools/`)

#### Purpose

Provide reusable tools for agents (search, scraping, database, PDF).

#### Tool Interfaces

##### `SearchTool` (`tools/search_tool.py`)

```python
class SearchTool:
    """Academic paper search via Semantic Scholar."""

    def __init__(self, semantic_scholar_mcp: Optional[MCPAdapter] = None):
        """Initialize with MCP adapter."""

    async def search_academic_papers(
        self,
        query: str,
        limit: int = 10,
        fields: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Search papers by query."""

    async def search_papers_parallel(
        self,
        queries: List[str],
        limit_per_query: int = 10,
    ) -> List[Dict[str, Any]]:
        """Search multiple queries in parallel."""
```

##### `ScrapingTool` (`tools/scraping_tool.py`)

```python
class ScrapingTool:
    """Web scraping via Playwright."""

    def __init__(self, playwright_mcp: Optional[MCPAdapter] = None):
        """Initialize with MCP adapter."""

    async def scrape_website(
        self,
        url: str,
        wait_for: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Scrape website content."""
```

##### `PDFTool` (`tools/pdf_tool.py`)

```python
class PDFTool:
    """PDF processing via MarkItDown."""

    def __init__(self, markitdown_mcp: Optional[MCPAdapter] = None):
        """Initialize with MCP adapter."""

    async def convert_pdf_to_markdown(
        self,
        file_path: str,
    ) -> str:
        """Convert PDF to Markdown."""
```

##### `DatabaseTool` (`tools/database_tool.py`)

```python
class DatabaseTool:
    """Supabase persistence."""

    def __init__(self, supabase_mcp: Optional[MCPAdapter] = None):
        """Initialize with MCP adapter."""

    async def save_paper(
        self,
        paper_id: str,
        title: str,
        abstract: str,
        year: int,
        citations: int,
    ) -> Dict[str, Any]:
        """Save paper to database."""
```

#### Testing Issues (8 failing tests)

**Problem**: Tests assume MCP attributes that don't exist

```python
# ❌ Test assumes this exists:
tool.playwright_mcp.scrape(...)
tool.supabase_mcp.insert_record(...)
tool.markitdown_mcp.convert(...)

# ✅ But tools actually have direct methods:
tool.scrape_website(...)
tool.save_paper(...)
tool.convert_pdf_to_markdown(...)
```

**Solution Options**:

**Option A: Update Tests** (Recommended)

```python
# Mock the actual public method
with patch("tools.scraping_tool.ScrapingTool.scrape_website", new_callable=AsyncMock):
    result = await tool.scrape_website(url)
```

**Option B: Add MCP Attributes**

```python
class ScrapingTool:
    def __init__(self):
        self.playwright_mcp = PlaywrightMCPAdapter()  # Add this
```

---

### 4. Agents Layer (`agents/`)

#### Purpose

Define specialized AI agents for each analysis phase.

#### Agent Creation Pattern

All agents follow this factory pattern:

```python
def create_<agent_name>(
    niche: str,
    context_task: Optional[Task] = None,
    **kwargs
) -> Tuple[Agent, Task]:
    """Create agent and task.

    Args:
        niche: Target niche for analysis
        context_task: Previous task for context passing
        **kwargs: Additional agent/task configuration

    Returns:
        (agent, task): Configured Agent and Task instances
    """

    # 1. Define agent with role, goal, backstory
    agent = Agent(
        role="...",
        goal="...",
        backstory="...",
        tools=[tool1, tool2],
        llm=llm_instance,
        verbose=True,
        max_rpm=...,
    )

    # 2. Define task with description, expected output
    task = Task(
        description="...",
        expected_output="...",
        agent=agent,
        context=[context_task] if context_task else [],
    )

    return agent, task
```

#### Agent Specifications

##### 1. NicheAnalyst (Gemini 2.5 Pro)

```python
# agents/niche_analyst.py
def create_niche_analyst(niche: str) -> Tuple[Agent, Task]:
    """
    Purpose: Market viability analysis
    Model: Gemini 2.5 Pro (cost-effective, creative)
    Duration: 7-8 min
    Cost: ~0.45 credits
    Tools: scraping_tool, search_tool

    Outputs:
    - Market size estimation
    - Trend analysis
    - Opportunity identification
    - Risk assessment
    """
```

##### 2. LiteratureResearcher (GPT-5)

```python
# agents/literature_researcher.py
def create_literature_researcher(
    niche: str,
    context_task: Task
) -> Tuple[Agent, Task]:
    """
    Purpose: Academic research and paper analysis
    Model: GPT-5 (best reasoning, extensive output)
    Duration: 20-25 min
    Cost: ~2.0 credits
    Tools: search_tool, pdf_tool, database_tool

    Outputs:
    - Top 50-100 papers analyzed
    - State-of-the-art summary
    - Research gaps identified
    - Citation network map
    """
```

##### 3. TechnicalArchitect (Claude Sonnet 4.5)

```python
# agents/technical_architect.py
def create_technical_architect(
    niche: str,
    context_task: Task
) -> Tuple[Agent, Task]:
    """
    Purpose: System design and architecture
    Model: Claude Sonnet 4.5 (structured thinking)
    Duration: 10-12 min
    Cost: ~0.75 credits
    Tools: scraping_tool, database_tool

    Outputs:
    - System architecture diagram
    - Technology stack recommendation
    - Scalability considerations
    - Security best practices
    """
```

##### 4. ImplementationSpecialist (DeepSeek V3)

```python
# agents/implementation_specialist.py
def create_implementation_specialist(
    niche: str,
    architecture_task: Task
) -> Tuple[Agent, Task]:
    """
    Purpose: Implementation roadmap and code planning
    Model: DeepSeek V3 (cost-effective, code-focused)
    Duration: 7-8 min
    Cost: ~0.25 credits
    Tools: scraping_tool, database_tool

    Outputs:
    - Sprint-by-sprint roadmap
    - Code structure recommendations
    - Testing strategy
    - Deployment plan
    """
```

##### 5. ContentSynthesizer (GPT-5)

```python
# agents/content_synthesizer.py
def create_content_synthesizer(
    niche: str,
    context_tasks: List[Task]
) -> Tuple[Agent, Task]:
    """
    Purpose: Executive report generation
    Model: GPT-5 (best synthesis, writing quality)
    Duration: 9-10 min
    Cost: ~1.0 credit
    Tools: database_tool

    Outputs:
    - Executive summary (2-3 pages)
    - Key findings
    - Actionable recommendations
    - Resource links
    """
```

---

### 5. Configuration (`config/settings.py`)

#### Purpose

Centralized configuration with Pydantic Settings.

#### Specifications

```python
class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Keys
    OPENAI_API_KEY: str
    ANTHROPIC_API_KEY: str
    GOOGLE_API_KEY: Optional[str] = None
    DEEPSEEK_API_KEY: Optional[str] = None

    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str

    # Redis (optional)
    REDIS_URL: Optional[str] = None

    # Budget
    TOTAL_BUDGET_CREDITS: float = 100.0
    ALERT_THRESHOLD: float = 0.8

    # Pipeline
    PIPELINE_TIMEOUT: int = 1800  # 30 minutes
    MAX_RETRIES: int = 3

    # Output
    OUTPUT_DIR: Path = Path("outputs")
    SAVE_LOCAL_BACKUP: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
```

---

## 🧪 Testing Specifications

### Test Organization

```
tests/
├── conftest.py              # Shared fixtures
├── test_budget_manager.py   # Budget tracking tests
├── test_pipeline.py         # Pipeline orchestration tests
├── test_tools.py            # Tool layer tests
└── integration/             # (future) Real API tests
    └── test_end_to_end.py
```

### Fixture Standards

#### Session-Level Fixtures

```python
@pytest.fixture(scope="session", autouse=True)
def mock_langchain_google_genai():
    """Mock langchain_google_genai to avoid import errors."""
    # Prevents: AttributeError: GenerationConfig has no attribute 'MediaResolution'
```

#### Function-Level Fixtures

```python
@pytest.fixture
def sample_niche() -> str:
    """Standard test niche."""
    return "Rust WASM for real-time audio processing"

@pytest.fixture
def mock_budget_manager() -> MagicMock:
    """Mock budget manager with AsyncMock methods."""
    manager = MagicMock()
    manager.get_remaining_credits = AsyncMock(return_value=10.0)
    return manager
```

### Mocking Patterns

#### Pattern 1: Mock Agent Creation

```python
# agents/<module>.py exports create_* functions
# Mock at import level to prevent real LLM initialization

with patch('agents.niche_analyst.create_niche_analyst', return_value=(mock_agent, mock_task)):
    # Test code
```

#### Pattern 2: Mock Crew Execution

```python
# Crew() constructor validates and initializes real CrewAI objects
# Mock constructor to return fake Crew

with patch('core.pipeline.Crew', return_value=mock_crew):
    # Test code
```

#### Pattern 3: Mock Async Methods

```python
# Methods that use 'await' must return AsyncMock

mock_manager.get_remaining_credits = AsyncMock(return_value=10.0)
# NOT: MagicMock(return_value=10.0)  # ❌ TypeError: can't await float
```

---

## 📊 Data Models

### PipelineResult

```python
@dataclass
class PipelineResult:
    """Result of pipeline execution."""

    niche: str
    status: PipelineStatus  # COMPLETED, FAILED, TIMEOUT
    final_report: Optional[str]
    errors: List[str]
    execution_time_seconds: float
    agents_executed: List[str]
    credits_used: float
    timestamp: datetime

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for JSON storage."""
```

### BudgetStatus

```python
@dataclass
class BudgetStatus:
    """Current budget state."""

    used_credits: float
    remaining_credits: float
    alert_triggered: bool
    usage_by_model: Dict[str, float]
    last_updated: datetime
```

### ModelCost

```python
@dataclass
class ModelCost:
    """Cost configuration for LLM model."""

    name: str
    input_cost_per_1k: float
    output_cost_per_1k: float
    max_rpm: int
    is_free: bool = False
```

---

## 🔌 External Integrations

### Semantic Scholar API

```python
# Rate limits: 100 requests/5min
# Fields: paperId, title, abstract, authors, year, citationCount, etc.
# Endpoint: https://api.semanticscholar.org/graph/v1/paper/search
```

### Supabase Schema

```sql
-- papers table
CREATE TABLE papers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    paper_id TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    abstract TEXT,
    year INTEGER,
    citation_count INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

-- analyses table
CREATE TABLE analyses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    niche TEXT NOT NULL,
    final_report TEXT NOT NULL,
    status TEXT NOT NULL,
    credits_used FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🚀 Performance Targets

### Execution Time

- Full analysis: <60 min (target: 45-55 min)
- Per agent: 5-25 min (depends on model)
- Supabase save: <2 seconds
- Local save: <1 second

### Resource Usage

- Memory: <2GB peak
- CPU: Mostly I/O bound (API calls)
- Disk: <100MB per analysis (JSON outputs)

### Cost Efficiency

- Target: <$5 per analysis
- Current estimate: $4.70 (based on model costs)
- Budget alerts at 80% ($4.00)

---

**Next Update**: After Phase 1 completion  
**Specification Owner**: GitHub Copilot  
**Last Validated**: 2025-11-08
