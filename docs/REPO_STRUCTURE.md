## Repository Structure Policy

This file defines where different artifact types should live so the repository remains searchable and predictable.

### Top-level ownership

- `virtualization-layer/`: virtualization implementation and docs for that track.
- `interface-emulation/`: interface emulation implementation and docs for that track.
- `cloud-desktop-model/`: cloud desktop implementation and docs for that track.
- `universal-teleportation/`: stateful teleportation implementation and docs for that track.
- `docs/`: cross-track and repo-level documentation only.

### Artifact placement rules

- Code and runtime assets stay with the owning module.
- Tests live in each module's `tests/` folder.
- Architecture, plans, and reports should live under module `docs/` folders or the repo `docs/` folder.
- Avoid placing planning or report files in implementation roots when a `docs/` folder exists.

### Naming conventions

- Use lowercase kebab-case for new markdown docs.
- Prefer `.md` for text documentation.
- Prefix phase documents consistently when applicable, for example `phase-07-plan.md`.

### Universal Teleportation guidance

Universal Teleportation documentation has been grouped under `universal-teleportation/docs/` by category.
Use `universal-teleportation/docs/INDEX.md` as the canonical map when adding or locating docs.
