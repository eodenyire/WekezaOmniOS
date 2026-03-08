Phase 1 is Local Process Checkpointing Prototype — proving that a running process can be paused, saved, and restored.
We will structure it like a serious systems project, not a small script.
________________________________________
🚀 Phase 1 — GitHub Repository Structure
Main repository:
WekezaOmniOS/
Inside:
WekezaOmniOS/

README.md
LICENSE
.gitignore

docs/
    architecture.md
    teleportation-overview.md
    phase1-design.md

universal-teleportation/

    state-capture/
    snapshot-engine/
    state-reconstruction/

    cli/
    api/

    configs/
    logs/
    tests/

scripts/
    setup.sh
    run_demo.sh
This keeps the project clean and scalable.
________________________________________
📂 Core Folder: universal-teleportation
universal-teleportation/
Inside:
universal-teleportation/

state-capture/
snapshot-engine/
state-reconstruction/
cli/
api/
configs/
________________________________________
1️⃣ state-capture
Responsible for capturing process state.
state-capture/

capture_manager.py
process_inspector.py
criu_wrapper.py
utils.py
capture_manager.py
Main logic controlling checkpoint.
Example:
class CaptureManager:

    def capture_process(self, pid):
        print(f"Capturing process {pid}")
________________________________________
process_inspector.py
Gets process information.
Example:
import psutil

def get_process_info(pid):
    process = psutil.Process(pid)
    return {
        "name": process.name(),
        "status": process.status(),
        "memory": process.memory_info().rss
    }
________________________________________
criu_wrapper.py
Interface to CRIU commands.
Uses subprocess.
Example:
import subprocess

def checkpoint_process(pid, directory):

    cmd = [
        "criu",
        "dump",
        "-t", str(pid),
        "-D", directory,
        "--shell-job"
    ]

    subprocess.run(cmd)
________________________________________
2️⃣ snapshot-engine
Packages captured state.
snapshot-engine/

snapshot_builder.py
snapshot_reader.py
snapshot_metadata.py
________________________________________
snapshot_builder.py
Creates portable snapshot.
Example:
import tarfile

def build_snapshot(snapshot_dir, output_file):

    with tarfile.open(output_file, "w:gz") as tar:
        tar.add(snapshot_dir)
Output:
snapshots/process_1821_snapshot.tar.gz
________________________________________
snapshot_metadata.py
Stores metadata.
Example:
{
  "process_id": 1821,
  "timestamp": "2026-03-07T18:20:00",
  "os": "ubuntu",
  "memory_size": "120MB"
}
________________________________________
3️⃣ state-reconstruction
Restores process.
state-reconstruction/

restore_manager.py
criu_restore.py
environment_loader.py
________________________________________
restore_manager.py
Main restore logic.
Example:
def restore_process(snapshot_dir):

    print("Restoring process from snapshot")
________________________________________
criu_restore.py
Wrapper around CRIU restore.
Example:
import subprocess

def restore(directory):

    cmd = [
        "criu",
        "restore",
        "-D", directory,
        "--shell-job"
    ]

    subprocess.run(cmd)
________________________________________
4️⃣ CLI Interface
Developers interact through CLI first.
cli/

teleport.py
commands.py
________________________________________
teleport.py
Main entry point.
Example usage:
python teleport.py capture 1921
Code:
import sys

def main():

    command = sys.argv[1]

    if command == "capture":
        pid = sys.argv[2]
        print(f"Capturing {pid}")
________________________________________
Example commands:
teleport capture 1921
teleport snapshot 1921
teleport restore snapshot_1921
________________________________________
5️⃣ API Layer
Later this will integrate with WekezaOmniOS UI.
api/

server.py
routes.py
models.py
Use FastAPI.
Example endpoint:
from fastapi import FastAPI

app = FastAPI()

@app.post("/capture")
def capture(pid: int):
    return {"status": "capturing"}
________________________________________
6️⃣ Configs
configs/

system.yaml
criu_config.yaml
teleportation.yaml
Example:
snapshot_directory: ./snapshots
log_directory: ./logs
________________________________________
7️⃣ Tests
tests/

test_capture.py
test_snapshot.py
test_restore.py
Use pytest.
________________________________________
8️⃣ Scripts
Automate setup.
scripts/

setup.sh
run_demo.sh
________________________________________
setup.sh
sudo apt update
sudo apt install criu python3-pip
pip install psutil fastapi uvicorn
________________________________________
run_demo.sh
Demo workflow.
python demo_app.py &

PID=$!

python cli/teleport.py capture $PID
________________________________________
📄 Example Demo App
Create:
demo_app.py
Example:
import time

while True:
    print("WekezaOmniOS Demo Running")
    time.sleep(2)
Then test teleportation.
________________________________________
📊 Phase 1 Success Criteria
Phase 1 is successful if you can:
✔ Start a process
✔ Capture its state
✔ Package snapshot
✔ Restore process
Flow:
Start App
   ↓
Capture PID
   ↓
Create Snapshot
   ↓
Restore Process
________________________________________
🌍 Why Phase 1 Matters
If Phase 1 works, you already demonstrate deep systems engineering.
This is related to techniques used in:
•	Docker
•	Kubernetes
•	CRIU
________________________________________
⭐ Next Step After This
Once Phase 1 works, the next powerful milestone is:
Phase 2 — Teleport Containers Between Machines
That’s when WekezaOmniOS starts looking like magic.
________________________________________


