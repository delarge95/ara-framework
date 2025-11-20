"""
ARA Framework FastAPI Main Application

API backend que conecta el frontend React existente con el core del framework.
Proporciona endpoints REST y WebSocket para comunicación en tiempo real.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import sys
import os

# Agregar el directorio padre al path para imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from api.routes import budget, pipeline
from core.budget_manager import BudgetManager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup: Initialize services
    print("🚀 ARA Framework API starting...")
    
    # Initialize budget manager
    try:
        budget_manager = BudgetManager()
        app.state.budget_manager = budget_manager
        print("✅ Budget Manager initialized")
    except Exception as e:
        print(f"⚠️ Budget Manager warning: {e}")
        app.state.budget_manager = None
    
    print("🎯 ARA Framework API ready!")
    yield
    
    # Shutdown: Cleanup
    print("🛑 ARA Framework API shutting down...")


# Create FastAPI app
app = FastAPI(
    title="ARA Framework API",
    description="Backend API for ARA Framework - Connects React frontend with LangGraph pipeline",
    version="0.1.0",
    lifespan=lifespan
)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # React dev server alternative
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "ARA Framework API is running",
        "version": "0.1.0",
        "status": "healthy",
        "endpoints": {
            "budget": "/api/budget",
            "pipeline": "/api/pipeline", 
            "models": "/api/models",
            "metrics": "/api/metrics",
            "websocket": "/ws"
        }
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "budget_manager": app.state.budget_manager is not None,
        "api_version": "0.1.0"
    }

# Include routers
app.include_router(budget.router, prefix="/api", tags=["budget"])
app.include_router(pipeline.router, prefix="/api", tags=["pipeline"])

if __name__ == "__main__":
    # Para desarrollo local
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=9090, 
        reload=False,  # Direct app object, no reload needed
        log_level="info"
    )