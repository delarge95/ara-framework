# Script para ejecutar test E2E en background con monitoreo
# Uso: .\run_e2e_background.ps1

$ErrorActionPreference = "Stop"

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$logFile = "outputs\e2e_test_$timestamp.log"
$pidFile = "outputs\e2e_test.pid"

Write-Host ""
Write-Host "=" -NoNewline; Write-Host ("=" * 79)
Write-Host "🚀 EJECUTANDO TEST END-TO-END EN BACKGROUND"
Write-Host "=" -NoNewline; Write-Host ("=" * 79)
Write-Host ""

# Activar venv y ejecutar
Write-Host "📁 Archivo de log: $logFile"
Write-Host "📋 Archivo de PID: $pidFile"
Write-Host ""

# Crear directorio outputs si no existe
if (-not (Test-Path "outputs")) {
    New-Item -ItemType Directory -Path "outputs" | Out-Null
}

# Ejecutar en background y redirigir salida
Write-Host "🔄 Iniciando proceso..."
$process = Start-Process -FilePath ".\.venv_py312\Scripts\python.exe" `
    -ArgumentList "test_e2e_monitored.py" `
    -WorkingDirectory $PSScriptRoot `
    -RedirectStandardOutput $logFile `
    -RedirectStandardError "$logFile.err" `
    -PassThru `
    -WindowStyle Hidden

# Guardar PID
$process.Id | Out-File -FilePath $pidFile -Encoding ASCII

Write-Host "✅ Proceso iniciado (PID: $($process.Id))"
Write-Host ""
Write-Host "📊 COMANDOS DE MONITOREO:"
Write-Host ""
Write-Host "   Ver progreso en tiempo real:"
Write-Host "   Get-Content '$logFile' -Wait -Tail 20"
Write-Host ""
Write-Host "   Ver últimas 50 líneas:"
Write-Host "   Get-Content '$logFile' -Tail 50"
Write-Host ""
Write-Host "   Verificar si sigue ejecutando:"
Write-Host "   Get-Process -Id $($process.Id) -ErrorAction SilentlyContinue"
Write-Host ""
Write-Host "   Detener proceso:"
Write-Host "   Stop-Process -Id $($process.Id) -Force"
Write-Host ""
Write-Host "=" -NoNewline; Write-Host ("=" * 79)
Write-Host ""

# Monitoreo inicial (primeros 30 segundos)
Write-Host "👀 Monitoreando inicio (primeros 30 segundos)..."
Write-Host ""

$monitorStart = Get-Date
$monitorDuration = 30

while (((Get-Date) - $monitorStart).TotalSeconds -lt $monitorDuration) {
    Start-Sleep -Seconds 5
    
    # Verificar si el proceso sigue vivo
    $processAlive = Get-Process -Id $process.Id -ErrorAction SilentlyContinue
    
    if (-not $processAlive) {
        Write-Host ""
        Write-Host "⚠️  Proceso terminó antes de tiempo!"
        Write-Host ""
        Write-Host "📄 Últimas líneas del log:"
        Write-Host ""
        if (Test-Path $logFile) {
            Get-Content $logFile -Tail 30
        }
        if (Test-Path "$logFile.err") {
            Write-Host ""
            Write-Host "❌ Errores:"
            Get-Content "$logFile.err"
        }
        exit 1
    }
    
    # Mostrar últimas líneas
    if (Test-Path $logFile) {
        $lines = Get-Content $logFile -Tail 5
        if ($lines) {
            Clear-Host
            Write-Host "⏱️  Monitoreando ($([int]((Get-Date) - $monitorStart).TotalSeconds)s / ${monitorDuration}s)"
            Write-Host ""
            $lines | ForEach-Object { Write-Host $_ }
        }
    }
}

Write-Host ""
Write-Host "=" -NoNewline; Write-Host ("=" * 79)
Write-Host "✅ Proceso ejecutándose correctamente en background"
Write-Host "=" -NoNewline; Write-Host ("=" * 79)
Write-Host ""
Write-Host "⏱️  Tiempo estimado total: 53-63 minutos"
Write-Host "💰 Costo estimado: 1-2.33 créditos (~`$0.05-`$0.12)"
Write-Host ""
Write-Host "Para ver el progreso en tiempo real, ejecuta:"
Write-Host "   Get-Content '$logFile' -Wait -Tail 20"
Write-Host ""
