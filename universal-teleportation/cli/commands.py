def execute_command(command, args):
    if command == "capture":
        pid = args[0]
        print(f"[CLI] Capturing process {pid}")
    elif command == "snapshot":
        pid = args[0]
        snapshot_name = args[1] if len(args) > 1 else f"snapshot_{pid}"
        print(f"[CLI] Creating snapshot '{snapshot_name}' for process {pid}")
    elif command == "restore":
        snapshot_name = args[0]
        print(f"[CLI] Restoring process from snapshot '{snapshot_name}'")
    else:
        print(f"Unknown command '{command}'")
