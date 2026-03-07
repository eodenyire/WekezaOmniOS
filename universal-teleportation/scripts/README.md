# 🛠️ WekezaOmniOS: Utility Scripts

This folder contains the automation layer for Phase 1 of the Universal Application Teleportation (UAT) engine. These scripts are designed to standardize the environment so that every teleportation test starts from a "known good" state.

## 🎯 Purpose

* **Environment Bootstrapping:** Automatically creates the necessary folder hierarchy (`logs/`, `snapshots/`, `temp/`).
* **Dependency Management:** Ensures all Python modules (like `fastapi`, `uvicorn`, and `psutil`) are installed.
* **Orchestration:** Launches background demo processes and tracks their PIDs for easy teleportation targeting.

## 📜 Available Scripts

### 1. `setup.sh`

Prepares the local machine for engine execution.

```bash
# Usage:
bash scripts/setup.sh

```

* **Actions:** Installs `requirements.txt`, clears old logs, and creates the snapshot storage directories.

### 2. `run_demo.sh`

Spins up the target applications we intend to teleport.

```bash
# Usage:
bash scripts/run_demo.sh

```

* **Actions:** Launches `demo_app.py` (a simple counter) and `demo_server.py` (a mock banking API) in the background. It saves their PIDs to the `temp/` folder for the **Capture Manager** to use.

---

### 📄 `setup.sh`

```bash
#!/bin/bash

# WekezaOmniOS Environment Setup Script
# Standardizes the Phase 1 workspace.

echo "🚀 Starting WekezaOmniOS Phase 1 setup..."

# 1. Create the required directory structure for the engine
echo "[Setup] Creating internal directories..."
mkdir -p logs snapshots temp snapshot/process_1821

# 2. Install dependencies
# Note: Ensure you are in your virtual environment before running this.
if [ -f "requirements.txt" ]; then
    echo "[Setup] Installing Python dependencies..."
    pip install -r requirements.txt
else
    echo "[Setup] WARNING: requirements.txt not found. Skipping dependency install."
fi

# 3. Set permissions (Critical for CRIU operations later)
chmod +x scripts/*.sh

echo "✅ Setup complete. The engine is ready for Phase 1 testing."

```

---

### 📄 `run_demo.sh`

```bash
#!/bin/bash

# WekezaOmniOS Demo Launcher
# Backgrounds the demo apps and captures PIDs for teleportation.

echo "🧊 Launching WekezaOmniOS Demo Applications..."

# 1. Start the simple Counter App
python3 demo/demo_app.py &
PID_APP=$!
echo "[Demo] Started demo_app.py with PID: $PID_APP"
echo $PID_APP > temp/demo_app.pid

# 2. Start the Mock Banking Server
python3 demo/demo_server.py &
PID_SERVER=$!
echo "[Demo] Started demo_server.py with PID: $PID_SERVER"
echo $PID_SERVER > temp/demo_server.pid

echo "--------------------------------------------------"
echo "✅ Apps are running in the background."
echo "💡 To teleport, use the PIDs found in the 'temp/' folder."
echo "--------------------------------------------------"

```

---

### 🛠️ Key Integration Details

* **The PID Handover:** By saving the PIDs to `temp/demo_app.pid`, you’ve created a bridge between the **OS layer** and the **WekezaOmniOS API**. Your CLI can now read that file and automatically know which process to target without you having to run `ps -ef | grep python` every time.
* **Idempotency:** The `mkdir -p` command ensures that running `setup.sh` multiple times won't cause errors—it simply ensures the folders exist.
* **Standardization:** This setup ensures that if another engineer at **Wekeza Bank** clones your repo, they can get the entire engine running in two commands.

---

### ✅ Scripts Module: COMPLETE

We have officially automated the "boring stuff." You now have a clean way to boot your environment and launch your targets.
