"""
Pipeline Management API Routes

Endpoints para gestión del pipeline que conectan con el frontend
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from datetime import datetime
import asyncio
import sys
import os

# Agregar path para imports del core
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

try:
    from core.pipeline import AnalysisPipeline
    from core.budget_manager import BudgetManager
except ImportError:
    AnalysisPipeline = None
    BudgetManager = None

router = APIRouter()

# Pydantic models
class PipelineRequest(BaseModel):
    niche: str
    priority: str = "normal"  # "low", "normal", "high"
    budget_limit: Optional[float] = None

class PipelineStatus(BaseModel):
    status: str  # "idle", "running", "completed", "failed"
    current_phase: Optional[str] = None
    progress_percentage: float = 0.0
    estimated_time_remaining: Optional[int] = None  # minutes
    niche: Optional[str] = None
    started_at: Optional[str] = None
    updated_at: str

class PipelineResult(BaseModel):
    id: str
    niche: str
    status: str
    final_report: Optional[str] = None
    metadata: Dict[str, Any]
    created_at: str
    completed_at: Optional[str] = None
    cost: float = 0.0
    tokens_used: int = 0

# Global state para tracking (en producción usaríamos Redis)
pipeline_state = {
    "status": "idle",
    "current_phase": None,
    "progress": 0.0,
    "niche": None,
    "started_at": None
}

active_pipelines = {}  # job_id -> pipeline_data

@router.get("/pipeline/status", response_model=PipelineStatus)
async def get_pipeline_status():
    """
    Obtener estado actual del pipeline
    
    Usado por el dashboard para mostrar progreso en tiempo real
    """
    return PipelineStatus(
        status=pipeline_state["status"],
        current_phase=pipeline_state["current_phase"],
        progress_percentage=pipeline_state["progress"],
        niche=pipeline_state["niche"],
        started_at=pipeline_state["started_at"],
        updated_at=datetime.now().isoformat()
    )

@router.post("/pipeline/run")
async def run_pipeline(
    request: PipelineRequest,
    background_tasks: BackgroundTasks
):
    """
    Iniciar análisis del pipeline
    
    Ejecuta el pipeline en background y retorna job_id para tracking
    """
    if pipeline_state["status"] == "running":
        raise HTTPException(
            status_code=409, 
            detail="Pipeline is already running. Only one analysis at a time."
        )
    
    # Generar job ID
    job_id = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Actualizar estado
    pipeline_state.update({
        "status": "running",
        "current_phase": "initialization",
        "progress": 0.0,
        "niche": request.niche,
        "started_at": datetime.now().isoformat()
    })
    
    # Agregar job a tracking
    active_pipelines[job_id] = {
        "niche": request.niche,
        "status": "running",
        "created_at": datetime.now().isoformat(),
        "progress": 0.0
    }
    
    # Ejecutar pipeline en background
    background_tasks.add_task(execute_pipeline_task, job_id, request)
    
    return {
        "message": "Pipeline started successfully",
        "job_id": job_id,
        "niche": request.niche,
        "estimated_duration": "45-60 minutes",
        "status_url": f"/api/pipeline/jobs/{job_id}"
    }

@router.get("/pipeline/jobs/{job_id}")
async def get_pipeline_job(job_id: str):
    """
    Obtener estado de un job específico
    """
    if job_id not in active_pipelines:
        raise HTTPException(status_code=404, detail="Pipeline job not found")
    
    return active_pipelines[job_id]

@router.delete("/pipeline/jobs/{job_id}")
async def cancel_pipeline_job(job_id: str):
    """
    Cancelar un job del pipeline
    """
    if job_id not in active_pipelines:
        raise HTTPException(status_code=404, detail="Pipeline job not found")
    
    # Marcar como cancelado
    active_pipelines[job_id]["status"] = "cancelled"
    
    # Actualizar estado global si es el job activo
    if pipeline_state["status"] == "running":
        pipeline_state.update({
            "status": "idle",
            "current_phase": None,
            "progress": 0.0,
            "niche": None,
            "started_at": None
        })
    
    return {"message": f"Pipeline job {job_id} cancelled successfully"}

@router.get("/pipeline/history")
async def get_pipeline_history():
    """
    Obtener historial de análisis completados
    """
    # Mock data por ahora
    return {
        "results": [
            {
                "id": "analysis_20251219_120000",
                "niche": "Rust WebAssembly for audio processing",
                "status": "completed",
                "created_at": "2025-12-19T12:00:00Z",
                "completed_at": "2025-12-19T13:45:00Z",
                "cost": 3.47,
                "tokens_used": 23500
            },
            {
                "id": "analysis_20251218_150000",
                "niche": "Quantum ML for drug discovery",
                "status": "completed", 
                "created_at": "2025-12-18T15:00:00Z",
                "completed_at": "2025-12-18T16:30:00Z",
                "cost": 4.12,
                "tokens_used": 28900
            }
        ],
        "total_analyses": 2,
        "avg_cost": 3.80,
        "avg_duration_minutes": 95
    }

@router.get("/models")
async def get_available_models():
    """
    Obtener lista de modelos disponibles
    
    Usado por ModelSelector.tsx
    """
    return {
        "models": [
            {
                "id": "gpt-4o", 
                "name": "GPT-4 Omni",
                "provider": "OpenAI",
                "cost_per_1m_tokens": 15.0,
                "context_window": 128000,
                "status": "available"
            },
            {
                "id": "claude-3-5-sonnet",
                "name": "Claude 3.5 Sonnet", 
                "provider": "Anthropic",
                "cost_per_1m_tokens": 15.0,
                "context_window": 200000,
                "status": "available"
            },
            {
                "id": "grok-beta",
                "name": "Grok Beta",
                "provider": "xAI", 
                "cost_per_1m_tokens": 5.0,
                "context_window": 131072,
                "status": "available"
            }
        ],
        "default_model": "gpt-4o",
        "total_models": 3
    }

async def execute_pipeline_task(job_id: str, request: PipelineRequest):
    """
    Ejecutar pipeline en background
    
    Simula ejecución del pipeline actual y actualiza el estado
    """
    try:
        phases = [
            ("initialization", 5),
            ("niche_analysis", 20),
            ("literature_research", 35), 
            ("technical_architecture", 55),
            ("implementation_planning", 75),
            ("content_synthesis", 90),
            ("finalization", 100)
        ]
        
        for phase_name, progress in phases:
            # Actualizar estado global
            pipeline_state.update({
                "current_phase": phase_name,
                "progress": progress
            })
            
            # Actualizar job específico
            active_pipelines[job_id].update({
                "status": "running",
                "progress": progress,
                "current_phase": phase_name
            })
            
            # Simular trabajo (en producción sería el pipeline real)
            await asyncio.sleep(2)
            
            # Check si fue cancelado
            if active_pipelines[job_id]["status"] == "cancelled":
                return
        
        # Completar pipeline
        pipeline_state.update({
            "status": "completed",
            "current_phase": "completed",
            "progress": 100.0
        })
        
        active_pipelines[job_id].update({
            "status": "completed",
            "progress": 100.0,
            "completed_at": datetime.now().isoformat(),
            "final_report": "# Analysis Complete\n\nDetailed analysis report would go here...",
            "cost": 3.47,
            "tokens_used": 23500
        })
        
        # Después de 5 segundos, resetear estado para siguiente job
        await asyncio.sleep(5)
        pipeline_state.update({
            "status": "idle",
            "current_phase": None,
            "progress": 0.0,
            "niche": None,
            "started_at": None
        })
        
    except Exception as e:
        # Marcar como fallido
        pipeline_state.update({
            "status": "failed",
            "current_phase": "error"
        })
        
        active_pipelines[job_id].update({
            "status": "failed",
            "error": str(e)
        })