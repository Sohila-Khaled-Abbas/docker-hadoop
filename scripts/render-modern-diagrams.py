# ==============================================================================
# Script: render-modern-diagrams.py
# Generates two ultra-modern, high-definition SVG & PNG diagrams:
# 1. hadoop-data-engineering-infographic.svg (Platform & Lifecycle Infographic)
# 2. hadoop-data-engineering-system-architecture.svg (Deep Distributed Architecture)
#
# Optimized for:
# - Zero text overflow: Every line mathematically fitted with generous padding
# - Modern dark-mode aesthetics: Glassmorphism, tailored gradients, glow filters
# - Full ecosystem update: Hadoop 3.1.2/3.3.6, Apache Spark 3.5 (Master, Worker,
#   History Server, PySpark, Spark SQL), Apache Hive Metastore, JupyterLab Studio,
#   Unified Big Data Control Hub (Port 3030), Docker, VMware, GCP Dataproc
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
      <stop offset="20%" stop-color="#a371f7" />
      <stop offset="40%" stop-color="#3fb950" />
      <stop offset="60%" stop-color="#f59e0b" />
      <stop offset="80%" stop-color="#f43f5e" />
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

    <linearGradient id="sparkGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#e11d48" />
      <stop offset="50%" stop-color="#f43f5e" />
      <stop offset="100%" stop-color="#fb7185" />
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
      <feDropShadow dx="0" dy="14" stdDeviation="16" flood-color="#000000" flood-opacity="0.6" />
    </filter>

    <filter id="glowBlue" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="6" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>

    <filter id="glowSpark" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="6" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>

    <!-- Directional Arrow Markers -->
    <marker id="arrowBlue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#58a6ff" />
    </marker>
    <marker id="arrowGreen" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#3fb950" />
    </marker>
    <marker id="arrowPurple" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#bc8cff" />
    </marker>
    <marker id="arrowRed" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#f85149" />
    </marker>
    <marker id="arrowSpark" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#fb7185" />
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
# 1. GENERATE INFOGRAPHIC SVG (Platform Ecosystem & Unified Data Hub Map)
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
  <!-- 1. HEADER SECTION (HERO BANNER WITH UNIFIED ECOSYSTEM BADGES)              -->
  <!-- ========================================================================= -->
  <g id="header-section" transform="translate(60, 50)">
    <rect x="0" y="0" width="2680" height="135" rx="16" fill="#151b28" stroke="#30363d" stroke-width="1.5" filter="url(#shadow)" />
    <path d="M 0 16 Q 0 0 16 0 L 22 0 L 22 135 L 16 135 Q 0 135 0 119 Z" fill="url(#headerGrad)" />

    <text x="48" y="54" class="title" font-size="30" letter-spacing="0.5">
      🐘 APACHE HADOOP, SPARK &amp; ECOSYSTEM UNIFIED BIG DATA PLATFORM
    </text>
    <text x="48" y="90" class="subtitle" font-size="14.5">
      Distributed HDFS • YARN • Apache Spark 3.5 • Hive • Sqoop • Oozie • Pig • JupyterLab Studio • Unified Platform Console (:3030)
    </text>

    <!-- Badges Row -->
    <g transform="translate(1360, 36)">
      <g transform="translate(0, 0)">
        <rect x="0" y="0" width="135" height="34" rx="8" fill="#1f6feb" fill-opacity="0.18" stroke="#388bfd" stroke-width="1.2" />
        <text x="67" y="22" class="badge" fill="#58a6ff" text-anchor="middle">HADOOP v3.1/3.3</text>
      </g>
      <g transform="translate(145, 0)">
        <rect x="0" y="0" width="145" height="34" rx="8" fill="#e11d48" fill-opacity="0.2" stroke="#f43f5e" stroke-width="1.2" />
        <text x="72" y="22" class="badge" fill="#fb7185" text-anchor="middle">⚡ SPARK 3.5</text>
      </g>
      <g transform="translate(300, 0)">
        <rect x="0" y="0" width="160" height="34" rx="8" fill="#d97706" fill-opacity="0.2" stroke="#f59e0b" stroke-width="1.2" />
        <text x="80" y="22" class="badge" fill="#fcd34d" text-anchor="middle">🐝 HIVE &amp; SQOOP</text>
      </g>
      <g transform="translate(470, 0)">
        <rect x="0" y="0" width="160" height="34" rx="8" fill="#8957e5" fill-opacity="0.2" stroke="#bc8cff" stroke-width="1.2" />
        <text x="80" y="22" class="badge" fill="#d2a8ff" text-anchor="middle">📋 OOZIE &amp; PIG</text>
      </g>
      <g transform="translate(640, 0)">
        <rect x="0" y="0" width="165" height="34" rx="8" fill="#0284c7" fill-opacity="0.2" stroke="#38bdf8" stroke-width="1.2" />
        <text x="82" y="22" class="badge" fill="#38bdf8" text-anchor="middle">🌐 CONTROL HUB :3030</text>
      </g>
      <g transform="translate(815, 0)">
        <rect x="0" y="0" width="155" height="34" rx="8" fill="#238636" fill-opacity="0.18" stroke="#3fb950" stroke-width="1.2" />
        <text x="77" y="22" class="badge" fill="#56d364" text-anchor="middle">🪐 JUPYTERLAB :8888</text>
      </g>
      <text x="965" y="72" class="body-text" font-size="12" fill="#8b949e" text-anchor="end">
        Enterprise Production-Grade Big Data Stack • Single Pane of Glass Management
      </text>
    </g>
  </g>

  <!-- ========================================================================= -->
  <!-- 2. MULTI-PLATFORM RUNTIMES STRIP (6 EQUAL CARDS)                         -->
  <!-- ========================================================================= -->
  <g id="multi-platform-section" transform="translate(60, 205)">
    <rect x="0" y="0" width="2680" height="165" rx="16" fill="url(#cardGrad)" stroke="#30363d" stroke-width="1.5" filter="url(#shadow)" />
    
    <rect x="25" y="16" width="340" height="28" rx="6" fill="#d29922" fill-opacity="0.15" stroke="#d29922" stroke-width="1" />
    <text x="195" y="35" class="subheading" font-size="13" fill="#e3b341" text-anchor="middle">🖥️ 6 UNIFIED DATA SYSTEM RUNTIMES</text>

    <!-- Card 1: Docker Full Stack -->
    <g transform="translate(25, 55)">
      <rect x="0" y="0" width="425" height="95" rx="10" fill="#0d1117" stroke="#388bfd" stroke-width="1.2" />
      <text x="16" y="26" class="bold-text" font-size="13.5" fill="#58a6ff">🐳 Docker Compose Full Stack</text>
      <text x="16" y="48" class="body-text" font-size="11.5">Hadoop + Spark + Hive + Jupyter + Control Hub</text>
      <rect x="16" y="60" width="393" height="22" rx="4" fill="#161b22" />
      <text x="24" y="75" class="mono" font-size="10.5" fill="#79c0ff">docker compose up -d • Hub at :3030</text>
    </g>

    <!-- Card 2: Spark Master & Worker -->
    <g transform="translate(465, 55)">
      <rect x="0" y="0" width="425" height="95" rx="10" fill="#0d1117" stroke="#f43f5e" stroke-width="1.2" />
      <text x="16" y="26" class="bold-text" font-size="13.5" fill="#fb7185">⚡ Apache Spark 3.5 Engine</text>
      <text x="16" y="48" class="body-text" font-size="11.5">Master (:8080) • Worker (:8081) • History (:18080)</text>
      <rect x="16" y="60" width="393" height="22" rx="4" fill="#161b22" />
      <text x="24" y="75" class="mono" font-size="10.5" fill="#fb7185">spark://spark-master:7077 • PySpark • SQL</text>
    </g>

    <!-- Card 3: GCP Dataproc -->
    <g transform="translate(905, 55)">
      <rect x="0" y="0" width="425" height="95" rx="10" fill="#0d1117" stroke="#38bdf8" stroke-width="1.2" />
      <text x="16" y="26" class="bold-text" font-size="13.5" fill="#38bdf8">☁️ Google Cloud Dataproc &amp; GCE</text>
      <text x="16" y="48" class="body-text" font-size="11.5">Ephemeral clusters • GCS (gs://) • Spot workers • Gateway</text>
      <rect x="16" y="60" width="393" height="22" rx="4" fill="#161b22" />
      <text x="24" y="75" class="mono" font-size="10.5" fill="#79c0ff">Deploy-Hadoop-GCP.bat • .ps1 • 30m Auto-Idle</text>
    </g>

    <!-- Card 4: VMware Workstation -->
    <g transform="translate(1345, 55)">
      <rect x="0" y="0" width="425" height="95" rx="10" fill="#0d1117" stroke="#bc8cff" stroke-width="1.2" />
      <text x="16" y="26" class="bold-text" font-size="13.5" fill="#d2a8ff">🐉 VMware Workstation (Kali)</text>
      <text x="16" y="48" class="body-text" font-size="11.5">Kali Rolling • Hadoop 3.3.6 • 6GB RAM / 4 vCPUs • G1GC</text>
      <rect x="16" y="60" width="393" height="22" rx="4" fill="#161b22" />
      <text x="24" y="75" class="mono" font-size="10.5" fill="#bc8cff">Launch-Kali-VMware.bat • HWCursor off • 1080p</text>
    </g>

    <!-- Card 5: Hyper-V -->
    <g transform="translate(1785, 55)">
      <rect x="0" y="0" width="425" height="95" rx="10" fill="#0d1117" stroke="#3fb950" stroke-width="1.2" />
      <text x="16" y="26" class="bold-text" font-size="13.5" fill="#56d364">🪟 Hyper-V Generation 2 (Ubuntu)</text>
      <text x="16" y="48" class="body-text" font-size="11.5">Ubuntu 24.04 • 4 vCPUs • Dynamic RAM • UEFI CA • NAT fix</text>
      <rect x="16" y="60" width="393" height="22" rx="4" fill="#161b22" />
      <text x="24" y="75" class="mono" font-size="10.5" fill="#7ee787">Fix-Lag-And-Start-VM.bat • optimize-hyperv.ps1</text>
    </g>

    <!-- Card 6: WSL 2 Ubuntu GUI -->
    <g transform="translate(2225, 55)">
      <rect x="0" y="0" width="430" height="95" rx="10" fill="#0d1117" stroke="#f2cc60" stroke-width="1.2" />
      <text x="16" y="26" class="bold-text" font-size="13.5" fill="#f2cc60">🐧 WSL 2 Ubuntu + Visual XFCE GUI</text>
      <text x="16" y="48" class="body-text" font-size="11.5">Windows 11 Native Kernel • xRDP Port 3390 • Zero VM lag</text>
      <rect x="16" y="60" width="398" height="22" rx="4" fill="#161b22" />
      <text x="24" y="75" class="mono" font-size="10.5" fill="#f2cc60">Ubuntu-WSL-GUI.rdp • install-hadoop-wsl.sh</text>
    </g>
  </g>

  <!-- ========================================================================= -->
  <!-- 3. MAIN ARCHITECTURE BODY (3 COLUMNS)                                     -->
  <!-- ========================================================================= -->

  <!-- LEFT COLUMN: DEVELOPER & HOST ACCESS LAYER (Width: 520) -->
  <g id="host-client-layer" transform="translate(60, 390)">
    <rect x="0" y="0" width="520" height="1100" rx="16" fill="url(#cardGrad)" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="6,4" filter="url(#shadow)" />
    
    <path d="M 0 16 Q 0 0 16 0 L 504 0 Q 520 0 520 16 L 520 54 L 0 54 Z" fill="url(#gcpGrad)" opacity="0.15" />
    <rect x="20" y="14" width="310" height="26" rx="6" fill="#0284c7" />
    <text x="175" y="32" class="heading" font-size="13" fill="#ffffff" text-anchor="middle">💻 UNIFIED CONTROL HUB &amp; CLIENTS</text>
    <text x="20" y="80" class="subheading" font-size="15" fill="#38bdf8">Single Pane of Glass Interface</text>
    <text x="20" y="100" class="body-text" font-size="13">Central dashboard, Web UIs &amp; Interactive Studios</text>

    <!-- Component 1: Unified Control Hub -->
    <g transform="translate(20, 115)">
      <rect x="0" y="0" width="480" height="210" rx="12" fill="#0d1117" stroke="#38bdf8" stroke-width="1.5" filter="url(#glowBlue)" />
      <text x="20" y="28" class="bold-text" font-size="15" fill="#38bdf8">🌐 Unified Big Data Control Hub</text>
      <text x="20" y="48" class="body-text" font-size="12">Port <tspan class="mono" fill="#38bdf8">:3030</tspan> &bull; Live Telemetry &amp; Interactive Studio</text>
      
      <rect x="18" y="58" width="444" height="24" rx="5" fill="#161b22" />
      <text x="28" y="74" class="mono" font-size="11" fill="#34d399">Cluster Health Monitor</text>
      <text x="450" y="74" class="mono" font-size="11" fill="#7ee787" text-anchor="end">10/10 Daemons Probed</text>

      <rect x="18" y="86" width="444" height="24" rx="5" fill="#161b22" />
      <text x="28" y="102" class="mono" font-size="11" fill="#38bdf8">Interactive HDFS Explorer</text>
      <text x="450" y="102" class="mono" font-size="11" fill="#79c0ff" text-anchor="end">WebHDFS File Browser</text>

      <rect x="18" y="114" width="444" height="24" rx="5" fill="#161b22" />
      <text x="28" y="130" class="mono" font-size="11" fill="#fb7185">Interactive Job Runner</text>
      <text x="450" y="130" class="mono" font-size="11" fill="#f43f5e" text-anchor="end">Spark Pi &bull; ETL &bull; Hive SQL</text>

      <rect x="18" y="142" width="444" height="24" rx="5" fill="#161b22" />
      <text x="28" y="158" class="mono" font-size="11" fill="#f59e0b">Architecture Diagram Viewer</text>
      <text x="450" y="158" class="mono" font-size="11" fill="#fcd34d" text-anchor="end">Interactive SVG Pan/Zoom</text>

      <rect x="18" y="170" width="444" height="26" rx="5" fill="#041226" stroke="#38bdf8" stroke-width="1" />
      <text x="240" y="187" class="mono" font-size="11" fill="#38bdf8" text-anchor="middle">http://localhost:3030 (1-Click Launch)</text>
    </g>

    <!-- Component 2: JupyterLab & Web Consoles -->
    <g transform="translate(20, 340)">
      <rect x="0" y="0" width="480" height="210" rx="12" fill="#0d1117" stroke="#30363d" stroke-width="1.2" />
      <text x="20" y="28" class="bold-text" font-size="15" fill="#56d364">🪐 Interactive Studios &amp; Consoles</text>
      <text x="20" y="48" class="body-text" font-size="12">Direct Developer Endpoints (Single-Click Web Access):</text>

      <rect x="18" y="58" width="444" height="24" rx="5" fill="#161b22" />
      <text x="28" y="74" class="mono" font-size="11" fill="#56d364">JupyterLab PySpark Studio</text>
      <text x="450" y="74" class="mono" font-size="11" fill="#7ee787" text-anchor="end">:8888 (Interactive ETL)</text>

      <rect x="18" y="86" width="444" height="24" rx="5" fill="#161b22" />
      <text x="28" y="102" class="mono" font-size="11" fill="#fb7185">Spark Master Web UI</text>
      <text x="450" y="102" class="mono" font-size="11" fill="#f43f5e" text-anchor="end">:8080 (Cluster Cores)</text>

      <rect x="18" y="114" width="444" height="24" rx="5" fill="#161b22" />
      <text x="28" y="130" class="mono" font-size="11" fill="#388bfd">HDFS NameNode UI</text>
      <text x="450" y="130" class="mono" font-size="11" fill="#79c0ff" text-anchor="end">:9870 (Namespace &amp; Files)</text>

      <rect x="18" y="142" width="444" height="24" rx="5" fill="#161b22" />
      <text x="28" y="158" class="mono" font-size="11" fill="#3fb950">YARN ResourceManager UI</text>
      <text x="450" y="158" class="mono" font-size="11" fill="#7ee787" text-anchor="end">:8088 (Apps &amp; Queues)</text>

      <rect x="18" y="170" width="444" height="26" rx="5" fill="#161b22" />
      <text x="28" y="187" class="mono" font-size="11" fill="#d2a8ff">Spark History / MR History</text>
      <text x="450" y="187" class="mono" font-size="11" fill="#d2a8ff" text-anchor="end">:18080 / :19888</text>
    </g>

    <!-- Component 3: 1-Click Launchers -->
    <g transform="translate(20, 565)">
      <rect x="0" y="0" width="480" height="195" rx="12" fill="#0d1117" stroke="#30363d" stroke-width="1.2" />
      <text x="20" y="28" class="bold-text" font-size="15" fill="#e3b341">🚀 1-Click Windows Launchers</text>
      <text x="20" y="48" class="body-text" font-size="12">Location: <tspan class="mono" fill="#f2cc60">launchers/windows/</tspan></text>

      <text x="20" y="75" class="bold-text" font-size="12.5" fill="#e6edf3">• Start-Hadoop-Docker.bat</text>
      <text x="35" y="92" class="body-text" font-size="11.5">Boots Hadoop + Spark + Hub &amp; auto-opens browser</text>

      <text x="20" y="115" class="bold-text" font-size="12.5" fill="#e6edf3">• Deploy-Hadoop-GCP.bat / .ps1</text>
      <text x="35" y="132" class="body-text" font-size="11.5">Provisions GCP Dataproc &amp; Compute Engine VM</text>

      <text x="20" y="155" class="bold-text" font-size="12.5" fill="#e6edf3">• Launch-Kali-VMware.bat</text>
      <text x="35" y="172" class="body-text" font-size="11.5">Calibrates VMX specs &amp; boots Kali Workstation</text>
    </g>

    <!-- Component 4: Pre-Packaged Datasets & Notebooks -->
    <g transform="translate(20, 775)">
      <rect x="0" y="0" width="480" height="175" rx="12" fill="#0d1117" stroke="#30363d" stroke-width="1.2" />
      <text x="20" y="28" class="bold-text" font-size="15" fill="#3fb950">📊 Datasets &amp; Interactive Notebooks</text>
      <text x="20" y="48" class="body-text" font-size="12">Hands-on tutorials in <tspan class="mono" fill="#7ee787">notebooks/</tspan> &amp; <tspan class="mono" fill="#7ee787">datasets/</tspan>:</text>

      <text x="20" y="75" class="bold-text" font-size="12.5" fill="#e6edf3">• 01-pyspark-hdfs-pipeline.ipynb</text>
      <text x="35" y="92" class="body-text" font-size="11.5">DataFrame CSV ingestion &amp; Snappy Parquet write</text>

      <text x="20" y="115" class="bold-text" font-size="12.5" fill="#e6edf3">• 02-spark-sql-hive-analytics.ipynb</text>
      <text x="35" y="132" class="body-text" font-size="11.5">Relational SQL queries &amp; Hive catalog integration</text>

      <text x="20" y="155" class="mono" font-size="11" fill="#79c0ff">• wordcount-sample.txt &bull; employees.csv</text>
    </g>

    <!-- Step 1 Indicator Pill -->
    <g transform="translate(20, 965)">
      <rect x="0" y="0" width="480" height="115" rx="12" fill="#1f6feb" fill-opacity="0.1" stroke="#1f6feb" stroke-width="1.2" />
      <circle cx="35" cy="35" r="16" fill="#1f6feb" />
      <text x="35" y="35" class="step-num">1</text>
      <text x="65" y="35" class="bold-text" font-size="15" fill="#58a6ff">Job &amp; Query Ingestion Trigger</text>
      <text x="25" y="70" class="body-text" font-size="12.5">Engineers submit Spark applications, Hive queries, or MR jobs</text>
      <text x="25" y="90" class="body-text" font-size="12.5">via Control Hub (:3030), JupyterLab (:8888), or Spark RPC (:7077).</text>
    </g>
  </g>

  <!-- CENTER REGION: HADOOP & SPARK DISTRIBUTED CLUSTER (Width: 1540) -->
  <g id="docker-container-boundary" transform="translate(620, 390)">
    <rect x="0" y="0" width="1540" height="1100" rx="20" fill="url(#cardGrad)" stroke="#1f6feb" stroke-width="2" filter="url(#shadow)" />

    <path d="M 0 20 Q 0 0 20 0 L 1520 0 Q 1540 0 1540 20 L 1540 60 L 0 60 Z" fill="url(#hdfsGrad)" opacity="0.18" />
    <rect x="30" y="16" width="430" height="30" rx="6" fill="#1f6feb" />
    <text x="245" y="36" class="heading" font-size="14" fill="#ffffff" text-anchor="middle">🐘 HADOOP &amp; SPARK CLUSTER CORE</text>

    <!-- Runtime Attributes Info Pill -->
    <g transform="translate(480, 16)">
      <rect x="0" y="0" width="1030" height="30" rx="6" fill="#161b22" stroke="#30363d" />
      <text x="20" y="20" class="mono" font-size="12" fill="#8b949e">
        <tspan fill="#58a6ff">HDFS:</tspan> 3.1.2 | <tspan fill="#fb7185">SPARK:</tspan> 3.5.1 | <tspan fill="#f59e0b">HIVE:</tspan> Metastore | <tspan fill="#3fb950">JAVA:</tspan> OpenJDK 8/11 | <tspan fill="#38bdf8">BRIDGE NET:</tspan> bigdata-net
      </text>
    </g>

    <!-- SUB-BOX A: DISTRIBUTED STORAGE LAYER (HDFS) [Width: 725] -->
    <g id="hdfs-storage-layer" transform="translate(30, 70)">
      <rect x="0" y="0" width="725" height="1000" rx="16" fill="#0d1117" stroke="#1f6feb" stroke-width="1.5" />
      
      <path d="M 0 16 Q 0 0 16 0 L 709 0 Q 725 0 725 16 L 725 46 L 0 46 Z" fill="#1f6feb" opacity="0.2" />
      <text x="25" y="30" class="heading" font-size="16" fill="#58a6ff">🗄️ HDFS DISTRIBUTED STORAGE LAYER</text>
      <rect x="535" y="10" width="170" height="26" rx="6" fill="#1f6feb" fill-opacity="0.3" stroke="#1f6feb" />
      <text x="620" y="27" class="badge" fill="#79c0ff" text-anchor="middle">RPC :9000 &bull; REST :9870</text>

      <!-- NameNode -->
      <g transform="translate(25, 55)">
        <rect x="0" y="0" width="675" height="265" rx="12" fill="#161b22" stroke="#388bfd" stroke-width="1.3" filter="url(#glowBlue)" />
        <rect x="15" y="14" width="220" height="28" rx="6" fill="#1f6feb" />
        <text x="125" y="32" class="heading" font-size="14" fill="#ffffff" text-anchor="middle">👑 NameNode (Master)</text>
        
        <rect x="500" y="14" width="160" height="28" rx="6" fill="#21262d" stroke="#30363d" />
        <text x="580" y="32" class="mono" font-size="12" fill="#79c0ff" text-anchor="middle">UI :9870 / WebHDFS</text>

        <text x="20" y="66" class="bold-text" font-size="13.5" fill="#e6edf3">Cluster Namespace Coordinator • Inodes Tree in RAM</text>
        
        <g transform="translate(20, 80)">
          <rect x="0" y="0" width="635" height="58" rx="8" fill="#0d1117" stroke="#21262d" />
          <text x="15" y="24" class="bold-text" font-size="12.5" fill="#58a6ff">🧠 In-Memory Namespace Tree (RAM)</text>
          <text x="15" y="44" class="body-text" font-size="11.5">Holds HDFS directory tree, file-to-block map, quotas, and WebHDFS REST endpoints</text>
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
            <text x="14" y="46" class="mono" font-size="10.5" fill="#8b949e">spark_employees.parquet</text>
            <text x="14" y="68" class="body-text" font-size="10.5" fill="#3fb950">CRC32C Verified ✓</text>
            <text x="14" y="88" class="body-text" font-size="10" fill="#8b949e">Localhost Block Storage</text>
          </g>
          <g transform="translate(217, 0)">
            <rect x="0" y="0" width="200" height="100" rx="8" fill="#0d1117" stroke="#1f6feb" stroke-dasharray="3,3" />
            <text x="14" y="24" class="bold-text" font-size="12" fill="#58a6ff">🧱 Block 2 (128 MB)</text>
            <text x="14" y="46" class="mono" font-size="10.5" fill="#8b949e">wordcount-sample.txt</text>
            <text x="14" y="68" class="body-text" font-size="10.5" fill="#3fb950">CRC32C Verified ✓</text>
            <text x="14" y="88" class="body-text" font-size="10" fill="#8b949e">Localhost Block Storage</text>
          </g>
          <g transform="translate(435, 0)">
            <rect x="0" y="0" width="200" height="100" rx="8" fill="#0d1117" stroke="#1f6feb" stroke-dasharray="3,3" />
            <text x="14" y="24" class="bold-text" font-size="12" fill="#58a6ff">🧱 Block 3 (128 MB)</text>
            <text x="14" y="46" class="mono" font-size="10.5" fill="#8b949e">/user/hive/warehouse</text>
            <text x="14" y="68" class="body-text" font-size="10.5" fill="#3fb950">CRC32C Verified ✓</text>
            <text x="14" y="88" class="body-text" font-size="10" fill="#8b949e">Hive Table Blocks</text>
          </g>
        </g>

        <!-- DataNode Heartbeats & Block Reports -->
        <g transform="translate(20, 198)">
          <rect x="0" y="0" width="635" height="82" rx="8" fill="#0d1117" stroke="#21262d" />
          <text x="15" y="24" class="bold-text" font-size="12" fill="#58a6ff">💓 Continuous Heartbeats (Every 3s) &amp; Block Reports (Every 6h)</text>
          <text x="15" y="44" class="body-text" font-size="11.5">If heartbeat missing for 10 minutes (600s), NameNode marks DataNode dead and</text>
          <text x="15" y="64" class="body-text" font-size="11.5">triggers automatic under-replicated block healing to surviving worker nodes.</text>
        </g>
      </g>

      <!-- Step 2 Indicator Pill -->
      <g transform="translate(25, 835)">
        <rect x="0" y="0" width="675" height="145" rx="12" fill="#1f6feb" fill-opacity="0.1" stroke="#1f6feb" stroke-width="1.2" />
        <circle cx="35" cy="35" r="16" fill="#1f6feb" />
        <text x="35" y="35" class="step-num">2</text>
        <text x="65" y="35" class="bold-text" font-size="15" fill="#58a6ff">Distributed Block Placement &amp; Persistence</text>
        <text x="25" y="70" class="body-text" font-size="12.5">Incoming data chunked into 128MB chunks. Writes stream</text>
        <text x="25" y="90" class="body-text" font-size="12.5">over Data Transfer Protocol (:9866). Inodes recorded in NameNode</text>
        <text x="25" y="110" class="body-text" font-size="12.5">WAL (<tspan class="mono" fill="#79c0ff">edits</tspan>) and committed to durable named Docker volumes.</text>
      </g>
    </g>

    <!-- SUB-BOX B: COMPUTE & SCHEDULING (YARN & SPARK) [Width: 725] -->
    <g id="compute-layer" transform="translate(785, 70)">
      <rect x="0" y="0" width="725" height="1000" rx="16" fill="#0d1117" stroke="#238636" stroke-width="1.5" />
      
      <path d="M 0 16 Q 0 0 16 0 L 709 0 Q 725 0 725 16 L 725 46 L 0 46 Z" fill="#238636" opacity="0.2" />
      <text x="25" y="30" class="heading" font-size="16" fill="#3fb950">⚡ YARN &amp; SPARK COMPUTE ENGINES</text>
      <rect x="545" y="10" width="160" height="26" rx="6" fill="#238636" fill-opacity="0.3" stroke="#3fb950" />
      <text x="625" y="27" class="badge" fill="#7ee787" text-anchor="middle">SPARK :7077 &bull; YARN :8088</text>

      <!-- Apache Spark Master & Worker -->
      <g transform="translate(25, 55)">
        <rect x="0" y="0" width="675" height="265" rx="12" fill="#161b22" stroke="#f43f5e" stroke-width="1.3" filter="url(#glowSpark)" />
        <rect x="15" y="14" width="250" height="28" rx="6" fill="#e11d48" />
        <text x="140" y="32" class="heading" font-size="14" fill="#ffffff" text-anchor="middle">⚡ Apache Spark 3.5 Master</text>
        
        <rect x="500" y="14" width="160" height="28" rx="6" fill="#21262d" stroke="#30363d" />
        <text x="580" y="32" class="mono" font-size="12" fill="#fb7185" text-anchor="middle">UI :8080 | RPC :7077</text>

        <text x="20" y="66" class="bold-text" font-size="13.5" fill="#e6edf3">In-Memory DAG Execution &bull; Distributed Spark Workers</text>
        
        <g transform="translate(20, 80)">
          <rect x="0" y="0" width="635" height="58" rx="8" fill="#0d1117" stroke="#21262d" />
          <text x="15" y="24" class="bold-text" font-size="12.5" fill="#fb7185">🧠 DAGScheduler &amp; TaskScheduler</text>
          <text x="15" y="44" class="body-text" font-size="11.5">Builds execution DAG of stages, optimizes shuffles, dispatches tasks to Worker Executors</text>
        </g>

        <g transform="translate(20, 148)">
          <g transform="translate(0, 0)">
            <rect x="0" y="0" width="310" height="100" rx="8" fill="#0d1117" stroke="#21262d" />
            <text x="14" y="24" class="bold-text" font-size="12" fill="#fb7185">🔨 Spark Worker (:8081)</text>
            <text x="14" y="46" class="body-text" font-size="11">2 CPU Cores &bull; 1024MB Memory</text>
            <text x="14" y="64" class="body-text" font-size="11">Executes in-memory Spark tasks</text>
            <text x="14" y="86" class="mono" font-size="10" fill="#fb7185">spark.master = spark://spark-master:7077</text>
          </g>
          <g transform="translate(325, 0)">
            <rect x="0" y="0" width="310" height="100" rx="8" fill="#0d1117" stroke="#21262d" />
            <text x="14" y="24" class="bold-text" font-size="12" fill="#fb7185">⏱️ Spark History Server</text>
            <text x="14" y="46" class="body-text" font-size="11">Event Log Profiler on Port :18080</text>
            <text x="14" y="64" class="body-text" font-size="11">Reads from hdfs://.../spark-logs</text>
            <text x="14" y="86" class="mono" font-size="10" fill="#fb7185">spark.history.fs.logDirectory</text>
          </g>
        </g>
      </g>

      <!-- YARN ResourceManager -->
      <g transform="translate(25, 335)">
        <rect x="0" y="0" width="675" height="240" rx="12" fill="#161b22" stroke="#2ea043" stroke-width="1.3" />
        <rect x="15" y="14" width="280" height="28" rx="6" fill="#238636" />
        <text x="155" y="32" class="heading" font-size="14" fill="#ffffff" text-anchor="middle">🧠 YARN ResourceManager (Master)</text>

        <rect x="525" y="14" width="135" height="28" rx="6" fill="#21262d" stroke="#30363d" />
        <text x="592" y="32" class="mono" font-size="12" fill="#7ee787" text-anchor="middle">Web UI :8088</text>

        <text x="20" y="66" class="bold-text" font-size="13.5" fill="#e6edf3">Capacity Scheduler &bull; 3072 MB Total Dynamic Memory Pool</text>

        <g transform="translate(20, 80)">
          <g transform="translate(0, 0)">
            <rect x="0" y="0" width="310" height="70" rx="8" fill="#0d1117" stroke="#21262d" />
            <text x="14" y="22" class="bold-text" font-size="12" fill="#3fb950">📋 ApplicationsManager (ASM)</text>
            <text x="14" y="42" class="body-text" font-size="11">Job submission gateway &amp; negotiator</text>
            <text x="14" y="58" class="mono" font-size="10" fill="#7ee787">yarn.resourcemanager.address</text>
          </g>
          <g transform="translate(325, 0)">
            <rect x="0" y="0" width="310" height="70" rx="8" fill="#0d1117" stroke="#21262d" />
            <text x="14" y="22" class="bold-text" font-size="12" fill="#3fb950">⚖️ CapacityScheduler</text>
            <text x="14" y="42" class="body-text" font-size="11">Pure resource allocation arbiter</text>
            <text x="14" y="58" class="mono" font-size="10" fill="#7ee787">yarn.scheduler.capacity.*</text>
          </g>
        </g>

        <g transform="translate(20, 160)">
          <rect x="0" y="0" width="635" height="65" rx="8" fill="#0d1117" stroke="#21262d" />
          <text x="15" y="22" class="bold-text" font-size="12" fill="#7ee787">🎯 Multi-Engine Orchestration: Spark on YARN &amp; MapReduce</text>
          <text x="15" y="42" class="body-text" font-size="11.5">Supports both standalone Spark and YARN client/cluster submissions (<tspan class="mono" fill="#7ee787">spark-submit --master yarn</tspan>).</text>
          <text x="15" y="58" class="mono" font-size="10.5" fill="#8b949e">Allocates 512MB slot containers with low-pause G1GC tuning.</text>
        </g>
      </g>

      <!-- YARN NodeManager & Containers -->
      <g transform="translate(25, 590)">
        <rect x="0" y="0" width="675" height="230" rx="12" fill="#161b22" stroke="#30363d" stroke-width="1.2" />
        <rect x="15" y="14" width="220" height="28" rx="6" fill="#21262d" stroke="#3fb950" stroke-width="1" />
        <text x="125" y="32" class="bold-text" font-size="13" fill="#3fb950" text-anchor="middle">👷 NodeManager (Worker)</text>

        <rect x="525" y="14" width="135" height="28" rx="6" fill="#21262d" stroke="#30363d" />
        <text x="592" y="32" class="mono" font-size="12" fill="#7ee787" text-anchor="middle">Web UI :8042</text>

        <text x="20" y="66" class="bold-text" font-size="13" fill="#c9d1d9">Slot Container Supervisor • vmem-check-enabled=false</text>

        <g transform="translate(20, 80)">
          <g transform="translate(0, 0)">
            <rect x="0" y="0" width="200" height="70" rx="8" fill="#0d1117" stroke="#238636" />
            <text x="12" y="22" class="bold-text" font-size="11.5" fill="#3fb950">📦 Container #001</text>
            <text x="12" y="40" class="mono" font-size="10" fill="#8b949e">ApplicationMaster</text>
            <text x="12" y="58" class="body-text" font-size="10" fill="#7ee787">Alloc: 512 MB</text>
          </g>
          <g transform="translate(217, 0)">
            <rect x="0" y="0" width="200" height="70" rx="8" fill="#0d1117" stroke="#238636" />
            <text x="12" y="22" class="bold-text" font-size="11.5" fill="#3fb950">📦 Container #002</text>
            <text x="12" y="40" class="mono" font-size="10" fill="#8b949e">Spark / MR Task</text>
            <text x="12" y="58" class="body-text" font-size="10" fill="#7ee787">Alloc: 512 MB</text>
          </g>
          <g transform="translate(435, 0)">
            <rect x="0" y="0" width="200" height="70" rx="8" fill="#0d1117" stroke="#238636" />
            <text x="12" y="22" class="bold-text" font-size="11.5" fill="#3fb950">📦 Container #003</text>
            <text x="12" y="40" class="mono" font-size="10" fill="#8b949e">Spark / MR Task</text>
            <text x="12" y="58" class="body-text" font-size="10" fill="#7ee787">Alloc: 512 MB</text>
          </g>
        </g>

        <!-- JobHistory Server Link -->
        <g transform="translate(20, 160)">
          <rect x="0" y="0" width="635" height="55" rx="8" fill="#0d1117" stroke="#21262d" />
          <text x="15" y="22" class="bold-text" font-size="12" fill="#d2a8ff">📜 MapReduce JobHistoryServer (Port :19888)</text>
          <text x="15" y="42" class="body-text" font-size="11.5">Archives completed tasks, aggregated container logs, and diagnostic counters.</text>
        </g>
      </g>

      <!-- Step 3 Indicator Pill -->
      <g transform="translate(25, 835)">
        <rect x="0" y="0" width="675" height="145" rx="12" fill="#238636" fill-opacity="0.1" stroke="#238636" stroke-width="1.2" />
        <circle cx="35" cy="35" r="16" fill="#238636" />
        <text x="35" y="35" class="step-num">3</text>
        <text x="65" y="35" class="bold-text" font-size="15" fill="#3fb950">Resource Negotiation &amp; Container Dispatch</text>
        <text x="25" y="70" class="body-text" font-size="12.5">Spark Master launches worker executors, while YARN allocates</text>
        <text x="25" y="90" class="body-text" font-size="12.5">isolated container slots with strict memory guards (512MB default).</text>
        <text x="25" y="110" class="body-text" font-size="12.5">Data locality reads 128MB HDFS blocks directly from local DataNode.</text>
      </g>
    </g>
  </g>

  <!-- RIGHT COLUMN: ANALYTICS & PROCESSING FRAMEWORKS (Width: 520) -->
  <g id="analytics-frameworks-layer" transform="translate(2220, 390)">
    <rect x="0" y="0" width="520" height="1100" rx="16" fill="url(#cardGrad)" stroke="#8957e5" stroke-width="1.5" stroke-dasharray="6,4" filter="url(#shadow)" />

    <path d="M 0 16 Q 0 0 16 0 L 504 0 Q 520 0 520 16 L 520 54 L 0 54 Z" fill="url(#engineGrad)" opacity="0.15" />
    <rect x="20" y="14" width="310" height="26" rx="6" fill="#8957e5" />
    <text x="175" y="32" class="heading" font-size="13" fill="#ffffff" text-anchor="middle">⚡ ANALYTICS &amp; PROCESSING</text>
    <text x="20" y="80" class="subheading" font-size="15" fill="#bc8cff">Distributed Computing Engines</text>
    <text x="20" y="100" class="body-text" font-size="13">Spark, Hive, MapReduce &amp; Streaming Frameworks</text>

    <!-- Engine 1: Apache Spark / PySpark -->
    <g transform="translate(20, 115)">
      <rect x="0" y="0" width="480" height="185" rx="12" fill="#0d1117" stroke="#f43f5e" stroke-width="1.3" />
      <text x="20" y="28" class="bold-text" font-size="15" fill="#fb7185">🔥 Apache Spark &amp; PySpark</text>
      <text x="20" y="48" class="body-text" font-size="12">In-Memory DataFrames, SQL &amp; Snappy Parquet:</text>

      <rect x="18" y="60" width="444" height="48" rx="6" fill="#161b22" />
      <text x="28" y="78" class="mono" font-size="11" fill="#fb7185">spark = SparkSession.builder.master("spark://...").getOrCreate()</text>
      <text x="28" y="96" class="mono" font-size="11" fill="#34d399">df.write.mode("overwrite").parquet("hdfs://localhost:9000/...")</text>

      <text x="20" y="132" class="mono" font-size="11" fill="#fb7185">examples/spark-pyspark/pyspark_hdfs_read_write.py</text>
      <text x="20" y="152" class="body-text" font-size="11.5">Predicate pushdown, column pruning &amp; 100x faster than MR</text>
    </g>

    <!-- Engine 2: Apache Hive Warehousing -->
    <g transform="translate(20, 310)">
      <rect x="0" y="0" width="480" height="175" rx="12" fill="#0d1117" stroke="#f59e0b" stroke-width="1.3" />
      <text x="20" y="28" class="bold-text" font-size="15" fill="#fcd34d">🐝 Apache Hive Data Warehouse</text>
      <text x="20" y="48" class="body-text" font-size="12">SQL over HDFS Storage &amp; HiveServer2 JDBC:</text>

      <rect x="18" y="60" width="444" height="48" rx="6" fill="#161b22" />
      <text x="28" y="78" class="mono" font-size="11" fill="#fcd34d">CREATE EXTERNAL TABLE ... LOCATION '/user/hive/warehouse'</text>
      <text x="28" y="96" class="mono" font-size="11" fill="#38bdf8">beeline -u jdbc:hive2://localhost:10000 -n hduser</text>

      <text x="20" y="132" class="mono" font-size="11" fill="#f59e0b">Metastore Thrift :9083 &bull; Web UI :10002</text>
      <text x="20" y="152" class="body-text" font-size="11.5">Schemas, partitions, and relational analytics over Big Data</text>
    </g>

    <!-- Engine 3: Native Java MapReduce -->
    <g transform="translate(20, 495)">
      <rect x="0" y="0" width="480" height="160" rx="12" fill="#0d1117" stroke="#30363d" stroke-width="1.2" />
      <text x="20" y="28" class="bold-text" font-size="15" fill="#bc8cff">☕ Native Java MapReduce</text>
      <text x="20" y="48" class="body-text" font-size="12">Enterprise compiled JAR application execution:</text>

      <rect x="18" y="60" width="444" height="48" rx="6" fill="#161b22" />
      <text x="28" y="78" class="mono" font-size="11" fill="#58a6ff">hadoop jar hadoop-mapreduce-examples-*.jar pi 2 10</text>
      <text x="28" y="96" class="mono" font-size="11" fill="#7ee787">javac -cp $(hadoop classpath) -d . WordCount.java</text>

      <text x="20" y="132" class="mono" font-size="11" fill="#bc8cff">examples/mapreduce-java/compile-and-run.sh</text>
    </g>

    <!-- Engine 4: Python Hadoop Streaming -->
    <g transform="translate(20, 665)">
      <rect x="0" y="0" width="480" height="155" rx="12" fill="#0d1117" stroke="#30363d" stroke-width="1.2" />
      <text x="20" y="28" class="bold-text" font-size="15" fill="#58a6ff">🐍 Python Hadoop Streaming</text>
      <text x="20" y="48" class="body-text" font-size="12">UNIX pipeline streaming mapper.py &amp; reducer.py:</text>

      <rect x="18" y="60" width="444" height="45" rx="6" fill="#161b22" />
      <text x="28" y="78" class="mono" font-size="11" fill="#79c0ff">cat data.txt | python mapper.py | sort |</text>
      <text x="28" y="94" class="mono" font-size="11" fill="#7ee787">python reducer.py  (Packaged via hadoop-streaming)</text>

      <text x="20" y="130" class="mono" font-size="11" fill="#bc8cff">examples/mapreduce-python/run.sh</text>
    </g>

    <!-- Step 4 & 5 Indicator Pill -->
    <g transform="translate(20, 830)">
      <rect x="0" y="0" width="480" height="250" rx="12" fill="#8957e5" fill-opacity="0.1" stroke="#8957e5" stroke-width="1.2" />
      <circle cx="35" cy="35" r="16" fill="#8957e5" />
      <text x="35" y="35" class="step-num">4</text>
      <text x="65" y="35" class="bold-text" font-size="15" fill="#bc8cff">Task Execution &amp; Shuffling</text>
      
      <text x="25" y="70" class="body-text" font-size="12.5">• Spark tasks run in executor memory (100x faster than disk).</text>
      <text x="25" y="92" class="body-text" font-size="12.5">• Intermediate key-values partitioned and shuffled across network.</text>
      <text x="25" y="114" class="body-text" font-size="12.5">• Reducers aggregate and sort grouped datasets.</text>

      <circle cx="35" cy="155" r="16" fill="#8957e5" />
      <text x="35" y="155" class="step-num">5</text>
      <text x="65" y="155" class="bold-text" font-size="15" fill="#bc8cff">Result Aggregation &amp; Output</text>
      <text x="25" y="185" class="body-text" font-size="12.5">Aggregated Parquet or CSV output written back to</text>
      <text x="25" y="205" class="body-text" font-size="12.5">HDFS DataNode (or GCS <tspan class="mono" fill="#38bdf8">gs://</tspan> bucket on Dataproc).</text>
      <text x="25" y="230" class="mono" font-size="11" fill="#3fb950">Status verified: SUCCESS across all pipeline stages.</text>
    </g>
  </g>

  <!-- ========================================================================= -->
  <!-- 4. BOTTOM PERSISTENCE SECTION                                             -->
  <!-- ========================================================================= -->
  <g id="docker-volumes-section" transform="translate(60, 1515)">
    <rect x="0" y="0" width="2680" height="180" rx="16" fill="url(#cardGrad)" stroke="#da3633" stroke-width="1.5" filter="url(#shadow)" />

    <path d="M 0 16 Q 0 0 16 0 L 16 0 L 16 180 L 0 180 Z" fill="url(#volGrad)" />
    <rect x="30" y="16" width="370" height="28" rx="6" fill="#da3633" fill-opacity="0.2" stroke="#da3633" stroke-width="1.2" />
    <text x="215" y="35" class="heading" font-size="13" fill="#f85149" text-anchor="middle">💾 PERSISTENT DISTRIBUTED STORAGE &amp; VOLUMES</text>
    <text x="420" y="35" class="body-text" font-size="13">Zero Data Loss: Named Docker Volumes, Spark Event Logs &amp; Cloud Storage (gs://)</text>

    <g transform="translate(2540, 20)">
      <circle cx="20" cy="20" r="18" fill="#da3633" />
      <text x="20" y="20" class="step-num">7</text>
    </g>

    <g transform="translate(30, 60)">
      <g transform="translate(0, 0)">
        <rect x="0" y="0" width="510" height="95" rx="10" fill="#0d1117" stroke="#30363d" stroke-width="1.2" />
        <text x="18" y="28" class="bold-text" font-size="13" fill="#58a6ff">📁 hadoop_namenode_data</text>
        <text x="18" y="50" class="mono" font-size="11.5" fill="#79c0ff">Container: /usr/local/hadoop/hdfs/namenode</text>
        <text x="18" y="74" class="body-text" font-size="11.5">Filesystem namespace tree, fsimage snapshots, and edits WAL</text>
      </g>

      <g transform="translate(535, 0)">
        <rect x="0" y="0" width="510" height="95" rx="10" fill="#0d1117" stroke="#30363d" stroke-width="1.2" />
        <text x="18" y="28" class="bold-text" font-size="13" fill="#58a6ff">🧱 hadoop_datanode_data</text>
        <text x="18" y="50" class="mono" font-size="11.5" fill="#79c0ff">Container: /usr/local/hadoop/hdfs/datanode</text>
        <text x="18" y="74" class="body-text" font-size="11.5">Raw 128MB replicated data blocks (blk_* and blk_*.meta checksums)</text>
      </g>

      <g transform="translate(1070, 0)">
        <rect x="0" y="0" width="510" height="95" rx="10" fill="#0d1117" stroke="#30363d" stroke-width="1.2" />
        <text x="18" y="28" class="bold-text" font-size="13" fill="#fb7185">⚡ spark_event_logs_data</text>
        <text x="18" y="50" class="mono" font-size="11.5" fill="#fb7185">Path: /spark-logs &bull; /opt/bitnami/spark/events</text>
        <text x="18" y="74" class="body-text" font-size="11.5">Spark DAG event logs &bull; Picked up by Spark History Server (:18080)</text>
      </g>

      <g transform="translate(1605, 0)">
        <rect x="0" y="0" width="510" height="95" rx="10" fill="#0d1117" stroke="#30363d" stroke-width="1.2" />
        <text x="18" y="28" class="bold-text" font-size="13" fill="#3fb950">📦 hadoop_tmp_data &amp; GCS</text>
        <text x="18" y="50" class="mono" font-size="11.5" fill="#7ee787">Path: /app/hadoop/tmp | gs://bucket/staging</text>
        <text x="18" y="74" class="body-text" font-size="11.5">Shuffle spills, temporary intermediate buffers, and cloud staging</text>
      </g>

      <g transform="translate(2140, 0)">
        <rect x="0" y="0" width="510" height="95" rx="10" fill="#0d1117" stroke="#30363d" stroke-width="1.2" />
        <text x="18" y="28" class="bold-text" font-size="13" fill="#bc8cff">📜 jupyter_notebooks_data</text>
        <text x="18" y="50" class="mono" font-size="11.5" fill="#d2a8ff">Container: /home/jovyan/work</text>
        <text x="18" y="74" class="body-text" font-size="11.5">Persisted PySpark pipelines, Jupyter notebooks, and dataset artifacts</text>
      </g>
    </g>
  </g>

  <!-- ========================================================================= -->
  <!-- 5. BOTTOM FOOTER BAR                                                      -->
  <!-- ========================================================================= -->
  <g id="footer-bar" transform="translate(60, 1720)">
    <rect x="0" y="0" width="2680" height="85" rx="12" fill="#151b28" stroke="#30363d" stroke-width="1.2" />
    
    <text x="30" y="32" class="bold-text" font-size="13.5" fill="#ffffff">UNIFIED BIG DATA ARCHITECTURE SPECIFICATIONS SUMMARY:</text>
    <text x="30" y="58" class="body-text" font-size="12">
      • <tspan fill="#58a6ff">HDFS Block Size:</tspan> 128 MB | <tspan fill="#fb7185">Spark Standalone:</tspan> 7077/8080 | <tspan fill="#f59e0b">Hive Warehouse:</tspan> /user/hive/warehouse | <tspan fill="#34d399">Control Hub:</tspan> Port 3030 | <tspan fill="#7ee787">JupyterLab:</tspan> Port 8888 | <tspan fill="#bc8cff">YARN Pool:</tspan> 3072MB | <tspan fill="#38bdf8">Cloud:</tspan> Dataproc 2.1
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

    <text x="48" y="54" class="title" font-size="30" letter-spacing="0.5">
      🏛️ DISTRIBUTED BIG DATA ARCHITECTURE BLUEPRINT (HADOOP + SPARK + HIVE + SQOOP + OOZIE)
    </text>
    <text x="48" y="90" class="subtitle" font-size="14.5">
      Protobuf RPC Bus • Inode Memory Graph • Spark DAG Scheduling • Hive Warehousing • Sqoop Ingestion • Oozie Orchestration • Control Hub (:3030)
    </text>

    <!-- Architecture Badges Row -->
    <g transform="translate(1340, 36)">
      <g transform="translate(0, 0)">
        <rect x="0" y="0" width="165" height="34" rx="8" fill="#1f6feb" fill-opacity="0.2" stroke="#388bfd" stroke-width="1.2" />
        <text x="82" y="22" class="badge" fill="#58a6ff" text-anchor="middle">PROTOBUF RPC :9000</text>
      </g>
      <g transform="translate(175, 0)">
        <rect x="0" y="0" width="165" height="34" rx="8" fill="#e11d48" fill-opacity="0.2" stroke="#f43f5e" stroke-width="1.2" />
        <text x="82" y="22" class="badge" fill="#fb7185" text-anchor="middle">SPARK MASTER :7077</text>
      </g>
      <g transform="translate(350, 0)">
        <rect x="0" y="0" width="165" height="34" rx="8" fill="#238636" fill-opacity="0.2" stroke="#3fb950" stroke-width="1.2" />
        <text x="82" y="22" class="badge" fill="#56d364" text-anchor="middle">YARN SCHEDULER :8030</text>
      </g>
      <g transform="translate(525, 0)">
        <rect x="0" y="0" width="165" height="34" rx="8" fill="#d97706" fill-opacity="0.2" stroke="#f59e0b" stroke-width="1.2" />
        <text x="82" y="22" class="badge" fill="#fcd34d" text-anchor="middle">HIVE &amp; SQOOP</text>
      </g>
      <g transform="translate(700, 0)">
        <rect x="0" y="0" width="165" height="34" rx="8" fill="#8957e5" fill-opacity="0.2" stroke="#bc8cff" stroke-width="1.2" />
        <text x="82" y="22" class="badge" fill="#d2a8ff" text-anchor="middle">OOZIE &amp; PIG</text>
      </g>
      <g transform="translate(875, 0)">
        <rect x="0" y="0" width="155" height="34" rx="8" fill="#0284c7" fill-opacity="0.2" stroke="#38bdf8" stroke-width="1.2" />
        <text x="77" y="22" class="badge" fill="#38bdf8" text-anchor="middle">HUB CONSOLE :3030</text>
      </g>
      <text x="1030" y="72" class="body-text" font-size="12" fill="#8b949e" text-anchor="end">
        Production-Ready Multi-Platform Reference Implementation
      </text>
    </g>
  </g>

  <!-- ========================================================================= -->
  <!-- 2. PROTOCOL & NETWORK BUS LAYER (4 PILLARS ACROSS 2680px)                 -->
  <!-- ========================================================================= -->
  <g id="protocol-layer" transform="translate(60, 205)">
    <rect x="0" y="0" width="2680" height="165" rx="16" fill="url(#cardGrad)" stroke="#30363d" stroke-width="1.5" filter="url(#shadow)" />
    
    <rect x="25" y="16" width="370" height="28" rx="6" fill="#388bfd" fill-opacity="0.15" stroke="#388bfd" stroke-width="1" />
    <text x="210" y="35" class="subheading" font-size="13" fill="#58a6ff" text-anchor="middle">🌐 4 DISTRIBUTED PROTOCOLS &amp; BUS TOPOLOGY</text>

    <!-- Pillar 1: RPC Protocol -->
    <g transform="translate(25, 55)">
      <rect x="0" y="0" width="640" height="95" rx="10" fill="#0d1117" stroke="#388bfd" stroke-width="1.2" />
      <text x="16" y="26" class="bold-text" font-size="13.5" fill="#58a6ff">🔌 Hadoop RPC &amp; WebHDFS (:9000 / :9870)</text>
      <text x="16" y="48" class="body-text" font-size="11.5">Protobuf over TCP for filesystem requests + WebHDFS REST API for Control Hub.</text>
      <rect x="16" y="60" width="608" height="22" rx="4" fill="#161b22" />
      <text x="24" y="75" class="mono" font-size="10.5" fill="#79c0ff">ClientProtocol.proto • SafeMode checks • Inodes lookup • Block allocation leases</text>
    </g>

    <!-- Pillar 2: Spark Standalone RPC -->
    <g transform="translate(685, 55)">
      <rect x="0" y="0" width="640" height="95" rx="10" fill="#0d1117" stroke="#f43f5e" stroke-width="1.2" />
      <text x="16" y="26" class="bold-text" font-size="13.5" fill="#fb7185">⚡ Spark Cluster Manager RPC (:7077)</text>
      <text x="16" y="48" class="body-text" font-size="11.5">High-throughput Netty transport for driver-to-executor communication &amp; stage dispatch.</text>
      <rect x="16" y="60" width="608" height="22" rx="4" fill="#161b22" />
      <text x="24" y="75" class="mono" font-size="10.5" fill="#fb7185">RegisterApplication • LaunchExecutor • HeartbeatReceiver • StatusUpdate</text>
    </g>

    <!-- Pillar 3: Data Transfer Protocol -->
    <g transform="translate(1345, 55)">
      <rect x="0" y="0" width="640" height="95" rx="10" fill="#0d1117" stroke="#3fb950" stroke-width="1.2" />
      <text x="16" y="26" class="bold-text" font-size="13.5" fill="#56d364">🌊 Streaming Block Protocol (:9866 Data Transfer)</text>
      <text x="16" y="48" class="body-text" font-size="11.5">High-throughput TCP streaming pipeline with 64KB data packets and ACK back-propagation.</text>
      <rect x="16" y="60" width="608" height="22" rx="4" fill="#161b22" />
      <text x="24" y="75" class="mono" font-size="10.5" fill="#7ee787">OpWriteBlock • OpReadBlock • Checksum 512B CRC32C • Direct Linux zero-copy</text>
    </g>

    <!-- Pillar 4: YARN IPC & Control Hub REST -->
    <g transform="translate(2005, 55)">
      <rect x="0" y="0" width="650" height="95" rx="10" fill="#0d1117" stroke="#f59e0b" stroke-width="1.2" />
      <text x="16" y="26" class="bold-text" font-size="13.5" fill="#fcd34d">⚙️ YARN IPC (:8030-:8033) &amp; Hub REST (:3030)</text>
      <text x="16" y="48" class="body-text" font-size="11.5">Heartbeats, slot claims, container allocations, and Unified Hub telemetry probes.</text>
      <rect x="16" y="60" width="618" height="22" rx="4" fill="#161b22" />
      <text x="24" y="75" class="mono" font-size="10.5" fill="#fcd34d">ApplicationClientProtocol • ResourceTracker • ContainerManagement • Hub REST API</text>
    </g>
  </g>

  <!-- ========================================================================= -->
  <!-- 3. MAIN ARCHITECTURAL COLUMNS (HDFS STORAGE + YARN/SPARK COMPUTE)         -->
  <!-- ========================================================================= -->

  <!-- LEFT HALF: DISTRIBUTED STORAGE LAYER (Width: 1320) -->
  <g id="arch-hdfs" transform="translate(60, 390)">
    <rect x="0" y="0" width="1320" height="1100" rx="18" fill="url(#cardGrad)" stroke="#1f6feb" stroke-width="2" filter="url(#shadow)" />
    
    <path d="M 0 18 Q 0 0 18 0 L 1302 0 Q 1320 0 1320 18 L 1320 50 L 0 50 Z" fill="#1f6feb" opacity="0.18" />
    <rect x="25" y="12" width="370" height="28" rx="6" fill="#1f6feb" />
    <text x="210" y="31" class="heading" font-size="13" fill="#ffffff" text-anchor="middle">🗄️ HDFS INTERNALS &amp; METADATA ENGINE</text>

    <!-- NameNode Deep Dive -->
    <g transform="translate(25, 60)">
      <rect x="0" y="0" width="1270" height="420" rx="14" fill="#0d1117" stroke="#388bfd" stroke-width="1.3" />
      
      <rect x="20" y="16" width="310" height="28" rx="6" fill="#1f6feb" />
      <text x="175" y="35" class="heading" font-size="14" fill="#ffffff" text-anchor="middle">👑 NameNode Architecture (:9870 / :9000)</text>
      
      <text x="350" y="35" class="bold-text" font-size="13" fill="#8b949e">Inode Memory Graph • FSImage Snapshots • WAL Journal • WebHDFS API</text>

      <!-- Inode Tree Diagram Box -->
      <g transform="translate(20, 60)">
        <rect x="0" y="0" width="600" height="340" rx="10" fill="#161b22" stroke="#21262d" />
        <text x="18" y="26" class="bold-text" font-size="13.5" fill="#58a6ff">🌳 In-Memory Inode Hierarchy (Zero-Disk Namespace)</text>
        <text x="18" y="46" class="body-text" font-size="11.5">Every file &amp; folder occupies ~150 bytes of JVM heap memory:</text>

        <!-- Inode Tree Mockup -->
        <g transform="translate(20, 65)">
          <rect x="0" y="0" width="150" height="36" rx="6" fill="#0d1117" stroke="#1f6feb" />
          <text x="75" y="23" class="mono" font-size="11.5" fill="#79c0ff" text-anchor="middle">INodeDirectory ("/")</text>

          <line x1="75" y1="36" x2="75" y2="60" stroke="#388bfd" stroke-width="1.5" />
          <line x1="75" y1="60" x2="250" y2="60" stroke="#388bfd" stroke-width="1.5" />

          <!-- Children -->
          <g transform="translate(0, 75)">
            <rect x="0" y="0" width="170" height="34" rx="6" fill="#0d1117" stroke="#21262d" />
            <text x="85" y="22" class="mono" font-size="11" fill="#c9d1d9" text-anchor="middle">INodeDirectory ("/user")</text>
          </g>

          <g transform="translate(190, 75)">
            <rect x="0" y="0" width="180" height="34" rx="6" fill="#0d1117" stroke="#f43f5e" />
            <text x="90" y="22" class="mono" font-size="11" fill="#fb7185" text-anchor="middle">INodeDirectory ("/spark-logs")</text>
          </g>

          <g transform="translate(390, 75)">
            <rect x="0" y="0" width="165" height="34" rx="6" fill="#0d1117" stroke="#f59e0b" />
            <text x="82" y="22" class="mono" font-size="11" fill="#fcd34d" text-anchor="middle">INode ("/user/hive/...")</text>
          </g>

          <!-- Grandchildren Files -->
          <g transform="translate(0, 130)">
            <rect x="0" y="0" width="555" height="50" rx="6" fill="#0d1117" stroke="#388bfd" stroke-width="1" />
            <text x="14" y="22" class="mono" font-size="11" fill="#58a6ff">INodeFile: "spark_employees.parquet"</text>
            <text x="14" y="38" class="body-text" font-size="10.5">Replication=1 • BlockID: blk_1073741825 (128MB) • Inode: 16384</text>
          </g>

          <g transform="translate(0, 190)">
            <rect x="0" y="0" width="555" height="50" rx="6" fill="#0d1117" stroke="#388bfd" stroke-width="1" />
            <text x="14" y="22" class="mono" font-size="11" fill="#58a6ff">INodeFile: "wordcount-sample.txt"</text>
            <text x="14" y="38" class="body-text" font-size="10.5">Replication=1 • BlockID: blk_1073741826 (128MB) • Inode: 16385</text>
          </g>
        </g>
      </g>

      <!-- FSImage & Edits Box -->
      <g transform="translate(640, 60)">
        <rect x="0" y="0" width="610" height="340" rx="10" fill="#161b22" stroke="#21262d" />
        <text x="18" y="26" class="bold-text" font-size="13.5" fill="#58a6ff">💾 Persistence Engine (fsimage + edits WAL)</text>
        <text x="18" y="46" class="body-text" font-size="11.5">Non-volatile storage maintaining cluster state across restarts:</text>

        <g transform="translate(18, 65)">
          <rect x="0" y="0" width="280" height="150" rx="8" fill="#0d1117" stroke="#21262d" />
          <text x="14" y="24" class="bold-text" font-size="12" fill="#79c0ff">📄 fsimage_0000000000000000042</text>
          <text x="14" y="46" class="body-text" font-size="11">• Serialized Protobuf snapshot</text>
          <text x="14" y="66" class="body-text" font-size="11">• Fast sequential disk loading</text>
          <text x="14" y="86" class="body-text" font-size="11">• Stored in <tspan class="mono" fill="#58a6ff">dfs.namenode.name.dir</tspan></text>
          <text x="14" y="110" class="mono" font-size="10.5" fill="#3fb950">Status: Verified Clean Image</text>
        </g>

        <g transform="translate(315, 65)">
          <rect x="0" y="0" width="280" height="150" rx="8" fill="#0d1117" stroke="#21262d" />
          <text x="14" y="24" class="bold-text" font-size="12" fill="#79c0ff">📝 edits_inprogress_000000043</text>
          <text x="14" y="46" class="body-text" font-size="11">• Write-Ahead Journal (WAL)</text>
          <text x="14" y="66" class="body-text" font-size="11">• Flushed &amp; synced on client ACK</text>
          <text x="14" y="86" class="body-text" font-size="11">• SecondaryNameNode checkpoints</text>
          <text x="14" y="110" class="mono" font-size="10.5" fill="#f59e0b">Status: Active Journal Stream</text>
        </g>

        <g transform="translate(18, 230)">
          <rect x="0" y="0" width="577" height="90" rx="8" fill="#0d1117" stroke="#1f6feb" stroke-dasharray="4,4" />
          <text x="16" y="24" class="bold-text" font-size="12" fill="#58a6ff">🔄 Checkpointing Lifecycle (SecondaryNameNode :9868):</text>
          <text x="16" y="46" class="body-text" font-size="11.5">1. SNN fetches fsimage &amp; edits via HTTP GET from NameNode.</text>
          <text x="16" y="66" class="body-text" font-size="11.5">2. Merges transactions in SNN memory ➔ Ships fsimage.ckpt back via HTTP POST.</text>
        </g>
      </g>
    </g>

    <!-- DataNode Deep Dive -->
    <g transform="translate(25, 500)">
      <rect x="0" y="0" width="1270" height="570" rx="14" fill="#0d1117" stroke="#388bfd" stroke-width="1.3" />
      
      <rect x="20" y="16" width="310" height="28" rx="6" fill="#1f6feb" />
      <text x="175" y="35" class="heading" font-size="14" fill="#ffffff" text-anchor="middle">📦 DataNode Storage &amp; Streaming Pipeline</text>
      
      <text x="350" y="35" class="bold-text" font-size="13" fill="#8b949e">128MB Chunks • Checksum Verification (CRC32C) • Zero-Copy Kernel Transfer</text>

      <!-- Chunk Pipeline Diagram -->
      <g transform="translate(20, 60)">
        <rect x="0" y="0" width="1230" height="220" rx="10" fill="#161b22" stroke="#21262d" />
        <text x="18" y="28" class="bold-text" font-size="13.5" fill="#58a6ff">🧱 3-Stage Client Write Pipeline (DataStreamer &amp; Packet ACKs)</text>
        <text x="18" y="48" class="body-text" font-size="11.5">How Spark &amp; MapReduce applications stream data directly into HDFS DataNode storage:</text>

        <!-- Stage 1 -->
        <g transform="translate(20, 65)">
          <rect x="0" y="0" width="370" height="135" rx="8" fill="#0d1117" stroke="#1f6feb" />
          <text x="16" y="24" class="bold-text" font-size="12" fill="#79c0ff">Stage 1: Leases &amp; Block Allocation</text>
          <text x="16" y="46" class="body-text" font-size="11">• Client requests lease from NameNode</text>
          <text x="16" y="66" class="body-text" font-size="11">• NameNode returns target DataNode list</text>
          <text x="16" y="86" class="body-text" font-size="11">• Client connects to DataNode on port :9866</text>
          <text x="16" y="112" class="mono" font-size="10.5" fill="#3fb950">RPC :9000 ➔ TCP Socket :9866</text>
        </g>

        <!-- Stage 2 -->
        <g transform="translate(420, 65)">
          <rect x="0" y="0" width="370" height="135" rx="8" fill="#0d1117" stroke="#1f6feb" />
          <text x="16" y="24" class="bold-text" font-size="12" fill="#79c0ff">Stage 2: 64KB Packet Streaming</text>
          <text x="16" y="46" class="body-text" font-size="11">• Client divides block into 64KB packets</text>
          <text x="16" y="66" class="body-text" font-size="11">• Packets queued in dataQueue memory buffer</text>
          <text x="16" y="86" class="body-text" font-size="11">• Streamed over TCP to DataNode 1</text>
          <text x="16" y="112" class="mono" font-size="10.5" fill="#3fb950">DataStreamer Thread (64KB chunks)</text>
        </g>

        <!-- Stage 3 -->
        <g transform="translate(820, 65)">
          <rect x="0" y="0" width="390" height="135" rx="8" fill="#0d1117" stroke="#1f6feb" />
          <text x="16" y="24" class="bold-text" font-size="12" fill="#79c0ff">Stage 3: Verification &amp; Commit</text>
          <text x="16" y="46" class="body-text" font-size="11">• DataNode computes 512B CRC32C checksums</text>
          <text x="16" y="66" class="body-text" font-size="11">• Flushes to disk (<tspan class="mono" fill="#58a6ff">blk_*</tspan> and <tspan class="mono" fill="#58a6ff">blk_*.meta</tspan>)</text>
          <text x="16" y="86" class="body-text" font-size="11">• Sends ACK packet upstream to client</text>
          <text x="16" y="112" class="mono" font-size="10.5" fill="#3fb950">ResponseProcessor ACK Verified ✓</text>
        </g>
      </g>

      <!-- Block Layout Details -->
      <g transform="translate(20, 300)">
        <rect x="0" y="0" width="1230" height="245" rx="10" fill="#161b22" stroke="#21262d" />
        <text x="18" y="28" class="bold-text" font-size="13.5" fill="#ffffff">🧱 Physical Storage Directory Layout on Docker Volume (hadoop_datanode_data):</text>
        
        <text x="18" y="55" class="body-text" font-size="12">
          Inside container: <tspan class="mono" fill="#58a6ff">/usr/local/hadoop/yarn_data/hdfs/datanode/current/BP-*-*/current/finalized/subdir0/subdir0/</tspan>
        </text>

        <g transform="translate(18, 70)">
          <rect x="0" y="0" width="585" height="155" rx="8" fill="#0d1117" stroke="#21262d" />
          <text x="14" y="24" class="bold-text" font-size="12" fill="#79c0ff">📦 Raw Data Block File: blk_1073741825</text>
          <text x="14" y="46" class="body-text" font-size="11">• Exact binary payload of Parquet / CSV records</text>
          <text x="14" y="66" class="body-text" font-size="11">• Size on disk: Matches file size (not rounded to 128MB)</text>
          <text x="14" y="86" class="body-text" font-size="11">• Linux ext4 / XFS block storage filesystem</text>
          <text x="14" y="110" class="mono" font-size="10.5" fill="#3fb950">No padding waste • Zero storage bloat</text>
        </g>

        <g transform="translate(620, 70)">
          <rect x="0" y="0" width="590" height="155" rx="8" fill="#0d1117" stroke="#21262d" />
          <text x="14" y="24" class="bold-text" font-size="12" fill="#79c0ff">🛡️ Metadata Checksum File: blk_1073741825_1001.meta</text>
          <text x="14" y="46" class="body-text" font-size="11">• CRC32C checksums stored for every 512 bytes</text>
          <text x="14" y="66" class="body-text" font-size="11">• Background BlockScanner periodically audits integrity</text>
          <text x="14" y="86" class="body-text" font-size="11">• Automatic silent corruption detection &amp; self-healing</text>
          <text x="14" y="110" class="mono" font-size="10.5" fill="#3fb950">Bit rot protection • 100% data integrity</text>
        </g>
      </g>
    </g>
  </g>

  <!-- RIGHT HALF: SPARK & YARN COMPUTE & EXECUTION (Width: 1320) -->
  <g id="arch-compute" transform="translate(1420, 390)">
    <rect x="0" y="0" width="1320" height="1100" rx="18" fill="url(#cardGrad)" stroke="#f43f5e" stroke-width="2" filter="url(#shadow)" />
    
    <path d="M 0 18 Q 0 0 18 0 L 1302 0 Q 1320 0 1320 18 L 1320 50 L 0 50 Z" fill="#f43f5e" opacity="0.18" />
    <rect x="25" y="12" width="370" height="28" rx="6" fill="#e11d48" />
    <text x="210" y="31" class="heading" font-size="13" fill="#ffffff" text-anchor="middle">⚡ SPARK &amp; YARN DISTRIBUTED ENGINES</text>

    <!-- Spark Standalone Cluster Architecture -->
    <g transform="translate(25, 60)">
      <rect x="0" y="0" width="1270" height="420" rx="14" fill="#0d1117" stroke="#f43f5e" stroke-width="1.3" filter="url(#glowSpark)" />
      
      <rect x="20" y="16" width="340" height="28" rx="6" fill="#e11d48" />
      <text x="190" y="35" class="heading" font-size="14" fill="#ffffff" text-anchor="middle">⚡ Apache Spark 3.5 Standalone Master</text>
      
      <text x="380" y="35" class="bold-text" font-size="13" fill="#8b949e">DAG Scheduler • Task Sets • In-Memory RDD/DataFrame Cache • Port :8080</text>

      <!-- Spark DAG Scheduling & Stages -->
      <g transform="translate(20, 60)">
        <rect x="0" y="0" width="600" height="340" rx="10" fill="#161b22" stroke="#21262d" />
        <text x="18" y="26" class="bold-text" font-size="13.5" fill="#fb7185">📈 DAG Execution Pipeline &amp; Shuffle Boundary</text>
        <text x="18" y="46" class="body-text" font-size="11.5">How Spark translates user queries into optimized physical stages:</text>

        <!-- Stage 0 -->
        <g transform="translate(20, 65)">
          <rect x="0" y="0" width="555" height="75" rx="8" fill="#0d1117" stroke="#f43f5e" />
          <text x="14" y="24" class="bold-text" font-size="12" fill="#fb7185">Stage 0: Map / Partition Processing (Local to HDFS)</text>
          <text x="14" y="44" class="body-text" font-size="11">• Read HDFS CSV/Parquet blocks via <tspan class="mono" fill="#79c0ff">hdfs://localhost:9000/...</tspan></text>
          <text x="14" y="62" class="body-text" font-size="11">• Row filtering, projection &amp; map-side combine in RAM</text>
        </g>

        <!-- Shuffle Arrow -->
        <g transform="translate(270, 150)">
          <text x="30" y="15" class="mono" font-size="11" fill="#f59e0b" text-anchor="middle">⬇️ Shuffle-Sort Boundary (Hash Partitioning)</text>
        </g>

        <!-- Stage 1 -->
        <g transform="translate(20, 180)">
          <rect x="0" y="0" width="555" height="75" rx="8" fill="#0d1117" stroke="#f43f5e" />
          <text x="14" y="24" class="bold-text" font-size="12" fill="#fb7185">Stage 1: Reduce / Aggregation &amp; Parquet Write</text>
          <text x="14" y="44" class="body-text" font-size="11">• Group-by reductions (<tspan class="mono" fill="#fb7185">groupBy("Department").agg(...)</tspan>)</text>
          <text x="14" y="62" class="body-text" font-size="11">• Write Snappy-compressed Parquet directly to HDFS</text>
        </g>

        <g transform="translate(20, 270)">
          <rect x="0" y="0" width="555" height="50" rx="6" fill="#0d1117" stroke="#21262d" />
          <text x="14" y="22" class="mono" font-size="11" fill="#34d399">spark.eventLog.dir = hdfs://hadoop:9000/spark-logs</text>
          <text x="14" y="38" class="body-text" font-size="10.5">Event logs streamed to HDFS and surfaced on Spark History Server (:18080)</text>
        </g>
      </g>

      <!-- Spark Worker Executors Box -->
      <g transform="translate(640, 60)">
        <rect x="0" y="0" width="610" height="340" rx="10" fill="#161b22" stroke="#21262d" />
        <text x="18" y="26" class="bold-text" font-size="13.5" fill="#fb7185">🔨 Spark Worker &amp; JVM Executor Architecture</text>
        <text x="18" y="46" class="body-text" font-size="11.5">Standalone worker container connected via <tspan class="mono" fill="#fb7185">spark://spark-master:7077</tspan>:</text>

        <g transform="translate(18, 65)">
          <rect x="0" y="0" width="280" height="150" rx="8" fill="#0d1117" stroke="#21262d" />
          <text x="14" y="24" class="bold-text" font-size="12" fill="#fb7185">🔨 Executor Slot #1</text>
          <text x="14" y="46" class="body-text" font-size="11">• 1 CPU Core allocated</text>
          <text x="14" y="66" class="body-text" font-size="11">• 512MB Execution RAM</text>
          <text x="14" y="86" class="body-text" font-size="11">• In-Memory DataFrame blocks</text>
          <text x="14" y="110" class="mono" font-size="10.5" fill="#3fb950">Status: Active Executor</text>
        </g>

        <g transform="translate(315, 65)">
          <rect x="0" y="0" width="280" height="150" rx="8" fill="#0d1117" stroke="#21262d" />
          <text x="14" y="24" class="bold-text" font-size="12" fill="#fb7185">🔨 Executor Slot #2</text>
          <text x="14" y="46" class="body-text" font-size="11">• 1 CPU Core allocated</text>
          <text x="14" y="66" class="body-text" font-size="11">• 512MB Execution RAM</text>
          <text x="14" y="86" class="body-text" font-size="11">• In-Memory DataFrame blocks</text>
          <text x="14" y="110" class="mono" font-size="10.5" fill="#3fb950">Status: Active Executor</text>
        </g>

        <g transform="translate(18, 230)">
          <rect x="0" y="0" width="577" height="90" rx="8" fill="#0d1117" stroke="#f43f5e" stroke-dasharray="4,4" />
          <text x="16" y="24" class="bold-text" font-size="12" fill="#fb7185">⚡ High-Performance Kryo Serialization &amp; Off-Heap Memory:</text>
          <text x="16" y="46" class="body-text" font-size="11.5">Tuned with <tspan class="mono" fill="#fb7185">org.apache.spark.serializer.KryoSerializer</tspan> for 10x faster serialization.</text>
          <text x="16" y="66" class="body-text" font-size="11.5">Zero Java GC overhead during large departmental aggregations.</text>
        </g>
      </g>
    </g>

    <!-- YARN Architecture & Scheduling -->
    <g transform="translate(25, 500)">
      <rect x="0" y="0" width="1270" height="570" rx="14" fill="#0d1117" stroke="#2ea043" stroke-width="1.3" />
      
      <rect x="20" y="16" width="340" height="28" rx="6" fill="#238636" />
      <text x="190" y="35" class="heading" font-size="14" fill="#ffffff" text-anchor="middle">⚙️ YARN Resource Negotiation &amp; Scheduling</text>
      
      <text x="380" y="35" class="bold-text" font-size="13" fill="#8b949e">Dynamic 3072MB Memory Pool • CapacityScheduler • NodeManager Slot Isolation</text>

      <!-- YARN Memory Allocation Chart -->
      <g transform="translate(20, 60)">
        <rect x="0" y="0" width="1230" height="220" rx="10" fill="#161b22" stroke="#21262d" />
        <text x="18" y="28" class="bold-text" font-size="13.5" fill="#3fb950">🧠 YARN Dynamic Container Scheduling Pool (3,072 MB Total)</text>
        <text x="18" y="48" class="body-text" font-size="11.5">512MB slot isolation ensures zero memory deadlocks across multi-tenant workloads:</text>

        <!-- Slots Visualizer -->
        <g transform="translate(20, 65)">
          <g transform="translate(0, 0)">
            <rect x="0" y="0" width="190" height="135" rx="8" fill="#0d1117" stroke="#2ea043" />
            <text x="14" y="24" class="bold-text" font-size="12" fill="#3fb950">Container 1 (512 MB)</text>
            <text x="14" y="46" class="body-text" font-size="11">AppMaster</text>
            <text x="14" y="66" class="body-text" font-size="11">YARN LifeCycle Mgr</text>
            <text x="14" y="112" class="mono" font-size="10" fill="#7ee787">Alloc: 512 MB</text>
          </g>

          <g transform="translate(205, 0)">
            <rect x="0" y="0" width="190" height="135" rx="8" fill="#0d1117" stroke="#2ea043" />
            <text x="14" y="24" class="bold-text" font-size="12" fill="#3fb950">Container 2 (512 MB)</text>
            <text x="14" y="46" class="body-text" font-size="11">Map Task 1</text>
            <text x="14" y="66" class="body-text" font-size="11">HDFS Data Locality</text>
            <text x="14" y="112" class="mono" font-size="10" fill="#7ee787">Alloc: 512 MB</text>
          </g>

          <g transform="translate(410, 0)">
            <rect x="0" y="0" width="190" height="135" rx="8" fill="#0d1117" stroke="#2ea043" />
            <text x="14" y="24" class="bold-text" font-size="12" fill="#3fb950">Container 3 (512 MB)</text>
            <text x="14" y="46" class="body-text" font-size="11">Map Task 2</text>
            <text x="14" y="66" class="body-text" font-size="11">HDFS Data Locality</text>
            <text x="14" y="112" class="mono" font-size="10" fill="#7ee787">Alloc: 512 MB</text>
          </g>

          <g transform="translate(615, 0)">
            <rect x="0" y="0" width="190" height="135" rx="8" fill="#0d1117" stroke="#2ea043" />
            <text x="14" y="24" class="bold-text" font-size="12" fill="#3fb950">Container 4 (512 MB)</text>
            <text x="14" y="46" class="body-text" font-size="11">Reduce Task</text>
            <text x="14" y="66" class="body-text" font-size="11">Shuffle Aggregator</text>
            <text x="14" y="112" class="mono" font-size="10" fill="#7ee787">Alloc: 512 MB</text>
          </g>

          <g transform="translate(820, 0)">
            <rect x="0" y="0" width="370" height="135" rx="8" fill="#0d1117" stroke="#30363d" stroke-dasharray="4,4" />
            <text x="14" y="24" class="bold-text" font-size="12" fill="#8b949e">Available Headroom (1,024 MB)</text>
            <text x="14" y="46" class="body-text" font-size="11">• Reserved for incoming dynamic jobs</text>
            <text x="14" y="66" class="body-text" font-size="11">• Spark on YARN executor allocation</text>
            <text x="14" y="112" class="mono" font-size="10" fill="#8b949e">yarn.nodemanager.resource.memory-mb</text>
          </g>
        </g>
      </g>

      <!-- Stability Details -->
      <g transform="translate(20, 300)">
        <rect x="0" y="0" width="1230" height="245" rx="10" fill="#161b22" stroke="#21262d" />
        <text x="18" y="28" class="bold-text" font-size="13.5" fill="#ffffff">🧠 NodeManager Enterprise Virtual Memory &amp; GC Stability Tuning:</text>
        
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
          Verified Execution: Spark Monte Carlo Pi + PySpark HDFS Parquet ETL + MapReduce Pi Benchmark running in harmony.
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
    <text x="420" y="35" class="body-text" font-size="13">Zero Data Loss: Named Docker Volumes, Spark Event Logs &amp; Google Cloud Storage Buckets (gs://)</text>

    <g transform="translate(30, 60)">
      <g transform="translate(0, 0)">
        <rect x="0" y="0" width="510" height="95" rx="10" fill="#0d1117" stroke="#30363d" stroke-width="1.2" />
        <text x="18" y="28" class="bold-text" font-size="13" fill="#58a6ff">📁 NameNode Volume (fsimage + edits)</text>
        <text x="18" y="50" class="mono" font-size="11.5" fill="#79c0ff">hadoop_namenode_data ➔ /usr/local/hadoop/hdfs/namenode</text>
        <text x="18" y="74" class="body-text" font-size="11.5">Filesystem namespace tree, fsimage snapshots, and edits WAL</text>
      </g>

      <g transform="translate(535, 0)">
        <rect x="0" y="0" width="510" height="95" rx="10" fill="#0d1117" stroke="#30363d" stroke-width="1.2" />
        <text x="18" y="28" class="bold-text" font-size="13" fill="#58a6ff">🧱 DataNode Volume (Raw 128MB Blocks)</text>
        <text x="18" y="50" class="mono" font-size="11.5" fill="#79c0ff">hadoop_datanode_data ➔ /usr/local/hadoop/hdfs/datanode</text>
        <text x="18" y="74" class="body-text" font-size="11.5">Stores actual raw 128MB replicated data blocks (blk_* and blk_*.meta checksums)</text>
      </g>

      <g transform="translate(1070, 0)">
        <rect x="0" y="0" width="510" height="95" rx="10" fill="#0d1117" stroke="#30363d" stroke-width="1.2" />
        <text x="18" y="28" class="bold-text" font-size="13" fill="#fb7185">⚡ Spark Events Volume</text>
        <text x="18" y="50" class="mono" font-size="11.5" fill="#fb7185">spark_event_logs_data ➔ /spark-logs &bull; :18080</text>
        <text x="18" y="74" class="body-text" font-size="11.5">Spark DAG event logs picked up by Spark History Server</text>
      </g>

      <g transform="translate(1605, 0)">
        <rect x="0" y="0" width="510" height="95" rx="10" fill="#0d1117" stroke="#30363d" stroke-width="1.2" />
        <text x="18" y="28" class="bold-text" font-size="13" fill="#3fb950">📦 Temporary Workspace &amp; GCS Staging</text>
        <text x="18" y="50" class="mono" font-size="11.5" fill="#7ee787">hadoop_tmp_data ➔ /app/hadoop/tmp | gs://bucket/staging</text>
        <text x="18" y="74" class="body-text" font-size="11.5">MapReduce shuffle spills, intermediate buffers, and cloud staging</text>
      </g>

      <g transform="translate(2140, 0)">
        <rect x="0" y="0" width="510" height="95" rx="10" fill="#0d1117" stroke="#30363d" stroke-width="1.2" />
        <text x="18" y="28" class="bold-text" font-size="13" fill="#bc8cff">📜 Jupyter Notebooks &amp; Logs</text>
        <text x="18" y="50" class="mono" font-size="11.5" fill="#d2a8ff">jupyter_notebooks_data ➔ /home/jovyan/work</text>
        <text x="18" y="74" class="body-text" font-size="11.5">Durable PySpark notebooks, ETL pipelines, and dataset artifacts</text>
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
      • <tspan fill="#58a6ff">HDFS Block Size:</tspan> 128 MB | <tspan fill="#fb7185">Spark Standalone:</tspan> 7077/8080 | <tspan fill="#f59e0b">Hive Warehouse:</tspan> /user/hive/warehouse | <tspan fill="#34d399">Control Hub:</tspan> Port 3030 | <tspan fill="#7ee787">JupyterLab:</tspan> Port 8888 | <tspan fill="#bc8cff">YARN Pool:</tspan> 3072MB | <tspan fill="#38bdf8">Cloud:</tspan> Dataproc 2.1
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
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--hide-scrollbars",
        f"--screenshot={png_file_1}",
        "--window-size=2800,1920",
        f"file:///{svg_file_1.as_posix()}"
    ]
    try:
        subprocess.run(cmd_1, check=True)
        print(f"[OK] Rendered {png_file_1} ({os.path.getsize(png_file_1)} bytes)")
    except Exception as e:
        print(f"[WARN] Error rendering PNG 1: {e}")

    cmd_2 = [
        msedge_path,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--hide-scrollbars",
        f"--screenshot={png_file_2}",
        "--window-size=2800,1920",
        f"file:///{svg_file_2.as_posix()}"
    ]
    try:
        subprocess.run(cmd_2, check=True)
        print(f"[OK] Rendered {png_file_2} ({os.path.getsize(png_file_2)} bytes)")
    except Exception as e:
        print(f"[WARN] Error rendering PNG 2: {e}")
else:
    print("[WARN] msedge.exe not found at default path, skipping PNG rendering")

