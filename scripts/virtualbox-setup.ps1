<#
.SYNOPSIS
    Automated Oracle VM VirtualBox VM Creator and Configurator for Ubuntu & Apache Hadoop.
.DESCRIPTION
    Creates and configures a VirtualBox VM with optimal settings for running Apache Hadoop on Ubuntu:
    - 2.5 GB RAM, 2 vCPUs, 40GB VDI disk
    - Port forwarding for SSH (2222), NameNode (9870), YARN (8088), DataNode (9864)
    - Automatically mounts Ubuntu ISO for installation.
#>

param(
    [string]$VmName = "Ubuntu-Hadoop",
    [string]$IsoPath = "D:\courses\AraBigData\docker-hadoop\ubuntu-26.04-desktop-amd64.iso",
    [string]$BaseFolder = "D:\VirtualBoxVMs",
    [int]$MemoryMB = 2560,
    [int]$CpuCount = 2,
    [int]$DiskSizeMB = 40960
)

$VBoxManage = "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"
if (-not (Test-Path $VBoxManage)) {
    $VBoxManage = (Get-Command VBoxManage -ErrorAction SilentlyContinue).Source
}

if (-not $VBoxManage) {
    Write-Error "VBoxManage.exe not found! Please install VirtualBox."
    exit 1
}

Write-Host "=== [1/5] Checking VM Existence ===" -ForegroundColor Cyan
$existingVm = & $VBoxManage list vms | Select-String $VmName
if ($existingVm) {
    Write-Warning "VM '$VmName' already exists. Use VBoxManage startvm `"$VmName`" to launch."
} else {
    Write-Host "=== [2/5] Creating Virtual Machine: $VmName ===" -ForegroundColor Cyan
    & $VBoxManage createvm --name $VmName --ostype "Ubuntu24_LTS_64" --register --basefolder $BaseFolder

    Write-Host "=== [3/5] Configuring Hardware & Ports ===" -ForegroundColor Cyan
    & $VBoxManage modifyvm $VmName `
        --memory $MemoryMB `
        --cpus $CpuCount `
        --vram 128 `
        --graphicscontroller vboxsvga `
        --accelerate-3d off `
        --mouse usbtablet `
        --clipboard-mode bidirectional `
        --drag-and-drop bidirectional `
        --paravirtprovider default `
        --hpet on `
        --pae on `
        --ioapic on `
        --boot1 dvd --boot2 disk --boot3 none --boot4 none `
        --natpf1 "ssh,tcp,,2222,,22" `
        --natpf1 "namenode,tcp,,9870,,9870" `
        --natpf1 "yarn,tcp,,8088,,8088" `
        --natpf1 "datanode,tcp,,9864,,9864"

    Write-Host "=== [4/5] Creating Storage & Attaching ISO ===" -ForegroundColor Cyan
    $vdiPath = Join-Path $BaseFolder "$VmName\$VmName.vdi"
    & $VBoxManage storagectl $VmName --name "SATA Controller" --add sata --controller IntelAhci --portcount 4
    & $VBoxManage createmedium disk --filename $vdiPath --size $DiskSizeMB --format VDI
    & $VBoxManage storageattach $VmName --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium $vdiPath

    if (Test-Path $IsoPath) {
        & $VBoxManage storageattach $VmName --storagectl "SATA Controller" --port 1 --device 0 --type dvddrive --medium $IsoPath
    } else {
        Write-Warning "ISO path '$IsoPath' not found. Please attach manually."
    }
}

Write-Host "=== [5/5] Starting VM ===" -ForegroundColor Cyan
& $VBoxManage startvm $VmName --type gui
Write-Host "Virtual Machine '$VmName' started successfully!" -ForegroundColor Green
