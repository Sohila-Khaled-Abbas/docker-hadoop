#!/usr/bin/env bash
# ==============================================================================
# ☕ Apache Sqoop — Code Generation for Java Data Models
# ==============================================================================
set -euo pipefail

DB_HOST="${DB_HOST:-mysql}"
DB_PORT="${DB_PORT:-3306}"
DB_NAME="${DB_NAME:-retail_db}"
DB_USER="${DB_USER:-root}"
DB_PASS="${DB_PASS:-H@doop2022}"
OUT_DIR="${OUT_DIR:-/tmp/sqoop-codegen}"

mkdir -p "${OUT_DIR}"

echo "=========================================================="
echo "🚀 Generating Java Serialization POJO for Table: customers"
echo "=========================================================="

sqoop codegen \
  --connect "jdbc:mysql://${DB_HOST}:${DB_PORT}/${DB_NAME}?useSSL=false&allowPublicKeyRetrieval=true" \
  --username "${DB_USER}" \
  --password "${DB_PASS}" \
  --table customers \
  --outdir "${OUT_DIR}" \
  --class-name CustomerRecord

echo "=========================================================="
echo "✅ Java Model Generated at ${OUT_DIR}/CustomerRecord.java"
echo "=========================================================="
