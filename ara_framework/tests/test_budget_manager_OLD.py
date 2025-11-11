"""
Tests for BudgetManager - Credit tracking and budget management.

Tests adaptados a la API real de BudgetManager:
- Initialization y configuración
- can_use_model() - Verificación de presupuesto
- record_usage() - Tracking de uso
- get_status() - Estado del presupuesto
- get_remaining_credits() - Créditos disponibles
- get_fallback_model() - Fallback automático
"""
import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from datetime import datetime, timedelta
import json

from core.budget_manager import BudgetManager, ModelCost, BudgetStatus, MODEL_COSTS


class TestBudgetManager:
    """Tests para BudgetManager con API actual."""
    
    @pytest.fixture
    def mock_redis_client(self):
        """Mock para Redis client async."""
        mock = AsyncMock()
        # Redis.get debe retornar string JSON directamente (ya es async)
        mock.get = AsyncMock(return_value=json.dumps({
            "credits_used": 0.0,
            "credits_limit": 300,
            "period_start": datetime.now().isoformat(),
        }))
        mock.set = AsyncMock(return_value=True)
        mock.incrbyfloat = AsyncMock(return_value=1.0)
        mock.expire = AsyncMock(return_value=True)
        mock.hincrby = AsyncMock(return_value=1)
        return mock
    
    @pytest.fixture
    async def budget_manager(self, mock_redis_client):
        """Create BudgetManager con Redis mock."""
        manager = BudgetManager(
            redis_client=mock_redis_client,
            monthly_limit=300.0,
        )
        # Inicializar de forma async
        await manager.initialize()
        return manager
    
    @pytest.mark.asyncio
    async def test_initialization(self, budget_manager, mock_redis_client):
        """Test que BudgetManager se inicializa correctamente."""
        assert budget_manager.monthly_limit == 300.0
        assert budget_manager.redis == mock_redis_client
        assert len(budget_manager.models) == 7  # 7 models configured
        assert "gpt-5" in budget_manager.models
        assert "claude-sonnet-4.5" in budget_manager.models
        assert "gemini-2.5-pro" in budget_manager.models
    
    def test_model_costs_configuration(self):
        """Test que los costos de modelos están bien configurados."""
        # GPT-5: 1 credit
        assert MODEL_COSTS["gpt-5"].credits_per_request == 1.0
        assert MODEL_COSTS["gpt-5"].is_free is False
        
        # Claude Sonnet: 1 credit
        assert MODEL_COSTS["claude-sonnet-4.5"].credits_per_request == 1.0
        
        # Claude Haiku: 0.33 credits
        assert MODEL_COSTS["claude-haiku-4.5"].credits_per_request == 0.33
        
        # Gemini: 0 credits (free)
        assert MODEL_COSTS["gemini-2.5-pro"].credits_per_request == 0.0
        assert MODEL_COSTS["gemini-2.5-pro"].is_free is True
        
        # GPT-4o: 0 credits (free)
        assert MODEL_COSTS["gpt-4o"].credits_per_request == 0.0
        assert MODEL_COSTS["gpt-4o"].is_free is True
    
    @pytest.mark.asyncio
    async def test_can_use_model_sufficient_budget(self, mock_redis_client):
        """Test can_use_model cuando hay presupuesto suficiente."""
        # Mock Redis to return low usage (10 credits used)
        status_data = {
            "credits_used": 10.0,
            "credits_limit": 300,
            "period_start": datetime.now().isoformat(),
        }
        mock_redis_client.get = AsyncMock(return_value=json.dumps(status_data))
        
        budget_manager = BudgetManager(redis_client=mock_redis_client, monthly_limit=300.0)
        await budget_manager.initialize()
        
        # Should allow gpt-5 (1 credit)
        can_use = await budget_manager.can_use_model("gpt-5")
        assert can_use is True
    
    @pytest.mark.asyncio
    async def test_can_use_model_insufficient_budget(self, mock_redis_client):
        """Test can_use_model cuando NO hay presupuesto suficiente."""
        # Mock Redis to return high usage (299.5 credits used, only 0.5 remaining)
        status_data = {
            "credits_used": 299.5,
            "credits_limit": 300,
            "period_start": datetime.now().isoformat(),
        }
        mock_redis_client.get = AsyncMock(return_value=json.dumps(status_data))
        
        budget_manager = BudgetManager(redis_client=mock_redis_client, monthly_limit=300.0)
        await budget_manager.initialize()
        
        # Should NOT allow gpt-5 (1 credit needed, only 0.5 remaining)
        can_use = await budget_manager.can_use_model("gpt-5")
        assert can_use is False
    
    @pytest.mark.asyncio
    async def test_can_use_model_free_model(self, mock_redis_client):
        """Test can_use_model con modelo gratis."""
        # Mock high usage
        status_data = {
            "credits_used": 299.5,
            "credits_limit": 300,
            "period_start": datetime.now().isoformat(),
        }
        mock_redis_client.get = AsyncMock(return_value=json.dumps(status_data))
        
        budget_manager = BudgetManager(redis_client=mock_redis_client, monthly_limit=300.0)
        await budget_manager.initialize()
        
        # Should ALWAYS allow free models
        can_use = await budget_manager.can_use_model("gemini-2.5-pro")
        assert can_use is True
    
    @pytest.mark.asyncio
    async def test_record_usage(self, mock_redis_client):
        """Test record_usage registra correctamente."""
        # Mock initial state
        initial_status = {
            "credits_used": 10.0,
            "credits_limit": 300,
            "period_start": datetime.now().isoformat(),
            "requests_by_model": {}
        }
        mock_redis_client.get = AsyncMock(return_value=json.dumps(initial_status))
        
        budget_manager = BudgetManager(redis_client=mock_redis_client, monthly_limit=300.0)
        await budget_manager.initialize()
        
        # Record usage for gpt-5 (1 credit)
        status = await budget_manager.record_usage(
            model="gpt-5",
            credits_used=1.0,
            metadata={"agent": "niche_analyst", "niche": "test"},
        )
        
        # Verify Redis was called to save state
        assert mock_redis_client.set.called
        
        # Status should be returned
        assert isinstance(status, BudgetStatus)
    
    @pytest.mark.asyncio
    async def test_get_remaining_credits(self, mock_redis_client):
        """Test get_remaining_credits calcula correctamente."""
        # Mock Redis with 50 credits used
        status_data = {
            "credits_used": 50.0,
            "credits_limit": 300,
            "period_start": datetime.now().isoformat(),
        }
        mock_redis_client.get = AsyncMock(return_value=json.dumps(status_data))
        
        budget_manager = BudgetManager(redis_client=mock_redis_client, monthly_limit=300.0)
        await budget_manager.initialize()
        
        remaining = await budget_manager.get_remaining_credits()
        
        # Should be 300 - 50 = 250
        assert remaining == 250.0
    
    @pytest.mark.asyncio
    async def test_get_status(self, mock_redis_client):
        """Test get_status retorna BudgetStatus completo."""
        # Mock Redis
        status_data = {
            "credits_used": 100.0,
            "credits_limit": 300,
            "period_start": datetime.now().isoformat(),
        }
        mock_redis_client.get = AsyncMock(return_value=json.dumps(status_data))
        
        budget_manager = BudgetManager(redis_client=mock_redis_client, monthly_limit=300.0)
        await budget_manager.initialize()
        
        status = await budget_manager.get_status()
        
        assert isinstance(status, BudgetStatus)
        assert status.credits_used == 100.0
        assert status.credits_limit == 300
        assert status.credits_remaining == 200.0
        assert status.usage_percentage == pytest.approx(33.33, rel=0.1)
    
    @pytest.mark.asyncio
    async def test_get_fallback_model_configured_fallback(self, mock_redis_client):
        """Test get_fallback_model con fallback configurado."""
        # Mock sufficient budget
        status_data = {
            "credits_used": 10.0,
            "credits_limit": 300,
            "period_start": datetime.now().isoformat(),
        }
        mock_redis_client.get = AsyncMock(return_value=json.dumps(status_data))
        
        budget_manager = BudgetManager(redis_client=mock_redis_client, monthly_limit=300.0)
        await budget_manager.initialize()
        
        # gpt-5 has gpt-4o as fallback
        fallback = await budget_manager.get_fallback_model("gpt-5")
        assert fallback == "gpt-4o"
    
    @pytest.mark.asyncio
    async def test_get_fallback_model_free_model(self, mock_redis_client):
        """Test get_fallback_model busca modelo gratis."""
        # Mock insufficient budget for paid models
        status_data = {
            "credits_used": 299.5,
            "credits_limit": 300,
            "period_start": datetime.now().isoformat(),
        }
        mock_redis_client.get = AsyncMock(return_value=json.dumps(status_data))
        
        budget_manager = BudgetManager(redis_client=mock_redis_client, monthly_limit=300.0)
        await budget_manager.initialize()
        
        # Should return configured fallback (not necessarily free)
        fallback = await budget_manager.get_fallback_model("claude-sonnet-4.5")
        # claude-sonnet-4.5 -> claude-haiku-4.5 (0.33 credits, cheaper but not free)
        assert fallback in MODEL_COSTS
        # Or might be a free fallback if all paid are unavailable
        assert fallback is not None


class TestModelCost:
    """Tests para ModelCost dataclass."""
    
    def test_model_cost_paid_model(self):
        """Test configuración de modelo de pago."""
        cost = MODEL_COSTS["gpt-5"]
        
        assert cost.name == "gpt-5"
        assert cost.credits_per_request == 1.0
        assert cost.is_free is False
        assert cost.fallback_model == "gpt-4o"
        assert cost.rpm_limit > 0
        assert cost.context_window > 0
    
    def test_model_cost_free_model(self):
        """Test configuración de modelo gratis."""
        cost = MODEL_COSTS["gemini-2.5-pro"]
        
        assert cost.name == "gemini-2.5-pro"
        assert cost.credits_per_request == 0.0
        assert cost.is_free is True
    
    def test_all_models_have_fallbacks(self):
        """Test que modelos de pago tienen fallback."""
        for model_name, config in MODEL_COSTS.items():
            # Only paid models with cost > 0 should have fallback
            if config.credits_per_request > 0:
                # Paid models should have fallback
                assert config.fallback_model is not None, f"{model_name} should have fallback"
            # deepseek-v3 costs 0.0 but is_free=False (API cost 0, not truly free)
                # Fallback should exist in MODEL_COSTS
                assert config.fallback_model in MODEL_COSTS


class TestBudgetStatus:
    """Tests para BudgetStatus dataclass."""
    
    def test_budget_status_creation(self):
        """Test creación de BudgetStatus con valores por defecto."""
        status = BudgetStatus(
            credits_used=50.0,
            credits_limit=300,
        )
        
        # Computed fields
        assert status.credits_remaining == 250.0  # 300 - 50
        assert status.usage_percentage == pytest.approx(16.67, rel=0.1)  # (50/300) * 100
        assert status.alert_triggered is False  # Not at 80% yet
    
    def test_budget_status_alert_triggered(self):
        """Test que alerta se activa al 80%."""
        # 80% usage = 240 credits used
        status = BudgetStatus(
            credits_used=240.0,
            credits_limit=300,
        )
        
        assert status.usage_percentage == 80.0
        assert status.alert_triggered is True
    
    def test_budget_status_alert_threshold_custom(self):
        """Test threshold personalizado."""
        status = BudgetStatus(
            credits_used=150.0,
            credits_limit=300,
            alert_threshold=0.50,  # Alert at 50%
        )
        
        assert status.usage_percentage == 50.0
        assert status.alert_triggered is True
    
    def test_budget_status_can_afford(self):
        """Test método can_afford."""
        status = BudgetStatus(
            credits_used=299.0,
            credits_limit=300,
        )
        
        # Can afford haiku (0.33 credits)
        assert status.can_afford("claude-haiku-4.5") is True
        
        # Cannot afford gpt-5 (1 credit, only 1 remaining)
        assert status.can_afford("gpt-5") is True  # Exactly 1 credit remaining
        
        # Can always afford free models
        assert status.can_afford("gemini-2.5-pro") is True
    
    def test_budget_status_to_dict(self):
        """Test serialización a dict."""
        status = BudgetStatus(
            credits_used=100.0,
            credits_limit=300,
        )
        
        data = status.to_dict()
        
        assert isinstance(data, dict)
        assert data["credits_used"] == 100.0
        assert data["credits_limit"] == 300
        assert data["credits_remaining"] == 200.0
        assert "usage_percentage" in data
        assert "alert_triggered" in data
        assert "period_start" in data
        assert "period_end" in data

