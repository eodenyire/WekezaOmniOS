Perfect! Now we’re at the **`ui-controls/` folder**, which is one of the **main user-facing modules** for Phase 1. Even if the teleportation engine is local and mostly mock at this stage, the **UI controls module defines how developers will interact visually** with teleportation commands.

This is critical because it **bridges the CLI/API engine with future GUI-based control**.

---

# 📁 Folder: `ui-controls/`

Purpose:

* Provide a **user interface layer** for interacting with teleportation
* Allow developers to **select a process and teleport it** to another environment
* Phase 1 can **simulate UI controls** while preparing for full GUI in later phases
* Integrates with CLI/API underneath

Responsibilities:

* Display apps/processes in a selectable list
* Provide **right-click “Teleport To” menu**
* Trigger teleportation commands (`capture`, `snapshot`, `restore`)
* Log user actions

---

# 📄 `README.md`

```md id="oiw4ds"
# WekezaOmniOS UI Controls

This module provides the UI layer for interacting with the Universal Application Teleportation (UAT) engine.

## Features

- Display running processes or demo apps
- Right-click menu: `Teleport To → Windows | Ubuntu | Android | Cloud Node`
- Call CLI/API endpoints to perform teleportation
- Phase 1: Mock UI using console or basic Python GUI
- Phase 2: Full cross-OS desktop UI integration

## Usage

### Right-Click Teleport

1. Select the process/app from UI list
2. Right-click → "Teleport To"
3. Choose target OS or node
4. System triggers teleportation through CLI/API
```

---

# 📄 `ui.py` (Phase 1 mock GUI)

* For Phase 1, we can **simulate UI with a console menu**. Later, this can evolve to **PyQt5 / Tkinter / Web-based GUI**.

```python
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
```

---

# 🔗 Integration Plan

```text
UI → CLI commands → state-capture / snapshot-engine / state-reconstruction
```

* Phase 1: UI triggers **mock CLI functions**
* Phase 2: UI triggers **API calls** → cluster nodes → real teleportation
* Logs actions to `logs/teleport.log`

---

# 📂 Final `ui-controls/` Folder Structure

```text
ui-controls/
    README.md
    ui.py
```

---

✅ **Next Step:**

Once UI controls are done, we can move to the **core teleportation logic**:

```text
state-capture/
```

This is where **the real process checkpointing starts** with **CRIU or mock engines**, which Phase 1 will integrate with CLI, API, and demo apps.

Do you want me to design `state-capture/` next?
