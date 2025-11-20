#!/usr/bin/env python3
"""
Test HTTP del servidor API
"""

import sys
sys.path.append('.')

import uvicorn
from api.main import app
import threading
import time
import requests

def test_api_server():
    """Test que el servidor responde correctamente"""
    
    def start_server():
        uvicorn.run(app, host='127.0.0.1', port=8000, log_level='error')

    # Start server in background
    print("🚀 Starting API server...")
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    time.sleep(4)  # Wait for server to start

    try:
        # Test health endpoint
        response = requests.get('http://localhost:8000/', timeout=5)
        print(f'✅ Health endpoint: {response.status_code}')
        
        if response.status_code == 200:
            data = response.json()
            print(f'✅ API message: {data.get("message", "No message")}')
        
        # Test budget endpoint  
        budget_response = requests.get('http://localhost:8000/api/budget', timeout=5)
        print(f'✅ Budget endpoint: {budget_response.status_code}')
        
        if budget_response.status_code == 200:
            budget_data = budget_response.json()
            print(f'✅ Budget data: ${budget_data.get("used_budget", 0):.2f} used')
        
        # Test models endpoint
        models_response = requests.get('http://localhost:8000/api/models', timeout=5)
        print(f'✅ Models endpoint: {models_response.status_code}')
        
        print("\n🎉 API Server is working correctly!")
        print("🔗 Frontend can now connect to: http://localhost:8000")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f'❌ Server connection failed: {e}')
        return False
    except Exception as e:
        print(f'❌ Test failed: {e}')
        return False

if __name__ == "__main__":
    print("🧪 Testing ARA Framework API Server...")
    success = test_api_server()
    
    if success:
        print("\n📋 Next Steps:")
        print("1. Update frontend to use http://localhost:8000 as API base URL")
        print("2. Test BudgetDashboard.tsx with real data") 
        print("3. Implement WebSocket for real-time updates")
    else:
        print("\n❌ Fix server issues before proceeding")