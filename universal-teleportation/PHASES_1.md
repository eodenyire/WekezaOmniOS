Perfect. Let’s design **Phase 1 so you can literally start coding today**.
Phase 1 is **Local Process Checkpointing Prototype** — proving that **a running process can be paused, saved, and restored**.

We will structure it like a **serious systems project**, not a small script.

---

# 🚀 Phase 1 — GitHub Repository Structure

Main repository:

```bash
WekezaOmniOS/
```

Inside:

```bash
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
```

This keeps the **project clean and scalable**.

---

# 📂 Core Folder: universal-teleportation

```bash
universal-teleportation/
```

Inside:

```bash
universal-teleportation/

state-capture/
snapshot-engine/
state-reconstruction/
cli/
api/
configs/
```

---

# 1️⃣ state-capture

Responsible for **capturing process state**.

```bash
state-capture/

capture_manager.py
process_inspector.py
criu_wrapper.py
utils.py
```

### capture_manager.py

Main logic controlling checkpoint.

Example:

```python
class CaptureManager:

    def capture_process(self, pid):
        print(f"Capturing process {pid}")
```

---

### process_inspector.py

Gets process information.

Example:

```python
import psutil

def get_process_info(pid):
    process = psutil.Process(pid)
    return {
        "name": process.name(),
        "status": process.status(),
        "memory": process.memory_info().rss
    }
```

---

### criu_wrapper.py

Interface to **CRIU commands**.

Uses subprocess.

Example:

```python
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
```

---

# 2️⃣ snapshot-engine

Packages captured state.

```bash
snapshot-engine/

snapshot_builder.py
snapshot_reader.py
snapshot_metadata.py
```

---

### snapshot_builder.py

Creates portable snapshot.

Example:

```python
import tarfile

def build_snapshot(snapshot_dir, output_file):

    with tarfile.open(output_file, "w:gz") as tar:
        tar.add(snapshot_dir)
```

Output:

```bash
snapshots/process_1821_snapshot.tar.gz
```

---

### snapshot_metadata.py

Stores metadata.

Example:

```json
{
  "process_id": 1821,
  "timestamp": "2026-03-07T18:20:00",
  "os": "ubuntu",
  "memory_size": "120MB"
}
```

---

# 3️⃣ state-reconstruction

Restores process.

```bash
state-reconstruction/

restore_manager.py
criu_restore.py
environment_loader.py
```

---

### restore_manager.py

Main restore logic.

Example:

```python
def restore_process(snapshot_dir):

    print("Restoring process from snapshot")
```

---

### criu_restore.py

Wrapper around CRIU restore.

Example:

```python
import subprocess

def restore(directory):

    cmd = [
        "criu",
        "restore",
        "-D", directory,
        "--shell-job"
    ]

    subprocess.run(cmd)
```

---

# 4️⃣ CLI Interface

Developers interact through CLI first.

```bash
cli/

teleport.py
commands.py
```

---

### teleport.py

Main entry point.

Example usage:

```bash
python teleport.py capture 1921
```

Code:

```python
import sys

def main():

    command = sys.argv[1]

    if command == "capture":
        pid = sys.argv[2]
        print(f"Capturing {pid}")
```

---

Example commands:

```bash
teleport capture 1921
teleport snapshot 1921
teleport restore snapshot_1921
```

---

# 5️⃣ API Layer

Later this will integrate with **WekezaOmniOS UI**.

```bash
api/

server.py
routes.py
models.py
```

Use **FastAPI**.

Example endpoint:

```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/capture")
def capture(pid: int):
    return {"status": "capturing"}
```

---

# 6️⃣ Configs

```bash
configs/

system.yaml
criu_config.yaml
teleportation.yaml
```

Example:

```yaml
snapshot_directory: ./snapshots
log_directory: ./logs
```

---

# 7️⃣ Tests

```bash
tests/

test_capture.py
test_snapshot.py
test_restore.py
```

Use **pytest**.

---

# 8️⃣ Scripts

Automate setup.

```bash
scripts/

setup.sh
run_demo.sh
```

---

### setup.sh

```bash
sudo apt update
sudo apt install criu python3-pip
pip install psutil fastapi uvicorn
```

---

### run_demo.sh

Demo workflow.

```bash
python demo_app.py &

PID=$!

python cli/teleport.py capture $PID
```

---

# 📄 Example Demo App

Create:

```bash
demo_app.py
```

Example:

```python
import time

while True:
    print("WekezaOmniOS Demo Running")
    time.sleep(2)
```

Then test teleportation.

---

# 📊 Phase 1 Success Criteria

Phase 1 is successful if you can:

✔ Start a process
✔ Capture its state
✔ Package snapshot
✔ Restore process

Flow:

```
Start App
   ↓
Capture PID
   ↓
Create Snapshot
   ↓
Restore Process
```

---

# 🌍 Why Phase 1 Matters

If Phase 1 works, you already demonstrate **deep systems engineering**.

This is related to techniques used in:

* Docker
* Kubernetes
* CRIU

---

# ⭐ Next Step After This

Once Phase 1 works, the **next powerful milestone** is:

### Phase 2 — Teleport Containers Between Machines

That’s when **WekezaOmniOS starts looking like magic**.

---

If you'd like, I can also show you something **extremely important before you start coding**:

The **engineering rules used by top systems projects (Linux kernel, Docker, Kubernetes)** so that **WekezaOmniOS is structured like a world-class open-source project from day one.**
