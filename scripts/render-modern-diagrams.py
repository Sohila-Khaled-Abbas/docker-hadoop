# ==============================================================================
# Script: render-modern-diagrams.py
# Generates two ultra-modern, high-definition SVG & PNG diagrams:
# 1. hadoop-data-engineering-infographic.svg (Platform & Lifecycle Infographic)
# 2. hadoop-data-engineering-system-architecture.svg (Deep Distributed Architecture)
#
# Optimized for:
# - Zero text overflow: Every line mathematically fitted with generous padding
# - Modern dark-mode aesthetics: Glassmorphism, tailored gradients, glow filters
# - Full repo updates: Hadoop 3.3.6 LTS, Kali VMware, GCP Dataproc, 512MB YARN alloc,
#   G1GC tuning, Monte Carlo Pi benchmark, 1-Click Launchers
# ==============================================================================
import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(r"D:\courses\AraBigData\docker-hadoop")
IMG_DIR = REPO_ROOT / "docs" / "images"
IMG_DIR.mkdir(parents=True, exist_ok=True)

# Common SVG definitions (Gradients, filters, patterns)
COMMON_DEFS = '''
    <!-- Modern Background Gradients -->
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#060913" />
      <stop offset="35%" stop-color="#0a0f1d" />
      <stop offset="70%" stop-color="#0e1526" />
      <stop offset="100%" stop-color="#070a14" />
    </linearGradient>

    <linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#388bfd" />
      <stop offset="25%" stop-color="#a371f7" />
      <stop offset="50%" stop-color="#3fb950" />
      <stop offset="75%" stop-color="#d29922" />
      <stop offset="100%" stop-color="#38bdf8" />
    </linearGradient>

    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#151b28" stop-opacity="0.95" />
      <stop offset="100%" stop-color="#0c101a" stop-opacity="0.98" />
    </linearGradient>

    <linearGradient id="hdfsGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#1f6feb" />
      <stop offset="100%" stop-color="#388bfd" />
    </linearGradient>

    <linearGradient id="yarnGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#238636" />
      <stop offset="100%" stop-color="#2ea043" />
    </linearGradient>

    <linearGradient id="engineGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#8957e5" />
      <stop offset="100%" stop-color="#bc8cff" />
    </linearGradient>

    <linearGradient id="gcpGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0284c7" />
      <stop offset="100%" stop-color="#38bdf8" />
    </linearGradient>

    <linearGradient id="volGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#da3633" />
      <stop offset="100%" stop-color="#f85149" />
    </linearGradient>

    <!-- Glassmorphic Glow Filters -->
    <filter id="shadow" x="-10%" y="-10%" width="120%" height="125%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#000000" flood-opacity="0.65" />
    </filter>
    <filter id="glowBlue" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="0" stdDeviation="8" flood-color="#388bfd" flood-opacity="0.4" />
    </filter>
    <filter id="glowGreen" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="0" stdDeviation="8" flood-color="#3fb950" flood-opacity="0.4" />
    </filter>
    <filter id="glowPurple" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="0" stdDeviation="8" flood-color="#bc8cff" flood-opacity="0.4" />
    </filter>
    <filter id="glowAmber" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="0" stdDeviation="8" flood-color="#d29922" flood-opacity="0.4" />
    </filter>

    <!-- Directional Arrow Markers -->
    <marker id="arrowBlue" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#58a6ff" />
    </marker>
    <marker id="arrowGreen" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#3fb950" />
    </marker>
    <marker id="arrowPurple" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#bc8cff" />
    </marker>
    <marker id="arrowRed" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#f85149" />
    </marker>

    <!-- Engineering Grid Pattern -->
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <line x1="0" y1="0" x2="40" y2="0" stroke="#121926" stroke-width="0.75" />
      <line x1="0" y1="0" x2="0" y2="40" stroke="#121926" stroke-width="0.75" />
      <circle cx="20" cy="20" r="0.75" fill="#182234" />
    </pattern>
'''

COMMON_STYLES = '''
    .title { font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif; font-weight: 800; fill: #ffffff; }
    .subtitle { font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif; font-weight: 400; fill: #8b949e; }
    .heading { font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif; font-weight: 700; fill: #ffffff; }
    .subheading { font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif; font-weight: 600; fill: #c9d1d9; }
    .bold-text { font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif; font-weight: 600; fill: #e6edf3; }
    .body-text { font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif; font-weight: 400; fill: #94a3b8; }
    .mono { font-family: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', Consolas, monospace; fill: #79c0ff; }
    .badge { font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif; font-weight: 600; font-size: 11px; }
    .step-num { font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif; font-weight: 800; font-size: 15px; fill: #ffffff; text-anchor: middle; dominant-baseline: central; }
'''

# ==============================================================================
# 1. GENERATE INFOGRAPHIC SVG (Multi-Platform Ecosystem & Data Engineering Map)
# ==============================================================================
infographic_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2800 1920" width="2800" height="1920">
  <defs>
{COMMON_DEFS}
  </defs>

  <style>
{COMMON_STYLES}
  </style>

  <!-- Background Base -->
  <rect width="2800" height="1920" fill="url(#bgGrad)" />
  <rect width="2800" height="1920" fill="url(#grid)" opacity="0.9" />

  <!-- Outer Architectural Border Frame -->
  <rect x="25" y="25" width="2750" height="1870" rx="24" fill="none" stroke="#21262d" stroke-width="2" />

  <!-- ========================================================================= -->
  <!-- 1. HEADER SECTION (HERO BANNER WITH ECOSYSTEM BADGES)                     -->
  <!-- ========================================================================= -->
  <g id="header-section" transform="translate(60, 50)">
    <rect x="0" y="0" width="2680" height="135" rx="16" fill="#151b28" stroke="#30363d" stroke-width="1.5" filter="url(#shadow)" />
    <path d="M 0 16 Q 0 0 16 0 L 22 0 L 22 135 L 16 135 Q 0 135 0 119 Z" fill="url(#headerGrad)" />

    <text x="48" y="54" class="title" font-size="31" letter-spacing="0.5">
      🐘 APACHE HADOOP 3.3.6 LTS &amp; MULTI-PLATFORM CLUSTER ECOSYSTEM
    </text>
    <text x="48" y="90" class="subtitle" font-size="15">
      Distributed HDFS Storage • YARN Container Scheduling • Low-Pause G1GC Tuning • Docker, VMware (Kali), Hyper-V &amp; Google Cloud Dataproc
    </text>

    <!-- Badges Row -->
    <g transform="translate(1420, 36)">
      <g transform="translate(0, 0)">
        <rect x="0" y="0" width="160" height="34" rx="8" fill="#1f6feb" fill-opacity="0.18" stroke="#388bfd" stroke-width="1.2" />
        <text x="80" y="22" class="badge" fill="#58a6ff" text-anchor="middle">HADOOP v3.3.6 LTS</text>
      </g>
      <g transform="translate(175, 0)">
        <rect x="0" y="0" width="165" height="34" rx="8" fill="#238636" fill-opacity="0.18" stroke="#3fb950" stroke-width="1.2" />
        <text x="82" y="22" class="badge" fill="#56d364" text-anchor="middle">OPENJDK 11 / 8 LTS</text>
      </g>
      <g transform="translate(355, 0)">
        <rect x="0" y="0" width="170" height="34" rx="8" fill="#8957e5" fill-opacity="0.18" stroke="#bc8cff" stroke-width="1.2" />
        <text x="85" y="22" class="badge" fill="#d2a8ff" text-anchor="middle">DOCKER COMPOSE</text>
      </g>
      <g transform="translate(540, 0)">
        <rect x="0" y="0" width="175" height="34" rx="8" fill="#0284c7" fill-opacity="0.18" stroke="#38bdf8" stroke-width="1.2" />
        <text x="87" y="22" class="badge" fill="#38bdf8" text-anchor="middle">☁️ GCP DATAPROC</text>
      </g>
      <g transform="translate(730, 0)">
        <rect x="0" y="0" width="175" height="34" rx="8" fill="#d29922" fill-opacity="0.18" stroke="#e3b341" stroke-width="1.2" />
        <text x="87" y="22" class="badge" fill="#f2cc60" text-anchor="middle">🐉 KALI LINUX VM</text>
      </g>
      <text x="905" y="72" class="body-text" font-size="12" fill="#8b949e" text-anchor="end">
        Enterprise Big Data Engineering Suite • Zero Silent Corruption
      </text>
    </g>
  </g>

  <!-- ========================================================================= -->
  <!-- 2. MULTI-PLATFORM RUNTIMES STRIP (6 EQUAL CARDS)                         -->
  <!-- ========================================================================= -->
  <g id="multi-platform-section" transform="translate(60, 205)">
    <rect x="0" y="0" width="2680" height="165" rx="16" fill="url(#cardGrad)" stroke="#30363d" stroke-width="1.5" filter="url(#shadow)" />
    
    <rect x="25" y="16" width="310" height="28" rx="6" fill="#d29922" fill-opacity="0.15" stroke="#d29922" stroke-width="1" />
    <text x="180" y="35" class="subheading" font-size="13" fill="#e3b341" text-anchor="middle">🖥️ 6 SUPPORTED MULTI-PLATFORM RUNTIMES</text>

    <!-- Card 1: Docker -->
    <g transform="translate(25, 55)">
      <rect x="0" y="0" width="425" height="95" rx="10" fill="#0d1117" stroke="#388bfd" stroke-width="1.2" />
      <text x="16" y="26" class="bold-text" font-size="13.5" fill="#58a6ff">🐳 Docker Engine / Compose</text>
      <text x="16" y="48" class="body-text" font-size="11.5">Single-Node container (hadoop-master) with named volumes</text>
      <rect x="16" y="60" width="393" height="22" rx="4" fill="#161b22" />
      <text x="24" y="75" class="mono" font-size="10.5" fill="#79c0ff">make up • docker compose up -d • Port 9870</text>
    </g>

    <!-- Card 2: VMware Kali -->
    <g transform="translate(465, 55)">
      <rect x="0" y="0" width="425" height="95" rx="10" fill="#0d1117" stroke="#bc8cff" stroke-width="1.2" />
      <text x="16" y="26" class="bold-text" font-size="13.5" fill="#d2a8ff">🐉 VMware Workstation (Kali)</text>
      <text x="16" y="48" class="body-text" font-size="11.5">Kali Rolling • Hadoop 3.3.6 • 6GB RAM / 4 vCPUs • G1GC</text>
      <rect x="16" y="60" width="393" height="22" rx="4" fill="#161b22" />
      <text x="24" y="75" class="mono" font-size="10.5" fill="#bc8cff">Launch-Kali-VMware.bat • HWCursor off • 1080p</text>
    </g>

    <!-- Card 3: GCP Dataproc -->
    <g transform="translate(905, 55)">
      <rect x="0" y="0" width="425" height="95" rx="10" fill="#0d1117" stroke="#38bdf8" stroke-width="1.2" />
      <text x="16" y="26" class="bold-text" font-size="13.5" fill="#38bdf8">☁️ Google Cloud Dataproc &amp; GCE</text>
      <text x="16" y="48" class="body-text" font-size="11.5">Ephemeral clusters • GCS (gs://) • Spot workers • Gateway</text>
      <rect x="16" y="60" width="393" height="22" rx="4" fill="#161b22" />
      <text x="24" y="75" class="mono" font-size="10.5" fill="#79c0ff">Deploy-Hadoop-GCP.bat • .ps1 • 30m Auto-Idle</text>
    </g>

    <!-- Card 4: Hyper-V -->
    <g transform="translate(1345, 55)">
      <rect x="0" y="0" width="425" height="95" rx="10" fill="#0d1117" stroke="#3fb950" stroke-width="1.2" />
      <text x="16" y="26" class="bold-text" font-size="13.5" fill="#56d364">🪟 Hyper-V Generation 2 (Ubuntu)</text>
      <text x="16" y="48" class="body-text" font-size="11.5">Ubuntu 24.04 • 4 vCPUs • Dynamic RAM • UEFI CA • NAT fix</text>
      <rect x="16" y="60" width="393" height="22" rx="4" fill="#161b22" />
      <text x="24" y="75" class="mono" font-size="10.5" fill="#7ee787">Fix-Lag-And-Start-VM.bat • optimize-hyperv.ps1</text>
    </g>

    <!-- Card 5: WSL 2 -->
    <g transform="translate(1785, 55)">
      <rect x="0" y="0" width="425" height="95" rx="10" fill="#0d1117" stroke="#f2cc60" stroke-width="1.2" />
      <text x="16" y="26" class="bold-text" font-size="13.5" fill="#f2cc60">🐧 WSL 2 Ubuntu + Visual XFCE GUI</text>
      <text x="16" y="48" class="body-text" font-size="11.5">Windows 11 Native Kernel • xRDP Port 3390 • Zero VM lag</text>
      <rect x="16" y="60" width="393" height="22" rx="4" fill="#161b22" />
      <text x="24" y="75" class="mono" font-size="10.5" fill="#f2cc60">Ubuntu-WSL-GUI.rdp • install-hadoop-wsl.sh</text>
    </g>

    <!-- Card 6: VirtualBox -->
    <g transform="translate(2225, 55)">
      <rect x="0" y="0" width="430" height="95" rx="10" fill="#0d1117" stroke="#e3b341" stroke-width="1.2" />
      <text x="16" y="26" class="bold-text" font-size="13.5" fill="#e3b341">📦 Oracle VirtualBox Automated Setup</text>
      <text x="16" y="48" class="body-text" font-size="11.5">PowerShell automated NAT port-forwarding &amp; provisioning</text>
      <rect x="16" y="60" width="398" height="22" rx="4" fill="#161b22" />
      <text x="24" y="75" class="mono" font-size="10.5" fill="#e3b341">virtualbox-setup.ps1 • SSH port 2222</text>
    </g>
  </g>

  <!-- ========================================================================= -->
  <!-- 3. MAIN ARCHITECTURE BODY (3 COLUMNS)                                     -->
  <!-- ========================================================================= -->

  <!-- LEFT COLUMN: DEVELOPER & HOST ACCESS LAYER (Width: 520) -->
  <g id="host-client-layer" transform="translate(60, 390)">
    <rect x="0" y="0" width="520" height="1100" rx="16" fill="url(#cardGrad)" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="6,4" filter="url(#shadow)" />
    
    <path d="M 0 16 Q 0 0 16 0 L 504 0 Q 520 0 520 16 L 520 54 L 0 54 Z" fill="url(#gcpGrad)" opacity="0.15" />
    <rect x="20" y="14" width="280" height="26" rx="6" fill="#0284c7" />
    <text x="160" y="32" class="heading" font-size="13" fill="#ffffff" text-anchor="middle">💻 HOST SYSTEM &amp; CLIENT ACCESS</text>
    <text x="20" y="80" class="subheading" font-size="15" fill="#38bdf8">Developer Control Planes</text>
    <text x="20" y="100" class="body-text" font-size="13">Native Windows Host interfaces connecting into Hadoop</text>

    <!-- Component 1: Web Browsers -->
    <g transform="translate(20, 120)">
      <rect x="0" y="0" width="480" height="195" rx="12" fill="#0d1117" stroke="#30363d" stroke-width="1.2" />
      <text x="20" y="30" class="bold-text" font-size="15" fill="#38bdf8">🌐 Web Consoles (Native Web UIs)</text>
      <text x="20" y="52" class="body-text" font-size="12">Administrative HTTP ports (Localhost or VM IP):</text>
      
      <rect x="18" y="65" width="444" height="26" rx="5" fill="#161b22" stroke="#21262d" />
      <text x="28" y="82" class="mono" font-size="11" fill="#58a6ff">HDFS NameNode UI</text>
      <text x="450" y="82" class="mono" font-size="11" fill="#79c0ff" text-anchor="end">:9870 (Overview &amp; Explorer)</text>

      <rect x="18" y="97" width="444" height="26" rx="5" fill="#161b22" stroke="#21262d" />
      <text x="28" y="114" class="mono" font-size="11" fill="#3fb950">YARN ResourceManager UI</text>
      <text x="450" y="114" class="mono" font-size="11" fill="#7ee787" text-anchor="end">:8088 (Cluster &amp; Apps)</text>

      <rect x="18" y="129" width="444" height="26" rx="5" fill="#161b22" stroke="#21262d" />
      <text x="28" y="146" class="mono" font-size="11" fill="#bc8cff">JobHistoryServer UI</text>
      <text x="450" y="146" class="mono" font-size="11" fill="#d2a8ff" text-anchor="end">:19888 (Metrics &amp; Logs)</text>

      <rect x="18" y="161" width="444" height="26" rx="5" fill="#161b22" stroke="#21262d" />
      <text x="28" y="178" class="mono" font-size="11" fill="#e3b341">DataNode / NodeManager</text>
      <text x="450" y="178" class="mono" font-size="11" fill="#f2cc60" text-anchor="end">:9864 / :8042 (Workers)</text>
    </g>

    <!-- Component 2: 1-Click Launchers -->
    <g transform="translate(20, 335)">
      <rect x="0" y="0" width="480" height="205" rx="12" fill="#0d1117" stroke="#30363d" stroke-width="1.2" />
      <text x="20" y="28" class="bold-text" font-size="15" fill="#e3b341">🚀 1-Click Windows Launchers</text>
      <text x="20" y="48" class="body-text" font-size="12">Location: <tspan class="mono" fill="#f2cc60">launchers/windows/</tspan></text>

      <text x="20" y="75" class="bold-text" font-size="12.5" fill="#e6edf3">• Deploy-Hadoop-GCP.bat / .ps1</text>
      <text x="35" y="92" class="body-text" font-size="11.5">Interactive GCP Dataproc &amp; GCE provisioning menu</text>

      <text x="20" y="115" class="bold-text" font-size="12.5" fill="#e6edf3">• Launch-Kali-VMware.bat</text>
      <text x="35" y="132" class="body-text" font-size="11.5">Applies VMX tuning &amp; launches Kali Hadoop VM</text>

      <text x="20" y="155" class="bold-text" font-size="12.5" fill="#e6edf3">• Start-Hadoop-Docker.bat / Stop-*.bat</text>
      <text x="35" y="172" class="body-text" font-size="11.5">Boots / gracefully shuts down containerized cluster</text>

      <text x="20" y="195" class="mono" font-size="11" fill="#79c0ff">• Ubuntu-WSL-GUI.rdp (Direct XFCE Desktop)</text>
    </g>

    <!-- Component 3: CLI / Terminal & SSH -->
    <g transform="translate(20, 560)">
      <rect x="0" y="0" width="480" height="185" rx="12" fill="#0d1117" stroke="#30363d" stroke-width="1.2" />
      <text x="20" y="28" class="bold-text" font-size="15" fill="#58a6ff">💻 Developer CLI &amp; SSH Bastion</text>
      <text x="20" y="48" class="body-text" font-size="12">Terminal Automation Suite (make / powershell):</text>

      <rect x="18" y="62" width="444" height="26" rx="5" fill="#161b22" />
      <text x="28" y="79" class="mono" font-size="11.5" fill="#58a6ff">make test</text>
      <text x="450" y="79" class="body-text" font-size="11.5" fill="#8b949e" text-anchor="end">Run full HDFS &amp; YARN test suite</text>

      <rect x="18" y="94" width="444" height="26" rx="5" fill="#161b22" />
      <text x="28" y="111" class="mono" font-size="11.5" fill="#58a6ff">make gcp-dataproc-create</text>
      <text x="450" y="111" class="body-text" font-size="11.5" fill="#8b949e" text-anchor="end">Provision Dataproc cluster</text>

      <rect x="18" y="126" width="444" height="26" rx="5" fill="#161b22" />
      <text x="28" y="143" class="mono" font-size="11.5" fill="#58a6ff">make vm-kali-optimize</text>
      <text x="450" y="143" class="body-text" font-size="11.5" fill="#8b949e" text-anchor="end">Calibrate VMware VMX memory</text>

      <rect x="18" y="158" width="444" height="22" rx="4" fill="#161b22" stroke="#1f6feb" stroke-width="1" />
      <text x="28" y="174" class="mono" font-size="10.5" fill="#79c0ff">ssh -p 22222 hduser@localhost  (Kali: ssh kali@192.168.13.128)</text>
    </g>

    <!-- Component 4: Pre-Packaged Datasets -->
    <g transform="translate(20, 765)">
      <rect x="0" y="0" width="480" height="155" rx="12" fill="#0d1117" stroke="#30363d" stroke-width="1.2" />
      <text x="20" y="28" class="bold-text" font-size="15" fill="#3fb950">📊 Built-In Practice Datasets</text>
      <text x="20" y="48" class="body-text" font-size="12">Zero-setup verification datasets in <tspan class="mono" fill="#7ee787">datasets/</tspan>:</text>

      <text x="20" y="75" class="bold-text" font-size="12.5" fill="#e6edf3">• wordcount-sample.txt (Unstructured Text)</text>
      <text x="35" y="94" class="body-text" font-size="11.5">Large text corpus for testing MapReduce &amp; Streaming</text>

      <text x="20" y="118" class="bold-text" font-size="12.5" fill="#e6edf3">• employees.csv (Tabular Schema)</text>
      <text x="35" y="137" class="body-text" font-size="11.5">Structured employee records for PySpark DataFrame jobs</text>
    </g>

    <!-- Step 1 Indicator Pill -->
    <g transform="translate(20, 935)">
      <rect x="0" y="0" width="480" height="145" rx="12" fill="#1f6feb" fill-opacity="0.1" stroke="#1f6feb" stroke-width="1.2" />
      <circle cx="35" cy="35" r="16" fill="#1f6feb" />
      <text x="35" y="35" class="step-num">1</text>
      <text x="65" y="35" class="bold-text" font-size="15" fill="#58a6ff">Job &amp; Data Ingestion Trigger</text>
      <text x="25" y="70" class="body-text" font-size="12.5">Developer initiates execution via 1-Click launcher, CLI script,</text>
      <text x="25" y="90" class="body-text" font-size="12.5">or PySpark pipeline. Requests dispatch to YARN RM (<tspan class="mono" fill="#79c0ff">:8032</tspan>)</text>
      <text x="25" y="110" class="body-text" font-size="12.5">and HDFS NameNode (<tspan class="mono" fill="#79c0ff">:9000</tspan> / <tspan class="mono" fill="#79c0ff">gs://</tspan> on Dataproc).</text>
    </g>
  </g>

  <!-- CENTER REGION: HADOOP CLUSTER DAEMON RUNTIME (Width: 1540) -->
  <g id="docker-container-boundary" transform="translate(620, 390)">
    <rect x="0" y="0" width="1540" height="1100" rx="20" fill="url(#cardGrad)" stroke="#1f6feb" stroke-width="2" filter="url(#shadow)" />

    <path d="M 0 20 Q 0 0 20 0 L 1520 0 Q 1540 0 1540 20 L 1540 60 L 0 60 Z" fill="url(#hdfsGrad)" opacity="0.18" />
    <rect x="30" y="16" width="370" height="30" rx="6" fill="#1f6feb" />
    <text x="215" y="36" class="heading" font-size="14" fill="#ffffff" text-anchor="middle">🐘 HADOOP CLUSTER ENGINE (6 DAEMONS)</text>

    <!-- Runtime Attributes Info Pill -->
    <g transform="translate(420, 16)">
      <rect x="0" y="0" width="1090" height="30" rx="6" fill="#161b22" stroke="#30363d" />
      <text x="20" y="20" class="mono" font-size="12" fill="#8b949e">
        <tspan fill="#58a6ff">HADOOP:</tspan> 3.3.6 LTS | <tspan fill="#3fb950">JAVA:</tspan> OpenJDK 11 | <tspan fill="#d2a8ff">GC:</tspan> -XX:+UseG1GC Low-Pause | <tspan fill="#f2cc60">ALLOCATION:</tspan> 512MB Deadlock-Free
      </text>
    </g>

    <!-- SUB-BOX A: DISTRIBUTED STORAGE LAYER (HDFS) [Width: 725] -->
    <g id="hdfs-storage-layer" transform="translate(30, 70)">
      <rect x="0" y="0" width="725" height="1000" rx="16" fill="#0d1117" stroke="#1f6feb" stroke-width="1.5" />
      
      <path d="M 0 16 Q 0 0 16 0 L 709 0 Q 725 0 725 16 L 725 46 L 0 46 Z" fill="#1f6feb" opacity="0.2" />
      <text x="25" y="30" class="heading" font-size="16" fill="#58a6ff">🗄️ HDFS DISTRIBUTED STORAGE LAYER</text>
      <rect x="575" y="10" width="130" height="26" rx="6" fill="#1f6feb" fill-opacity="0.3" stroke="#1f6feb" />
      <text x="640" y="27" class="badge" fill="#79c0ff" text-anchor="middle">RPC PORT: 9000</text>

      <!-- NameNode -->
      <g transform="translate(25, 55)">
        <rect x="0" y="0" width="675" height="265" rx="12" fill="#161b22" stroke="#388bfd" stroke-width="1.3" filter="url(#glowBlue)" />
        <rect x="15" y="14" width="220" height="28" rx="6" fill="#1f6feb" />
        <text x="125" y="32" class="heading" font-size="14" fill="#ffffff" text-anchor="middle">👑 NameNode (Master)</text>
        
        <rect x="525" y="14" width="135" height="28" rx="6" fill="#21262d" stroke="#30363d" />
        <text x="592" y="32" class="mono" font-size="12" fill="#79c0ff" text-anchor="middle">Web UI :9870</text>

        <text x="20" y="66" class="bold-text" font-size="13.5" fill="#e6edf3">Cluster Namespace Coordinator • Heap: 1024MB Max (G1GC)</text>
        
        <g transform="translate(20, 80)">
          <rect x="0" y="0" width="635" height="58" rx="8" fill="#0d1117" stroke="#21262d" />
          <text x="15" y="24" class="bold-text" font-size="12.5" fill="#58a6ff">🧠 In-Memory Namespace Tree (RAM)</text>
          <text x="15" y="44" class="body-text" font-size="11.5">Holds entire HDFS directory structure, file-to-block mapping, permissions, and quotas</text>
        </g>

        <g transform="translate(20, 148)">
          <g transform="translate(0, 0)">
            <rect x="0" y="0" width="310" height="100" rx="8" fill="#0d1117" stroke="#21262d" />
            <text x="14" y="24" class="bold-text" font-size="12" fill="#79c0ff">📄 fsimage (System Image)</text>
            <text x="14" y="46" class="body-text" font-size="11">Frozen checkpoint of directory tree</text>
            <text x="14" y="64" class="body-text" font-size="11">and block metadata serialized on disk</text>
            <text x="14" y="86" class="mono" font-size="10" fill="#58a6ff">dfs.namenode.name.dir</text>
          </g>
          <g transform="translate(325, 0)">
            <rect x="0" y="0" width="310" height="100" rx="8" fill="#0d1117" stroke="#21262d" />
            <text x="14" y="24" class="bold-text" font-size="12" fill="#79c0ff">📝 edits (Write-Ahead Journal)</text>
            <text x="14" y="46" class="body-text" font-size="11">Transaction log recording every file</text>
            <text x="14" y="64" class="body-text" font-size="11">creation, rename, replication change</text>
            <text x="14" y="86" class="mono" font-size="10" fill="#58a6ff">edits_inprogress_* log stream</text>
          </g>
        </g>
      </g>

      <!-- SecondaryNameNode -->
      <g transform="translate(25, 335)">
        <rect x="0" y="0" width="675" height="175" rx="12" fill="#161b22" stroke="#30363d" stroke-width="1.2" />
        <rect x="15" y="14" width="280" height="28" rx="6" fill="#21262d" stroke="#58a6ff" stroke-width="1" />
        <text x="155" y="32" class="bold-text" font-size="13" fill="#58a6ff" text-anchor="middle">🔄 SecondaryNameNode (Checkpointer)</text>

        <rect x="525" y="14" width="135" height="28" rx="6" fill="#21262d" stroke="#30363d" />
        <text x="592" y="32" class="mono" font-size="12" fill="#79c0ff" text-anchor="middle">HTTP :9868</text>

        <text x="20" y="68" class="bold-text" font-size="13" fill="#c9d1d9">State Consolidation &amp; Checkpointing Engine (Prevents Bloated Edits)</text>
        <text x="20" y="90" class="body-text" font-size="12">Periodically pulls <tspan class="mono" fill="#79c0ff">fsimage</tspan> and <tspan class="mono" fill="#79c0ff">edits</tspan> via HTTP, merges them in RAM, and ships</text>
        <text x="20" y="110" class="body-text" font-size="12">the fresh checkpoint image back to the Active NameNode for instant reboots.</text>

        <g transform="translate(20, 125)">
          <rect x="0" y="0" width="635" height="34" rx="6" fill="#0d1117" stroke="#21262d" />
          <text x="317" y="22" class="mono" font-size="11.5" fill="#388bfd" text-anchor="middle">
            Pull [fsimage + edits] ➔ Merge in Memory ➔ Push [fsimage.ckpt] ➔ Roll Edits
          </text>
        </g>
      </g>

      <!-- DataNode -->
      <g transform="translate(25, 525)">
        <rect x="0" y="0" width="675" height="295" rx="12" fill="#161b22" stroke="#388bfd" stroke-width="1.3" />
        <rect x="15" y="14" width="220" height="28" rx="6" fill="#1f6feb" />
        <text x="125" y="32" class="heading" font-size="14" fill="#ffffff" text-anchor="middle">📦 DataNode (Worker)</text>

        <rect x="500" y="14" width="160" height="28" rx="6" fill="#21262d" stroke="#30363d" />
        <text x="580" y="32" class="mono" font-size="12" fill="#79c0ff" text-anchor="middle">Transfer :9866 | UI :9864</text>

        <text x="20" y="68" class="bold-text" font-size="13.5" fill="#e6edf3">Physical Distributed Block Storage &amp; Integrity Verification</text>

        <g transform="translate(20, 85)">
          <g transform="translate(0, 0)">
            <rect x="0" y="0" width="200" height="100" rx="8" fill="#0d1117" stroke="#1f6feb" stroke-dasharray="3,3" />
            <text x="14" y="24" class="bold-text" font-size="12" fill="#58a6ff">🧱 Block 1 (128 MB)</text>
            <text x="14" y="46" class="mono" font-size="10.5" fill="#8b949e">blk_1073741825</text>
            <text x="14" y="68" class="body-text" font-size="10.5" fill="#3fb950">CRC32C Verified ✓</text>
            <text x="14" y="88" class="body-text" font-size="10" fill="#8b949e">Localhost Data Storage</text>
          </g>
          <g transform="translate(217, 0)">
            <rect x="0" y="0" width="200" height="100" rx="8" fill="#0d1117" stroke="#1f6feb" stroke-dasharray="3,3" />
            <text x="14" y="24" class="bold-text" font-size="12" fill="#58a6ff">🧱 Block 2 (128 MB)</text>
            <text x="14" y="46" class="mono" font-size="10.5" fill="#8b949e">blk_1073741826</text>
            <text x="14" y="68" class="body-text" font-size="10.5" fill="#3fb950">CRC32C Verified ✓</text>
            <text x="14" y="88" class="body-text" font-size="10" fill="#8b949e">Localhost Data Storage</text>
          </g>
          <g transform="translate(435, 0)">
            <rect x="0" y="0" width="200" height="100" rx="8" fill="#0d1117" stroke="#1f6feb" stroke-dasharray="3,3" />
            <text x="14" y="24" class="bold-text" font-size="12" fill="#58a6ff">🧱 Block 3 (Remainder)</text>
            <text x="14" y="46" class="mono" font-size="10.5" fill="#8b949e">blk_1073741827</text>
            <text x="14" y="68" class="body-text" font-size="10.5" fill="#3fb950">CRC32C Verified ✓</text>
            <text x="14" y="88" class="body-text" font-size="10" fill="#8b949e">Final Split Partition</text>
          </g>
        </g>

        <g transform="translate(20, 205)">
          <rect x="0" y="0" width="635" height="72" rx="8" fill="#0d1117" stroke="#21262d" />
          <text x="15" y="24" class="bold-text" font-size="12" fill="#c9d1d9">Heartbeat &amp; Block Reporting Pipeline:</text>
          <text x="15" y="46" class="body-text" font-size="11.5">• <tspan fill="#3fb950">Heartbeat (3s)</tspan>: Reports node liveness &amp; remaining volume capacity to NameNode.</text>
          <text x="15" y="64" class="body-text" font-size="11.5">• <tspan fill="#58a6ff">Block Report (6h)</tspan>: Transmits inventory of all active raw block IDs for replication check.</text>
        </g>
      </g>

      <!-- Step 6 Indicator Pill -->
      <g transform="translate(25, 840)">
        <rect x="0" y="0" width="675" height="135" rx="10" fill="#1f6feb" fill-opacity="0.1" stroke="#1f6feb" stroke-width="1.2" />
        <circle cx="35" cy="35" r="16" fill="#1f6feb" />
        <text x="35" y="35" class="step-num">6</text>
        <text x="65" y="35" class="bold-text" font-size="15" fill="#58a6ff">Checkpointing &amp; Zero Data-Loss Resilience</text>
        <text x="25" y="70" class="body-text" font-size="12.5">SecondaryNameNode merges transactions every 3600 seconds or 1,000,000 edits.</text>
        <text x="25" y="92" class="body-text" font-size="12.5">Ensures NameNode boots instantly without replaying gigabytes of transaction logs.</text>
        <text x="25" y="114" class="body-text" font-size="12.5">Protected against the legacy course typo <tspan class="mono" fill="#f85149">dfs.namemode</tspan> with dedicated persistent directories.</text>
      </g>
    </g>

    <!-- SUB-BOX B: COMPUTE & SCHEDULING LAYER (YARN) [Width: 725] -->
    <g id="yarn-compute-layer" transform="translate(785, 70)">
      <rect x="0" y="0" width="725" height="1000" rx="16" fill="#0d1117" stroke="#238636" stroke-width="1.5" />
      
      <path d="M 0 16 Q 0 0 16 0 L 709 0 Q 725 0 725 16 L 725 46 L 0 46 Z" fill="#238636" opacity="0.2" />
      <text x="25" y="30" class="heading" font-size="16" fill="#3fb950">⚙️ YARN RESOURCE &amp; COMPUTE ORCHESTRATION</text>
      <rect x="565" y="10" width="140" height="26" rx="6" fill="#238636" fill-opacity="0.3" stroke="#238636" />
      <text x="635" y="27" class="badge" fill="#7ee787" text-anchor="middle">IPC PORT: 8032</text>

      <!-- ResourceManager -->
      <g transform="translate(25, 55)">
        <rect x="0" y="0" width="675" height="265" rx="12" fill="#161b22" stroke="#2ea043" stroke-width="1.3" filter="url(#glowGreen)" />
        <rect x="15" y="14" width="250" height="28" rx="6" fill="#238636" />
        <text x="140" y="32" class="heading" font-size="14" fill="#ffffff" text-anchor="middle">🧠 ResourceManager (Master)</text>

        <rect x="525" y="14" width="135" height="28" rx="6" fill="#21262d" stroke="#30363d" />
        <text x="592" y="32" class="mono" font-size="12" fill="#7ee787" text-anchor="middle">Web UI :8088</text>

        <text x="20" y="66" class="bold-text" font-size="13.5" fill="#e6edf3">Cluster Resource Arbitration &amp; Scheduling • Pool: 3072MB (4 vCPUs)</text>

        <g transform="translate(20, 80)">
          <g transform="translate(0, 0)">
            <rect x="0" y="0" width="310" height="165" rx="8" fill="#0d1117" stroke="#21262d" />
            <text x="14" y="26" class="bold-text" font-size="12.5" fill="#56d364">📊 Pluggable Scheduler</text>
            <text x="14" y="48" class="body-text" font-size="11.5">• Capacity &amp; Fair allocation policies</text>
            <text x="14" y="68" class="body-text" font-size="11.5">• Min Allocation: 256 MB</text>
            <text x="14" y="88" class="body-text" font-size="11.5">• Max Allocation: 3072 MB</text>
            <text x="14" y="108" class="body-text" font-size="11.5">• Deadlock-free container balancing</text>
            <text x="14" y="132" class="mono" font-size="10.5" fill="#7ee787">Scheduler IPC: Port 8030</text>
          </g>
          <g transform="translate(325, 0)">
            <rect x="0" y="0" width="310" height="165" rx="8" fill="#0d1117" stroke="#21262d" />
            <text x="14" y="26" class="bold-text" font-size="12.5" fill="#56d364">🎯 ApplicationsManager (ASM)</text>
            <text x="14" y="48" class="body-text" font-size="11.5">• Accepts client job submissions</text>
            <text x="14" y="68" class="body-text" font-size="11.5">• Negotiates 1st container for AppMaster</text>
            <text x="14" y="88" class="body-text" font-size="11.5">• Restarts ApplicationMaster on fail</text>
            <text x="14" y="108" class="body-text" font-size="11.5">• Dispatches status to Client UI</text>
            <text x="14" y="132" class="mono" font-size="10.5" fill="#7ee787">ResourceTracker: Port 8031</text>
          </g>
        </g>
      </g>

      <!-- NodeManager & Containers -->
      <g transform="translate(25, 335)">
        <rect x="0" y="0" width="675" height="310" rx="12" fill="#161b22" stroke="#2ea043" stroke-width="1.3" />
        <rect x="15" y="14" width="220" height="28" rx="6" fill="#238636" />
        <text x="125" y="32" class="heading" font-size="14" fill="#ffffff" text-anchor="middle">👷 NodeManager (Worker)</text>

        <rect x="500" y="14" width="160" height="28" rx="6" fill="#21262d" stroke="#30363d" />
        <text x="580" y="32" class="mono" font-size="12" fill="#7ee787" text-anchor="middle">IPC :8040 | UI :8042</text>

        <text x="20" y="68" class="bold-text" font-size="13.5" fill="#e6edf3">Container Lifecycle Management &amp; Resource Telemetry</text>

        <g transform="translate(20, 82)">
          <!-- AM -->
          <g transform="translate(0, 0)">
            <rect x="0" y="0" width="200" height="135" rx="8" fill="#0d1117" stroke="#2ea043" stroke-width="1.2" />
            <rect x="10" y="10" width="180" height="22" rx="4" fill="#238636" fill-opacity="0.3" />
            <text x="100" y="25" class="badge" fill="#56d364" text-anchor="middle">ApplicationMaster (AM)</text>
            <text x="12" y="52" class="body-text" font-size="11">• Memory: 512 MB</text>
            <text x="12" y="70" class="body-text" font-size="11">• JVM: -Xmx400m G1GC</text>
            <text x="12" y="88" class="body-text" font-size="11">• Requests task slots</text>
            <text x="12" y="106" class="body-text" font-size="11">• Tracks job lifecycle</text>
            <text x="12" y="124" class="mono" font-size="10" fill="#3fb950">Container #001</text>
          </g>

          <!-- Map -->
          <g transform="translate(217, 0)">
            <rect x="0" y="0" width="200" height="135" rx="8" fill="#0d1117" stroke="#bc8cff" stroke-width="1.2" />
            <rect x="10" y="10" width="180" height="22" rx="4" fill="#8957e5" fill-opacity="0.3" />
            <text x="100" y="25" class="badge" fill="#d2a8ff" text-anchor="middle">MapTask (Split 0)</text>
            <text x="12" y="52" class="body-text" font-size="11">• Memory: 512 MB</text>
            <text x="12" y="70" class="body-text" font-size="11">• Data Locality: NODE</text>
            <text x="12" y="88" class="body-text" font-size="11">• Reads local Block 1</text>
            <text x="12" y="106" class="body-text" font-size="11">• Emits key-values</text>
            <text x="12" y="124" class="mono" font-size="10" fill="#bc8cff">Container #002</text>
          </g>

          <!-- Reduce -->
          <g transform="translate(435, 0)">
            <rect x="0" y="0" width="200" height="135" rx="8" fill="#0d1117" stroke="#bc8cff" stroke-width="1.2" />
            <rect x="10" y="10" width="180" height="22" rx="4" fill="#8957e5" fill-opacity="0.3" />
            <text x="100" y="25" class="badge" fill="#d2a8ff" text-anchor="middle">ReduceTask (Part 0)</text>
            <text x="12" y="52" class="body-text" font-size="11">• Memory: 512 MB</text>
            <text x="12" y="70" class="body-text" font-size="11">• Shuffle &amp; Sort phase</text>
            <text x="12" y="88" class="body-text" font-size="11">• Aggregates values</text>
            <text x="12" y="106" class="body-text" font-size="11">• Writes part-r-00000</text>
            <text x="12" y="124" class="mono" font-size="10" fill="#bc8cff">Container #003</text>
          </g>
        </g>

        <!-- Memory protection pill -->
        <g transform="translate(20, 226)">
          <rect x="0" y="0" width="635" height="70" rx="8" fill="#0d1117" stroke="#21262d" />
          <text x="15" y="24" class="bold-text" font-size="12" fill="#c9d1d9">Resource Monitoring &amp; Virtual Memory Protection:</text>
          <text x="15" y="44" class="body-text" font-size="11.5">• <tspan fill="#7ee787">vmem-check-enabled=false</tspan>: Prevents Java 11 glibc thread memory over-allocation kills.</text>
          <text x="15" y="60" class="body-text" font-size="11.5">• Total concurrent container demand: 1536 MB &lt; 3072 MB pool (Eliminates deadlock at reduce 0%).</text>
        </g>
      </g>

      <!-- JobHistoryServer -->
      <g transform="translate(25, 660)">
        <rect x="0" y="0" width="675" height="165" rx="12" fill="#161b22" stroke="#30363d" stroke-width="1.2" />
        <rect x="15" y="14" width="280" height="28" rx="6" fill="#21262d" stroke="#3fb950" stroke-width="1" />
        <text x="155" y="32" class="bold-text" font-size="13" fill="#3fb950" text-anchor="middle">📜 MapReduce JobHistoryServer (JHS)</text>

        <rect x="525" y="14" width="135" height="28" rx="6" fill="#21262d" stroke="#30363d" />
        <text x="592" y="32" class="mono" font-size="12" fill="#7ee787" text-anchor="middle">Web UI :19888</text>

        <text x="20" y="68" class="bold-text" font-size="13" fill="#c9d1d9">Historical Metrics, Log Aggregation &amp; Audit Trail</text>
        <text x="20" y="88" class="body-text" font-size="12">Collects finished application metrics, task counters, timeline data, and container logs</text>
        <text x="20" y="108" class="body-text" font-size="12">even after ApplicationMaster and compute worker containers have terminated.</text>
        <rect x="20" y="122" width="635" height="30" rx="5" fill="#0d1117" stroke="#21262d" />
        <text x="35" y="142" class="mono" font-size="11" fill="#7ee787">IPC Port: 10020 • History Dir: /tmp/hadoop-yarn/staging/history/done</text>
      </g>

      <!-- Step 2 Indicator Pill -->
      <g transform="translate(25, 840)">
        <rect x="0" y="0" width="675" height="135" rx="10" fill="#238636" fill-opacity="0.1" stroke="#238636" stroke-width="1.2" />
        <circle cx="35" cy="35" r="16" fill="#238636" />
        <text x="35" y="35" class="step-num">2</text>
        <text x="65" y="35" class="bold-text" font-size="15" fill="#56d364">Container Negotiation &amp; Scheduling Flow</text>
        <text x="25" y="70" class="body-text" font-size="12.5">ResourceManager arbitrates memory and spawns the ApplicationMaster container.</text>
        <text x="25" y="92" class="body-text" font-size="12.5">AM negotiates Map and Reduce task slots, prioritizing Data Locality (NODE_LOCAL).</text>
        <text x="25" y="114" class="body-text" font-size="12.5">Benchmarked: Monte Carlo Pi task finishes in 42.8s with 100% Map and Reduce execution.</text>
      </g>
    </g>
  </g>

  <!-- RIGHT COLUMN: ANALYTICS ENGINES & GOOGLE CLOUD SUITE (Width: 520) -->
  <g id="analytics-engines-layer" transform="translate(2220, 390)">
    <rect x="0" y="0" width="520" height="1100" rx="16" fill="url(#cardGrad)" stroke="#8957e5" stroke-width="1.5" stroke-dasharray="6,4" filter="url(#shadow)" />

    <path d="M 0 16 Q 0 0 16 0 L 504 0 Q 520 0 520 16 L 520 54 L 0 54 Z" fill="url(#engineGrad)" opacity="0.15" />
    <rect x="20" y="14" width="300" height="26" rx="6" fill="#8957e5" />
    <text x="170" y="32" class="heading" font-size="13" fill="#ffffff" text-anchor="middle">⚡ ANALYTICS &amp; CLOUD ENGINES</text>
    <text x="20" y="80" class="subheading" font-size="15" fill="#bc8cff">Programming Models &amp; Cloud</text>
    <text x="20" y="100" class="body-text" font-size="13">Supported frameworks in <tspan class="mono" fill="#d2a8ff">examples/</tspan> &amp; <tspan class="mono" fill="#d2a8ff">scripts/gcp/</tspan></text>

    <!-- Engine 1: Spark -->
    <g transform="translate(20, 120)">
      <rect x="0" y="0" width="480" height="160" rx="12" fill="#0d1117" stroke="#30363d" stroke-width="1.2" />
      <text x="20" y="30" class="bold-text" font-size="15" fill="#f85149">🔥 Apache Spark &amp; PySpark</text>
      <text x="20" y="52" class="body-text" font-size="12">In-memory distributed DataFrame processing on HDFS:</text>

      <rect x="18" y="65" width="444" height="48" rx="6" fill="#161b22" />
      <text x="28" y="84" class="mono" font-size="11" fill="#79c0ff">df = spark.read.csv("hdfs://localhost:9000/data/emp.csv")</text>
      <text x="28" y="102" class="mono" font-size="11" fill="#3fb950">df.groupBy("dept").count().write.parquet("hdfs://...")</text>

      <text x="20" y="140" class="mono" font-size="11" fill="#bc8cff">examples/spark-pyspark/pyspark_hdfs_read_write.py</text>
    </g>

    <!-- Engine 2: GCP Dataproc -->
    <g transform="translate(20, 295)">
      <rect x="0" y="0" width="480" height="165" rx="12" fill="#0d1117" stroke="#38bdf8" stroke-width="1.2" />
      <text x="20" y="30" class="bold-text" font-size="15" fill="#38bdf8">☁️ Google Cloud Dataproc (GCP)</text>
      <text x="20" y="52" class="body-text" font-size="12">Fully managed, auto-deleting cloud Hadoop clusters:</text>

      <rect x="18" y="65" width="444" height="50" rx="6" fill="#161b22" />
      <text x="28" y="84" class="mono" font-size="11" fill="#79c0ff">gcloud dataproc clusters create hadoop-cluster-lab</text>
      <text x="28" y="102" class="mono" font-size="11" fill="#56d364">--bucket=gs://my-bucket --enable-component-gateway</text>

      <text x="20" y="142" class="mono" font-size="11" fill="#38bdf8">scripts/gcp/create-dataproc-cluster.sh • 30m idle</text>
    </g>

    <!-- Engine 3: Native Java MapReduce -->
    <g transform="translate(20, 475)">
      <rect x="0" y="0" width="480" height="160" rx="12" fill="#0d1117" stroke="#30363d" stroke-width="1.2" />
      <text x="20" y="30" class="bold-text" font-size="15" fill="#bc8cff">☕ Native Java MapReduce</text>
      <text x="20" y="52" class="body-text" font-size="12">Enterprise compiled JAR application execution:</text>

      <rect x="18" y="65" width="444" height="48" rx="6" fill="#161b22" />
      <text x="28" y="84" class="mono" font-size="11" fill="#58a6ff">hadoop jar hadoop-mapreduce-examples-*.jar pi 2 10</text>
      <text x="28" y="102" class="mono" font-size="11" fill="#7ee787">javac -cp $(hadoop classpath) -d . WordCount.java</text>

      <text x="20" y="140" class="mono" font-size="11" fill="#bc8cff">examples/mapreduce-java/compile-and-run.sh</text>
    </g>

    <!-- Engine 4: Python Hadoop Streaming -->
    <g transform="translate(20, 650)">
      <rect x="0" y="0" width="480" height="155" rx="12" fill="#0d1117" stroke="#30363d" stroke-width="1.2" />
      <text x="20" y="30" class="bold-text" font-size="15" fill="#58a6ff">🐍 Python Hadoop Streaming</text>
      <text x="20" y="52" class="body-text" font-size="12">UNIX pipeline streaming mapper.py &amp; reducer.py:</text>

      <rect x="18" y="65" width="444" height="45" rx="6" fill="#161b22" />
      <text x="28" y="84" class="mono" font-size="11" fill="#79c0ff">cat data.txt | python mapper.py | sort |</text>
      <text x="28" y="100" class="mono" font-size="11" fill="#7ee787">python reducer.py  (Packaged via hadoop-streaming)</text>

      <text x="20" y="136" class="mono" font-size="11" fill="#bc8cff">examples/mapreduce-python/run.sh</text>
    </g>

    <!-- Step 4 & 5 Indicator Pill -->
    <g transform="translate(20, 820)">
      <rect x="0" y="0" width="480" height="260" rx="12" fill="#8957e5" fill-opacity="0.1" stroke="#8957e5" stroke-width="1.2" />
      <circle cx="35" cy="35" r="16" fill="#8957e5" />
      <text x="35" y="35" class="step-num">4</text>
      <text x="65" y="35" class="bold-text" font-size="15" fill="#bc8cff">Task Execution &amp; Shuffling</text>
      
      <text x="25" y="70" class="body-text" font-size="12.5">• Mapper containers execute code on local HDFS blocks.</text>
      <text x="25" y="92" class="body-text" font-size="12.5">• Intermediate key-values partitioned and sorted in memory.</text>
      <text x="25" y="114" class="body-text" font-size="12.5">• Network shuffle routes partitions to Reducer tasks.</text>

      <circle cx="35" cy="155" r="16" fill="#8957e5" />
      <text x="35" y="155" class="step-num">5</text>
      <text x="65" y="155" class="bold-text" font-size="15" fill="#bc8cff">Result Aggregation &amp; Output</text>
      <text x="25" y="185" class="body-text" font-size="12.5">Reducers aggregate groups and write <tspan class="mono" fill="#d2a8ff">part-r-00000</tspan></text>
      <text x="25" y="205" class="body-text" font-size="12.5">directly back to HDFS DataNode (or GCS <tspan class="mono" fill="#38bdf8">gs://</tspan> bucket).</text>
      <text x="25" y="232" class="mono" font-size="11" fill="#3fb950">Status verified: SUCCESS across 54 MapReduce counters.</text>
    </g>
  </g>

  <!-- ========================================================================= -->
  <!-- 4. BOTTOM PERSISTENCE SECTION                                             -->
  <!-- ========================================================================= -->
  <g id="docker-volumes-section" transform="translate(60, 1515)">
    <rect x="0" y="0" width="2680" height="180" rx="16" fill="url(#cardGrad)" stroke="#da3633" stroke-width="1.5" filter="url(#shadow)" />

    <path d="M 0 16 Q 0 0 16 0 L 16 0 L 16 180 L 0 180 Z" fill="url(#volGrad)" />
    <rect x="30" y="16" width="310" height="28" rx="6" fill="#da3633" fill-opacity="0.2" stroke="#da3633" stroke-width="1.2" />
    <text x="185" y="35" class="heading" font-size="13" fill="#f85149" text-anchor="middle">💾 PERSISTENT DISTRIBUTED STORAGE</text>
    <text x="360" y="35" class="body-text" font-size="13">Zero Data Loss: Named Docker Volumes &amp; Google Cloud Storage Buckets (gs://)</text>

    <g transform="translate(2540, 20)">
      <circle cx="20" cy="20" r="18" fill="#da3633" />
      <text x="20" y="20" class="step-num">7</text>
    </g>

    <g transform="translate(30, 60)">
      <g transform="translate(0, 0)">
        <rect x="0" y="0" width="635" height="95" rx="10" fill="#0d1117" stroke="#30363d" stroke-width="1.2" />
        <text x="18" y="28" class="bold-text" font-size="13" fill="#58a6ff">📁 hadoop_namenode_data</text>
        <text x="18" y="50" class="mono" font-size="11.5" fill="#79c0ff">Container: /usr/local/hadoop/hdfs/namenode</text>
        <text x="18" y="74" class="body-text" font-size="11.5">Stores filesystem namespace tree, fsimage snapshots, and edits transaction logs</text>
      </g>

      <g transform="translate(660, 0)">
        <rect x="0" y="0" width="635" height="95" rx="10" fill="#0d1117" stroke="#30363d" stroke-width="1.2" />
        <text x="18" y="28" class="bold-text" font-size="13" fill="#58a6ff">🧱 hadoop_datanode_data</text>
        <text x="18" y="50" class="mono" font-size="11.5" fill="#79c0ff">Container: /usr/local/hadoop/hdfs/datanode</text>
        <text x="18" y="74" class="body-text" font-size="11.5">Stores actual raw 128MB replicated data blocks (blk_* and blk_*.meta checksums)</text>
      </g>

      <g transform="translate(1320, 0)">
        <rect x="0" y="0" width="635" height="95" rx="10" fill="#0d1117" stroke="#30363d" stroke-width="1.2" />
        <text x="18" y="28" class="bold-text" font-size="13" fill="#3fb950">📦 hadoop_tmp_data &amp; GCS Staging</text>
        <text x="18" y="50" class="mono" font-size="11.5" fill="#7ee787">Path: /app/hadoop/tmp | gs://bucket/staging</text>
        <text x="18" y="74" class="body-text" font-size="11.5">MapReduce spill buffers, intermediate shuffle partitions, and cloud staging data</text>
      </g>

      <g transform="translate(1980, 0)">
        <rect x="0" y="0" width="640" height="95" rx="10" fill="#0d1117" stroke="#30363d" stroke-width="1.2" />
        <text x="18" y="28" class="bold-text" font-size="13" fill="#bc8cff">📜 hadoop_logs_data</text>
        <text x="18" y="50" class="mono" font-size="11.5" fill="#d2a8ff">Container: /usr/local/hadoop/logs</text>
        <text x="18" y="74" class="body-text" font-size="11.5">Daemon stdout/stderr logs for NameNode, DataNode, RM, NM, and JobHistoryServer</text>
      </g>
    </g>
  </g>

  <!-- ========================================================================= -->
  <!-- 5. BOTTOM FOOTER BAR                                                      -->
  <!-- ========================================================================= -->
  <g id="footer-bar" transform="translate(60, 1720)">
    <rect x="0" y="0" width="2680" height="85" rx="12" fill="#151b28" stroke="#30363d" stroke-width="1.2" />
    
    <text x="30" y="32" class="bold-text" font-size="13.5" fill="#ffffff">ENTERPRISE ARCHITECTURE SPECIFICATIONS SUMMARY:</text>
    <text x="30" y="58" class="body-text" font-size="12">
      • <tspan fill="#58a6ff">HDFS Block Size:</tspan> 128 MB | <tspan fill="#3fb950">Replication Factor:</tspan> 1 (Dev) / 3 (Prod) | <tspan fill="#d2a8ff">YARN Alloc:</tspan> 512MB/task (3072MB pool) | <tspan fill="#f2cc60">JVM GC:</tspan> -XX:+UseG1GC Low-Pause | <tspan fill="#38bdf8">Cloud:</tspan> Dataproc 2.1
    </text>

    <text x="2650" y="34" class="mono" font-size="12" fill="#58a6ff" text-anchor="end">https://github.com/Sohila-Khaled-Abbas/docker-hadoop</text>
    <text x="2650" y="58" class="body-text" font-size="11" fill="#6e7681" text-anchor="end">Distributed Big Data Engineering &amp; Distributed Systems Education • Apache 2.0 Licensed</text>
  </g>

  <!-- Connectors -->
  <path d="M 580 575 C 610 575, 620 480, 660 480" fill="none" stroke="#58a6ff" stroke-width="3" marker-end="url(#arrowBlue)" stroke-dasharray="8,4" />
  <path d="M 580 620 C 850 620, 1100 480, 1425 480" fill="none" stroke="#3fb950" stroke-width="3" marker-end="url(#arrowGreen)" stroke-dasharray="8,4" />
  <path d="M 1750 690 L 1750 720" fill="none" stroke="#3fb950" stroke-width="3" marker-end="url(#arrowGreen)" />
  <path d="M 1430 840 C 1370 840, 1370 840, 1315 840" fill="none" stroke="#388bfd" stroke-width="3" marker-end="url(#arrowBlue)" />
  <path d="M 2135 840 C 2180 840, 2180 620, 2220 620" fill="none" stroke="#bc8cff" stroke-width="3" marker-end="url(#arrowPurple)" stroke-dasharray="6,4" />
  <path d="M 2220 740 C 1850 740, 1400 960, 1315 960" fill="none" stroke="#388bfd" stroke-width="3" marker-end="url(#arrowBlue)" stroke-dasharray="6,4" />
  <path d="M 980 1445 L 980 1515" fill="none" stroke="#f85149" stroke-width="3" marker-end="url(#arrowRed)" />
  <path d="M 1750 1445 L 1750 1515" fill="none" stroke="#f85149" stroke-width="3" marker-end="url(#arrowRed)" />
</svg>'''

# ==============================================================================
# 2. GENERATE SYSTEM ARCHITECTURE DEEP DIVE BLUEPRINT SVG
# ==============================================================================
architecture_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2800 1920" width="2800" height="1920">
  <defs>
{COMMON_DEFS}
  </defs>

  <style>
{COMMON_STYLES}
  </style>

  <!-- Background Base -->
  <rect width="2800" height="1920" fill="url(#bgGrad)" />
  <rect width="2800" height="1920" fill="url(#grid)" opacity="0.95" />

  <!-- Outer Frame -->
  <rect x="25" y="25" width="2750" height="1870" rx="24" fill="none" stroke="#21262d" stroke-width="2" />

  <!-- ========================================================================= -->
  <!-- 1. HEADER SECTION                                                         -->
  <!-- ========================================================================= -->
  <g id="arch-header" transform="translate(60, 50)">
    <rect x="0" y="0" width="2680" height="135" rx="16" fill="#151b28" stroke="#30363d" stroke-width="1.5" filter="url(#shadow)" />
    <path d="M 0 16 Q 0 0 16 0 L 22 0 L 22 135 L 16 135 Q 0 135 0 119 Z" fill="url(#headerGrad)" />

    <text x="48" y="54" class="title" font-size="31" letter-spacing="0.5">
      🏛️ APACHE HADOOP 3.3.6 &amp; 3.1.2 INTERNAL SYSTEM ARCHITECTURE BLUEPRINT
    </text>
    <text x="48" y="90" class="subtitle" font-size="15">
      Low-Level Protocol Architecture • Inode Memory Graphs • YARN Resource Pools • Pipeline Stages • Zero Data Corruption
    </text>

    <!-- Architecture Badges Row -->
    <g transform="translate(1380, 36)">
      <g transform="translate(0, 0)">
        <rect x="0" y="0" width="180" height="34" rx="8" fill="#1f6feb" fill-opacity="0.2" stroke="#388bfd" stroke-width="1.2" />
        <text x="90" y="22" class="badge" fill="#58a6ff" text-anchor="middle">PROTOBUF RPC :9000</text>
      </g>
      <g transform="translate(195, 0)">
        <rect x="0" y="0" width="185" height="34" rx="8" fill="#238636" fill-opacity="0.2" stroke="#3fb950" stroke-width="1.2" />
        <text x="92" y="22" class="badge" fill="#56d364" text-anchor="middle">IPC SCHEDULER :8030</text>
      </g>
      <g transform="translate(395, 0)">
        <rect x="0" y="0" width="175" height="34" rx="8" fill="#8957e5" fill-opacity="0.2" stroke="#bc8cff" stroke-width="1.2" />
        <text x="87" y="22" class="badge" fill="#d2a8ff" text-anchor="middle">SHUFFLE-SORT ENGINE</text>
      </g>
      <g transform="translate(585, 0)">
        <rect x="0" y="0" width="165" height="34" rx="8" fill="#0284c7" fill-opacity="0.2" stroke="#38bdf8" stroke-width="1.2" />
        <text x="82" y="22" class="badge" fill="#38bdf8" text-anchor="middle">LOW-PAUSE G1GC</text>
      </g>
      <g transform="translate(765, 0)">
        <rect x="0" y="0" width="180" height="34" rx="8" fill="#da3633" fill-opacity="0.2" stroke="#f85149" stroke-width="1.2" />
        <text x="90" y="22" class="badge" fill="#f85149" text-anchor="middle">128MB CRC32C BLOCKS</text>
      </g>
      <text x="945" y="72" class="body-text" font-size="12" fill="#8b949e" text-anchor="end">
        Production-Ready Multi-Platform Reference Implementation
      </text>
    </g>
  </g>

  <!-- ========================================================================= -->
  <!-- 2. PROTOCOL & NETWORK BUS LAYER (4 PILLARS ACROSS 2680px)                 -->
  <!-- ========================================================================= -->
  <g id="protocol-layer" transform="translate(60, 205)">
    <rect x="0" y="0" width="2680" height="165" rx="16" fill="url(#cardGrad)" stroke="#30363d" stroke-width="1.5" filter="url(#shadow)" />
    
    <rect x="25" y="16" width="340" height="28" rx="6" fill="#388bfd" fill-opacity="0.15" stroke="#388bfd" stroke-width="1" />
    <text x="195" y="35" class="subheading" font-size="13" fill="#58a6ff" text-anchor="middle">🌐 4 CORE WIRE PROTOCOLS &amp; BUS TOPOLOGY</text>

    <!-- Pillar 1: RPC Protocol -->
    <g transform="translate(25, 55)">
      <rect x="0" y="0" width="640" height="95" rx="10" fill="#0d1117" stroke="#388bfd" stroke-width="1.2" />
      <text x="16" y="26" class="bold-text" font-size="13.5" fill="#58a6ff">🔌 Hadoop RPC (Protobuf over TCP :9000)</text>
      <text x="16" y="48" class="body-text" font-size="11.5">Client &amp; external frameworks (Spark/PySpark) send filesystem requests to NameNode.</text>
      <rect x="16" y="60" width="608" height="22" rx="4" fill="#161b22" />
      <text x="24" y="75" class="mono" font-size="10.5" fill="#79c0ff">ClientProtocol.proto • SafeMode checks • Inodes lookup • Block allocation leases</text>
    </g>

    <!-- Pillar 2: Data Transfer Protocol -->
    <g transform="translate(685, 55)">
      <rect x="0" y="0" width="640" height="95" rx="10" fill="#0d1117" stroke="#3fb950" stroke-width="1.2" />
      <text x="16" y="26" class="bold-text" font-size="13.5" fill="#56d364">🌊 Streaming Block Protocol (:9866 Data Transfer)</text>
      <text x="16" y="48" class="body-text" font-size="11.5">High-throughput TCP streaming pipeline with 64KB data packets and ACK back-propagation.</text>
      <rect x="16" y="60" width="608" height="22" rx="4" fill="#161b22" />
      <text x="24" y="75" class="mono" font-size="10.5" fill="#7ee787">DataTransferProtocol.proto • OP_WRITE_BLOCK • OP_READ_BLOCK • CRC32C Checksums</text>
    </g>

    <!-- Pillar 3: YARN Protocol -->
    <g transform="translate(1345, 55)">
      <rect x="0" y="0" width="640" height="95" rx="10" fill="#0d1117" stroke="#bc8cff" stroke-width="1.2" />
      <text x="16" y="26" class="bold-text" font-size="13.5" fill="#d2a8ff">⚙️ YARN ApplicationMaster Protocol (:8030 / :8032)</text>
      <text x="16" y="48" class="body-text" font-size="11.5">ApplicationMaster heartbeats, resource slot negotiation, and container token grants.</text>
      <rect x="16" y="60" width="608" height="22" rx="4" fill="#161b22" />
      <text x="24" y="75" class="mono" font-size="10.5" fill="#bc8cff">ApplicationClientProtocol • ApplicationMasterProtocol • ContainerManagementProtocol</text>
    </g>

    <!-- Pillar 4: Web Consoles -->
    <g transform="translate(2005, 55)">
      <rect x="0" y="0" width="650" height="95" rx="10" fill="#0d1117" stroke="#38bdf8" stroke-width="1.2" />
      <text x="16" y="26" class="bold-text" font-size="13.5" fill="#38bdf8">🌐 Administrative Web Consoles &amp; REST APIs</text>
      <text x="16" y="48" class="body-text" font-size="11.5">WebHDFS REST API, JMX health metrics, and browser management consoles.</text>
      <rect x="16" y="60" width="618" height="22" rx="4" fill="#161b22" />
      <text x="24" y="75" class="mono" font-size="10.5" fill="#38bdf8">NN :9870 • RM :8088 • JHS :19888 • DN :9864 • NM :8042 • GCP Component Gateway</text>
    </g>
  </g>

  <!-- ========================================================================= -->
  <!-- 3. DEEP ARCHITECTURAL SUBSYSTEMS (2 EQUAL COLUMNS: HDFS & YARN)           -->
  <!-- ========================================================================= -->

  <!-- LEFT COLUMN: HDFS STORAGE SUBSYSTEMS (Width: 1320) -->
  <g id="hdfs-subsystems" transform="translate(60, 390)">
    <rect x="0" y="0" width="1320" height="1100" rx="18" fill="url(#cardGrad)" stroke="#1f6feb" stroke-width="1.8" filter="url(#shadow)" />
    
    <path d="M 0 18 Q 0 0 18 0 L 1302 0 Q 1320 0 1320 18 L 1320 54 L 0 54 Z" fill="url(#hdfsGrad)" opacity="0.2" />
    <rect x="25" y="14" width="370" height="28" rx="6" fill="#1f6feb" />
    <text x="210" y="33" class="heading" font-size="13" fill="#ffffff" text-anchor="middle">🗄️ HDFS INTERNALS &amp; METADATA SUBSYSTEMS</text>
    <text x="415" y="34" class="subheading" font-size="13" fill="#58a6ff">Hadoop 3.3.6 / 3.1.2 Distributed Storage Engine</text>

    <!-- Subsystem 1: NameNode Memory & Journal (Height: 495) -->
    <g transform="translate(25, 70)">
      <rect x="0" y="0" width="1270" height="495" rx="14" fill="#0d1117" stroke="#388bfd" stroke-width="1.3" filter="url(#glowBlue)" />
      
      <rect x="18" y="14" width="260" height="28" rx="6" fill="#1f6feb" />
      <text x="148" y="32" class="heading" font-size="13.5" fill="#ffffff" text-anchor="middle">👑 NameNode Internal Architecture</text>
      <text x="295" y="33" class="mono" font-size="12" fill="#79c0ff">Heap: -Xmx1024m (Low-Pause G1GC) • RPC :9000 • Web :9870</text>

      <!-- In-Memory Inodes Tree (Left half, width 610) -->
      <g transform="translate(18, 55)">
        <rect x="0" y="0" width="610" height="255" rx="10" fill="#161b22" stroke="#21262d" />
        <text x="18" y="28" class="bold-text" font-size="13.5" fill="#58a6ff">🧠 In-Memory Namespace Graph (RAM)</text>
        <text x="18" y="50" class="body-text" font-size="11.5">Direct pointer graph representation of directory hierarchy:</text>

        <rect x="16" y="62" width="578" height="30" rx="5" fill="#0d1117" stroke="#1f6feb" stroke-width="0.8" />
        <text x="26" y="81" class="mono" font-size="11" fill="#79c0ff">INodeDirectory: /user/hduser/ (Permissions: 0755, Quotas)</text>

        <rect x="16" y="98" width="578" height="48" rx="5" fill="#0d1117" stroke="#1f6feb" stroke-width="0.8" />
        <text x="26" y="117" class="mono" font-size="11" fill="#58a6ff">INodeFile: /data/wordcount-sample.txt</text>
        <text x="26" y="135" class="body-text" font-size="10.5" fill="#8b949e">Replication: 1 • Size: 268MB • Block List: [blk_1073741825, blk_1073741826, ...]</text>

        <rect x="16" y="152" width="578" height="52" rx="5" fill="#0d1117" stroke="#21262d" />
        <text x="26" y="171" class="bold-text" font-size="11" fill="#c9d1d9">Block-to-DataNode Mapping Table (Dynamic):</text>
        <text x="26" y="190" class="mono" font-size="10.5" fill="#3fb950">blk_1073741825 ➔ [DataNode 192.168.13.128:9866 (Active, StorageID: DS-xxx)]</text>

        <text x="18" y="235" class="body-text" font-size="11" fill="#8b949e">
          RAM cost: ~150 bytes per object. 1 GB Heap supports &gt; 7 million files and blocks without GC stutter.
        </text>
      </g>

      <!-- Disk Journal & Checkpointing (Right half, width 610) -->
      <g transform="translate(642, 55)">
        <rect x="0" y="0" width="610" height="255" rx="10" fill="#161b22" stroke="#21262d" />
        <text x="18" y="28" class="bold-text" font-size="13.5" fill="#58a6ff">💾 Persistent Disk Metadata &amp; Journal</text>
        <text x="18" y="50" class="body-text" font-size="11.5">ACID Write-Ahead Journal &amp; Periodic Snapshot Images:</text>

        <rect x="16" y="62" width="578" height="42" rx="5" fill="#0d1117" stroke="#21262d" />
        <text x="26" y="80" class="mono" font-size="11" fill="#79c0ff">fsimage_0000000000000000054 (Checkpoint Snapshot)</text>
        <text x="26" y="96" class="body-text" font-size="10.5" fill="#8b949e">Complete frozen directory tree and block attributes serialized via Protobuf.</text>

        <rect x="16" y="110" width="578" height="42" rx="5" fill="#0d1117" stroke="#21262d" />
        <text x="26" y="128" class="mono" font-size="11" fill="#e3b341">edits_inprogress_0000000000000000055 (Active WAL Journal)</text>
        <text x="26" y="144" class="body-text" font-size="10.5" fill="#8b949e">Sequential stream recording every file creation, append, rename, and permission edit.</text>

        <rect x="16" y="158" width="578" height="46" rx="5" fill="#0d1117" stroke="#21262d" />
        <text x="26" y="176" class="mono" font-size="11" fill="#3fb950">dfs.namenode.name.dir = file:///usr/local/hadoop/hdfs/namenode</text>
        <text x="26" y="194" class="body-text" font-size="10.5" fill="#8b949e">Protected by non-root execution and backed into Docker volume / persistent virtual disk.</text>

        <text x="18" y="235" class="body-text" font-size="11" fill="#8b949e">
          Zero Data Loss: Edits committed to disk synchronously before acknowledging client writes.
        </text>
      </g>

      <!-- SafeMode & SecondaryNameNode Checkpoint Pipeline (Bottom full width) -->
      <g transform="translate(18, 320)">
        <rect x="0" y="0" width="1234" height="155" rx="10" fill="#161b22" stroke="#21262d" />
        <text x="18" y="28" class="bold-text" font-size="13" fill="#ffffff">🔄 SecondaryNameNode 2-Way Checkpoint Pipeline &amp; SafeMode Guardian:</text>

        <g transform="translate(18, 42)">
          <rect x="0" y="0" width="285" height="95" rx="8" fill="#0d1117" stroke="#388bfd" />
          <text x="14" y="24" class="bold-text" font-size="12" fill="#58a6ff">1. HTTP Pull (Port :9868)</text>
          <text x="14" y="44" class="body-text" font-size="11">Periodically downloads current</text>
          <text x="14" y="60" class="mono" font-size="10.5" fill="#79c0ff">fsimage</text>
          <text x="68" y="60" class="body-text" font-size="11">and</text>
          <text x="96" y="60" class="mono" font-size="10.5" fill="#79c0ff">edits</text>
          <text x="135" y="60" class="body-text" font-size="11">from Active NN.</text>
          <text x="14" y="80" class="body-text" font-size="10.5" fill="#8b949e">Every 3600s or 1M txns.</text>
        </g>

        <g transform="translate(320, 42)">
          <rect x="0" y="0" width="285" height="95" rx="8" fill="#0d1117" stroke="#bc8cff" />
          <text x="14" y="24" class="bold-text" font-size="12" fill="#bc8cff">2. In-Memory Replay</text>
          <text x="14" y="44" class="body-text" font-size="11">Replays transactions into</text>
          <text x="14" y="60" class="body-text" font-size="11">fresh in-memory namespace.</text>
          <text x="14" y="80" class="mono" font-size="10.5" fill="#d2a8ff">Produces fsimage.ckpt</text>
        </g>

        <g transform="translate(620, 42)">
          <rect x="0" y="0" width="285" height="95" rx="8" fill="#0d1117" stroke="#3fb950" />
          <text x="14" y="24" class="bold-text" font-size="12" fill="#3fb950">3. Push Back &amp; Roll</text>
          <text x="14" y="44" class="body-text" font-size="11">Uploads merged checkpoint</text>
          <text x="14" y="60" class="body-text" font-size="11">back to NameNode via HTTP.</text>
          <text x="14" y="80" class="mono" font-size="10.5" fill="#7ee787">NN rolls edit log instantly.</text>
        </g>

        <g transform="translate(920, 42)">
          <rect x="0" y="0" width="295" height="95" rx="8" fill="#0d1117" stroke="#d29922" />
          <text x="14" y="24" class="bold-text" font-size="12" fill="#e3b341">4. SafeMode Threshold</text>
          <text x="14" y="44" class="body-text" font-size="11">Read-only state on boot until</text>
          <text x="14" y="60" class="body-text" font-size="11">99.9% blocks are reported:</text>
          <text x="14" y="80" class="mono" font-size="10.5" fill="#f2cc60">hdfs dfsadmin -safemode wait</text>
        </g>
      </g>
    </g>

    <!-- Subsystem 2: DataNode Storage & CRC32C Integrity (Height: 495) -->
    <g transform="translate(25, 580)">
      <rect x="0" y="0" width="1270" height="495" rx="14" fill="#0d1117" stroke="#388bfd" stroke-width="1.3" />
      
      <rect x="18" y="14" width="260" height="28" rx="6" fill="#1f6feb" />
      <text x="148" y="32" class="heading" font-size="13.5" fill="#ffffff" text-anchor="middle">📦 DataNode Physical Storage Engine</text>
      <text x="295" y="33" class="mono" font-size="12" fill="#79c0ff">Transfer :9866 • Web UI :9864 • Block Size: 128MB • Non-Root hduser:1000</text>

      <!-- 3 Physical Disk Blocks -->
      <g transform="translate(18, 55)">
        <g transform="translate(0, 0)">
          <rect x="0" y="0" width="395" height="235" rx="10" fill="#161b22" stroke="#21262d" />
          <text x="18" y="28" class="bold-text" font-size="13.5" fill="#58a6ff">🧱 Block 1 (128 MB Raw Chunk)</text>
          <text x="18" y="50" class="mono" font-size="11" fill="#8b949e">File: blk_1073741825 (134,217,728 bytes)</text>
          
          <rect x="16" y="65" width="363" height="45" rx="6" fill="#0d1117" />
          <text x="24" y="84" class="mono" font-size="10.5" fill="#3fb950">blk_1073741825_1001.meta</text>
          <text x="24" y="100" class="body-text" font-size="10" fill="#8b949e">CRC32C Checksums (4 bytes per 512-byte slice)</text>

          <text x="18" y="135" class="body-text" font-size="11.5">• Physical Path in volume:</text>
          <text x="28" y="153" class="mono" font-size="10" fill="#79c0ff">current/BP-123/current/finalized/subdir0/subdir0/</text>

          <text x="18" y="180" class="body-text" font-size="11.5">• Block Scanner Periodic Verification:</text>
          <text x="28" y="198" class="body-text" font-size="11" fill="#3fb950">Validated every 504 hours (Zero bit-rot guarantee)</text>

          <text x="18" y="222" class="mono" font-size="10.5" fill="#58a6ff">Status: HEALTHY • 0 Missing • 0 Corrupt</text>
        </g>

        <g transform="translate(418, 0)">
          <rect x="0" y="0" width="395" height="235" rx="10" fill="#161b22" stroke="#21262d" />
          <text x="18" y="28" class="bold-text" font-size="13.5" fill="#58a6ff">🧱 Block 2 (128 MB Raw Chunk)</text>
          <text x="18" y="50" class="mono" font-size="11" fill="#8b949e">File: blk_1073741826 (134,217,728 bytes)</text>
          
          <rect x="16" y="65" width="363" height="45" rx="6" fill="#0d1117" />
          <text x="24" y="84" class="mono" font-size="10.5" fill="#3fb950">blk_1073741826_1002.meta</text>
          <text x="24" y="100" class="body-text" font-size="10" fill="#8b949e">CRC32C Checksums (4 bytes per 512-byte slice)</text>

          <text x="18" y="135" class="body-text" font-size="11.5">• Physical Path in volume:</text>
          <text x="28" y="153" class="mono" font-size="10" fill="#79c0ff">current/BP-123/current/finalized/subdir0/subdir0/</text>

          <text x="18" y="180" class="body-text" font-size="11.5">• Streaming Transfer Protocol (:9866):</text>
          <text x="28" y="198" class="body-text" font-size="11" fill="#3fb950">Streams 64KB packets with zero-copy splicing</text>

          <text x="18" y="222" class="mono" font-size="10.5" fill="#58a6ff">Status: HEALTHY • 0 Missing • 0 Corrupt</text>
        </g>

        <g transform="translate(836, 0)">
          <rect x="0" y="0" width="395" height="235" rx="10" fill="#161b22" stroke="#21262d" />
          <text x="18" y="28" class="bold-text" font-size="13.5" fill="#58a6ff">🧱 Block 3 (Remainder Partition)</text>
          <text x="18" y="50" class="mono" font-size="11" fill="#8b949e">File: blk_1073741827 (12,410,210 bytes)</text>
          
          <rect x="16" y="65" width="363" height="45" rx="6" fill="#0d1117" />
          <text x="24" y="84" class="mono" font-size="10.5" fill="#3fb950">blk_1073741827_1003.meta</text>
          <text x="24" y="100" class="body-text" font-size="10" fill="#8b949e">Tail split partition checksummed to EOF</text>

          <text x="18" y="135" class="body-text" font-size="11.5">• Space Efficiency:</text>
          <text x="28" y="153" class="body-text" font-size="11" fill="#c9d1d9">Consumes only actual bytes used (12MB on disk)</text>

          <text x="18" y="180" class="body-text" font-size="11.5">• Heartbeat &amp; Block Report Pipeline:</text>
          <text x="28" y="198" class="body-text" font-size="11" fill="#58a6ff">Reports capacity &amp; block list to NameNode</text>

          <text x="18" y="222" class="mono" font-size="10.5" fill="#58a6ff">Status: HEALTHY • 0 Missing • 0 Corrupt</text>
        </g>
      </g>

      <!-- Storage Telemetry & Resilience Details -->
      <g transform="translate(18, 305)">
        <rect x="0" y="0" width="1234" height="170" rx="10" fill="#161b22" stroke="#21262d" />
        <text x="18" y="28" class="bold-text" font-size="13" fill="#ffffff">🛡️ DataNode Storage Guardrails &amp; Network Pipeline Mechanics:</text>
        
        <text x="18" y="55" class="body-text" font-size="12">
          • <tspan class="bold-text" fill="#58a6ff">Heartbeat Telemetry (3s Interval):</tspan> Reports node health, disk capacity (56.75 GB Free in Kali VM), and active transfer connections.
        </text>
        <text x="18" y="78" class="body-text" font-size="12">
          • <tspan class="bold-text" fill="#58a6ff">Block Inventory Reports (6h Interval):</tspan> Sends full cryptographic hash inventory of all blocks to NameNode to verify replication quotas.
        </text>
        <text x="18" y="101" class="body-text" font-size="12">
          • <tspan class="bold-text" fill="#3fb950">Pipeline Writing with ACKs:</tspan> Client streams 64KB packets to DataNode 1 ➔ DataNode 1 forwards to DataNode 2 ➔ ACKs return in reverse order.
        </text>
        <text x="18" y="124" class="body-text" font-size="12">
          • <tspan class="bold-text" fill="#f85149">Legacy Typo Immunity:</tspan> Configured strictly via <tspan class="mono" fill="#7ee787">dfs.datanode.data.dir</tspan> (never the broken 2018 course typo <tspan class="mono" fill="#f85149">dfs.data.dir</tspan>).
        </text>
        <text x="18" y="148" class="mono" font-size="11" fill="#79c0ff">
          Verified Active: hdfs dfsadmin -report ➔ 1 Live DataNode • 0 Dead • 0 Under-replicated • 0 Corrupt Blocks
        </text>
      </g>
    </g>
  </g>

  <!-- RIGHT COLUMN: YARN COMPUTE & SCHEDULING SUBSYSTEMS (Width: 1320) -->
  <g id="yarn-subsystems" transform="translate(1420, 390)">
    <rect x="0" y="0" width="1320" height="1100" rx="18" fill="url(#cardGrad)" stroke="#238636" stroke-width="1.8" filter="url(#shadow)" />
    
    <path d="M 0 18 Q 0 0 18 0 L 1302 0 Q 1320 0 1320 18 L 1320 54 L 0 54 Z" fill="url(#yarnGrad)" opacity="0.2" />
    <rect x="25" y="14" width="410" height="28" rx="6" fill="#238636" />
    <text x="230" y="33" class="heading" font-size="13" fill="#ffffff" text-anchor="middle">⚙️ YARN RESOURCE &amp; SCHEDULING SUBSYSTEMS</text>
    <text x="455" y="34" class="subheading" font-size="13" fill="#56d364">Deadlock-Free 512MB Container Architecture</text>

    <!-- Subsystem 3: ResourceManager Internals (Height: 495) -->
    <g transform="translate(25, 70)">
      <rect x="0" y="0" width="1270" height="495" rx="14" fill="#0d1117" stroke="#2ea043" stroke-width="1.3" filter="url(#glowGreen)" />
      
      <rect x="18" y="14" width="280" height="28" rx="6" fill="#238636" />
      <text x="158" y="32" class="heading" font-size="13.5" fill="#ffffff" text-anchor="middle">🧠 ResourceManager Scheduling Engine</text>
      <text x="315" y="33" class="mono" font-size="12" fill="#7ee787">Pool: 3072 MB • 4 vCPUs • Web UI :8088 • IPC :8032</text>

      <!-- Pluggable Capacity Scheduler (Left half, width 610) -->
      <g transform="translate(18, 55)">
        <rect x="0" y="0" width="610" height="255" rx="10" fill="#161b22" stroke="#21262d" />
        <text x="18" y="28" class="bold-text" font-size="13.5" fill="#56d364">📊 Pluggable Capacity Scheduler</text>
        <text x="18" y="50" class="body-text" font-size="11.5">Hierarchical multi-tenant resource queues and isolation:</text>

        <rect x="16" y="62" width="578" height="42" rx="5" fill="#0d1117" stroke="#238636" stroke-width="0.8" />
        <text x="26" y="80" class="bold-text" font-size="11" fill="#7ee787">root.default Queue (100% Cluster Memory = 3072 MB)</text>
        <text x="26" y="96" class="body-text" font-size="10.5" fill="#8b949e">Minimum Allocation: 256 MB • Maximum Allocation: 3072 MB (1 vCore step)</text>

        <rect x="16" y="110" width="578" height="52" rx="5" fill="#0d1117" stroke="#21262d" />
        <text x="26" y="128" class="bold-text" font-size="11" fill="#c9d1d9">Deadlock-Free Resource Sizing Formula:</text>
        <text x="26" y="148" class="mono" font-size="10.5" fill="#56d364">AM (512MB) + Map (512MB) + Reduce (512MB) = 1536 MB &lt; 3072 MB Pool</text>

        <rect x="16" y="168" width="578" height="38" rx="5" fill="#0d1117" stroke="#21262d" />
        <text x="26" y="186" class="mono" font-size="10.5" fill="#8b949e">Scheduler IPC Protocol: Port 8030 • DominantResourceCalculator</text>

        <text x="18" y="235" class="body-text" font-size="11" fill="#8b949e">
          Eliminates the single-node deadlock where AM (1536MB) + Reduce (2048MB) exceeded 3072MB.
        </text>
      </g>

      <!-- ApplicationsManager & State Machine (Right half, width 610) -->
      <g transform="translate(642, 55)">
        <rect x="0" y="0" width="610" height="255" rx="10" fill="#161b22" stroke="#21262d" />
        <text x="18" y="28" class="bold-text" font-size="13.5" fill="#56d364">🎯 ApplicationsManager (ASM)</text>
        <text x="18" y="50" class="body-text" font-size="11.5">Client application intake, verification &amp; AM supervisor:</text>

        <rect x="16" y="62" width="578" height="42" rx="5" fill="#0d1117" stroke="#21262d" />
        <text x="26" y="80" class="bold-text" font-size="11" fill="#7ee787">1. Job Submission Verification (IPC :8032)</text>
        <text x="26" y="96" class="body-text" font-size="10.5" fill="#8b949e">Validates user permissions, tokens, queue limits, and resource availability.</text>

        <rect x="16" y="110" width="578" height="42" rx="5" fill="#0d1117" stroke="#21262d" />
        <text x="26" y="128" class="bold-text" font-size="11" fill="#7ee787">2. ApplicationMaster Slot Negotiation</text>
        <text x="26" y="144" class="body-text" font-size="10.5" fill="#8b949e">Negotiates 1st container with NodeManager and generates ContainerToken.</text>

        <rect x="16" y="158" width="578" height="42" rx="5" fill="#0d1117" stroke="#21262d" />
        <text x="26" y="176" class="bold-text" font-size="11" fill="#7ee787">3. Failure Recovery State Machine</text>
        <text x="26" y="192" class="body-text" font-size="10.5" fill="#8b949e">Monitors AM liveness. If AM crashes, ASM automatically restarts it up to 2 times.</text>

        <text x="18" y="235" class="body-text" font-size="11" fill="#8b949e">
          Application States: NEW ➔ SUBMITTED ➔ ACCEPTED ➔ RUNNING ➔ FINISHED / FAILED.
        </text>
      </g>

      <!-- ResourceTracker & Heartbeat Pipeline (Bottom full width) -->
      <g transform="translate(18, 320)">
        <rect x="0" y="0" width="1234" height="155" rx="10" fill="#161b22" stroke="#21262d" />
        <text x="18" y="28" class="bold-text" font-size="13" fill="#ffffff">⚡ ResourceTracker &amp; Node Liveness Protocol (Port :8031):</text>

        <g transform="translate(18, 42)">
          <rect x="0" y="0" width="285" height="95" rx="8" fill="#0d1117" stroke="#238636" />
          <text x="14" y="24" class="bold-text" font-size="12" fill="#56d364">1. Node Registration</text>
          <text x="14" y="44" class="body-text" font-size="11">NodeManager connects on boot,</text>
          <text x="14" y="60" class="body-text" font-size="11">advertises 3072 MB RAM and</text>
          <text x="14" y="80" class="mono" font-size="10.5" fill="#7ee787">4 vCores capacity.</text>
        </g>

        <g transform="translate(320, 42)">
          <rect x="0" y="0" width="285" height="95" rx="8" fill="#0d1117" stroke="#3fb950" />
          <text x="14" y="24" class="bold-text" font-size="12" fill="#3fb950">2. Node Heartbeats (1s)</text>
          <text x="14" y="44" class="body-text" font-size="11">Reports running containers,</text>
          <text x="14" y="60" class="body-text" font-size="11">completed tasks, CPU load,</text>
          <text x="14" y="80" class="mono" font-size="10.5" fill="#7ee787">and memory utilization.</text>
        </g>

        <g transform="translate(620, 42)">
          <rect x="0" y="0" width="285" height="95" rx="8" fill="#0d1117" stroke="#bc8cff" />
          <text x="14" y="24" class="bold-text" font-size="12" fill="#bc8cff">3. Container Token Security</text>
          <text x="14" y="44" class="body-text" font-size="11">Issues HMAC-SHA256 tokens</text>
          <text x="14" y="60" class="body-text" font-size="11">authorizing AM to launch</text>
          <text x="14" y="80" class="mono" font-size="10.5" fill="#d2a8ff">tasks on NodeManagers.</text>
        </g>

        <g transform="translate(920, 42)">
          <rect x="0" y="0" width="295" height="95" rx="8" fill="#0d1117" stroke="#38bdf8" />
          <text x="14" y="24" class="bold-text" font-size="12" fill="#38bdf8">4. Health Checker Service</text>
          <text x="14" y="44" class="body-text" font-size="11">Marks node UNHEALTHY if</text>
          <text x="14" y="60" class="body-text" font-size="11">local disks fill &gt; 90% or</text>
          <text x="14" y="80" class="mono" font-size="10.5" fill="#38bdf8">heartbeat drops &gt; 10 mins.</text>
        </g>
      </g>
    </g>

    <!-- Subsystem 4: NodeManager & Shuffle-Sort Pipeline (Height: 495) -->
    <g transform="translate(25, 580)">
      <rect x="0" y="0" width="1270" height="495" rx="14" fill="#0d1117" stroke="#2ea043" stroke-width="1.3" />
      
      <rect x="18" y="14" width="280" height="28" rx="6" fill="#238636" />
      <text x="158" y="32" class="heading" font-size="13.5" fill="#ffffff" text-anchor="middle">👷 NodeManager &amp; Compute Pipeline</text>
      <text x="315" y="33" class="mono" font-size="12" fill="#7ee787">IPC :8040 • Web UI :8042 • cgroups Isolation • JobHistoryServer :19888</text>

      <!-- 3 Containers Execution Cards -->
      <g transform="translate(18, 55)">
        <!-- AM Container -->
        <g transform="translate(0, 0)">
          <rect x="0" y="0" width="395" height="235" rx="10" fill="#161b22" stroke="#2ea043" stroke-width="1.2" />
          <rect x="14" y="12" width="367" height="26" rx="5" fill="#238636" fill-opacity="0.3" />
          <text x="197" y="29" class="badge" fill="#56d364" text-anchor="middle">Container #001: ApplicationMaster (512 MB)</text>

          <text x="18" y="60" class="bold-text" font-size="12" fill="#e6edf3">• JVM Heap:</text>
          <text x="100" y="60" class="mono" font-size="11" fill="#7ee787">-Xmx400m -XX:+UseG1GC</text>

          <text x="18" y="82" class="bold-text" font-size="12" fill="#e6edf3">• Lifecycle:</text>
          <text x="90" y="82" class="body-text" font-size="11.5">Per-job coordinator spawned by RM</text>

          <text x="18" y="104" class="bold-text" font-size="12" fill="#e6edf3">• Splits:</text>
          <text x="75" y="104" class="body-text" font-size="11.5">Reads InputSplits from HDFS (:9000)</text>

          <text x="18" y="126" class="bold-text" font-size="12" fill="#e6edf3">• Negotiation:</text>
          <text x="110" y="126" class="body-text" font-size="11.5">Requests 1 Map + 1 Reduce slot</text>

          <text x="18" y="148" class="bold-text" font-size="12" fill="#e6edf3">• Data Locality:</text>
          <text x="115" y="148" class="body-text" font-size="11.5" fill="#3fb950">NODE_LOCAL preferred</text>

          <rect x="14" y="165" width="367" height="52" rx="5" fill="#0d1117" />
          <text x="24" y="184" class="mono" font-size="10.5" fill="#7ee787">yarn.app.mapreduce.am.resource.mb = 512</text>
          <text x="24" y="202" class="body-text" font-size="10.5" fill="#8b949e">Prevents starvation of worker task containers.</text>
        </g>

        <!-- Map Container -->
        <g transform="translate(418, 0)">
          <rect x="0" y="0" width="395" height="235" rx="10" fill="#161b22" stroke="#8957e5" stroke-width="1.2" />
          <rect x="14" y="12" width="367" height="26" rx="5" fill="#8957e5" fill-opacity="0.3" />
          <text x="197" y="29" class="badge" fill="#d2a8ff" text-anchor="middle">Container #002: MapTask (512 MB)</text>

          <text x="18" y="60" class="bold-text" font-size="12" fill="#e6edf3">• Input:</text>
          <text x="70" y="60" class="body-text" font-size="11.5">Reads local Block 1 from DataNode</text>

          <text x="18" y="82" class="bold-text" font-size="12" fill="#e6edf3">• RecordReader:</text>
          <text x="120" y="82" class="body-text" font-size="11.5">Parses lines ➔ (Key, Value)</text>

          <text x="18" y="104" class="bold-text" font-size="12" fill="#e6edf3">• In-Memory Spill:</text>
          <text x="135" y="104" class="body-text" font-size="11.5">100MB ring buffer (80% thresh)</text>

          <text x="18" y="126" class="bold-text" font-size="12" fill="#e6edf3">• Partitioner:</text>
          <text x="105" y="126" class="body-text" font-size="11.5">HashPartitioner routes by reducer ID</text>

          <text x="18" y="148" class="bold-text" font-size="12" fill="#e6edf3">• Spill Sort:</text>
          <text x="95" y="148" class="body-text" font-size="11.5">QuickSort by key ➔ merged to disk</text>

          <rect x="14" y="165" width="367" height="52" rx="5" fill="#0d1117" />
          <text x="24" y="184" class="mono" font-size="10.5" fill="#bc8cff">mapreduce.map.memory.mb = 512</text>
          <text x="24" y="202" class="body-text" font-size="10.5" fill="#8b949e">Execution verified: 100% complete in seconds.</text>
        </g>

        <!-- Reduce Container -->
        <g transform="translate(836, 0)">
          <rect x="0" y="0" width="395" height="235" rx="10" fill="#161b22" stroke="#8957e5" stroke-width="1.2" />
          <rect x="14" y="12" width="367" height="26" rx="5" fill="#8957e5" fill-opacity="0.3" />
          <text x="197" y="29" class="badge" fill="#d2a8ff" text-anchor="middle">Container #003: ReduceTask (512 MB)</text>

          <text x="18" y="60" class="bold-text" font-size="12" fill="#e6edf3">• Shuffle:</text>
          <text x="80" y="60" class="body-text" font-size="11.5">Fetches partition spills via HTTP</text>

          <text x="18" y="82" class="bold-text" font-size="12" fill="#e6edf3">• Merge-Sort:</text>
          <text x="110" y="82" class="body-text" font-size="11.5">Merges sorted runs into single stream</text>

          <text x="18" y="104" class="bold-text" font-size="12" fill="#e6edf3">• Aggregation:</text>
          <text x="115" y="104" class="body-text" font-size="11.5">reduce(K, Iterator&lt;V&gt;) logic</text>

          <text x="18" y="126" class="bold-text" font-size="12" fill="#e6edf3">• Output:</text>
          <text x="80" y="126" class="mono" font-size="11" fill="#d2a8ff">part-r-00000</text>
          <text x="180" y="126" class="body-text" font-size="11.5">written back to HDFS</text>

          <text x="18" y="148" class="bold-text" font-size="12" fill="#e6edf3">• JobHistory:</text>
          <text x="105" y="148" class="body-text" font-size="11.5">Audit metrics aggregated on :19888</text>

          <rect x="14" y="165" width="367" height="52" rx="5" fill="#0d1117" />
          <text x="24" y="184" class="mono" font-size="10.5" fill="#bc8cff">mapreduce.reduce.memory.mb = 512</text>
          <text x="24" y="202" class="body-text" font-size="10.5" fill="#8b949e">Benchmarked Pi task: 42.8s total runtime.</text>
        </g>
      </g>

      <!-- Memory Stability & Tuning Details -->
      <g transform="translate(18, 305)">
        <rect x="0" y="0" width="1234" height="170" rx="10" fill="#161b22" stroke="#21262d" />
        <text x="18" y="28" class="bold-text" font-size="13" fill="#ffffff">🧠 NodeManager Enterprise Virtual Memory &amp; GC Stability Tuning:</text>
        
        <text x="18" y="55" class="body-text" font-size="12">
          • <tspan class="bold-text" fill="#7ee787">vmem-check-enabled=false:</tspan> Java 11/17 glibc threads allocate 64MB virtual memory arenas. Disabling vmem check prevents NodeManager from killing healthy containers.
        </text>
        <text x="18" y="78" class="body-text" font-size="12">
          • <tspan class="bold-text" fill="#7ee787">Low-Pause G1GC (-XX:+UseG1GC):</tspan> Replaces outdated ParallelGC. Predictable pause targets (&lt;200ms) prevent false container heartbeat timeouts during large job shuffles.
        </text>
        <text x="18" y="101" class="body-text" font-size="12">
          • <tspan class="bold-text" fill="#bc8cff">MapReduce JobHistoryServer (JHS :19888):</tspan> Preserves task counters, timeline data, and execution logs even after containers terminate.
        </text>
        <text x="18" y="124" class="body-text" font-size="12">
          • <tspan class="bold-text" fill="#38bdf8">Cloud Storage Connector (CloudStorageFileSystem):</tspan> On GCP Dataproc, containers stream directly to <tspan class="mono" fill="#38bdf8">gs://</tspan> buckets with 11 9s durability and zero disk bottlenecks.
        </text>
        <text x="18" y="148" class="mono" font-size="11" fill="#7ee787">
          Verified Execution: Monte Carlo Pi Benchmark finished in 42.8s • 100% Map and 100% Reduce completion across all containers.
        </text>
      </g>
    </g>
  </g>

  <!-- ========================================================================= -->
  <!-- 4. BOTTOM PERSISTENCE & STORAGE TIER                                      -->
  <!-- ========================================================================= -->
  <g id="storage-tier" transform="translate(60, 1515)">
    <rect x="0" y="0" width="2680" height="180" rx="16" fill="url(#cardGrad)" stroke="#da3633" stroke-width="1.5" filter="url(#shadow)" />

    <path d="M 0 16 Q 0 0 16 0 L 16 0 L 16 180 L 0 180 Z" fill="url(#volGrad)" />
    <rect x="30" y="16" width="370" height="28" rx="6" fill="#da3633" fill-opacity="0.2" stroke="#da3633" stroke-width="1.2" />
    <text x="215" y="35" class="heading" font-size="13" fill="#f85149" text-anchor="middle">💾 MULTI-PLATFORM PERSISTENCE &amp; CLOUD STORAGE TIER</text>
    <text x="420" y="35" class="body-text" font-size="13">Zero Data Loss: Named Docker Volumes, VMware Virtual Disks &amp; Google Cloud Storage Buckets (gs://)</text>

    <g transform="translate(30, 60)">
      <g transform="translate(0, 0)">
        <rect x="0" y="0" width="635" height="95" rx="10" fill="#0d1117" stroke="#30363d" stroke-width="1.2" />
        <text x="18" y="28" class="bold-text" font-size="13" fill="#58a6ff">📁 NameNode Volume (fsimage + edits)</text>
        <text x="18" y="50" class="mono" font-size="11.5" fill="#79c0ff">hadoop_namenode_data ➔ /usr/local/hadoop/hdfs/namenode</text>
        <text x="18" y="74" class="body-text" font-size="11.5">Stores filesystem namespace tree, fsimage snapshots, and edits transaction logs</text>
      </g>

      <g transform="translate(660, 0)">
        <rect x="0" y="0" width="635" height="95" rx="10" fill="#0d1117" stroke="#30363d" stroke-width="1.2" />
        <text x="18" y="28" class="bold-text" font-size="13" fill="#58a6ff">🧱 DataNode Volume (Raw 128MB Blocks)</text>
        <text x="18" y="50" class="mono" font-size="11.5" fill="#79c0ff">hadoop_datanode_data ➔ /usr/local/hadoop/hdfs/datanode</text>
        <text x="18" y="74" class="body-text" font-size="11.5">Stores actual raw 128MB replicated data blocks (blk_* and blk_*.meta checksums)</text>
      </g>

      <g transform="translate(1320, 0)">
        <rect x="0" y="0" width="635" height="95" rx="10" fill="#0d1117" stroke="#3fb950" stroke-width="1.2" />
        <text x="18" y="28" class="bold-text" font-size="13" fill="#3fb950">📦 Temporary Workspace &amp; GCS Staging</text>
        <text x="18" y="50" class="mono" font-size="11.5" fill="#7ee787">hadoop_tmp_data ➔ /app/hadoop/tmp | gs://bucket/staging</text>
        <text x="18" y="74" class="body-text" font-size="11.5">MapReduce spill buffers, intermediate shuffle partitions, and cloud staging data</text>
      </g>

      <g transform="translate(1980, 0)">
        <rect x="0" y="0" width="640" height="95" rx="10" fill="#0d1117" stroke="#30363d" stroke-width="1.2" />
        <text x="18" y="28" class="bold-text" font-size="13" fill="#bc8cff">📜 Cluster Daemon Logs &amp; Audit Trail</text>
        <text x="18" y="50" class="mono" font-size="11.5" fill="#d2a8ff">hadoop_logs_data ➔ /usr/local/hadoop/logs</text>
        <text x="18" y="74" class="body-text" font-size="11.5">Daemon stdout/stderr logs for NameNode, DataNode, RM, NM, and JobHistoryServer</text>
      </g>
    </g>
  </g>

  <!-- ========================================================================= -->
  <!-- 5. FOOTER SPECIFICATIONS BAR                                              -->
  <!-- ========================================================================= -->
  <g id="footer-specs" transform="translate(60, 1720)">
    <rect x="0" y="0" width="2680" height="85" rx="12" fill="#151b28" stroke="#30363d" stroke-width="1.2" />
    
    <text x="30" y="32" class="bold-text" font-size="13.5" fill="#ffffff">SYSTEM ARCHITECTURE SPECIFICATIONS SUMMARY:</text>
    <text x="30" y="58" class="body-text" font-size="12">
      • <tspan fill="#58a6ff">HDFS Block Size:</tspan> 128 MB | <tspan fill="#3fb950">Replication Factor:</tspan> 1 (Dev) / 3 (Prod) | <tspan fill="#d2a8ff">YARN Alloc:</tspan> 512MB/task (3072MB pool) | <tspan fill="#f2cc60">JVM GC:</tspan> -XX:+UseG1GC Low-Pause | <tspan fill="#38bdf8">Cloud:</tspan> Dataproc 2.1
    </text>

    <text x="2650" y="34" class="mono" font-size="12" fill="#58a6ff" text-anchor="end">https://github.com/Sohila-Khaled-Abbas/docker-hadoop</text>
    <text x="2650" y="58" class="body-text" font-size="11" fill="#6e7681" text-anchor="end">Distributed Big Data Engineering &amp; Distributed Systems Education • Apache 2.0 Licensed</text>
  </g>

  <!-- Cross-Subsystem Connectors -->
  <path d="M 720 730 L 720 780" fill="none" stroke="#58a6ff" stroke-width="2.5" marker-end="url(#arrowBlue)" />
  <path d="M 2080 730 L 2080 780" fill="none" stroke="#3fb950" stroke-width="2.5" marker-end="url(#arrowGreen)" />
  <path d="M 1420 890 C 1380 890, 1380 890, 1345 890" fill="none" stroke="#bc8cff" stroke-width="3" marker-end="url(#arrowPurple)" stroke-dasharray="6,4" />
  <path d="M 720 1445 L 720 1515" fill="none" stroke="#f85149" stroke-width="3" marker-end="url(#arrowRed)" />
  <path d="M 2080 1445 L 2080 1515" fill="none" stroke="#f85149" stroke-width="3" marker-end="url(#arrowRed)" />
</svg>'''

# Save both SVGs
svg_file_1 = IMG_DIR / "hadoop-data-engineering-infographic.svg"
svg_file_2 = IMG_DIR / "hadoop-data-engineering-system-architecture.svg"

with open(svg_file_1, "w", encoding="utf-8") as f:
    f.write(infographic_svg)
print(f"[OK] Written {svg_file_1}")

with open(svg_file_2, "w", encoding="utf-8") as f:
    f.write(architecture_svg)
print(f"[OK] Written {svg_file_2}")

# Render to high-resolution PNGs via headless Microsoft Edge
msedge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if os.path.exists(msedge_path):
    png_file_1 = IMG_DIR / "hadoop-data-engineering-infographic.png"
    png_file_2 = IMG_DIR / "hadoop-data-engineering-system-architecture.png"
    
    cmd_1 = [
        msedge_path,
        "--headless",
        "--hide-scrollbars",
        f"--screenshot={png_file_1}",
        "--window-size=2800,1920",
        str(svg_file_1)
    ]
    subprocess.run(cmd_1, check=True)
    print(f"[OK] Rendered {png_file_1} ({os.path.getsize(png_file_1)} bytes)")

    cmd_2 = [
        msedge_path,
        "--headless",
        "--hide-scrollbars",
        f"--screenshot={png_file_2}",
        "--window-size=2800,1920",
        str(svg_file_2)
    ]
    subprocess.run(cmd_2, check=True)
    print(f"[OK] Rendered {png_file_2} ({os.path.getsize(png_file_2)} bytes)")
else:
    print("[WARN] msedge.exe not found at default path, skipping PNG rendering")
