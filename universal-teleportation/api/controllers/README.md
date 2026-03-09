# API Controllers

This folder contains controller classes used by route modules to orchestrate domain operations. Controllers provide a stable boundary between HTTP endpoints and lower-level platform modules.

## Purpose

Controllers keep endpoint files small by centralizing business orchestration logic, such as:

- coordinating capture, snapshot, transfer, and restore steps
- handling cross-node lookup and health behavior
- emitting telemetry events
- delegating runtime-specific behavior to adapters

## Files

- `node_controller.py`
- `teleport_controller.py`
- `__init__.py`

## Responsibilities

### `node_controller.py`

- wraps cluster node manager access
- supports node registration, lookup, listing, and reachability checks
- standardizes registry path usage

### `teleport_controller.py`

- orchestrates remote process teleportation flow
- manages container checkpoint/restore/teleport operations
- enriches metadata for runtime dispatch translation
- emits telemetry for operations and outcomes

## Design Notes

- Controllers are imported by route modules under `api/routes/`.
- Controllers depend on project modules outside `api/` (snapshot engine, transfer layer, monitoring, runtime adapters).
- Top-level compatibility wrappers remain in `api/` for legacy imports.

## Extension Guidance

When adding a new operation:

1. add the orchestration method in the relevant controller
2. keep route handler thin and focused on HTTP concerns
3. return plain Python dicts or values that route layer maps to response schemas
4. avoid embedding HTTP-only concepts (status codes, request objects) in controllers
