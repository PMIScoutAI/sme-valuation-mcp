Param(
    [switch]$NoVenv
)

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

if (-not $NoVenv) {
    if (-not (Test-Path ".venv\Scripts\python.exe")) {
        Write-Host "[setup] Creo virtualenv..."
        python -m venv .venv
    }

    Write-Host "[setup] Attivo venv e installo dipendenze..."
    & .\.venv\Scripts\python.exe -m pip install -r requirements.txt
    Write-Host "[run] Avvio server MCP..."
    & .\.venv\Scripts\python.exe -m src.mcp_server
    exit $LASTEXITCODE
}

Write-Host "[run] Avvio server MCP con python di sistema..."
python -m src.mcp_server
exit $LASTEXITCODE
