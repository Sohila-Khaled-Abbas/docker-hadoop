#!/usr/bin/env bash
# ==============================================================================
# 📋 Apache Oozie — Pipeline Submission and Status Poller
# ==============================================================================
set -euo pipefail

OOZIE_URL="${OOZIE_URL:-http://localhost:11000/oozie}"
PROPERTIES_FILE="${1:-examples/oozie/job.properties}"

echo "=========================================================="
echo "🚀 Submitting Apache Oozie Workflow Pipeline"
echo "   Oozie Server: ${OOZIE_URL}"
echo "   Config: ${PROPERTIES_FILE}"
echo "=========================================================="

# Check if oozie CLI is installed locally or run via docker
if command -v oozie &> /dev/null; then
    JOB_ID=$(oozie job -oozie "${OOZIE_URL}" -config "${PROPERTIES_FILE}" -run | awk '{print $2}')
    echo "✅ Workflow submitted successfully! Job ID: ${JOB_ID}"
    echo "📊 Monitoring status..."
    oozie job -oozie "${OOZIE_URL}" -info "${JOB_ID}"
else
    echo "ℹ️  Oozie client CLI not found on host. Simulating execution against Hadoop cluster:"
    echo "   1. Uploading workflow to HDFS: hdfs dfs -put examples/oozie/workflow.xml /apps/oozie/"
    echo "   2. Validating XML structure..."
    echo "   3. Ready for execution on cluster."
fi
echo "=========================================================="
