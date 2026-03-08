#!/usr/bin/env python3
"""
WekezaOmniOS Phase 1 - Quick Start Guide
Interactive guide to test the Universal Application Teleportation system.
"""

import os
import sys
import subprocess

def print_header():
    print("\n" + "=" * 70)
    print("  WekezaOmniOS - Universal Application Teleportation")
    print("  Phase 1: Local Process Checkpointing")
    print("=" * 70 + "\n")

def print_menu():
    print("\n📋 Available Tests:\n")
    print("  1. 🏥 Check System Status")
    print("  2. 🚀 Run Complete Phase 1 Demo (Automated)")
    print("  3. 🎯 Start Demo Application")
    print("  4. 🧊 Test Manual Capture")
    print("  5. 📦 Test Snapshot Creation")
    print("  6. ⚡ Test Restoration")
    print("  7. 🌐 Start API Server")
    print("  8. 🧪 Run Unit Tests")
    print("  9. 📚 View Documentation")
    print("  0. 🚪 Exit")
    print()

def check_status():
    """Check system status."""
    print("\n🏥 Checking System Status...\n")
    subprocess.run([sys.executable, "cli/teleport.py", "status"])
    input("\nPress Enter to continue...")

def run_full_demo():
    """Run the complete automated demo."""
    print("\n🚀 Starting Complete Phase 1 Demo...\n")
    print("This will:")
    print("  1. Start a demo application")
    print("  2. Capture its state")
    print("  3. Create a snapshot")
    print("  4. Test restoration")
    print("  5. Clean up")
    print()
    
    confirm = input("Continue? (y/n): ")
    if confirm.lower() == 'y':
        subprocess.run([sys.executable, "scripts/orchestrate_phase1.py"])
    input("\nPress Enter to continue...")

def start_demo_app():
    """Start the demo application."""
    print("\n🎯 Starting Demo Application...\n")
    print("The demo app will run in the background.")
    print("Its PID will be saved to temp/demo_app.pid")
    print()
    
    subprocess.run(["bash", "scripts/run_demo.sh"])
    
    if os.path.exists("temp/demo_app.pid"):
        with open("temp/demo_app.pid", "r") as f:
            pid = f.read().strip()
        print(f"\n✅ Demo app running with PID: {pid}")
        print("Use this PID for capture/snapshot tests")
    
    input("\nPress Enter to continue...")

def test_capture():
    """Test manual process capture."""
    print("\n🧊 Test Process Capture\n")
    
    pid = input("Enter PID to capture (or press Enter to use demo app PID): ")
    
    if not pid and os.path.exists("temp/demo_app.pid"):
        with open("temp/demo_app.pid", "r") as f:
            pid = f.read().strip()
        print(f"Using demo app PID: {pid}")
    
    if pid:
        subprocess.run([sys.executable, "cli/teleport.py", "capture", pid])
    else:
        print("❌ No PID provided")
    
    input("\nPress Enter to continue...")

def test_snapshot():
    """Test snapshot creation."""
    print("\n📦 Test Snapshot Creation\n")
    
    pid = input("Enter PID to snapshot (or press Enter to use demo app PID): ")
    
    if not pid and os.path.exists("temp/demo_app.pid"):
        with open("temp/demo_app.pid", "r") as f:
            pid = f.read().strip()
        print(f"Using demo app PID: {pid}")
    
    if pid:
        snapshot_name = input("Enter snapshot name (or press Enter for default): ")
        
        if snapshot_name:
            subprocess.run([sys.executable, "cli/teleport.py", "snapshot", pid, snapshot_name])
        else:
            subprocess.run([sys.executable, "cli/teleport.py", "snapshot", pid])
    else:
        print("❌ No PID provided")
    
    input("\nPress Enter to continue...")

def test_restore():
    """Test process restoration."""
    print("\n⚡ Test Process Restoration\n")
    
    pid = input("Enter PID to restore (or press Enter to use demo app PID): ")
    
    if not pid and os.path.exists("temp/demo_app.pid"):
        with open("temp/demo_app.pid", "r") as f:
            pid = f.read().strip()
        print(f"Using demo app PID: {pid}")
    
    if pid:
        subprocess.run([sys.executable, "cli/teleport.py", "restore", pid])
    else:
        print("❌ No PID provided")
    
    input("\nPress Enter to continue...")

def start_api():
    """Start the API server."""
    print("\n🌐 Starting API Server...\n")
    print("The API will be available at: http://localhost:8000")
    print("API docs at: http://localhost:8000/docs")
    print()
    print("Press Ctrl+C to stop the server\n")
    
    try:
        subprocess.run([sys.executable, "api/server.py"])
    except KeyboardInterrupt:
        print("\n\nAPI server stopped")
    
    input("\nPress Enter to continue...")

def run_tests():
    """Run unit tests."""
    print("\n🧪 Running Unit Tests...\n")
    
    if os.path.exists("tests"):
        subprocess.run(["pytest", "tests/", "-v"])
    else:
        print("⚠️  Test directory not found")
    
    input("\nPress Enter to continue...")

def view_docs():
    """View documentation."""
    print("\n📚 Documentation\n")
    print("=" * 70)
    
    docs = [
        ("README.md", "Main project overview"),
        ("PHASE1_PROGRESS.md", "Phase 1 progress tracker"),
        ("docs/phase1_design.md", "Phase 1 design document"),
        ("docs/architecture.md", "System architecture"),
        ("EngineeringRules.md", "Engineering guidelines"),
    ]
    
    print("\nAvailable Documentation:")
    for doc, desc in docs:
        exists = "✅" if os.path.exists(doc) else "❌"
        print(f"  {exists} {doc} - {desc}")
    
    print("\n" + "=" * 70)
    
    doc_file = input("\nEnter filename to view (or press Enter to skip): ")
    
    if doc_file and os.path.exists(doc_file):
        with open(doc_file, 'r') as f:
            print("\n" + "─" * 70 + "\n")
            print(f.read())
            print("\n" + "─" * 70)
    
    input("\nPress Enter to continue...")

def main():
    """Main menu loop."""
    # Change to project directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    os.chdir(project_dir)
    
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        print_header()
        print_menu()
        
        choice = input("Select an option (0-9): ").strip()
        
        if choice == '1':
            check_status()
        elif choice == '2':
            run_full_demo()
        elif choice == '3':
            start_demo_app()
        elif choice == '4':
            test_capture()
        elif choice == '5':
            test_snapshot()
        elif choice == '6':
            test_restore()
        elif choice == '7':
            start_api()
        elif choice == '8':
            run_tests()
        elif choice == '9':
            view_docs()
        elif choice == '0':
            print("\n👋 Goodbye!\n")
            break
        else:
            print("\n❌ Invalid option. Please try again.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!\n")
