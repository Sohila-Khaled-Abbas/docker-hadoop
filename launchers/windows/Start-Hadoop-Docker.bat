@echo off
title Launch Apache Hadoop & Spark Big Data Cluster (Docker)
cd /d "%~dp0..\..\"

echo =================================================================
echo   🐘 Unified Apache Hadoop & Spark Ecosystem - 1-Click Launcher
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

echo --> Starting Big Data cluster containers in background...
docker compose up -d

if %errorlevel% neq 0 (
    echo [ERROR] Failed to start containers via docker compose.
    pause
    exit /b %errorlevel%
)

echo.
echo =================================================================
echo   ✅ Big Data Engineering Cluster Started Successfully!
echo =================================================================
echo.
echo   🌐 Unified Big Data Control Hub (Single Pane of Glass):
echo       ==> http://localhost:3030
echo.
echo   Component Web Consoles:
echo     - Unified Control Hub:    http://localhost:3030
echo     - Spark Master UI:        http://localhost:8080
echo     - Spark Worker UI:        http://localhost:8081
echo     - Spark History Server:   http://localhost:18080
echo     - JupyterLab PySpark:     http://localhost:8888
echo     - HDFS NameNode UI:       http://localhost:9870
echo     - HDFS DataNode UI:       http://localhost:9864
echo     - YARN ResourceManager:   http://localhost:8088
echo     - MapReduce JobHistory:   http://localhost:19888
echo.
echo   Endpoints:
echo     - Spark Master RPC:       spark://localhost:7077
echo     - HDFS RPC Endpoint:      hdfs://localhost:9000
echo     - SSH Bastion:            ssh -p 22222 hduser@localhost  (password: ubuntu)
echo.
echo =================================================================
docker compose ps
echo.

:: Automatically open default browser to the Unified Control Hub
start http://localhost:3030

pause
