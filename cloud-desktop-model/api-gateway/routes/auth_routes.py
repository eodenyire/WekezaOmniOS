"""
Auth routes — register, login, logout, and profile.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ..schemas.models import LoginRequest, RegisterRequest, TokenResponse, UserProfile
from ..controllers.auth_controller import AuthController

router = APIRouter(prefix="/auth", tags=["Authentication"])
_auth = AuthController()
_bearer = HTTPBearer(auto_error=False)


@router.post("/register", response_model=UserProfile, status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest):
    """Create a new user account."""
    try:
        user = _auth.register(
            username=request.username,
            password=request.password,
            email=request.email,
        )
        return user
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest):
    """Authenticate and receive a bearer token."""
    try:
        return _auth.login(request.username, request.password)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )


@router.post("/logout")
def logout(credentials: HTTPAuthorizationCredentials = Depends(_bearer)):
    """Revoke the current bearer token."""
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No token provided")
    revoked = _auth.logout(credentials.credentials)
    return {"status": "ok" if revoked else "token_not_found"}


@router.get("/me", response_model=UserProfile)
def get_profile(credentials: HTTPAuthorizationCredentials = Depends(_bearer)):
    """Return the profile of the authenticated user."""
    from ..middleware.auth_middleware import _active_tokens
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    user_id = _active_tokens.get(credentials.credentials)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    profile = _auth.get_profile(user_id)
    if profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return profile
