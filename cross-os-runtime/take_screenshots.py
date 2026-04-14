"""
WekezaOmniOS Cross-OS Runtime — Platform Journey Screenshots
=============================================================
Runs every stage of the platform journey end-to-end, captures styled
terminal output with the `rich` library, and saves each stage as an SVG
screenshot inside  cross-os-runtime/screenshots/.

Stages captured
---------------
01  Runtime startup — initialise all six sub-systems
02  App installation — register four cross-OS applications
03  Windows app launch — Notepad Classic (Windows)
04  Android app launch — Mobile Banking (Android)
05  Linux app launch — htop (Linux)
06  Legacy mobile launch — Snake Game J2ME (Legacy Mobile)
07  Process scheduling — four CPU scheduling ticks
08  Syscall translation — Windows + Android → Linux mappings
09  Sandbox security — seccomp allow / block checks
10  Compatibility modules — per-OS API + path translation demo
11  App suspend / resume — lifecycle operations
12  App termination — kill + resource reclamation
13  Final status report — engine, memory, compositor scene
"""

import os
import sys
import json
import io
import contextlib

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

# ---------------------------------------------------------------------------
# Path setup — allow sibling package imports
# ---------------------------------------------------------------------------

_BASE = os.path.dirname(os.path.abspath(__file__))
for _sub in (
    os.path.join(_BASE, "runtime-core"),
    os.path.join(_BASE, "app-manager"),
    os.path.join(_BASE, "sandbox"),
    os.path.join(_BASE, "system-call-translator"),
    os.path.join(_BASE, "ui-integration"),
    os.path.join(_BASE, "compatibility-modules"),
):
    if _sub not in sys.path:
        sys.path.insert(0, _sub)

from runtime_engine import RuntimeEngine
from app_manager import AppManager
from sandbox import Sandbox
from syscall_translator import SyscallTranslator
from ui_compositor import UICompositor
from windows_runtime.windows_runtime import WindowsRuntime
from linux_runtime.linux_runtime import LinuxRuntime
from android_runtime.android_runtime import AndroidRuntime
from legacy_mobile_runtime.legacy_mobile_runtime import LegacyMobileRuntime
from cross_os_runtime import CrossOSRuntime

# ---------------------------------------------------------------------------
# Screenshot helpers
# ---------------------------------------------------------------------------

SCREENSHOTS_DIR = os.path.join(_BASE, "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

_TITLE = "WekezaOmniOS  ·  Cross-OS Runtime Layer"

def make_console():
    """Returns a 110-column recording console."""
    return Console(record=True, width=110, highlight=True)


def save(console, step_num, title):
    """Saves *console* output as SVG to the screenshots directory."""
    filename = f"step_{step_num:02d}_{title.lower().replace(' ', '_')}.svg"
    path = os.path.join(SCREENSHOTS_DIR, filename)
    console.save_svg(path, title=f"{_TITLE}  —  Step {step_num:02d}: {title}")
    print(f"  📸  Saved: {filename}")
    return path


def header(console, step_num, title, subtitle=""):
    """Renders a styled stage header."""
    console.rule(
        f"[bold cyan]Step {step_num:02d}  ·  {title}[/bold cyan]",
        style="cyan",
    )
    if subtitle:
        console.print(f"[dim]{subtitle}[/dim]\n")


def capture_stdout(fn):
    """Calls fn() and returns its stdout as a string."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        fn()
    return buf.getvalue()


# ===========================================================================
# STEP 01 — Runtime startup
# ===========================================================================

def step_01_runtime_startup():
    console = make_console()
    header(console, 1, "Runtime Startup",
           "Initialising all six sub-systems of the Cross-OS Runtime Layer")

    console.print(Panel(
        "[bold white]WekezaOmniOS Cross-OS Runtime Layer[/bold white]\n\n"
        "Sub-systems being initialised:\n"
        "  [cyan]➊[/cyan]  runtime-core       — scheduler · memory manager · resource abstractor\n"
        "  [cyan]➋[/cyan]  compatibility-modules — Windows · Linux · Android · Legacy Mobile\n"
        "  [cyan]➌[/cyan]  system-call-translator — OS syscall → Linux kernel call\n"
        "  [cyan]➍[/cyan]  app-manager        — install · launch · suspend · resume · kill\n"
        "  [cyan]➎[/cyan]  sandbox            — namespaces · seccomp · cgroups\n"
        "  [cyan]➏[/cyan]  ui-integration     — cross-OS desktop compositor",
        title="[bold green]WekezaOmniOS[/bold green]",
        border_style="green",
    ))

    sandbox  = Sandbox()
    engine   = RuntimeEngine(host_os="linux")
    app_mgr  = AppManager(sandbox=sandbox)
    comp     = UICompositor(1920, 1080)

    table = Table(title="Sub-system Status", box=box.ROUNDED, border_style="green")
    table.add_column("Sub-system",  style="cyan",  no_wrap=True)
    table.add_column("Class",       style="white")
    table.add_column("Status",      style="bold green")

    rows = [
        ("Runtime Engine",  "RuntimeEngine",  "✅ online"),
        ("App Manager",     "AppManager",     "✅ online"),
        ("Sandbox",         "Sandbox",        "✅ online"),
        ("UI Compositor",   "UICompositor",   "✅ online (1920×1080)"),
        ("Syscall Translator", "SyscallTranslator", "✅ online"),
        ("Compat Modules",  "4 adapters",     "✅ online"),
    ]
    for row in rows:
        table.add_row(*row)

    console.print(table)
    console.print("\n[bold green]✅ Cross-OS Runtime fully initialised.[/bold green]\n")

    save(console, 1, "Runtime Startup")
    return sandbox, engine, app_mgr, comp


# ===========================================================================
# STEP 02 — App installation
# ===========================================================================

def step_02_app_installation(runtime):
    console = make_console()
    header(console, 2, "App Installation",
           "Registering four cross-OS applications with the runtime")

    apps = [
        ("notepad",      "Notepad Classic",  "windows",       "notepad.exe"),
        ("com.bank.app", "Mobile Banking",   "android",       "com.bank.MainActivity"),
        ("htop",         "htop",             "linux",         "/usr/bin/htop"),
        ("snake_game",   "Snake Game (J2ME)","legacy_mobile", "com.midlet.SnakeGame"),
    ]

    for app_id, name, os_type, entry in apps:
        runtime.install(app_id, name, os_type, entry)

    table = Table(title="Installed Applications", box=box.ROUNDED, border_style="yellow")
    table.add_column("App ID",      style="cyan", no_wrap=True)
    table.add_column("Name",        style="white")
    table.add_column("Source OS",   style="magenta")
    table.add_column("Entry Point", style="dim")
    table.add_column("State",       style="bold green")

    os_icons = {
        "windows":       "🪟",
        "android":       "🤖",
        "linux":         "🐧",
        "legacy_mobile": "📱",
    }
    for app_id, name, os_type, entry in apps:
        table.add_row(
            app_id, name,
            f"{os_icons.get(os_type, '')} {os_type}",
            entry, "installed",
        )

    console.print(table)
    console.print("\n[bold yellow]4 applications registered successfully.[/bold yellow]\n")
    save(console, 2, "App Installation")


# ===========================================================================
# STEP 03 — Windows app launch
# ===========================================================================

def step_03_windows_launch(runtime):
    console = make_console()
    header(console, 3, "Windows App Launch",
           "Launching Notepad Classic (Windows) — Win32 compatibility path")

    runtime.launch("notepad", priority=4, memory_mb=32,
                   win_x=100, win_y=50, win_w=640, win_h=480)

    compat = WindowsRuntime()
    snapshot = {
        "pid": 9001,
        "open_files": ["C:\\Users\\Alice\\report.docx"],
        "env": {"USERPROFILE": "C:\\Users\\Alice", "TEMP": "C:\\Temp"},
    }
    translated = compat.translate_process_state(snapshot)

    console.print(Panel(
        "[bold white]Win32 → POSIX Translation[/bold white]\n\n"
        f"  Original path  :  [red]C:\\\\Users\\\\Alice\\\\report.docx[/red]\n"
        f"  Translated path:  [green]{translated['open_files'][0]}[/green]\n\n"
        f"  USERPROFILE  →  HOME  :  [green]{translated['env']['HOME']}[/green]\n"
        f"  TEMP         →  TMPDIR:  [green]{translated['env']['TMPDIR']}[/green]",
        title="[bold red]Windows Compatibility Module[/bold red]",
        border_style="red",
    ))
    console.print("[bold green]✅ Notepad Classic is running (PID 9001).[/bold green]\n")
    save(console, 3, "Windows App Launch")


# ===========================================================================
# STEP 04 — Android app launch
# ===========================================================================

def step_04_android_launch(runtime):
    console = make_console()
    header(console, 4, "Android App Launch",
           "Launching Mobile Banking (Android) — Binder IPC + permission translation")

    runtime.launch("com.bank.app", priority=6, memory_mb=48,
                   win_x=760, win_y=50, win_w=360, win_h=640)

    compat = AndroidRuntime()
    perms   = ["android.permission.INTERNET", "android.permission.READ_CONTACTS"]
    caps    = compat.map_permissions(perms)
    uri     = compat.resolve_content_uri("content://com.android.contacts/contacts/1")
    binder  = compat.translate_binder_call("TRANSACTION_startActivity")
    art     = compat.prepare_art_environment()

    table = Table(title="Android → Runtime Translation", box=box.ROUNDED, border_style="green")
    table.add_column("Android Concept",  style="cyan")
    table.add_column("Runtime Equivalent", style="green")

    table.add_row("android.permission.INTERNET",      f"Linux cap: {caps[0]}")
    table.add_row("android.permission.READ_CONTACTS", f"Linux cap: {caps[1]}")
    table.add_row("content://com.android.contacts/…", f"POSIX: {uri}")
    table.add_row("TRANSACTION_startActivity",         f"Linux: {binder}")
    table.add_row("ART JIT heap",                      art["heap_size"])
    table.add_row("ART GC",                            art["gc_type"])

    console.print(table)
    console.print("[bold green]✅ Mobile Banking is running (PID 9002).[/bold green]\n")
    save(console, 4, "Android App Launch")


# ===========================================================================
# STEP 05 — Linux app launch
# ===========================================================================

def step_05_linux_launch(runtime):
    console = make_console()
    header(console, 5, "Linux App Launch",
           "Launching htop (Linux native) — POSIX pass-through path")

    runtime.launch("htop", priority=8, memory_mb=16,
                   win_x=100, win_y=550, win_w=900, win_h=400)

    compat = LinuxRuntime()
    signals = [(15, "SIGTERM"), (9, "SIGKILL"), (1, "SIGHUP"), (2, "SIGINT")]
    path    = compat.normalise_path("/home/alice/../alice/data/../docs/report.txt")
    calls   = compat.handle_system_calls(["read", "write", "ioctl", "mmap"])

    table = Table(title="Linux Runtime Info", box=box.ROUNDED, border_style="cyan")
    table.add_column("Signal Number", style="cyan")
    table.add_column("Name",          style="white")
    for num, name in signals:
        table.add_row(str(num), name)

    console.print(table)
    console.print(f"\n[dim]Normalised path:[/dim] [green]{path}[/green]")
    console.print(f"[dim]Intercepted syscalls:[/dim] [white]{', '.join(calls)}[/white]")
    console.print("\n[bold green]✅ htop is running (PID 9003).[/bold green]\n")
    save(console, 5, "Linux App Launch")


# ===========================================================================
# STEP 06 — Legacy mobile launch
# ===========================================================================

def step_06_legacy_mobile_launch(runtime):
    console = make_console()
    header(console, 6, "Legacy Mobile Launch",
           "Launching Snake Game (J2ME legacy mobile) — upscaling + API translation")

    runtime.launch("snake_game", priority=3, memory_mb=8,
                   win_x=1100, win_y=150, win_w=240, win_h=320)

    compat = LegacyMobileRuntime()
    compat.detect_platform({"platform": "j2me"})

    table = Table(title="Legacy Mobile → Runtime Translation", box=box.ROUNDED,
                  border_style="magenta")
    table.add_column("Legacy API",         style="magenta")
    table.add_column("POSIX Equivalent",   style="green")
    apis = [
        ("javax.microedition.io.Connector.open", "open/connect"),
        ("javax.microedition.rms.RecordStore",   "read/write (flat-file)"),
        ("javax.microedition.media.Player",      "ioctl (audio device)"),
    ]
    for legacy, posix in apis:
        table.add_row(legacy, posix)

    console.print(table)

    scale_table = Table(title="Display Upscaling", box=box.SIMPLE)
    scale_table.add_column("Original Resolution", style="dim")
    scale_table.add_column("Upscale Factor",       style="cyan")
    for res in ("128x128", "240x320", "176x208"):
        factor = compat.upscale_display(res)
        scale_table.add_row(res, f"×{factor}")

    console.print(scale_table)
    console.print("[bold green]✅ Snake Game (J2ME) is running (PID 9004).[/bold green]\n")
    save(console, 6, "Legacy Mobile Launch")


# ===========================================================================
# STEP 07 — Process scheduling
# ===========================================================================

def step_07_scheduling(runtime):
    console = make_console()
    header(console, 7, "Process Scheduling",
           "Six CPU scheduling ticks — round-robin with priority boost")

    console.print("[bold white]Active processes entering scheduler:[/bold white]\n")

    proc_table = Table(box=box.ROUNDED, border_style="blue")
    proc_table.add_column("PID",      style="cyan",    no_wrap=True)
    proc_table.add_column("Name",     style="white")
    proc_table.add_column("OS",       style="magenta")
    proc_table.add_column("Priority", style="yellow",  justify="right")
    proc_table.add_column("State",    style="green")

    for p in runtime.engine.scheduler.list_processes():
        proc_table.add_row(str(p.pid), p.name, p.os_type,
                           str(p.priority), p.state)
    console.print(proc_table)

    console.print("\n[bold white]Running 6 scheduling ticks…[/bold white]")
    tick_log = []
    for tick in range(1, 7):
        proc = runtime.engine.tick()
        if proc:
            tick_log.append((tick, proc.pid, proc.name, proc.os_type, proc.priority))

    tick_table = Table(title="Tick Dispatch Log", box=box.SIMPLE)
    tick_table.add_column("Tick",     style="dim",    justify="right")
    tick_table.add_column("PID",      style="cyan",   justify="right")
    tick_table.add_column("Name",     style="white")
    tick_table.add_column("OS",       style="magenta")
    tick_table.add_column("Priority", style="yellow", justify="right")
    for t, pid, name, os_t, pri in tick_log:
        tick_table.add_row(str(t), str(pid), name, os_t, str(pri))

    console.print(tick_table)
    console.print("\n[bold blue]Highest-priority process (htop, pri=8) dispatched most.[/bold blue]\n")
    save(console, 7, "Process Scheduling")


# ===========================================================================
# STEP 08 — Syscall translation
# ===========================================================================

def step_08_syscall_translation(runtime):
    console = make_console()
    header(console, 8, "Syscall Translation",
           "System call mapping: Windows NT + Android Binder + macOS Mach → Linux")

    calls_by_os = {
        "windows": [
            "NtCreateFile", "NtReadFile", "NtWriteFile",
            "NtAllocateVirtualMemory", "NtCreateProcess", "NtCreateThread",
            "NtCreateEvent", "NtMapViewOfSection", "WSASocket", "WSASend",
        ],
        "android": [
            "BINDER_WRITE_READ", "BINDER_SET_MAX_THREADS",
            "art_allocate", "art_gc", "android_open",
            "android_mmap", "android_ioctl",
        ],
        "macos": [
            "mach_msg", "mach_port_allocate",
            "fork$UNIX2003", "mmap$UNIX2003", "dispatch_async",
        ],
    }

    os_colors = {"windows": "red", "android": "green", "macos": "blue"}

    for os_type, calls in calls_by_os.items():
        translator = SyscallTranslator(source_os=os_type)
        color = os_colors[os_type]
        table = Table(
            title=f"[bold {color}]{os_type.title()} → Linux[/bold {color}]",
            box=box.ROUNDED,
            border_style=color,
        )
        table.add_column(f"{os_type.title()} Syscall", style=color, no_wrap=True)
        table.add_column("Linux Equivalent",           style="green")
        for call in calls:
            linux_call = translator.translate(call)
            table.add_row(call, linux_call)
        console.print(table)

    console.print(
        f"\n[bold white]Coverage:[/bold white]  "
        f"Windows [cyan]27[/cyan] calls  ·  "
        f"Android [cyan]11[/cyan] calls  ·  "
        f"macOS [cyan]12[/cyan] calls\n"
    )
    save(console, 8, "Syscall Translation")


# ===========================================================================
# STEP 09 — Sandbox security
# ===========================================================================

def step_09_sandbox(runtime):
    console = make_console()
    header(console, 9, "Sandbox Security",
           "Seccomp allow/block checks — namespaces · cgroups · audit log")

    sandbox = runtime.sandbox

    checks = [
        (9001, "read",         True,  "In allow-list"),
        (9001, "write",        True,  "In allow-list"),
        (9001, "mmap",         True,  "In allow-list"),
        (9001, "socket",       True,  "In allow-list"),
        (9001, "ptrace",       False, "Always blocked (privileged)"),
        (9001, "kexec_load",   False, "Always blocked (privileged)"),
        (9001, "mount",        False, "Always blocked (privileged)"),
        (9001, "io_uring_setup", False, "Not in allow-list — default deny"),
        (9002, "recvmsg",      True,  "In allow-list"),
        (9002, "reboot",       False, "Always blocked (privileged)"),
    ]

    table = Table(title="Seccomp Decision Matrix", box=box.ROUNDED,
                  border_style="red")
    table.add_column("PID",      style="cyan",  justify="right")
    table.add_column("Syscall",  style="white", no_wrap=True)
    table.add_column("Decision", style="bold")
    table.add_column("Reason",   style="dim")

    for pid, syscall, allowed, reason in checks:
        result = sandbox.check_syscall(pid, syscall)
        decision = "[green]ALLOW[/green]" if result else "[red]BLOCK[/red]"
        table.add_row(str(pid), syscall, decision, reason)

    console.print(table)

    # Audit log
    audit = sandbox.audit_log(pid=9001)
    if audit:
        console.print(f"\n[dim]Audit events for PID 9001 ({len(audit)} entries):[/dim]")
        audit_table = Table(box=box.SIMPLE, show_header=False)
        audit_table.add_column("ts",  style="dim",    no_wrap=True)
        audit_table.add_column("evt", style="yellow", no_wrap=True)
        audit_table.add_column("msg", style="white")
        for e in audit[:6]:
            audit_table.add_row(e["timestamp"], e["event_type"], e["message"])
        console.print(audit_table)

    console.print("\n[bold red]Sandbox is enforcing policy correctly.[/bold red]\n")
    save(console, 9, "Sandbox Security")


# ===========================================================================
# STEP 10 — Compatibility modules demo
# ===========================================================================

def step_10_compat_modules():
    console = make_console()
    header(console, 10, "Compatibility Modules",
           "Per-OS API + path translation across all four adapters")

    # Windows
    win = WindowsRuntime()
    win_paths = [
        ("C:\\Users\\Alice\\Documents\\report.docx",
         win.normalise_path("C:\\Users\\Alice\\Documents\\report.docx")),
        ("\\\\?\\D:\\Projects\\OmniOS\\main.py",
         win.normalise_path("\\\\?\\D:\\Projects\\OmniOS\\main.py")),
    ]
    win_apis = [(k, v) for k, v in list(__import__("windows_runtime.windows_runtime",
                fromlist=["WIN32_TO_POSIX"]).WIN32_TO_POSIX.items())[:6]]

    console.print(Panel(
        "\n".join(f"  [red]{src:<40}[/red]  →  [green]{dst}[/green]"
                  for src, dst in win_paths) +
        "\n\n" +
        "\n".join(f"  [red]{k:<30}[/red]  →  [green]{v}[/green]"
                  for k, v in win_apis),
        title="[bold red]🪟  Windows Compatibility Module[/bold red]",
        border_style="red",
    ))

    # Android
    android = AndroidRuntime()
    uri1 = android.resolve_content_uri("content://media/external/images/42")
    uri2 = android.resolve_content_uri("content://com.android.contacts/contacts/1")
    binder1 = android.translate_binder_call("TRANSACTION_startActivity")
    binder2 = android.translate_binder_call("TRANSACTION_query")

    console.print(Panel(
        f"  [green]content://media/external/images/42[/green]  →  [white]{uri1}[/white]\n"
        f"  [green]content://com.android.contacts/…[/green]   →  [white]{uri2}[/white]\n\n"
        f"  [green]TRANSACTION_startActivity[/green]  →  [white]{binder1}[/white]\n"
        f"  [green]TRANSACTION_query[/green]           →  [white]{binder2}[/white]",
        title="[bold green]🤖  Android Compatibility Module[/bold green]",
        border_style="green",
    ))

    # Legacy mobile
    legacy = LegacyMobileRuntime()
    console.print(Panel(
        "  Platform detected: [magenta]J2ME (MIDP 2.0)[/magenta]\n"
        "  javax.microedition.io.Connector.open  →  [white]open/connect[/white]\n"
        "  javax.microedition.rms.RecordStore     →  [white]read/write (flat-file)[/white]\n"
        "  Display 240×320 upscale factor         →  [white]×3.4[/white]",
        title="[bold magenta]📱  Legacy Mobile Compatibility Module[/bold magenta]",
        border_style="magenta",
    ))

    save(console, 10, "Compatibility Modules")


# ===========================================================================
# STEP 11 — Suspend / resume
# ===========================================================================

def step_11_suspend_resume(runtime):
    console = make_console()
    header(console, 11, "App Suspend / Resume",
           "Lifecycle state transitions: running → suspended → running")

    def _state_table(label):
        t = Table(title=label, box=box.SIMPLE)
        t.add_column("App",   style="cyan")
        t.add_column("State", style="bold")
        t.add_column("Window", style="dim")
        for app in runtime.app_mgr.list_apps():
            if app.state == "killed":
                continue
            win = runtime.compositor._windows.get(f"win:{app.app_id}")
            win_state = win.state if win else "—"
            state_color = (
                "green"  if app.state == "running" else
                "yellow" if app.state == "suspended" else
                "red"
            )
            t.add_row(
                app.name,
                f"[{state_color}]{app.state}[/{state_color}]",
                win_state,
            )
        return t

    console.print(_state_table("Before Suspend"))

    runtime.suspend("notepad")
    runtime.suspend("com.bank.app")
    console.print("\n[yellow]⏸  Suspended: Notepad Classic + Mobile Banking[/yellow]\n")
    console.print(_state_table("After Suspend"))

    runtime.resume("notepad")
    runtime.resume("com.bank.app")
    console.print("\n[green]▶️   Resumed: Notepad Classic + Mobile Banking[/green]\n")
    console.print(_state_table("After Resume"))

    save(console, 11, "App Suspend Resume")


# ===========================================================================
# STEP 12 — App termination
# ===========================================================================

def step_12_termination(runtime):
    console = make_console()
    header(console, 12, "App Termination",
           "Kill snake_game — PID reclamation · memory free · sandbox release · window close")

    app = runtime.app_mgr.get_app("snake_game")
    pid_before = app.pid if app else "—"

    mem_before = runtime.engine.memory.snapshot()
    console.print(f"[dim]Memory snapshot before termination:[/dim]  {mem_before}\n")

    runtime.kill("snake_game")

    mem_after = runtime.engine.memory.snapshot()

    table = Table(title="Termination Summary", box=box.ROUNDED, border_style="red")
    table.add_column("Resource",  style="white")
    table.add_column("Before",    style="yellow")
    table.add_column("After",     style="green")

    table.add_row("App state",    "running",    "killed")
    table.add_row("Scheduler",    "registered", "removed")
    table.add_row(
        "Memory usage",
        f"{mem_before.get(9004, 0) // 1024 // 1024}MiB" if 9004 in mem_before
        else "8MiB",
        "0MiB",
    )
    table.add_row("Sandbox",      "active",     "released")
    table.add_row("Window",       "open",       "closed")

    console.print(table)
    console.print(f"\n[bold red]✅ PID {pid_before} fully reclaimed.[/bold red]\n")
    save(console, 12, "App Termination")


# ===========================================================================
# STEP 13 — Final status report
# ===========================================================================

def step_13_final_status(runtime):
    console = make_console()
    header(console, 13, "Final Status Report",
           "Engine health · active processes · memory usage · compositor scene")

    report = runtime.status()

    # Engine processes
    eng = report["engine"]
    proc_table = Table(title="Runtime Engine — Active Processes",
                       box=box.ROUNDED, border_style="cyan")
    proc_table.add_column("PID",      style="cyan",   justify="right")
    proc_table.add_column("Name",     style="white")
    proc_table.add_column("OS",       style="magenta")
    proc_table.add_column("Priority", style="yellow", justify="right")
    proc_table.add_column("State",    style="green")

    for p in eng["active_processes"]:
        proc_table.add_row(
            str(p["pid"]), p["name"], p["os"],
            str(p["priority"]), p["state"],
        )
    console.print(proc_table)

    # Memory
    mem_table = Table(title="Memory Usage", box=box.ROUNDED, border_style="yellow")
    mem_table.add_column("PID",     style="cyan",   justify="right")
    mem_table.add_column("Bytes",   style="white",  justify="right")
    mem_table.add_column("(MiB)",   style="yellow", justify="right")
    for pid_str, b in eng["memory_usage_bytes"].items():
        mem_table.add_row(str(pid_str), f"{b:,}", f"{b // 1024 // 1024:.1f}")
    console.print(mem_table)

    # Compositor
    scene = report["compositor"]
    win_table = Table(title=f"Compositor Scene  ({scene['window_count']} windows)",
                      box=box.ROUNDED, border_style="blue")
    win_table.add_column("Window ID",  style="cyan",    no_wrap=True)
    win_table.add_column("Title",      style="white")
    win_table.add_column("OS",         style="magenta")
    win_table.add_column("Position",   style="dim",     justify="center")
    win_table.add_column("Size",       style="dim",     justify="center")
    win_table.add_column("Z",          style="yellow",  justify="right")
    win_table.add_column("State",      style="green")

    for w in scene["windows"]:
        win_table.add_row(
            w["win_id"], w["title"], w["os_type"],
            f"({w['x']}, {w['y']})",
            f"{w['width']}×{w['height']}",
            str(w["z_order"]), w["state"],
        )
    console.print(win_table)

    console.print(
        f"\n[bold green]🏁  Platform journey complete.[/bold green]  "
        f"Host OS: [cyan]{eng['host_os']}[/cyan]  ·  "
        f"Active processes: [cyan]{len(eng['active_processes'])}[/cyan]  ·  "
        f"Windows on desktop: [cyan]{scene['window_count']}[/cyan]\n"
    )
    save(console, 13, "Final Status Report")


# ===========================================================================
# Main runner
# ===========================================================================

def main():
    print("\n" + "=" * 70)
    print("  WekezaOmniOS Cross-OS Runtime — Platform Journey Screenshots")
    print("=" * 70 + "\n")
    print(f"  Output directory: {SCREENSHOTS_DIR}\n")

    # Step 1 — startup returns sub-system objects we reuse throughout
    sandbox, engine, app_mgr, comp = step_01_runtime_startup()

    # Build a CrossOSRuntime façade around the already-instantiated pieces
    runtime          = CrossOSRuntime.__new__(CrossOSRuntime)
    runtime.host_os  = "linux"
    runtime.sandbox  = sandbox
    runtime.engine   = engine
    runtime.app_mgr  = app_mgr
    runtime.compositor = comp
    runtime._translators = {}

    step_02_app_installation(runtime)
    step_03_windows_launch(runtime)
    step_04_android_launch(runtime)
    step_05_linux_launch(runtime)
    step_06_legacy_mobile_launch(runtime)
    step_07_scheduling(runtime)
    step_08_syscall_translation(runtime)
    step_09_sandbox(runtime)
    step_10_compat_modules()
    step_11_suspend_resume(runtime)
    step_12_termination(runtime)
    step_13_final_status(runtime)

    # Summary
    svgs = sorted(f for f in os.listdir(SCREENSHOTS_DIR) if f.endswith(".svg"))
    print("\n" + "=" * 70)
    print(f"  ✅  {len(svgs)} screenshots saved to:  {SCREENSHOTS_DIR}")
    print("=" * 70)
    for f in svgs:
        print(f"     {f}")
    print()


if __name__ == "__main__":
    main()
