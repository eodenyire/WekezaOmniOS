# **WekezaOmniOS Universal Teleportation — Developer Guide**

| Module / Folder           | File                            | Phase | Description                                                                 |
| ------------------------- | ------------------------------- | ----- | --------------------------------------------------------------------------- |
| **api/**                  | `teleport_endpoint.py`          | 1–2   | Handles standard teleport API requests between nodes or OS environments.    |
|                           | `clone_endpoint.py`             | 3     | Handles clone execution requests for duplicating apps.                      |
|                           | `interplanetary_endpoint.py`    | 15    | Schedules teleportation across interplanetary or high-latency nodes.        |
|                           | `hardware_endpoint.py`          | 20    | Interface for future teleportation hardware integration.                    |
| **cli/**                  | `commands.py`                   | 1     | CLI commands for teleportation operations.                                  |
|                           | `teleport.py`                   | 1–2   | Command-line tool to initiate teleport of a process.                        |
|                           | `utils.py`                      | 1     | Helper functions for CLI operations.                                        |
| **cluster/**              | `cluster_manager.py`            | 2     | Manages nodes, orchestration, and cluster state.                            |
|                           | `node_registry.json`            | 2     | Stores registered cluster nodes and metadata.                               |
| **configs/**              | `criu_config.yaml`              | 1     | CRIU checkpointing options.                                                 |
|                           | `system.yaml`                   | 1     | Global system configuration.                                                |
|                           | `teleportation.yaml`            | 1–20  | Teleportation-specific configuration for snapshots, transfer, and adapters. |
| **demo/**                 | `demo_app.py`                   | 1     | Sample app to teleport.                                                     |
|                           | `demo_server.py`                | 1     | Demonstrates teleportation server functionality.                            |
|                           | `README.md`                     | 1     | Documentation for demo execution.                                           |
| **docs/**                 | `architecture.md`               | 1     | System architecture of UAT platform.                                        |
|                           | `phase1_design.md`              | 1     | Phase 1 design and module breakdown.                                        |
|                           | `snapshot_format.md`            | 1     | Snapshot structure and metadata specification.                              |
|                           | `teleportation-overview.md`     | 1     | High-level overview of teleportation functionality.                         |
|                           | `teleportation_architecture.md` | 1     | Details of engines, transfer layer, and runtime adapters.                   |
|                           | `UTP_RFC.md`                    | 2     | RFC for the Universal Teleportation Protocol (UTP).                         |
| **logs/**                 | `capture.log`                   | 1     | Logs for state capture events.                                              |
|                           | `restore.log`                   | 1     | Logs for state restoration events.                                          |
|                           | `teleport.log`                  | 1     | General teleportation events log.                                           |
| **monitoring/**           | `telemetry_hub.py`              | 1     | Observability and telemetry for running processes.                          |
| **runtime-adapters/**     | `linux_adapter.py`              | 1     | OS-specific adapter for Linux environments.                                 |
|                           | `windows_adapter.py`            | 1     | Adapter for Windows environment mapping.                                    |
|                           | `android_adapter.py`            | 1     | Adapter for Android processes.                                              |
|                           | `apple_adapter.py`              | 6     | Adapter for Apple OS environments.                                          |
| **scripts/**              | `setup.sh`                      | 1     | Installs dependencies and sets up environment.                              |
|                           | `run_demo.sh`                   | 1     | Runs demo application in background and logs PID.                           |
| **snapshot-engine/**      | `snapshot_builder.py`           | 1     | Builds portable snapshots from captured state.                              |
|                           | `snapshot_reader.py`            | 1     | Reads and interprets snapshot data.                                         |
|                           | `snapshot_metadata.py`          | 1     | Stores metadata for snapshots.                                              |
|                           | `matter_scanner.py`             | 16    | Scans process state for hypothetical matter teleportation.                  |
|                           | `energy_simulation.py`          | 16    | Simulates energy-to-matter conversion for teleportation.                    |
|                           | `quantum_metadata.json`         | 11    | Placeholder for quantum simulation metadata.                                |
|                           | `biological_metadata.json`      | 12    | Placeholder for biological state data.                                      |
|                           | `matter_metadata.json`          | 16    | Metadata for matter simulation.                                             |
|                           | `energy_metadata.json`          | 16    | Metadata for energy simulation.                                             |
| **snapshot/**             | `env.json`                      | 1     | Environment variables of captured process.                                  |
|                           | `filesystem.tar`                | 1     | Compressed filesystem of the process.                                       |
|                           | `memory.dump`                   | 1     | Memory dump for snapshot reconstruction.                                    |
|                           | `metadata.json`                 | 1     | Snapshot metadata including process ID, timestamp, OS.                      |
|                           | `README.md`                     | 1     | Portability rules and snapshot explanation.                                 |
| **state-capture/**        | `capture_manager.py`            | 1     | Controls checkpointing of process.                                          |
|                           | `process_inspector.py`          | 1     | Retrieves process info such as PID, memory, threads.                        |
|                           | `criu_wrapper.py`               | 1     | Wrapper for CRIU dump commands.                                             |
|                           | `utils.py`                      | 1     | Helper functions for state capture.                                         |
|                           | `quantum_layer.py`              | 11    | Simulates probabilistic quantum states of apps.                             |
|                           | `biological_layer.py`           | 12    | Simulates biological states for digital twin processes.                     |
| **state-reconstruction/** | `restore_manager.py`            | 1     | Controls restoration from snapshot.                                         |
|                           | `criu_restore.py`               | 1     | Wrapper for CRIU restore commands.                                          |
|                           | `environment_loader.py`         | 1     | Loads environment variables into restored process.                          |
|                           | `multi_restore_manager.py`      | 14    | Handles multi-node or interplanetary restores.                              |
|                           | `atomic_reconstructor.py`       | 17    | Atomic-level reconstruction of snapshots.                                   |
|                           | `biological_safety.py`          | 18    | Validates biological teleportation safety rules.                            |
| **teleportation-api/**    | `teleport.py`                   | 1     | Main API for teleporting processes.                                         |
|                           | `clone.py`                      | 3     | API for clone execution mode.                                               |
|                           | `interplanetary.py`             | 15    | API for teleporting across extreme latency nodes.                           |
|                           | `hardware.py`                   | 20    | API for integrating teleportation hardware.                                 |
| **tests/**                | `test_capture.py`               | 1     | Unit tests for state-capture module.                                        |
|                           | `test_snapshot.py`              | 1     | Unit tests for snapshot-engine module.                                      |
|                           | `test_restore.py`               | 1     | Unit tests for state-reconstruction module.                                 |
| **transfer-layer/**       | `parallel_transfer.py`          | 2     | Supports cross-node snapshot transfers.                                     |
|                           | `routing_engine.py`             | 14    | Planet-scale teleportation routing.                                         |
|                           | `latency_optimizer.py`          | 14    | Optimizes snapshot transfer latency.                                        |
|                           | `hardware_interface.py`         | 20    | Hardware interface for teleportation devices.                               |
| **ui-controls/**          | `ui.py`                         | 1     | Provides context menu and UI integration for teleporting apps.              |
| **Root**                  | `.gitignore`                    | 1     | Standard Git ignore file.                                                   |
|                           | `EngineeringRules.md`           | 1     | Project engineering rules.                                                  |
|                           | `LICENSE`                       | 1     | MIT License placeholder.                                                    |
|                           | `PHASES.md`                     | 1     | Teleportation project phases 1–20.                                          |
|                           | `PHASES_1.md`                   | 1     | Phase 1 implementation details.                                             |
|                           | `PHASE1_PROGRESS.md`            | 1     | Phase 1 progress report.                                                    |
|                           | `README.md`                     | 1     | Main project README.                                                        |

---

This table gives a **full developer overview**:

* Which **phase each file belongs to**
* **What each file does**
* Enables **tracking features from Phase 1 → Phase 20**
---


Do you want me to do that next?
