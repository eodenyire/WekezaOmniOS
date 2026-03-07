# WekezaOmniOS Transfer Layer

This module handles the movement of snapshots between environments for Universal Application Teleportation (UAT).

## Phase 1

- Supports **local file transfer**  
- Placeholder for **SSH, gRPC, WebRTC, distributed storage**  

## Example Flow

1. Capture process → snapshot  
2. Call `transfer_manager.send_snapshot(process_id, target_path)`  
3. Snapshot is moved to target directory  
4. Restore manager can use snapshot to reconstruct process
