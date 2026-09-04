# ==============================================================================
# Script: apply-guest-mouse-fix.ps1
# Deploys and executes the mouse pointer fix directly into the running Kali VM
# ==============================================================================
[CmdletBinding()]
param(
    [string]$VmxPath = "D:\courses\AraBigData\docker-hadoop\kali-linux-2026.2-vmware-amd64.vmwarevm\kali-linux-2026.2-vmware-amd64.vmx"
)

$ErrorActionPreference = "Stop"
$Vmrun = "C:\Program Files\VMware\VMware Workstation\vmrun.exe"
if (-not (Test-Path $Vmrun)) {
    $Vmrun = "C:\Program Files (x86)\VMware\VMware Workstation\vmrun.exe"
}

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "  🖱️  Deploying Mouse Cursor & Pointer Fix directly into Kali VM  " -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan

# Check if VM is running
$RunningList = & $Vmrun list
Write-Host "--> Running VMs detected:" -ForegroundColor Gray
$RunningList | ForEach-Object { Write-Host "    $_" -ForegroundColor Gray }

if ($RunningList -notmatch [regex]::Escape($VmxPath)) {
    Write-Warning "VM is not listed as running. Attempting to start it..."
    & $Vmrun -T ws start $VmxPath gui
    Start-Sleep -Seconds 10
}

# 1. Update VMware Host Preferences for Mouse
$PrefFile = "$env:APPDATA\VMware\preferences.ini"
if (Test-Path $PrefFile) {
    Write-Host "--> Updating host VMware preferences.ini..." -ForegroundColor Green
    $lines = Get-Content $PrefFile
    $newLines = @()
    $foundGaming = $false
    $foundUngrab = $false
    foreach ($line in $lines) {
        if ($line -match '^pref\.gamingMouseMode\s*=') {
            $newLines += 'pref.gamingMouseMode = "always"'
            $foundGaming = $true
        } elseif ($line -match '^pref\.motionUngrab\s*=') {
            $newLines += 'pref.motionUngrab = "TRUE"'
            $foundUngrab = $true
        } else {
            $newLines += $line
        }
    }
    if (-not $foundGaming) {
        $newLines += 'pref.gamingMouseMode = "always"'
    }
    if (-not $foundUngrab) {
        $newLines += 'pref.motionUngrab = "TRUE"'
    }
    Set-Content -Path $PrefFile -Value $newLines -Encoding Ascii
    Write-Host "    - Set pref.gamingMouseMode = 'always'" -ForegroundColor Cyan
    Write-Host "    - Set pref.motionUngrab = 'TRUE'" -ForegroundColor Cyan
}

# 2. Copy the mouse fix script into the guest
$LocalFixScript = Join-Path $PSScriptRoot "fix-mouse-in-guest.sh"
if (-not (Test-Path $LocalFixScript)) {
    $LocalFixScript = "D:\courses\AraBigData\docker-hadoop\scripts\fix-mouse-in-guest.sh"
}

Write-Host "--> Copying fix script into guest /tmp/fix-mouse-in-guest.sh..." -ForegroundColor Green
& $Vmrun -T ws -gu kali -gp kali copyFileFromHostToGuest $VmxPath $LocalFixScript "/tmp/fix-mouse-in-guest.sh"

# 3. Execute the script inside the guest
Write-Host "--> Applying X11 software cursor configuration..." -ForegroundColor Green
& $Vmrun -T ws -gu kali -gp kali runProgramInGuest $VmxPath -noWait /bin/bash /tmp/fix-mouse-in-guest.sh

Start-Sleep -Seconds 3

# 4. Reboot the guest cleanly so hardware version 21 and X11 software cursor load
Write-Host "--> Rebooting Kali Linux VM cleanly to apply hardware and cursor updates..." -ForegroundColor Green
& $Vmrun -T ws reset $VmxPath soft

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "  ✅ Mouse pointer fix applied and Kali VM restarted!            " -ForegroundColor Green
Write-Host "  🖱️  Mouse cursor is now active with software rendering.         " -ForegroundColor Green
Write-Host "=================================================================" -ForegroundColor Cyan
