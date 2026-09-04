# ==============================================================================
# Script: run-in-kali.ps1
# Runs any bash command or script inside the running Kali VM via VMware VIX API
# ==============================================================================
[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)]
    [string]$Command,
    [string]$VmxPath = "D:\courses\AraBigData\docker-hadoop\kali-linux-2026.2-vmware-amd64.vmwarevm\kali-linux-2026.2-vmware-amd64.vmx"
)

$ErrorActionPreference = "Stop"
$Vmrun = "C:\Program Files\VMware\VMware Workstation\vmrun.exe"
if (-not (Test-Path $Vmrun)) {
    $Vmrun = "C:\Program Files (x86)\VMware\VMware Workstation\vmrun.exe"
}

# Write command to local temp script
$LocalScript = Join-Path $PSScriptRoot "temp_guest_cmd.sh"
$ScriptText = "#!/usr/bin/env bash`n" + $Command + "`n"
$ScriptText = $ScriptText -replace "`r`n", "`n"
[System.IO.File]::WriteAllText($LocalScript, $ScriptText)

try {
    # Copy to guest
    & $Vmrun -T ws -gu kali -gp kali copyFileFromHostToGuest $VmxPath $LocalScript "/tmp/temp_guest_cmd.sh"

    # Execute in guest and capture output
    & $Vmrun -T ws -gu kali -gp kali runProgramInGuest $VmxPath /bin/bash -c "chmod +x /tmp/temp_guest_cmd.sh; /tmp/temp_guest_cmd.sh > /tmp/temp_guest_cmd.out 2>&1"

    # Copy output back
    $LocalOut = Join-Path $PSScriptRoot "temp_guest_cmd.out"
    & $Vmrun -T ws -gu kali -gp kali copyFileFromGuestToHost $VmxPath "/tmp/temp_guest_cmd.out" $LocalOut

    if (Test-Path $LocalOut) {
        Get-Content $LocalOut
        Remove-Item $LocalOut -ErrorAction SilentlyContinue
    }
}
finally {
    Remove-Item $LocalScript -ErrorAction SilentlyContinue
}
