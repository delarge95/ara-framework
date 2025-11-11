"""
Test End-to-End del pipeline con monitoreo detallado.
Ejecuta análisis real con logs en tiempo real.
"""
import asyncio
import sys
from datetime import datetime
from pathlib import Path
import structlog

# Configurar logging verbose
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.ConsoleRenderer(colors=True)
    ],
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=False,
)

logger = structlog.get_logger()


async def test_e2e():
    """Test end-to-end con monitoreo."""
    
    logger.info(">> INICIANDO TEST END-TO-END")
    logger.info("=" * 80)
    
    niche = "Rust WebAssembly for real-time audio processing"
    start_time = datetime.now()
    
    try:
        # 1. Validar configuración
        logger.info("📋 PASO 1/6: Validando configuración")
        from config.settings import settings
        
        logger.info("✅ Settings cargado", 
                   env=settings.ENV,
                   gemini_configured=bool(settings.GEMINI_API_KEY))
        
        # 2. Inicializar BudgetManager
        logger.info("📋 PASO 2/6: Inicializando BudgetManager")
        from core.budget_manager import BudgetManager
        
        budget_manager = BudgetManager(
            redis_client=None,
            supabase_client=None,
            monthly_limit=settings.MONTHLY_CREDIT_LIMIT
        )
        
        status = budget_manager.get_status()
        logger.info("✅ BudgetManager inicializado",
                   limit=status.monthly_limit,
                   available=status.available,
                   models=len(budget_manager.models))
        
        # 3. Crear agentes
        logger.info("📋 PASO 3/6: Creando agentes especializados")
        from agents.niche_analyst import create_niche_analyst
        from agents.literature_researcher import create_literature_researcher
        from agents.technical_architect import create_technical_architect
        from agents.implementation_specialist import create_implementation_specialist
        from agents.content_synthesizer import create_content_synthesizer
        
        agents = [
            create_niche_analyst(budget_manager),
            create_literature_researcher(budget_manager),
            create_technical_architect(budget_manager),
            create_implementation_specialist(budget_manager),
            create_content_synthesizer(budget_manager)
        ]
        
        logger.info("✅ Agentes creados", count=len(agents))
        for i, agent in enumerate(agents, 1):
            logger.info(f"   {i}. {agent.role}")
        
        # 4. Crear Crew
        logger.info("📋 PASO 4/6: Configurando Crew")
        from crewai import Crew, Process
        
        # Crear tareas simples para cada agente
        from crewai import Task
        
        tasks = []
        
        # Task 1: Análisis del nicho
        task1 = Task(
            description=f"Analiza la viabilidad del nicho '{niche}'. Evalúa demanda, competencia y tendencias.",
            agent=agents[0],
            expected_output="Análisis de viabilidad en formato JSON"
        )
        tasks.append(task1)
        logger.info("✅ Task 1 creada: NicheAnalyst")
        
        # Task 2: Investigación literatura (depende de task1)
        task2 = Task(
            description=f"Busca papers académicos sobre '{niche}' usando Semantic Scholar. Enfócate en los más citados de últimos 3 años.",
            agent=agents[1],
            expected_output="Lista de 10-15 papers relevantes con abstracts",
            context=[task1]
        )
        tasks.append(task2)
        logger.info("✅ Task 2 creada: LiteratureResearcher")
        
        # Task 3: Arquitectura técnica (depende de task2)
        task3 = Task(
            description=f"Diseña arquitectura técnica para '{niche}'. Incluye stack, componentes clave y flujo de datos.",
            agent=agents[2],
            expected_output="Propuesta de arquitectura detallada",
            context=[task1, task2]
        )
        tasks.append(task3)
        logger.info("✅ Task 3 creada: TechnicalArchitect")
        
        # Task 4: Especificación implementación (depende de task3)
        task4 = Task(
            description=f"Detalla pasos de implementación para '{niche}'. Incluye desafíos y mejores prácticas.",
            agent=agents[3],
            expected_output="Plan de implementación paso a paso",
            context=[task2, task3]
        )
        tasks.append(task4)
        logger.info("✅ Task 4 creada: ImplementationSpecialist")
        
        # Task 5: Síntesis final (depende de todas)
        task5 = Task(
            description=f"Genera reporte ejecutivo sobre '{niche}' integrando todos los análisis previos. Formato: markdown profesional de 15-25 páginas.",
            agent=agents[4],
            expected_output="Reporte completo en markdown",
            context=[task1, task2, task3, task4]
        )
        tasks.append(task5)
        logger.info("✅ Task 5 creada: ContentSynthesizer")
        
        # Crear Crew
        crew = Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=True,
            max_rpm=10  # Limitar RPM para evitar rate limits
        )
        
        logger.info("✅ Crew configurado",
                   agents=len(agents),
                   tasks=len(tasks),
                   process="sequential")
        
        # 5. Ejecutar pipeline
        logger.info("📋 PASO 5/6: EJECUTANDO PIPELINE")
        logger.info("⏱️  Tiempo estimado: 53-63 minutos")
        logger.info("💰 Costo estimado: 1-2.33 créditos")
        logger.info("-" * 80)
        
        # Ejecutar con timeout
        result = crew.kickoff()
        
        logger.info("-" * 80)
        logger.info("✅ Pipeline completado!")
        
        # 6. Guardar resultado
        logger.info("📋 PASO 6/6: Guardando resultado")
        
        output_dir = Path("outputs")
        output_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"e2e_test_{timestamp}.md"
        output_path = output_dir / filename
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"# Análisis: {niche}\n\n")
            f.write(f"**Fecha**: {datetime.now().isoformat()}\n\n")
            f.write(f"**Duración**: {(datetime.now() - start_time).total_seconds():.1f} segundos\n\n")
            f.write("---\n\n")
            f.write(str(result))
        
        logger.info("✅ Resultado guardado", path=str(output_path))
        
        # Resumen final
        duration = (datetime.now() - start_time).total_seconds()
        logger.info("=" * 80)
        logger.info("🎉 TEST END-TO-END COMPLETADO",
                   duration_seconds=duration,
                   duration_minutes=duration/60,
                   output=str(output_path))
        
        # Ver budget usado
        final_status = budget_manager.get_status()
        logger.info("💰 Budget usado",
                   used=final_status.monthly_limit - final_status.available,
                   remaining=final_status.available)
        
        return True
        
    except KeyboardInterrupt:
        logger.warning("⚠️  Test interrumpido por usuario")
        return False
        
    except Exception as e:
        logger.error("❌ Error en test E2E",
                    error=str(e),
                    error_type=type(e).__name__)
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n")
    print("=" * 80)
    print("ARA FRAMEWORK - TEST END-TO-END CON MONITOREO")
    print("=" * 80)
    print("\n")
    
    success = asyncio.run(test_e2e())
    
    sys.exit(0 if success else 1)
