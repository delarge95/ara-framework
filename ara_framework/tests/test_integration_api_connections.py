"""
Script para validar conexiones a APIs reales.

Este script verifica que las API keys estén configuradas correctamente
antes de intentar una ejecución end-to-end del pipeline.
"""
import asyncio
from typing import Dict, Tuple
from config.settings import settings


async def test_gemini_api() -> Tuple[bool, str]:
    """Test Gemini API."""
    try:
        if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY.startswith("test_"):
            return False, "API key no configurada (placeholder detectado)"
        
        import google.generativeai as genai
        genai.configure(api_key=settings.GEMINI_API_KEY)
        
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        response = model.generate_content("Test")
        
        return True, f"OK - Response: {len(response.text)} chars"
        
    except Exception as e:
        return False, f"Error: {str(e)[:100]}"


async def test_deepseek_api() -> Tuple[bool, str]:
    """Test DeepSeek API."""
    try:
        if not settings.DEEPSEEK_API_KEY or settings.DEEPSEEK_API_KEY.startswith("test_"):
            return False, "API key no configurada (placeholder detectado)"
        
        from openai import AsyncOpenAI
        
        client = AsyncOpenAI(
            api_key=settings.DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com"
        )
        
        response = await client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": "Test"}],
            max_tokens=10
        )
        
        return True, f"OK - {response.choices[0].message.content}"
        
    except Exception as e:
        return False, f"Error: {str(e)[:100]}"


async def test_anthropic_api() -> Tuple[bool, str]:
    """Test Anthropic Claude API."""
    try:
        if not settings.ANTHROPIC_API_KEY or settings.ANTHROPIC_API_KEY.startswith("test_"):
            return False, "API key no configurada (placeholder detectado)"
        
        from anthropic import AsyncAnthropic
        
        client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
        
        message = await client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=10,
            messages=[{"role": "user", "content": "Test"}]
        )
        
        return True, f"OK - {message.content[0].text}"
        
    except Exception as e:
        return False, f"Error: {str(e)[:100]}"


async def test_redis_connection() -> Tuple[bool, str]:
    """Test Redis connection."""
    try:
        if not settings.REDIS_URL:
            return False, "Redis URL no configurada en .env"
        
        from redis.asyncio import from_url
        
        redis_client = from_url(settings.REDIS_URL, decode_responses=True)
        await redis_client.ping()
        await redis_client.close()
        
        return True, "OK - Redis respondiendo"
        
    except Exception as e:
        return False, f"Error: {str(e)[:100]}"


async def test_supabase_connection() -> Tuple[bool, str]:
    """Test Supabase connection."""
    try:
        if not settings.SUPABASE_URL or settings.SUPABASE_URL.startswith("https://test-"):
            return False, "Supabase URL no configurada (placeholder detectado)"
        
        if not settings.SUPABASE_SERVICE_ROLE_KEY or settings.SUPABASE_SERVICE_ROLE_KEY.startswith("test_"):
            return False, "Supabase service role key no configurada"
        
        from supabase import create_client
        
        client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_SERVICE_ROLE_KEY
        )
        
        # Test simple query
        response = client.table("analyses").select("id").limit(1).execute()
        
        return True, f"OK - Conectado (tablas accesibles)"
        
    except Exception as e:
        return False, f"Error: {str(e)[:100]}"


async def test_semantic_scholar() -> Tuple[bool, str]:
    """Test Semantic Scholar API (rate limited: 1 req/seg)."""
    try:
        import httpx
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.semanticscholar.org/graph/v1/paper/search",
                params={"query": "machine learning", "limit": 1},
                timeout=10.0
            )
            
            if response.status_code == 200:
                data = response.json()
                return True, f"OK - {data.get('total', 0)} papers encontrados"
            else:
                return False, f"HTTP {response.status_code}"
                
    except Exception as e:
        return False, f"Error: {str(e)[:100]}"


async def main():
    """Ejecuta todas las validaciones."""
    print("\n" + "="*70)
    print(" 🔌 VALIDACIÓN DE CONEXIONES A APIS ".center(70, "="))
    print("="*70 + "\n")
    
    tests = [
        ("Gemini API (Google)", test_gemini_api),
        ("DeepSeek API", test_deepseek_api),
        ("Anthropic Claude API", test_anthropic_api),
        ("Redis Cache", test_redis_connection),
        ("Supabase Database", test_supabase_connection),
        ("Semantic Scholar API", test_semantic_scholar),
    ]
    
    results: Dict[str, Tuple[bool, str]] = {}
    
    for name, test_func in tests:
        print(f"Testing {name}...", end=" ", flush=True)
        success, message = await test_func()
        results[name] = (success, message)
        
        status = "✅" if success else "❌"
        print(f"{status} {message}")
        
        # Rate limit para Semantic Scholar
        if "Scholar" in name:
            await asyncio.sleep(1)
    
    print("\n" + "="*70)
    print(" RESUMEN ".center(70, "="))
    print("="*70 + "\n")
    
    total = len(results)
    passed = sum(1 for success, _ in results.values() if success)
    
    for name, (success, _) in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {name}")
    
    print(f"\nTotal: {passed}/{total} servicios disponibles ({passed/total*100:.1f}%)")
    
    # Recomendaciones
    if passed < total:
        print("\n⚠️  RECOMENDACIONES:\n")
        
        for name, (success, message) in results.items():
            if not success:
                if "API key no configurada" in message:
                    env_var = name.split()[0].upper().replace(" ", "_") + "_API_KEY"
                    print(f"   • {name}: Editar .env y configurar {env_var}")
                elif "Redis" in name:
                    print(f"   • {name}: Iniciar Redis localmente o configurar URL en .env")
                elif "Supabase" in name:
                    print(f"   • {name}: Crear proyecto en Supabase y configurar credenciales")
    
    print("\n" + "="*70)
    
    # Determinar si podemos hacer una prueba end-to-end
    ai_apis_ok = results.get("Gemini API (Google)", (False, ""))[0] or \
                 results.get("DeepSeek API", (False, ""))[0] or \
                 results.get("Anthropic Claude API", (False, ""))[0]
    
    scholar_ok = results.get("Semantic Scholar API", (False, ""))[0]
    
    if ai_apis_ok and scholar_ok:
        print("\n✅ LISTO PARA PRUEBA END-TO-END")
        print("   Al menos una AI API y Semantic Scholar están disponibles.")
        print("\n   Ejecutar:")
        print("   python -m cli.main run \"Rust WASM for audio processing\" --output analysis.md")
    else:
        print("\n⚠️  NO LISTO PARA PRUEBA END-TO-END")
        if not ai_apis_ok:
            print("   Falta: Configurar al menos una AI API (Gemini/DeepSeek/Anthropic)")
        if not scholar_ok:
            print("   Falta: Semantic Scholar API no responde (verificar conexión a internet)")
    
    print("\n" + "="*70)
    
    return passed == total


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
