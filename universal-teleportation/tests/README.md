# WekezaOmniOS Teleportation Tests

This folder contains automated tests for the Phase 1 teleportation engine.

## Rules

- Rule 8 — Everything must be testable
- Use `pytest` for unit and integration tests
- Tests must cover:
  - State capture (`state-capture/`)
  - Snapshot creation (`snapshot-engine/`)
  - Process restore (`state-reconstruction/`)

## Example Usage

Run all tests:

```bash
pytest -v
