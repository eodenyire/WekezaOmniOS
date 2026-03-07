import time

def list_apps():
    # Demo apps for Phase 1
    apps = ["demo_app.py", "demo_server.py"]
    print("Running apps:")
    for i, app in enumerate(apps):
        print(f"{i + 1}. {app}")
    return apps

def select_app(apps):
    choice = int(input("Select app to teleport: ")) - 1
    return apps[choice]

def teleport_menu(app_name):
    targets = ["Windows", "Ubuntu", "Android", "Cloud Node"]
    print(f"Teleporting '{app_name}' → Select target environment:")
    for i, target in enumerate(targets):
        print(f"{i + 1}. {target}")
    choice = int(input("Select target: ")) - 1
    target_env = targets[choice]
    print(f"[UI] Teleporting '{app_name}' to {target_env}...")
    # Phase 1: Mock call; later: integrate CLI/API
    time.sleep(1)
    print(f"[UI] Teleport complete (mock)")

def main():
    apps = list_apps()
    app_name = select_app(apps)
    teleport_menu(app_name)

if __name__ == "__main__":
    main()
