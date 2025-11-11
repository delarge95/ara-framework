"""
Budget Manager para GitHub Copilot Pro (300 créditos/mes).

Fuente: docs/02_PROJECT_CONSTITUTION.md (Sistema de créditos Nov 2025)
Referencia: docs/03_PROJECT_SPEC.md (Budget capacity: 100 análisis/mes)

Funcionalidades:
- Tracking de créditos consumidos (0x, 0.33x, 1x)
- Rate limiting por proveedor
- Fallback automático a modelos más baratos
- Alerting cuando se acerca al límite (80% = 240 créditos)
- Integración con Supabase para persistencia
"""
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Literal, Optional, Any
from dataclasses import dataclass, field
import structlog
from redis.asyncio import Redis

# Supabase deshabilitado temporalmente por problemas de compatibilidad con websockets 15.0.1
# TODO: Re-habilitar cuando se solucione el bug de websockets/enum en Python 3.11
SUPABASE_AVAILABLE = False
SupabaseClient = Any
create_client = None
print("WARNING: Supabase deshabilitado temporalmente")
print("INFO: Usando solo Redis para almacenamiento")

from config.settings import settings

logger = structlog.get_logger()


ModelType = Literal[
    "gpt-5",
    "gpt-4o",
    "claude-sonnet-4.5",
    "claude-haiku-4.5",
    "gemini-2.5-pro",
    "deepseek-v3",
    "minimax-m2",
]


@dataclass
class ModelCost:
    """Costo en créditos de Copilot Pro por modelo."""
    
    name: ModelType
    credits_per_request: float
    is_free: bool = False
    fallback_model: Optional[ModelType] = None
    
    # Rate limits (requests per minute)
    rpm_limit: int = 60
    
    # Características
    context_window: int = 128_000
    best_for: str = ""


# Configuración de modelos (fuente: docs/03_PROJECT_SPEC.md)
MODEL_COSTS: Dict[ModelType, ModelCost] = {
    "gpt-5": ModelCost(
        name="gpt-5",
        credits_per_request=1.0,
        fallback_model="gpt-4o",
        rpm_limit=50,
        context_window=128_000,
        best_for="reasoning, orchestration, synthesis",
    ),
    "gpt-4o": ModelCost(
        name="gpt-4o",
        credits_per_request=0.0,
        is_free=True,
        rpm_limit=100,  # Sin límite real, pero conservador
        context_window=128_000,
        best_for="fallback, simple tasks",
    ),
    "claude-sonnet-4.5": ModelCost(
        name="claude-sonnet-4.5",
        credits_per_request=1.0,
        fallback_model="claude-haiku-4.5",
        rpm_limit=50,
        context_window=200_000,
        best_for="architecture, complex reasoning",
    ),
    "claude-haiku-4.5": ModelCost(
        name="claude-haiku-4.5",
        credits_per_request=0.33,
        fallback_model="gpt-4o",
        rpm_limit=100,
        context_window=200_000,
        best_for="fast tasks, cost-sensitive",
    ),
    "gemini-2.5-pro": ModelCost(
        name="gemini-2.5-pro",
        credits_per_request=0.0,
        is_free=True,
        rpm_limit=15,  # 1500 req/día = ~15 req/min
        context_window=1_000_000,
        best_for="large context, niche analysis",
    ),
    "deepseek-v3": ModelCost(
        name="deepseek-v3",
        credits_per_request=0.0,  # Pago directo ($0.27/M), no créditos
        is_free=False,  # Pago pero no usa créditos Copilot
        rpm_limit=60,
        context_window=64_000,
        best_for="code generation, technical architecture",
    ),
    "minimax-m2": ModelCost(
        name="minimax-m2",
        credits_per_request=0.0,
        is_free=True,  # Beta gratuita
        rpm_limit=30,
        context_window=128_000,
        best_for="academic analysis, literature review",
    ),
}


@dataclass
class BudgetStatus:
    """Estado actual del presupuesto."""
    
    credits_used: float = 0.0
    credits_limit: int = 300  # Copilot Pro monthly limit
    credits_remaining: float = field(init=False)
    usage_percentage: float = field(init=False)
    
    # Contadores por modelo
    requests_by_model: Dict[ModelType, int] = field(default_factory=dict)
    
    # Alertas
    alert_triggered: bool = False
    alert_threshold: float = 0.80  # 80% = 240 credits
    
    # Timing
    period_start: datetime = field(default_factory=datetime.now)
    period_end: datetime = field(init=False)
    
    def __post_init__(self):
        self.credits_remaining = self.credits_limit - self.credits_used
        self.usage_percentage = (self.credits_used / self.credits_limit) * 100
        self.period_end = self.period_start + timedelta(days=30)
        
        if self.usage_percentage >= (self.alert_threshold * 100):
            self.alert_triggered = True
    
    def can_afford(self, model: ModelType) -> bool:
        """Verifica si hay créditos suficientes para el modelo."""
        cost = MODEL_COSTS[model].credits_per_request
        return self.credits_remaining >= cost
    
    def to_dict(self) -> dict:
        """Serializa a dict para Supabase."""
        return {
            "credits_used": self.credits_used,
            "credits_limit": self.credits_limit,
            "credits_remaining": self.credits_remaining,
            "usage_percentage": self.usage_percentage,
            "requests_by_model": self.requests_by_model,
            "alert_triggered": self.alert_triggered,
            "period_start": self.period_start.isoformat(),
            "period_end": self.period_end.isoformat(),
        }


class BudgetManager:
    """
    Gestor de presupuesto para Copilot Pro (300 créditos/mes).
    
    Responsabilidades:
    1. Track usage en tiempo real (Redis)
    2. Persist histórico en Supabase
    3. Enforce rate limits por modelo
    4. Auto-fallback a modelos más baratos
    5. Alerting cuando se acerca al límite
    
    Uso:
        budget = BudgetManager()
        
        # Verificar antes de usar modelo
        if await budget.can_use_model("gpt-5"):
            result = await agent.run()
            await budget.record_usage("gpt-5")
        else:
            fallback = await budget.get_fallback_model("gpt-5")
            result = await agent.run(model=fallback)
    """
    
    def __init__(
        self,
        redis_client: Optional[Redis] = None,
        supabase_client: Optional[Any] = None,  # Type: Client cuando disponible
        monthly_limit: float = 300.0,  # Copilot Pro monthly limit
    ):
        # Inicializar logger PRIMERO
        self.logger = logger.bind(component="budget_manager")
        
        self.redis = redis_client
        
        # Supabase es opcional - solo inicializar si está configurado
        try:
            if not SUPABASE_AVAILABLE:
                self.supabase = None
                self.logger.warning("supabase_disabled", reason="supabase library not available")
            elif supabase_client:
                self.supabase = supabase_client
            elif settings.SUPABASE_URL and settings.SUPABASE_SERVICE_ROLE_KEY and create_client:
                self.supabase = create_client(
                    settings.SUPABASE_URL,
                    settings.SUPABASE_SERVICE_ROLE_KEY
                )
            else:
                self.supabase = None
                self.logger.warning("supabase_disabled", reason="no credentials configured")
        except Exception as e:
            self.supabase = None
            self.logger.error("supabase_load_error", error=str(e))
        
        self.monthly_limit = monthly_limit
        self.models = MODEL_COSTS  # Diccionario de configuraciones de modelos
        
        # Locks para evitar race conditions
        self._locks: Dict[ModelType, asyncio.Lock] = {
            model: asyncio.Lock() for model in MODEL_COSTS.keys()
        }
    
    async def initialize(self) -> None:
        """Inicializa el budget manager."""
        # Cargar estado desde Redis o Supabase
        status = await self._load_status()
        
        if status.period_end < datetime.now():
            # Nuevo período, resetear
            await self._reset_period()
            self.logger.info("budget_period_reset", status="new_month")
        
        self.logger.info(
            "budget_manager_initialized",
            credits_used=status.credits_used,
            credits_remaining=status.credits_remaining,
            usage_percentage=f"{status.usage_percentage:.1f}%",
        )
    
    async def can_use_model(
        self,
        model: ModelType,
        required_credits: Optional[float] = None,
    ) -> bool:
        """
        Verifica si se puede usar el modelo.
        
        Args:
            model: Modelo a verificar
            required_credits: Créditos requeridos (default: cost del modelo)
        
        Returns:
            True si hay presupuesto disponible
        """
        status = await self._load_status()
        cost = required_credits or MODEL_COSTS[model].credits_per_request
        
        can_afford = status.credits_remaining >= cost
        
        if not can_afford:
            self.logger.warning(
                "insufficient_budget",
                model=model,
                required=cost,
                remaining=status.credits_remaining,
            )
        
        return can_afford
    
    async def record_usage(
        self,
        model: ModelType,
        credits_used: Optional[float] = None,
        metadata: Optional[dict] = None,
    ) -> BudgetStatus:
        """
        Registra el uso de un modelo.
        
        Args:
            model: Modelo utilizado
            credits_used: Créditos consumidos (default: cost del modelo)
            metadata: Datos adicionales (agent_name, task_id, etc.)
        
        Returns:
            Estado actualizado del presupuesto
        """
        async with self._locks[model]:
            cost = credits_used or MODEL_COSTS[model].credits_per_request
            
            # Actualizar Redis (cache rápido)
            await self._increment_usage(model, cost)
            
            # Actualizar Supabase (persistencia)
            await self._persist_usage(model, cost, metadata)
            
            # Cargar estado actualizado
            status = await self._load_status()
            
            # Log y alertas
            self.logger.info(
                "model_usage_recorded",
                model=model,
                credits=cost,
                remaining=status.credits_remaining,
                usage_pct=f"{status.usage_percentage:.1f}%",
            )
            
            if status.alert_triggered and not status.alert_triggered:
                # Primera vez que se cruza el threshold
                await self._send_alert(status)
            
            return status
    
    async def get_fallback_model(self, model: ModelType) -> ModelType:
        """
        Obtiene modelo fallback si el primario no está disponible.
        
        Estrategia:
        1. Si hay fallback configurado, usarlo
        2. Si no, buscar modelo gratis similar
        3. Último recurso: gpt-4o (gratis ilimitado)
        """
        config = MODEL_COSTS[model]
        
        # Fallback configurado
        if config.fallback_model:
            fallback = config.fallback_model
            if await self.can_use_model(fallback):
                self.logger.info(
                    "fallback_selected",
                    original=model,
                    fallback=fallback,
                )
                return fallback
        
        # Buscar modelo gratis
        for candidate_name, candidate_config in MODEL_COSTS.items():
            if candidate_config.is_free and candidate_name != model:
                self.logger.info(
                    "free_model_selected",
                    original=model,
                    fallback=candidate_name,
                )
                return candidate_name
        
        # Último recurso
        self.logger.warning("using_last_resort_fallback", original=model)
        return "gpt-4o"
    
    async def get_status(self) -> BudgetStatus:
        """Obtiene el estado actual del presupuesto."""
        return await self._load_status()
    
    async def get_remaining_credits(self) -> float:
        """
        Obtiene los créditos restantes del mes actual.
        
        Returns:
            Créditos disponibles (credits_limit - credits_used)
        """
        status = await self._load_status()
        return status.credits_remaining
    
    async def get_recommendations(self) -> dict:
        """
        Genera recomendaciones para optimizar costos.
        
        Returns:
            Dict con sugerencias basadas en usage patterns
        """
        status = await self._load_status()
        
        recommendations = []
        
        # Si uso alto, recomendar modelos gratis
        if status.usage_percentage > 60:
            recommendations.append({
                "priority": "high",
                "message": "Considerar usar más modelos gratuitos (Gemini, GPT-4o)",
                "savings": "Hasta 1 crédito por request",
            })
        
        # Si uso de Sonnet alto, recomendar Haiku
        sonnet_count = status.requests_by_model.get("claude-sonnet-4.5", 0)
        haiku_count = status.requests_by_model.get("claude-haiku-4.5", 0)
        
        if sonnet_count > haiku_count * 2:
            recommendations.append({
                "priority": "medium",
                "message": "Usar Claude Haiku (0.33x) en vez de Sonnet (1x) para tareas simples",
                "savings": "0.67 créditos por request",
            })
        
        # Si quedan pocos créditos
        if status.credits_remaining < 50:
            recommendations.append({
                "priority": "critical",
                "message": f"Solo {status.credits_remaining:.0f} créditos restantes. Usar solo modelos gratuitos.",
                "savings": "Preservar para tareas críticas",
            })
        
        return {
            "status": status.to_dict(),
            "recommendations": recommendations,
            "projected_end_of_month_usage": self._project_usage(status),
        }
    
    # ============================================================
    # MÉTODOS PRIVADOS
    # ============================================================
    
    async def _load_status(self) -> BudgetStatus:
        """Carga estado desde Redis (cache) o Supabase (source of truth)."""
        # Intentar Redis primero
        if self.redis:
            cached = await self._load_from_redis()
            if cached:
                return cached
        
        # Cargar desde Supabase
        return await self._load_from_supabase()
    
    async def _load_from_redis(self) -> Optional[BudgetStatus]:
        """Carga estado desde Redis."""
        if not self.redis:
            return None
        
        try:
            data = await self.redis.hgetall("budget:current")
            
            if not data:
                return None
            
            return BudgetStatus(
                credits_used=float(data.get("credits_used", 0)),
                credits_limit=int(data.get("credits_limit", 300)),
                requests_by_model=eval(data.get("requests_by_model", "{}")),
                period_start=datetime.fromisoformat(
                    data.get("period_start", datetime.now().isoformat())
                ),
            )
        except Exception as e:
            self.logger.error("redis_load_error", error=str(e))
            return None
    
    async def _load_from_supabase(self) -> BudgetStatus:
        """Carga estado desde Supabase."""
        if not self.supabase:
            # Si Supabase no está disponible, retornar estado inicial
            now = datetime.now()
            period_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            return BudgetStatus(period_start=period_start)
        
        try:
            # Query del período actual
            now = datetime.now()
            period_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            
            response = self.supabase.table(settings.DB_TABLE_BUDGET).select("*").gte(
                "period_start", period_start.isoformat()
            ).order("created_at", desc=True).limit(1).execute()
            
            if response.data:
                data = response.data[0]
                return BudgetStatus(
                    credits_used=data["credits_used"],
                    credits_limit=data["credits_limit"],
                    requests_by_model=data["requests_by_model"],
                    period_start=datetime.fromisoformat(data["period_start"]),
                )
            else:
                # Primer uso del mes
                return BudgetStatus(period_start=period_start)
        
        except Exception as e:
            self.logger.error("supabase_load_error", error=str(e))
            # Fallback to default
            return BudgetStatus()
    
    async def _increment_usage(self, model: ModelType, credits: float) -> None:
        """Incrementa el uso en Redis."""
        if not self.redis:
            return
        
        try:
            # Incrementar créditos totales
            await self.redis.hincrbyfloat("budget:current", "credits_used", credits)
            
            # Incrementar contador del modelo
            await self.redis.hincrby(
                "budget:current",
                f"model:{model}",
                1
            )
            
            # Set expiry (30 días)
            await self.redis.expire("budget:current", 30 * 24 * 60 * 60)
        
        except Exception as e:
            self.logger.error("redis_increment_error", error=str(e))
    
    async def _persist_usage(
        self,
        model: ModelType,
        credits: float,
        metadata: Optional[dict],
    ) -> None:
        """Persiste el uso en Supabase."""
        if not self.supabase:
            # Si Supabase no está disponible, simplemente retornar
            return
        
        try:
            data = {
                "model": model,
                "credits_used": credits,
                "timestamp": datetime.now().isoformat(),
                "metadata": metadata or {},
            }
            
            self.supabase.table("usage_log").insert(data).execute()
        
        except Exception as e:
            self.logger.error("supabase_persist_error", error=str(e))
    
    async def _reset_period(self) -> None:
        """Resetea el presupuesto para un nuevo período."""
        if self.redis:
            await self.redis.delete("budget:current")
        
        # Crear nuevo registro en Supabase solo si está disponible
        if not self.supabase:
            return
        
        now = datetime.now()
        period_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        data = {
            "period_start": period_start.isoformat(),
            "period_end": (period_start + timedelta(days=30)).isoformat(),
            "credits_used": 0.0,
            "credits_limit": settings.BUDGET_MAX_CREDITS_PER_MONTH,
            "requests_by_model": {},
        }
        
        self.supabase.table(settings.DB_TABLE_BUDGET).insert(data).execute()
    
    async def _send_alert(self, status: BudgetStatus) -> None:
        """Envía alerta cuando se cruza el threshold."""
        self.logger.warning(
            "budget_alert_triggered",
            usage_pct=f"{status.usage_percentage:.1f}%",
            credits_remaining=status.credits_remaining,
            alert_threshold=f"{status.alert_threshold * 100:.0f}%",
        )
        
        # TODO: Integrar con sistema de notificaciones
        # (Email, Slack, Discord, etc.)
    
    def _project_usage(self, status: BudgetStatus) -> dict:
        """Proyecta el uso al final del mes basado en el patrón actual."""
        days_elapsed = (datetime.now() - status.period_start).days
        days_remaining = 30 - days_elapsed
        
        if days_elapsed == 0:
            return {"projected_credits": 0, "will_exceed": False}
        
        daily_rate = status.credits_used / days_elapsed
        projected_total = status.credits_used + (daily_rate * days_remaining)
        
        return {
            "daily_rate": round(daily_rate, 2),
            "projected_total": round(projected_total, 2),
            "will_exceed": projected_total > status.credits_limit,
            "days_until_limit": int(status.credits_remaining / daily_rate) if daily_rate > 0 else 999,
        }


# Singleton instance
_budget_manager: Optional[BudgetManager] = None


async def get_budget_manager() -> BudgetManager:
    """Factory function para obtener el budget manager singleton."""
    global _budget_manager
    
    if _budget_manager is None:
        from redis.asyncio import from_url
        
        redis_client = await from_url(
            settings.REDIS_URL,
            **settings.redis_client_kwargs
        )
        
        _budget_manager = BudgetManager(redis_client=redis_client)
        await _budget_manager.initialize()
    
    return _budget_manager
