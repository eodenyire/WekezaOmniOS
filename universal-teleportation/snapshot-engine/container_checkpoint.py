"""
WekezaOmniOS Container Checkpoint Module - Phase 2
Creates container snapshots for teleportation.
"""
import os
import json
import tarfile
import subprocess
from datetime import datetime
from typing import Dict, Optional, List


class ContainerCheckpointEngine:
    """Checkpoints container state and creates transferable snapshots."""
    
    def __init__(self, snapshot_dir: str = "./snapshots"):
        """
        Initialize checkpoint engine.
        
        Args:
            snapshot_dir: Directory for storing snapshots
        """
        self.snapshot_dir = snapshot_dir
        self.checkpoints = {}
        os.makedirs(snapshot_dir, exist_ok=True)
        print(f"[ContainerCheckpointEngine] 📂 Snapshot directory: {snapshot_dir}")
    
    def checkpoint_docker_container(self, container_id: str, name: str = None) -> Optional[Dict]:
        """
        Checkpoint a Docker container.
        
        Args:
            container_id: Container ID or name
            name: Custom checkpoint name
            
        Returns:
            Checkpoint metadata
        """
        print(f"[ContainerCheckpointEngine] 📦 Checkpointing Docker container: {container_id}")
        
        checkpoint_name = name or f"docker-{container_id[:12]}-{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        checkpoint_dir = os.path.join(self.snapshot_dir, checkpoint_name)
        os.makedirs(checkpoint_dir, exist_ok=True)
        
        try:
            # Get container info
            result = subprocess.run(
                ["docker", "inspect", container_id],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print(f"[ContainerCheckpointEngine] ❌ Container not found")
                return None
            
            container_info = json.loads(result.stdout)[0]
            
            # Create checkpoint metadata
            checkpoint_meta = {
                "type": "docker_container",
                "container_id": container_id,
                "container_name": container_info["Name"].lstrip("/"),
                "image": container_info["Config"]["Image"],
                "timestamp": datetime.now().isoformat(),
                "state": container_info["State"]["Status"],
                "mounts": [m["Source"] for m in container_info.get("Mounts", [])],
                "ports": list(container_info.get("NetworkSettings", {}).get("Ports", {}).keys()),
                "env": container_info["Config"].get("Env", []),
                "labels": container_info["Config"].get("Labels", {}),
                "cmd": container_info["Config"].get("Cmd", []),
                "entrypoint": container_info["Config"].get("Entrypoint", [])
            }
            
            # Save container info
            info_path = os.path.join(checkpoint_dir, "container_info.json")
            with open(info_path, "w") as f:
                json.dump(container_info, f, indent=4)
            
            # Save checkpoint metadata
            meta_path = os.path.join(checkpoint_dir, "checkpoint.json")
            with open(meta_path, "w") as f:
                json.dump(checkpoint_meta, f, indent=4)
            
            # Export filesystem
            filesystem_archive = os.path.join(checkpoint_dir, "filesystem.tar.gz")
            print(f"[ContainerCheckpointEngine] 💾 Exporting filesystem...")
            
            # Export container
            export_path = os.path.join(checkpoint_dir, "container_export.tar")
            result = subprocess.run(
                ["docker", "export", container_id, "-o", export_path],
                capture_output=True
            )
            
            if result.returncode != 0:
                print(f"[ContainerCheckpointEngine] ⚠️  Checkpoint metadata created (filesystem export skipped)")
            else:
                # Compress
                with tarfile.open(filesystem_archive, "w:gz") as tar:
                    tar.add(export_path, arcname="filesystem.tar")
                os.remove(export_path)
                print(f"[ContainerCheckpointEngine] ✅ Filesystem exported and compressed")
            
            # Store checkpoint info
            checkpoint_info = {
                "name": checkpoint_name,
                "path": checkpoint_dir,
                "container_id": container_id,
                "metadata": checkpoint_meta,
                "created": datetime.now().isoformat()
            }
            
            self.checkpoints[checkpoint_name] = checkpoint_info
            
            print(f"[ContainerCheckpointEngine] ✅ Checkpoint created: {checkpoint_name}")
            return checkpoint_info
            
        except Exception as e:
            print(f"[ContainerCheckpointEngine] ❌ Error: {e}")
            return None
    
    def checkpoint_containerd_container(self, container_id: str, name: str = None) -> Optional[Dict]:
        """
        Checkpoint a containerd container.
        
        Args:
            container_id: Container ID
            name: Custom checkpoint name
            
        Returns:
            Checkpoint metadata
        """
        print(f"[ContainerCheckpointEngine] 📦 Checkpointing containerd container: {container_id}")
        
        checkpoint_name = name or f"containerd-{container_id[:12]}-{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        checkpoint_dir = os.path.join(self.snapshot_dir, checkpoint_name)
        os.makedirs(checkpoint_dir, exist_ok=True)
        
        try:
            # Get container info
            result = subprocess.run(
                ["ctr", "container", "info", container_id],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print(f"[ContainerCheckpointEngine] ❌ Container not found")
                return None
            
            container_info = json.loads(result.stdout)
            
            # Create checkpoint metadata (simplified for Phase 2)
            checkpoint_meta = {
                "type": "containerd_container",
                "container_id": container_id,
                "timestamp": datetime.now().isoformat(),
                "metadata": container_info
            }
            
            # Save checkpoint metadata
            meta_path = os.path.join(checkpoint_dir, "checkpoint.json")
            with open(meta_path, "w") as f:
                json.dump(checkpoint_meta, f, indent=4)
            
            checkpoint_info = {
                "name": checkpoint_name,
                "path": checkpoint_dir,
                "container_id": container_id,
                "metadata": checkpoint_meta,
                "created": datetime.now().isoformat()
            }
            
            self.checkpoints[checkpoint_name] = checkpoint_info
            
            print(f"[ContainerCheckpointEngine] ✅ Checkpoint created: {checkpoint_name}")
            return checkpoint_info
            
        except Exception as e:
            print(f"[ContainerCheckpointEngine] ❌ Error: {e}")
            return None
    
    def get_checkpoint(self, checkpoint_name: str) -> Optional[Dict]:
        """Get checkpoint information."""
        return self.checkpoints.get(checkpoint_name)
    
    def list_checkpoints(self) -> List[Dict]:
        """List all checkpoints."""
        return list(self.checkpoints.values())
    
    def delete_checkpoint(self, checkpoint_name: str) -> bool:
        """Delete a checkpoint."""
        if checkpoint_name in self.checkpoints:
            import shutil
            checkpoint_path = self.checkpoints[checkpoint_name]["path"]
            shutil.rmtree(checkpoint_path)
            del self.checkpoints[checkpoint_name]
            print(f"[ContainerCheckpointEngine] ✅ Checkpoint deleted: {checkpoint_name}")
            return True
        return False


# Example usage
if __name__ == "__main__":
    print("🚀 WekezaOmniOS Container Checkpoint Engine - Phase 2\n")
    
    engine = ContainerCheckpointEngine()
    
    # Try to checkpoint a container if one exists
    containers = []
    try:
        result = subprocess.run(
            ["docker", "ps", "-q"],
            capture_output=True,
            text=True
        )
        containers = result.stdout.strip().split("\n") if result.stdout.strip() else []
    except:
        pass
    
    if containers and containers[0]:
        print(f"Found Docker container: {containers[0][:12]}")
        checkpoint = engine.checkpoint_docker_container(containers[0])
        if checkpoint:
            print(f"✅ Checkpoint created successfully\n")
            print(json.dumps(checkpoint["metadata"], indent=2))
    else:
        print("No running Docker containers found")
        print("Demo: Checkpoint engine ready for Phase 2\n")
    
    print("\n✅ Container checkpoint engine ready")
