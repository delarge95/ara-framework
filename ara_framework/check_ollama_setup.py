"""
Diagnóstico Rápido - Verificar configuración de Ollama.

Este script verifica que todo está configurado correctamente antes de ejecutar
las pruebas completas de tool calling.

Uso:
    python check_ollama_setup.py
"""

import sys
import subprocess
import os
from pathlib import Path

print("\n" + "="*70)
print(" 🔍 DIAGNÓSTICO DE CONFIGURACIÓN OLLAMA")
print("="*70 + "\n")

checks_passed = 0
checks_total = 0

# ============================================================================
# CHECK 1: Python Version
# ============================================================================
checks_total += 1
print("✓ Check 1: Python Version")
python_version = sys.version_info
print(f"   Python {python_version.major}.{python_version.minor}.{python_version.micro}")
if python_version >= (3, 11):
    print("   ✅ PASS: Python 3.11+ requerido")
    checks_passed += 1
else:
    print("   ❌ FAIL: Se requiere Python 3.11 o superior")

# ============================================================================
# CHECK 2: langchain-ollama instalado
# ============================================================================
checks_total += 1
print("\n✓ Check 2: langchain-ollama package")
try:
    import langchain_ollama
    version = getattr(langchain_ollama, "__version__", "unknown")
    print(f"   Versión: {version}")
    print("   ✅ PASS: langchain-ollama instalado")
    checks_passed += 1
except ImportError:
    print("   ❌ FAIL: langchain-ollama no instalado")
    print("   Ejecuta: pip install langchain-ollama")

# ============================================================================
# CHECK 3: Directorio de modelos existe
# ============================================================================
checks_total += 1
print("\n✓ Check 3: Directorio de modelos")
models_path = Path(r"E:\modelos_ollama")
if models_path.exists():
    print(f"   Ruta: {models_path}")
    print(f"   ✅ PASS: Directorio existe")
    checks_passed += 1
    
    # Listar modelos si es posible
    try:
        models = list(models_path.glob("**/*"))
        print(f"   Archivos encontrados: {len(models)}")
    except Exception as e:
        print(f"   ⚠️  No se pudo listar contenido: {e}")
else:
    print(f"   Ruta: {models_path}")
    print("   ❌ FAIL: Directorio no existe")
    print("   Verifica que configuraste: set OLLAMA_MODELS=E:\\modelos_ollama")

# ============================================================================
# CHECK 4: Ollama ejecutable
# ============================================================================
checks_total += 1
print("\n✓ Check 4: Ollama ejecutable")
try:
    # Intentar ejecutar ollama --version
    result = subprocess.run(
        ["ollama", "--version"],
        capture_output=True,
        text=True,
        timeout=5
    )
    if result.returncode == 0:
        version = result.stdout.strip()
        print(f"   Versión: {version}")
        print("   ✅ PASS: Ollama accesible en PATH")
        checks_passed += 1
    else:
        print("   ❌ FAIL: Ollama ejecutable encontrado pero error al ejecutar")
        print(f"   Error: {result.stderr}")
except FileNotFoundError:
    print("   ❌ FAIL: 'ollama' no encontrado en PATH")
    print("   Solución 1: Ejecuta desde terminal donde funcionó 'ollama pull'")
    print("   Solución 2: Agrega Ollama al PATH de esta terminal")
except subprocess.TimeoutExpired:
    print("   ⚠️  TIMEOUT: Ollama no responde")

# ============================================================================
# CHECK 5: Ollama server respondiendo
# ============================================================================
checks_total += 1
print("\n✓ Check 5: Ollama server (HTTP API)")
try:
    import httpx
    response = httpx.get("http://localhost:11434/api/tags", timeout=5.0)
    if response.status_code == 200:
        data = response.json()
        models = data.get("models", [])
        print(f"   URL: http://localhost:11434")
        print(f"   Status: {response.status_code} OK")
        print(f"   Modelos disponibles: {len(models)}")
        
        # Buscar mistral
        mistral_found = False
        for model in models:
            name = model.get("name", "")
            if "mistral" in name.lower():
                print(f"   🎯 Mistral encontrado: {name}")
                mistral_found = True
        
        if mistral_found:
            print("   ✅ PASS: Ollama server respondiendo con Mistral")
            checks_passed += 1
        else:
            print("   ⚠️  PARTIAL: Server OK pero Mistral no listado")
            print("   Ejecuta: ollama pull mistral:7b")
    else:
        print(f"   ❌ FAIL: Server responde con status {response.status_code}")
except ImportError:
    print("   ⚠️  SKIP: httpx no instalado (no crítico)")
    print("   Para verificar API: pip install httpx")
except Exception as e:
    print(f"   ❌ FAIL: No se puede conectar con Ollama server")
    print(f"   Error: {type(e).__name__}: {e}")
    print("   Solución: Ejecuta 'ollama serve' en terminal separada")

# ============================================================================
# CHECK 6: Config settings.py
# ============================================================================
checks_total += 1
print("\n✓ Check 6: Configuración en settings.py")
try:
    # Intentar importar settings
    current_dir = Path(__file__).parent
    sys.path.insert(0, str(current_dir))
    from config.settings import settings
    
    print(f"   OLLAMA_BASE_URL: {settings.OLLAMA_BASE_URL}")
    print(f"   OLLAMA_MODEL: {settings.OLLAMA_MODEL}")
    print(f"   OLLAMA_MODELS_PATH: {settings.OLLAMA_MODELS_PATH}")
    print(f"   OLLAMA_NUM_CTX: {settings.OLLAMA_NUM_CTX}")
    print("   ✅ PASS: Configuración presente")
    checks_passed += 1
except ImportError as e:
    print(f"   ❌ FAIL: No se puede importar settings")
    print(f"   Error: {e}")
except AttributeError as e:
    print(f"   ❌ FAIL: Configuración OLLAMA_* no encontrada")
    print(f"   Error: {e}")

# ============================================================================
# RESUMEN
# ============================================================================
print("\n" + "="*70)
print(" 📊 RESUMEN")
print("="*70)
print(f"\nChecks pasados: {checks_passed}/{checks_total}")
print(f"Porcentaje: {(checks_passed/checks_total)*100:.1f}%\n")

if checks_passed == checks_total:
    print("✅✅✅ EXCELENTE: Todo configurado correctamente")
    print("\n🚀 Próximo paso:")
    print("   python test_ollama_mistral.py")
elif checks_passed >= checks_total - 1:
    print("⚠️ CASI LISTO: Falta un check menor")
    print("\n📋 Revisa los checks fallidos arriba")
    print("   Probablemente puedas ejecutar: python test_ollama_mistral.py")
elif checks_passed >= checks_total // 2:
    print("⚠️ CONFIGURACIÓN INCOMPLETA: Varios checks fallaron")
    print("\n📋 Problemas principales:")
    print("   1. Revisa que Ollama esté instalado")
    print("   2. Ejecuta: ollama serve (en terminal separada)")
    print("   3. Verifica: ollama list (debe mostrar mistral:7b)")
else:
    print("❌ CONFIGURACIÓN CRÍTICA FALTANTE")
    print("\n📋 Acciones requeridas:")
    print("   1. Instalar Ollama: https://ollama.com/download")
    print("   2. Descargar Mistral: ollama pull mistral:7b")
    print("   3. Instalar paquetes: pip install langchain-ollama httpx")
    print("   4. Iniciar server: ollama serve")
    print("   5. Re-ejecutar este script")

print("\n" + "="*70 + "\n")

# Exit code para automation
sys.exit(0 if checks_passed == checks_total else 1)
