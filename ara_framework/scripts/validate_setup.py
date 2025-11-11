"""
Script de validación para verificar que el entorno está correctamente configurado.
Ejecutar después de setup.ps1
"""

import sys
import importlib
import subprocess
from pathlib import Path
from typing import List, Tuple

def print_header(text: str) -> None:
    """Imprime un header formateado."""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def check_python_version() -> bool:
    """Verifica que Python sea 3.11+"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} (se requiere 3.11+)")
        return False

def check_package(package_name: str, import_name: str = None) -> bool:
    """Verifica que un paquete esté instalado."""
    if import_name is None:
        import_name = package_name
    
    try:
        module = importlib.import_module(import_name)
        version = getattr(module, "__version__", "unknown")
        print(f"✅ {package_name}: {version}")
        return True
    except ImportError:
        print(f"❌ {package_name}: no instalado")
        return False

def check_playwright_browsers() -> bool:
    """Verifica que los browsers de Playwright estén instalados."""
    try:
        result = subprocess.run(
            ["playwright", "install", "--dry-run"],
            capture_output=True,
            text=True
        )
        if "chromium" in result.stdout.lower():
            print("✅ Playwright browsers instalados")
            return True
        else:
            print("❌ Playwright browsers no instalados")
            return False
    except FileNotFoundError:
        print("❌ Playwright CLI no encontrado")
        return False

def check_env_file() -> Tuple[bool, List[str]]:
    """Verifica que el archivo .env exista y tenga las keys necesarias."""
    env_path = Path(".env")
    if not env_path.exists():
        print("❌ Archivo .env no encontrado")
        return False, []
    
    required_keys = ["OPENAI_API_KEY"]
    missing_keys = []
    
    with open(env_path, "r") as f:
        content = f.read()
        for key in required_keys:
            if key not in content or f"{key}=your_" in content or f"{key}=" == content:
                missing_keys.append(key)
    
    if missing_keys:
        print(f"⚠️  Archivo .env existe pero faltan keys: {', '.join(missing_keys)}")
        return False, missing_keys
    else:
        print("✅ Archivo .env configurado correctamente")
        return True, []

def check_directories() -> bool:
    """Verifica que los directorios necesarios existan."""
    required_dirs = [
        "agents",
        "mcp_servers",
        "tools",
        "config",
        "tests",
        "outputs",
        "docs"
    ]
    
    all_exist = True
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"✅ {dir_name}/")
        else:
            print(f"❌ {dir_name}/ no encontrado")
            all_exist = False
    
    return all_exist

def main() -> int:
    """Función principal de validación."""
    print("\n🔍 Validando configuración del Marco ARA...\n")
    
    all_checks_passed = True
    
    # 1. Python version
    print_header("1. Verificando Python")
    if not check_python_version():
        all_checks_passed = False
    
    # 2. Core packages
    print_header("2. Verificando Paquetes Core")
    core_packages = [
        ("crewai", "crewai"),
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"),
        ("playwright", "playwright"),
        ("openai", "openai"),
        ("pydantic", "pydantic")
    ]
    
    for package, import_name in core_packages:
        if not check_package(package, import_name):
            all_checks_passed = False
    
    # 3. Development packages
    print_header("3. Verificando Paquetes de Desarrollo")
    dev_packages = [
        ("pytest", "pytest"),
        ("ruff", "ruff"),
        ("black", "black"),
        ("mypy", "mypy")
    ]
    
    for package, import_name in dev_packages:
        if not check_package(package, import_name):
            all_checks_passed = False
    
    # 4. Playwright browsers
    print_header("4. Verificando Playwright Browsers")
    if not check_playwright_browsers():
        all_checks_passed = False
    
    # 5. .env file
    print_header("5. Verificando Archivo .env")
    env_ok, missing_keys = check_env_file()
    if not env_ok:
        all_checks_passed = False
    
    # 6. Directory structure
    print_header("6. Verificando Estructura de Directorios")
    if not check_directories():
        all_checks_passed = False
    
    # Final summary
    print_header("RESUMEN")
    if all_checks_passed:
        print("✅ ¡Todas las verificaciones pasaron!")
        print("\n🚀 Estás listo para comenzar el desarrollo.")
        print("\nPróximos pasos:")
        print("  1. Leer docs/TASKS.md")
        print("  2. Comenzar con Fase 1: WebScraping MCP Server")
        print("  3. Ejecutar tests: pytest tests/ -v")
        return 0
    else:
        print("❌ Algunas verificaciones fallaron.")
        print("\n🔧 Acciones recomendadas:")
        print("  1. Ejecutar: .\\setup.ps1")
        print("  2. Editar .env y agregar OPENAI_API_KEY")
        print("  3. Ejecutar nuevamente: python scripts/validate_setup.py")
        return 1

if __name__ == "__main__":
    sys.exit(main())
