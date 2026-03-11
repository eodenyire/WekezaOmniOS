# state-capture/engines

## Purpose
Contains pluggable capture engines used to collect runtime state from different execution environments.

## Key Modules
- `capture_manager.py`: Engine selection and capture orchestration.
- `container_engine.py`: Container-focused capture implementation.
- `criu_engine.py`: CRIU-based capture integration.
