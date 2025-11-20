"""
Test rápido de GitHub Models integrado en los agentes
"""
import asyncio
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from config.settings import settings

load_dotenv()

async def test_github_models_agent():
    """Test básico de ChatOpenAI con GitHub Models"""
    
    print("="*70)
    print("🧪 TEST DE GITHUB MODELS EN AGENTES")
    print("="*70)
    print()
    
    # Verificar configuración
    if not settings.GITHUB_TOKEN:
        print("❌ ERROR: GITHUB_TOKEN no configurado en .env")
        return
    
    print(f"✅ GitHub Token: {settings.GITHUB_TOKEN[:8]}...{settings.GITHUB_TOKEN[-4:]}")
    print(f"✅ GitHub Model: {settings.GITHUB_MODEL}")
    print(f"✅ Base URL: {settings.GITHUB_MODELS_BASE_URL}")
    print()
    
    # Crear LLM
    print("🔄 Inicializando ChatOpenAI con GitHub Models...")
    llm = ChatOpenAI(
        model=settings.GITHUB_MODEL,
        temperature=0.7,
        api_key=settings.GITHUB_TOKEN,
        base_url=settings.GITHUB_MODELS_BASE_URL,
    )
    
    # Test simple
    print("🔄 Probando respuesta del modelo...")
    try:
        response = await llm.ainvoke("Di 'OK' si puedes leerme y estás listo para trabajar en un framework de investigación académica.")
        print(f"✅ Respuesta del modelo: {response.content}")
        print()
        
        # Test con contexto más complejo (similar a los agentes)
        print("🔄 Probando análisis de nicho simulado...")
        complex_prompt = """Eres un agente experto en análisis de nichos de investigación.

NICHE: "WebAssembly para procesamiento de audio en tiempo real en navegadores"

Analiza brevemente (en 2-3 frases):
1. Viabilidad del nicho
2. Principales desafíos
3. Una oportunidad de investigación"""

        response2 = await llm.ainvoke(complex_prompt)
        print("✅ Análisis generado:")
        print("-" * 70)
        print(response2.content)
        print("-" * 70)
        print()
        
        print("="*70)
        print("🎉 ÉXITO: GitHub Models está funcionando correctamente")
        print("="*70)
        print()
        print("📊 Próximos pasos:")
        print("1. Los 5 agentes ya están configurados con GitHub Models")
        print("2. Puedes ejecutar el pipeline completo con:")
        print("   python test_single_agent.py")
        print()
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print()
        print("🔍 Posibles causas:")
        print("1. Token inválido o expirado")
        print("2. Rate limit excedido")
        print("3. Modelo no disponible")
        print()

if __name__ == "__main__":
    asyncio.run(test_github_models_agent())
