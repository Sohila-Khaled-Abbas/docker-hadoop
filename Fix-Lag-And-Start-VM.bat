@echo off
title Optimizing Hyper-V Ubuntu VM & Fixing Lag
cd /d "%~dp0"

:: Request Administrator Elevation
net session >nul 2>&1
if %errorLevel% == 0 (
    goto :run_script
) else (
    echo Requesting Administrator privileges to configure Hyper-V VM...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:run_script
echo =================================================================
echo   Fixing Hyper-V Lag, Upgrading to 4 vCPUs, and Launching VM...
echo =================================================================
powershell -ExecutionPolicy Bypass -File "%~dp0scripts\optimize-hyperv-vm.ps1"
pause
