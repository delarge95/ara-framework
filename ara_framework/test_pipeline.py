"""
Script para probar el pipeline completo de investigación.

Este script ejecuta el pipeline con un nicho de prueba y muestra
resultados intermedios y finales.
"""

import asyncio
import sys
from pathlib import Path

# Agregar path del proyecto
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from graphs.research_graph import run_research_pipeline
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
import structlog

logger = structlog.get_logger(__name__)
console = Console()


async def main():
    """Ejecuta el pipeline de investigación con un nicho de prueba."""
    
    # Nicho de prueba (cambia esto por el que quieras)
    niche = "Rust WebAssembly for real-time audio processing in web browsers"
    
    console.print(Panel.fit(
        f"🚀 Iniciando análisis de investigación\n\n"
        f"📝 Nicho: {niche}\n"
        f"💰 Presupuesto: $10.00 (GRATIS con Groq)\n"
        f"⏱️  Tiempo estimado: 60-75 minutos",
        title="ARA Framework - Research Pipeline",
        border_style="cyan"
    ))
    
    try:
        # Ejecutar pipeline
        console.print("\n⏳ Ejecutando pipeline... (esto tomará ~60-75 min)\n", style="yellow")
        
        result = await run_research_pipeline(
            niche=niche,
            budget_limit=10.0,
            enable_checkpointing=True,
        )
        
        # Mostrar resultados
        console.print("\n✅ [green]Pipeline completado exitosamente![/green]\n")
        
        # Metadata
        console.print(Panel(
            f"🕐 Inicio: {result.get('start_time', 'N/A')}\n"
            f"🕐 Fin: {result.get('end_time', 'N/A')}\n"
            f"👥 Agentes ejecutados: {len(result.get('agent_history', []))}\n"
            f"💬 Mensajes totales: {len(result.get('messages', []))}\n"
            f"💰 Créditos usados: ${result.get('total_credits_used', 0.0):.2f}\n"
            f"⚠️  Errores: {len(result.get('errors', []))}",
            title="📊 Metadata de Ejecución",
            border_style="blue"
        ))
        
        # Outputs de cada agente
        console.print("\n" + "="*80 + "\n", style="cyan")
        console.print("📄 OUTPUTS DE AGENTES", style="bold cyan")
        console.print("="*80 + "\n", style="cyan")
        
        agents = [
            ("1️⃣  Niche Analysis", "niche_analysis"),
            ("2️⃣  Literature Review", "literature_review"),
            ("3️⃣  Technical Architecture", "technical_architecture"),
            ("4️⃣  Implementation Plan", "implementation_plan"),
            ("5️⃣  Final Report", "final_report"),
        ]
        
        for title, key in agents:
            output = result.get(key)
            if output:
                console.print(f"\n{title}", style="bold yellow")
                console.print("-" * 80, style="yellow")
                # Mostrar primeros 500 caracteres
                preview = output[:500] + ("..." if len(output) > 500 else "")
                console.print(preview)
                console.print(f"\n✓ Longitud total: {len(output)} caracteres\n")
        
        # Guardar reporte final
        output_file = project_root / "output" / "final_report.md"
        output_file.parent.mkdir(exist_ok=True)
        output_file.write_text(result.get("final_report", ""), encoding="utf-8")
        
        console.print(Panel(
            f"📁 Reporte guardado en:\n{output_file}\n\n"
            f"✅ Análisis completo con éxito!",
            title="🎉 Resultado Final",
            border_style="green"
        ))
        
    except KeyboardInterrupt:
        console.print("\n⚠️  [yellow]Ejecución interrumpida por el usuario[/yellow]")
        console.print("💡 Los checkpoints permiten reanudar más tarde con el mismo thread_id")
        
    except Exception as e:
        console.print(f"\n❌ [red]Error durante la ejecución:[/red]\n{str(e)}")
        logger.error("pipeline_failed", error=str(e), error_type=type(e).__name__)
        raise


if __name__ == "__main__":
    # Ejecutar
    asyncio.run(main())
