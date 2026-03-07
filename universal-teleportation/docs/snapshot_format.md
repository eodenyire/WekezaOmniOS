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

