# ejecutar.ps1 - Script para iniciar tu proyecto fácilmente
Write-Host "=== INICIADOR DE PROYECTO DJANGO/FLASK ===" -ForegroundColor Cyan

# Preguntar qué proyecto ejecutar
Write-Host "`n¿Qué proyecto quieres ejecutar?" -ForegroundColor Yellow
Write-Host "1. Django (http://127.0.0.1:8000)" -ForegroundColor Green
Write-Host "2. Flask (http://127.0.0.1:5000)" -ForegroundColor Blue
$opcion = Read-Host "Selecciona (1 o 2)"

# Activar entorno virtual
Write-Host "`nActivando entorno virtual..." -ForegroundColor Yellow
if (Test-Path ".\venv\Scripts\Activate.ps1") {
    .\venv\Scripts\Activate.ps1
    Write-Host "✅ Entorno virtual activado" -ForegroundColor Green
} else {
    Write-Host "❌ No se encontró el entorno virtual" -ForegroundColor Red
    exit
}

# Ejecutar según opción
switch ($opcion) {
    "1" {
        Write-Host "`n=== INICIANDO DJANGO ===" -ForegroundColor Green
        
        # Verificar que estamos en la carpeta correcta
        if (Test-Path "manage.py") {
            Write-Host "✅ Encontrado manage.py" -ForegroundColor Green
        } else {
            Write-Host "❌ No se encontró manage.py. Buscando..." -ForegroundColor Red
            
            # Buscar manage.py en subcarpetas
            $managePath = Get-ChildItem -Path . -Filter "manage.py" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
            if ($managePath) {
                Write-Host "✅ Encontrado en: $($managePath.DirectoryName)" -ForegroundColor Green
                cd $managePath.DirectoryName
            } else {
                Write-Host "❌ No se encontró manage.py en ningún lado" -ForegroundColor Red
                Write-Host "   Asegúrate de estar en la carpeta del proyecto Django" -ForegroundColor Yellow
                exit
            }
        }
        
        # Verificar migraciones
        Write-Host "`nVerificando base de datos..." -ForegroundColor Yellow
        python manage.py check
        
        # Preguntar si ejecutar migraciones
        $hacerMigraciones = Read-Host "¿Ejecutar migraciones? (s/n)"
        if ($hacerMigraciones -eq "s") {
            python manage.py makemigrations
            python manage.py migrate
        }
        
        # Iniciar servidor
        Write-Host "`n=== INICIANDO SERVIDOR ===" -ForegroundColor Green
        Write-Host "Servidor disponible en: http://127.0.0.1:8000/" -ForegroundColor Cyan
        Write-Host "Admin panel: http://127.0.0.1:8000/admin/" -ForegroundColor Cyan
        Write-Host "Presiona Ctrl+C para detener" -ForegroundColor Yellow
        python manage.py runserver
    }
    
    "2" {
        Write-Host "`n=== INICIANDO FLASK ===" -ForegroundColor Blue
        
        # Buscar app.py
        if (Test-Path "app.py") {
            Write-Host "✅ Encontrado app.py" -ForegroundColor Green
        } else {
            $appPath = Get-ChildItem -Path . -Filter "app.py" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
            if ($appPath) {
                Write-Host "✅ Encontrado en: $($appPath.DirectoryName)" -ForegroundColor Green
                cd $appPath.DirectoryName
            } else {
                Write-Host "❌ No se encontró app.py" -ForegroundColor Red
                exit
            }
        }
        
        # Configurar Flask
        $env:FLASK_APP = "app.py"
        $env:FLASK_ENV = "development"
        
        # Iniciar servidor
        Write-Host "`n=== INICIANDO SERVIDOR ===" -ForegroundColor Green
        Write-Host "Servidor disponible en: http://127.0.0.1:5000/" -ForegroundColor Cyan
        Write-Host "Presiona Ctrl+C para detener" -ForegroundColor Yellow
        flask run --debug
    }
    
    default {
        Write-Host "❌ Opción no válida" -ForegroundColor Red
    }
}