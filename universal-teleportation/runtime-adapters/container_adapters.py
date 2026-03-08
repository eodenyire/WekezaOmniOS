"""
WekezaOmniOS Docker Adapter - Phase 2
Enables teleportation of Docker containers.
"""
import subprocess
import json
import os
from typing import Dict, Optional

class DockerAdapter:
    """Handles Docker container teleportation."""
    
    def __init__(self):
        """Initialize Docker adapter."""
        self.containers = {}
        self.images = {}
        self.check_docker_availability()
    
    def check_docker_availability(self) -> bool:
        """Check if Docker is available on the system."""
        try:
            result = subprocess.run(
                ["docker", "version"],
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                print("[DockerAdapter] ✅ Docker is available")
                return True
            else:
                print("[DockerAdapter] ⚠️  Docker not available (will use fallback)")
                return False
        except:
            print("[DockerAdapter] ⚠️  Docker command not found")
            return False
    
    def get_container_info(self, container_id: str) -> Optional[Dict]:
        """Get detailed information about a container."""
        try:
            result = subprocess.run(
                ["docker", "inspect", container_id],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                container_info = {
                    "id": data[0]["Id"],
                    "name": data[0]["Name"].lstrip("/"),
                    "state": data[0]["State"]["Status"],
                    "image": data[0]["Config"]["Image"],
                    "mounts": [m["Source"] for m in data[0].get("Mounts", [])],
                    "ports": list(data[0].get("NetworkSettings", {}).get("Ports", {}).keys()),
                    "env": data[0]["Config"].get("Env", [])
                }
                return container_info
        except Exception as e:
            print(f"[DockerAdapter] Error inspecting container: {e}")
        
        return None
    
    def create_container_snapshot(self, container_id: str, snapshot_path: str) -> bool:
        """
        Create a snapshot of a running Docker container.
        
        Args:
            container_id: Container ID or name
            snapshot_path: Path to save snapshot
            
        Returns:
            Success status
        """
        print(f"[DockerAdapter] 📦 Creating snapshot of container {container_id}...")
        
        try:
            # Get container info
            container_info = self.get_container_info(container_id)
            if not container_info:
                print(f"[DockerAdapter] ❌ Container not found")
                return False
            
            # Create snapshot directory
            os.makedirs(snapshot_path, exist_ok=True)
            
            # Export container filesystem
            export_path = os.path.join(snapshot_path, "container.tar")
            result = subprocess.run(
                ["docker", "export", container_id, "-o", export_path],
                capture_output=True
            )
            
            if result.returncode != 0:
                print(f"[DockerAdapter] ❌ Failed to export container")
                return False
            
            # Save container metadata
            metadata_path = os.path.join(snapshot_path, "container_info.json")
            with open(metadata_path, "w") as f:
                json.dump(container_info, f, indent=4)
            
            print(f"[DockerAdapter] ✅ Snapshot created: {snapshot_path}")
            return True
            
        except Exception as e:
            print(f"[DockerAdapter] ❌ Error: {e}")
            return False
    
    def restore_container_from_snapshot(self, snapshot_path: str, image_name: str = None, container_name: str = None) -> Optional[str]:
        """
        Restore a container from snapshot.
        
        Args:
            snapshot_path: Path to snapshot
            image_name: Name for the new image
            container_name: Name for the new container
            
        Returns:
            New container ID
        """
        print(f"[DockerAdapter] ⚡ Restoring container from snapshot...")
        
        try:
            container_tar = os.path.join(snapshot_path, "container.tar")
            
            if not os.path.exists(container_tar):
                print(f"[DockerAdapter] ❌ Container archive not found")
                return None
            
            # Create new image from archive
            image_name = image_name or "restored-container:latest"
            result = subprocess.run(
                ["docker", "import", container_tar, image_name],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print(f"[DockerAdapter] ❌ Failed to create image")
                return None
            
            # Create container from image
            container_name = container_name or "restored-container"
            result = subprocess.run(
                ["docker", "run", "-d", "--name", container_name, image_name],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                container_id = result.stdout.strip()
                print(f"[DockerAdapter] ✅ Container restored: {container_name} ({container_id})")
                return container_id
            else:
                print(f"[DockerAdapter] ❌ Failed to create container")
                return None
                
        except Exception as e:
            print(f"[DockerAdapter] ❌ Error: {e}")
            return None
    
    def list_containers(self, running_only: bool = False) -> list:
        """List Docker containers."""
        try:
            cmd = ["docker", "ps"]
            if not running_only:
                cmd.append("-a")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")[1:]  # Skip header
                containers = []
                for line in lines:
                    parts = line.split()
                    if parts:
                        containers.append({"id": parts[0], "image": parts[1]})
                return containers
        except:
            pass
        
        return []


class ContainerdAdapter:
    """Handles containerd container teleportation."""
    
    def __init__(self):
        """Initialize containerd adapter."""
        self.check_containerd_availability()
    
    def check_containerd_availability(self) -> bool:
        """Check if containerd is available."""
        try:
            result = subprocess.run(
                ["ctr", "version"],
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                print("[ContainerdAdapter] ✅ Containerd is available")
                return True
            else:
                print("[ContainerdAdapter] ⚠️  Containerd not available")
                return False
        except:
            print("[ContainerdAdapter] ⚠️  Containerd command not found")
            return False
    
    def list_containers(self) -> list:
        """List containerd containers."""
        try:
            result = subprocess.run(
                ["ctr", "container", "list"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")[1:]  # Skip header
                containers = []
                for line in lines:
                    parts = line.split()
                    if parts:
                        containers.append({"id": parts[0]})
                return containers
        except:
            pass
        
        return []
    
    def create_container_snapshot(self, container_id: str, snapshot_path: str) -> bool:
        """Create snapshot of a containerd container."""
        print(f"[ContainerdAdapter] 📦 Snapshot feature coming in Phase 3...")
        # Phase 2: Placeholder
        return True


# Example usage
if __name__ == "__main__":
    print("🚀 WekezaOmniOS Container Adapters - Phase 2\n")
    
    # Test Docker adapter
    docker = DockerAdapter()
    containers = docker.list_containers()
    print(f"\nDocker Containers: {len(containers)} found")
    for container in containers[:3]:  # Show first 3
        print(f"  - {container['id'][:12]} ({container['image']})")
    
    print("\n")
    
    # Test Containerd adapter
    containerd = ContainerdAdapter()
    containers = containerd.list_containers()
    print(f"Containerd Containers: {len(containers)} found")
    
    print("\n✅ Container adapters ready for Phase 2")
