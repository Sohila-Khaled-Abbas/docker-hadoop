#!/usr/bin/env bash
# ==============================================================================
# 🔄 Apache Sqoop — Import MySQL Table into HDFS & Hive
# ==============================================================================
set -euo pipefail

DB_HOST="${DB_HOST:-mysql}"
DB_PORT="${DB_PORT:-3306}"
DB_NAME="${DB_NAME:-retail_db}"
DB_USER="${DB_USER:-root}"
DB_PASS="${DB_PASS:-H@doop2022}"
HDFS_TARGET_DIR="${HDFS_TARGET_DIR:-/data/sqoop/customers}"

echo "=========================================================="
echo "🚀 Starting Apache Sqoop Import: MySQL -> HDFS & Hive"
echo "   Database: jdbc:mysql://${DB_HOST}:${DB_PORT}/${DB_NAME}"
echo "   Target HDFS: ${HDFS_TARGET_DIR}"
echo "=========================================================="

# 1. Ensure target HDFS directory does not exist or allow overwrite
echo "📁 Pre-cleaning target HDFS directory..."
hdfs dfs -rm -r -f "${HDFS_TARGET_DIR}" || true

# 2. Execute Sqoop Import
sqoop import \
  --connect "jdbc:mysql://${DB_HOST}:${DB_PORT}/${DB_NAME}?useSSL=false&allowPublicKeyRetrieval=true" \
  --username "${DB_USER}" \
  --password "${DB_PASS}" \
  --table customers \
  --target-dir "${HDFS_TARGET_DIR}" \
  --split-by customer_id \
  --num-mappers 2 \
  --fields-terminated-by ',' \
  --lines-terminated-by '\n' \
  --delete-target-dir \
  --hive-import \
  --hive-table retail_db.customers \
  --create-hive-table

echo "=========================================================="
echo "✅ Sqoop Import Successfully Completed!"
echo "   Verifying HDFS output directory:"
hdfs dfs -ls "${HDFS_TARGET_DIR}"
echo "   Previewing imported records:"
hdfs dfs -cat "${HDFS_TARGET_DIR}/part-m-00000" | head -n 5
echo "=========================================================="
