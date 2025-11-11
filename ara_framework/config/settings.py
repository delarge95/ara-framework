"""
Configuración global del ARA Framework.

Fuente: docs/02_PROJECT_CONSTITUTION.md (Stack definitivo Nov 2025)
"""
import os
from typing import Literal, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración del proyecto con validación Pydantic."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # ============================================================
    # ENVIRONMENT
    # ============================================================
    ENV: Literal["development", "production"] = "development"
    DEBUG: bool = True
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    LOG_FORMAT: Literal["json", "text"] = "json"
    
    # ============================================================
    # GITHUB COPILOT PRO + CONTINUE.DEV
    # ============================================================
    # Continue.dev maneja la autenticación automáticamente
    # No requiere API key explícita, usa GitHub OAuth
    
    # ============================================================
    # GEMINI 2.5 PRO (FREE - 1500 req/día)
    # ============================================================
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-2.5-pro"
    GEMINI_TEMPERATURE: float = 0.7
    
    # ============================================================
    # DEEPSEEK V3 (685B MoE - $0.27/M input, $1.10/M output)
    # ============================================================
    DEEPSEEK_API_KEY: Optional[str] = None
    DEEPSEEK_MODEL: str = "deepseek-chat"
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com"
    DEEPSEEK_TEMPERATURE: float = 0.7
    
    # ============================================================
    # MINIMAX-M2 (229B MoE - Beta Gratuita)
    # ============================================================
    MINIMAX_API_KEY: Optional[str] = None
    MINIMAX_MODEL: str = "minimax-m2"
    MINIMAX_BASE_URL: str = "https://api.minimaxi.com/v1"
    MINIMAX_TEMPERATURE: float = 0.7
    
    # ============================================================
    # ANTHROPIC CLAUDE (via Copilot Pro - 0.33x/1x credits)
    # ============================================================
    ANTHROPIC_API_KEY: Optional[str] = None  # Opcional, Copilot Pro lo maneja
    
    # ============================================================
    # OPENAI (GPT-5, GPT-4o via Copilot Pro - 0x/1x credits)
    # ============================================================
    OPENAI_API_KEY: Optional[str] = None  # Opcional, Copilot Pro lo maneja
    
    # ============================================================
    # MCP SERVERS - Tokens y URLs
    # ============================================================
    # GitHub MCP
    GITHUB_PERSONAL_ACCESS_TOKEN: Optional[str] = None
    
    # Jina AI Reader MCP (scraping avanzado)
    JINA_API_KEY: Optional[str] = None
    
    # Supabase MCP (PostgreSQL + Storage)
    SUPABASE_URL: Optional[str] = None
    SUPABASE_ANON_KEY: Optional[str] = None
    SUPABASE_SERVICE_ROLE_KEY: Optional[str] = None
    
    # Notion MCP (opcional)
    NOTION_API_KEY: Optional[str] = None
    
    # Composio/Rube MCP (workflows)
    COMPOSIO_API_KEY: Optional[str] = None
    
    # ============================================================
    # SEMANTIC SCHOLAR API (No requiere key, 1 req/seg limit)
    # ============================================================
    SEMANTIC_SCHOLAR_DELAY: float = 1.0  # 1 segundo entre requests (CRÍTICO)
    SEMANTIC_SCHOLAR_BASE_URL: str = "https://api.semanticscholar.org/graph/v1"
    
    # ============================================================
    # VALKEY/REDIS - Cache Configuration
    # ============================================================
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_TTL_PAPERS: int = 604800  # 7 días (papers son estables)
    REDIS_TTL_CONTENT: int = 259200  # 3 días (scraped content)
    REDIS_TTL_ANALYSIS: int = 2592000  # 30 días (resultados de análisis)
    REDIS_MAX_CONNECTIONS: int = 10
    
    # ============================================================
    # UPTRACE - Observability (1TB/mes gratis)
    # ============================================================
    UPTRACE_DSN: Optional[str] = None
    UPTRACE_SERVICE_NAME: str = "ara-framework"
    UPTRACE_SERVICE_VERSION: str = "0.1.0"
    
    # ============================================================
    # AGENT TIMEOUTS (segundos) - SLAs por agente
    # ============================================================
    AGENT_TIMEOUT_NICHE: int = 480  # 8 min (NicheAnalyst)
    AGENT_TIMEOUT_LITERATURE: int = 1500  # 25 min (LiteratureResearcher - bottleneck)
    AGENT_TIMEOUT_ARCHITECT: int = 720  # 12 min (TechnicalArchitect)
    AGENT_TIMEOUT_IMPLEMENTATION: int = 480  # 8 min (ImplementationSpecialist)
    AGENT_TIMEOUT_SYNTHESIS: int = 600  # 10 min (ContentSynthesizer)
    AGENT_TIMEOUT_ORCHESTRATOR: int = 420  # 7 min (Orchestrator)
    
    # ============================================================
    # BUDGET MANAGER - Copilot Pro Credits (300/mes)
    # ============================================================
    BUDGET_MAX_CREDITS_PER_MONTH: int = 300  # Copilot Pro limit
    BUDGET_ALERT_THRESHOLD: float = 0.80  # Alert at 80% usage (240 credits)
    BUDGET_PROJECTED_USAGE_PER_ANALYSIS: float = 0.45  # créditos por análisis
    
    # Credit costs por modelo (según docs/03_PROJECT_SPEC.md)
    CREDIT_COST_GPT5: float = 1.0  # GPT-5
    CREDIT_COST_CLAUDE_SONNET: float = 1.0  # Claude Sonnet 4.5
    CREDIT_COST_CLAUDE_HAIKU: float = 0.33  # Claude Haiku 4.5
    CREDIT_COST_GPT4O: float = 0.0  # GPT-4o (gratis ilimitado)
    CREDIT_COST_GEMINI: float = 0.0  # Gemini 2.5 Pro (gratis)
    CREDIT_COST_DEEPSEEK: float = 0.0  # DeepSeek V3 (pago directo, no créditos)
    CREDIT_COST_MINIMAX: float = 0.0  # MiniMax-M2 (beta gratis)
    
    # ============================================================
    # CIRCUIT BREAKER - Resilience Configuration
    # ============================================================
    CIRCUIT_BREAKER_FAIL_MAX: int = 5  # Max failures before opening
    CIRCUIT_BREAKER_TIMEOUT: int = 60  # Seconds to wait before half-open
    
    # ============================================================
    # RETRY STRATEGY - Tenacity Configuration
    # ============================================================
    RETRY_MAX_ATTEMPTS: int = 3
    RETRY_WAIT_EXPONENTIAL_MULTIPLIER: int = 1  # 1, 2, 4, 8... seconds
    RETRY_WAIT_EXPONENTIAL_MAX: int = 10  # Max wait time
    
    # ============================================================
    # BLENDER CONTROL (opcional para visualización 3D)
    # ============================================================
    BLENDER_PATH: Optional[str] = None
    BLENDER_ZMQ_PORT: int = 5555
    
    # ============================================================
    # PIPELINE CONFIGURATION
    # ============================================================
    PIPELINE_MAX_CONCURRENT_AGENTS: int = 3  # Paralelización limitada
    PIPELINE_ENABLE_CACHE: bool = True
    PIPELINE_ENABLE_TELEMETRY: bool = True
    
    # ============================================================
    # DATABASE - Supabase Tables
    # ============================================================
    DB_TABLE_ANALYSIS: str = "analysis_results"
    DB_TABLE_PAPERS: str = "papers_cache"
    DB_TABLE_BUDGET: str = "budget_tracking"
    
    # ============================================================
    # OUTPUT PATHS
    # ============================================================
    OUTPUT_DIR: str = "outputs"
    OUTPUT_FORMAT: Literal["markdown", "pdf", "html"] = "markdown"
    
    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.ENV == "production"
    
    @property
    def redis_client_kwargs(self) -> dict:
        """Redis client configuration."""
        return {
            "decode_responses": True,
            "max_connections": self.REDIS_MAX_CONNECTIONS,
            "socket_connect_timeout": 5,
            "socket_keepalive": True,
        }
    
    @property
    def uptrace_config(self) -> dict:
        """Uptrace configuration for OpenTelemetry."""
        return {
            "dsn": self.UPTRACE_DSN,
            "service_name": self.UPTRACE_SERVICE_NAME,
            "service_version": self.UPTRACE_SERVICE_VERSION,
            "deployment_environment": self.ENV,
        }


# Singleton instance
settings = Settings()


# Validación al importar
def validate_critical_settings() -> None:
    """Valida que las configuraciones críticas estén presentes."""
    critical_keys = [
        "GEMINI_API_KEY",
        "DEEPSEEK_API_KEY",
        "MINIMAX_API_KEY",
        "GITHUB_PERSONAL_ACCESS_TOKEN",
        "JINA_API_KEY",
        "SUPABASE_URL",
        "SUPABASE_ANON_KEY",
        "SUPABASE_SERVICE_ROLE_KEY",
        "UPTRACE_DSN",
    ]
    
    missing = []
    for key in critical_keys:
        value = getattr(settings, key, None)
        if not value:
            missing.append(key)
    
    if missing:
        raise ValueError(
            f"❌ Missing critical settings: {', '.join(missing)}\n"
            f"📖 Ver docs/08_GETTING_STARTED.md para obtener las API keys"
        )


# Ejecutar validación al importar (solo en producción)
if settings.ENV == "production":
    validate_critical_settings()
