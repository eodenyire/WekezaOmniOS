"""
Auth Middleware — lightweight bearer-token validator for the Cloud Desktop
API Gateway.  In production this would verify JWT signatures; here it
validates tokens against the in-memory user store managed by AuthController.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

_bearer = HTTPBearer(auto_error=True)

# Shared token → user_id map, populated by AuthController
_active_tokens: dict[str, str] = {}


def register_token(token: str, user_id: str) -> None:
    _active_tokens[token] = user_id


def revoke_token(token: str) -> None:
    _active_tokens.pop(token, None)


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
) -> str:
    token = credentials.credentials
    user_id = _active_tokens.get(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_id
