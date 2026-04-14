"""
OS Launcher routes — launch, list, and terminate desktop OS sessions.
"""

from fastapi import APIRouter, Depends, HTTPException

from ..schemas.models import (
    LaunchSessionRequest,
    SessionResponse,
    SessionStatusResponse,
    TerminateSessionRequest,
)
from ..middleware.auth_middleware import get_current_user_id

router = APIRouter(prefix="/sessions", tags=["OS Launcher"])

# Populated by server.py after the ControlPlane is initialised
_os_launcher = None


def set_os_launcher(launcher) -> None:
    global _os_launcher
    _os_launcher = launcher


def _get_launcher():
    if _os_launcher is None:
        raise HTTPException(status_code=503, detail="OS launcher not initialised")
    return _os_launcher


@router.post("/launch", response_model=SessionResponse, status_code=201)
def launch_session(request: LaunchSessionRequest,
                   _uid: str = Depends(get_current_user_id)):
    """Launch a new cloud desktop OS session."""
    launcher = _get_launcher()
    try:
        session = launcher.launch(
            user_id=request.user_id,
            os_profile=request.os_profile,
            cpu_cores=request.cpu_cores,
            ram_gb=request.ram_gb,
        )
        return session
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))


@router.get("", summary="List active sessions")
def list_sessions(user_id: str = None, _uid: str = Depends(get_current_user_id)):
    """Return all active sessions, optionally filtered by user_id."""
    launcher = _get_launcher()
    sessions = launcher.list_sessions(user_id=user_id)
    return {"status": "ok", "count": len(sessions), "sessions": sessions}


@router.get("/{session_id}", summary="Get session details")
def get_session(session_id: str, _uid: str = Depends(get_current_user_id)):
    launcher = _get_launcher()
    session = launcher.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail=f"Session not found: {session_id}")
    return session


@router.delete("/{session_id}", response_model=SessionStatusResponse)
def terminate_session(session_id: str, _uid: str = Depends(get_current_user_id)):
    """Terminate a running desktop session."""
    launcher = _get_launcher()
    result = launcher.terminate(session_id)
    return {"status": result.get("status", "ok"), "session_id": session_id}
