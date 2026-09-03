# ==============================================================================
# Fix Hyper-V VM Internet by connecting to NAT Default Switch
# Run as Administrator
# ==============================================================================
param (
    [string]$VMName = "Ubuntu-Hadoop"
)

Write-Host "================================================================="
Write-Host "  🌐 Fixing Hyper-V VM Internet Connection                       "
Write-Host "================================================================="

$vm = Get-VM -Name $VMName -ErrorAction SilentlyContinue
if ($null -eq $vm) {
    $vm = Get-VM | Where-Object { $_.Name -match "Ubuntu" } | Select-Object -First 1
}

if ($vm) {
    $VMName = $vm.Name
    Write-Host "Target VM: $VMName"

    Write-Host "--> Connecting '$VMName' to Hyper-V 'Default Switch' (NAT)..."
    Get-VMNetworkAdapter -VMName $VMName | Connect-VMNetworkAdapter -SwitchName "Default Switch"
    
    Write-Host "================================================================="
    Write-Host "  🎉 VM '$VMName' is now connected to 'Default Switch'!           "
    Write-Host "  Internet and DNS will now route through host Wi-Fi via NAT.    "
    Write-Host "================================================================="
} else {
    Write-Warning "Could not find VM '$VMName'. Please verify VM name in Hyper-V Manager."
}
