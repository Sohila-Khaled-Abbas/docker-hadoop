# ==============================================================================
# Hyper-V Ubuntu-Hadoop Performance & Lag Fix Optimization Script
# Must be executed in PowerShell (Right-click -> Run with PowerShell as Admin)
# ==============================================================================
param (
    [string]$VMName = "Ubuntu-Hadoop"
)

Write-Host "================================================================="
Write-Host "  🚀 Optimizing Hyper-V VM '$VMName' for Peak Performance        "
Write-Host "================================================================="

# 1. Stop VM if running to apply hardware changes
$vm = Get-VM -Name $VMName -ErrorAction SilentlyContinue
if ($null -eq $vm) {
    # Try finding any VM with Ubuntu in name
    $vm = Get-VM | Where-Object { $_.Name -match "Ubuntu" } | Select-Object -First 1
    if ($null -ne $vm) {
        $VMName = $vm.Name
    } else {
        Write-Error "Could not find Hyper-V VM '$VMName'. Please verify VM name in Hyper-V Manager."
        Pause
        exit 1
    }
}

Write-Host "Target VM: $VMName (State: $($vm.State))"

if ($vm.State -eq 'Running') {
    Write-Host "--> Turning off VM to modify CPU, Memory, and Firmware settings..."
    Stop-VM -Name $VMName -TurnOff -Force
    Start-Sleep -Seconds 2
}

# 2. Fix 1-Core CPU Lag -> Upgrade to 4 vCPUs
Write-Host "--> [1/4] Upgrading CPU from 1 vCPU to 4 vCPUs (eliminates GUI lag)..."
Set-VMProcessor -VMName $VMName -Count 4

# 3. Optimize Memory: 3GB Startup, 4GB Max with Dynamic Memory
Write-Host "--> [2/4] Configuring Memory (3072 MB Startup, Dynamic 2048-4096 MB)..."
Set-VMMemory -VMName $VMName -DynamicMemoryEnabled $true -MinimumBytes 2048MB -StartupBytes 3072MB -MaximumBytes 4096MB

# 4. Fix Secure Boot Error for Linux ISO
Write-Host "--> [3/4] Setting Secure Boot Template to 'MicrosoftUEFICertificateAuthority'..."
Set-VMFirmware -VMName $VMName -EnableSecureBoot On -SecureBootTemplate "MicrosoftUEFICertificateAuthority"

# 5. Set DVD (ISO) as First Boot Device
Write-Host "--> [4/5] Setting DVD Drive as Primary Boot Device..."
$dvd = Get-VMDvdDrive -VMName $VMName -ErrorAction SilentlyContinue
if ($null -ne $dvd) {
    Set-VMFirmware -VMName $VMName -FirstBootDevice $dvd
}

# 6. Configure Native 1920x1080 Full Screen Display Resolution
Write-Host "--> [5/5] Configuring Native 1920x1080 Full HD Resolution (edge-to-edge)..."
Set-VMVideo -VMName $VMName -HorizontalResolution 1920 -VerticalResolution 1080 -ResolutionType Single -ErrorAction SilentlyContinue

# 7. Start the VM and open Connection window
Write-Host "--> Starting VM '$VMName'..."
Start-VM -Name $VMName
Start-Process "vmconnect.exe" -ArgumentList "localhost", $VMName

Write-Host "================================================================="
Write-Host "  🎉 VM '$VMName' is now running smoothly with 4 vCPUs & 4GB RAM! "
Write-Host "================================================================="
Start-Sleep -Seconds 3
