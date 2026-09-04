@echo off
title Launch Apache Hadoop Single-Node Cluster (Docker)
cd /d "%~dp0..\..\"

echo =================================================================
echo   🐘 Apache Hadoop 3.1.2 Docker Cluster - 1-Click Launcher
echo =================================================================
echo.

:: Verify Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker Engine / Docker Desktop does not appear to be running.
    echo Please start Docker Desktop and try running this script again.
    echo.
    pause
    exit /b 1
)

echo --> Starting Hadoop cluster containers in background...
docker compose up -d

if %errorlevel% neq 0 (
    echo [ERROR] Failed to start containers via docker compose.
    pause
    exit /b %errorlevel%
)

echo.
echo =================================================================
echo   ✅ Hadoop Cluster Started Successfully!
echo =================================================================
echo.
echo   Web Consoles:
echo     - HDFS NameNode:          http://localhost:9870
echo     - YARN ResourceManager:   http://localhost:8088
echo     - HDFS DataNode:          http://localhost:9864
echo     - MapReduce JobHistory:   http://localhost:19888
echo.
echo   SSH Access:
echo     ssh -p 22222 hduser@localhost  (password: ubuntu)
echo.
echo =================================================================
docker compose ps
echo.
pause
