import os
import importlib.util


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODULE_PATH = os.path.join(BASE_DIR, "security", "encryption.py")


def load_module(name, path):
	spec = importlib.util.spec_from_file_location(name, path)
	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)
	return module


encryption_module = load_module("encryption", MODULE_PATH)


def test_encrypt_decrypt_roundtrip(tmp_path):
	key_path = tmp_path / ".key"
	manager = encryption_module.EncryptionManager(key_path=str(key_path))
	payload = b"phase2-secret-payload"
	encrypted = manager.encrypt(payload)
	decrypted = manager.decrypt(encrypted)
	assert decrypted == payload


def test_sha256_changes_with_data(tmp_path):
	manager = encryption_module.EncryptionManager(key_path=str(tmp_path / ".key2"))
	h1 = manager.sha256(b"data-a")
	h2 = manager.sha256(b"data-b")
	assert h1 != h2


def test_encrypt_decrypt_default_key():
	manager = encryption_module.EncryptionManager()
	data = b"hello"
	encrypted = manager.encrypt(data)
	decrypted = manager.decrypt(encrypted)
	assert decrypted == data
