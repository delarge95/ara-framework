"""
Test E2E con monitoreo en tiempo real
======================================
Muestra progreso cada 30 segundos para detectar cuelgues
"""

import os
import sys
import time
import threading
from datetime import datetime
from pathlib import Path

# Agregar directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

from core.pipeline import run_analysis_sync, PipelineStatus

# Variables globales para monitoreo
last_activity = datetime.now()
activity_log = []
is_running = True

def log_activity(message):
    """Registra actividad para detectar cuelgues"""
    global last_activity, activity_log
    last_activity = datetime.now()
    timestamp = last_activity.strftime("%H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    activity_log.append(log_entry)
    print(log_entry)

def monitor_thread():
    """Thread que monitorea si el proceso se cuelga"""
    global last_activity, is_running
    
    while is_running:
        time.sleep(30)  # Revisa cada 30 segundos
        
        if not is_running:
            break
            
        elapsed = (datetime.now() - last_activity).total_seconds()
        
        if elapsed > 180:  # 3 minutos sin actividad
            print(f"\n!!! WARNING: No hay actividad desde hace {int(elapsed)} segundos !!!")
            print(f"    Ultima actividad: {last_activity.strftime('%H:%M:%S')}")
            print(f"    Puede estar colgado o procesando algo muy largo")
        elif elapsed > 60:
            print(f"\n... Esperando respuesta (sin actividad por {int(elapsed)}s) ...")

def run_test():
    """Ejecuta el test con monitoreo"""
    global is_running
    
    try:
        log_activity("=== INICIO TEST E2E CON MONITOREO ===")
        log_activity(f"Niche: Rust WebAssembly for real-time audio processing")
        log_activity(f"Duracion estimada: 53-63 minutos")
        log_activity(f"Monitoreo: Alertas cada 3 min sin actividad\n")
        
        # Iniciar thread de monitoreo
        monitor = threading.Thread(target=monitor_thread, daemon=True)
        monitor.start()
        log_activity("Monitor de cuelgues iniciado (alerta cada 3 min)\n")
        
        # Ejecutar análisis
        log_activity("[1/6] Iniciando run_analysis_sync()...")
        log_activity("      (Este paso puede tardar 2-5 min en iniciar)")
        
        start_time = time.time()
        result = run_analysis_sync(niche="Rust WebAssembly for real-time audio processing")
        elapsed_minutes = (time.time() - start_time) / 60
        
        log_activity(f"\n[3/6] Crew finalizado en {elapsed_minutes:.1f} minutos")
        
        # Mostrar resultado
        log_activity(f"[4/6] Status: {result.status}")
        log_activity(f"[5/6] Creditos usados: {result.total_credits_used}")
        
        if result.status == PipelineStatus.COMPLETED:
            log_activity(f"[6/6] Output guardado en: {result.output_path}")
            log_activity("\n=== TEST EXITOSO ===")
            return 0
        else:
            log_activity(f"\n!!! TEST FALLIDO !!!")
            log_activity(f"Errores: {len(result.agent_results)}")
            for agent_res in result.agent_results:
                if agent_res.status != "success":
                    log_activity(f"  - {agent_res.agent_name}: {agent_res.error}")
            return 1
            
    except KeyboardInterrupt:
        log_activity("\n\n=== TEST CANCELADO POR USUARIO ===")
        return 2
    except Exception as e:
        log_activity(f"\n!!! ERROR INESPERADO !!!")
        log_activity(f"Tipo: {type(e).__name__}")
        log_activity(f"Mensaje: {str(e)}")
        import traceback
        log_activity(f"\nTraceback completo:")
        log_activity(traceback.format_exc())
        return 1
    finally:
        is_running = False
        
        # Guardar log
        log_file = f"outputs/test_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        os.makedirs("outputs", exist_ok=True)
        with open(log_file, "w", encoding="utf-8") as f:
            f.write("\n".join(activity_log))
        print(f"\nLog guardado en: {log_file}")

if __name__ == "__main__":
    print("\n" + "="*70)
    print("TEST E2E CON MONITOREO DE CUELGUES")
    print("="*70)
    print("\nCaracteristicas:")
    print("  - Muestra progreso cada 30 segundos")
    print("  - Alerta si no hay actividad por 3 minutos")
    print("  - Guarda log completo al finalizar")
    print("  - Presiona Ctrl+C para cancelar\n")
    print("="*70 + "\n")
    
    time.sleep(2)  # Pausa para que el usuario lea
    
    exit_code = run_test()
    sys.exit(exit_code)
