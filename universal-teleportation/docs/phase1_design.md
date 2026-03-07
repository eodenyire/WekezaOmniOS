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

