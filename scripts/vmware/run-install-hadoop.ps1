[CmdletBinding()]
param(
    [string]$VmxPath = "D:\courses\AraBigData\docker-hadoop\kali-linux-2026.2-vmware-amd64.vmwarevm\kali-linux-2026.2-vmware-amd64.vmx"
)

$ErrorActionPreference = "Stop"
$Vmrun = "C:\Program Files\VMware\VMware Workstation\vmrun.exe"
if (-not (Test-Path $Vmrun)) {
    $Vmrun = "C:\Program Files (x86)\VMware\VMware Workstation\vmrun.exe"
}

$InstallScriptHost = Join-Path $PSScriptRoot "install-hadoop-kali.sh"
$TempHostScript = Join-Path $PSScriptRoot "install-hadoop-kali-lf.sh"

Write-Host "--> Normalizing line endings to LF..." -ForegroundColor Cyan
$Content = [System.IO.File]::ReadAllText($InstallScriptHost)
$ContentLF = $Content -replace "`r`n", "`n"
[System.IO.File]::WriteAllText($TempHostScript, $ContentLF)

try {
    Write-Host "--> Copying installer script to Kali VM (/home/kali/install-hadoop-kali.sh)..." -ForegroundColor Cyan
    & $Vmrun -T ws -gu kali -gp kali copyFileFromHostToGuest $VmxPath $TempHostScript "/home/kali/install-hadoop-kali.sh"

    Write-Host "--> Launching Hadoop installation inside Kali VM..." -ForegroundColor Cyan
    & $Vmrun -T ws -gu kali -gp kali runProgramInGuest $VmxPath /bin/bash -c "chmod +x /home/kali/install-hadoop-kali.sh; /home/kali/install-hadoop-kali.sh > /home/kali/install_hadoop.log 2>&1"

    Write-Host "--> Retrieving execution log from Kali VM..." -ForegroundColor Cyan
    $LocalLog = Join-Path $PSScriptRoot "install_hadoop.log"
    & $Vmrun -T ws -gu kali -gp kali copyFileFromGuestToHost $VmxPath "/home/kali/install_hadoop.log" $LocalLog

    if (Test-Path $LocalLog) {
        Write-Host "=== Kali Hadoop Installer Output ===" -ForegroundColor Green
        Get-Content $LocalLog
    }
}
finally {
    Remove-Item $TempHostScript -Force -ErrorAction SilentlyContinue
}
