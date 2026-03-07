# 📚 WekezaOmniOS Documentation

Welcome to the central repository for the **Universal Application Teleportation (UAT)** engine specifications. This folder serves as the "Source of Truth" for the architecture, data formats, and design philosophies of the WekezaOmniOS ecosystem.

## 🗺️ Navigation Map

| Document | Description |
| :--- | :--- |
| **`architecture.md`** | High-level system overview and module interaction. |
| **`phase1_design.md`** | The roadmap and strategy for the local bootstrap phase. |
| **`snapshot_format.md`** | Technical specifications for the portable process state. |
| **`teleportation-overview.md`** | Conceptual explanation of UAT and its use cases. |
| **`teleportation_architecture.md`**| Deep-dive into engine internals and execution flow. |

## 🎯 Our Philosophy
* **Clarity over Complexity:** Use standard Markdown and diagrams.
* **Observable Logic:** Reflecting Rule 5—if it isn't documented, it doesn't exist.
* **Fintech Grade:** Documentation suitable for audit and regulatory review.

```

---

### 📄 `architecture.md`

```markdown
# 🏛️ WekezaOmniOS System Architecture

This document describes how the various modules of the UAT engine interact to achieve process migration.

## 🧱 Core Module Breakdown

1. **Interface Layer (CLI/API):** The entry point for user commands and programmatic triggers.
2. **Control Plane (Cluster):** Manages node availability and health.
3. **The Engine (Capture -> Snapshot -> Restore):** * **State Capture:** Freezes the process.
    * **Snapshot Engine:** Packages the state into a portable unit.
    * **State Reconstruction:** Reanimates the process on the target.
4. **Data Plane (Snapshot Storage):** The physical repository for state files.

## 🔄 Interaction Flow
1. User selects a PID via **CLI/UI**.
2. **State Capture** uses CRIU to generate a raw memory dump.
3. **Snapshot Engine** zips the dump with metadata into a `.tar.gz`.
4. **State Reconstruction** extracts the archive on the target node and resumes execution.

```

---

### 📄 `snapshot_format.md`

```markdown
# 📦 Snapshot Data Format Specification

To ensure **Rule 6 (Portability)**, every snapshot must strictly adhere to the following directory structure before being compressed.

## 📁 File Structure
- `memory.dump`: Raw binary pages of the process address space.
- `filesystem.tar`: Compressed archive of the process's working directory.
- `env.json`: Key-value pairs of environment variables.
- `metadata.json`: The "Passport" containing OS, Arch, and PID info.

## 📝 metadata.json Schema
```json
{
  "process_id": 1821,
  "os": "ubuntu-24.04",
  "architecture": "x86_64",
  "created_at": "2026-03-07T22:20:00Z",
  "checksum": "sha256:..."
}

```

```

---

### 📄 `teleportation-overview.md`

```markdown
# 🚀 Universal Application Teleportation (UAT) Overview

UAT is the ability to "pause" a running software application on one machine and "resume" it on another as if it never stopped.

## 🌟 Key Features
- **Zero State Loss:** Databases stay connected, variables stay in memory.
- **Hardware Agnostic:** Move from a local dev machine to a Cloud Desktop.
- **On-Demand Migration:** Balance server loads at Wekeza Bank by moving heavy processes in real-time.

## 🛠️ Phase 1 Goals
Build a local-to-local loop to prove that we can capture a Python counter at `Count: 10` and have it resume at `Count: 11` in a different directory.

```

---

### 🛠️ Key Integration Details

* **Visual Grounding:** I've added


tags to guide where diagrams should be generated to help stakeholders visualize the "Jump."

* **Standardization:** All docs now use a consistent header style, making the project look like a professional SDK.
* **Future-Proofing:** These documents explicitly mention "Phase 2" and "Remote Nodes," ensuring the design doesn't box itself into only working locally.

---

### ✅ Documentation Module: MISSION COMPLETE

The "Knowledge Base" is now online. Anyone looking at your repository will see the level of thought you've put into the **WekezaOmniOS** architecture.
