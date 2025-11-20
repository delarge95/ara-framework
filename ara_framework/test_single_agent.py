"""
Test rápido del Niche Analyst (primer agente).
Duración: ~7-8 minutos
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime, timezone
import os

# Set working directory to script location
script_dir = Path(__file__).parent
os.chdir(script_dir)

project_root = script_dir
sys.path.insert(0, str(project_root))

try:
    from rich.console import Console
    from rich.panel import Panel
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    print("⚠️  Rich no disponible, usando print simple")

if HAS_RICH:
    console = Console()


async def main():
    niche = "Rust WebAssembly for real-time audio processing"
    
    if HAS_RICH:
        console.print(Panel.fit(
            f"🧪 Test del Niche Analyst\n\n"
            f"📝 Nicho: {niche}\n"
            f"⏱️  Tiempo estimado: 7-8 minutos",
            title="Quick Test",
            border_style="cyan"
        ))
    else:
        print("=" * 60)
        print("🧪 Test del Niche Analyst")
        print(f"📝 Nicho: {niche}")
        print("⏱️  Tiempo estimado: 7-8 minutos")
        print("=" * 60)
    
    # Verificar importaciones antes de continuar
    try:
        from graphs.research_graph import create_research_graph
    except ImportError as e:
        error_msg = f"❌ Error al importar research_graph: {str(e)}"
        if HAS_RICH:
            console.print(error_msg, style="red")
        else:
            print(error_msg)
        print("\n💡 Verifica que todas las dependencias estén instaladas:")
        print("   pip install -r requirements.txt")
        return
    
    # Crear grafo
    try:
        if HAS_RICH:
            console.print("\n🔧 Creando grafo...", style="yellow")
        else:
            print("\n🔧 Creando grafo...")
        
        graph = create_research_graph(enable_checkpointing=False)
        
        if HAS_RICH:
            console.print("✓ Grafo creado exitosamente", style="green")
        else:
            print("✓ Grafo creado exitosamente")
    except Exception as e:
        error_msg = f"❌ Error al crear grafo: {str(e)}"
        if HAS_RICH:
            console.print(error_msg, style="red")
        else:
            print(error_msg)
        raise
    
    # Estado inicial
    initial_state = {
        "niche": niche,
        "messages": [],
        "agent_history": [],
        "errors": [],
        "retry_count": {},
        "total_credits_used": 0.0,
        "budget_limit": 10.0,
        "budget_exceeded": False,
        "start_time": datetime.now(timezone.utc).isoformat(),
    }
    
    if HAS_RICH:
        console.print("\n⏳ Ejecutando Niche Analyst...\n", style="yellow")
    else:
        print("\n⏳ Ejecutando Niche Analyst...\n")
    
    try:
        # Ejecutar solo hasta el primer agente
        # Nota: Esto ejecutará TODOS los agentes porque el grafo es secuencial
        # Para ejecutar solo uno necesitaríamos modificar el grafo o llamar al nodo directamente
        result = await graph.ainvoke(initial_state)
        
        # Mostrar resultado
        if HAS_RICH:
            console.print("\n✅ [green]Pipeline completado![/green]\n")
        else:
            print("\n✅ Pipeline completado!\n")
        
        analysis = result.get("niche_analysis", "")
        
        if HAS_RICH:
            console.print(Panel(
                analysis[:1000] + ("..." if len(analysis) > 1000 else ""),
                title="📊 Análisis de Nicho (preview)",
                border_style="green"
            ))
        else:
            print("=" * 60)
            print("📊 Análisis de Nicho (preview)")
            print("=" * 60)
            print(analysis[:1000] + ("..." if len(analysis) > 1000 else ""))
            print("=" * 60)
        
        print(f"\n📏 Longitud total: {len(analysis)} caracteres")
        print(f"💰 Costo: ${result.get('total_credits_used', 0.0):.2f}")
        print(f"👥 Agentes ejecutados: {result.get('agent_history', [])}")
        
    except KeyboardInterrupt:
        msg = "\n⚠️  Ejecución interrumpida por el usuario"
        if HAS_RICH:
            console.print(msg, style="yellow")
        else:
            print(msg)
        
    except Exception as e:
        error_msg = f"\n❌ Error durante ejecución: {str(e)}"
        if HAS_RICH:
            console.print(error_msg, style="red")
        else:
            print(error_msg)
        
        import traceback
        print("\n🔍 Traceback completo:")
        traceback.print_exc()
        raise


if __name__ == "__main__":
    asyncio.run(main())
