# ⚡ Script de Inicio Rápido para el Marco ARA

Write-Host "🚀 Iniciando setup del Marco ARA..." -ForegroundColor Cyan
Write-Host ""

# Verificar Python
Write-Host "📌 Verificando Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($pythonVersion -match "Python 3\.11" -or $pythonVersion -match "Python 3\.12") {
    Write-Host "✅ $pythonVersion detectado" -ForegroundColor Green
} else {
    Write-Host "❌ Python 3.11+ es requerido. Versión actual: $pythonVersion" -ForegroundColor Red
    exit 1
}

# Crear entorno virtual
Write-Host ""
Write-Host "📦 Creando entorno virtual..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "⚠️  Entorno virtual ya existe. Eliminando..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force venv
}

python -m venv venv
Write-Host "✅ Entorno virtual creado" -ForegroundColor Green

# Activar entorno virtual
Write-Host ""
Write-Host "🔌 Activando entorno virtual..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host ""
Write-Host "⬆️  Actualizando pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet

# Instalar dependencias
Write-Host ""
Write-Host "📥 Instalando dependencias principales..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet

Write-Host ""
Write-Host "📥 Instalando dependencias de desarrollo..." -ForegroundColor Yellow
pip install -r requirements-dev.txt --quiet

# Instalar Playwright
Write-Host ""
Write-Host "🎭 Instalando Playwright browsers..." -ForegroundColor Yellow
playwright install chromium

# Crear .env si no existe
Write-Host ""
if (-not (Test-Path ".env")) {
    Write-Host "📝 Creando archivo .env desde template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "⚠️  IMPORTANTE: Edita .env y agrega tu OPENAI_API_KEY" -ForegroundColor Red
} else {
    Write-Host "✅ Archivo .env ya existe" -ForegroundColor Green
}

# Crear directorios de output si no existen
Write-Host ""
Write-Host "📁 Verificando directorios de output..." -ForegroundColor Yellow
$outputDirs = @("outputs/theses", "outputs/assets", "outputs/reports", "outputs/logs")
foreach ($dir in $outputDirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "  ✅ Creado: $dir" -ForegroundColor Green
    }
}

# Verificar instalación
Write-Host ""
Write-Host "🔍 Verificando instalación..." -ForegroundColor Yellow

$packages = @("crewai", "fastapi", "playwright", "openai")
foreach ($package in $packages) {
    $installed = pip show $package 2>$null
    if ($installed) {
        $version = ($installed | Select-String "Version:").ToString().Split(":")[1].Trim()
        Write-Host "  ✅ $package $version" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $package no instalado" -ForegroundColor Red
    }
}

# Resumen final
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "✨ Setup completado exitosamente!" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Próximos pasos:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  1️⃣  Editar .env y agregar tu OPENAI_API_KEY:" -ForegroundColor White
Write-Host "     notepad .env" -ForegroundColor Gray
Write-Host ""
Write-Host "  2️⃣  Activar el entorno virtual (en nuevas terminales):" -ForegroundColor White
Write-Host "     .\venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host ""
Write-Host "  3️⃣  Ejecutar tests:" -ForegroundColor White
Write-Host "     pytest tests/ -v" -ForegroundColor Gray
Write-Host ""
Write-Host "  4️⃣  Iniciar un MCP Server:" -ForegroundColor White
Write-Host "     cd mcp_servers/webscraping" -ForegroundColor Gray
Write-Host "     uvicorn server:app --port 8001 --reload" -ForegroundColor Gray
Write-Host ""
Write-Host "  5️⃣  Leer documentación:" -ForegroundColor White
Write-Host "     - docs/PROJECT_CONSTITUTION.md" -ForegroundColor Gray
Write-Host "     - docs/PROJECT_SPEC.md" -ForegroundColor Gray
Write-Host "     - docs/TECHNICAL_PLAN.md" -ForegroundColor Gray
Write-Host "     - docs/TASKS.md" -ForegroundColor Gray
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""
Write-Host "🚀 ¡Listo para comenzar el desarrollo!" -ForegroundColor Green
Write-Host ""
