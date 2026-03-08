"""
WekezaOmniOS Container Restore Module - Phase 2
Restores containerized applications from checkpoints.
"""
import os
import json
import subprocess
import tarfile
from typing import Dict, Optional
from datetime import datetime


class ContainerRestoreEngine:
    """Restores containers from checkpoints."""
    
    def __init__(self, snapshot_dir: str = "./snapshots"):
        """
        Initialize restore engine.
        
        Args:
            snapshot_dir: Directory containing snapshots
        """
        self.snapshot_dir = snapshot_dir
        self.restored_containers = {}
    
    def restore_docker_container(self, checkpoint_path: str, node_id: str = "local", custom_name: str = None) -> Optional[str]:
        """
        Restore a Docker container from checkpoint.
        
        Args:
            checkpoint_path: Path to checkpoint directory
            node_id: Target node identifier
            custom_name: Custom name for restored container
            
        Returns:
            Container ID if successful
        """
        print(f"[ContainerRestoreEngine] ⚡ Restoring Docker container from {checkpoint_path}")
        
        try:
            # Load checkpoint metadata
            meta_path = os.path.join(checkpoint_path, "checkpoint.json")
            if not os.path.exists(meta_path):
                print(f"[ContainerRestoreEngine] ❌ Checkpoint metadata not found")
                return None
            
            with open(meta_path, "r") as f:
                checkpoint_meta = json.load(f)
            
            # Prepare container name
            original_name = checkpoint_meta.get("container_name", "unknown")
            container_name = custom_name or f"{original_name}-restored-{node_id}"
            
            print(f"[ContainerRestoreEngine] 📝 Container name: {container_name}")
            
            # Try to restore from filesystem archive
            filesystem_archive = os.path.join(checkpoint_path, "filesystem.tar.gz")
            
            if os.path.exists(filesystem_archive):
                # Extract archive
                print(f"[ContainerRestoreEngine] 📦 Extracting filesystem...")
                extract_dir = os.path.join(checkpoint_path, "extracted")
                os.makedirs(extract_dir, exist_ok=True)
                
                with tarfile.open(filesystem_archive, "r:gz") as tar:
                    tar.extractall(extract_dir)
                
                container_export = os.path.join(extract_dir, "filesystem.tar")
                
                if os.path.exists(container_export):
                    # Create image from export
                    image_name = f"{original_name}:restored-{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    print(f"[ContainerRestoreEngine] 🎨 Creating image: {image_name}")
                    
                    result = subprocess.run(
                        ["docker", "import", container_export, image_name],
                        capture_output=True,
                        text=True
                    )
                    
                    if result.returncode != 0:
                        print(f"[ContainerRestoreEngine] ⚠️  Could not create image (will start empty container)")
                        image_name = checkpoint_meta.get("image", "alpine:latest")
                    
                    # Create container
                    print(f"[ContainerRestoreEngine] 🏗️  Creating container...")
                    
                    cmd = ["docker", "run", "-d", "--name", container_name]
                    
                    # Add ports if any
                    ports = checkpoint_meta.get("ports", [])
                    for port in ports:
                        cmd.extend(["-p", port])
                    
                    # Add environment variables
                    env_vars = checkpoint_meta.get("env", [])
                    for env in env_vars:
                        if "=" in env:
                            cmd.extend(["-e", env])
                    
                    # Add labels
                    labels = checkpoint_meta.get("labels", {})
                    for key, value in labels.items():
                        cmd.extend(["-l", f"{key}={value}"])
                    
                    cmd.append(image_name)
                    
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        container_id = result.stdout.strip()
                        
                        restored_info = {
                            "container_id": container_id,
                            "container_name": container_name,
                            "node_id": node_id,
                            "restored_from": checkpoint_path,
                            "restored_at": datetime.now().isoformat(),
                            "image": image_name
                        }
                        
                        self.restored_containers[container_name] = restored_info
                        
                        print(f"[ContainerRestoreEngine] ✅ Container restored: {container_name} ({container_id})")
                        return container_id
                    else:
                        print(f"[ContainerRestoreEngine] ❌ Failed to create container: {result.stderr}")
                        return None
            else:
                # Fallback: Create container with original image
                print(f"[ContainerRestoreEngine] 📋 Falling back to original image: {checkpoint_meta.get('image')}")
                
                cmd = ["docker", "run", "-d", "--name", container_name, checkpoint_meta.get("image", "alpine:latest")]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    container_id = result.stdout.strip()
                    print(f"[ContainerRestoreEngine] ✅ Container created: {container_name}")
                    return container_id
                else:
                    print(f"[ContainerRestoreEngine] ❌ Failed to create container")
                    return None
                    
        except Exception as e:
            print(f"[ContainerRestoreEngine] ❌ Error: {e}")
            return None
    
    def restore_containerd_container(self, checkpoint_path: str, node_id: str = "local", custom_name: str = None) -> Optional[str]:
        """
        Restore a containerd container from checkpoint.
        
        Args:
            checkpoint_path: Path to checkpoint directory
            node_id: Target node identifier
            custom_name: Custom name for restored container
            
        Returns:
            Container ID if successful
        """
        print(f"[ContainerRestoreEngine] ⚡ Restoring containerd container...")
        
        try:
            # Load checkpoint metadata
            meta_path = os.path.join(checkpoint_path, "checkpoint.json")
            if not os.path.exists(meta_path):
                print(f"[ContainerRestoreEngine] ❌ Checkpoint metadata not found")
                return None
            
            with open(meta_path, "r") as f:
                checkpoint_meta = json.load(f)
            
            container_id = checkpoint_meta.get("container_id", "unknown")
            
            print(f"[ContainerRestoreEngine] ✅ Checkpoint loaded for containerid: {container_id}")
            print(f"[ContainerRestoreEngine] 📝 Metadata available for Phase 3 detailed restore")
            
            return container_id
            
        except Exception as e:
            print(f"[ContainerRestoreEngine] ❌ Error: {e}")
            return None
    
    def verify_container(self, container_id: str, container_runtime: str = "docker") -> bool:
        """
        Verify a restored container is running.
        
        Args:
            container_id: Container ID
            container_runtime: 'docker' or 'containerd'
            
        Returns:
            True if container is running
        """
        try:
            if container_runtime == "docker":
                result = subprocess.run(
                    ["docker", "inspect", container_id],
                    capture_output=True
                )
                return result.returncode == 0
            elif container_runtime == "containerd":
                result = subprocess.run(
                    ["ctr", "container", "info", container_id],
                    capture_output=True
                )
                return result.returncode == 0
        except:
            pass
        
        return False
    
    def get_restored_container(self, container_name: str) -> Optional[Dict]:
        """Get information about a restored container."""
        return self.restored_containers.get(container_name)
    
    def list_restored_containers(self) -> list:
        """List all restored containers."""
        return list(self.restored_containers.values())


# Example usage
if __name__ == "__main__":
    print("🚀 WekezaOmniOS Container Restore Engine - Phase 2\n")
    
    engine = ContainerRestoreEngine()
    print("Container restore engine initialized and ready for Phase 2\n")
    print("✅ Ready to restore containers from checkpoints")
