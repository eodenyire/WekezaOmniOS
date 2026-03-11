# WekezaOmniOS Universal Application Teleportation - Quick Reference

## 🚀 Quick Start (5 Minutes)

### Option 1: Automated Demo
```bash
cd /workspaces/WekezaOmniOS/universal-teleportation
python3 scripts/orchestrate_phase1.py
```

### Option 2: Interactive Guide
```bash
cd /workspaces/WekezaOmniOS/universal-teleportation
python3 scripts/quickstart.py
```

### Option 3: Manual Testing
```bash
# 1. Check status
python3 cli/teleport.py status

# 2. Start demo app
python3 demo/demo_app.py &
PID=$!

# 3. Capture it
python3 cli/teleport.py capture $PID

# 4. Create snapshot
python3 cli/teleport.py snapshot $PID my_test

# 5. Test restore
python3 cli/teleport.py restore $PID

# 6. Cleanup
kill $PID
```

---

## 📋 CLI Commands

### Status Check
```bash
python3 cli/teleport.py status
```

### Capture Process
```bash
python3 cli/teleport.py capture <PID>
```

### Create Snapshot
```bash
python3 cli/teleport.py snapshot <PID> [snapshot_name]
```

### Restore Process
```bash
python3 cli/teleport.py restore <PID>
```

---

## 🌐 API Endpoints

### Start API Server
```bash
python3 api/server.py
```
Visit: http://localhost:8000/docs (Interactive documentation)

### Health Check
```bash
curl http://localhost:8000/
```

### Engine Status
```bash
curl http://localhost:8000/status
```

### Capture Process
```bash
curl -X POST http://localhost:8000/capture \
  -H "Content-Type: application/json" \
  -d '{"pid": 12345}'
```

### Create Snapshot
```bash
curl -X POST http://localhost:8000/snapshot \
  -H "Content-Type: application/json" \
  -d '{"pid": 12345, "snapshot_name": "my_snapshot"}'
```

### Restore Process
```bash
curl -X POST http://localhost:8000/restore \
  -H "Content-Type: application/json" \
  -d '{"snapshot_name": "my_snapshot"}'
```

### Full Teleportation
```bash
curl -X POST http://localhost:8000/teleport \
  -H "Content-Type: application/json" \
  -d '{
    "process_id": 12345,
    "source_env": "local",
    "target_env": "local"
  }'
```

---

## 📂 Important Directories

```
snapshots/           # Generated snapshots and archives
logs/                # Application logs
temp/                # Temporary files (PIDs)
demo/                # Demo applications
scripts/             # Automation scripts
```

---

## 🧪 Testing

### Run All Tests
```bash
pytest tests/ -v
```

### Specific Tests
```bash
pytest tests/test_capture.py -v
pytest tests/test_snapshot.py -v
pytest tests/test_restore.py -v
```

---

## 📊 Viewing Snapshots

### List Snapshots
```bash
ls -lh snapshots/
```

### View Snapshot Contents
```bash
tar -tzf snapshots/<snapshot_name>.tar.gz
```

### Extract Snapshot
```bash
tar -xzf snapshots/<snapshot_name>.tar.gz -C /tmp/
```

### View Metadata
```bash
cat snapshots/process_<PID>/metadata.json
cat snapshots/process_<PID>/process_metadata.json
cat snapshots/process_<PID>/env.json
```

---

## 🔍 Troubleshooting

### CRIU Not Available
- **Expected:** Fallback mode captures metadata only
- **Solution:** Install CRIU for full functionality
  ```bash
  # Note: CRIU may not work in all environments
  sudo apt install criu
  ```

### Permission Denied
- **Solution:** Run with appropriate permissions
  ```bash
  sudo python3 cli/teleport.py capture <PID>
  ```

### Process Not Found
- **Check:** Verify process is running
  ```bash
  ps aux | grep <PID>
  ```

### Import Errors
- **Solution:** Ensure you're in the project directory
  ```bash
  cd /workspaces/WekezaOmniOS/universal-teleportation
  ```

---

## 📚 Full Documentation

- `PHASE1_IMPLEMENTATION_COMPLETE.md` - Complete Phase 1 documentation
- `PHASE1_PROGRESS.md` - Progress tracking
- `docs/phase1_design.md` - Design details
- `docs/architecture.md` - System architecture
- `README.md` - Project overview

---

## 🎯 What Phase 1 Provides

✅ Local process state capture  
✅ Snapshot packaging  
✅ State restoration  
✅ CLI interface  
✅ REST API  
✅ Fallback mechanisms  
✅ Comprehensive logging  

## 🚀 Coming in Phase 2

- Cross-environment transfer
- Multi-OS support
- Cluster orchestration
- Advanced security
- Live migration

---

*Quick Reference for WekezaOmniOS Universal Application Teleportation Phase 1*
