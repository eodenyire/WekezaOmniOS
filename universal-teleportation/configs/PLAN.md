Perfect. We are now in the **`configs/` folder**, which is **critical for Phase 1** because it centralizes all system-wide settings, paths, and configuration parameters. This makes the teleportation engine **modular, maintainable, and easy to deploy**.

Let’s design it properly.

---

# 📁 Folder: `configs/`

Purpose:
Store all configuration files required by **Universal Teleportation**.

Responsibilities:

* Define directories (snapshots, logs)
* Configure CRIU and container paths
* Centralize system settings for CLI, API, and modules
* Enable easy modification for future nodes or cloud environments

---

# 📄 `README.md`

```md
# WekezaOmniOS Configurations

This folder contains all configuration files used by the Universal Application Teleportation (UAT) engine.

## Files

- `system.yaml` — General system settings
- `criu_config.yaml` — CRIU-specific configuration
- `teleportation.yaml` — Teleportation engine settings

## Purpose

- Provide a **single source of truth** for all engine parameters
- Support **phase 1 local teleportation**
- Prepare for **phase 2 distributed teleportation**
- Allow easy overrides without changing code
```

---

# 📄 `system.yaml`

Phase 1 local system configuration.

```yaml
# system.yaml
snapshot_directory: ./snapshots
log_directory: ./logs
temp_directory: ./temp
default_node: local-node
```

* `snapshot_directory`: where process snapshots are stored
* `log_directory`: where logs for capture/restore are saved
* `temp_directory`: temporary files
* `default_node`: node name for Phase 1 (local simulation)

---

# 📄 `criu_config.yaml`

CRIU-specific settings.

```yaml
# criu_config.yaml
criu_path: /usr/sbin/criu
use_shell_job: true
tcp_established: true
ext_unix_sk: true
```

* `criu_path`: path to CRIU binary
* `use_shell_job`: enable shell job support
* `tcp_established`: checkpoint TCP connections
* `ext_unix_sk`: external UNIX socket support

---

# 📄 `teleportation.yaml`

Teleportation engine settings.

```yaml
# teleportation.yaml
max_snapshot_size_mb: 500
default_restore_mode: pause_resume
enable_logging: true
default_engine: criu
```

* `max_snapshot_size_mb`: max allowed snapshot size
* `default_restore_mode`: options: `pause_resume`, `live_migration`
* `enable_logging`: toggle logging
* `default_engine`: default checkpoint engine (CRIU for Phase 1)

---

# 🔗 Integration Plan

All modules **read configs** from this folder:

```text
state-capture.capture_manager() → system.yaml, criu_config.yaml
snapshot-engine.snapshot_builder() → system.yaml
state-reconstruction.restore_manager() → teleportation.yaml
cli.teleport.py → system.yaml
api.server.py → teleportation.yaml
```

* Centralizes paths and engine settings
* Allows **easy migration to Phase 2 multi-node** without changing code

---

# 📂 Final `configs/` Folder Structure

```text
configs/
    README.md
    system.yaml
    criu_config.yaml
    teleportation.yaml
```

---

✅ **Next Step:**

After configs, the next critical folder is:

```text
demo/
```

This is where we **create demo apps** that run in Phase 1 and will be **captured, snapshotted, and restored**.

We can design `demo/README.md`, `demo_app.py`, and `demo_server.py` next, documenting the **demo workflow for testing teleportation**.

Do you want me to do that?
