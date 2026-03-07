"""
WekezaOmniOS: Universal Application Teleportation Console
Phase 1: Integrated Dashboard for Process Discovery & Migration.
"""

import os
import time
import sys

# Adding parent directory to path to allow future integration with engine modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def clear_screen():
    """Clears the terminal screen for a clean UI experience."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_running_demos():
    """
    Dynamic Discovery: Reads PIDs from the temp directory.
    This ensures the UI is always synced with scripts/run_demo.sh.
    """
    apps = []
    temp_dir = "temp"
    if os.path.exists(temp_dir):
        for file in os.listdir(temp_dir):
            if file.endswith(".pid"):
                try:
                    with open(os.path.join(temp_dir, file), "r") as f:
                        pid = f.read().strip()
                        # Verify PID is a number before adding
                        if pid.isdigit():
                            apps.append({"name": file.replace(".pid", ""), "pid": pid})
                except Exception as e:
                    print(f"[UI Error] Could not read {file}: {e}")
    return apps

def display_header():
    """Main dashboard branding."""
    print("="*60)
    print("      WekezaOmniOS: UNIVERSAL TELEPORTATION DASHBOARD      ")
    print("="*60)
    print(f" Status: PHASE 1 BOOTSTRAP | Node: Nairobi-Local-01")
    print("-" * 60)

def main_menu():
    """Primary navigation loop."""
    while True:
        clear_screen()
        display_header()
        
        apps = get_running_demos()
        
        if not apps:
            print("\n[!] ALERT: No active demo processes detected.")
            print("    Please run 'bash scripts/run_demo.sh' in another terminal.")
            print("\n1. Refresh Dashboard")
            print("2. Exit")
        else:
            print("ACTIVE TELEPORTATION TARGETS:")
            for i, app in enumerate(apps):
                print(f" {i + 1}. {app['name'].upper():<15} [PID: {app['pid']}]")
            print(f" {len(apps) + 1}. Exit")

        try:
            choice_raw = input("\nSelection > ")
            if not choice_raw: continue
            
            choice = int(choice_raw)
            
            # Handle Exit
            max_choice = len(apps) + 1 if apps else 2
            if choice == max_choice:
                print("\n[UI] Shutting down WekezaOmniOS Console...")
                break
            
            # Refresh if no apps found
            if not apps and choice == 1:
                continue
                
            # Select App
            if apps and 1 <= choice <= len(apps):
                target_menu(apps[choice - 1])
            else:
                print("Invalid selection. Try again.")
                time.sleep(1)
                
        except (ValueError, IndexError):
            print("Invalid input. Please enter a number.")
            time.sleep(1)

def target_menu(app):
    """Destination selection and teleportation sequence."""
    clear_screen()
    display_header()
    print(f"TARGET SELECTED: {app['name'].upper()} (PID: {app['pid']})")
    print("-" * 60)
    
    print("CHOOSE DESTINATION NODE / OS:")
    targets = [
        "Windows Node (NTFS Adapter)", 
        "Ubuntu Node (POSIX Adapter)", 
        "Android Mobile (ART Adapter)", 
        "Apple Mac/iPhone (Darwin Adapter)",
        "Cloud Cluster (Distributed Node)"
    ]
    
    for i, t in enumerate(targets):
        print(f" {i + 1}. {t}")
    
    try:
        choice = int(input("\nTeleport To > "))
        target_env = targets[choice - 1]
        
        # --- TELEPORTATION ENGINE SEQUENCE (PHASE 1 MOCK) ---
        print(f"\n[UI] 🧊 Initializing State Capture...")
        time.sleep(0.8)
        print(f"[UI] 💾 Memory Dump generated for PID {app['pid']}...")
        time.sleep(1)
        print(f"[UI] 📦 Snapshot Engine: Packaging process metadata...")
        time.sleep(1)
        print(f"[UI] 🚀 COMPRESSION: Creating {app['name']}_snapshot.tar.gz...")
        time.sleep(1.2)
        print(f"[UI] 📡 TRANSFER: Moving state to {target_env}...")
        time.sleep(2)
        print(f"\n✅ SUCCESS: {app['name'].upper()} is now RESUMED on {target_env}!")
        # ----------------------------------------------------
        
        input("\nPress Enter to return to Dashboard...")
    except (ValueError, IndexError):
        print("Invalid target selected.")
        time.sleep(1)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n[UI] Emergency Stop: Dashboard closed.")
        sys.exit(0)
