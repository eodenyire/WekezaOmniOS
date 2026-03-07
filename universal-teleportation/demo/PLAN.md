Perfect! Now we’re in the **`demo/` folder**, which is essential for **Phase 1 testing of the Universal Teleportation engine**. This folder contains **demo applications** that we will **capture, snapshot, and restore** using the teleportation system.

Even though Phase 1 is local and simple, this folder allows developers to **verify teleportation without using production apps**.

---

# 📁 Folder: `demo/`

Purpose:

* Provide **test applications** for teleportation
* Allow Phase 1 workflow: **capture → snapshot → restore**
* Serve as examples for developers

Responsibilities:

* Run simple, observable processes
* Log activity to verify checkpointing
* Include optional “server” to simulate background processes

---

# 📄 `README.md`

````md
# WekezaOmniOS Demo Applications

This folder contains demo applications used to test the Universal Application Teleportation (UAT) engine.

## Contents

- `demo_app.py` — a simple long-running console process
- `demo_server.py` — simulates a background service for teleportation testing

## Purpose

- Provide safe, reproducible workloads
- Verify process capture, snapshot, and restore functionality
- Demonstrate teleportation engine features without production apps

## Usage

### Running demo_app.py

```bash
python demo_app.py
````

You should see output every 2 seconds:

```
WekezaOmniOS Demo Running
```

### Running demo_server.py

```bash
python demo_server.py
```

* Runs a background “server” loop
* Logs activity for verification

````

---

# 📄 `demo_app.py`

A simple **long-running Python process** for Phase 1.

```python
import time

def main():
    counter = 0
    while True:
        counter += 1
        print(f"[demo_app] WekezaOmniOS Demo Running | Tick {counter}")
        time.sleep(2)

if __name__ == "__main__":
    main()
````

* Prints ticks to **verify checkpointing**
* Easy to **capture snapshot** and restore

---

# 📄 `demo_server.py`

Simulates a **background process** with logging.

```python
import time
import logging

logging.basicConfig(
    filename="demo_server.log",
    level=logging.INFO,
    format="%(asctime)s [demo_server] %(message)s"
)

def main():
    counter = 0
    while True:
        counter += 1
        logging.info(f"Server tick {counter}")
        print(f"[demo_server] Server tick {counter}")
        time.sleep(5)

if __name__ == "__main__":
    main()
```

* Writes **to log file** for snapshot verification
* Simulates **services running in background**

---

# 🔗 Integration Plan

```text
CLI/API → capture demo_app.py / demo_server.py → snapshot → restore → verify output/log
```

* CLI commands: `teleport capture <PID>`
* Snapshot engine: stores process state
* Restore engine: resumes process with logs intact

---

# 📂 Final `demo/` Folder Structure

```text
demo/
    README.md
    demo_app.py
    demo_server.py
```

---

✅ **Next Step:**

After demo, the next **core folder is `logs/`**, which **records telemetry for capture, restore, and snapshot actions**. This folder is critical for debugging and verifying teleportation.

We can design `logs/README.md` and the logging conventions next.

Do you want me to do that?
