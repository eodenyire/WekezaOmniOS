# 📜 WekezaOmniOS: Logging Module

The **Logging Module** is the source of truth for the Universal Application Teleportation (UAT) engine. In a high-integrity environment—especially for banking applications at **Wekeza Bank**—visibility isn't just a feature; it's a requirement for security and auditability.

### ⚖️ Rule 5: Everything Must Be Observable

Systems software must be transparent. Every state change, from the moment a process is "frozen" to the millisecond it "reanimates," must leave a timestamped, structured trail.

---

## 📂 Folder Structure & File Responsibilities

| Log File | Responsibility | Triggered By |
| --- | --- | --- |
| **`capture.log`** | Tracks process inspection and memory dumping. | `capture_manager.py` |
| **`restore.log`** | Records environment rehydration and process resumption. | `restore_manager.py` |
| **`teleport.log`** | The high-level "Master Log" for the full end-to-end journey. | `teleportation-api` |

---

## 📝 Logging Standards (Phase 1)

Every entry in **WekezaOmniOS** must follow the structured format:
`[TIMESTAMP] [LEVEL] [COMPONENT] [PID/ID] Message`

### Example Audit Trail:

```text
[2026-03-07 22:15:01] [INFO] [CAPTURE] [PID:1821] Freezing process 'wekeza_core'.
[2026-03-07 22:15:05] [INFO] [SNAPSHOT] [PID:1821] Generated 'process_1821.tar.gz' (120MB).
[2026-03-07 22:15:10] [INFO] [RESTORE] [PID:1821] Resuming on target node 'ubuntu-prod-01'.
[2026-03-07 22:15:12] [SUCCESS] [TELEPORT] [PID:1821] Teleportation cycle complete.

```

---

## 🛠️ Integration Plan

The logging system is woven into the engine's core logic:

1. **State Capture:** When the engine initiates a "Freeze," the `capture_manager` writes the PID and memory size to `capture.log`.
2. **Snapshot Engine:** As the "Cargo" is zipped, the archive success is noted in `teleport.log`.
3. **State Reconstruction:** When the process "thaws," the `restore_manager` logs the new execution state to `restore.log`.
4. **Monitoring:** The `monitoring/` module (Phase 2) will tail these logs to provide real-time health alerts to the **Wekeza Bank** dashboard.

---

## 🚀 Phase 2 Evolution: JSON Logging

While Phase 1 uses human-readable text files for easy CLI debugging, Phase 2 will transition to **JSON-structured logs**. This will allow you to pipe logs directly into ELK (Elasticsearch, Logstash, Kibana) or Prometheus for advanced fintech analytics.

---

### ✅ Logging Module: MISSION COMPLETE

We have established the audit trail. Now, even if a teleportation fails, we will know exactly at which millisecond the "jump" was interrupted.
