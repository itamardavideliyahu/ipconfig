#!/bin/bash
###############################################################
#  EC2 Bootstrap Script — runs once on first launch
#  1. Installs Docker
#  2. Clones the GitHub repo
#  3. Builds and starts the IDPS container
###############################################################

set -euo pipefail
exec > /var/log/user-data.log 2>&1   # log everything

echo "=== [1/5] System update ==="
apt-get update -y
apt-get upgrade -y

echo "=== [2/5] Install Docker ==="
curl -fsSL https://get.docker.com | sh
systemctl enable docker
systemctl start docker
usermod -aG docker ubuntu

echo "=== [3/5] Clone repository ==="
git clone ${github_repo} /opt/idps-app
cd /opt/idps-app/cyber/idps-docker

echo "=== [4/5] Build Docker image ==="
docker build -t ${docker_image}:latest .

echo "=== [5/5] Start container ==="
docker run -d \
  --name idps-sim \
  --restart unless-stopped \
  -p ${app_port}:8080 \
  ${docker_image}:latest

echo "=== DONE — App running on port ${app_port} ==="
echo "Health check: curl http://localhost:${app_port}/health"
curl --retry 10 --retry-delay 3 --silent http://localhost:${app_port}/health || true
