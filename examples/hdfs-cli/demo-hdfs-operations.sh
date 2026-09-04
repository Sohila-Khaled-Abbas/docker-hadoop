#!/usr/bin/env bash
# ==============================================================================
# Apache Hadoop HDFS CLI End-to-End Operations Demonstration
# ==============================================================================
set -euo pipefail

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

log_step() {
    echo -e "\n${CYAN}=================================================================${NC}"
    echo -e "${GREEN}==>${NC} ${YELLOW}$1${NC}"
    echo -e "${CYAN}=================================================================${NC}"
}

# Ensure HDFS binary is reachable
if ! command -v hdfs &> /dev/null; then
    echo -e "${RED}[ERROR] 'hdfs' command not found in PATH. Please run inside the Hadoop container or load environment variables.${NC}"
    exit 1
fi

DEMO_DIR="/demo/hdfs_cli"
LOCAL_TMP="/tmp/hdfs_demo_file.txt"

log_step "1. Checking HDFS SafeMode Status"
hdfs dfsadmin -safemode get

log_step "2. Creating Directory Hierarchy in HDFS: ${DEMO_DIR}"
hdfs dfs -mkdir -p "${DEMO_DIR}/input"
hdfs dfs -mkdir -p "${DEMO_DIR}/staging"
hdfs dfs -mkdir -p "${DEMO_DIR}/output"
hdfs dfs -ls -R /demo

log_step "3. Creating Local Sample Data File and Uploading to HDFS (-put)"
cat << 'EOF' > "${LOCAL_TMP}"
HDFS (Hadoop Distributed File System) Demo File
Line 1: High Fault Tolerance with Block Replication
Line 2: Rack Awareness and Pipeline Block Placement
Line 3: Streaming Data Access Pattern for Batch Computing
Line 4: SecondaryNameNode Periodic Checkpointing
EOF

hdfs dfs -put -f "${LOCAL_TMP}" "${DEMO_DIR}/input/sample.txt"
hdfs dfs -ls "${DEMO_DIR}/input"

log_step "4. Inspecting File Contents in HDFS (-cat, -tail)"
hdfs dfs -cat "${DEMO_DIR}/input/sample.txt"

log_step "5. Inspecting Block Replication & Adjusting Replication Factor (-setrep)"
echo "Current replication details:"
hdfs dfs -stat "Replication: %r | Block Size: %o bytes | Modification: %y" "${DEMO_DIR}/input/sample.txt"
echo "Setting replication factor to 1 (Single-Node cluster standard):"
hdfs dfs -setrep 1 "${DEMO_DIR}/input/sample.txt"

log_step "6. Verifying File Checksum in HDFS (-checksum)"
hdfs dfs -checksum "${DEMO_DIR}/input/sample.txt"

log_step "7. Measuring Disk Usage and Space Quotas (-du, -count)"
echo "Disk usage in bytes and human-readable units:"
hdfs dfs -du -h "${DEMO_DIR}"
echo "Directory and file count summary:"
hdfs dfs -count -q -h "${DEMO_DIR}"

log_step "8. Copying Within HDFS (-cp) and Moving Files (-mv)"
hdfs dfs -cp "${DEMO_DIR}/input/sample.txt" "${DEMO_DIR}/staging/sample_backup.txt"
hdfs dfs -ls -R "${DEMO_DIR}"

log_step "9. Downloading File Back to Local Filesystem (-get)"
DOWNLOAD_TARGET="/tmp/hdfs_downloaded_sample.txt"
rm -f "${DOWNLOAD_TARGET}"
hdfs dfs -get "${DEMO_DIR}/staging/sample_backup.txt" "${DOWNLOAD_TARGET}"
ls -lh "${DOWNLOAD_TARGET}"
head -n 2 "${DOWNLOAD_TARGET}"

log_step "10. Cleaning up Demo Directory in HDFS (-rm -r)"
hdfs dfs -rm -r -skipTrash "${DEMO_DIR}"
rm -f "${LOCAL_TMP}" "${DOWNLOAD_TARGET}"
echo -e "${GREEN}Verification: Listing /demo:${NC}"
hdfs dfs -ls /demo || echo "Demo folder cleanly removed."

echo -e "\n${GREEN}=================================================================${NC}"
echo -e "${GREEN}  ✅ HDFS CLI Interactive Operations Demo Completed Successfully!${NC}"
echo -e "${GREEN}=================================================================${NC}\n"
