Perfect! Now we are in the **`docs/` folder**, which is critical for **Phase 1** because documentation ensures **any contributor or developer quickly understands the system architecture, snapshot format, and design of the teleportation engine**.

Even though Phase 1 is local and mostly mock logic, **well-structured docs** set the standard for **world-class open-source engineering**.

---

# 📁 Folder: `docs/`

Purpose:

* Document **system architecture**, **teleportation design**, and **snapshot formats**
* Serve as **reference for future developers**
* Explain **Phase 1 design decisions**
* Prepare for **Phase 2 distributed teleportation**

---

# 📄 `README.md`

```md
# WekezaOmniOS Documentation

This folder contains the documentation for the Universal Application Teleportation (UAT) engine.

## Contents

- `architecture.md` — Overall system architecture
- `phase1_design.md` — Phase 1 design notes and implementation plan
- `snapshot_format.md` — Format of process snapshots
- `teleportation-overview.md` — Overview of teleportation concept
- `teleportation_architecture.md` — Detailed architecture of teleportation engine

## Purpose

- Ensure **future contributors understand the system quickly**
- Serve as **reference for engineers integrating with Phase 1**
- Standardize documentation style for **later phases**
```

---

# 📄 `architecture.md`

* Diagrams and descriptions of **how all modules interact**
* Example content:

```md
# WekezaOmniOS System Architecture

## Module Overview

```

CLI / API
↓
Cluster Module
↓
State Capture → Snapshot Engine → State Reconstruction
↓
Demo / Nodes

```

## Module Responsibilities

- **CLI**: Developer-facing commands
- **API**: Control plane for programmatic access
- **Cluster**: Node management
- **State Capture**: Process checkpointing
- **Snapshot Engine**: Snapshot packaging and metadata
- **State Reconstruction**: Restore processes
- **Demo**: Test workloads
```

---

# 📄 `phase1_design.md`

* Document **Phase 1 goals and integration**:

```md
# Phase 1 Design — Universal Teleportation

## Goals

- Build **local teleportation prototype**
- Implement **CLI and API mocks**
- Test with **demo applications**
- Design **configs and logging**

## Integration Flow

```

CLI / API → state-capture → snapshot-engine → state-reconstruction → demo apps

```

## Key Decisions

- Phase 1 uses **local nodes only**
- Snapshots stored in `./snapshots`
- Logs stored in `./logs`
- CRIU as default checkpoint engine
```

---

# 📄 `snapshot_format.md`

* Define **how snapshots are stored**:

````md
# Snapshot Format

## Files

- `memory.dump` — memory pages
- `filesystem.tar` — process files
- `env.json` — environment variables
- `metadata.json` — process metadata

## metadata.json Example

```json
{
  "process_id": 1921,
  "os": "ubuntu",
  "architecture": "x86_64",
  "created_at": "2026-03-07T18:20:00",
  "snapshot_name": "snapshot_1921"
}
````

## Purpose

* Ensure **portable process state**
* Enable **restoration across nodes**

````

---

# 📄 `teleportation-overview.md`

- High-level explanation of teleportation:

```md
# Teleportation Overview

Universal Application Teleportation (UAT) allows **moving a running process from one environment to another** while preserving its state.

## Features

- Capture memory, CPU, open files, and environment
- Create snapshots
- Restore processes locally
- Future: distributed node teleportation
````

---

# 📄 `teleportation_architecture.md`

* Detailed breakdown for **engine internals**:

```md
# Teleportation Engine Architecture

## Modules

- `state-capture/`
- `snapshot-engine/`
- `state-reconstruction/`
- `cluster/`
- `cli/`
- `api/`

## Flow

```

1. CLI/API request → state-capture.capture_manager()
2. snapshot-engine.snapshot_builder()
3. state-reconstruction.restore_manager()
4. Logging to ./logs

```

## Future Integration

- Remote nodes
- Cloud teleportation
- Multiple snapshot engines
```

---

# 📂 Final `docs/` Folder Structure

```text
docs/
    README.md
    architecture.md
    phase1_design.md
    snapshot_format.md
    teleportation-overview.md
    teleportation_architecture.md
```

---

✅ **Next Step:**

After docs, the next critical folder is:

```text
logs/
```

This folder **collects all logs from capture, snapshot, and restore actions**, which is vital for **debugging and verifying teleportation**.

We can design `logs/README.md` and the log conventions next.

Do you want me to do that?
