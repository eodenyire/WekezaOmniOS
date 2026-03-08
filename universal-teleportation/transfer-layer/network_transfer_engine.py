"""
WekezaOmniOS Network Transfer Engine - Phase 2
Handles snapshot transfer between nodes via various protocols.
"""
import os
import shutil
import json
import hashlib
from typing import Dict, Optional
import time

class NetworkTransferEngine:
    """Manages snapshot transfers between cluster nodes."""
    
    def __init__(self):
        """Initialize network transfer engine."""
        self.transfer_history = []
        self.chunk_size = 1024 * 1024  # 1MB chunks
    
    def calculate_checksum(self, file_path: str) -> str:
        """Calculate SHA256 checksum of a file."""
        sha256_hash = hashlib.sha256()
        
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        
        return sha256_hash.hexdigest()
    
    def verify_transfer(self, source_path: str, target_path: str) -> bool:
        """Verify transfer integrity by comparing checksums."""
        source_checksum = self.calculate_checksum(source_path)
        target_checksum = self.calculate_checksum(target_path)
        
        if source_checksum == target_checksum:
            print(f"[NetworkTransfer] ✅ Checksum verified: {source_checksum}")
            return True
        else:
            print(f"[NetworkTransfer] ❌ Checksum mismatch!")
            return False
    
    def record_transfer(self, source: str, destination: str, size: int, duration: float, success: bool):
        """Record transfer operation for metrics."""
        record = {
            "timestamp": time.time(),
            "source": source,
            "destination": destination,
            "size_bytes": size,
            "duration_seconds": duration,
            "throughput_mbps": (size / (1024 * 1024)) / duration if duration > 0 else 0,
            "success": success
        }
        self.transfer_history.append(record)
        
        if success:
            mbps = record["throughput_mbps"]
            print(f"[NetworkTransfer] 📊 Throughput: {mbps:.2f} MB/s")
    
    def get_transfer_stats(self) -> Dict:
        """Get overall transfer statistics."""
        if not self.transfer_history:
            return {"total_transfers": 0, "successful": 0, "failed": 0}
        
        total = len(self.transfer_history)
        successful = sum(1 for t in self.transfer_history if t["success"])
        total_size = sum(t["size_bytes"] for t in self.transfer_history)
        total_time = sum(t["duration_seconds"] for t in self.transfer_history)
        
        return {
            "total_transfers": total,
            "successful": successful,
            "failed": total - successful,
            "total_data_transferred_gb": total_size / (1024 ** 3),
            "average_throughput_mbps": (total_size / (1024 ** 2)) / total_time if total_time > 0 else 0
        }


class LocalTransferEngine(NetworkTransferEngine):
    """Transfer snapshots locally."""
    
    def transfer(self, source_path: str, destination_path: str, verify: bool = True) -> bool:
        """
        Transfer snapshot locally.
        
        Args:
            source_path: Source snapshot file
            destination_path: Destination path
            verify: Verify transfer integrity
            
        Returns:
            Success status
        """
        if not os.path.exists(source_path):
            print(f"[LocalTransfer] ❌ Source not found: {source_path}")
            return False

        start_time = time.time()
        
        try:
            print(f"[LocalTransfer] 📋 Copying {os.path.basename(source_path)}")
            
            # Ensure destination directory exists
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            
            # Copy the file
            shutil.copy2(source_path, destination_path)
            
            file_size = os.path.getsize(source_path)
            duration = time.time() - start_time
            
            # Verify transfer
            if verify:
                if not self.verify_transfer(source_path, destination_path):
                    return False
            
            self.record_transfer(source_path, destination_path, file_size, duration, True)
            print(f"[LocalTransfer] ✅ Transfer complete")
            
            return True
            
        except Exception as e:
            duration = time.time() - start_time
            self.record_transfer(source_path, destination_path, 0, duration, False)
            print(f"[LocalTransfer] ❌ Transfer failed: {e}")
            return False

    def transfer_file(self, source_path: str, destination_path: str, verify: bool = True):
        """Compatibility wrapper returning success and stats tuple."""
        ok = self.transfer(source_path, destination_path, verify=verify)
        stats = self.transfer_history[-1] if self.transfer_history else {}
        return ok, stats


class ManifestTransfer(NetworkTransferEngine):
    """Transfer metadata alongside snapshots."""
    
    def create_manifest(self, snapshot_path: str, additional_info: Optional[Dict] = None) -> Dict:
        """
        Create a manifest file for the snapshot.
        
        Args:
            snapshot_path: Path to snapshot
            additional_info: Extra metadata
            
        Returns:
            Manifest dictionary
        """
        if os.path.isdir(snapshot_path):
            files = []
            total_size = 0
            for root, _, filenames in os.walk(snapshot_path):
                for name in filenames:
                    full_path = os.path.join(root, name)
                    rel = os.path.relpath(full_path, snapshot_path)
                    size = os.path.getsize(full_path)
                    total_size += size
                    files.append(
                        {
                            "name": rel,
                            "size_bytes": size,
                            "checksum_sha256": self.calculate_checksum(full_path),
                        }
                    )
            manifest = {
                "directory": os.path.basename(snapshot_path),
                "path": os.path.abspath(snapshot_path),
                "size_bytes": total_size,
                "files": files,
                "timestamp": time.time(),
                "additional_info": additional_info or {},
            }
        else:
            file_size = os.path.getsize(snapshot_path)
            checksum = self.calculate_checksum(snapshot_path)
            manifest = {
                "file": os.path.basename(snapshot_path),
                "path": os.path.abspath(snapshot_path),
                "size_bytes": file_size,
                "checksum_sha256": checksum,
                "timestamp": time.time(),
                "additional_info": additional_info or {},
            }
        
        return manifest
    
    def save_manifest(self, manifest: Dict, destination_path: str) -> str:
        """Save manifest to a file path or directory path."""
        if destination_path.endswith(".json"):
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            manifest_path = destination_path
        else:
            os.makedirs(destination_path, exist_ok=True)
            manifest_path = os.path.join(destination_path, "manifest.json")
        
        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=4)
        
        print(f"[ManifestTransfer] ✅ Manifest saved: {manifest_path}")
        
        return manifest_path


# Example usage
if __name__ == "__main__":
    print("🚀 WekezaOmniOS Network Transfer Engine - Phase 2\n")
    
    # Test local transfer
    engine = LocalTransferEngine()
    
    # Create test snapshot
    test_source = "/tmp/test_snapshot.tar.gz"
    test_dest = "/tmp/test_snapshot_copy.tar.gz"
    
    with open(test_source, "wb") as f:
        f.write(b"test snapshot data" * 10000)
    
    print("Testing Local Transfer:")
    success = engine.transfer(test_source, test_dest)
    
    if success:
        print("\nTransfer Statistics:")
        stats = engine.get_transfer_stats()
        for key, value in stats.items():
            print(f"  {key}: {value}")
    
    print("\n✅ Network transfer engine ready")
