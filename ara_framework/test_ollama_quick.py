"""
Test rápido: Verificar que Ollama funciona con el system completo

Ejecuta una invocación simple del Agent 1 con Ollama para verificar:
- La integración funciona
- Los tools se llaman
- El output es coherente

Duración: ~3-5 minutos (vs 15 min del test completo)
"""

import asyncio
import os
from datetime import datetime

import structlog
from graphs.research_graph import ResearchState

logger = structlog.get_logger(__name__)


async def quick_test():
    """Test rápido de Ollama integración."""
    
    print("\n" + "="*70)
    print(" TEST RÁPIDO: OLLAMA INTEGRACIÓN")
    print("="*70)
    
    # Forzar Ollama
    os.environ["USE_OLLAMA"] = "true"
    
    # Reimportar para aplicar cambio
    import importlib
    import graphs.research_graph as rg
    importlib.reload(rg)
    
    print("\n✅ Variable USE_OLLAMA activada")
    print("📦 LLM Provider: Ollama")
    print("🤖 Modelo: mistral:7b")
    print("🎯 Agent: Niche Analyst (Agent 1)")
    print("📝 Niche: 'blockchain for supply chain'")
    print("\n⏳ Ejecutando... (esto tardará ~3-5 minutos)")
    print("="*70 + "\n")
    
    # Estado inicial simplificado
    initial_state: ResearchState = {
        "niche": "blockchain for supply chain",
        "niche_analysis": None,
        "literature_review": None,
        "technical_architecture": None,
        "implementation_plan": None,
        "final_report": None,
        "messages": [],
        "current_agent": "niche_analyst",
        "agent_history": [],
        "start_time": datetime.now().isoformat(),
        "end_time": None,
        "errors": [],
        "warnings": [],
        "retry_count": {},
        "total_credits_used": 0.0,
        "budget_limit": 10.0,
        "budget_exceeded": False,
    }
    
    try:
        # Ejecutar Agent 1
        result = await rg.niche_analyst_node(initial_state)
        
        # Analizar resultado
        analysis = result.get("niche_analysis", "")
        errors = result.get("errors", [])
        warnings = result.get("warnings", [])
        
        print("\n" + "="*70)
        print(" RESULTADOS")
        print("="*70)
        
        if analysis:
            print(f"\n✅ ÉXITO: Análisis generado")
            print(f"📝 Longitud: {len(analysis):,} caracteres")
            
            # Verificar componentes esperados
            has_score = "viability" in analysis.lower() and any(str(i) in analysis for i in range(1, 11))
            has_trends = "trend" in analysis.lower()
            has_keywords = "keyword" in analysis.lower()
            has_github = "github" in analysis.lower()
            
            print(f"\n🎯 Componentes esperados:")
            print(f"   Viability Score: {'✅' if has_score else '❌'}")
            print(f"   Trends:          {'✅' if has_trends else '❌'}")
            print(f"   Keywords:        {'✅' if has_keywords else '❌'}")
            print(f"   GitHub repos:    {'✅' if has_github else '❌'}")
            
            # Preview
            print(f"\n--- Preview (primeros 800 caracteres) ---")
            print(analysis[:800])
            if len(analysis) > 800:
                print(f"\n[... +{len(analysis) - 800:,} caracteres más ...]")
            
            # Calidad
            quality_score = sum([has_score, has_trends, has_keywords, has_github])
            print(f"\n📊 Calidad: {quality_score}/4 componentes presentes")
            
            if quality_score >= 3:
                print("✅ CALIDAD ACEPTABLE para desarrollo")
            elif quality_score >= 2:
                print("⚠️  CALIDAD PARCIAL - revisar componentes faltantes")
            else:
                print("❌ CALIDAD INSUFICIENTE")
        else:
            print("\n❌ ERROR: No se generó análisis")
        
        # Errores y warnings
        if errors:
            print(f"\n⚠️  Errores encontrados ({len(errors)}):")
            for err in errors[:3]:  # Solo primeros 3
                print(f"   - {err}")
        
        if warnings:
            print(f"\n⚠️  Warnings ({len(warnings)}):")
            for warn in warnings[:3]:
                print(f"   - {warn}")
        
        print("\n" + "="*70)
        print(" RECOMENDACIÓN")
        print("="*70)
        
        if analysis and len(analysis) > 1000:
            print("\n✅ Ollama funciona correctamente con el sistema")
            print("💡 Puedes usarlo para desarrollo sin límites")
            print("\n📋 Próximos pasos:")
            print("   1. Ejecutar test completo: python test_ollama_vs_github.py")
            print("   2. O usar directamente: USE_OLLAMA=true python main.py")
        else:
            print("\n⚠️  Revisar configuración o comparar con GitHub Models")
            print("   python test_ollama_vs_github.py")
        
        print("\n" + "="*70)
        
    except Exception as e:
        print("\n" + "="*70)
        print(" ERROR DURANTE EJECUCIÓN")
        print("="*70)
        print(f"\n❌ {str(e)}")
        print("\nVerifica:")
        print("   1. Ollama server corriendo: curl http://localhost:11434")
        print("   2. Mistral descargado: ollama list")
        print("   3. Ejecutar diagnóstico: python check_ollama_setup.py")
        print("\n" + "="*70)


if __name__ == "__main__":
    asyncio.run(quick_test())
