"""Encryption manager for secure snapshot transfer in Phase 2."""

import base64
import hashlib
import os

try:
    from cryptography.fernet import Fernet
except Exception:
    Fernet = None


class EncryptionManager:
    def __init__(self, key_path="configs/.encryption.key"):
        self.key_path = key_path
        os.makedirs(os.path.dirname(self.key_path), exist_ok=True)
        self.key = self._load_or_create_key()
        self.cipher = Fernet(self.key) if Fernet else None

    def _load_or_create_key(self):
        if os.path.exists(self.key_path):
            with open(self.key_path, "rb") as f:
                return f.read().strip()
        if Fernet:
            key = Fernet.generate_key()
        else:
            # Fallback key material when cryptography isn't available.
            key = base64.urlsafe_b64encode(os.urandom(32))
        with open(self.key_path, "wb") as f:
            f.write(key)
        return key

    def encrypt(self, data):
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("data must be bytes")
        if self.cipher:
            return self.cipher.encrypt(data)
        # Weak fallback obfuscation for environments without cryptography.
        return base64.urlsafe_b64encode(data)

    def decrypt(self, data):
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("data must be bytes")
        if self.cipher:
            return self.cipher.decrypt(data)
        return base64.urlsafe_b64decode(data)

    def sha256(self, data):
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("data must be bytes")
        return hashlib.sha256(data).hexdigest()
