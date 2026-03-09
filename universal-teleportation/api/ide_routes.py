"""API routes for the WekezaOmniOS inbuilt Developer IDE."""

from __future__ import annotations

import datetime
import json
import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

# Lock IDE actions to the project subtree.
IDE_ROOT = Path("/workspaces/WekezaOmniOS/universal-teleportation").resolve()

router = APIRouter(prefix="/developer", tags=["Developer IDE"])


class FileContent(BaseModel):
    path: str
    content: str


class FilePath(BaseModel):
    path: str


class CodeExecutionRequest(BaseModel):
    language: str = Field(..., description="python|javascript|bash|c|cpp|java")
    code: str
    args: List[str] = Field(default_factory=list)
    timeout_seconds: int = Field(default=15, ge=1, le=120)


class DeployRequest(BaseModel):
    file_path: str = Field(..., description="Workspace-relative file path to deploy")
    app_name: str = Field(default="developer-app")
    environment: str = Field(default="production", description="preview|staging|production")
    process_id: int | None = Field(default=None, description="Optional active process id to prefill in console")


def _resolve_inside_root(user_path: str) -> Path:
    candidate = (IDE_ROOT / user_path).resolve()
    if candidate != IDE_ROOT and IDE_ROOT not in candidate.parents:
        raise HTTPException(status_code=400, detail="Path escapes IDE root")
    return candidate


def _run_command(command: list[str], cwd: Path, timeout_seconds: int) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(
            command,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise HTTPException(
            status_code=408,
            detail={
                "status": "timeout",
                "command": command,
                "stdout": exc.stdout or "",
                "stderr": exc.stderr or "",
            },
        )


def _slugify(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9_-]+", "-", value.strip().lower())
    return value.strip("-") or "app"


@router.get("", response_class=HTMLResponse, include_in_schema=False)
def developer_ui():
    ui_path = Path(__file__).resolve().parent / "developer.html"
    if not ui_path.exists():
        raise HTTPException(status_code=404, detail="Developer UI not found")
    return ui_path.read_text(encoding="utf-8")


@router.get("/files/list")
def list_files(path: str = "."):
    target_path = _resolve_inside_root(path)
    if not target_path.exists() or not target_path.is_dir():
        raise HTTPException(status_code=404, detail="Directory not found")

    items = []
    for item in sorted(target_path.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower())):
        items.append(
            {
                "name": item.name,
                "path": str(item.relative_to(IDE_ROOT)),
                "is_dir": item.is_dir(),
            }
        )
    return {"status": "success", "items": items}


@router.get("/files/read")
def read_file(path: str):
    target_path = _resolve_inside_root(path)
    if not target_path.exists() or target_path.is_dir():
        raise HTTPException(status_code=404, detail="File not found")

    return {
        "status": "success",
        "path": str(target_path.relative_to(IDE_ROOT)),
        "content": target_path.read_text(encoding="utf-8"),
    }


@router.post("/files/write")
def write_file(file_data: FileContent):
    target_path = _resolve_inside_root(file_data.path)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(file_data.content, encoding="utf-8")
    return {"status": "success", "message": f"File '{file_data.path}' saved."}


@router.post("/files/create")
def create_file(file_path: FilePath):
    target_path = _resolve_inside_root(file_path.path)
    if target_path.exists():
        raise HTTPException(status_code=400, detail="File already exists")

    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.touch()
    return {"status": "success", "message": f"File '{file_path.path}' created."}


@router.post("/files/create_dir")
def create_directory(file_path: FilePath):
    target_path = _resolve_inside_root(file_path.path)
    if target_path.exists():
        raise HTTPException(status_code=400, detail="Directory already exists")

    target_path.mkdir(parents=True, exist_ok=True)
    return {"status": "success", "message": f"Directory '{file_path.path}' created."}


@router.post("/run")
def run_code(request: CodeExecutionRequest):
    lang = request.language.strip().lower()
    start = time.time()

    language_map = {
        "python": {"ext": ".py", "runner": "python3"},
        "javascript": {"ext": ".js", "runner": "node"},
        "node": {"ext": ".js", "runner": "node"},
        "bash": {"ext": ".sh", "runner": "bash"},
        "sh": {"ext": ".sh", "runner": "bash"},
        "c": {"ext": ".c", "compiler": "gcc"},
        "cpp": {"ext": ".cpp", "compiler": "g++"},
        "c++": {"ext": ".cpp", "compiler": "g++"},
        "java": {"ext": ".java", "compiler": "javac", "runner": "java"},
    }

    if lang not in language_map:
        raise HTTPException(status_code=400, detail=f"Unsupported language: {request.language}")

    config = language_map[lang]
    with tempfile.TemporaryDirectory(prefix="wekeza-ide-") as temp_dir:
        temp_path = Path(temp_dir)
        source_path = temp_path / f"Main{config['ext']}"
        source_path.write_text(request.code, encoding="utf-8")

        compile_output = ""
        if "compiler" in config:
            compiler = config["compiler"]
            if shutil.which(compiler) is None:
                raise HTTPException(status_code=400, detail=f"Compiler not available: {compiler}")

            if lang in ("c",):
                binary_path = temp_path / "main"
                compile_cmd = [compiler, str(source_path), "-o", str(binary_path)]
                compile_result = _run_command(compile_cmd, temp_path, request.timeout_seconds)
                compile_output = (compile_result.stdout or "") + (compile_result.stderr or "")
                if compile_result.returncode != 0:
                    return {
                        "status": "compile_error",
                        "language": lang,
                        "command": compile_cmd,
                        "compile_output": compile_output,
                        "exit_code": compile_result.returncode,
                        "duration_ms": int((time.time() - start) * 1000),
                    }
                run_cmd = [str(binary_path)] + request.args

            elif lang in ("cpp", "c++"):
                binary_path = temp_path / "main"
                compile_cmd = [compiler, str(source_path), "-o", str(binary_path)]
                compile_result = _run_command(compile_cmd, temp_path, request.timeout_seconds)
                compile_output = (compile_result.stdout or "") + (compile_result.stderr or "")
                if compile_result.returncode != 0:
                    return {
                        "status": "compile_error",
                        "language": lang,
                        "command": compile_cmd,
                        "compile_output": compile_output,
                        "exit_code": compile_result.returncode,
                        "duration_ms": int((time.time() - start) * 1000),
                    }
                run_cmd = [str(binary_path)] + request.args

            else:  # java
                compile_cmd = [compiler, str(source_path)]
                compile_result = _run_command(compile_cmd, temp_path, request.timeout_seconds)
                compile_output = (compile_result.stdout or "") + (compile_result.stderr or "")
                if compile_result.returncode != 0:
                    return {
                        "status": "compile_error",
                        "language": lang,
                        "command": compile_cmd,
                        "compile_output": compile_output,
                        "exit_code": compile_result.returncode,
                        "duration_ms": int((time.time() - start) * 1000),
                    }
                if shutil.which("java") is None:
                    raise HTTPException(status_code=400, detail="Runtime not available: java")
                run_cmd = ["java", "Main"] + request.args

        else:
            runner = config["runner"]
            if shutil.which(runner) is None:
                raise HTTPException(status_code=400, detail=f"Runtime not available: {runner}")
            run_cmd = [runner, str(source_path)] + request.args

        run_result = _run_command(run_cmd, temp_path, request.timeout_seconds)
        return {
            "status": "success" if run_result.returncode == 0 else "runtime_error",
            "language": lang,
            "command": run_cmd,
            "compile_output": compile_output,
            "stdout": run_result.stdout,
            "stderr": run_result.stderr,
            "exit_code": run_result.returncode,
            "duration_ms": int((time.time() - start) * 1000),
        }


@router.post("/deploy")
def deploy_to_environment(request: DeployRequest):
    target_file = _resolve_inside_root(request.file_path)
    if not target_file.exists() or target_file.is_dir():
        raise HTTPException(status_code=404, detail="Deploy target file not found")

    app_slug = _slugify(request.app_name)
    env_slug = _slugify(request.environment)
    deployment_id = f"dep-{datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')}"

    extension = target_file.suffix.lower()
    runtime_map = {
        ".py": "python",
        ".js": "javascript",
        ".sh": "bash",
        ".c": "c",
        ".cpp": "cpp",
        ".java": "java",
    }
    runtime = runtime_map.get(extension, "generic")
    target_role = "cloud-runtime"
    target_os = "linux"
    target_node_id = f"{app_slug}-prod-node"

    deployment_record = {
        "deployment_id": deployment_id,
        "app_name": request.app_name,
        "environment": request.environment,
        "runtime": runtime,
        "process_id": request.process_id,
        "target_role": target_role,
        "target_os": target_os,
        "target_node_id": target_node_id,
        "file_path": str(target_file.relative_to(IDE_ROOT)),
        "created_at": datetime.datetime.utcnow().isoformat() + "Z",
    }

    deployment_dir = IDE_ROOT / "temp" / "deployments"
    deployment_dir.mkdir(parents=True, exist_ok=True)
    (deployment_dir / f"{deployment_id}.json").write_text(
        json.dumps(deployment_record, indent=2), encoding="utf-8"
    )

    production_url = f"https://{app_slug}.{env_slug}.wekeza.local/{deployment_id}"
    pid_query = f"&process_id={request.process_id}" if request.process_id is not None else ""
    console_url = (
        f"/console?deployment_id={deployment_id}"
        f"&app={app_slug}"
        f"&runtime={runtime}"
        f"{pid_query}"
        f"&target_role={target_role}"
        f"&target_os={target_os}"
        f"&target_node_id={target_node_id}"
    )

    return {
        "status": "success",
        "message": "Deployment prepared. Use console link to teleport this workload.",
        "deployment_id": deployment_id,
        "runtime": runtime,
        "process_id": request.process_id,
        "target_role": target_role,
        "target_os": target_os,
        "target_node_id": target_node_id,
        "production_url": production_url,
        "console_url": console_url,
        "record_path": str((deployment_dir / f"{deployment_id}.json").relative_to(IDE_ROOT)),
    }
