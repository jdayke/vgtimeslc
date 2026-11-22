@echo off
echo started %date% %time% > "%~dp0jobs\_cmd_started.txt"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0watchdog.ps1"
echo exited %errorlevel% >> "%~dp0jobs\_cmd_started.txt"
pause
