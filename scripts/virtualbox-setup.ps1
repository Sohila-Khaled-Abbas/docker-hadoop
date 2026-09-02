<#
.SYNOPSIS
    Automated Oracle VM VirtualBox VM Creator and Configurator for Ubuntu & Apache Hadoop.
.DESCRIPTION
    Creates and configures a VirtualBox VM with optimal, rock-solid settings for running Apache Hadoop on Ubuntu:
    - 4.0 GB RAM, 2 vCPUs, 40GB VDI disk with Host I/O Cache
    - UEFI / EFI firmware with native Full HD (1920x1080) GOP framebuffer
    - Hyper-V paravirtualization for precise clock sync and zero timer stalls
    - Audio disabled to eliminate Windows WASAPI host thread latency/crashes
    - VMSVGA graphics with dynamic window auto-resize and 100% 1:1 scaling
    - Port forwarding for SSH (2222), NameNode (9870), YARN (8088), DataNode (9864), JobHistory (19888)
    - Automatically mounts Ubuntu ISO for installation.
#>

param(
    [string]$VmName = "Ubuntu-Hadoop",
    [string]$IsoPath = "D:\courses\AraBigData\docker-hadoop\ubuntu-26.04-desktop-amd64.iso",
    [string]$BaseFolder = "D:\VirtualBoxVMs",
    [int]$MemoryMB = 5120,
    [int]$CpuCount = 4,
    [int]$DiskSizeMB = 40960,
    [switch]$Headless,
    [switch]$Rebuild
)

$VBoxManage = "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"
if (-not (Test-Path $VBoxManage)) {
    $VBoxManage = (Get-Command VBoxManage -ErrorAction SilentlyContinue).Source
}

if (-not $VBoxManage) {
    Write-Error "VBoxManage.exe not found! Please install Oracle VirtualBox."
    exit 1
}

$VdiFolder = Join-Path $BaseFolder $VmName
$VdiPath = Join-Path $VdiFolder "$VmName.vdi"

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "  🐘 Oracle VM VirtualBox & Ubuntu Hadoop Provisioner            " -ForegroundColor Cyan
Write-Host "  ⚡ High-Performance & Reliable Big Data Engineering Profile    " -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan

$existingVm = & $VBoxManage list vms | Select-String "`"$VmName`""
if ($existingVm) {
    if ($Rebuild) {
        Write-Host "--> [Rebuild] Powering off and deleting existing VM: $VmName..." -ForegroundColor Yellow
        & $VBoxManage controlvm $VmName poweroff 2>$null
        Start-Sleep -Seconds 2
        & $VBoxManage unregistervm $VmName --delete 2>$null
        Start-Sleep -Seconds 2
        if (Test-Path $VdiFolder) {
            Remove-Item -Path $VdiFolder -Recurse -Force -ErrorAction SilentlyContinue
        }
    } else {
        Write-Warning "VM '$VmName' already exists. Updating settings and launching..."
        & $VBoxManage modifyvm $VmName `
            --memory $MemoryMB `
            --cpus $CpuCount `
            --paravirtprovider hyperv `
            --hpet on `
            --ioapic on `
            --x2apic on `
            --large-pages off `
            --nested-paging on

        $startType = if ($Headless) { "headless" } else { "gui" }
        Write-Host "--> Starting VM in $startType mode..." -ForegroundColor Green
        & $VBoxManage startvm $VmName --type $startType
        exit 0
    }
}

Write-Host "--> [1/5] Creating Virtual Machine: $VmName..." -ForegroundColor Green
& $VBoxManage createvm --name $VmName --ostype "Ubuntu24_LTS_64" --register --basefolder $BaseFolder

Write-Host "--> [2/5] Configuring Hardware, Display & Hyper-V Paravirtualization..." -ForegroundColor Green
& $VBoxManage modifyvm $VmName `
    --memory $MemoryMB `
    --cpus $CpuCount `
    --vram 128 `
    --graphicscontroller vmsvga `
    --accelerate3d off `
    --firmware efi `
    --paravirtprovider hyperv `
    --audio none `
    --audio-out off `
    --audio-in off `
    --mouse usbtablet `
    --keyboard usb `
    --hpet on `
    --pae on `
    --ioapic on `
    --x2apic on `
    --nested-paging on `
    --large-pages off `
    --nested-hw-virt off `
    --boot1 dvd --boot2 disk --boot3 none --boot4 none `
    --natpf1 "ssh,tcp,,2222,,22" `
    --natpf1 "namenode,tcp,,9870,,9870" `
    --natpf1 "yarn,tcp,,8088,,8088" `
    --natpf1 "datanode,tcp,,9864,,9864" `
    --natpf1 "nodemanager,tcp,,8042,,8042" `
    --natpf1 "jobhistory,tcp,,19888,,19888" `
    --natpf1 "hdfs-rpc,tcp,,9000,,9000" `
    --natpf1 "sparkui,tcp,,4040,,4040" `
    --natpf1 "sparkhistory,tcp,,18080,,18080" `
    --natpf1 "hive,tcp,,10000,,10000" `
    --natpf1 "hiveweb,tcp,,10002,,10002" `
    --natdnshostresolver1 on `
    --natdnsproxy1 on

Write-Host "--> [3/5] Setting Native Full HD (1920x1080) & Dynamic Auto-Resize..." -ForegroundColor Green
& $VBoxManage setextradata $VmName "VBoxInternal2/EfiGraphicsResolution" "1920x1080"
& $VBoxManage setextradata $VmName "CustomVideoMode1" "1920x1080x32"
& $VBoxManage setextradata $VmName "GUI/ScaleFactor" "1.0"
& $VBoxManage setextradata $VmName "GUI/VirtualScreen1/ScaleFactor" "1.0"
& $VBoxManage setextradata $VmName "GUI/MaxGuestResolution" "any"
& $VBoxManage setextradata $VmName "GUI/AutoResizeGuest" "on"
& $VBoxManage setextradata $VmName "GUI/LastGuestSizeHint" "1920,1080"

Write-Host "--> [4/5] Creating 40GB VDI Disk and Enabling Host I/O Cache..." -ForegroundColor Green
& $VBoxManage storagectl $VmName --name "SATA Controller" --add sata --controller IntelAhci --portcount 4 --bootable on --hostiocache on
& $VBoxManage createmedium disk --filename $VdiPath --size $DiskSizeMB --format VDI
& $VBoxManage storageattach $VmName --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium $VdiPath

if (Test-Path $IsoPath) {
    & $VBoxManage storageattach $VmName --storagectl "SATA Controller" --port 1 --device 0 --type dvddrive --medium $IsoPath
    Write-Host "Attached installation ISO: $IsoPath" -ForegroundColor Gray
} else {
    Write-Warning "ISO path '$IsoPath' not found. Please attach manually if installing OS."
}

$startType = if ($Headless) { "headless" } else { "gui" }
Write-Host "--> [5/5] Launching VM in $startType Mode..." -ForegroundColor Green
& $VBoxManage startvm $VmName --type $startType

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "  🎉 Virtual Machine '$VmName' Started Successfully!             " -ForegroundColor Green
Write-Host "  - Connect via SSH:  ssh -p 2222 hadoopuser@127.0.0.1           " -ForegroundColor Yellow
Write-Host "  - HDFS NameNode:    http://127.0.0.1:9870                      " -ForegroundColor Yellow
Write-Host "  - YARN UI:          http://127.0.0.1:8088                      " -ForegroundColor Yellow
Write-Host "  - MapReduce UI:     http://127.0.0.1:19888                     " -ForegroundColor Yellow
Write-Host "  - Spark UI:         http://127.0.0.1:4040                      " -ForegroundColor Yellow
Write-Host "=================================================================" -ForegroundColor Cyan
