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
