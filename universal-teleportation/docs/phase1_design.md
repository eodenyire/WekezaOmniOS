### 🏗️ Phase 1: The "Local Loop" Prototype

Phase 1 focuses on the **Single-Node Lifecycle**. We are building the plumbing that allows a process to be frozen, packaged, and reanimated within the same Linux environment.

## 🎯 Primary Goals

* **Proof of Concept (PoC):** Demonstrate a running Python "Counter" app being captured at `N` and resumed at `N+1`.
* **Infrastructure Mocking:** Create the CLI and API interfaces that will eventually control a global cluster, but pointed at `localhost`.
* **Artifact Standardization:** Finalize the `.tar.gz` snapshot format that will become the "Universal Cargo" for the engine.
* **Observability (Rule 5):** Implement the logging and telemetry required to audit a teleportation event.

---

## 🔄 Integration Flow: The Teleportation Pipeline

The engine operates as a sequential pipeline where each module hands off a standardized artifact to the next.

1. **Trigger:** User issues a `teleport capture <PID>` via CLI.
2. **Freeze:** `state-capture` uses **CRIU** to dump the process memory to a temporary directory.
3. **Package:** `snapshot-engine` aggregates the memory dump, `env.json`, and `metadata.json` into a compressed archive.
4. **Handoff:** The archive is moved to the `./snapshots` repository.
5. **Reanimate:** `state-reconstruction` extracts the archive and signals the kernel to resume the process.

---

## 🛠️ Critical Design Decisions

| Decision | Implementation | Justification |
| --- | --- | --- |
| **Node Scope** | **Local Only** | Removes network latency/security variables to focus on memory integrity. |
| **Storage Path** | `./snapshots/` | Standardized location ensures **Rule 6 (Portability)** testing is easy. |
| **Core Engine** | **CRIU** | Industry-standard for Checkpoint/Restore in Userspace on Linux. |
| **Interface** | **Python SDK** | Allows for rapid prototyping and easy integration with `psutil` and `subprocess`. |

---

## 🚦 Phase 1 Success Metrics (The "Green Light")

* **State Persistence:** Does the process retain its variable values after restoration?
* **File Handle Continuity:** Does the process keep its connection to open logs or temp files?
* **Telemetry Accuracy:** Does `logs/teleport.log` correctly show the start and end timestamps?

---

### ✅ Documentation: STRATEGY LOCKED

We have the goals, the flow, and the rules. This document is the "North Star" for the next few development sprints.
