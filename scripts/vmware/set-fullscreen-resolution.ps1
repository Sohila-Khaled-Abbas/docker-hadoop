# ==============================================================================
# Script: set-fullscreen-resolution.ps1
# Configures VMware host and Kali guest to fill the entire screen (1920x1080 Full HD)
# ==============================================================================
[CmdletBinding()]
param(
    [string]$VmxPath = "D:\courses\AraBigData\docker-hadoop\kali-linux-2026.2-vmware-amd64.vmwarevm\kali-linux-2026.2-vmware-amd64.vmx",
    [int]$Width = 1920,
    [int]$Height = 1080
)

$ErrorActionPreference = "Stop"
$Vmrun = "C:\Program Files\VMware\VMware Workstation\vmrun.exe"
if (-not (Test-Path $Vmrun)) {
    $Vmrun = "C:\Program Files (x86)\VMware\VMware Workstation\vmrun.exe"
}

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "  🖥️  Configuring Full Screen (1920x1080) for Kali Linux VM       " -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan

# 1. Update VMware Host Preferences for Auto-Fit Guest & Window
$PrefFile = "$env:APPDATA\VMware\preferences.ini"
if (Test-Path $PrefFile) {
    Write-Host "--> Configuring VMware host Auto-Fit preferences..." -ForegroundColor Green
    $lines = Get-Content $PrefFile
    $newLines = @()
    $hasAutoFitGuest = $false
    $hasAutoFitWindow = $false
    
    foreach ($line in $lines) {
        if ($line -match '^pref\.view\.autoFitGuest\s*=') {
            $newLines += 'pref.view.autoFitGuest = "TRUE"'
            $hasAutoFitGuest = $true
        } elseif ($line -match '^pref\.view\.autoFitWindow\s*=') {
            $newLines += 'pref.view.autoFitWindow = "TRUE"'
            $hasAutoFitWindow = $true
        } else {
            $newLines += $line
        }
    }
    if (-not $hasAutoFitGuest) { $newLines += 'pref.view.autoFitGuest = "TRUE"' }
    if (-not $hasAutoFitWindow) { $newLines += 'pref.view.autoFitWindow = "TRUE"' }

    Set-Content -Path $PrefFile -Value $newLines -Encoding Ascii
    Write-Host "    - Enabled AutoFitGuest and AutoFitWindow in preferences.ini" -ForegroundColor Cyan
}

# 2. Write display resolution script for Kali guest
$GuestScriptPath = Join-Path $PSScriptRoot "set-guest-res.sh"
if (-not $GuestScriptPath) {
    $GuestScriptPath = "D:\courses\AraBigData\docker-hadoop\scripts\set-guest-res.sh"
}
$ScriptContent = @'
#!/usr/bin/env bash
export DISPLAY=:0
export XAUTHORITY=/home/kali/.Xauthority

# Ensure open-vm-tools is running
echo "kali" | sudo -S systemctl start open-vm-tools 2>/dev/null || true

# Try setting 1920x1080 directly with xrandr
xrandr -s 1920x1080 2>/dev/null || true

# If xrandr output is connected, set mode
OUTPUT=$(xrandr 2>/dev/null | grep ' connected' | awk '{print $1}' | head -n 1)
if [ -n "$OUTPUT" ]; then
    xrandr --output "$OUTPUT" --auto 2>/dev/null || true
fi
'@ -replace "`r`n", "`n"

[System.IO.File]::WriteAllText($GuestScriptPath, $ScriptContent)

Write-Host "--> Copying resolution script to Kali guest..." -ForegroundColor Green
& $Vmrun -T ws -gu kali -gp kali copyFileFromHostToGuest $VmxPath $GuestScriptPath "/tmp/set-guest-res.sh"

Write-Host "--> Setting resolution to 1920x1080 inside Kali..." -ForegroundColor Green
& $Vmrun -T ws -gu kali -gp kali runProgramInGuest $VmxPath /bin/bash /tmp/set-guest-res.sh

Remove-Item $GuestScriptPath -ErrorAction SilentlyContinue

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "  ✅ Resolution updated to 1920x1080 Full HD!                     " -ForegroundColor Green
Write-Host "  💡 Tip: Press Ctrl + Alt + Enter in VMware to toggle Full Screen!" -ForegroundColor Green
Write-Host "=================================================================" -ForegroundColor Cyan
