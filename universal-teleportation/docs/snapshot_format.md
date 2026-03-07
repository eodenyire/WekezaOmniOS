### 📦 Standardized Snapshot Format (UAT-v1)

To achieve **Rule 6: Snapshots Must Be Portable**, all teleportation data must be stored in a machine-agnostic structure. This document defines the mandatory files and schemas required for a valid process snapshot.

## 📁 File Manifest

Every snapshot is a directory (or compressed `.tar.gz`) containing the following four core components:

| File | Type | Description |
| --- | --- | --- |
| **`memory.dump`** | Binary | A raw dump of the process's virtual memory pages. This is the "Soul" of the process. |
| **`filesystem.tar`** | Archive | A compressed collection of any local files, logs, or temp data the process was using. |
| **`env.json`** | JSON | A map of all environment variables active at the moment of capture. |
| **`metadata.json`** | JSON | The "Passport" of the snapshot, containing telemetry and hardware requirements. |

---

## 📝 Metadata Schema (`metadata.json`)

The metadata file allows the engine to perform a **Compatibility Check** before attempting a restore. It prevents the system from trying to "thaw" a Linux process on a native Windows kernel without the proper adapter.

### Example Manifest:

```json
{
    "process_id": 1921,
    "snapshot_name": "snapshot_1921_wekeza_core",
    "engine_version": "1.0.0-phase1",
    "timestamp": "2026-03-07T18:20:00Z",
    "system_specs": {
        "os": "ubuntu-24.04",
        "architecture": "x86_64",
        "kernel": "6.8.0-101-generic"
    },
    "resource_usage": {
        "memory_rss_bytes": 128450560,
        "thread_count": 4
    },
    "checksum": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
}

```

---

## 🎯 Portability & Security Goals

1. **Hardware Independence:** Snapshots must rely on virtual memory addresses rather than physical RAM offsets.
2. **Integrity Verification:** The `checksum` field ensures that the snapshot was not corrupted during the "Jump" (transfer) across nodes.
3. **Atomic Restoration:** The **State Reconstruction** module must verify that all four files exist and match the `metadata.json` before initiating the reanimation process.

---

### ✅ Documentation: FORMAT LOCKED

We now have a clear blueprint for how our data will be stored. This is critical because it tells the **Snapshot Engine** exactly what to build.
