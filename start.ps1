$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
Write-Host "Pchelka: http://localhost:8000 . No keys or .env file required."
$job = Start-Job { Start-Sleep -Seconds 2; Start-Process "http://localhost:8000" }
if (Get-Command py -ErrorAction SilentlyContinue) { py -3 server.py }
elseif (Get-Command python -ErrorAction SilentlyContinue) { python server.py }
else { throw "Python 3 is required. Install it from https://www.python.org/downloads/" }
