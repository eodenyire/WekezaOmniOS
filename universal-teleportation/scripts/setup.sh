#!/bin/bash

# WekezaOmniOS: Phase 1 Environment Setup
# Automates system dependencies, directory structure, and Python requirements.

echo "🚀 Starting WekezaOmniOS Phase 1 setup..."

# 1. System-Level Dependencies
# CRIU is the backbone of our teleportation engine.
echo "[Setup] Updating system and installing CRIU..."
sudo apt update
sudo apt install -y criu python3-pip

# 2. Directory Architecture
# Establishing the workspace for logs, snapshots, and PIDs.
echo "[Setup] Creating internal directories..."
mkdir -p logs snapshots temp demo

# 3. Python Environment
# Installing the core SDKs needed for the API and Process Inspection.
echo "[Setup] Installing Python dependencies..."
pip install psutil fastapi uvicorn

# If a requirements file exists, we'll sync that as well.
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

# 4. Permissions Check
# Ensuring our scripts have the right execution bits.
chmod +x scripts/*.sh

echo "--------------------------------------------------"
echo "✅ Setup complete. WekezaOmniOS is ready for boot."
echo "💡 PRO-TIP: Ensure your kernel supports CRIU by running 'criu check'."
echo "--------------------------------------------------"
