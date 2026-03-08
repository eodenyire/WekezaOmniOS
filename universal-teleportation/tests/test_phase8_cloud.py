"""
WekezaOmniOS Phase 8 Tests — Cloud Teleportation
"""
import pytest
from cloud_adapters.aws_adapter import AWSAdapter
from cloud_adapters.gcp_adapter import GCPAdapter
from cloud_adapters.azure_adapter import AzureAdapter
from cloud_adapters.cloud_teleporter import CloudTeleporter


# ------ AWS ------

def test_aws_provision_node():
    aws = AWSAdapter()
    node = aws.provision_node()
    assert "instance_id" in node
    assert node["state"] == "running"


def test_aws_list_nodes():
    aws = AWSAdapter()
    aws.provision_node()
    assert len(aws.list_nodes()) == 1


def test_aws_upload_snapshot(tmp_path):
    snap = tmp_path / "snapshot.tar.gz"
    snap.write_bytes(b"data")
    aws = AWSAdapter()
    uri = aws.upload_snapshot(str(snap), "snap-001")
    assert uri.startswith("s3://")
    assert "snap-001" in uri


def test_aws_teleport(tmp_path):
    snap = tmp_path / "snapshot.tar.gz"
    snap.write_bytes(b"data")
    aws = AWSAdapter()
    result = aws.teleport(str(snap))
    assert "node" in result
    assert "snapshot_id" in result
    assert result["node"]["state"] == "running"


# ------ GCP ------

def test_gcp_provision_node():
    gcp = GCPAdapter()
    node = gcp.provision_node()
    assert "name" in node
    assert node["status"] == "RUNNING"


def test_gcp_teleport(tmp_path):
    snap = tmp_path / "snapshot.tar.gz"
    snap.write_bytes(b"data")
    gcp = GCPAdapter()
    result = gcp.teleport(str(snap))
    assert "node" in result
    assert "gcs_uri" in result


# ------ Azure ------

def test_azure_provision_node():
    azure = AzureAdapter()
    vm = azure.provision_node()
    assert "name" in vm
    assert "running" in vm["power_state"]


def test_azure_teleport(tmp_path):
    snap = tmp_path / "snapshot.tar.gz"
    snap.write_bytes(b"data")
    azure = AzureAdapter()
    result = azure.teleport(str(snap))
    assert "node" in result
    assert "blob_url" in result


# ------ Cloud Teleporter ------

def test_cloud_teleporter_aws(tmp_path):
    snap = tmp_path / "snapshot.tar.gz"
    snap.write_bytes(b"data")
    t = CloudTeleporter(provider="aws")
    result = t.teleport(str(snap))
    assert result["provider"] == "aws"


def test_cloud_teleporter_gcp(tmp_path):
    snap = tmp_path / "snapshot.tar.gz"
    snap.write_bytes(b"data")
    t = CloudTeleporter(provider="gcp")
    result = t.teleport(str(snap))
    assert result["provider"] == "gcp"


def test_cloud_teleporter_azure(tmp_path):
    snap = tmp_path / "snapshot.tar.gz"
    snap.write_bytes(b"data")
    t = CloudTeleporter(provider="azure")
    result = t.teleport(str(snap))
    assert result["provider"] == "azure"


def test_cloud_teleporter_unsupported_raises():
    with pytest.raises(ValueError, match="Unknown provider"):
        CloudTeleporter(provider="oracle")


def test_cloud_teleporter_supported_providers():
    t = CloudTeleporter(provider="aws")
    providers = t.supported_providers()
    assert "aws" in providers
    assert "gcp" in providers
    assert "azure" in providers
