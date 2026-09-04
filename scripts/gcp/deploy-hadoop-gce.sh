#!/usr/bin/env bash
# ==============================================================================
# Apache Hadoop Docker Cluster on Google Compute Engine (GCE)
#
# Launches an Ubuntu VM with Docker, clones the repository, configures firewall
# rules, and starts the containerized Hadoop cluster on Google Cloud.
# ==============================================================================

set -euo pipefail

PROJECT_ID="${GCP_PROJECT_ID:-$(gcloud config get-value project 2>/dev/null || echo '')}"
ZONE="${GCP_ZONE:-us-central1-a}"
INSTANCE_NAME="${GCE_INSTANCE_NAME:-hadoop-docker-vm}"
MACHINE_TYPE="${GCE_MACHINE_TYPE:-e2-standard-4}" # 4 vCPUs, 16 GB RAM
FIREWALL_RULE="allow-hadoop-web-consoles"

echo "=========================================================="
echo "🐳 Google Compute Engine (GCE) - Docker Hadoop Deployer"
echo "=========================================================="
echo "Project ID:       ${PROJECT_ID}"
echo "Zone:             ${ZONE}"
echo "Instance:         ${INSTANCE_NAME}"
echo "Machine Type:     ${MACHINE_TYPE}"
echo "=========================================================="

if [ -z "${PROJECT_ID}" ]; then
    echo "❌ ERROR: GCP Project ID is not set."
    exit 1
fi

# 1. Create VPC Firewall Rule for Hadoop Web Interfaces
echo "==> [1/3] Creating/Verifying VPC Firewall Rule..."
if ! gcloud compute firewall-rules describe "${FIREWALL_RULE}" --project="${PROJECT_ID}" >/dev/null 2>&1; then
    gcloud compute firewall-rules create "${FIREWALL_RULE}" \
        --project="${PROJECT_ID}" \
        --direction=INGRESS \
        --priority=1000 \
        --network=default \
        --action=ALLOW \
        --rules=tcp:9870,tcp:9864,tcp:8088,tcp:8042,tcp:19888,tcp:9000,tcp:22222 \
        --source-ranges=0.0.0.0/0 \
        --target-tags=hadoop-node \
        --description="Allow inbound traffic to Apache Hadoop Web Consoles and endpoints"
    echo "✅ Firewall rule created."
else
    echo "✅ Firewall rule already exists."
fi

# 2. Launch Compute Engine VM with Docker startup script
echo "==> [2/3] Provisioning GCE VM instance '${INSTANCE_NAME}'..."
gcloud compute instances create "${INSTANCE_NAME}" \
    --project="${PROJECT_ID}" \
    --zone="${ZONE}" \
    --machine-type="${MACHINE_TYPE}" \
    --image-family="ubuntu-2204-lts" \
    --image-project="ubuntu-os-cloud" \
    --boot-disk-size="60GB" \
    --boot-disk-type="pd-balanced" \
    --tags=hadoop-node \
    --metadata=startup-script='#!/bin/bash
set -e
# Install Docker and Compose
apt-get update
apt-get install -y ca-certificates curl gnupg git
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg
echo "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Clone docker-hadoop repository
cd /opt
if [ ! -d "/opt/docker-hadoop" ]; then
    git clone https://github.com/Sohila-Khaled-Abbas/docker-hadoop.git
fi
cd /opt/docker-hadoop
docker compose up -d
'

echo "==> [3/3] Fetching VM External IP Address..."
EXTERNAL_IP=$(gcloud compute instances describe "${INSTANCE_NAME}" \
    --project="${PROJECT_ID}" \
    --zone="${ZONE}" \
    --format='get(networkInterfaces[0].accessConfigs[0].natIP)')

echo "=========================================================="
echo "✅ GCE Hadoop Docker VM deployed successfully!"
echo "Instance External IP:  ${EXTERNAL_IP}"
echo ""
echo "Web Interfaces (allow ~2 minutes for Docker image build and startup):"
echo "  - HDFS NameNode:          http://${EXTERNAL_IP}:9870"
echo "  - YARN ResourceManager:   http://${EXTERNAL_IP}:8088"
echo "  - JobHistory Server:      http://${EXTERNAL_IP}:19888"
echo ""
echo "SSH into your instance:"
echo "  gcloud compute ssh ${INSTANCE_NAME} --zone=${ZONE}"
echo "=========================================================="
