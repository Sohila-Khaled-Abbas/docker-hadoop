# 🚀 1-Click Environment Launchers

This directory contains standalone, 1-click desktop launchers and connection profiles designed for Windows developers running Apache Hadoop, VMware Kali Linux, Hyper-V, and WSL 2.

All launchers are self-contained and invoke their corresponding backend orchestration scripts located in [`scripts/`](../scripts).

---

## 📂 Directory Layout

```text
launchers/
└── windows/
    ├── Start-Hadoop-Docker.bat          # Starts Hadoop Docker container cluster
    ├── Stop-Hadoop-Docker.bat           # Gracefully stops Docker cluster
    ├── Launch-Kali-VMware.bat           # Optimizes VMX hardware & boots Kali Linux
    ├── Fix-Lag-And-Start-VM.bat         # Allocates 4 vCPUs & launches Hyper-V VM
    ├── Fix-VM-Internet.bat              # Repairs Hyper-V DNS & NAT connectivity
    ├── Eject-ISO-And-Enable-Clipboard.bat # Ejects installer ISO & enables Enhanced Session
    └── Ubuntu-WSL-GUI.rdp               # Remote Desktop connection for WSL 2 (Port 3390)
```

---

## 🛠️ Launcher Descriptions & Usage

### 1. Docker Cluster Management

| Launcher | Target Platform | Description |
|:---|:---|:---|
| [`Start-Hadoop-Docker.bat`](windows/Start-Hadoop-Docker.bat) | Docker Desktop | Checks Docker engine daemon status, boots `hadoop-master` container in detached mode (`docker compose up -d`), verifies health, and displays web UI URLs (`:9870`, `:8088`, `:19888`). |
| [`Stop-Hadoop-Docker.bat`](windows/Stop-Hadoop-Docker.bat) | Docker Desktop | Gracefully stops containerized daemons and halts container (`docker compose down`) while safely retaining all persistent HDFS named volumes. |

### 2. VMware Workstation (Kali Linux)

| Launcher | Target Platform | Description |
|:---|:---|:---|
| [`Launch-Kali-VMware.bat`](windows/Launch-Kali-VMware.bat) | VMware Workstation Pro | Invokes [`scripts/vmware/optimize-kali-vmx.ps1`](../scripts/vmware/optimize-kali-vmx.ps1) to adjust RAM to 6GB, 4 vCPUs, clipboard synchronization, and disables WHPX nested VT-x conflicts before launching the VM. |

### 3. Microsoft Hyper-V (Ubuntu 22.04 / 24.04)

| Launcher | Target Platform | Description |
|:---|:---|:---|
| [`Fix-Lag-And-Start-VM.bat`](windows/Fix-Lag-And-Start-VM.bat) | Hyper-V Manager | Elevates to Administrator, stops lagging VM, scales CPU allocation to 4 vCPUs, configures dynamic memory (3072 MB - 4096 MB), prioritizes boot order, and opens `vmconnect.exe`. |
| [`Fix-VM-Internet.bat`](windows/Fix-VM-Internet.bat) | Hyper-V Manager | Runs [`scripts/hyperv/fix-vm-internet.ps1`](../scripts/hyperv/fix-vm-internet.ps1) to restart Hyper-V Virtual Switch NAT bindings and verify gateway communication when guest internet drops. |
| [`Eject-ISO-And-Enable-Clipboard.bat`](windows/Eject-ISO-And-Enable-Clipboard.bat) | Hyper-V Manager | Ejects installation ISO from virtual DVD drive and triggers PowerShell commands to enable Hyper-V Enhanced Session mode for bidirectional clipboard and high-res display. |

### 4. Windows Subsystem for Linux (WSL 2)

| Launcher | Target Platform | Description |
|:---|:---|:---|
| [`Ubuntu-WSL-GUI.rdp`](windows/Ubuntu-WSL-GUI.rdp) | WSL 2 (Ubuntu) | Pre-configured Windows Remote Desktop connection targeting `localhost:3390` with 32-bit color, audio redirection, and clipboard sharing for the XFCE4 desktop. |

---

## 💡 Notes for Linux / macOS Users

Linux and macOS developers can execute equivalent shell commands directly from the root using `make`:
- Start Docker: `make up`
- Stop Docker: `make down`
- Run health checks: `make test`
- View logs: `make logs`
