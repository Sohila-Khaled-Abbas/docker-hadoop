#!/usr/bin/env bash
# ==============================================================================
# 📤 Apache Sqoop — Export Aggregated HDFS Data Back to MySQL
# ==============================================================================
set -euo pipefail

DB_HOST="${DB_HOST:-mysql}"
DB_PORT="${DB_PORT:-3306}"
DB_NAME="${DB_NAME:-retail_db}"
DB_USER="${DB_USER:-root}"
DB_PASS="${DB_PASS:-H@doop2022}"
HDFS_SOURCE_DIR="${HDFS_SOURCE_DIR:-/data/analytics/customer_summary}"

echo "=========================================================="
echo "🚀 Starting Apache Sqoop Export: HDFS -> MySQL"
echo "   Source HDFS: ${HDFS_SOURCE_DIR}"
echo "   Target Table: ${DB_NAME}.customer_analytics_summary"
echo "=========================================================="

sqoop export \
  --connect "jdbc:mysql://${DB_HOST}:${DB_PORT}/${DB_NAME}?useSSL=false&allowPublicKeyRetrieval=true" \
  --username "${DB_USER}" \
  --password "${DB_PASS}" \
  --table customer_analytics_summary \
  --export-dir "${HDFS_SOURCE_DIR}" \
  --input-fields-terminated-by ',' \
  --input-lines-terminated-by '\n' \
  --update-key country \
  --update-mode allowinsert \
  --num-mappers 2

echo "=========================================================="
echo "✅ Sqoop Export Successfully Finished!"
echo "=========================================================="
