# 📦 WekezaOmniOS: Snapshot Engine

The **Snapshot Engine** is the industrial packaging arm of the Universal Application Teleportation (UAT) platform. It is responsible for converting raw system states into highly portable, compressed, and self-describing archives.

### 🎯 Purpose

* **Portability:** Ensures snapshots can be moved between directories, servers, or cloud nodes without losing integrity.
* **Standardization:** Defines the uniform structure for process state across different operating systems.
* **Efficiency:** Uses high-compression formats (GZIP) to minimize bandwidth during network-based teleportation.

---

## 📁 Module Breakdown

| File | Responsibility |
| --- | --- |
| **`snapshot_builder.py`** | The "Packer." Compresses the captured directory into a `.tar.gz` archive. |
| **`snapshot_metadata.py`** | The "Registrar." Generates and manages the `metadata.json` for every snapshot. |
| **`snapshot_reader.py`** | The "Inspector." Validates the archive and reads metadata before restoration. |

---

## 🏗️ Snapshot Format (Phase 1)

Every snapshot produced by this engine follows a strict structural contract to ensure the **Restore Manager** can reanimate it:

* **`memory.dump`** — The raw binary representation of the process memory.
* **`filesystem.tar`** — An archive of any local files the process was accessing.
* **`environment.json`** — A snapshot of the process's environment variables.
* **`metadata.json`** — The "Passport" (PID, Timestamp, OS, Architecture).

---

## 🚀 Phase 1 Workflow

1. **Capture Handoff:** The `state-capture` module dumps raw data into a temporary directory.
2. **Manifest Creation:** `snapshot_metadata.py` generates the identifying JSON.
3. **Encapsulation:** `snapshot_builder.py` zips the raw data and manifest into a single `.tar.gz`.
4. **Verification:** `snapshot_reader.py` performs a "smoke test" to ensure the archive isn't corrupt.

---

## 🔗 Integration Plan

The Snapshot Engine acts as the critical bridge in the teleportation pipeline:

> **State Capture** ⮕ **Snapshot Engine** ⮕ **Transfer Layer** ⮕ **State Reconstruction**

* **Upstream:** Triggered by the CLI or UI once a process is successfully frozen.
* **Downstream:** Feeds the `transfer-layer` (Phase 2) or directly into `state-reconstruction` (Phase 1).

---

### ✅ Snapshot Engine: MISSION COMPLETE

With the storage logic, reader, and builder finalized, we now have a "Portable Soul" for our processes.
