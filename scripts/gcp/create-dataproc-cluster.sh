#!/usr/bin/env bash
# ==============================================================================
# Apache Hadoop on Google Cloud Dataproc - Cluster Provisioner
#
# Creates a production-ready, auto-terminating Apache Hadoop & Spark cluster
# on Google Cloud Platform with Component Gateway (Web UIs) and GCS integration.
# ==============================================================================

set -euo pipefail

# Configuration with sensible defaults
PROJECT_ID="${GCP_PROJECT_ID:-$(gcloud config get-value project 2>/dev/null || echo '')}"
REGION="${GCP_REGION:-us-central1}"
ZONE="${GCP_ZONE:-us-central1-a}"
CLUSTER_NAME="${DATAPROC_CLUSTER_NAME:-hadoop-cluster-lab}"
BUCKET_NAME="${GCP_BUCKET_NAME:-${PROJECT_ID}-hadoop-lab-data}"
MASTER_MACHINE_TYPE="${GCP_MASTER_TYPE:-e2-standard-4}"
WORKER_MACHINE_TYPE="${GCP_WORKER_TYPE:-e2-standard-4}"
NUM_WORKERS="${GCP_NUM_WORKERS:-2}"
NUM_PREEMPTIBLE="${GCP_NUM_PREEMPTIBLE:-1}"
MAX_IDLE="${GCP_MAX_IDLE:-30m}" # Automatically delete if idle for 30 minutes

echo "=========================================================="
echo "🐘 Google Cloud Dataproc - Hadoop Cluster Provisioner"
echo "=========================================================="
echo "Project ID:            ${PROJECT_ID}"
echo "Region / Zone:         ${REGION} / ${ZONE}"
echo "Cluster Name:          ${CLUSTER_NAME}"
echo "Staging GCS Bucket:    gs://${BUCKET_NAME}"
echo "Master Node:           1x ${MASTER_MACHINE_TYPE} (50GB SSD)"
echo "Worker Nodes:          ${NUM_WORKERS}x ${WORKER_MACHINE_TYPE} (50GB SSD)"
echo "Preemptible Workers:   ${NUM_PREEMPTIBLE}x (Cost-optimized spot instances)"
echo "Auto-Delete on Idle:   ${MAX_IDLE}"
echo "=========================================================="

if [ -z "${PROJECT_ID}" ]; then
    echo "❌ ERROR: GCP Project ID is not set. Please run 'gcloud config set project <PROJECT_ID>' or export GCP_PROJECT_ID."
    exit 1
fi

# 1. Enable required GCP APIs
echo "==> [1/4] Enabling required Google Cloud APIs..."
gcloud services enable dataproc.googleapis.com storage.googleapis.com compute.googleapis.com --project="${PROJECT_ID}"

# 2. Ensure Google Cloud Storage Bucket exists
echo "==> [2/4] Verifying Cloud Storage bucket (gs://${BUCKET_NAME})..."
if ! gcloud storage buckets describe "gs://${BUCKET_NAME}" --project="${PROJECT_ID}" >/dev/null 2>&1; then
    echo "Creating Cloud Storage bucket gs://${BUCKET_NAME} in region ${REGION}..."
    gcloud storage buckets create "gs://${BUCKET_NAME}" \
        --project="${PROJECT_ID}" \
        --location="${REGION}" \
        --uniform-bucket-level-access
    echo "✅ GCS Bucket created."
else
    echo "✅ GCS Bucket already exists."
fi

# 3. Create Dataproc Cluster
echo "==> [3/4] Creating Dataproc Cluster '${CLUSTER_NAME}'..."
gcloud dataproc clusters create "${CLUSTER_NAME}" \
    --project="${PROJECT_ID}" \
    --region="${REGION}" \
    --zone="${ZONE}" \
    --single-node="${GCP_SINGLE_NODE:-false}" \
    --master-machine-type="${MASTER_MACHINE_TYPE}" \
    --master-boot-disk-type="pd-ssd" \
    --master-boot-disk-size="50GB" \
    --num-workers="${NUM_WORKERS}" \
    --worker-machine-type="${WORKER_MACHINE_TYPE}" \
    --worker-boot-disk-type="pd-ssd" \
    --worker-boot-disk-size="50GB" \
    --num-secondary-workers="${NUM_PREEMPTIBLE}" \
    --secondary-worker-type="spot" \
    --bucket="${BUCKET_NAME}" \
    --image-version="2.1-debian11" \
    --enable-component-gateway \
    --optional-components=JUPYTER,DOCKER \
    --max-idle="${MAX_IDLE}" \
    --labels="environment=lab,orchestrator=docker-hadoop-suite"

echo "=========================================================="
echo "✅ Dataproc Hadoop Cluster '${CLUSTER_NAME}' is LIVE!"
echo "=========================================================="
echo "Web Interfaces available via Component Gateway in Google Cloud Console:"
echo "  - YARN ResourceManager UI"
echo "  - HDFS NameNode UI"
echo "  - MapReduce JobHistory UI"
echo "  - Jupyter Notebooks"
echo ""
echo "Access via Console:"
echo "  https://console.cloud.google.com/dataproc/clusters/${REGION}/${CLUSTER_NAME}/view?project=${PROJECT_ID}"
echo ""
echo "Submit sample jobs using:"
echo "  bash scripts/gcp/submit-mapreduce-job.sh"
echo "=========================================================="
