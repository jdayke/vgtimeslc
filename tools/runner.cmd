@echo off
echo started %date% %time% > "%~dp0jobs\_cmd_started.txt"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0runner.ps1" 2> "%~dp0jobs\_runner_error.txt"
echo exited %errorlevel% >> "%~dp0jobs\_cmd_started.txt"
pause
