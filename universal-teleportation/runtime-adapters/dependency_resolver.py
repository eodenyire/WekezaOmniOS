"""
WekezaOmniOS Dependency Resolver
Phase 3: Resolves runtime dependencies for container and process teleportation.
"""


class DependencyResolver:
    """
    Inspects a snapshot and identifies the runtime dependencies required
    to restore the workload on a target node.
    """

    def __init__(self):
        self.resolved = {}

    def resolve(self, snapshot_metadata: dict) -> dict:
        """
        Analyse snapshot metadata and return a dependency manifest.

        Args:
            snapshot_metadata: dict loaded from a snapshot's metadata.json

        Returns:
            dict with keys 'libraries', 'environment', 'runtime'
        """
        target_os = snapshot_metadata.get("target_os", "linux")
        dependencies = {
            "runtime": snapshot_metadata.get("runtime", "python3"),
            "libraries": snapshot_metadata.get("dependencies", []),
            "environment": snapshot_metadata.get("env_vars", {}),
            "target_os": target_os,
        }
        self.resolved = dependencies
        print(f"[DependencyResolver] Resolved {len(dependencies['libraries'])} libraries for {target_os}.")
        return dependencies

    def check_compatibility(self, source_os: str, target_os: str) -> bool:
        """
        Check whether a snapshot from source_os can run on target_os.

        Args:
            source_os: The OS the snapshot was captured on.
            target_os: The OS where restoration is intended.

        Returns:
            bool: True if compatible, False otherwise.
        """
        compatible_pairs = {
            ("linux", "linux"),
            ("linux", "android"),
            ("windows", "windows"),
        }
        result = (source_os, target_os) in compatible_pairs
        print(f"[DependencyResolver] {source_os} -> {target_os}: {'compatible' if result else 'incompatible'}")
        return result
