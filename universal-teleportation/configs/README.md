# WekezaOmniOS Configurations

This folder contains all configuration files used by the Universal Application Teleportation (UAT) engine.

## Files

- `system.yaml` — General system settings
- `criu_config.yaml` — CRIU-specific configuration
- `teleportation.yaml` — Teleportation engine settings

## Purpose

- Provide a **single source of truth** for all engine parameters
- Support **phase 1 local teleportation**
- Prepare for **phase 2 distributed teleportation**
- Allow easy overrides without changing code
