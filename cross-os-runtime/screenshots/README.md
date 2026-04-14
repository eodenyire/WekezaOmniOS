# Cross-OS Runtime — Platform Journey Screenshots

This folder contains SVG screenshots captured from a live end-to-end run of
the **WekezaOmniOS Cross-OS Runtime Layer**.  Each file documents one stage
of the platform journey.  Open any `.svg` file in a browser to view the
styled terminal output.

## How screenshots were generated

```
cd cross-os-runtime/
python take_screenshots.py
```

`take_screenshots.py` runs every stage of the journey, captures styled terminal
output with the `rich` library, and exports each stage as a self-contained SVG.

---

## Journey Stages

| File | Stage | What it shows |
|------|-------|---------------|
| `step_01_runtime_startup.svg` | **Runtime Startup** | All six sub-systems initialising (RuntimeEngine, AppManager, Sandbox, UICompositor, SyscallTranslator, compat modules) |
| `step_02_app_installation.svg` | **App Installation** | Four cross-OS apps registered: Windows, Android, Linux, Legacy Mobile |
| `step_03_windows_app_launch.svg` | **Windows App Launch** | Notepad Classic launched; Win32 → POSIX path + env translation shown |
| `step_04_android_app_launch.svg` | **Android App Launch** | Mobile Banking launched; Binder IPC, permissions → capabilities, Content URI resolution |
| `step_05_linux_app_launch.svg` | **Linux App Launch** | htop launched; POSIX pass-through, signal number mapping, syscall interception |
| `step_06_legacy_mobile_launch.svg` | **Legacy Mobile Launch** | Snake Game (J2ME) launched; API translation + display upscaling |
| `step_07_process_scheduling.svg` | **Process Scheduling** | Six CPU scheduling ticks with round-robin + priority boost; htop (pri=8) wins |
| `step_08_syscall_translation.svg` | **Syscall Translation** | Windows NT, Android Binder, and macOS Mach calls mapped to Linux equivalents |
| `step_09_sandbox_security.svg` | **Sandbox Security** | Seccomp decision matrix: ALLOW/BLOCK per syscall; audit log entries |
| `step_10_compatibility_modules.svg` | **Compatibility Modules** | Side-by-side demo of all four OS adapters: Windows, Android, Linux, Legacy Mobile |
| `step_11_app_suspend_resume.svg` | **App Suspend / Resume** | State table before suspend, after suspend, and after resume |
| `step_12_app_termination.svg` | **App Termination** | Snake Game killed; PID, memory, sandbox, and window reclaimed |
| `step_13_final_status_report.svg` | **Final Status Report** | Engine health, memory usage per PID, and compositor scene with 3 active windows |

---

## Architecture reminder

```
CrossOSRuntime
    ├── RuntimeEngine  ──→  ProcessScheduler + MemoryManager + ResourceAbstractor
    ├── AppManager     ──→  install / launch / suspend / resume / kill
    ├── Sandbox        ──→  namespaces · seccomp · cgroups · audit
    ├── UICompositor   ──→  cross-OS window Z-ordering + scene rendering
    ├── SyscallTranslator ─→ Windows/Android/macOS → Linux
    └── Compatibility Modules
            ├── WindowsRuntime
            ├── LinuxRuntime
            ├── AndroidRuntime
            └── LegacyMobileRuntime
```
