"""
Ejecuta el test E2E importando el modulo de Python compatible
Evita problemas de importacion ejecutando en un proceso separado
"""

import subprocess
import sys
import time
import threading
from datetime import datetime

# Variables globales para monitoreo
last_output_time = datetime.now()
output_lines = []
is_running = True

def monitor_thread():
    """Thread que monitorea si el proceso se cuelga"""
    global last_output_time, is_running
    
    while is_running:
        time.sleep(30)  # Revisa cada 30 segundos
        
        if not is_running:
            break
            
        elapsed = (datetime.now() - last_output_time).total_seconds()
        
        if elapsed > 180:  # 3 minutos sin output
            print(f"\n!!! WARNING: No hay output desde hace {int(elapsed)} segundos !!!")
            print(f"    Ultimo output: {last_output_time.strftime('%H:%M:%S')}")
            print(f"    Puede estar colgado o procesando algo muy largo")
        elif elapsed > 60:
            print(f"\n... Esperando output (sin actividad por {int(elapsed)}s) ...")

def run_test():
    """Ejecuta el test en un subprocess"""
    global last_output_time, is_running, output_lines
    
    try:
        print("="*70)
        print("TEST E2E CON MONITOREO DE CUELGUES")
        print("="*70)
        print("\nCaracteristicas:")
        print("  - Muestra output en tiempo real")
        print("  - Alerta si no hay output por 3 minutos")
        print("  - Guarda log completo al finalizar")
        print("  - Presiona Ctrl+C para cancelar\n")
        print("="*70 + "\n")
        
        # Iniciar monitor
        monitor = threading.Thread(target=monitor_thread, daemon=True)
        monitor.start()
        
        # Ejecutar test_simple.py (que ya sabemos que funciona)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Iniciando test...")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Niche: Rust WebAssembly for real-time audio processing\n")
        
        process = subprocess.Popen(
            [sys.executable, "test_simple.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Leer output en tiempo real
        for line in iter(process.stdout.readline, ''):
            if line:
                last_output_time = datetime.now()
                timestamp = last_output_time.strftime("%H:%M:%S")
                output_line = f"[{timestamp}] {line.rstrip()}"
                print(output_line)
                output_lines.append(output_line)
        
        process.wait()
        
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Proceso finalizado con código: {process.returncode}")
        
        return process.returncode
        
    except KeyboardInterrupt:
        print("\n\n=== TEST CANCELADO POR USUARIO ===")
        if 'process' in locals():
            process.terminate()
        return 2
    except Exception as e:
        print(f"\n!!! ERROR INESPERADO !!!")
        print(f"Tipo: {type(e).__name__}")
        print(f"Mensaje: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        is_running = False
        
        # Guardar log
        log_file = f"outputs/test_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        import os
        os.makedirs("outputs", exist_ok=True)
        with open(log_file, "w", encoding="utf-8") as f:
            f.write("\n".join(output_lines))
        print(f"\nLog guardado en: {log_file}")

if __name__ == "__main__":
    exit_code = run_test()
    sys.exit(exit_code)
