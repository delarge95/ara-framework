"""
Budget Management API Routes

Endpoints para gestión de presupuesto que conectan con BudgetDashboard.tsx
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from typing import Dict, Any, Optional
import sys
import os

# Agregar path para imports del core
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

try:
    from core.budget_manager import BudgetManager
except ImportError:
    BudgetManager = None

router = APIRouter()

# Pydantic models para responses
class BudgetStatus(BaseModel):
    total_budget: float
    used_budget: float
    remaining_budget: float
    percentage_used: float
    credit_limit: Optional[float] = None
    status: str  # "healthy", "warning", "critical"

class BudgetUpdate(BaseModel):
    amount: float
    description: str
    category: str

class TokenUsage(BaseModel):
    model_name: str
    tokens_used: int
    cost_usd: float
    timestamp: str

def get_budget_manager(request: Request) -> Optional[BudgetManager]:
    """Dependency para obtener budget manager de app state"""
    return getattr(request.app.state, 'budget_manager', None)

@router.get("/", response_model=BudgetStatus)
async def get_budget_status():
    """
    Obtener estado actual del presupuesto
    
    Usado por BudgetDashboard.tsx para mostrar métricas en tiempo real
    
    TODO: Conectar con BudgetManager real una vez que se configure Redis/Supabase
    """
    # Por ahora usar datos mock realistas hasta configurar database
    return BudgetStatus(
        total_budget=300.0,  # Copilot Pro monthly limit
        used_budget=85.50,   # Uso actual simulado
        remaining_budget=214.50,
        percentage_used=28.5,
        credit_limit=300.0,
        status="healthy"
    )

@router.post("/track")
async def track_expense(
    expense: BudgetUpdate,
    budget_manager: Optional[BudgetManager] = Depends(get_budget_manager)
):
    """
    Registrar un gasto
    
    Usado cuando el pipeline consume tokens o recursos
    """
    if not budget_manager:
        return {"message": "Budget tracking disabled (no manager available)"}
    
    try:
        # Track expense with budget manager
        budget_manager.track_expense(
            amount=expense.amount,
            description=expense.description,
            category=expense.category
        )
        
        return {
            "message": "Expense tracked successfully",
            "amount": expense.amount,
            "category": expense.category
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error tracking expense: {str(e)}")

@router.get("/usage")
async def get_token_usage():
    """
    Obtener histórico de uso de tokens
    
    Datos para charts en el frontend
    """
    # Mock data por ahora - luego conectar con métricas reales
    return {
        "daily_usage": [
            {"date": "2025-12-19", "tokens": 15420, "cost": 0.23},
            {"date": "2025-12-18", "tokens": 12800, "cost": 0.19},
            {"date": "2025-12-17", "tokens": 18900, "cost": 0.28},
        ],
        "by_model": [
            {"model": "gpt-4o", "tokens": 8500, "cost": 0.15},
            {"model": "claude-3.5-sonnet", "tokens": 6920, "cost": 0.08},
        ],
        "total_today": {
            "tokens": 15420,
            "cost": 0.23,
            "calls": 47
        }
    }

@router.post("/emergency-stop")
async def emergency_stop(
    budget_manager: Optional[BudgetManager] = Depends(get_budget_manager)
):
    """
    Activar parada de emergencia del presupuesto
    
    Usado por el botón de emergencia en BudgetDashboard.tsx
    """
    if not budget_manager:
        return {"message": "Emergency stop disabled (no manager available)"}
    
    try:
        budget_manager.emergency_stop()
        return {
            "message": "Emergency stop activated",
            "status": "stopped",
            "timestamp": "2025-12-19T18:30:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error activating emergency stop: {str(e)}")

@router.delete("/emergency-stop")
async def deactivate_emergency_stop(
    budget_manager: Optional[BudgetManager] = Depends(get_budget_manager)
):
    """
    Desactivar parada de emergencia del presupuesto
    """
    if not budget_manager:
        return {"message": "Emergency stop disabled (no manager available)"}
    
    try:
        # Suponiendo que existe este método
        if hasattr(budget_manager, 'deactivate_emergency_stop'):
            budget_manager.deactivate_emergency_stop()
        
        return {
            "message": "Emergency stop deactivated", 
            "status": "active",
            "timestamp": "2025-12-19T18:35:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deactivating emergency stop: {str(e)}")