# 📦 WekezaOmniOS: Snapshot Storage

The `snapshot/` directory is the physical storage layer for the **Universal Application Teleportation (UAT)** engine. This folder acts as the "frozen state" repository where processes are held in suspended animation between capture and reconstruction.

### 📜 Rule 6: Snapshots Must Be Portable

To achieve true teleportation, a snapshot must never be tethered to a specific machine's hardware ID or local path. This folder enforces a standardized, machine-agnostic format that allows for cross-node and cross-OS execution.

---

## 📂 Standardized Snapshot Structure

Every process "teleported" by WekezaOmniOS is stored in its own subdirectory using the following schema:

| File | Content Description | Purpose |
| --- | --- | --- |
| `metadata.json` | Process ID, OS version, Architecture, Timestamp | Inventory & Validation |
| `memory.dump` | Raw binary dump of the process memory pages | State Restoration |
| `filesystem.tar` | Compressed archive of the process's local files | Data Continuity |
| `env.json` | Key-value pairs of environment variables | Context Rehydration |

---

## 📝 Metadata Specification (`metadata.json`)

The metadata file is the "passport" of the process. It is checked by the `RestoreManager` before reanimation to ensure compatibility with the target host.

```json
{
    "process_id": 1821,
    "os": "ubuntu",
    "architecture": "x86_64",
    "status": "frozen",
    "memory_size_bytes": 1048576,
    "created_at": "2026-03-07T18:20:00Z",
    "checksum": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
}

```

---

## 🔗 Integration Logic

The snapshot folder is the central handoff point in the UAT lifecycle:

1. **Ingress:** The `snapshot-engine` collects raw data from `state-capture` and organizes it here.
2. **Validation:** The `monitoring` module watches this folder to verify snapshot integrity.
3. **Egress:** The `state-reconstruction` module reads these files to "thaw" the process and resume execution.

---

## 🛠️ Usage in Phase 1

In this initial phase, snapshots are stored in local subdirectories to simulate node-to-node movement.

> **Pro-Tip:** If you are testing locally, you can manually inspect `env.json` to ensure your **Wekeza Bank** API keys and database connection strings are being captured correctly before they are moved to the target node.

---

### ✅ Snapshot Layer: MISSION ACCOMPLISHED

We have defined the storage contract. This is the "cargo" that our teleportation engine will carry.
