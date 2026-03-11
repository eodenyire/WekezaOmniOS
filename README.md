# WekezaOmniOS

WekezaOmniOS is a research and engineering repository for multiple ways of delivering a universal operating environment. The repo contains four major implementation tracks, each exploring a different path toward the OmniOS goal: virtualization, interface emulation, cloud-hosted desktops, and stateful application teleportation.

## Core Idea

OmniOS is not a single prototype. It is a family of system designs for giving users and developers access to applications, interfaces, and workloads across different devices and operating systems.

The implementations in this repository answer the same question in four different ways:

1. Run the target environment directly through virtualization.
2. Recreate the target experience through interface emulation.
3. Host the environment remotely through a cloud desktop platform.
4. Move the live application state itself through universal teleportation.

## The Four OmniOS Implementations

### 1. Virtualization Layer

The virtualization model focuses on running real operating systems and workloads inside managed virtual machines or containers.

Main area:
- `virtualization-layer/`: VM, container, auth, and image orchestration concepts.

Typical use case:
- Delivering a native guest OS session with strong isolation and predictable behavior.

### 2. Interface Emulation

The interface emulation model uses a Linux-based foundation while recreating the user experience of other operating systems through skins, command translation, and compatibility layers.

Main area:
- `interface-emulation/`: UI skins, compatibility modules, kernel abstractions, and desktop management.

Typical use case:
- Giving users a familiar OS experience without fully running that OS underneath.

### 3. Cloud Desktop Model

The cloud desktop model treats the desktop as a remotely orchestrated service. Compute, storage, API management, and browser delivery are handled through distributed cloud components.

Main area:
- `cloud-desktop-model/`: API gateway, compute nodes, control plane, storage system, web platform, and workspace manager.

Typical use case:
- Serving workspaces or application sessions from centralized infrastructure.

### 4. Universal Teleportation

Universal Teleportation is the fourth OmniOS implementation and the most advanced systems experiment in the repository. Instead of only reproducing an operating system or hosting it remotely, this approach captures the live state of an application and reconstructs it on another target environment.

Main area:
- `universal-teleportation/`: State capture, snapshot packaging, transfer, runtime adaptation, security, orchestration, and cross-platform restore.

Typical use case:
- Moving a running application session from one device, OS, or node to another without restarting from scratch.

## Repository Layout

Top-level implementation tracks:
- `virtualization-layer/`
- `interface-emulation/`
- `cloud-desktop-model/`
- `universal-teleportation/`

Supporting areas:
- `benchmarking/`: Performance and measurement work.
- `cli/`: Command-line interfaces and tooling entry points.
- `cluster/`: Cluster-level scaffolding.
- `cross-os-runtime/`: Runtime translation and cross-OS execution concepts.
- `dev-tools/`: Developer utilities and support tooling.
- `docs/`: Shared project documentation.
- `monitoring/`: Observability and monitoring components.
- `sdk/`: Developer-facing SDK assets.
- `snapshots/`: Root-level demo and test snapshot artifacts.

## How To Read This Repository

If you are new to the project, use this order:

1. Start with the root architecture folders to understand the four implementation strategies.
2. Read the `README.md` inside each major folder for the responsibilities of that subsystem.
3. Dive into `universal-teleportation/` if you want the most complete and deeply implemented track.

## Current Position

The repository began with three OmniOS implementation directions, but it now clearly contains a fourth: Universal Teleportation. The root structure and documentation should be read as a four-track OmniOS research platform, not a three-track one.

## Goal

The long-term goal of WekezaOmniOS is to discover the most practical path toward seamless cross-device, cross-platform, and cross-environment computing, whether that is achieved by virtualization, emulation, cloud delivery, teleportation, or a hybrid of all four.