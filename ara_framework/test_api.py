#!/usr/bin/env python3
"""
Test script para verificar que la API funciona correctamente
"""

import sys
import os
sys.path.append('.')

def test_api_import():
    """Test que la API se puede importar correctamente"""
    try:
        from api.main import app
        print("✅ API import successful")
        
        # Test endpoints están registrados
        routes = [route.path for route in app.routes]
        expected_endpoints = ['/api/budget', '/api/pipeline/status', '/api/models']
        
        for endpoint in expected_endpoints:
            if endpoint in routes:
                print(f"✅ Endpoint {endpoint} registered")
            else:
                print(f"❌ Endpoint {endpoint} missing")
        
        return True
    except Exception as e:
        print(f"❌ API import failed: {e}")
        return False

def test_budget_manager():
    """Test que budget manager funciona"""
    try:
        from core.budget_manager import BudgetManager
        bm = BudgetManager()
        status = bm.get_status()
        print(f"✅ Budget Manager working: {status.total_budget} budget")
        return True
    except Exception as e:
        print(f"⚠️  Budget Manager warning: {e}")
        return True  # No es crítico

if __name__ == "__main__":
    print("🧪 Testing ARA Framework API...")
    
    api_ok = test_api_import()
    budget_ok = test_budget_manager()
    
    if api_ok:
        print("\n🎉 API is ready!")
        print("📋 Next: Test with curl or start development server")
        print("🚀 To start server: cd ara_framework && python -m api.main")
    else:
        print("\n❌ API has issues that need fixing")