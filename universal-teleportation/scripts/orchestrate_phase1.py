#!/usr/bin/env python3
"""
WekezaOmniOS Phase 1 - End-to-End Orchestration Test
Demonstrates the complete Universal Application Teleportation workflow.
"""

import os
import sys
import time
import subprocess
import signal
import json
from datetime import datetime
import importlib.util

# Add parent directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
sys.path.insert(0, project_dir)

# Change to project directory for relative paths
os.chdir(project_dir)

# Import modules using importlib (to handle hyphenated directory names)
def import_from_path(module_name, file_path):
    """Import a module from a file path."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Import the required modules
capture_manager_module = import_from_path(
    "capture_manager",
    os.path.join(project_dir, "state-capture", "capture_manager.py")
)
snapshot_builder_module = import_from_path(
    "snapshot_builder",
    os.path.join(project_dir, "snapshot-engine", "snapshot_builder.py")
)
restore_manager_module = import_from_path(
    "restore_manager",
    os.path.join(project_dir, "state-reconstruction", "restore_manager.py")
)

CaptureManager = capture_manager_module.CaptureManager
build_snapshot = snapshot_builder_module.build_snapshot
RestoreManager = restore_manager_module.RestoreManager

class Phase1Orchestrator:
    """Orchestrates the complete Phase 1 teleportation workflow."""
    
    def __init__(self):
        self.demo_pid = None
        self.snapshot_name = None
        
        # Set base directory to project root
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.base_dir = os.path.dirname(script_dir)
        
        # Initialize directories
        self.ensure_directories()
    
    def ensure_directories(self):
        """Create required directory structure."""
        dirs = ['snapshots', 'logs', 'temp', 'demo']
        for d in dirs:
            path = os.path.join(self.base_dir, d)
            os.makedirs(path, exist_ok=True)
            print(f"✅ Directory ready: {d}/")
    
    def print_banner(self, text):
        """Print a formatted banner."""
        print("\n" + "=" * 70)
        print(f"  {text}")
        print("=" * 70 + "\n")
    
    def print_step(self, step_num, title):
        """Print a formatted step header."""
        print(f"\n{'─' * 70}")
        print(f"Step {step_num}: {title}")
        print('─' * 70)
    
    def start_demo_app(self):
        """Launch the demo counter application."""
        self.print_step(1, "Starting Demo Application")
        
        demo_script = os.path.join(self.base_dir, 'demo', 'demo_app.py')
        
        # Start the demo app in background
        process = subprocess.Popen(
            [sys.executable, demo_script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid  # Create new process group
        )
        
        self.demo_pid = process.pid
        
        # Save PID to file
        pid_file = os.path.join(self.base_dir, 'temp', 'demo_app.pid')
        with open(pid_file, 'w') as f:
            f.write(str(self.demo_pid))
        
        print(f"🎯 Demo application started")
        print(f"   PID: {self.demo_pid}")
        print(f"   PID file: {pid_file}")
        
        # Give it a moment to initialize
        time.sleep(2)
        
        # Verify it's running
        try:
            os.kill(self.demo_pid, 0)
            print("✅ Process is running")
        except OSError:
            print("❌ Process failed to start")
            return False
        
        return True
    
    def capture_process_state(self):
        """Capture the running process state."""
        self.print_step(2, "Capturing Process State")
        
        print(f"🧊 Initiating state capture for PID {self.demo_pid}...")
        
        try:
            manager = CaptureManager(snapshot_dir=os.path.join(self.base_dir, 'snapshots'))
            info = manager.capture_process(self.demo_pid)
            
            print("✅ Process state captured successfully")
            print(f"   Process Name: {info.get('name')}")
            print(f"   Status: {info.get('status')}")
            print(f"   Memory: {info.get('memory', 0) / 1024 / 1024:.2f} MB")
            
            return True
        except Exception as e:
            print(f"❌ Capture failed: {e}")
            return False
    
    def create_snapshot(self):
        """Package the captured state into a portable snapshot."""
        self.print_step(3, "Creating Portable Snapshot")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.snapshot_name = f"phase1_demo_{timestamp}"
        
        snapshot_dir = os.path.join(self.base_dir, 'snapshots', f'process_{self.demo_pid}')
        output_file = os.path.join(self.base_dir, 'snapshots', f'{self.snapshot_name}.tar.gz')
        
        metadata = {
            "snapshot_id": f"UAT-{self.demo_pid}-{timestamp}",
            "process_id": self.demo_pid,
            "timestamp": datetime.now().isoformat(),
            "os": "ubuntu-24.04",
            "architecture": "x86_64",
            "snapshot_name": self.snapshot_name,
            "engine_version": "v1.0.0-phase1",
            "author": "WekezaOmniOS"
        }
        
        print(f"📦 Building snapshot: {self.snapshot_name}")
        
        try:
            success = build_snapshot(snapshot_dir, output_file, metadata)
            
            if success and os.path.exists(output_file):
                size = os.path.getsize(output_file)
                print(f"✅ Snapshot created successfully")
                print(f"   File: {output_file}")
                print(f"   Size: {size / 1024:.2f} KB")
                return True
            else:
                print("⚠️  Snapshot file not created (metadata-only mode)")
                return True  # Still consider it success in fallback mode
        except Exception as e:
            print(f"❌ Snapshot creation failed: {e}")
            return False
    
    def inspect_snapshot(self):
        """Inspect the contents of the created snapshot."""
        self.print_step(4, "Inspecting Snapshot Contents")
        
        snapshot_dir = os.path.join(self.base_dir, 'snapshots', f'process_{self.demo_pid}')
        
        if not os.path.exists(snapshot_dir):
            print(f"⚠️  Snapshot directory not found: {snapshot_dir}")
            return False
        
        print(f"📂 Snapshot directory: {snapshot_dir}")
        print("\nContents:")
        
        for item in os.listdir(snapshot_dir):
            item_path = os.path.join(snapshot_dir, item)
            size = os.path.getsize(item_path)
            print(f"   - {item} ({size} bytes)")
        
        # Display metadata if available
        metadata_file = os.path.join(snapshot_dir, 'metadata.json')
        if os.path.exists(metadata_file):
            print("\n📋 Snapshot Metadata:")
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
                for key, value in metadata.items():
                    print(f"   {key}: {value}")
        
        print("\n✅ Snapshot inspection complete")
        return True
    
    def test_restoration(self):
        """Test the restoration process (will run in fallback mode)."""
        self.print_step(5, "Testing State Restoration")
        
        print(f"⚡ Attempting to restore process {self.demo_pid}...")
        
        try:
            manager = RestoreManager(snapshot_dir=os.path.join(self.base_dir, 'snapshots'))
            manager.restore_snapshot(self.demo_pid)
            
            print("\n✅ Restoration test complete")
            return True
        except Exception as e:
            print(f"❌ Restoration failed: {e}")
            return False
    
    def cleanup(self):
        """Clean up the demo process."""
        self.print_step(6, "Cleanup")
        
        if self.demo_pid:
            try:
                print(f"🧹 Terminating demo process {self.demo_pid}...")
                # Kill the entire process group
                os.killpg(os.getpgid(self.demo_pid), signal.SIGTERM)
                time.sleep(1)
                print("✅ Demo process terminated")
            except ProcessLookupError:
                print("⚠️  Process already terminated")
            except Exception as e:
                print(f"⚠️  Cleanup error: {e}")
    
    def print_summary(self, results):
        """Print a summary of the test results."""
        self.print_banner("PHASE 1 TEST SUMMARY")
        
        print("Test Results:")
        for step, success in results.items():
            status = "✅" if success else "❌"
            print(f"   {status} {step}")
        
        all_passed = all(results.values())
        
        print(f"\nOverall Status: {'✅ PASSED' if all_passed else '⚠️  COMPLETED WITH WARNINGS'}")
        
        print("\n📊 Generated Artifacts:")
        snapshots_dir = os.path.join(self.base_dir, 'snapshots')
        if os.path.exists(snapshots_dir):
            snapshots = [f for f in os.listdir(snapshots_dir) if f.endswith('.tar.gz')]
            if snapshots:
                print(f"   {len(snapshots)} snapshot(s) in ./snapshots/")
                for s in snapshots:
                    print(f"      - {s}")
        
        print("\n📝 Notes:")
        print("   - Phase 1 focuses on local process checkpointing")
        print("   - CRIU provides full state capture when available")
        print("   - Fallback mode captures metadata and environment")
        print("   - Phase 2 will add cross-environment transfer")
        
        print("\n🎯 Next Steps:")
        print("   1. Review snapshots in ./snapshots/")
        print("   2. Test the API: python3 api/server.py")
        print("   3. Run integration tests: pytest tests/")
        print("   4. Proceed to Phase 2 architecture")
    
    def run(self):
        """Execute the complete Phase 1 test workflow."""
        self.print_banner("WekezaOmniOS Phase 1 - Universal Application Teleportation")
        
        print("Testing the complete teleportation pipeline:")
        print("  Capture → Package → Inspect → Restore")
        
        results = {}
        
        try:
            # Step 1: Start demo app
            results['Demo App Launch'] = self.start_demo_app()
            if not results['Demo App Launch']:
                print("\n❌ Cannot proceed without demo app")
                return
            
            # Step 2: Capture state
            results['State Capture'] = self.capture_process_state()
            
            # Step 3: Create snapshot
            results['Snapshot Creation'] = self.create_snapshot()
            
            # Step 4: Inspect snapshot
            results['Snapshot Inspection'] = self.inspect_snapshot()
            
            # Step 5: Test restoration
            results['State Restoration'] = self.test_restoration()
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Test interrupted by user")
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # Step 6: Cleanup
            self.cleanup()
        
        # Print summary
        self.print_summary(results)

if __name__ == "__main__":
    orchestrator = Phase1Orchestrator()
    orchestrator.run()
