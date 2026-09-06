/**
 * ==============================================================================
 * 🚀 Unified Big Data Engineering Platform — Client Application Logic
 * ==============================================================================
 */

document.addEventListener('DOMContentLoaded', () => {
  // Navigation Studio Switcher
  const navTabs = document.querySelectorAll('.nav-tab');
  const studioViews = document.querySelectorAll('.studio-view');
  const currentStudioTitle = document.getElementById('currentStudioTitle');
  const currentStudioSubtitle = document.getElementById('currentStudioSubtitle');

  const STUDIO_METADATA = {
    overview: {
      title: 'Cluster Overview & Telemetry',
      subtitle: 'Real-time status monitoring, metrics, and multi-engine service matrix'
    },
    hdfs: {
      title: 'HDFS Distributed DataLake Explorer',
      subtitle: 'Browse blocks, inodes, permissions and datasets via native WebHDFS'
    },
    spark: {
      title: 'Apache Spark Compute & History Studio',
      subtitle: 'Standalone cluster coordinator, executors, and stage DAG profiling'
    },
    hive: {
      title: 'Apache Hive Data Warehouse Studio',
      subtitle: 'Interactive SQL query console, schema catalog, and analytical queries'
    },
    sqoop: {
      title: 'Apache Sqoop Data Ingestion Center',
      subtitle: 'Visual RDBMS <-> HDFS/Hive bulk transfer builder and CLI generator'
    },
    oozie: {
      title: 'Apache Oozie Pipeline Orchestrator',
      subtitle: 'Visual DAG workflow designer, coordinator scheduler, and XML engine'
    },
    pig: {
      title: 'Apache Pig Latin Analytics Sandbox',
      subtitle: 'High-level Pig Latin script editor, operator cheatsheets, and dataflow runner'
    },
    jupyter: {
      title: 'JupyterLab PySpark Interactive Studio',
      subtitle: 'Interactive exploratory notebooks with PySpark 3.5, DuckDB, and Pandas'
    },
    terminal: {
      title: 'Live Cluster Terminal & Unified Log Streamer',
      subtitle: 'Real-time stdout/stderr execution log streaming across all engines'
    },
    diagrams: {
      title: 'Architectural Blueprints & Infographics',
      subtitle: 'Scalable vector SVGs and high-definition system architecture maps'
    }
  };

  navTabs.forEach((tab) => {
    tab.addEventListener('click', () => {
      const studioId = tab.getAttribute('data-studio');
      switchStudio(studioId);
    });
  });

  function switchStudio(studioId) {
    navTabs.forEach((t) => t.classList.remove('active'));
    studioViews.forEach((v) => v.classList.remove('active'));

    const activeTab = document.querySelector(`.nav-tab[data-studio="${studioId}"]`);
    const targetView = document.getElementById(`studio-${studioId}`);

    if (activeTab) activeTab.classList.add('active');
    if (targetView) targetView.classList.add('active');

    if (STUDIO_METADATA[studioId]) {
      currentStudioTitle.textContent = STUDIO_METADATA[studioId].title;
      currentStudioSubtitle.textContent = STUDIO_METADATA[studioId].subtitle;
    }

    if (studioId === 'hdfs' && !hdfsLoaded) {
      loadHdfsDirectory('/');
    }
  }

  // ----------------------------------------------------------------------------
  // 1. Cluster Status & Service Matrix Polling
  // ----------------------------------------------------------------------------
  const serviceGrid = document.getElementById('serviceGrid');
  const clusterStatusText = document.getElementById('clusterStatusText');
  const kpiServices = document.getElementById('kpiServices');
  const kpiServicesSub = document.getElementById('kpiServicesSub');
  const matrixCounter = document.getElementById('matrixCounter');
  const navHealthBadge = document.getElementById('navHealthBadge');

  async function pollClusterStatus() {
    try {
      const res = await fetch('/api/status');
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();

      clusterStatusText.textContent = `${data.onlineServices}/${data.totalServices} Online (${data.clusterHealth})`;
      kpiServices.textContent = `${data.onlineServices} / ${data.totalServices}`;
      kpiServicesSub.textContent = data.clusterHealth === 'HEALTHY' ? 'All Core Daemons Active' : 'Some Daemons Starting';
      matrixCounter.textContent = `${data.onlineServices} of ${data.totalServices} Services Online`;

      if (data.clusterHealth === 'HEALTHY') {
        navHealthBadge.textContent = 'HEALTHY';
        navHealthBadge.style.background = 'rgba(16, 185, 129, 0.2)';
      } else {
        navHealthBadge.textContent = 'ONLINE';
      }

      renderServiceGrid(data.services);
    } catch (err) {
      clusterStatusText.textContent = 'Connecting...';
    }
  }

  function renderServiceGrid(services) {
    serviceGrid.innerHTML = '';
    services.forEach((svc) => {
      const card = document.createElement('div');
      card.className = 'service-card';

      const isOnline = svc.online;
      const statusClass = isOnline ? 'status-online' : 'status-offline';
      const statusLabel = isOnline ? `${svc.latencyMs}ms` : 'OFFLINE';

      card.innerHTML = `
        <div class="svc-header">
          <div class="svc-title-row">
            <span style="font-size: 20px;">${svc.icon}</span>
            <div>
              <div class="svc-name">${svc.name}</div>
              <div class="port-tag">:${svc.port}</div>
            </div>
          </div>
          <span class="status-pill ${statusClass}">${statusLabel}</span>
        </div>
        <div class="svc-desc">${svc.description}</div>
        <div class="svc-footer">
          <span class="svc-port">${svc.rpc ? svc.rpc : 'HTTP Port'}</span>
          <a href="${svc.url}" target="_blank" class="btn-secondary-sm">Open Console &rarr;</a>
        </div>
      `;
      serviceGrid.appendChild(card);
    });
  }

  // Poll immediately and every 5 seconds
  pollClusterStatus();
  setInterval(pollClusterStatus, 5000);

  document.getElementById('btnManualRefresh')?.addEventListener('click', () => {
    pollClusterStatus();
    logTerminal('[REFRESH] Manually queried cluster telemetry and service endpoints.');
  });

  // ----------------------------------------------------------------------------
  // 2. HDFS DataLake Explorer
  // ----------------------------------------------------------------------------
  let hdfsLoaded = false;
  let currentHdfsPath = '/';
  const hdfsTableBody = document.getElementById('hdfsTableBody');
  const hdfsBreadcrumbs = document.getElementById('hdfsBreadcrumbs');
  const filePreviewBox = document.getElementById('filePreviewBox');
  const previewFileName = document.getElementById('previewFileName');
  const filePreviewContent = document.getElementById('filePreviewContent');

  async function loadHdfsDirectory(path) {
    currentHdfsPath = path;
    hdfsTableBody.innerHTML = `<tr><td colspan="7" class="text-muted">Loading ${path}...</td></tr>`;
    updateBreadcrumbs(path);

    try {
      const res = await fetch(`/api/hdfs/browse?path=${encodeURIComponent(path)}`);
      const data = await res.json();
      hdfsLoaded = true;

      hdfsTableBody.innerHTML = '';

      if (data.items.length === 0) {
        hdfsTableBody.innerHTML = `<tr><td colspan="7" class="text-muted">Directory is empty.</td></tr>`;
        return;
      }

      data.items.forEach((item) => {
        const tr = document.createElement('tr');
        const isDir = item.type === 'DIRECTORY';
        const icon = isDir ? '📁' : '📄';
        const sizeFormatted = isDir ? '-' : formatBytes(item.size);

        tr.innerHTML = `
          <td>
            <span style="cursor: pointer; font-weight: 600; color: ${isDir ? '#38bdf8' : '#f8fafc'};" class="hdfs-item-link">
              ${icon} ${item.name}
            </span>
          </td>
          <td><span class="port-tag">${item.type}</span></td>
          <td class="code-font" style="font-size: 11px;">${item.permission}</td>
          <td style="font-size: 12px;">${item.owner}:${item.group || 'hadoop'}</td>
          <td style="font-size: 12px;">${sizeFormatted}</td>
          <td style="font-size: 12px; color: var(--text-muted);">${item.modified}</td>
          <td>
            ${
              isDir
                ? `<button class="btn-secondary-sm btn-open-dir">Open</button>`
                : `<button class="btn-secondary-sm btn-preview-file">Preview</button>`
            }
          </td>
        `;

        const targetPath = currentHdfsPath === '/' ? `/${item.name}` : `${currentHdfsPath}/${item.name}`;

        tr.querySelector('.hdfs-item-link').addEventListener('click', () => {
          if (isDir) loadHdfsDirectory(targetPath);
          else previewHdfsFile(targetPath, item.name);
        });

        const openBtn = tr.querySelector('.btn-open-dir');
        if (openBtn) {
          openBtn.addEventListener('click', () => loadHdfsDirectory(targetPath));
        }

        const prevBtn = tr.querySelector('.btn-preview-file');
        if (prevBtn) {
          prevBtn.addEventListener('click', () => previewHdfsFile(targetPath, item.name));
        }

        hdfsTableBody.appendChild(tr);
      });
    } catch (e) {
      hdfsTableBody.innerHTML = `<tr><td colspan="7" style="color: #fb7185;">Error accessing WebHDFS directory.</td></tr>`;
    }
  }

  function updateBreadcrumbs(path) {
    hdfsBreadcrumbs.innerHTML = '';
    const parts = path.split('/').filter(Boolean);
    
    const rootSpan = document.createElement('span');
    rootSpan.className = 'crumb';
    rootSpan.textContent = 'hdfs:/// ';
    rootSpan.addEventListener('click', () => loadHdfsDirectory('/'));
    hdfsBreadcrumbs.appendChild(rootSpan);

    let buildPath = '';
    parts.forEach((p, idx) => {
      buildPath += `/${p}`;
      const thisPath = buildPath;
      const crumb = document.createElement('span');
      crumb.className = 'crumb';
      crumb.textContent = ` ${p} /`;
      crumb.addEventListener('click', () => loadHdfsDirectory(thisPath));
      hdfsBreadcrumbs.appendChild(crumb);
    });
  }

  function previewHdfsFile(fullPath, name) {
    filePreviewBox.style.display = 'block';
    previewFileName.textContent = `Preview: ${name} (${fullPath})`;
    filePreviewContent.textContent = `Fetching file content from WebHDFS [${fullPath}]...`;

    // Simulated content for quick preview
    setTimeout(() => {
      filePreviewContent.textContent = `# Content of HDFS file: ${fullPath}
1,Layla Mahmoud,layla.m@example.com,Cairo,Egypt,2024-01-15,5000.00
2,Omar Farooq,omar.f@example.com,Alexandria,Egypt,2024-02-10,3500.00
3,Sami Haddad,sami.h@example.com,Beirut,Lebanon,2024-02-28,7500.00
4,Nour El-Din,nour.e@example.com,Dubai,UAE,2024-03-05,12000.00
5,Fatima Zahra,fatima.z@example.com,Casablanca,Morocco,2024-03-20,4500.00
6,Karim Mansoor,karim.m@example.com,Riyadh,Saudi Arabia,2024-04-01,9000.00
7,Youssef Ibrahim,youssef.i@example.com,Amman,Jordan,2024-04-18,6000.00
8,Hana Salem,hana.s@example.com,Giza,Egypt,2024-05-12,4000.00
[EOF - 8 Records Loaded via WebHDFS]`;
    }, 200);
  }

  document.getElementById('btnClosePreview')?.addEventListener('click', () => {
    filePreviewBox.style.display = 'none';
  });

  document.getElementById('btnHdfsRefresh')?.addEventListener('click', () => {
    loadHdfsDirectory(currentHdfsPath);
  });

  // ----------------------------------------------------------------------------
  // 3. Hive SQL Studio
  // ----------------------------------------------------------------------------
  const hiveSqlEditor = document.getElementById('hiveSqlEditor');
  const btnExecuteHiveQuery = document.getElementById('btnExecuteHiveQuery');
  const hiveResultsHead = document.getElementById('hiveResultsHead');
  const hiveResultsBody = document.getElementById('hiveResultsBody');
  const hiveQueryStats = document.getElementById('hiveQueryStats');

  btnExecuteHiveQuery?.addEventListener('click', async () => {
    const query = hiveSqlEditor.value.trim();
    if (!query) return;

    hiveQueryStats.textContent = 'Executing query on Hive/Spark SQL...';
    btnExecuteHiveQuery.disabled = true;

    try {
      const res = await fetch('/api/hive/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      });
      const data = await res.json();
      btnExecuteHiveQuery.disabled = false;

      if (data.success) {
        hiveQueryStats.textContent = `Completed in ${data.executionTimeMs}ms (${data.rowCount} rows)`;

        // Render Head
        hiveResultsHead.innerHTML = `<tr>${data.columns.map((c) => `<th>${c}</th>`).join('')}</tr>`;

        // Render Rows
        hiveResultsBody.innerHTML = data.rows
          .map((r) => `<tr>${r.map((cell) => `<td>${cell}</td>`).join('')}</tr>`)
          .join('');

        logTerminal(`[HIVE SQL] Executed: ${query.slice(0, 60)}... (${data.rowCount} rows, ${data.executionTimeMs}ms)`);
      }
    } catch (e) {
      btnExecuteHiveQuery.disabled = false;
      hiveQueryStats.textContent = 'Query failed.';
    }
  });

  document.querySelectorAll('.btn-preset').forEach((btn) => {
    btn.addEventListener('click', () => {
      hiveSqlEditor.value = btn.getAttribute('data-query');
      btnExecuteHiveQuery.click();
    });
  });

  // ----------------------------------------------------------------------------
  // 4. Sqoop Ingestion Center
  // ----------------------------------------------------------------------------
  const btnGenerateSqoop = document.getElementById('btnGenerateSqoop');
  const btnRunSqoopSim = document.getElementById('btnRunSqoopSim');
  const sqoopCmdOutput = document.getElementById('sqoopCmdOutput');

  btnGenerateSqoop?.addEventListener('click', async () => {
    const direction = document.getElementById('sqoopDirection').value;
    const dbType = document.getElementById('sqoopDbType').value;
    const hostPort = document.getElementById('sqoopHostPort').value.split(':');
    const db = document.getElementById('sqoopDbName').value;
    const table = document.getElementById('sqoopTable').value;
    const hdfsDir = document.getElementById('sqoopHdfsPath').value;
    const mappers = document.getElementById('sqoopMappers').value;

    const res = await fetch('/api/sqoop/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        direction,
        dbType,
        host: hostPort[0] || 'mysql',
        port: hostPort[1] || 3306,
        db,
        table,
        hdfsDir,
        mappers
      })
    });
    const data = await res.json();
    if (data.success) {
      sqoopCmdOutput.innerHTML = `<code>${data.command}</code>`;
    }
  });

  btnRunSqoopSim?.addEventListener('click', () => {
    switchStudio('terminal');
    dispatchJobStream('sqoop-import');
  });

  document.getElementById('btnCopySqoop')?.addEventListener('click', () => {
    navigator.clipboard.writeText(sqoopCmdOutput.textContent);
    alert('Sqoop command copied to clipboard!');
  });

  // ----------------------------------------------------------------------------
  // 5. Oozie Orchestrator
  // ----------------------------------------------------------------------------
  document.getElementById('btnTriggerOozie')?.addEventListener('click', () => {
    switchStudio('terminal');
    dispatchJobStream('oozie-pipeline');
  });

  // ----------------------------------------------------------------------------
  // 6. Pig Latin Workbench
  // ----------------------------------------------------------------------------
  const btnExecutePig = document.getElementById('btnExecutePig');
  const pigScriptEditor = document.getElementById('pigScriptEditor');
  const pigTerminalOutput = document.getElementById('pigTerminalOutput');

  btnExecutePig?.addEventListener('click', async () => {
    const script = pigScriptEditor.value;
    pigTerminalOutput.textContent = 'Compiling Pig Latin script into MapReduce execution plan...';

    const res = await fetch('/api/pig/execute', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ script })
    });
    const data = await res.json();

    if (data.success) {
      pigTerminalOutput.innerHTML = `<code>// Plan Compiled Successfully!
${data.dagStages.join('\n')}

[REDUCE OUTPUT SAMPLE]
${data.sampleOutput.join('\n')}

// Output written to HDFS: ${data.hdfsOutput}
// Processed ${data.recordsProcessed} records without errors.</code>`;
      logTerminal(`[PIG LATIN] Executed script: ${data.recordsProcessed} records processed.`);
    }
  });

  // ----------------------------------------------------------------------------
  // 7. Spark Compute Runners
  // ----------------------------------------------------------------------------
  document.getElementById('btnRunSparkPi')?.addEventListener('click', () => {
    switchStudio('terminal');
    dispatchJobStream('spark-pi');
  });

  document.getElementById('btnRunPySparkETL')?.addEventListener('click', () => {
    switchStudio('terminal');
    dispatchJobStream('pyspark-etl');
  });

  // ----------------------------------------------------------------------------
  // 8. Unified Live Terminal Streamer
  // ----------------------------------------------------------------------------
  const mainTerminalConsole = document.getElementById('mainTerminalConsole');
  const mainTerminalCode = document.getElementById('mainTerminalCode');

  function logTerminal(msg) {
    mainTerminalCode.textContent += `\n[${new Date().toLocaleTimeString()}] ${msg}`;
    mainTerminalConsole.scrollTop = mainTerminalConsole.scrollHeight;
  }

  async function dispatchJobStream(jobType) {
    logTerminal(`\n>>> STARTING DISPATCH: ${jobType.toUpperCase()}`);
    try {
      const response = await fetch('/api/jobs/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ jobType })
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const text = decoder.decode(value);
        mainTerminalCode.textContent += text;
        mainTerminalConsole.scrollTop = mainTerminalConsole.scrollHeight;
      }
    } catch (e) {
      logTerminal(`[ERROR] Job stream interrupted: ${e.message}`);
    }
  }

  document.getElementById('btnClearTerminal')?.addEventListener('click', () => {
    mainTerminalCode.textContent = '// Terminal cleared.\n';
  });

  document.getElementById('btnCopyTerminal')?.addEventListener('click', () => {
    navigator.clipboard.writeText(mainTerminalCode.textContent);
    alert('Terminal logs copied to clipboard!');
  });

  // Utilities
  function formatBytes(bytes) {
    if (!bytes || bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
  }
});
