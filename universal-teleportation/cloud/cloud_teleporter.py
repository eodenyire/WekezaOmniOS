"""
WekezaOmniOS Cloud Teleporter
Phase 8: High-level orchestrator that dispatches workloads to the correct
         cloud provider (AWS, GCP, Azure) based on configuration.
"""
from .aws_adapter import AWSAdapter
from .gcp_adapter import GCPAdapter
from .azure_adapter import AzureAdapter


PROVIDER_MAP = {
    "aws": AWSAdapter,
    "gcp": GCPAdapter,
    "azure": AzureAdapter,
}


class CloudTeleporter:
    """
    Unified cloud teleportation interface.

    Usage::

        teleporter = CloudTeleporter(provider="aws")
        result = teleporter.teleport("/path/to/snapshot.tar.gz")
    """

    def __init__(self, provider: str = "aws", **kwargs):
        """
        Args:
            provider: Cloud provider key — 'aws', 'gcp', or 'azure'.
            **kwargs: Passed directly to the provider adapter constructor.
        """
        key = provider.lower()
        cls = PROVIDER_MAP.get(key)
        if cls is None:
            raise ValueError(
                f"[CloudTeleporter] Unknown provider '{provider}'. "
                f"Supported: {list(PROVIDER_MAP.keys())}"
            )
        self.provider = key
        self.adapter = cls(**kwargs)
        print(f"[CloudTeleporter] Initialized with provider: {provider.upper()}")

    def teleport(self, snapshot_path: str, **kwargs) -> dict:
        """
        Teleport a snapshot to the configured cloud provider.

        Args:
            snapshot_path: Local path to the snapshot archive.
            **kwargs: Provider-specific options (e.g., instance_type, vm_size).

        Returns:
            dict with provider-specific result metadata.
        """
        print(f"[CloudTeleporter] Starting cloud teleportation via {self.provider.upper()}...")
        result = self.adapter.teleport(snapshot_path, **kwargs)
        result["provider"] = self.provider
        return result

    def list_nodes(self) -> list:
        """List all provisioned cloud nodes for the current provider."""
        return self.adapter.list_nodes()

    def supported_providers(self) -> list:
        """Return the list of supported cloud providers."""
        return list(PROVIDER_MAP.keys())
