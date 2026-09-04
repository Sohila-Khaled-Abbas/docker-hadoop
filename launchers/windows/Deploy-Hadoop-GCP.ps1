<#
.SYNOPSIS
    Interactive Google Cloud Platform Hadoop / Dataproc Provisioner and Job Orchestrator.
.DESCRIPTION
    Automates deployment of Apache Hadoop clusters on Google Cloud Dataproc and Compute Engine,
    supports submitting MapReduce jobs, and cost-effective cluster lifecycle management.
#>
[CmdletBinding()]
param()

$Host.UI.RawUI.WindowTitle = "Apache Hadoop - Google Cloud Launcher (PowerShell)"

function Show-Header {
    Clear-Host
    Write-Host "==========================================================" -ForegroundColor Cyan
    Write-Host "   ☁️ Apache Hadoop - Google Cloud Platform Orchestrator   " -ForegroundColor Yellow
    Write-Host "==========================================================" -ForegroundColor Cyan
    Write-Host " Select Deployment Option:"
    Write-Host "  [1] Create Ephemeral Dataproc Cluster (Hadoop 3 + Component Gateway)" -ForegroundColor Green
    Write-Host "  [2] Submit Python Streaming WordCount Job to Dataproc" -ForegroundColor Green
    Write-Host "  [3] Submit Java Native MapReduce Pi Job to Dataproc" -ForegroundColor Green
    Write-Host "  [4] Delete / Teardown Dataproc Cluster (Save Cloud Costs)" -ForegroundColor Yellow
    Write-Host "  [5] Deploy Containerized Docker Hadoop to Compute Engine (GCE)" -ForegroundColor Cyan
    Write-Host "  [6] Open Dataproc Console in Web Browser" -ForegroundColor Magenta
    Write-Host "  [7] Exit" -ForegroundColor Red
    Write-Host ""
}

Show-Header
$selection = Read-Host "Enter selection [1-7]"

$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")

switch ($selection) {
    "1" {
        Write-Host "`n--> Starting Dataproc cluster creation..." -ForegroundColor Cyan
        & bash "$ProjectRoot/scripts/gcp/create-dataproc-cluster.sh"
        pause
    }
    "2" {
        Write-Host "`n--> Submitting Python Streaming MapReduce job to Dataproc..." -ForegroundColor Cyan
        & bash "$ProjectRoot/scripts/gcp/submit-mapreduce-job.sh" streaming
        pause
    }
    "3" {
        Write-Host "`n--> Submitting Java MapReduce Pi job to Dataproc..." -ForegroundColor Cyan
        & bash "$ProjectRoot/scripts/gcp/submit-mapreduce-job.sh" java
        pause
    }
    "4" {
        Write-Host "`n--> Tearing down Dataproc cluster..." -ForegroundColor Yellow
        & bash "$ProjectRoot/scripts/gcp/teardown-dataproc-cluster.sh"
        pause
    }
    "5" {
        Write-Host "`n--> Deploying Docker Hadoop cluster to Google Compute Engine (GCE)..." -ForegroundColor Cyan
        & bash "$ProjectRoot/scripts/gcp/deploy-hadoop-gce.sh"
        pause
    }
    "6" {
        Write-Host "`n--> Opening Google Cloud Dataproc Console..." -ForegroundColor Green
        Start-Process "https://console.cloud.google.com/dataproc/clusters"
    }
    default {
        Write-Host "`nExiting."
    }
}
