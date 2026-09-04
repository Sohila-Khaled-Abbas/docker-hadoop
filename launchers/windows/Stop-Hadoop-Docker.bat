@echo off
title Stop Apache Hadoop Single-Node Cluster (Docker)
cd /d "%~dp0..\..\"

echo =================================================================
echo   🛑 Stopping Apache Hadoop 3.1.2 Docker Cluster
echo =================================================================
echo.

docker compose down

echo.
echo =================================================================
echo   ✅ Hadoop Docker Cluster Stopped Gracefully.
echo   (Persistent volumes retained)
echo =================================================================
timeout /t 5
