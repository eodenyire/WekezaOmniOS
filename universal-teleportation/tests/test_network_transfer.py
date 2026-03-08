import os
import importlib.util


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODULE_PATH = os.path.join(BASE_DIR, "transfer-layer", "network_transfer_engine.py")


def load_module(name, path):
	spec = importlib.util.spec_from_file_location(name, path)
	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)
	return module


network_transfer_engine = load_module("network_transfer_engine", MODULE_PATH)


def test_local_transfer_file(tmp_path):
	engine = network_transfer_engine.LocalTransferEngine()
	src = tmp_path / "src.tar.gz"
	dst = tmp_path / "dst.tar.gz"
	src.write_bytes(b"snapshot-data" * 100)

	success, stats = engine.transfer_file(str(src), str(dst))
	assert success is True
	assert dst.exists()
	assert stats.get("success") is True


def test_manifest_for_directory(tmp_path):
	transfer = network_transfer_engine.ManifestTransfer()
	root = tmp_path / "artifact"
	root.mkdir()
	(root / "a.bin").write_bytes(b"abc")
	(root / "b.txt").write_text("hello", encoding="utf-8")

	manifest = transfer.create_manifest(str(root))
	assert "files" in manifest
	assert len(manifest["files"]) == 2

	out = tmp_path / "manifest.json"
	path = transfer.save_manifest(manifest, str(out))
	assert os.path.exists(path)

