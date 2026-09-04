@echo off
setlocal enabledelayedexpansion
title Apache Hadoop - Google Cloud Launcher

echo ==========================================================
echo    Apache Hadoop - Google Cloud Platform Orchestrator
echo ==========================================================
echo  Select Deployment Option:
echo.
echo  [1] Create Ephemeral Dataproc Cluster (Hadoop 3 + Component Gateway)
echo  [2] Submit Python Streaming WordCount Job to Dataproc
echo  [3] Submit Java Native MapReduce Pi Job to Dataproc
echo  [4] Delete / Teardown Dataproc Cluster (Save Cloud Costs)
echo  [5] Deploy Containerized Docker Hadoop to Compute Engine (GCE)
echo  [6] Open Dataproc Console in Web Browser
echo  [7] Exit
echo.
set /p OPT="Enter selection [1-7]: "

if "%OPT%"=="1" (
    echo.
    echo Starting Dataproc cluster creation...
    bash scripts/gcp/create-dataproc-cluster.sh
    pause
    exit /b
)
if "%OPT%"=="2" (
    echo.
    echo Submitting Python Streaming MapReduce job to Dataproc...
    bash scripts/gcp/submit-mapreduce-job.sh streaming
    pause
    exit /b
)
if "%OPT%"=="3" (
    echo.
    echo Submitting Java MapReduce Pi job to Dataproc...
    bash scripts/gcp/submit-mapreduce-job.sh java
    pause
    exit /b
)
if "%OPT%"=="4" (
    echo.
    echo Tearing down Dataproc cluster...
    bash scripts/gcp/teardown-dataproc-cluster.sh
    pause
    exit /b
)
if "%OPT%"=="5" (
    echo.
    echo Deploying Docker Hadoop cluster to Google Compute Engine (GCE)...
    bash scripts/gcp/deploy-hadoop-gce.sh
    pause
    exit /b
)
if "%OPT%"=="6" (
    echo.
    echo Opening Google Cloud Dataproc Console...
    start https://console.cloud.google.com/dataproc/clusters
    exit /b
)

echo Exiting.
