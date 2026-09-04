#!/usr/bin/env bash
# ==============================================================================
# Apache Hadoop on Google Cloud Dataproc - Teardown & Cost Management
#
# Gracefully deletes an ephemeral Dataproc cluster to prevent cloud charges.
# ==============================================================================

set -euo pipefail

PROJECT_ID="${GCP_PROJECT_ID:-$(gcloud config get-value project 2>/dev/null || echo '')}"
REGION="${GCP_REGION:-us-central1}"
CLUSTER_NAME="${DATAPROC_CLUSTER_NAME:-hadoop-cluster-lab}"

echo "=========================================================="
echo "🧹 Google Cloud Dataproc - Cluster Teardown"
echo "=========================================================="
echo "Project ID:       ${PROJECT_ID}"
echo "Region:           ${REGION}"
echo "Cluster Name:     ${CLUSTER_NAME}"
echo "=========================================================="

if [ -z "${PROJECT_ID}" ]; then
    echo "❌ ERROR: GCP Project ID is not set."
    exit 1
fi

echo "==> Checking if cluster '${CLUSTER_NAME}' exists..."
if gcloud dataproc clusters describe "${CLUSTER_NAME}" --project="${PROJECT_ID}" --region="${REGION}" >/dev/null 2>&1; then
    echo "Deleting cluster '${CLUSTER_NAME}'..."
    gcloud dataproc clusters delete "${CLUSTER_NAME}" \
        --project="${PROJECT_ID}" \
        --region="${REGION}" \
        --quiet
    echo "✅ Dataproc cluster successfully deleted. Compute billing stopped."
else
    echo "ℹ️ Cluster '${CLUSTER_NAME}' does not exist or has already been deleted."
fi

echo "=========================================================="
echo "Note: Your output and datasets remain safe in Cloud Storage (gs://)."
echo "=========================================================="
