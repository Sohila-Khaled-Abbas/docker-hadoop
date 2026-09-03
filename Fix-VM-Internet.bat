@echo off
title Fix Hyper-V VM Internet Connection
cd /d "%~dp0"

:: Request Administrator Elevation
net session >nul 2>&1
if %errorLevel% == 0 (
    goto :run_script
) else (
    echo Requesting Administrator privileges to configure Hyper-V network...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:run_script
echo =================================================================
echo   Connecting Ubuntu VM to Default Switch (NAT Internet)...
echo =================================================================
powershell -ExecutionPolicy Bypass -File "%~dp0scripts\fix-vm-internet.ps1"
pause
