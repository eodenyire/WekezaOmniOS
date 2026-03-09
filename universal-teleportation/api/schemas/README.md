# API Schemas

This folder contains Pydantic models used by the API.

## Purpose

Schema models provide typed contracts for:

- request payload validation
- response payload structure
- clear API documentation in OpenAPI
- consistent model reuse across route modules

## Files

- `models.py`
- `__init__.py`

## Current Coverage

`models.py` includes schema classes for:

- orchestration requests and responses
- process capture/snapshot/restore
- health and status payloads
- node registration and cluster operations
- remote teleport parameters
- container checkpoint/restore/teleport flows

## Design Notes

- Route modules import from `api.schemas.models`.
- `api/models.py` is maintained as a compatibility re-export wrapper.
- Prefer adding new API contract classes here rather than inside route modules.

## Extension Guidance

When adding a schema:

1. define it in `models.py`
2. add field descriptions/defaults where useful
3. keep naming explicit and endpoint-aligned
4. update route module imports to use the schema
