# ==============================================================================
# Script: optimize-kali-vmx.ps1
# Purpose: Tune VMware VMX for Kali Linux based on host hardware & Hadoop needs
# ==============================================================================
[CmdletBinding()]
param(
    [string]$VmxPath = "",
    [int]$RamMB = 6144,
    [int]$vCPUs = 4
)

$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($VmxPath)) {
    $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    if ([string]::IsNullOrWhiteSpace($scriptDir)) {
        $scriptDir = $PSScriptRoot
    }
    if ([string]::IsNullOrWhiteSpace($scriptDir)) {
        $scriptDir = (Get-Location).Path
    }
    $candidate1 = Join-Path $scriptDir "..\kali-linux-2026.2-vmware-amd64.vmwarevm\kali-linux-2026.2-vmware-amd64.vmx"
    $candidate2 = Join-Path (Get-Location).Path "kali-linux-2026.2-vmware-amd64.vmwarevm\kali-linux-2026.2-vmware-amd64.vmx"
    if (Test-Path $candidate1) {
        $VmxPath = $candidate1
    } elseif (Test-Path $candidate2) {
        $VmxPath = $candidate2
    } else {
        $VmxPath = $candidate1
    }
}

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "  ⚙️  Optimizing Kali Linux VMware Virtual Machine Configuration  " -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan

# 1. Resolve and Validate VMX path
$ResolvedVmx = Resolve-Path $VmxPath -ErrorAction SilentlyContinue
if (-not $ResolvedVmx -or -not (Test-Path $ResolvedVmx)) {
    Write-Error "VMX file not found at: $VmxPath. Please ensure the 7z archive is extracted."
    exit 1
}
$VmxFullPath = $ResolvedVmx.Path
Write-Host "--> Located VMX: $VmxFullPath" -ForegroundColor Green

# 2. Check Host Hardware
$HostRAM = [math]::round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB, 1)
$HostCPU = (Get-CimInstance Win32_Processor).Name
$LogicalCPUs = (Get-CimInstance Win32_Processor).NumberOfLogicalProcessors
Write-Host "--> Host Detected: $HostCPU ($LogicalCPUs Threads, ${HostRAM} GB RAM)" -ForegroundColor Gray

# Safe check: do not allocate more than 60% of host RAM
if ($RamMB -gt ($HostRAM * 1024 * 0.65)) {
    Write-Warning "Requested RAM ($RamMB MB) exceeds 65% of host physical RAM. Clamping to 6144 MB for safety."
    $RamMB = 6144
}

# 3. Create Backup of VMX
$BackupPath = "$VmxFullPath.bak"
if (-not (Test-Path $BackupPath)) {
    Copy-Item -Path $VmxFullPath -Destination $BackupPath -Force
    Write-Host "--> Created backup: $BackupPath" -ForegroundColor Green
}

# 4. Parse and Update Key-Value pairs
$Content = Get-Content -Path $VmxFullPath
$Config = [ordered]@{}

foreach ($line in $Content) {
    if ($line -match '^\s*([^\s=]+)\s*=\s*"(.*)"\s*$') {
        $Config[$matches[1].Trim()] = $matches[2]
    } elseif ($line -match '^\s*([^\s=]+)\s*=\s*(.*?)\s*$') {
        $Config[$matches[1].Trim()] = $matches[2]
    }
}

# Apply Tuning
$Config["memsize"] = "$RamMB"
$Config["numvcpus"] = "$vCPUs"
$Config["cpuid.coresPerSocket"] = "$vCPUs"
$Config["vcpu.hotadd"] = "TRUE"
# Disable nested virtualization to prevent "Virtualized Intel VT-x/EPT is not supported" popup on Windows
$Config["vhv.enable"] = "FALSE"
$Config["vpmc.enable"] = "FALSE"

# Hardware Compatibility Upgrade (from legacy v8 to modern v21)
$Config["virtualHW.version"] = "21"

# Fix Mouse Pointer & Input Synchronization
$Config["vmmouse.present"] = "FALSE"        # Forces USB tablet absolute pointer; eliminates invisible cursor bug
$Config["mouse.vusb.enable"] = "TRUE"       # Enables virtual USB mouse bus
$Config["usb.generic.allowHID"] = "TRUE"

# Enable Clipboard & Drag-Drop
$Config["isolation.tools.copy.disable"] = "FALSE"
$Config["isolation.tools.paste.disable"] = "FALSE"
$Config["isolation.tools.dnd.disable"] = "FALSE"
$Config["isolation.tools.hgfs.disable"] = "FALSE"

# Graphics & Performance (Disable 3D to prevent invisible cursor in XFCE/Xorg)
$Config["mks.enable3d"] = "FALSE"
$Config["tools.syncTime"] = "TRUE"
$Config["prefvmx.useSharedProcessorsInSingleLargePageVM"] = "TRUE"

# Reconstruct and Save VMX
$NewLines = foreach ($k in $Config.Keys) {
    "$k = `"$($Config[$k])`""
}

Set-Content -Path $VmxFullPath -Value $NewLines -Encoding Ascii
Write-Host "--> Applied Optimizations:" -ForegroundColor Green
Write-Host "    - Memory (RAM):       $RamMB MB ($([math]::round($RamMB/1024, 1)) GB)" -ForegroundColor Cyan
Write-Host "    - vCPUs:              $vCPUs Cores (1 Socket x $vCPUs Cores)" -ForegroundColor Cyan
Write-Host "    - Nested VT-x/EPT:    Disabled (vhv.enable=FALSE - Prevents Windows WHPX popups)" -ForegroundColor Cyan
Write-Host "    - Clipboard Sharing:  Enabled (Copy/Paste & Drag/Drop)" -ForegroundColor Cyan
Write-Host "    - Shared Folders:     Enabled (HGFS)" -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "  ✅ Kali Linux VMX successfully optimized for Big Data workloads!" -ForegroundColor Green
Write-Host "=================================================================" -ForegroundColor Cyan
