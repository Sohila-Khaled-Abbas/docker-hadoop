@echo off
title Unfreeze WSL2 & Restart Docker Desktop
cd /d "%~dp0..\..\"

echo =================================================================
echo   🔄 WSL2 & Docker Desktop Engine Recovery Utility
echo =================================================================
echo.

:: Request Administrator Elevation
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Requesting Administrator privileges to restart WSL Service...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

echo --> Terminating hung Docker and WSL client processes...
taskkill /IM docker.exe /F >nul 2>&1
taskkill /IM docker-compose.exe /F >nul 2>&1
taskkill /IM "Docker Desktop.exe" /F >nul 2>&1
taskkill /IM com.docker.backend.exe /F >nul 2>&1
taskkill /IM com.docker.build.exe /F >nul 2>&1
taskkill /IM wsl.exe /F >nul 2>&1

echo --> Restarting Windows WSL Service (wslservice)...
net stop wslservice
net start wslservice

echo --> Restarting Docker Desktop Service (com.docker.service)...
net start com.docker.service >nul 2>&1

echo --> Launching Docker Desktop...
start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"

echo.
echo =================================================================
echo   ✅ WSL2 and Docker Desktop have been reset successfully!
echo   Wait 15-30 seconds for Docker Desktop to reach green 'Running' state,
echo   then run: launchers\windows\Start-Hadoop-Docker.bat
echo =================================================================
timeout /t 5
