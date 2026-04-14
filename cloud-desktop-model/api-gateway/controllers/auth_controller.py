"""
Auth Controller — handles user registration, login, and logout.
Uses an in-memory store with bcrypt-style hashing (hashlib PBKDF2).
"""

import datetime
import hashlib
import os
import secrets
import threading
from typing import Optional

from ..middleware.auth_middleware import register_token, revoke_token


class AuthController:
    """Simple auth controller backed by an in-memory user registry."""

    def __init__(self):
        self._users: dict[str, dict] = {}
        self._tokens: dict[str, str] = {}  # token → user_id
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _hash_password(self, password: str, salt: str) -> str:
        dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 260_000)
        return dk.hex()

    def _make_token(self) -> str:
        return secrets.token_urlsafe(32)

    def _make_user_id(self, username: str) -> str:
        return f"usr-{hashlib.sha256(username.encode()).hexdigest()[:12]}"

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def register(self, username: str, password: str,
                 email: Optional[str] = None) -> dict:
        with self._lock:
            if username in self._users:
                raise ValueError(f"Username already taken: {username!r}")
            salt = secrets.token_hex(16)
            user_id = self._make_user_id(username)
            self._users[username] = {
                "user_id": user_id,
                "username": username,
                "email": email,
                "password_hash": self._hash_password(password, salt),
                "salt": salt,
                "created_at": datetime.datetime.utcnow().isoformat() + "Z",
            }
        return {"user_id": user_id, "username": username, "email": email,
                "created_at": self._users[username]["created_at"]}

    def login(self, username: str, password: str) -> dict:
        with self._lock:
            user = self._users.get(username)
            if user is None:
                raise ValueError("Invalid credentials")
            expected = self._hash_password(password, user["salt"])
            if not secrets.compare_digest(expected, user["password_hash"]):
                raise ValueError("Invalid credentials")
            token = self._make_token()
            self._tokens[token] = user["user_id"]
            register_token(token, user["user_id"])
        return {
            "access_token": token,
            "token_type": "bearer",
            "user_id": user["user_id"],
            "username": username,
        }

    def logout(self, token: str) -> bool:
        with self._lock:
            user_id = self._tokens.pop(token, None)
            if user_id is None:
                return False
            revoke_token(token)
        return True

    def get_profile(self, user_id: str) -> Optional[dict]:
        with self._lock:
            for u in self._users.values():
                if u["user_id"] == user_id:
                    return {k: v for k, v in u.items()
                            if k not in ("password_hash", "salt")}
        return None
