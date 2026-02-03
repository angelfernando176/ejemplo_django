# Activador automático para PowerShell
Write-Host "Activando entorno virtual Django..." -ForegroundColor Cyan

# Buscar y activar el entorno virtual
$venvPath = ".\venv_nuevo"
if (Test-Path $venvPath) {
    & "$venvPath\Scripts\Activate.ps1"
    Write-Host "Entorno virtual activado: $venvPath" -ForegroundColor Green
} else {
    # Buscar cualquier venv
    $venvs = Get-ChildItem -Path . -Filter "python.exe" -Recurse | Where-Object {$_.DirectoryName -like "*venv*"} | Select-Object -First 1
    if ($venvs) {
        $venvDir = Split-Path (Split-Path $venvs.FullName)
        & "$venvDir\Scripts\Activate.ps1"
        Write-Host "Entorno virtual activado: $venvDir" -ForegroundColor Green
    } else {
        Write-Host " No se encontró entorno virtual" -ForegroundColor Red
    }
}

# Mostrar información
python --version
python -c "import django; print(f'Django {django.__version__}')"
Write-Host "`nEjecutar servidor: python manage.py runserver" -ForegroundColor Yellow
