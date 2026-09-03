@echo off
title Hyper-V Eject ISO and Enable Clipboard & Full Screen
cd /d "%~dp0"

:: Request Administrator Elevation
net session >nul 2>&1
if %errorLevel% == 0 (
    goto :run_script
) else (
    echo Requesting Administrator privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:run_script
echo =================================================================
echo   Ejecting Installation ISO & Enabling Enhanced Session Mode...
echo =================================================================
powershell -ExecutionPolicy Bypass -File "%~dp0scripts\configure-hyperv-host-enhanced-session.ps1"
pause
