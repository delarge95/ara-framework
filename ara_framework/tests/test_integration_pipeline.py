"""
Test manual del pipeline con datos mock.

Este script prueba componentes clave sin hacer llamadas reales a APIs.
"""
import asyncio
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock


async def test_budget_manager():
    """Test 1: BudgetManager funcional."""
    print("\n" + "="*60)
    print("TEST 1: Budget Manager")
    print("="*60)
    
    try:
        from core.budget_manager import BudgetManager, MODEL_COSTS
        
        # Crear instancia (sin Redis/Supabase)
        budget = BudgetManager(
            redis_client=None,
            supabase_client=None,
            monthly_limit=300.0
        )
        
        print("✅ BudgetManager inicializado")
        print(f"   - Límite mensual: {budget.monthly_limit} créditos")
        print(f"   - Modelos configurados: {len(budget.models)}")
        
        # Verificar modelos
        for name, cost in list(MODEL_COSTS.items())[:3]:
            status = "FREE" if cost.is_free else "PAID"
            print(f"   - {name}: {cost.credits_per_request} cr/req [{status}]")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en BudgetManager: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_config_loading():
    """Test 2: Carga de configuración."""
    print("\n" + "="*60)
    print("TEST 2: Configuración (.env)")
    print("="*60)
    
    try:
        from config.settings import settings
        
        print("✅ Configuración cargada desde .env")
        print(f"   - ENV: {settings.ENV}")
        print(f"   - DEBUG: {settings.DEBUG}")
        print(f"   - LOG_LEVEL: {settings.LOG_LEVEL}")
        print(f"   - Redis URL configurado: {'Sí' if settings.REDIS_URL else 'No'}")
        print(f"   - Supabase URL configurado: {'Sí' if settings.SUPABASE_URL else 'No'}")
        
        # Verificar API keys (sin mostrar valores)
        api_keys = [
            ("Gemini", settings.GEMINI_API_KEY),
            ("DeepSeek", settings.DEEPSEEK_API_KEY),
            ("Anthropic", settings.ANTHROPIC_API_KEY),
        ]
        
        for name, key in api_keys:
            status = "✓" if key and not key.startswith("test_") else "⚠"
            print(f"   - {name} API Key: {status} {'(mock)' if key and key.startswith('test_') else '(configurado)'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        return False


async def test_mock_analysis():
    """Test 3: Simulación de análisis."""
    print("\n" + "="*60)
    print("TEST 3: Simulación de Análisis Pipeline")
    print("="*60)
    
    try:
        # Simular flujo de análisis completo
        niche = "Rust WASM for audio processing"
        
        print(f"📋 Niche: {niche}")
        print(f"   Longitud: {len(niche)} caracteres")
        print(f"   Validación: {'✅ PASS' if len(niche) >= 10 else '❌ FAIL'}")
        
        # Simular resultado de análisis
        print("\n📊 Flujo de análisis simulado:")
        
        agents = [
            ("NicheAnalyst", "7-8 min", "0 cr"),
            ("LiteratureResearcher", "20-25 min", "0-0.33 cr"),
            ("TechnicalArchitect", "10-12 min", "0.33-1 cr"),
            ("ImplementationSpecialist", "7-8 min", "0.33 cr"),
            ("ContentSynthesizer", "9-10 min", "0.33 cr"),
        ]
        
        total_time_min = 0
        total_time_max = 0
        
        for i, (agent, duration, credits) in enumerate(agents, 1):
            print(f"   {i}. {agent:25} → {duration:10} | {credits}")
            # Extraer tiempos
            times = duration.replace(" min", "").split("-")
            total_time_min += int(times[0])
            total_time_max += int(times[1])
        
        print(f"\n⏱️  Tiempo estimado: {total_time_min}-{total_time_max} minutos")
        print(f"💰 Costo estimado: 1-2.33 créditos")
        
        # Simular guardado
        analysis_id = f"mock-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
        print(f"\n✅ Análisis simulado guardado: {analysis_id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en simulación: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_agent_configuration():
    """Test 4: Configuración de agentes."""
    print("\n" + "="*60)
    print("TEST 4: Configuración de Agentes")
    print("="*60)
    
    try:
        from agents import (
            create_niche_analyst,
            create_literature_researcher,
            create_technical_architect,
            create_implementation_specialist,
            create_content_synthesizer,
        )
        
        print("✅ Imports de agentes exitosos")
        
        # Simular creación de agentes
        agents_config = [
            ("NicheAnalyst", create_niche_analyst),
            ("LiteratureResearcher", create_literature_researcher),
            ("TechnicalArchitect", create_technical_architect),
            ("ImplementationSpecialist", create_implementation_specialist),
            ("ContentSynthesizer", create_content_synthesizer),
        ]
        
        for name, creator_func in agents_config:
            print(f"   - {name}: Función disponible ✓")
        
        print("\n✅ Todos los agentes tienen funciones de creación disponibles")
        return True
        
    except Exception as e:
        print(f"❌ Error en configuración de agentes: {e}")
        return False


async def main():
    """Ejecuta todos los tests manuales."""
    print("\n" + "="*70)
    print(" 🧪 TEST MANUAL DEL PIPELINE - ARA FRAMEWORK ".center(70, "="))
    print("="*70)
    
    results = []
    
    # Test 1: Budget Manager
    results.append(("Budget Manager", await test_budget_manager()))
    
    # Test 2: Configuración
    results.append(("Configuración", await test_config_loading()))
    
    # Test 3: Simulación Análisis
    results.append(("Simulación Análisis", await test_mock_analysis()))
    
    # Test 4: Configuración de Agentes
    results.append(("Configuración Agentes", await test_agent_configuration()))
    
    # Resumen
    print("\n" + "="*70)
    print(" RESUMEN DE TESTS ".center(70, "="))
    print("="*70)
    
    total = len(results)
    passed = sum(1 for _, result in results if result)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print("\n" + "-"*70)
    print(f"Total: {passed}/{total} tests pasados ({passed/total*100:.1f}%)")
    print("="*70)
    
    return passed == total


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
