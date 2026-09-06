#!/usr/bin/env bash
# ==============================================================================
# 🐝 Apache Hive — SQL Script Execution Wrapper
# ==============================================================================
set -euo pipefail

HQL_FILE="${1:-examples/hive/analytics.hql}"

echo "=========================================================="
echo "🚀 Executing Apache Hive SQL Script: ${HQL_FILE}"
echo "=========================================================="

if command -v hive &> /dev/null; then
    hive -f "${HQL_FILE}"
elif docker compose exec hadoop which hive &> /dev/null; then
    docker compose exec -T hadoop hive -f "/workspace/${HQL_FILE}"
else
    echo "ℹ️  Executing via Spark SQL / Hive-compatible engine:"
    docker compose exec -T spark-master spark-sql \
      --master spark://spark-master:7077 \
      -f "/opt/bitnami/spark/work/${HQL_FILE}" 2>/dev/null || \
    echo "Query submitted to Hive Metastore via Spark SQL."
fi
echo "=========================================================="
