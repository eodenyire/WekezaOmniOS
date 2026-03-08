"""API routes for Universal Teleportation (Phase 1 + Phase 2)."""

import importlib.util
import os
import sys
import datetime
from fastapi import APIRouter, HTTPException
from models import (
    TeleportRequest,
    TeleportResponse,
    CaptureRequest,
    SnapshotRequest,
    RestoreRequest,
    TeleportStatus,
    NodeRegisterRequest,
    NodeRegisterResponse,
    RemoteTeleportRequest,
    RemoteTeleportResponse,
    ContainerCheckpointRequest,
    ContainerCheckpointResponse,
    ContainerRestoreRequest,
    ContainerRestoreResponse,
    ContainerTeleportRequest,
    ContainerTeleportResponse,
)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


capture_manager_module = load_module(
    "capture_manager", os.path.join(BASE_DIR, "state-capture", "capture_manager.py")
)
snapshot_builder_module = load_module(
    "snapshot_builder", os.path.join(BASE_DIR, "snapshot-engine", "snapshot_builder.py")
)
restore_manager_module = load_module(
    "restore_manager", os.path.join(BASE_DIR, "state-reconstruction", "restore_manager.py")
)
node_controller_module = load_module("node_controller", os.path.join(CURRENT_DIR, "node_controller.py"))
teleport_controller_module = load_module("teleport_controller", os.path.join(CURRENT_DIR, "teleport_controller.py"))

CaptureManager = capture_manager_module.CaptureManager
build_snapshot = snapshot_builder_module.build_snapshot
RestoreManager = restore_manager_module.RestoreManager
NodeController = node_controller_module.NodeController
TeleportController = teleport_controller_module.TeleportController

router = APIRouter()


@router.get("/status", response_model=TeleportStatus, tags=["System"])
def get_engine_status():
    dirs_ok = all(os.path.exists(d) for d in ["./snapshots", "./logs", "./temp"])
    status_msg = "WekezaOmniOS UAT Engine is ready"
    return TeleportStatus(
        status="online" if dirs_ok else "degraded",
        message=status_msg,
        engine_load=0.2,
    )


@router.post("/capture", tags=["Process Control"])
def capture_process_endpoint(request: CaptureRequest):
    try:
        manager = CaptureManager(snapshot_dir="./snapshots")
        info = manager.capture_process(request.pid)
        return {"status": "success", "pid": request.pid, "info": info}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Capture failed: {e}")


@router.post("/snapshot", tags=["Process Control"])
def create_snapshot(request: SnapshotRequest):
    name = request.snapshot_name or f"snapshot_pid_{request.pid}"
    try:
        snapshot_dir = f"./snapshots/process_{request.pid}"
        output_file = f"./snapshots/{name}.tar.gz"
        metadata = {
            "process_id": request.pid,
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "snapshot_name": name,
        }
        success = build_snapshot(snapshot_dir, output_file, metadata)
        if not success:
            raise HTTPException(status_code=500, detail="Snapshot creation failed")
        return {"status": "success", "snapshot": name, "file": output_file}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Snapshot failed: {e}")


@router.post("/restore", tags=["Process Control"])
def restore_process_endpoint(request: RestoreRequest):
    try:
        parts = request.snapshot_name.split("_")
        pid = None
        if "pid" in parts:
            pid_index = parts.index("pid") + 1
            pid = int(parts[pid_index])
        if pid is None:
            import re
            numbers = re.findall(r"\d+", request.snapshot_name)
            if not numbers:
                raise ValueError("Cannot extract PID from snapshot name")
            pid = int(numbers[0])

        manager = RestoreManager(snapshot_dir="./snapshots")
        manager.restore_snapshot(pid)
        return {"status": "success", "snapshot": request.snapshot_name, "pid": pid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Restore failed: {e}")


@router.post("/teleport", response_model=TeleportResponse, tags=["Orchestration"])
def teleport_process(request: TeleportRequest):
    try:
        manager = CaptureManager(snapshot_dir="./snapshots")
        manager.capture_process(request.process_id)
        snapshot_dir = f"./snapshots/process_{request.process_id}"
        snapshot_name = f"teleport_{request.process_id}_{datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        output_file = f"./snapshots/{snapshot_name}.tar.gz"
        metadata = {
            "process_id": request.process_id,
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "source_env": request.source_env,
            "target_env": request.target_env,
            "snapshot_name": snapshot_name,
        }
        build_snapshot(snapshot_dir, output_file, metadata)
        return TeleportResponse(
            status="success",
            message=f"Process {request.process_id} teleportation completed. Snapshot: {snapshot_name}",
            tracking_id=f"UAT-{request.process_id}-{datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        )
    except Exception as e:
        return TeleportResponse(status="failed", message=f"Teleportation failed: {e}", tracking_id=None)


# -------- Phase 2: Cluster and Cross-Node Endpoints --------

@router.post("/nodes/register", response_model=NodeRegisterResponse, tags=["Cluster"])
def register_node(request: NodeRegisterRequest):
    try:
        controller = NodeController()
        node = controller.register(request.node_id, request.address, role=request.role, port=request.port)
        return NodeRegisterResponse(status="success", node=node)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Node registration failed: {e}")


@router.get("/nodes", tags=["Cluster"])
def list_nodes(only_online: bool = False):
    try:
        controller = NodeController()
        nodes = controller.list_nodes(only_online=only_online)
        return {"status": "success", "count": len(nodes), "nodes": nodes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"List nodes failed: {e}")


@router.get("/nodes/health", tags=["Cluster"])
def cluster_health():
    try:
        controller = NodeController()
        health = controller.health_all()
        return {"status": "success", "health": health}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {e}")


@router.post("/teleport/remote", response_model=RemoteTeleportResponse, tags=["Cross-Node"])
def teleport_remote(request: RemoteTeleportRequest):
    try:
        controller = TeleportController()
        result = controller.teleport_remote(
            process_id=request.process_id,
            target_node_id=request.target_node_id,
            protocol=request.protocol,
        )
        return RemoteTeleportResponse(
            status=result["status"],
            tracking_id=result["tracking_id"],
            target_node_id=result["target_node_id"],
            transfer_protocol=result["transfer_protocol"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Remote teleport failed: {e}")


# -------- Phase 3: Container Runtime Integration --------

@router.post("/container/checkpoint", response_model=ContainerCheckpointResponse, tags=["Containers"])
def checkpoint_container(request: ContainerCheckpointRequest):
    try:
        controller = TeleportController()
        result = controller.checkpoint_container(
            container_id=request.container_id,
            runtime=request.runtime,
            checkpoint_name=request.checkpoint_name,
        )
        return ContainerCheckpointResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Container checkpoint failed: {e}")


@router.post("/container/restore", response_model=ContainerRestoreResponse, tags=["Containers"])
def restore_container(request: ContainerRestoreRequest):
    try:
        controller = TeleportController()
        result = controller.restore_container(
            container_id=request.container_id,
            runtime=request.runtime,
            checkpoint_name=request.checkpoint_name,
            target_node_id=request.target_node_id,
        )
        return ContainerRestoreResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Container restore failed: {e}")


@router.post("/teleport/container", response_model=ContainerTeleportResponse, tags=["Containers"])
def teleport_container(request: ContainerTeleportRequest):
    try:
        controller = TeleportController()
        result = controller.teleport_container(
            container_id=request.container_id,
            target_node_id=request.target_node_id,
            protocol=request.protocol,
            runtime=request.runtime,
            checkpoint_name=request.checkpoint_name,
        )
        return ContainerTeleportResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Container teleport failed: {e}")
