#!/bin/bash

# WekezaOmniOS Demo Launcher
# Backgrounds the demo apps and captures PIDs for teleportation orchestration.

echo "🧊 Launching WekezaOmniOS Demo Applications..."

# 1. Ensure the temp directory exists for PID storage
mkdir -p temp

# 2. Launch the Simple Counter App
# This app simulates a long-running computation task.
python3 demo/demo_app.py &
PID_APP=$!
echo "[Demo] Started demo_app.py with PID: $PID_APP"
echo $PID_APP > temp/demo_app.pid

# 3. Launch the Mock Banking Server
# This simulates a stateful microservice at Wekeza Bank.
python3 demo/demo_server.py &
PID_SERVER=$!
echo "[Demo] Started demo_server.py with PID: $PID_SERVER"
echo $PID_SERVER > temp/demo_server.pid

echo "--------------------------------------------------"
echo "✅ Demo applications are now active in the background."
echo "📂 PIDs saved to temp/ folder for the CLI to access."
echo "--------------------------------------------------"

# 💡 Example of how you can immediately trigger a capture for testing:
# PID=$(cat temp/demo_app.pid)
# python3 cli/teleport.py capture $PID
