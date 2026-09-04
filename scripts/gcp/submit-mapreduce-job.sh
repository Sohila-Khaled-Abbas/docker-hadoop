#!/usr/bin/env bash
# ==============================================================================
# Apache Hadoop on Google Cloud Dataproc - Job Submitter
#
# Submits Python Streaming WordCount and Java MapReduce jobs to Dataproc
# using Google Cloud Storage (gs://) for decoupled distributed storage.
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

PROJECT_ID="${GCP_PROJECT_ID:-$(gcloud config get-value project 2>/dev/null || echo '')}"
REGION="${GCP_REGION:-us-central1}"
CLUSTER_NAME="${DATAPROC_CLUSTER_NAME:-hadoop-cluster-lab}"
BUCKET_NAME="${GCP_BUCKET_NAME:-${PROJECT_ID}-hadoop-lab-data}"
JOB_TYPE="${1:-streaming}" # "streaming", "java", or "pi"

echo "=========================================================="
echo "⚡ Google Cloud Dataproc - MapReduce Job Execution"
echo "=========================================================="
echo "Project ID:       ${PROJECT_ID}"
echo "Region:           ${REGION}"
echo "Cluster Name:     ${CLUSTER_NAME}"
echo "Storage Bucket:   gs://${BUCKET_NAME}"
echo "Job Type:         ${JOB_TYPE}"
echo "=========================================================="

if [ -z "${PROJECT_ID}" ]; then
    echo "❌ ERROR: GCP Project ID is not set."
    exit 1
fi

TIMESTAMP="$(date +%s)"

case "${JOB_TYPE}" in
    "streaming")
        echo "==> [1/4] Uploading sample dataset & Python scripts to Cloud Storage..."
        gcloud storage cp "${REPO_ROOT}/datasets/wordcount-sample.txt" "gs://${BUCKET_NAME}/mapreduce/input/wordcount-sample.txt"
        gcloud storage cp "${REPO_ROOT}/examples/mapreduce-python/mapper.py" "gs://${BUCKET_NAME}/mapreduce/code/mapper.py"
        gcloud storage cp "${REPO_ROOT}/examples/mapreduce-python/reducer.py" "gs://${BUCKET_NAME}/mapreduce/code/reducer.py"

        OUTPUT_DIR="gs://${BUCKET_NAME}/mapreduce/output-python-${TIMESTAMP}"
        echo "==> [2/4] Target Output Path: ${OUTPUT_DIR}"

        echo "==> [3/4] Submitting Hadoop Streaming Job to Dataproc..."
        gcloud dataproc jobs submit hadoop \
            --project="${PROJECT_ID}" \
            --region="${REGION}" \
            --cluster="${CLUSTER_NAME}" \
            --files="gs://${BUCKET_NAME}/mapreduce/code/mapper.py,gs://${BUCKET_NAME}/mapreduce/code/reducer.py" \
            --jar="file:///usr/lib/hadoop-mapreduce/hadoop-streaming.jar" \
            -- \
            -files="gs://${BUCKET_NAME}/mapreduce/code/mapper.py,gs://${BUCKET_NAME}/mapreduce/code/reducer.py" \
            -mapper="python3 mapper.py" \
            -reducer="python3 reducer.py" \
            -input="gs://${BUCKET_NAME}/mapreduce/input/wordcount-sample.txt" \
            -output="${OUTPUT_DIR}"

        echo "==> [4/4] Output Results from Cloud Storage:"
        echo "----------------------------------------------------------"
        gcloud storage cat "${OUTPUT_DIR}/part*" | head -n 30
        echo "----------------------------------------------------------"
        echo "✅ Python Streaming Job completed successfully on Google Cloud Dataproc!"
        ;;

    "java"|"pi")
        echo "==> Submitting Standard MapReduce Pi Job to Dataproc..."
        gcloud dataproc jobs submit hadoop \
            --project="${PROJECT_ID}" \
            --region="${REGION}" \
            --cluster="${CLUSTER_NAME}" \
            --jar="file:///usr/lib/hadoop-mapreduce/hadoop-mapreduce-examples.jar" \
            -- \
            pi 16 1000
        echo "✅ Native MapReduce Job completed successfully on Google Cloud Dataproc!"
        ;;

    *)
        echo "❌ Unknown JOB_TYPE: ${JOB_TYPE}. Usage: $0 [streaming|java|pi]"
        exit 1
        ;;
esac
