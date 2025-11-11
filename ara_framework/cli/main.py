"""
CLI Interface for ARA Framework.

Comandos principales:
- ara run <niche>             Ejecuta análisis completo
- ara status [analysis_id]    Muestra status de análisis
- ara list                     Lista análisis recientes
- ara cache clear             Limpia cache Redis
- ara logs [--tail N]         Muestra logs recientes
- ara budget                   Muestra uso de créditos
- ara test                     Ejecuta tests del framework

Usage:
    python -m cli.main run "Rust WASM for audio"
    python -m cli.main status abc123
    python -m cli.main budget
    python -m cli.main cache clear
"""
import asyncio
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
import json

import typer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.panel import Panel
from rich.markdown import Markdown
from rich import box
import structlog

from core.pipeline import AnalysisPipeline, PipelineStatus, run_quick_analysis
from core.budget_manager import BudgetManager
from config.settings import settings

# Initialize
app = typer.Typer(
    name="ara",
    help="🔬 ARA Framework - Automated Research & Analysis",
    add_completion=False,
)
console = Console()
logger = structlog.get_logger(__name__)


def format_duration(seconds: float) -> str:
    """Formatea duración en formato legible."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        return f"{seconds / 60:.1f}min"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"


def format_credits(credits: float) -> str:
    """Formatea créditos con color."""
    if credits == 0:
        return "[green]FREE[/green]"
    elif credits < 1:
        return f"[yellow]{credits:.2f}[/yellow]"
    else:
        return f"[red]{credits:.2f}[/red]"


@app.command()
def run(
    niche: str = typer.Argument(..., help="Niche a analizar (ej: 'Rust WASM for audio')"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Archivo de salida (.md)"),
    timeout: int = typer.Option(90, "--timeout", "-t", help="Timeout en minutos"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Modo verbose"),
):
    """
    🚀 Ejecuta análisis completo del niche.
    
    El pipeline ejecutará 5 agentes especializados:
    1. NicheAnalyst - Viabilidad y tendencias
    2. LiteratureResearcher - Búsqueda de papers
    3. TechnicalArchitect - Arquitectura técnica
    4. ImplementationSpecialist - Plan de implementación
    5. ContentSynthesizer - Reporte final
    
    Examples:
        ara run "Rust WASM for real-time audio processing"
        ara run "Python ML for medical imaging" --output report.md
    """
    console.print(Panel.fit(
        f"🔬 [bold]ARA Framework[/bold] - Automated Research & Analysis\n"
        f"📊 Niche: [cyan]{niche}[/cyan]\n"
        f"⏱️  Timeout: {timeout} minutos\n"
        f"💰 Estimado: ~3-5 créditos",
        border_style="blue",
    ))
    
    # Check budget
    try:
        budget_manager = BudgetManager()
        remaining = asyncio.run(budget_manager.get_remaining_credits())
        
        if remaining < 5:
            console.print(
                f"⚠️  [yellow]Créditos bajos: {remaining:.2f} disponibles[/yellow]\n"
                f"   El pipeline usará modelos gratuitos (Gemini, DeepSeek)",
                style="yellow",
            )
    except Exception as e:
        console.print(f"⚠️  No se pudo verificar budget: {e}", style="yellow")
    
    console.print()
    
    # Create pipeline
    pipeline = AnalysisPipeline(
        timeout_minutes=timeout,
        enable_telemetry=True,
        enable_circuit_breaker=True,
    )
    
    # Execute with progress bar
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task(
            f"[cyan]Analizando '{niche}'...",
            total=None,  # Indeterminate
        )
        
        try:
            result = asyncio.run(pipeline.run_analysis(niche))
            
            progress.update(task, completed=True)
            console.print()
            
            # Display results
            if result.status == PipelineStatus.COMPLETED:
                console.print("✅ [bold green]Análisis completado exitosamente[/bold green]")
                
                # Metrics table
                table = Table(show_header=False, box=box.SIMPLE)
                table.add_column("Metric", style="cyan")
                table.add_column("Value", style="white")
                
                table.add_row("⏱️  Duración", format_duration(result.duration_seconds))
                table.add_row("💰 Créditos usados", format_credits(result.total_credits_used))
                table.add_row("📊 Tamaño reporte", f"{len(result.final_report):,} caracteres")
                
                if result.supabase_saved:
                    table.add_row("💾 Supabase ID", result.supabase_record_id or "N/A")
                elif result.local_backup_path:
                    table.add_row("💾 Backup local", result.local_backup_path)
                
                console.print(table)
                console.print()
                
                # Warnings
                if result.warnings:
                    console.print(f"⚠️  [yellow]{len(result.warnings)} advertencias:[/yellow]")
                    for warning in result.warnings:
                        console.print(f"   • {warning}", style="yellow")
                    console.print()
                
                # Save output if requested
                if output:
                    output.write_text(result.final_report, encoding="utf-8")
                    console.print(f"💾 Reporte guardado en: [cyan]{output}[/cyan]")
                else:
                    # Display preview
                    console.print(Panel(
                        Markdown(result.final_report[:500] + "\n\n[... preview truncado ...]"),
                        title="📄 Preview del Reporte",
                        border_style="green",
                    ))
                    console.print("\n💡 Usa --output para guardar el reporte completo")
            
            elif result.status == PipelineStatus.TIMEOUT:
                console.print(f"⏱️  [bold red]Timeout después de {timeout} minutos[/bold red]")
                console.print("   Intenta aumentar el timeout con --timeout")
            
            elif result.status == PipelineStatus.FAILED:
                console.print("❌ [bold red]Análisis fallido[/bold red]")
                
                if result.errors:
                    console.print("\n🔴 Errores:")
                    for error in result.errors:
                        console.print(f"   • {error}", style="red")
            
            elif result.status == PipelineStatus.PARTIAL:
                console.print("⚠️  [bold yellow]Análisis parcial[/bold yellow]")
                console.print(f"   Algunos agentes completados, ver: {result.local_backup_path}")
        
        except KeyboardInterrupt:
            progress.stop()
            console.print("\n❌ Análisis cancelado por el usuario", style="red")
            raise typer.Exit(1)
        
        except Exception as e:
            progress.stop()
            console.print(f"\n❌ [bold red]Error inesperado:[/bold red] {e}", style="red")
            
            if verbose:
                import traceback
                console.print("\n[red]Traceback:[/red]")
                console.print(traceback.format_exc())
            
            raise typer.Exit(1)


@app.command()
def budget():
    """
    💰 Muestra información de créditos y uso.
    
    Muestra:
    - Créditos disponibles
    - Uso del mes actual
    - Uso por modelo
    - Alertas
    """
    console.print(Panel.fit(
        "💰 [bold]Budget & Credits[/bold]",
        border_style="green",
    ))
    
    try:
        budget_manager = BudgetManager()
        
        # Get metrics
        remaining = asyncio.run(budget_manager.get_remaining_credits())
        used = budget_manager.monthly_limit - remaining
        percentage = (used / budget_manager.monthly_limit) * 100
        
        # Main metrics
        console.print()
        console.print(f"📊 [bold]Límite mensual:[/bold] {budget_manager.monthly_limit:.2f} créditos")
        console.print(f"✅ [bold]Disponible:[/bold] {format_credits(remaining)}")
        console.print(f"📉 [bold]Usado:[/bold] {format_credits(used)} ({percentage:.1f}%)")
        console.print()
        
        # Progress bar
        from rich.progress import BarColumn, Progress as RichProgress
        with RichProgress(BarColumn(), console=console) as progress:
            progress.add_task("", completed=used, total=budget_manager.monthly_limit)
        
        console.print()
        
        # Models table
        table = Table(title="🤖 Modelos Configurados", box=box.ROUNDED)
        table.add_column("Modelo", style="cyan")
        table.add_column("Costo", justify="right")
        table.add_column("RPM Limit", justify="right")
        table.add_column("Status", justify="center")
        
        for model_name, config in budget_manager.models.items():
            status = "🟢 FREE" if config.is_free else "💰 PAID"
            table.add_row(
                model_name,
                f"{config.credits_per_request:.2f} cr",
                f"{config.rpm_limit}/min",
                status,
            )
        
        console.print(table)
        console.print()
        
        # Alerts
        if remaining < budget_manager.monthly_limit * 0.2:
            console.print("⚠️  [bold yellow]Alerta:[/bold yellow] Créditos bajos (<20%)", style="yellow")
            console.print("   Considera usar modelos gratuitos (Gemini, DeepSeek)")
    
    except Exception as e:
        console.print(f"❌ Error obteniendo budget: {e}", style="red")
        raise typer.Exit(1)


@app.command()
def status(
    analysis_id: Optional[str] = typer.Argument(None, help="ID del análisis"),
):
    """
    📊 Muestra status de análisis (último o por ID).
    """
    console.print("📊 [bold]Analysis Status[/bold]\n")
    
    if analysis_id:
        console.print(f"🔍 Buscando análisis: [cyan]{analysis_id}[/cyan]")
        console.print("⚠️  [yellow]Feature en desarrollo[/yellow]")
    else:
        console.print("📋 Mostrando último análisis")
        console.print("⚠️  [yellow]Feature en desarrollo[/yellow]")


@app.command()
def list(
    limit: int = typer.Option(10, "--limit", "-n", help="Número de análisis a mostrar"),
):
    """
    📋 Lista análisis recientes.
    """
    console.print(f"📋 [bold]Últimos {limit} análisis[/bold]\n")
    console.print("⚠️  [yellow]Feature en desarrollo[/yellow]")


@app.command()
def cache(
    action: str = typer.Argument(..., help="Acción: clear, stats"),
):
    """
    🗄️  Gestiona cache Redis.
    
    Acciones:
    - clear: Limpia todo el cache
    - stats: Muestra estadísticas
    """
    if action == "clear":
        console.print("🗄️  Limpiando cache...", style="yellow")
        try:
            import redis
            r = redis.from_url(settings.REDIS_URL)
            r.flushdb()
            console.print("✅ Cache limpiado exitosamente", style="green")
        except Exception as e:
            console.print(f"❌ Error limpiando cache: {e}", style="red")
            raise typer.Exit(1)
    
    elif action == "stats":
        console.print("📊 [bold]Cache Stats[/bold]\n")
        try:
            import redis
            r = redis.from_url(settings.REDIS_URL)
            info = r.info("stats")
            
            table = Table(show_header=False, box=box.SIMPLE)
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="white")
            
            table.add_row("Total connections", str(info.get("total_connections_received", 0)))
            table.add_row("Total commands", str(info.get("total_commands_processed", 0)))
            table.add_row("Keyspace hits", str(info.get("keyspace_hits", 0)))
            table.add_row("Keyspace misses", str(info.get("keyspace_misses", 0)))
            
            console.print(table)
        except Exception as e:
            console.print(f"❌ Error obteniendo stats: {e}", style="red")
            raise typer.Exit(1)
    
    else:
        console.print(f"❌ Acción desconocida: {action}", style="red")
        console.print("Acciones válidas: clear, stats")
        raise typer.Exit(1)


@app.command()
def test(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
    coverage: bool = typer.Option(False, "--coverage", "-c", help="Run with coverage"),
):
    """
    🧪 Ejecuta tests del framework.
    """
    import subprocess
    
    console.print("🧪 [bold]Running Tests[/bold]\n")
    
    cmd = ["pytest", "tests/"]
    
    if verbose:
        cmd.append("-v")
        cmd.append("-s")
    
    if coverage:
        cmd.extend(["--cov=ara_framework", "--cov-report=html", "--cov-report=term"])
    
    console.print(f"📝 Comando: [cyan]{' '.join(cmd)}[/cyan]\n")
    
    try:
        result = subprocess.run(cmd, check=False)
        
        if result.returncode == 0:
            console.print("\n✅ [bold green]Tests passed![/bold green]")
        else:
            console.print(f"\n❌ [bold red]Tests failed (exit code: {result.returncode})[/bold red]")
            raise typer.Exit(result.returncode)
    
    except FileNotFoundError:
        console.print("❌ pytest no encontrado. Instala con: pip install pytest", style="red")
        raise typer.Exit(1)


@app.command()
def version():
    """
    📦 Muestra versión del framework.
    """
    console.print(Panel.fit(
        "🔬 [bold]ARA Framework[/bold]\n"
        "Version: [cyan]1.0.0[/cyan]\n"
        "Build: [cyan]2025-01-01[/cyan]\n"
        "Python: [cyan]3.11+[/cyan]",
        border_style="blue",
    ))


def main():
    """Entry point."""
    app()


if __name__ == "__main__":
    main()
