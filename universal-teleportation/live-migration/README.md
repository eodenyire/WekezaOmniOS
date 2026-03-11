# live-migration

## Purpose
Implements live process and memory migration components for low-downtime teleportation flows.

## Key Modules
- `migration_controller.py`: Orchestrates migration phases.
- `dirty_page_tracker.py`, `page_bitmap.py`: Incremental memory tracking.
- `memory_streamer.py`: Streams memory pages to target runtime.
- `migration_state.py`: Shared migration state model.
