---

## 🛠️ Transfer Layer Integration Plan

The Transfer Layer acts as the bridge between **Source State** and **Target Execution**. In Phase 1, we treat different local directories as "Virtual Nodes" to simulate real-world teleportation.

### 1. The Functional Flow

The integration follows a strict linear sequence to ensure data integrity:

1. **Trigger:** The `cli/` or `teleportation-api/` receives a `/teleport` request.
2. **Handoff:** After `snapshot-engine` finishes packaging the `.tar.gz`, it signals the `TransferManager`.
3. **Validation:** `TransferManager` verifies the snapshot exists in the `./snapshots` directory (the "Source Node").
4. **Transport:** `local_transfer.py` executes the move to the `./target_node/restoration_area`.
5. **Notification:** Once the move is complete, a success signal is sent to `state-reconstruction` to begin the "Resume" process.

---

### 2. Module Dependencies

To function, the Transfer Layer interacts with these specific modules:

* **`configs/system.yaml`**: To retrieve the default `snapshot_directory` and `temp_directory`.
* **`logs/teleport.log`**: Every transfer start, progress, and completion must be recorded for audit.
* **`snapshot/`**: This is the source "Warehouse" where the transfer layer picks up its cargo.

---

### 3. Integration Interface (Internal API)

The `TransferManager` exposes a clean internal method that other developers at **Wekeza Bank** can use without knowing the underlying protocol (Local vs. SSH):

```python
# Internal Integration Call
transfer_status = transfer_manager.send_snapshot(
    process_id=pid, 
    target_path=target_env_path
)

```

---

### 4. Phase 1 Testing Strategy (The "Smoke Test")

To verify the integration is successful, we will perform the following local test:

1. **Launch** the `demo/demo_app.py`.
2. **Manually** place a dummy `metadata.json` in `snapshots/process_demo/`.
3. **Run** the `TransferManager` to move it to `temp/target_node/`.
4. **Verify** the file hash or directory size in the target folder matches the source.

---

### 5. Transition to Phase 2

The architecture is already "Plug-and-Play." When we move to Phase 2:

* We will add a conditional check in `transfer_manager.py`.
* If `target_env` is a remote IP, it will automatically switch from `local_transfer.py` to `ssh_transfer.py`.
* **No other code in the API or CLI will need to change.**

---
