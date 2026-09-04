@echo off
title Launching Kali Linux in VMware Workstation (Tuned for Big Data & Hadoop)
cd /d "%~dp0"

echo =================================================================
echo   🚀 Preparing & Launching Kali Linux in VMware Workstation       
echo =================================================================

:: 1. Run PowerShell VMX Optimizer
powershell -ExecutionPolicy Bypass -File "%~dp0scripts\optimize-kali-vmx.ps1"
if %errorlevel% neq 0 (
    echo [ERROR] Optimization script encountered an error.
    pause
    exit /b %errorlevel%
)

:: 2. Locate VMware Workstation Executable
set "VMWARE_EXE=C:\Program Files\VMware\VMware Workstation\vmware.exe"
if not exist "%VMWARE_EXE%" (
    set "VMWARE_EXE=C:\Program Files (x86)\VMware\VMware Workstation\vmware.exe"
)

if not exist "%VMWARE_EXE%" (
    echo [ERROR] VMware Workstation executable could not be found.
    echo Please ensure VMware Workstation is installed.
    pause
    exit /b 1
)

set "VMX_FILE=%~dp0kali-linux-2026.2-vmware-amd64.vmwarevm\kali-linux-2026.2-vmware-amd64.vmx"

echo --> Launching VMware Workstation with Kali Linux...
echo --> VM File: %VMX_FILE%
echo.
echo [NOTE] On first boot, if VMware prompts "Did you move it or copy it?",
echo        select "I copied it" (or "I moved it").
echo.
start "" "%VMWARE_EXE%" "%VMX_FILE%"

echo =================================================================
echo   ✅ Kali Linux VM launched in VMware Workstation!
echo   Default Credentials:
echo     Username: kali
echo     Password: kali
echo =================================================================
timeout /t 5
