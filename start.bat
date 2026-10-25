@echo off
cd /d "%~dp0"
echo Pchelka: http://localhost:8000
where py >nul 2>nul
if %errorlevel%==0 (
  start "Pchelka" powershell -NoProfile -Command "Start-Sleep -Seconds 2; Start-Process 'http://localhost:8000'"
  py -3 server.py
  goto end
)
where python >nul 2>nul
if %errorlevel%==0 (
  start "Pchelka" powershell -NoProfile -Command "Start-Sleep -Seconds 2; Start-Process 'http://localhost:8000'"
  python server.py
  goto end
)
echo Python 3 was not found. Install it from https://www.python.org/downloads/
:end
pause
