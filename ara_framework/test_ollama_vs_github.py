"""
Script de comparación: GitHub Models (gpt-4o) vs Ollama (mistral:7b)

Ejecuta el Agent 1 (Niche Analyst) con ambos proveedores y compara:
- Tiempo de ejecución
- Calidad de output
- Uso de herramientas
- Longitud y coherencia de respuestas

Uso:
    python test_ollama_vs_github.py
"""

import asyncio
import time
import os
from datetime import datetime

import structlog
from graphs.research_graph import niche_analyst_node, ResearchState

logger = structlog.get_logger(__name__)


async def test_provider(provider_name: str, niche: str) -> dict:
    """
    Ejecuta Agent 1 con un proveedor específico.
    
    Args:
        provider_name: "github" o "ollama"
        niche: Topic de investigación
        
    Returns:
        dict con métricas y resultados
    """
    print(f"\n{'='*70}")
    print(f"PRUEBA CON {provider_name.upper()}")
    print(f"{'='*70}\n")
    
    # Configurar variable de entorno
    os.environ["USE_OLLAMA"] = "true" if provider_name == "ollama" else "false"
    
    # Reimportar para aplicar cambios
    import importlib
    import graphs.research_graph as rg
    importlib.reload(rg)
    
    # Estado inicial
    initial_state: ResearchState = {
        "niche": niche,
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
    
    # Ejecutar y medir tiempo
    start_time = time.time()
    
    try:
        result_state = await rg.niche_analyst_node(initial_state)
        execution_time = time.time() - start_time
        
        # Analizar resultados
        analysis = result_state.get("niche_analysis", "")
        
        metrics = {
            "provider": provider_name,
            "success": True,
            "execution_time": execution_time,
            "output_length": len(analysis),
            "output_preview": analysis[:500] if analysis else "NO OUTPUT",
            "has_viability_score": "viability score" in analysis.lower() if analysis else False,
            "has_trends": "trends" in analysis.lower() if analysis else False,
            "has_keywords": "keywords" in analysis.lower() if analysis else False,
            "errors": result_state.get("errors", []),
            "warnings": result_state.get("warnings", []),
        }
        
        print(f"\n✅ Ejecución exitosa")
        print(f"⏱️  Tiempo: {execution_time:.2f} segundos")
        print(f"📝 Longitud output: {metrics['output_length']} caracteres")
        print(f"🎯 Viability Score presente: {metrics['has_viability_score']}")
        print(f"📊 Trends presentes: {metrics['has_trends']}")
        print(f"🔑 Keywords presentes: {metrics['has_keywords']}")
        
        if metrics['errors']:
            print(f"⚠️  Errores: {len(metrics['errors'])}")
            for error in metrics['errors']:
                print(f"   - {error}")
        
        print(f"\n--- Preview del Output (primeros 500 chars) ---")
        print(metrics['output_preview'])
        print(f"{'='*70}\n")
        
        return metrics
        
    except Exception as e:
        execution_time = time.time() - start_time
        
        print(f"\n❌ Error durante ejecución")
        print(f"⏱️  Tiempo hasta error: {execution_time:.2f} segundos")
        print(f"🔴 Error: {str(e)}")
        print(f"{'='*70}\n")
        
        return {
            "provider": provider_name,
            "success": False,
            "execution_time": execution_time,
            "error": str(e),
            "output_length": 0,
        }


async def main():
    """Ejecuta comparación completa."""
    
    print("\n" + "="*70)
    print(" COMPARACIÓN: GITHUB MODELS vs OLLAMA")
    print("="*70)
    print("\n📋 Configuración:")
    print("   - Agent: Niche Analyst (Agent 1)")
    print("   - GitHub Model: gpt-4o")
    print("   - Ollama Model: mistral:7b")
    print("   - Niche: 'deep learning for drug discovery'")
    print("\n⏳ Nota: Cada prueba tarda ~5-8 minutos")
    print("="*70)
    
    # Niche de prueba (mismo para ambos)
    test_niche = "deep learning for drug discovery"
    
    # Ejecutar con GitHub Models
    github_metrics = await test_provider("github", test_niche)
    
    # Ejecutar con Ollama
    ollama_metrics = await test_provider("ollama", test_niche)
    
    # Comparación final
    print("\n" + "="*70)
    print(" COMPARACIÓN FINAL")
    print("="*70)
    
    if github_metrics.get("success") and ollama_metrics.get("success"):
        print("\n✅ Ambas pruebas completadas exitosamente\n")
        
        print("⏱️  TIEMPO DE EJECUCIÓN:")
        print(f"   GitHub (gpt-4o):     {github_metrics['execution_time']:.2f}s")
        print(f"   Ollama (mistral:7b): {ollama_metrics['execution_time']:.2f}s")
        speed_diff = ((ollama_metrics['execution_time'] - github_metrics['execution_time']) 
                      / github_metrics['execution_time'] * 100)
        print(f"   Diferencia:          {speed_diff:+.1f}%")
        
        print("\n📝 LONGITUD DE OUTPUT:")
        print(f"   GitHub (gpt-4o):     {github_metrics['output_length']:,} caracteres")
        print(f"   Ollama (mistral:7b): {ollama_metrics['output_length']:,} caracteres")
        length_diff = ((ollama_metrics['output_length'] - github_metrics['output_length']) 
                       / github_metrics['output_length'] * 100)
        print(f"   Diferencia:          {length_diff:+.1f}%")
        
        print("\n🎯 COMPONENTES REQUERIDOS:")
        print(f"   Viability Score:")
        print(f"      GitHub:  {'✅' if github_metrics['has_viability_score'] else '❌'}")
        print(f"      Ollama:  {'✅' if ollama_metrics['has_viability_score'] else '❌'}")
        print(f"   Trends:")
        print(f"      GitHub:  {'✅' if github_metrics['has_trends'] else '❌'}")
        print(f"      Ollama:  {'✅' if ollama_metrics['has_trends'] else '❌'}")
        print(f"   Keywords:")
        print(f"      GitHub:  {'✅' if github_metrics['has_keywords'] else '❌'}")
        print(f"      Ollama:  {'✅' if ollama_metrics['has_keywords'] else '❌'}")
        
        print("\n" + "="*70)
        print(" RECOMENDACIÓN")
        print("="*70)
        
        # Análisis de calidad
        ollama_quality_score = sum([
            ollama_metrics['has_viability_score'],
            ollama_metrics['has_trends'],
            ollama_metrics['has_keywords'],
            ollama_metrics['output_length'] > 1000,
        ])
        
        if ollama_quality_score >= 3:
            print("\n✅ OLLAMA APTO PARA DESARROLLO")
            print("   - Tool calling funciona correctamente")
            print("   - Output cumple requisitos básicos")
            print("   - Recomendado para iteración rápida")
            print("\n💡 Estrategia sugerida:")
            print("   • Desarrollo/pruebas: Ollama (ilimitado)")
            print("   • Validación final: GitHub Models (mayor calidad)")
        elif ollama_quality_score >= 2:
            print("\n⚠️  OLLAMA PARCIALMENTE APTO")
            print("   - Tool calling funciona")
            print("   - Output incompleto o inferior")
            print("\n💡 Estrategia sugerida:")
            print("   • Agentes simples: Ollama")
            print("   • Agentes complejos: GitHub Models")
        else:
            print("\n❌ OLLAMA NO RECOMENDADO")
            print("   - Calidad muy inferior a GitHub Models")
            print("\n💡 Estrategia sugerida:")
            print("   • Usar solo GitHub Models")
            print("   • Optimizar uso (caching, rate limiting)")
        
    else:
        print("\n❌ Una o ambas pruebas fallaron")
        if not github_metrics.get("success"):
            print(f"   GitHub error: {github_metrics.get('error')}")
        if not ollama_metrics.get("success"):
            print(f"   Ollama error: {ollama_metrics.get('error')}")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    asyncio.run(main())
