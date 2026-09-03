# ==============================================================================
# Configure Hyper-V Host for Enhanced Session Mode, Clipboard & Eject ISO
# Run in elevated PowerShell (Right-click -> Run as Administrator)
# ==============================================================================
param (
    [string]$VMName = "Ubuntu-Hadoop"
)

Write-Host "================================================================="
Write-Host "  🚀 Configuring Hyper-V Host for Enhanced Session & Ejecting ISO"
Write-Host "================================================================="

# 1. Enable Enhanced Session Mode on Hyper-V Host
Write-Host "--> [1/3] Enabling Enhanced Session Mode on Hyper-V host..."
Set-VMHost -EnableEnhancedSessionMode $true

# 2. Find VM
$vm = Get-VM -Name $VMName -ErrorAction SilentlyContinue
if ($null -eq $vm) {
    $vm = Get-VM | Where-Object { $_.Name -match "Ubuntu" } | Select-Object -First 1
}

if ($vm) {
    $VMName = $vm.Name
    Write-Host "Target VM: $VMName"

    # 3. Configure HvSocket transport
    Write-Host "--> [2/3] Enabling EnhancedSessionTransportType 'HvSocket' on '$VMName'..."
    Set-VM -VMName $VMName -EnhancedSessionTransportType HvSocket

    # 4. Eject Installation ISO from DVD drive
    Write-Host "--> [3/3] Ejecting installation medium from DVD drive..."
    $dvd = Get-VMDvdDrive -VMName $VMName -ErrorAction SilentlyContinue
    if ($null -ne $dvd) {
        Set-VMDvdDrive -VMName $VMName -Path $null -ErrorAction SilentlyContinue
        Write-Host "--> DVD Drive emptied (installation ISO removed)!"
    }
} else {
    Write-Warning "Could not locate VM '$VMName'. Please verify VM name in Hyper-V Manager."
}

Write-Host "================================================================="
Write-Host "  🎉 Hyper-V Host Configured: Enhanced Session Ready & ISO Ejected!"
Write-Host "================================================================="
